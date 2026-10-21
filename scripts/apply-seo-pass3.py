#!/usr/bin/env python3
"""SEO pass 3: twitter descriptions, schema neutralization, inline JPEG extraction."""

import base64
import html
import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
INLINE_IMG = ROOT / "assets" / "hero-lombardia.jpg"
IMG_RE = re.compile(
    r'<img\s+src="data:image/jpeg;base64,([A-Za-z0-9+/=\s]+)"([^>]*)>',
    re.I,
)
META_DESC_RE = re.compile(
    r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>',
    re.I,
)
TWITTER_DESC_RE = re.compile(
    r'(<meta\s+name="twitter:description"\s+content=")([^"]*)(")',
    re.I,
)


def truncate_twitter(text: str, limit: int = 200) -> str:
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return (cut or text[: limit - 1]) + "…"


def get_meta_description(text: str) -> Optional[str]:
    m = META_DESC_RE.search(text)
    return html.unescape(m.group(1)) if m else None


def sync_twitter_description(text: str) -> str:
    desc = get_meta_description(text)
    if not desc or 'name="twitter:description"' not in text:
        return text
    tw = truncate_twitter(desc)
    return TWITTER_DESC_RE.sub(
        lambda m: f'{m.group(1)}{html.escape(tw, quote=True)}{m.group(3)}',
        text,
        count=1,
    )


def neutralize_schema(text: str) -> str:
    text = text.replace("Valutazione immobiliare", "Informazione immobiliare")
    text = re.sub(r',\s*""', "", text)
    text = re.sub(r'\[\s*,', "[", text)
    text = re.sub(r',\s*,', ",", text)
    text = text.replace("strumenti di analisi", "strumenti informativi")
    text = text.replace(
        "valutazione, verifica pre-vendita, valorizzazione",
        "informazione immobiliare, verifica documentale, valorizzazione",
    )
    return text


def ensure_jpeg_file(b64: str) -> None:
    if INLINE_IMG.exists():
        return
    INLINE_IMG.parent.mkdir(parents=True, exist_ok=True)
    INLINE_IMG.write_bytes(base64.b64decode(re.sub(r"\s+", "", b64)))


def replace_inline_jpegs(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        ensure_jpeg_file(m.group(1))
        attrs = m.group(2)
        if "alt=" not in attrs.lower():
            attrs += ' alt="Proprietario che valuta un immobile in Lombardia"'
        if "loading=" not in attrs.lower():
            attrs += ' loading="lazy"'
        if "decoding=" not in attrs.lower():
            attrs += ' decoding="async"'
        if "width=" not in attrs.lower():
            attrs += ' width="435"'
        if "height=" not in attrs.lower():
            attrs += ' height="307"'
        count += 1
        return f'<img src="/assets/hero-lombardia.jpg"{attrs}>'

    return IMG_RE.sub(repl, text), count


def process(path: Path) -> list[str]:
    changes: list[str] = []
    text = path.read_text(encoding="utf-8")
    orig = text

    text = sync_twitter_description(text)
    if text != orig:
        changes.append("twitter")
        orig = text

    text = neutralize_schema(text)
    if text != orig:
        changes.append("schema")
        orig = text

    text, nimg = replace_inline_jpegs(text)
    if nimg:
        changes.append(f"inline-img×{nimg}")

    if text != path.read_text(encoding="utf-8") if changes else text != orig:
        pass

    final_orig = path.read_text(encoding="utf-8")
    # re-read only if we already mutated - simplify
    if changes:
        # we need to apply all transforms on original in one pass
        pass

    return changes


def main() -> None:
    n = 0
    for html_path in sorted(ROOT.rglob("*.html")):
        text = html_path.read_text(encoding="utf-8")
        orig = text
        changes: list[str] = []

        new = sync_twitter_description(text)
        if new != text:
            changes.append("twitter")
            text = new

        new = neutralize_schema(text)
        if new != text:
            changes.append("schema")
            text = new

        new, nimg = replace_inline_jpegs(text)
        if nimg:
            changes.append(f"inline-img×{nimg}")
            text = new

        if text != orig:
            html_path.write_text(text, encoding="utf-8")
            n += 1
            print(f"{html_path.relative_to(ROOT)}: {', '.join(changes)}")

    if INLINE_IMG.exists():
        print(f"\nExtracted {INLINE_IMG.relative_to(ROOT)} ({INLINE_IMG.stat().st_size // 1024} KB)")
    print(f"\nUpdated {n} files.")


if __name__ == "__main__":
    main()
