#!/usr/bin/env python3
"""Final SEO/technical polish pass across ValoreCasaTua.it."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://valorecasatua.it"
TODAY = "2026-07-04"
LEGAL_OG = f"{BASE}/assets/og-risorse.jpg"
LEGAL_ALT = "ValoreCasaTua.it — consulenza immobiliare in Lombardia"

LEGAL_PAGES = {
    "cookie/index.html",
    "privacy/index.html",
    "grazie-checklist/index.html",
}


def sync_social_meta(text: str) -> str:
    head = text.split("</head>")[0]
    title_m = re.search(r"<title>([^<]+)</title>", head)
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', head)
    if not title_m:
        return text

    title = title_m.group(1)
    text = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{title}"',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta name="twitter:title" content="[^"]*"',
        f'<meta name="twitter:title" content="{title}"',
        text,
        count=1,
    )

    if desc_m:
        desc = desc_m.group(1)
        text = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{desc}"',
            text,
            count=1,
        )
        if 'name="twitter:description"' in text:
            text = re.sub(
                r'<meta name="twitter:description" content="[^"]*"',
                f'<meta name="twitter:description" content="{desc}"',
                text,
                count=1,
            )
    return text


def remove_keywords(text: str) -> str:
    return re.sub(r'\n<meta name="keywords" content="[^"]*">', "", text)


def fix_schema_trailing_slashes(text: str) -> str:
    """Ensure valorecasatua.it/slug URLs in JSON-LD end with / (except homepage)."""

    def repl(m: re.Match) -> str:
        key = m.group(1)
        url = m.group(2)
        if url == f"{BASE}/" or url.endswith("/"):
            return m.group(0)
        return f'"{key}": "{url}/"'

    return re.sub(
        rf'"(@id|url|mainEntityOfPage)":\s*"(https://valorecasatua\.it/[^"/]+)"',
        repl,
        text,
    )


def bump_date_modified(text: str) -> str:
    if '"dateModified"' not in text:
        return text
    return re.sub(
        r'"dateModified":\s*"\d{4}-\d{2}-\d{2}"',
        f'"dateModified": "{TODAY}"',
        text,
    )


def fix_legal_og(text: str, rel: str) -> str:
    if rel not in LEGAL_PAGES:
        return text
    text = re.sub(
        r'<meta property="og:image" content="[^"]*"',
        f'<meta property="og:image" content="{LEGAL_OG}"',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta name="twitter:image" content="[^"]*"',
        f'<meta name="twitter:image" content="{LEGAL_OG}"',
        text,
        count=1,
    )
    if 'property="og:image:alt"' in text:
        text = re.sub(
            r'<meta property="og:image:alt" content="[^"]*"',
            f'<meta property="og:image:alt" content="{LEGAL_ALT}"',
            text,
            count=1,
        )
    return text


def normalize_org_url(text: str) -> str:
    return text.replace(
        '"url":"https://valorecasatua.it"',
        '"url":"https://valorecasatua.it/"',
    ).replace(
        '"url": "https://valorecasatua.it"',
        '"url": "https://valorecasatua.it/"',
    )


def process_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8")
    text = original
    changes: list[str] = []

    for fn, label in [
        (remove_keywords, "keywords-removed"),
        (sync_social_meta, "social-sync"),
        (fix_schema_trailing_slashes, "schema-slashes"),
        (normalize_org_url, "org-url"),
        (bump_date_modified, "dateModified"),
    ]:
        new = fn(text)
        if new != text:
            changes.append(label)
            text = new

    new = fix_legal_og(text, rel)
    if new != text:
        changes.append("legal-og")
        text = new

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
    print(f"\nUpdated {updated} HTML files.")


if __name__ == "__main__":
    main()
