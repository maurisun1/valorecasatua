#!/usr/bin/env python3
"""Generate category OG images (1200x630) and Organization logo."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OG_DIR = ROOT / "assets" / "og"
ASSETS = ROOT / "assets"
W, H = 1200, 630

COLORS = {
    "bg": (250, 248, 244),
    "bg2": (242, 237, 228),
    "ink": (26, 46, 59),
    "teal": (47, 148, 136),
    "teal_dark": (26, 122, 111),
    "gold": (139, 105, 20),
    "muted": (107, 124, 135),
    "line": (220, 210, 196),
}

CATEGORIES = {
    "og-home.jpg": {
        "eyebrow": "STIMA ORIENTATIVA · DATI OMI",
        "title": "Quanto vale\nla tua casa?",
        "subtitle": "Lombardia · 12 province · gratuito",
        "footer": "Calcolatore valore immobiliare",
    },
    "og-strumenti.jpg": {
        "eyebrow": "STRUMENTI · PORTALE INFORMATIVO",
        "title": "Strumenti per\ncapire il valore",
        "subtitle": "Verifica, ristrutturazione, affitti, energia",
        "footer": "Orientamento informativo senza impegno",
    },
    "og-guide.jpg": {
        "eyebrow": "GUIDE · DATI OMI · LOMBARDIA",
        "title": "Prezzi al m²\nper provincia",
        "subtitle": "Quotazioni ufficiali Agenzia delle Entrate",
        "footer": "12 province · aggiornamento 2025",
    },
    "og-situazioni.jpg": {
        "eyebrow": "SITUAZIONI DI VITA",
        "title": "Vendere casa\nnelle situazioni reali",
        "subtitle": "Separazione, eredità, mutuo, inquilino…",
        "footer": "Guide pratiche · nessuna pressione",
    },
    "og-risorse.jpg": {
        "eyebrow": "RISORSE · MERCATO LOMBARDIA",
        "title": "Informazione\nper decidere meglio",
        "subtitle": "Mercato, costi, progetto e approfondimenti",
        "footer": "ValoreCasaTua.it",
    },
    "og-valorecasatua.jpg": {
        "eyebrow": "VALORECASATUA.IT",
        "title": "Più informazioni.\nPiù consapevolezza.",
        "subtitle": "Portale informativo immobiliare in Lombardia",
        "footer": "Dati OMI · strumenti gratuiti",
    },
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_house_icon(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    s = scale
    draw.polygon(
        [(x, y + int(8 * s)), (x + int(22 * s), y + int(28 * s)), (x + int(44 * s), y + int(8 * s))],
        outline=COLORS["teal"],
        width=max(2, int(3 * s)),
    )
    draw.rectangle(
        (x + int(8 * s), y + int(24 * s), x + int(36 * s), y + int(52 * s)),
        outline=COLORS["gold"],
        width=max(2, int(3 * s)),
    )
    draw.rectangle(
        (x + int(18 * s), y + int(32 * s), x + int(26 * s), y + int(40 * s)),
        fill=COLORS["teal_dark"],
    )


def add_bg_decor(img: Image.Image) -> Image.Image:
    draw = ImageDraw.Draw(img)
    for cx, cy, r, alpha in [(980, 120, 180, 28), (1050, 480, 220, 22), (180, 520, 140, 18)]:
        overlay = Image.new("RGB", (W, H), COLORS["bg"])
        odraw = ImageDraw.Draw(overlay)
        odraw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=COLORS["bg2"])
        img = Image.blend(img, overlay, alpha / 100)
        draw = ImageDraw.Draw(img)
    return img, draw


def render_category(filename: str, cfg: dict) -> Path:
    img = Image.new("RGB", (W, H), COLORS["bg"])
    img, draw = add_bg_decor(img)
    draw_house_icon(draw, 72, 72, 1.15)

    font_label = load_font(22, bold=True)
    font_brand = load_font(28, bold=True)
    font_title = load_font(72, bold=True)
    font_sub = load_font(32, bold=False)
    font_footer = load_font(24, bold=False)

    draw.text((72, 150), cfg["eyebrow"], fill=COLORS["gold"], font=font_label)
    draw.line((72, 195, 520, 195), fill=COLORS["gold"], width=2)

    y = 220
    for line in cfg["title"].split("\n"):
        draw.text((72, y), line, fill=COLORS["ink"], font=font_title)
        y += 78

    draw.text((72, y + 10), cfg["subtitle"], fill=COLORS["teal"], font=font_sub)
    draw.line((72, 470, 1128, 470), fill=COLORS["line"], width=1)
    draw.text((72, 500), "ValoreCasaTua.it", fill=COLORS["ink"], font=font_brand)
    draw.text((72, 545), cfg["footer"], fill=COLORS["muted"], font=font_footer)

    draw.ellipse((900, 250, 1120, 430), outline=COLORS["teal"], width=3)

    OG_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSETS / filename
    img.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    return path


def render_logo() -> Path:
    size = 512
    img = Image.new("RGB", (size, size), COLORS["bg"])
    draw = ImageDraw.Draw(img)

    draw.ellipse((24, 24, size - 24, size - 24), outline=COLORS["line"], width=2)
    draw_house_icon(draw, size // 2 - 44, 120, 1.4)

    font_brand = load_font(42, bold=True)
    font_tag = load_font(20, bold=False)
    brand = "ValoreCasaTua.it"
    bbox = draw.textbbox((0, 0), brand, font=font_brand)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw) // 2, 300), brand, fill=COLORS["ink"], font=font_brand)
    tag = "Portale informativo · Lombardia"
    bbox = draw.textbbox((0, 0), tag, font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw) // 2, 365), tag, fill=COLORS["muted"], font=font_tag)

    path = ASSETS / "logo-valorecasatua.jpg"
    img.save(path, "JPEG", quality=90, optimize=True)
    return path


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for filename, cfg in CATEGORIES.items():
        path = render_category(filename, cfg)
        print(f"Created {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)")
    logo = render_logo()
    print(f"Created {logo.relative_to(ROOT)} ({logo.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
