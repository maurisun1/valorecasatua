#!/usr/bin/env python3
"""SEO pass 4: twitter, OG dimensions, dateModified, meta trim."""

import html
import json
import re
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
DATE_MOD = "2026-07-05"

META_DESC_RE = re.compile(
    r'(<meta\s+name="description"\s+content=")([^"]*)(")',
    re.I,
)
TWITTER_DESC_RE = re.compile(
    r'(<meta\s+name="twitter:description"\s+content=")([^"]*)(")',
    re.I,
)
OG_IMAGE_RE = re.compile(
    r'(<meta\s+property="og:image"\s+content=")([^"]*)(")',
    re.I,
)

META_FIXES = {
    "chi-siamo/index.html": (
        "Portale informativo su valore immobiliare in Lombardia: dati OMI, strumenti gratuiti e guide per decidere con consapevolezza.",
        "Cos'è ValoreCasaTua.it: portale informativo su valore immobiliare in Lombardia. Metodo basato su dati OMI, strumenti gratuiti e guide per decidere con consapevolezza.",
    ),
    "pensione-cambiare-casa/index.html": (
        "In pensione si rivaluta anche la casa: troppo grande, città sbagliata o perfetta com'è? Guida per ragionare senza fretta.",
        "Andare in pensione è spesso il momento in cui si rivaluta tutto, anche la casa. Troppo grande, città sbagliata o perfetta com'è? Guida per ragionare senza fretta.",
    ),
}


def get_meta_description(text: str) -> Optional[str]:
    m = META_DESC_RE.search(text)
    return html.unescape(m.group(2)) if m else None


def sync_twitter(text: str) -> tuple[str, bool]:
    if 'name="twitter:description"' in text:
        return text, False
    desc = get_meta_description(text)
    if not desc:
        return text, False
    esc = html.escape(desc, quote=True)
    if 'name="twitter:card"' in text:
        return re.sub(
            r'(<meta\s+name="twitter:card"[^>]*>)',
            rf'\1\n<meta name="twitter:description" content="{esc}" />',
            text,
            count=1,
            flags=re.I,
        ), True
    if 'property="og:image"' in text:
        return re.sub(
            r'(<meta\s+property="og:image"[^>]*>)',
            rf'\1\n<meta name="twitter:description" content="{esc}" />',
            text,
            count=1,
            flags=re.I,
        ), True
    return text, False


def og_dimensions(text: str) -> tuple[str, bool]:
    if "og:image:width" in text:
        return text, False
    m = OG_IMAGE_RE.search(text)
    if not m:
        return text, False
    insert = (
        f'{m.group(1)}{m.group(2)}{m.group(3)}\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:type" content="image/jpeg">'
    )
    return OG_IMAGE_RE.sub(insert, text, count=1), True


def add_date_modified_to_json(obj: Any) -> bool:
    changed = False
    if isinstance(obj, dict):
        typ = obj.get("@type")
        types = typ if isinstance(typ, list) else [typ] if typ else []
        schema_types = {
            "Article",
            "WebPage",
            "CollectionPage",
            "AboutPage",
            "Service",
            "WebApplication",
            "FAQPage",
        }
        if any(t in schema_types for t in types if t):
            if "dateModified" not in obj:
                obj["dateModified"] = DATE_MOD
                changed = True
            if "datePublished" not in obj and typ in {"Article", "WebPage", "CollectionPage"}:
                obj.setdefault("datePublished", "2026-06-20")
                changed = True
        for key, val in list(obj.items()):
            if key == "@graph" and isinstance(val, list):
                for item in val:
                    if add_date_modified_to_json(item):
                        changed = True
            elif isinstance(val, (dict, list)):
                if add_date_modified_to_json(val):
                    changed = True
    elif isinstance(obj, list):
        for item in obj:
            if add_date_modified_to_json(item):
                changed = True
    return changed


def patch_json_ld(text: str) -> tuple[str, bool]:
    changed = False

    def repl(m: re.Match[str]) -> str:
        nonlocal changed
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if add_date_modified_to_json(data):
            changed = True
            return (
                '<script type="application/ld+json">'
                + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                + "</script>"
            )
        return m.group(0)

    new_text = re.sub(
        r'<script type="application/ld\+json">(.*?)</script>',
        repl,
        text,
        flags=re.S | re.I,
    )
    return new_text, changed


def apply_meta_fixes(text: str, rel: str) -> tuple[str, bool]:
    if rel not in META_FIXES:
        return text, False
    new_desc, old_desc = META_FIXES[rel]
    if old_desc not in text and new_desc in text:
        return text, False
    orig = text
    text = text.replace(old_desc, new_desc)
    text = META_DESC_RE.sub(
        lambda m: f'{m.group(1)}{html.escape(new_desc, quote=True)}{m.group(3)}',
        text,
        count=1,
    )
    esc = html.escape(new_desc, quote=True)
    if 'name="twitter:description"' in text:
        text = TWITTER_DESC_RE.sub(
            lambda m: f'{m.group(1)}{esc}{m.group(3)}',
            text,
            count=1,
        )
    return text, text != orig


def main() -> None:
    n = 0
    for html_path in sorted(ROOT.rglob("*.html")):
        rel = str(html_path.relative_to(ROOT))
        text = html_path.read_text(encoding="utf-8")
        orig = text
        changes: list[str] = []

        new, c = apply_meta_fixes(text, rel)
        if c:
            changes.append("meta-trim")
            text = new

        new, c = sync_twitter(text)
        if c:
            changes.append("twitter")
            text = new

        new, c = og_dimensions(text)
        if c:
            changes.append("og-dims")
            text = new

        new, c = patch_json_ld(text)
        if c:
            changes.append("dateModified")
            text = new

        if text != orig:
            html_path.write_text(text, encoding="utf-8")
            n += 1
            print(f"{rel}: {', '.join(changes)}")

    print(f"\nUpdated {n} files.")


if __name__ == "__main__":
    main()
