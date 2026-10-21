#!/usr/bin/env python3
"""Apply recommended SEO fixes across all HTML pages."""

import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://valorecasatua.it"
OG_IMAGE = f"{BASE}/assets/og-valorecasatua.jpg"
AI_META = (
    '<meta name="GPTBot" content="index, follow">'
    '<meta name="ClaudeBot" content="index, follow">'
    '<meta name="PerplexityBot" content="index, follow">'
    '<meta name="Google-Extended" content="index, follow">'
)
NOINDEX_SLUGS = {"cookie", "privacy", "grazie-checklist"}


def canonical_url(text: str) -> Optional[str]:
    m = re.search(r'<link rel="canonical" href="([^"]+)"', text)
    return m.group(1) if m else None


def is_noindex(text: str) -> bool:
    head = text.split("</head>")[0] if "</head>" in text else text[:8000]
    return bool(re.search(r'name="robots"[^>]*content="[^"]*noindex', head, re.I))


def abs_schema_urls(text: str) -> str:
    """Turn relative schema.org paths into absolute URLs."""

    def repl(m: re.Match) -> str:
        val = m.group(1)
        if val.startswith("http"):
            return m.group(0)
        key = m.group(0).split('":"')[0].strip('"')
        return f'"{key}":"{BASE}{val}"'

    text = re.sub(
        r'"(?:@id|url|logo|mainEntityOfPage|image|item)":"(/[^"]*)"',
        repl,
        text,
    )
    text = re.sub(
        r'"urlTemplate":"(/[^"]*)"',
        lambda m: f'"urlTemplate":"{BASE}{m.group(1)}"',
        text,
    )
    return text


def fix_og_twitter(text: str, canonical: Optional[str]) -> str:
    if canonical:
        text = re.sub(
            r'<meta property="og:url" content="[^"]*"',
            f'<meta property="og:url" content="{canonical}"',
            text,
            count=1,
        )

    text = re.sub(
        r'(<meta property="og:image" content=")(/[^"]+)',
        lambda m: m.group(1) + BASE + m.group(2),
        text,
    )

    head = text.split("</head>")[0]
    if 'name="twitter:card"' in head and 'name="twitter:image"' not in head:
        og = re.search(r'property="og:image" content="([^"]+)"', head)
        img = og.group(1) if og else OG_IMAGE
        if img.startswith("/"):
            img = BASE + img
        text = re.sub(
            r'(<meta name="twitter:card" content="[^"]*">)',
            rf'\1\n<meta name="twitter:image" content="{img}">',
            text,
            count=1,
        )
    return text


def ensure_ai_meta(text: str) -> str:
    if is_noindex(text) or 'name="GPTBot"' in text.split("</head>")[0]:
        return text
    if '<meta name="theme-color"' in text:
        return text.replace(
            '<meta name="theme-color"',
            AI_META + '\n<meta name="theme-color"',
            1,
        )
    return text.replace("</head>", AI_META + "\n</head>", 1)


def process_file(path: Path) -> list[str]:
    original = path.read_text(encoding="utf-8")
    text = original
    changes: list[str] = []

    canonical = canonical_url(text)
    new_text = fix_og_twitter(text, canonical)
    if new_text != text:
        changes.append("og/twitter")
        text = new_text

    new_text = abs_schema_urls(text)
    if new_text != text:
        changes.append("schema-urls")
        text = new_text

    new_text = ensure_ai_meta(text)
    if new_text != text:
        changes.append("ai-meta")
        text = new_text

    if text != original:
        path.write_text(text, encoding="utf-8")
    return changes


def main() -> None:
    updated = 0
    for html in sorted(ROOT.rglob("*.html")):
        changes = process_file(html)
        if changes:
            updated += 1
            print(f"{html.relative_to(ROOT)}: {', '.join(changes)}")
    print(f"\nUpdated {updated} files.")


if __name__ == "__main__":
    main()
