from pathlib import Path


TEXT_EXTENSIONS = {
    ".py",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
    ".go",
    ".rs",
    ".kt",
}


def count_lines(directory: Path):

    total = 0

    for file in directory.rglob("*"):

        if not file.is_file():
            continue

        if file.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        try:

            with file.open(
                encoding="utf-8",
                errors="ignore"
            ) as f:

                total += sum(1 for _ in f)

        except Exception:

            pass

    return total