#!/usr/bin/env python3
"""Copertine 1200×675 WebP per articoli e guide di ValoreCasaTua.

Genera assets/covers/{slug}.webp (titolo, dato chiave se c'è, logo),
inserisce l'immagine sotto l'H1, aggiorna og:image e image negli Article
JSON-LD, e aggiunge le copertine a sitemap-images.xml.

Non modifica dateModified, lastmod né le date visibili: è un aggiornamento
grafico. Idempotente: si può rilanciare.

Richiede Pillow. I font sono in scripts/fonts/.
"""

from __future__ import annotations

import html as html_lib
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path(__file__).resolve().parent / "fonts"
COVER_DIR = ROOT / "assets" / "covers"
LOGO_PATH = ROOT / "assets" / "brand" / "logo-schema.svg.png"
SITEMAP = ROOT / "sitemap.xml"
SITEMAP_IMAGES = ROOT / "sitemap-images.xml"
ORIGIN = "https://valorecasatua.it"

W, H = 1200, 675
CREAM = (250, 248, 244)
NAVY = (12, 35, 52)
TEAL = (26, 122, 111)
TEAL_SOFT = (15, 92, 84)
GOLD = (139, 105, 20)
MUTED = (90, 104, 116)

# Pagine che non sono articoli né guide.
SKIP = {
    "/",
    "/verifica-casa/",
    "/conviene-ristrutturare/",
    "/risorse/",
    "/glossario/",
    "/chi-siamo/",
    "/per-la-stampa/",
}
# Pagine lunghe senza @type Article: copertina, og:image e sitemap, non il JSON-LD.
EXTRA = {
    "/mercato-immobiliare-lombardia-2026/",
    "/checklist-documenti-vendere-casa/",
}

AMOUNT = re.compile(r"€\s*(\d{1,3}(?:\.\d{3})+|\d{2,6})")
DA_A = re.compile(
    r"da\s+(?:circa\s+)?€\s*(\d{1,3}(?:\.\d{3})+|\d{2,6})(?:\s*/\s*m²)?"
    r"\s+a\s+(oltre\s+)?€\s*(\d{1,3}(?:\.\d{3})+|\d{2,6})"
)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def knock_cream(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r > 218 and g > 208 and b > 190 and abs(r - g) < 35:
                px[x, y] = (r, g, b, 0)
    return im


def wrap(text: str, face: ImageFont.FreeTypeFont, max_w: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = word if not cur else f"{cur} {word}"
        if face.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_title(text: str, max_w: float) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in (56, 50, 44, 38, 32):
        face = font("PlayfairDisplay-600.ttf", size)
        lines = wrap(text, face, max_w)
        if len(lines) <= 4:
            return face, lines
    face = font("PlayfairDisplay-600.ttf", 28)
    return face, wrap(text, face, max_w)[:5]


def tracked(draw: ImageDraw.ImageDraw, xy, text, face, fill, tracking: float) -> None:
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=face, fill=fill)
        x += face.getlength(ch) + tracking


def _euro(raw: str) -> int:
    return int(raw.replace(".", ""))


def _fmt_it(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def key_from_text(source: str) -> str | None:
    suffix = "/m²" if "m²" in source else ""
    pair = DA_A.search(source)
    if pair:
        lo, hi = _euro(pair.group(1)), _euro(pair.group(3))
        if lo > hi:
            lo, hi = hi, lo
        hi_txt = f"oltre {_fmt_it(hi)}" if pair.group(2) else _fmt_it(hi)
        return f"€ {_fmt_it(min(lo, hi))} – {hi_txt}{suffix}"
    found = list(AMOUNT.finditer(source))
    if not found:
        return None
    values = [_euro(match.group(1)) for match in found]
    lo, hi = min(values), max(values)
    if lo == hi:
        return f"€ {_fmt_it(lo)}{suffix}"
    return f"€ {_fmt_it(lo)} – {_fmt_it(hi)}{suffix}"


def find_key(page: str) -> str | None:
    desc = re.search(r'<meta name="description" content="([^"]*)"', page)
    if desc:
        key = key_from_text(html_lib.unescape(desc.group(1)))
        if key:
            return key
    qa = re.search(r'class="vct-quick-answer".*?</aside>', page, re.S)
    if not qa:
        return None
    text = re.sub(r"<[^>]+>", " ", qa.group(0))
    key = key_from_text(html_lib.unescape(text))
    if key and "/m²" in key:
        return key
    return None


def h1_text(page: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    if not match:
        raise SystemExit("H1 mancante")
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return re.sub(r"\s+", " ", html_lib.unescape(text)).strip()


_LOGO: Image.Image | None = None


def load_logo(size: int) -> Image.Image:
    global _LOGO
    if _LOGO is None:
        _LOGO = knock_cream(Image.open(LOGO_PATH))
    return _LOGO.resize((size, size), Image.Resampling.LANCZOS)


def render(title: str, key: str | None, dest: Path) -> None:
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 14, H), fill=TEAL)
    draw.rectangle((900, 0, W, H), fill=TEAL_SOFT)
    draw.rectangle((900, 0, 906, H), fill=GOLD)

    logo = load_logo(92)
    canvas.paste(logo, (48, 40), logo)
    brand = font("HankenGrotesk-700.ttf", 22)
    tracked(draw, (160, 58), "VALORECASATUA.IT", brand, GOLD, 1.6)
    payoff = font("HankenGrotesk-500.ttf", 18)
    draw.text(
        (160, 96),
        "Più informazioni. Più consapevolezza. Più valore.",
        font=payoff,
        fill=MUTED,
    )
    draw.rectangle((48, 168, 860, 171), fill=GOLD)

    face, lines = fit_title(title, 800)
    y = 210
    for line in lines:
        draw.text((48, y), line, font=face, fill=NAVY)
        y += int(face.size * 1.18)

    if key:
        label = font("HankenGrotesk-700.ttf", 16)
        tracked(draw, (48, y + 28), "DATO CHIAVE", label, GOLD, 2.2)
        stat = font("PlayfairDisplay-600.ttf", 48)
        while stat.size > 28 and stat.getlength(key) > 800:
            stat = font("PlayfairDisplay-600.ttf", stat.size - 2)
        draw.text((48, y + 56), key, font=stat, fill=TEAL)

    big = load_logo(210)
    canvas.paste(big, (945, 232), big)

    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, "WEBP", quality=82, method=6)


def attr_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
    )


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def cover_tag(src: str, alt: str) -> str:
    return (
        f'\n<img class="vct-cover" src="{src}" alt="{attr_escape(alt)}" '
        f'width="1200" height="675" fetchpriority="high" '
        f'style="width:100%;height:auto;margin:18px 0 8px;border-radius:16px">'
    )


def set_meta(page: str, attr: str, name: str, content: str) -> tuple[str, bool]:
    patterns = [
        re.compile(
            rf'(<meta\b[^>]*\b{attr}=["\']{re.escape(name)}["\'][^>]*\bcontent=["\'])([^"\']*)(["\'])',
            re.I,
        ),
        re.compile(
            rf'(<meta\b[^>]*\bcontent=["\'])([^"\']*)(["\'][^>]*\b{attr}=["\']{re.escape(name)}["\'])',
            re.I,
        ),
    ]
    for pattern in patterns:
        updated, count = pattern.subn(rf"\g<1>{content}\3", page, count=1)
        if count:
            return updated, True
    return page, False


def patch_article_image(page: str, image_url: str) -> str:
    def replacer(match: re.Match) -> str:
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        changed = False

        def visit(node) -> None:
            nonlocal changed
            if isinstance(node, dict):
                kind = node.get("@type")
                kinds = kind if isinstance(kind, list) else [kind]
                if "Article" in kinds and node.get("image") != image_url:
                    node["image"] = image_url
                    changed = True
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)

        visit(data)
        if not changed:
            return match.group(0)
        dumped = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        return '<script type="application/ld+json">' + dumped + "</script>"

    return re.sub(
        r'<script type="application/ld\+json">(.*?)</script>',
        replacer,
        page,
        flags=re.S,
    )


def date_fingerprint(page: str) -> tuple:
    modified = re.findall(r'"dateModified"\s*:\s*"([^"]+)"', page)
    visible = re.findall(r"Aggiornato il [^<\"]+", page)
    published = re.findall(r'"datePublished"\s*:\s*"([^"]+)"', page)
    return (tuple(modified), tuple(visible), tuple(published))


def has_article(page: str) -> bool:
    return bool(re.search(r'"@type"\s*:\s*"Article"', page))


def sitemap_locs() -> list[str]:
    text = SITEMAP.read_text(encoding="utf-8")
    return re.findall(r"<loc>(https://valorecasatua\.it[^<]*)</loc>", text)


def lastmod_for(loc: str) -> str:
    text = SITEMAP.read_text(encoding="utf-8")
    match = re.search(
        rf"<loc>{re.escape(loc)}</loc>\s*<lastmod>([^<]+)</lastmod>",
        text,
    )
    if not match:
        raise SystemExit(f"lastmod assente in sitemap.xml per {loc}")
    return match.group(1)


def slug_for(path: str) -> str:
    if path == "/guide/":
        return "guide"
    return path.strip("/").split("/")[-1]


def alt_for(title: str, key: str | None) -> str:
    if key:
        return f"Copertina: {title}. {key}."
    return f"Copertina: {title}."


def patch_html(page: str, src: str, absolute: str, alt: str) -> str:
    tag = cover_tag(src, alt)
    existing = re.search(r'\n?<img class="vct-cover"[^>]*>', page)
    if existing:
        page = page[: existing.start()] + tag + page[existing.end() :]
    else:
        if "</h1>" not in page:
            raise SystemExit("H1 di chiusura mancante")
        page = page.replace("</h1>", "</h1>" + tag, 1)

    page, found = set_meta(page, "property", "og:image", absolute)
    if not found:
        snippet = (
            f'<meta property="og:image" content="{absolute}">'
            f'<meta property="og:image:width" content="1200">'
            f'<meta property="og:image:height" content="675">'
            f'<meta property="og:image:type" content="image/webp">'
            f'<meta property="og:image:alt" content="{attr_escape(alt)}">'
        )
        page = page.replace("</head>", snippet + "</head>", 1)
    page, _ = set_meta(page, "property", "og:image:width", "1200")
    page, _ = set_meta(page, "property", "og:image:height", "675")
    page, _ = set_meta(page, "property", "og:image:type", "image/webp")
    page, _ = set_meta(page, "property", "og:image:alt", attr_escape(alt))
    page, _ = set_meta(page, "name", "twitter:image", absolute)
    page = patch_article_image(page, absolute)
    return page


def add_to_image_sitemap(entries: list[tuple[str, str, str]]) -> None:
    xml = SITEMAP_IMAGES.read_text(encoding="utf-8")
    before = re.findall(r"<lastmod>([^<]+)</lastmod>", xml)
    for loc, image_url, title in entries:
        block_re = re.compile(
            rf"(<url>\s*<loc>{re.escape(loc)}</loc>.*?</url>)",
            re.S,
        )
        match = block_re.search(xml)
        image_xml = (
            "    <image:image>\n"
            f"      <image:loc>{image_url}</image:loc>\n"
            f"      <image:title>{xml_escape(title)}</image:title>\n"
            "    </image:image>\n"
        )
        if match:
            block = match.group(1)
            if image_url in block:
                updated = re.sub(
                    rf"(<image:loc>{re.escape(image_url)}</image:loc>\s*<image:title>)[^<]*(</image:title>)",
                    rf"\g<1>{xml_escape(title)}\2",
                    block,
                    count=1,
                )
                if updated != block:
                    xml = xml[: match.start()] + updated + xml[match.end() :]
                continue
            updated = block.replace("</url>", image_xml + "  </url>", 1)
            xml = xml[: match.start()] + updated + xml[match.end() :]
        else:
            lastmod = lastmod_for(loc)
            addition = (
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"    <lastmod>{lastmod}</lastmod>\n"
                f"{image_xml}"
                "  </url>\n"
            )
            xml = xml.replace("</urlset>", addition + "</urlset>", 1)
    after = re.findall(r"<lastmod>([^<]+)</lastmod>", xml)
    if after[: len(before)] != before:
        raise SystemExit("lastmod di sitemap-images.xml è cambiato: annullo")
    SITEMAP_IMAGES.write_text(xml, encoding="utf-8")


def main() -> None:
    for needed in (
        FONT_DIR / "PlayfairDisplay-600.ttf",
        FONT_DIR / "HankenGrotesk-500.ttf",
        FONT_DIR / "HankenGrotesk-700.ttf",
        LOGO_PATH,
    ):
        if not needed.exists():
            raise SystemExit(f"Manca {needed}")

    locs = sitemap_locs()
    chosen: list[tuple[str, Path]] = []
    slugs: dict[str, str] = {}
    for loc in locs:
        path = loc[len(ORIGIN) :]
        if not path.endswith("/"):
            path += "/"
        if path in SKIP:
            continue
        html_path = ROOT / path.strip("/") / "index.html"
        page = html_path.read_text(encoding="utf-8")
        if path.startswith("/guide/") or path in EXTRA or has_article(page):
            slug = slug_for(path)
            if slug in slugs:
                raise SystemExit(f"Slug duplicato {slug}: {slugs[slug]} e {path}")
            slugs[slug] = path
            chosen.append((path, html_path))

    entries = []
    for path, html_path in chosen:
        original = html_path.read_text(encoding="utf-8")
        before = date_fingerprint(original)
        title = h1_text(original)
        key = find_key(original)
        slug = slug_for(path)
        dest = COVER_DIR / f"{slug}.webp"
        render(title, key, dest)
        src = f"/assets/covers/{slug}.webp"
        absolute = f"{ORIGIN}{src}"
        alt = alt_for(title, key)
        updated = patch_html(original, src, absolute, alt)
        if date_fingerprint(updated) != before:
            raise SystemExit(f"Date cambiate in {path}: annullo")
        if 'loading="lazy"' in updated[updated.find('class="vct-cover"') : updated.find('class="vct-cover"') + 400]:
            raise SystemExit(f"lazy loading sulla copertina di {path}")
        html_path.write_text(updated, encoding="utf-8")
        entries.append((f"{ORIGIN}{path}", absolute, alt))
        print(f"{slug}\t{key or '—'}\t{title}")

    sitemap_before = SITEMAP.read_text(encoding="utf-8")
    add_to_image_sitemap(entries)
    if SITEMAP.read_text(encoding="utf-8") != sitemap_before:
        raise SystemExit("sitemap.xml è cambiato: non doveva")
    print(f"\n{len(entries)} copertine")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
