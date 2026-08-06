#!/usr/bin/env python3
"""Generate README.md listing every image file in the repository.

Run from anywhere: `python3 scripts/generate_readme.py`. Output is
deterministic (no timestamps), so CI only commits when the gallery changes.
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

IMAGE_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif", ".tiff",
}
SKIP_DIRS = {".git", ".github", ".mimocode", "scripts", "node_modules"}

# Escape characters that break Markdown link syntax in file names.
def esc(name: str) -> str:
    return (
        name.replace(" ", "%20")
        .replace("(", "%28")
        .replace(")", "%29")
        .replace("[", "%5B")
        .replace("]", "%5D")
        .replace("|", "%7C")
    )


def find_images(root: Path) -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for f in sorted(filenames):
            if Path(f).suffix.lower() in IMAGE_EXTS:
                found.append(Path(dirpath) / f)
    return sorted(found)


GRID_COLS = 4


def build_readme(images: list[Path]) -> str:
    lines = [
        "# Wallpapers",
        "",
        f"Total: **{len(images)}** images.",
        "",
        "## Gallery",
        "",
        "|" + "|".join([""] * GRID_COLS) + "|",
        "|" + "|".join(["---"] * GRID_COLS) + "|",
    ]
    for i in range(0, len(images), GRID_COLS):
        cells = [f"![{img.stem}]({esc(img.relative_to(ROOT).as_posix())})" for img in images[i : i + GRID_COLS]]
        cells += [""] * (GRID_COLS - len(cells))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    images = find_images(ROOT)
    content = build_readme(images)
    if README.exists() and README.read_text() == content:
        print("README.md is up to date, no changes.")
        return
    README.write_text(content)
    print(f"README.md updated with {len(images)} images.")


if __name__ == "__main__":
    main()
