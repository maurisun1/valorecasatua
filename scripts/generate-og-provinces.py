#!/usr/bin/env python3
"""Generate per-province Open Graph images (1200x630) for OMI guide pages."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "og" / "province"
W, H = 1200, 630

# slug -> display name
PROVINCES = {
    "milano": "Milano",
    "brescia": "Brescia",
    "bergamo": "Bergamo",
    "como": "Como",
    "varese": "Varese",
    "monza-brianza": "Monza e Brianza",
    "lecco": "Lecco",
    "lodi": "Lodi",
    "pavia": "Pavia",
    "cremona": "Cremona",
    "mantova": "Mantova",
    "sondrio": "Sondrio",
}

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
    # roof
    draw.polygon(
        [(x, y + int(8 * s)), (x + int(22 * s), y + int(28 * s)), (x + int(44 * s), y + int(8 * s))],
        outline=COLORS["teal"],
        width=max(2, int(3 * s)),
    )
    # walls
    draw.rectangle(
        (x + int(8 * s), y + int(24 * s), x + int(36 * s), y + int(52 * s)),
        outline=COLORS["gold"],
        width=max(2, int(3 * s)),
    )
    # window
    draw.rectangle(
        (x + int(18 * s), y + int(32 * s), x + int(26 * s), y + int(40 * s)),
        fill=COLORS["teal_dark"],
    )


def render_province(slug: str, name: str) -> Path:
    img = Image.new("RGB", (W, H), COLORS["bg"])
    draw = ImageDraw.Draw(img)

    # soft background circles
    for cx, cy, r, alpha in [(980, 120, 180, 28), (1050, 480, 220, 22), (180, 520, 140, 18)]:
        overlay = Image.new("RGB", (W, H), COLORS["bg"])
        odraw = ImageDraw.Draw(overlay)
        odraw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=COLORS["bg2"])
        img = Image.blend(img, overlay, alpha / 100)
        draw = ImageDraw.Draw(img)

    draw_house_icon(draw, 72, 72, 1.15)

    font_label = load_font(22, bold=True)
    font_brand = load_font(28, bold=True)
    font_sub = load_font(34, bold=False)
    font_province = load_font(86 if len(name) < 14 else 72, bold=True)
    font_footer = load_font(24, bold=False)

    draw.text((72, 150), "GUIDE · DATI OMI · LOMBARDIA", fill=COLORS["gold"], font=font_label)
    draw.line((72, 195, 420, 195), fill=COLORS["gold"], width=2)

    # province name — shrink if long
    bbox = draw.textbbox((0, 0), name, font=font_province)
    tw = bbox[2] - bbox[0]
    if tw > 900:
        font_province = load_font(58, bold=True)
    draw.text((72, 220), name, fill=COLORS["ink"], font=font_province)

    draw.text((72, 340), "Prezzi al m² · quotazioni OMI ufficiali", fill=COLORS["teal"], font=font_sub)
    draw.text((72, 400), "Agenzia delle Entrate · 2° semestre 2025", fill=COLORS["muted"], font=font_footer)

    draw.line((72, 470, 1128, 470), fill=COLORS["line"], width=1)
    draw.text((72, 500), "ValoreCasaTua.it", fill=COLORS["ink"], font=font_brand)
    draw.text((72, 545), "Stima gratuita del tuo immobile in provincia", fill=COLORS["muted"], font=font_footer)

    # decorative map hint (simple lombardy blob)
    draw.ellipse((900, 250, 1120, 430), outline=COLORS["teal"], width=3)
    draw.ellipse((940, 290, 1080, 390), outline=COLORS["line"], width=2)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"og-guide-{slug}.jpg"
    img.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    return path


def main() -> None:
    for slug, name in PROVINCES.items():
        path = render_province(slug, name)
        print(f"Created {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
