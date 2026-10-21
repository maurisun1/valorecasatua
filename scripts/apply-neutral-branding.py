#!/usr/bin/env python3
"""Neutral portal branding: remove agent signals site-wide."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ORG_NEUTRAL = (
    '{"@type":"Organization","@id":"https://valorecasatua.it/#org",'
    '"name":"ValoreCasaTua.it",'
    '"url":"https://valorecasatua.it/",'
    '"logo":"https://valorecasatua.it/assets/logo-valorecasatua.jpg",'
    '"slogan":"Più informazioni. Più consapevolezza. Più valore.",'
    '"description":"Portale informativo per proprietari immobiliari in Lombardia: stime OMI, guide e strumenti di analisi.",'
    '"email":"info@valorecasatua.it",'
    '"foundingDate":"2026",'
    '"knowsAbout":["Valutazione immobiliare","Quotazioni OMI","Mercato immobiliare Lombardia","Documenti per la vendita immobiliare"],'
    '"areaServed":{"@type":"AdministrativeArea","name":"Lombardia"},'
    '"sameAs":["https://www.instagram.com/valorecasatua.it/","https://www.facebook.com/valorecasatua.it"]}'
)

RE_BLOCK = re.compile(
    r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*\[\s*"RealEstateAgent"[\s\S]*?</script>\s*',
    re.MULTILINE,
)


def strip_realestate_agent(text: str) -> str:
    return RE_BLOCK.sub("", text)


def neutralize_org_blocks(text: str) -> str:
    text = text.replace(
        '"knowsAbout":["Valutazione immobiliare","Quotazioni OMI","Mercato immobiliare della Lombardia","Mediazione immobiliare (Legge 39/1989)"]',
        '"knowsAbout":["Valutazione immobiliare","Quotazioni OMI","Mercato immobiliare Lombardia","Documenti per la vendita immobiliare"]',
    )
    text = text.replace(
        '"knowsAbout": ["Valutazione immobiliare", "Mercato immobiliare della Lombardia", "Mediazione immobiliare (Legge 39/1989)", "Rendimento da locazione", "Affitto breve, transitorio e 4+4"]',
        '"knowsAbout": ["Valutazione immobiliare", "Mercato immobiliare Lombardia", "Rendimento da locazione", "Affitto breve, transitorio e 4+4"]',
    )
    text = text.replace("Mediazione immobiliare (Legge 39/1989)", "")
    text = text.replace('"Mercato immobiliare della Lombardia"', '"Mercato immobiliare Lombardia"')
    text = re.sub(
        r'"https://www\.google\.com/maps/place/ValoreCasaTua\.it[^"]*",\s*',
        "",
        text,
    )
    text = re.sub(
        r',\s*"https://www\.google\.com/maps/place/ValoreCasaTua\.it[^"]*"',
        "",
        text,
    )
    text = re.sub(r'https://valorecasatua\.it/#org/', "https://valorecasatua.it/#org", text)
    text = re.sub(r',?"founder":\s*\{\s*"@id":\s*"https://valorecasatua\.it/#founder/?"\s*\}', "", text)
    text = re.sub(
        r'\{"@type":"Person","@id":\s*"https://valorecasatua\.it/#founder/?"[\s\S]*?\}(?=,|\])',
        "",
        text,
    )
    text = text.replace('"author":{"@id":"https://valorecasatua.it/#founder"}', '"author":{"@id":"https://valorecasatua.it/#org"}')
    text = text.replace('"author":{"@id": "https://valorecasatua.it/#founder"}', '"author":{"@id":"https://valorecasatua.it/#org"}')
    text = text.replace('"author": {"@id": "https://valorecasatua.it/#founder"}', '"author": {"@id": "https://valorecasatua.it/#org"}')
    text = text.replace(',,', ',')
    text = text.replace('[,', '[')
    text = text.replace(',]', ']')
    text = text.replace('["",', '["')
    text = text.replace(', "",', ',')
    text = text.replace(', ""]', ']')
    return text


def footer_label(text: str) -> str:
    return text.replace('>Chi Siamo</a>', '>Il progetto</a>')


def process_file(path: Path) -> list[str]:
    original = path.read_text(encoding="utf-8")
    text = original
    changes: list[str] = []

    new = strip_realestate_agent(text)
    if new != text:
        changes.append("removed-RealEstateAgent")
        text = new

    new = neutralize_org_blocks(text)
    if new != text:
        changes.append("neutral-org")
        text = new

    new = footer_label(text)
    if new != text:
        changes.append("footer-label")
        text = new

    if text != original:
        path.write_text(text, encoding="utf-8")
    return changes


def main() -> None:
    n = 0
    for html in sorted(ROOT.rglob("*.html")):
        ch = process_file(html)
        if ch:
            n += 1
            print(f"{html.relative_to(ROOT)}: {', '.join(ch)}")
    print(f"\nUpdated {n} files.")


if __name__ == "__main__":
    main()
