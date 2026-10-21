#!/usr/bin/env python3
"""Apply neutral-portal coherence fixes site-wide."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

OLD_LEGAL = (
    '<div class="vct-legal"><p>'
    'Editore: Maurizio Piraino P.IVA 14597560961 · <a href="mailto:info@valorecasatua.it">info@valorecasatua.it</a>'
    "</p></div>"
)
NEW_LEGAL = (
    '<div class="vct-legal"><p>'
    "Editore: Maurizio Piraino · P.IVA 14597560961 · "
    "Portale informativo — nessuna mediazione immobiliare tramite questo sito · "
    '<a href="mailto:info@valorecasatua.it">info@valorecasatua.it</a>'
    "</p></div>"
)

OLD_FOOT_DISC = (
    "ValoreCasaTua.it offre orientamento immobiliare e informativo. "
    "Le valutazioni sono indicative"
)
NEW_FOOT_DISC = (
    "ValoreCasaTua.it è un portale informativo e non svolge attività di mediazione immobiliare. "
    "Le valutazioni sono orientative"
)

FORM_DISC = (
    '<p class="vct-form-disc">Servizio informativo orientativo. '
    "Non costituisce perizia, proposta contrattuale, incarico o attività di mediazione "
    "immobiliare ai sensi della L. 39/1989.</p>\n    "
)

REPLACEMENTS = [
    ("Consulenza gratuita · Senza impegno", "Gratuito · Senza impegno"),
    ("Consulenza gratuita · Riservata", "Gratuito · Riservato"),
    ("Analisi gratuita · Riservata", "Gratuito · Riservato"),
    ("Analisi gratuita &middot; Riservata", "Gratuito · Riservato"),
    ("Richiedi la consulenza gratuita →", "Ricevi il riepilogo →"),
    ("Richiedi la consulenza gratuita &rarr;", "Ricevi il riepilogo →"),
    ("Richiedi l'analisi gratuita →", "Ricevi il riepilogo →"),
    ("Richiedi l'analisi gratuita &rarr;", "Ricevi il riepilogo →"),
    (
        "La prossima analisi pu&ograve; essere la tua",
        "Hai i numeri. Vuoi il passo successivo?",
    ),
    (
        "Stesso approccio: prima l'analisi, poi la vendita. Chiaro, riservato, senza pressioni.",
        "Gratuito · riservato · nessun obbligo",
    ),
]


def add_form_disclaimers(text: str) -> str:
    if "vct-form-disc" in text or "formspree.io" not in text:
        return text
    if "index.html" in text and 'id="btnSubmit"' in text:
        return text

    patterns = [
        r'(\s*)<button type="submit" class="vct-lead-btn">',
        r'(\s*)<button class="btn btn-primary btn-full" type="submit">',
    ]
    for pat in patterns:
        if re.search(pat, text):

            def repl(m: re.Match[str]) -> str:
                indent = m.group(1)
                return f"{indent}{FORM_DISC.strip()}\n{indent}<button" + m.group(0).split("<button", 1)[1]

            text, n = re.subn(pat, repl, text, count=1)
            if n:
                break
    return text


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text

    if OLD_LEGAL in text:
        text = text.replace(OLD_LEGAL, NEW_LEGAL)
    if OLD_FOOT_DISC in text:
        text = text.replace(OLD_FOOT_DISC, NEW_FOOT_DISC)
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = add_form_disclaimers(text)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for html in sorted(ROOT.rglob("*.html")):
        if process(html):
            n += 1
            print(html.relative_to(ROOT))
    print(f"\nUpdated {n} HTML files.")


if __name__ == "__main__":
    main()
