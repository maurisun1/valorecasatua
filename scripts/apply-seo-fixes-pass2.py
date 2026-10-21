#!/usr/bin/env python3
"""SEO pass 2: titles, descriptions, og:image:alt, apple-touch-icon, schema cleanup."""

import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://valorecasatua.it"
OG_ALT_DEFAULT = "ValoreCasaTua.it — stima immobiliare gratuita in Lombardia"
APPLE_ICON = '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">'
TODAY = "2026-07-04"

TITLE_FIXES = {
    "affitto-breve-vs-transitorio/index.html": (
        "Affitto breve o transitorio? Guida e calcolo | ValoreCasaTua.it™",
        "Affitto breve o transitorio: guida e calcolo | ValoreCasaTua",
    ),
    "casa-separazione-divorzio-lombardia/index.html": (
        "Separazione o divorzio: cosa fare con la casa? | ValoreCasaTua.it™",
        "Separazione e divorzio: cosa fare con la casa | ValoreCasaTua",
    ),
    "guide/prezzi-mq-monza-brianza/index.html": (
        "Prezzi case al m² a Monza e Brianza: dati OMI | ValoreCasaTua.it",
        "Prezzi al m² Monza e Brianza: dati OMI | ValoreCasaTua",
    ),
    "index.html": (
        "Quanto vale la tua casa? Analisi gratuita OMI | ValoreCasaTua.it",
        "Quanto vale la tua casa? Stima OMI gratis | ValoreCasaTua",
    ),
    "quanto-costa-vendere-casa/index.html": (
        "Quanto costa vendere casa? Tutte le spese 2026 | ValoreCasaTua.it™",
        "Quanto costa vendere casa? Spese 2026 | ValoreCasaTua",
    ),
    "trasferimento-lavoro-vendere-affittare-casa/index.html": (
        "Trasferimento di lavoro: vendere o affittare | ValoreCasaTua.it",
        "Trasferimento lavoro: vendere o affittare | ValoreCasaTua",
    ),
    "verifica-casa/index.html": (
        "Verifica documenti e check-up pre-vendita | ValoreCasaTua.it™",
        "Check-up documenti pre-vendita | ValoreCasaTua",
    ),
}

DESC_FIXES = {
    "index.html": (
        "Scopri il valore orientativo del tuo immobile in Lombardia con dati OMI aggiornati. Analisi gratuita, nessun obbligo. Milano, Brescia, Bergamo e tutta la Lombardia.",
        "Stima gratuita del valore immobiliare in Lombardia con dati OMI aggiornati. Nessun obbligo. Milano, Brescia, Bergamo e 12 province.",
    ),
    "verifica-casa/index.html": (
        "Quali documenti servono per vendere casa in Lombardia? Verifica preliminare gratuita di planimetria, visura, APE e provenienza, con Score Vendibilità orientativo.",
        "Documenti per vendere casa in Lombardia: verifica gratuita di planimetria, visura, APE e provenienza con Score Vendibilità.",
    ),
    "casa-ereditata-divisione-eredi-lombardia/index.html": (
        "Quando un immobile passa a più eredi, la vera difficoltà non è solo il valore della casa, ma trovare una soluzione condivisa. Guida pratica per capire le opzioni.",
        "Casa ereditata da più eredi: oltre al valore, serve una soluzione condivisa. Guida pratica alle opzioni di vendita e divisione.",
    ),
    "plusvalenza-vendita-casa/index.html": (
        "Vendendo casa potresti dover pagare la plusvalenza, ma solo in certi casi. Ecco la regola dei 5 anni, le esenzioni principali e cosa verificare prima di vendere.",
        "Plusvalenza sulla vendita casa: quando si paga, regola dei 5 anni, esenzioni e cosa verificare prima di vendere.",
    ),
    "quanto-costa-vendere-casa/index.html": (
        "Tutte le spese per vendere casa: APE, plusvalenza, notaio, cancellazione ipoteca, conformità, provvigioni. Con esempi pratici e cifre reali per il mercato lombardo.",
        "Spese per vendere casa: APE, plusvalenza, notaio, ipoteca, conformità e provvigioni. Esempi e cifre per il mercato lombardo.",
    ),
}


def abs_schema_urls_loose(text: str) -> str:
    """Absolutize schema paths, including JSON with spaces after colons."""

    def repl(m: re.Match) -> str:
        key = m.group(1)
        val = m.group(2)
        if val.startswith("http"):
            return m.group(0)
        return f'"{key}": "{BASE}{val}"'

    return re.sub(
        r'"(@id|url|logo|mainEntityOfPage|image|item)":\s*"(/[^"]*)"',
        repl,
        text,
    )


def page_og_alt(text: str) -> str:
    head = text.split("</head>")[0]
    m = re.search(r'<title>([^<]+)</title>', head)
    if not m:
        return OG_ALT_DEFAULT
    title = m.group(1).split("|")[0].strip()
    if len(title) > 100:
        title = title[:97] + "..."
    return f"{title} — ValoreCasaTua.it"


def ensure_og_image_alt(text: str) -> str:
    head = text.split("</head>")[0]
    if 'property="og:image"' not in head or 'property="og:image:alt"' in head:
        return text
    alt = page_og_alt(text).replace('"', "&quot;")
    return re.sub(
        r'(<meta property="og:image" content="[^"]*">)',
        rf'\1\n<meta property="og:image:alt" content="{alt}">',
        text,
        count=1,
    )


def ensure_apple_touch_icon(text: str) -> str:
    if "apple-touch-icon" in text.split("</head>")[0]:
        return text
    if '<link rel="icon"' in text:
        return text.replace(
            '<link rel="icon"',
            APPLE_ICON + '\n<link rel="icon"',
            1,
        )
    return text.replace("</head>", APPLE_ICON + "\n</head>", 1)


def bump_date_modified(text: str) -> str:
    if '"dateModified"' not in text:
        return text
    return re.sub(
        r'"dateModified":\s*"\d{4}-\d{2}-\d{2}"',
        f'"dateModified": "{TODAY}"',
        text,
    )


def process_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_text(encoding="utf-8")
    text = original
    changes: list[str] = []

    if rel in TITLE_FIXES:
        old, new = TITLE_FIXES[rel]
        if old in text:
            text = text.replace(old, new, 1)
            changes.append("title")

    if rel in DESC_FIXES:
        old, new = DESC_FIXES[rel]
        if old in text:
            text = text.replace(old, new)
            changes.append("description")

    new_text = abs_schema_urls_loose(text)
    if new_text != text:
        changes.append("schema-urls")
        text = new_text

    new_text = ensure_og_image_alt(text)
    if new_text != text:
        changes.append("og:image:alt")
        text = new_text

    new_text = ensure_apple_touch_icon(text)
    if new_text != text:
        changes.append("apple-touch-icon")
        text = new_text

    if rel in DESC_FIXES or rel in TITLE_FIXES:
        new_text = bump_date_modified(text)
        if new_text != text:
            changes.append("dateModified")
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

    # Verification
    issues = []
    for f in sorted(ROOT.rglob("*.html")):
        t = f.read_text()
        head = t.split("</head>")[0]
        rel = f.relative_to(ROOT).as_posix()
        m = re.search(r"<title>([^<]+)</title>", head)
        if m and len(m.group(1)) > 60:
            issues.append(f"title>60: {rel} ({len(m.group(1))})")
        m = re.search(r'name="description" content="([^"]+)"', head)
        if m and len(m.group(1)) > 160:
            issues.append(f"desc>160: {rel} ({len(m.group(1))})")
        if '"url": "/' in t or '"url":"/' in t:
            issues.append(f"schema rel url: {rel}")
        if 'property="og:image"' in head and 'property="og:image:alt"' not in head:
            issues.append(f"no og:image:alt: {rel}")
        if "apple-touch-icon" not in head:
            issues.append(f"no apple-touch-icon: {rel}")

    if issues:
        print("\nRemaining issues:")
        for i in issues:
            print(" ", i)
    else:
        print("\nAll pass-2 checks passed.")


if __name__ == "__main__":
    main()
