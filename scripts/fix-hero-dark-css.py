#!/usr/bin/env python3
"""Remove all dark-theme hero CSS from index.html."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

DARK_PATTERNS = [
    r"@media\(max-width:768px\)\{\s*\.hero-section,\s*section\.hero,\s*\.hero\s*\{[^}]*#0a3d38[^}]*\}[^}]*\}[^}]*\}[^}]*\}[^}]*\}[^}]*\}",
    r"\.hero\{color:#fff;background:radial-gradient\([^)]*#06101f[^)]*\)[^}]*\}\.hero::before[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}[^}]+\}",
]

REPLACEMENTS = [
    (
        re.compile(
            r"@media\(max-width:768px\)\{\s*"
            r"\.hero-section,\s*section\.hero,\s*\.hero\s*\{\s*"
            r"background:\s*linear-gradient\(160deg,\s*#0a3d38[^}]+\}\s*"
            r"(?:\.hero[^}]+\})+"
            r"\}",
            re.S,
        ),
        "",
    ),
    (
        ".panel-map{background:linear-gradient(135deg,#0b332f,#e9fff9 48%,#fff0bd)}",
        ".panel-map{background:linear-gradient(135deg,#dff8f4,#ffffff 52%,#f8efd6)}",
    ),
]

BUILD_MARKER = '<meta name="x-build" content="20260705-hero-light-v2">'
CSS_LINK = '<link rel="stylesheet" href="/assets/home-hero-light.css?v=20260705-hero-light">'


def strip_dark_hero_block(text: str) -> str:
    marker = "@media(max-width:768px)"
    dark = "#0a3d38"
    while marker in text and dark in text:
        start = text.find(marker)
        if start == -1:
            break
        block = text[start : start + 800]
        if dark not in block:
            break
        end = text.find("\n}", start)
        if end == -1:
            break
        end = text.find("}", end + 1) + 1
        text = text[:start] + text[end:]
    return text


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    orig = text

    text = strip_dark_hero_block(text)

    if '.hero{color:#fff;background:radial-gradient' in text and "#06101f" in text:
        i = text.find('.hero{color:#fff;background:radial-gradient')
        j = text.find(".premium-panel{", i)
        if j > i:
            text = text[:i] + text[j:]

    for old, new in REPLACEMENTS:
        if isinstance(old, str):
            text = text.replace(old, new)
        else:
            text = old.sub(new, text)

    if BUILD_MARKER not in text:
        text = text.replace("<meta charset=\"UTF-8\">", f"<meta charset=\"UTF-8\">\n{BUILD_MARKER}", 1)

    if CSS_LINK not in text:
        text = text.replace("</head>", f"{CSS_LINK}\n</head>", 1)

    if text != orig:
        INDEX.write_text(text, encoding="utf-8")
        print("index.html: dark hero CSS removed, build marker + CSS link added")
    else:
        print("index.html: already clean")

    assert "#0a3d38" not in text, "dark mobile gradient still present"
    assert CSS_LINK in text


if __name__ == "__main__":
    main()
