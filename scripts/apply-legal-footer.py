#!/usr/bin/env python3
"""Add sober legal footer block (P.IVA) before vct-foot-bottom on all pages."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LEGAL = (
    '<div class="vct-legal"><p>'
    'Editore: Maurizio Piraino P.IVA 14597560961 · <a href="mailto:info@valorecasatua.it">info@valorecasatua.it</a>'
    "</p></div>\n"
)

MARKER = '<div class="vct-foot-bottom">'


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "vct-legal" in text:
        return False
    if MARKER not in text:
        print(f"SKIP (no footer): {path.relative_to(ROOT)}")
        return False
    path.write_text(text.replace(MARKER, LEGAL + MARKER, 1), encoding="utf-8")
    return True


def main() -> None:
    n = 0
    for html in sorted(ROOT.rglob("*.html")):
        if process(html):
            n += 1
            print(html.relative_to(ROOT))
    print(f"\nUpdated {n} files.")


if __name__ == "__main__":
    main()
