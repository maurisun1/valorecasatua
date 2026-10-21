#!/usr/bin/env python3
"""Sync twitter:title and twitter:description with on-page meta tags."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.I)
OG_TITLE_RE = re.compile(r'<meta\s+property="og:title"\s+content="([^"]*)"', re.I)
META_DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
TWITTER_TITLE_RE = re.compile(
    r'(<meta\s+name="twitter:title"\s+content=")([^"]*)(")',
    re.I,
)
TWITTER_DESC_RE = re.compile(
    r'(<meta\s+name="twitter:description"\s+content=")([^"]*)(")',
    re.I,
)
TWITTER_CARD_RE = re.compile(r'(<meta\s+name="twitter:card"[^>]*>)', re.I)


def get_title(text: str):
    m = OG_TITLE_RE.search(text)
    if m:
        return m.group(1)
    m = TITLE_RE.search(text)
    return m.group(1).strip() if m else None


def get_meta_desc_raw(text: str):
    m = META_DESC_RE.search(text)
    return m.group(1) if m else None


def add_twitter_title(text: str, title: str) -> tuple[str, bool]:
    if 'name="twitter:title"' in text:
        return text, False
    if 'name="twitter:card"' not in text:
        return text, False
    insert = f'\n<meta name="twitter:title" content="{title}">'
    return TWITTER_CARD_RE.sub(rf"\1{insert}", text, count=1), True


def sync_twitter_desc(text: str, desc_raw: str) -> tuple[str, bool]:
    if 'name="twitter:description"' not in text:
        return text, False
    m = TWITTER_DESC_RE.search(text)
    if not m or m.group(2) == desc_raw:
        return text, False
    return TWITTER_DESC_RE.sub(
        lambda match: f"{match.group(1)}{desc_raw}{match.group(3)}",
        text,
        count=1,
    ), True


def main() -> None:
    updated = 0
    for html_path in sorted(ROOT.rglob("index.html")):
        rel = str(html_path.relative_to(ROOT))
        text = html_path.read_text(encoding="utf-8")
        orig = text
        changes: list[str] = []

        title = get_title(text)
        desc_raw = get_meta_desc_raw(text)

        if title:
            text, c = add_twitter_title(text, title)
            if c:
                changes.append("twitter:title")

        if desc_raw:
            text, c = sync_twitter_desc(text, desc_raw)
            if c:
                changes.append("twitter:desc-sync")

        if text != orig:
            html_path.write_text(text, encoding="utf-8")
            updated += 1
            print(f"{rel}: {', '.join(changes)}")

    print(f"\nUpdated {updated} files.")


if __name__ == "__main__":
    main()
