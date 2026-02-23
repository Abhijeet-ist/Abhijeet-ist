#!/bin/bash
# ⒸAngelaMos | 2025 | CertGames.com

set -e

echo "Starting LOC counting process..."

WORKSPACE_DIR="$(pwd)"
REPOS_JSON="$WORKSPACE_DIR/scripts/repos.json"
OUTPUT_FILE="$WORKSPACE_DIR/loc-data.json"
TEMP_DIR=$(mktemp -d)

echo "Workspace: $WORKSPACE_DIR"
echo "Temporary directory: $TEMP_DIR"

# Require a GitHub token to access private repositories
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN is not set. A personal access token with 'repo' scope is required."
    exit 1
fi

# Fetch all repos (public + private) owned by the authenticated user via GitHub API
echo "Fetching repository list from GitHub API..."
ALL_REPOS=()
PAGE=1
while true; do
    RESPONSE=$(curl -s \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github+json" \
        "https://api.github.com/user/repos?per_page=100&page=${PAGE}&type=owner")

    # Check if response is a JSON array; if not, it's an API error
    IS_ARRAY=$(echo "$RESPONSE" | jq -r 'if type == "array" then "yes" else "no" end' 2>/dev/null || echo "no")
    if [ "$IS_ARRAY" != "yes" ]; then
        ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // "Unknown error"' 2>/dev/null || echo "Invalid response")
        echo "Error: GitHub API returned an error: $ERROR_MSG"
        echo "Make sure the GH_PAT secret is set and has the 'repo' scope."
        exit 1
    fi

    REPOS_ON_PAGE=$(echo "$RESPONSE" | jq -r '.[].full_name // empty')

    if [ -z "$REPOS_ON_PAGE" ]; then
        break
    fi

    while IFS= read -r repo; do
        ALL_REPOS+=("$repo")
    done <<< "$REPOS_ON_PAGE"

    COUNT=$(echo "$RESPONSE" | jq '. | length')
    if [ "$COUNT" -lt 100 ]; then
        break
    fi

    PAGE=$((PAGE + 1))
done

echo "Found ${#ALL_REPOS[@]} repositories (public + private)."

cd "$TEMP_DIR"

echo "Cloning repositories..."
for repo in "${ALL_REPOS[@]}"; do
    echo "  Cloning $repo..."
    git clone --depth 1 "https://${GITHUB_TOKEN}@github.com/${repo}.git" "$(basename "$repo")" 2>/dev/null \
        || echo "  Warning: Failed to clone $repo, skipping."
done

echo "Running tokei to count lines of code..."
tokei . --output json --exclude '*.md,*.txt,README*,LICENSE*' > "$OUTPUT_FILE"

echo "Cleaning up temporary directory..."
cd "$WORKSPACE_DIR"
rm -rf "$TEMP_DIR"

echo "LOC counting complete! Results saved to $OUTPUT_FILE"

cat "$OUTPUT_FILE" | jq '.'