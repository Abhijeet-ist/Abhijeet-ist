#!/bin/bash

set -e

echo "Starting LOC counting process..."

WORKSPACE_DIR="$(pwd)"
REPOS_JSON="$WORKSPACE_DIR/scripts/repos.json"
OUTPUT_FILE="$WORKSPACE_DIR/loc-data.json"
TEMP_DIR=$(mktemp -d)

echo "Workspace: $WORKSPACE_DIR"
echo "Temporary directory: $TEMP_DIR"

cd "$TEMP_DIR"

echo "Cloning repositories..."
jq -r '.repos[]' "$REPOS_JSON" | while read -r repo; do
    echo "  Cloning $repo..."
    git clone --depth 1 "https://github.com/$repo.git" "$(basename $repo)" 2>/dev/null || echo "Failed to clone $repo"
done

echo "Building tokei exclusion flags from repos.json..."
# Map exclude_languages entries to glob patterns for tokei
EXCLUDE_FLAGS=" --exclude '*.txt' --exclude 'README*' --exclude 'LICENSE*' --exclude 'package-lock.json' --exclude 'yarn.lock' --exclude 'pnpm-lock.yaml'"

while IFS= read -r lang; do
    case "$(echo $lang | tr '[:upper:]' '[:lower:]')" in
        json)       EXCLUDE_FLAGS="$EXCLUDE_FLAGS --exclude '*.json'" ;;
        text)       EXCLUDE_FLAGS="$EXCLUDE_FLAGS --exclude '*.txt'" ;;
        toml)       EXCLUDE_FLAGS="$EXCLUDE_FLAGS --exclude '*.toml'" ;;
        xml)        EXCLUDE_FLAGS="$EXCLUDE_FLAGS --exclude '*.xml'" ;;
    esac
done < <(jq -r '.exclude_languages[]' "$REPOS_JSON" 2>/dev/null || true)

echo "Running tokei to count lines of code..."
eval "tokei . --output json $EXCLUDE_FLAGS" > "$OUTPUT_FILE"

echo "Cleaning up temporary directory..."
cd "$WORKSPACE_DIR"
rm -rf "$TEMP_DIR"

echo "LOC counting complete! Results saved to $OUTPUT_FILE"

cat "$OUTPUT_FILE" | jq '.'