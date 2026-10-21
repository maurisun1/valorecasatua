#!/usr/bin/env python3
"""Assign category-specific Open Graph images across HTML pages."""

import re
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://valorecasatua.it"
OG_PROVINCE_DIR = f"{BASE}/assets/og/province"

PROVINCE_NAMES = {
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

CATEGORIES = {
    "home": {
        "image": f"{BASE}/assets/og-home.jpg",
        "alt": "Quanto vale la tua casa? Stima gratuita OMI in Lombardia — ValoreCasaTua.it",
        "paths": {"index.html"},
    },
    "strumenti": {
        "image": f"{BASE}/assets/og-strumenti.jpg",
        "alt": "Strumenti immobiliari: check-up, ristrutturazione, affitti, energia — ValoreCasaTua.it",
        "paths": {
            "verifica-casa/index.html",
            "conviene-ristrutturare/index.html",
            "affitto-breve-vs-transitorio/index.html",
            "classe-energetica-valore-casa/index.html",
            "checklist-documenti-vendere-casa/index.html",
        },
    },
    "guide_index": {
        "image": f"{BASE}/assets/og-guide.jpg",
        "alt": "Prezzi al m² in Lombardia con dati OMI ufficiali — ValoreCasaTua.it",
        "paths": {"guide/index.html"},
    },
    "situazioni": {
        "image": f"{BASE}/assets/og-situazioni.jpg",
        "alt": "Guide pratiche per vendere casa nelle situazioni di vita — ValoreCasaTua.it",
        "prefixes": (
            "vendere-",
            "casa-",
            "comprare-",
            "trasferimento-",
            "pensione-",
            "plusvalenza-",
            "quanto-costa-",
        ),
    },
    "risorse": {
        "image": f"{BASE}/assets/og-risorse.jpg",
        "alt": "Risorse e approfondimenti sul mercato immobiliare lombardo — ValoreCasaTua.it",
        "paths": {
            "risorse/index.html",
            "chi-siamo/index.html",
            "mercato-immobiliare-lombardia-2026/index.html",
        },
    },
}

DEFAULT_IMAGE = f"{BASE}/assets/og-valorecasatua.jpg"
DEFAULT_ALT = "ValoreCasaTua.it — stima immobiliare gratuita in Lombardia"


def province_og(rel: str) -> Optional[Tuple[str, str]]:
    """Return OG image + alt for guide/prezzi-mq-<slug>/ pages."""
    m = re.match(r"guide/prezzi-mq-([^/]+)/index\.html$", rel)
    if not m:
        return None
    slug = m.group(1)
    name = PROVINCE_NAMES.get(slug)
    if not name:
        return None
    return (
        f"{OG_PROVINCE_DIR}/og-guide-{slug}.jpg",
        f"Prezzi al m² a {name}: dati OMI ufficiali — ValoreCasaTua.it",
    )


def category_for(rel: str) -> Tuple[str, str]:
    prov = province_og(rel)
    if prov:
        return prov

    for cfg in CATEGORIES.values():
        if rel in cfg.get("paths", ()):
            return cfg["image"], cfg["alt"]
        for prefix in cfg.get("prefixes", ()):
            if rel.startswith(prefix):
                return cfg["image"], cfg["alt"]
    return DEFAULT_IMAGE, DEFAULT_ALT


def set_og_image(text: str, image: str, alt: str) -> str:
    text = re.sub(
        r'<meta property="og:image" content="[^"]*"',
        f'<meta property="og:image" content="{image}"',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta name="twitter:image" content="[^"]*"',
        f'<meta name="twitter:image" content="{image}"',
        text,
        count=1,
    )
    if 'property="og:image:alt"' in text:
        text = re.sub(
            r'<meta property="og:image:alt" content="[^"]*"',
            f'<meta property="og:image:alt" content="{alt}"',
            text,
            count=1,
        )
    else:
        text = re.sub(
            r'(<meta property="og:image" content="[^"]*">)',
            rf'\1\n<meta property="og:image:alt" content="{alt}">',
            text,
            count=1,
        )
    return text


def main() -> None:
    counts: dict[str, int] = {}
    for html in sorted(ROOT.rglob("*.html")):
        rel = html.relative_to(ROOT).as_posix()
        image, alt = category_for(rel)
        original = html.read_text(encoding="utf-8")
        updated = set_og_image(original, image, alt)
        if updated != original:
            html.write_text(updated, encoding="utf-8")
        cat = image.split("/")[-1].replace(".jpg", "")
        counts[cat] = counts.get(cat, 0) + 1
        print(f"{rel} → {cat}")

    print("\nSummary:")
    for cat, n in sorted(counts.items()):
        print(f"  {cat}: {n} pages")


if __name__ == "__main__":
    main()
