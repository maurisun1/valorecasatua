#!/usr/bin/env python3
"""Corregge schede, confronti e frasi rimaste sul semestre precedente."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = json.loads((ROOT / "data/omi/lombardia-2025-2.json").read_text(encoding="utf-8"))
NEW = json.loads((ROOT / "data/omi/lombardia-2026-1.json").read_text(encoding="utf-8"))


def euro(n: int) -> str:
    return f"{int(n):,}".replace(",", ".")


def civil_span(feat: dict) -> tuple[int, int] | None:
    norms, otts = [], []
    for quote in feat.get("quotes") or []:
        if quote.get("tipologia") != "Abitazioni civili":
            continue
        if quote.get("stato") == "NORMALE":
            norms.append((quote["min"], quote["max"]))
        elif quote.get("stato") == "OTTIMO":
            otts.append((quote["min"], quote["max"]))
    if not norms and not otts:
        return None
    lo = min(pair[0] for pair in (norms or otts))
    hi = max(pair[1] for pair in (otts or norms))
    return int(lo), int(hi)


def page_spans(data: dict) -> dict[str, tuple[int, int]]:
    acc: dict[str, list] = defaultdict(list)
    for feat in data["features"]:
        span = civil_span(feat)
        if span:
            acc[feat["comuneName"]].append(span)
    return {
        name: (min(a for a, _b in rows), max(b for _a, b in rows))
        for name, rows in acc.items()
    }


OLD_SPAN = page_spans(OLD)
NEW_SPAN = page_spans(NEW)
ALIASES = {
    "SALO": "SALO`",
    "TEMU": "TEMU`",
    "CASTIGLIONE DELLE STIVIERE": "CASTIGLIONE D STIVIERE",
}


def norm(name: str) -> str:
    name = name.upper().replace("’", "'").replace("`", "")
    for src, dst in (("À", "A"), ("È", "E"), ("É", "E"), ("Ì", "I"), ("Ò", "O"), ("Ù", "U")):
        name = name.replace(src, dst)
    return re.sub(r"[^A-Z0-9 ]", "", name)


BY_NORM = {}
for name, span in NEW_SPAN.items():
    BY_NORM[norm(name)] = name


def swap_stat_cards(html: str) -> str:
    def repl(match: re.Match) -> str:
        block = match.group(0)
        values = re.findall(r'(<div class="v">)€ [\d\.]+(</div>)', block)
        if len(values) != 3:
            return block
        nums = re.findall(r"€ [\d\.]+", block)
        if len(nums) != 3:
            return block
        order = [nums[0], nums[2], nums[1]]
        i = 0

        def one(m: re.Match) -> str:
            nonlocal i
            out = m.group(1) + order[i] + m.group(2)
            i += 1
            return out

        return re.sub(r'(<div class="v">)€ [\d\.]+(</div>)', one, block, count=3)

    return re.sub(r'<div class="stat-cards">.*?</div>\s*</div>\s*</div>', repl, html, count=1, flags=re.S)


def update_nearby(html: str) -> tuple[str, int]:
    pat = re.compile(
        r'(<div class="qa"><h3>)([^<]+)(</h3><p>€ )([\d\.]+)( – )([\d\.]+)( /m²</p></div>)'
    )
    count = 0

    def repl(match: re.Match) -> str:
        nonlocal count
        label = match.group(2)
        key = norm(label)
        official = ALIASES.get(key) or BY_NORM.get(key)
        if not official or official not in OLD_SPAN or official not in NEW_SPAN:
            return match.group(0)
        old_lo, old_hi = OLD_SPAN[official]
        new_lo, new_hi = NEW_SPAN[official]
        shown = (int(match.group(4).replace(".", "")), int(match.group(6).replace(".", "")))
        if shown != (old_lo, old_hi) or (old_lo, old_hi) == (new_lo, new_hi):
            return match.group(0)
        count += 1
        return (
            match.group(1) + label + match.group(3) + euro(new_lo)
            + match.group(5) + euro(new_hi) + match.group(7)
        )

    return pat.sub(repl, html), count


def must(html: str, old: str, new: str, n: int, path: Path) -> str:
    found = html.count(old)
    if found != n:
        raise SystemExit(f"{path}: attese {n} occorrenze, trovate {found} di {old[:80]!r}")
    return html.replace(old, new)


def main() -> None:
    for path in (ROOT / "guide").rglob("index.html"):
        html = path.read_text(encoding="utf-8")
        html = swap_stat_cards(html)
        html, n = update_nearby(html)
        if n:
            print(f"{path.parent.name}: {n} schede comuni")
        path.write_text(html, encoding="utf-8")

    fixes: dict[str, list[tuple[str, str, int]]] = {
        "guide/prezzi-mq-seregno/index.html": [
            (
                "Il minimo, 1.850 €/m², è solo cinquanta euro sopra l’altra zona; il massimo, 3.100, è il punto più alto pubblicato a Seregno.",
                "Il minimo, 2.050 €/m², è cento euro sotto l’altra zona; il massimo, 3.300, è il punto più alto pubblicato a Seregno.",
                1,
            ),
            (
                "Il pavimento è quasi identico all’altra zona; il soffitto è duecento euro più basso.",
                "Il pavimento è cento euro sopra l’altra zona; il soffitto è 350 euro più basso.",
                1,
            ),
            (
                "da <strong>€ 1.800</strong> a <strong>€ 3.100/m²</strong>",
                "da <strong>€ 2.050</strong> a <strong>€ 3.300/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-lissone/index.html": [
            (
                "L’ottimo pubblicato, 2.850, supera di cinquanta euro il centro urbano e di 250 la frazione Santa Margherita. Il minimo, 1.500, è cinquanta euro sotto il centro. È una fascia larga: 1.350 €/m² tra normale e ottimo.",
                "L’ottimo pubblicato, 2.900, supera di cinquanta euro il centro urbano e di 300 la frazione Santa Margherita. Il minimo, 1.600, è uguale a quello del centro. È una fascia larga: 1.300 €/m² tra normale e ottimo.",
                1,
            ),
            (
                "1.600–2.850 €/m². Pavimento più alto della periferia, soffitto appena più basso.",
                "1.600–2.850 €/m². Il minimo è pari a quello della periferia, il soffitto è cinquanta euro più basso.",
                1,
            ),
            (
                "Il tetto, 2.600, sta 200 euro sotto il centro e 250 sotto la periferia.",
                "Il tetto, 2.600, sta 250 euro sotto il centro e 300 sotto la periferia.",
                1,
            ),
            (
                "Sui massimi, no. La periferia arriva a 2.850 €/m², il centro urbano a 2.800. Il centro ha il minimo più alto: 1.550 contro 1.500. Santa Margherita resta sotto, 1.450–2.600.",
                "Sui massimi, no. La periferia arriva a 2.900 €/m², il centro urbano a 2.850. I minimi di periferia e centro sono pari, a 1.600. Santa Margherita resta sotto, 1.450–2.600.",
                2,
            ),
            (
                "da <strong>€ 1.450</strong> a <strong>€ 2.850/m²</strong>",
                "da <strong>€ 1.450</strong> a <strong>€ 2.900/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-legnano/index.html": [
            (
                "Il tetto, 3.200 €/m², sta 650 euro sopra la zona del castello e 850 sopra Edison e le provinciali. Il minimo, 1.600, è il più alto delle quattro fasce insieme a nessuna altra: le altre partono da 1.200 o da 1.400.",
                "Il tetto, 3.300 €/m², sta 650 euro sopra la zona del castello e 900 sopra Edison e le provinciali. Il minimo, 1.700, è il più alto delle quattro fasce: le altre partono da 1.300 o da 1.450.",
                1,
            ),
            (
                "da <strong>€ 1.200</strong> a <strong>€ 3.200/m²</strong>",
                "da <strong>€ 1.300</strong> a <strong>€ 3.300/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-sesto-san-giovanni/index.html": [
            (
                "Il minimo, 2.300 €/m², è già sopra il minimo di Cascina Gatti; il massimo, 3.800, è settecento euro sopra il tetto dell’altra zona.",
                "Il minimo, 2.400 €/m², è già sopra il minimo di Cascina Gatti; il massimo, 3.900, è settecento euro sopra il tetto dell’altra zona.",
                1,
            ),
            (
                "La zona OMI più alta (fino a 3.800 €/m²) è proprio quella di Rondò, Marelli e stazione.",
                "La zona OMI più alta (fino a 3.900 €/m²) è proprio quella di Rondò, Marelli e stazione.",
                2,
            ),
            (
                "da <strong>€ 1.950</strong> a <strong>€ 3.800/m²</strong>",
                "da <strong>€ 2.000</strong> a <strong>€ 3.900/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-rho/index.html": [
            (
                "Il massimo, 3.200 €/m², supera di cinquecento euro il tetto dell’altra zona. Il minimo, 1.850, è solo cinquanta euro sopra.",
                "Il massimo, 3.300 €/m², supera di 550 euro il tetto dell’altra zona. Il minimo, 1.900, è solo cinquanta euro sopra.",
                1,
            ),
            (
                "da <strong>€ 1.800</strong> a <strong>€ 3.200/m²</strong>",
                "da <strong>€ 1.850</strong> a <strong>€ 3.300/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-cinisello-balsamo/index.html": [
            (
                "Il massimo, 2.850 €/m², è il tetto del comune, duecento euro sopra l’altra zona. Il minimo, 1.700, è cento euro sotto.",
                "Il massimo, 3.100 €/m², è il tetto del comune, 400 euro sopra l’altra zona. Il minimo, 1.700, è 150 euro sotto.",
                1,
            ),
            (
                "da <strong>€ 1.700</strong> a <strong>€ 2.850/m²</strong>",
                "da <strong>€ 1.700</strong> a <strong>€ 3.100/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-paderno-dugnano/index.html": [
            (
                "Il massimo, 3.200 €/m², supera di 350 euro il centro. Il minimo, 1.650, è 150 euro sotto il centro.",
                "Il massimo, 3.200 €/m², supera di 250 euro il centro. Il minimo, 1.650, è 250 euro sotto il centro.",
                1,
            ),
        ],
        "guide/prezzi-mq-vimercate/index.html": [
            (
                "Il minimo è solo cento euro sotto le altre due zone",
                "Il minimo è solo cinquanta euro sotto le altre due zone",
                1,
            ),
            (
                "da <strong>€ 1.500</strong> a <strong>€ 3.300/m²</strong>",
                "da <strong>€ 1.550</strong> a <strong>€ 3.300/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-treviglio/index.html": [
            (
                "Il massimo, 1.900, sta sotto XX Settembre e molto sotto il centro. Il minimo, 1.350, coincide con la zona semicentrale.",
                "Il massimo, 1.950, sta sotto XX Settembre e molto sotto il centro. Il minimo, 1.400, è 50 euro sopra il minimo della zona semicentrale.",
                1,
            ),
            (
                "sopra le due periferie sul massimo (1.750 contro 1.700 a nord e 1.450 a sud).",
                "sopra le due periferie sul massimo (1.800 contro 1.700 a nord e 1.450 a sud).",
                1,
            ),
            (
                "Il massimo è di poco sotto il semicentro e cinquecento euro sotto via del Bosco.",
                "Il massimo è di poco sotto il semicentro e 250 euro sotto via del Bosco.",
                1,
            ),
        ],
        "guide/prezzi-mq-segrate/index.html": [
            (
                "È la fascia più alta, e non di poco: 2.800–4.400 €/m². Milano 2 è il quartiere pianificato a est di Milano, con i canali interni, costruito come città autonoma dentro il comune di Segrate. Non è il centro comunale e non è Novegro. Il minimo, 3.000 €/m², è già uguale o sopra il massimo di diverse altre zone di questa lista di comuni; il massimo, 4.600, è il tetto di Segrate. Lo scarto interno resta 1.600 €/m².",
                "È la fascia con il minimo più alto: 2.800–4.400 €/m². Milano 2 è il quartiere pianificato a est di Milano, con i canali interni, costruito come città autonoma dentro il comune di Segrate. Non è il centro comunale e non è Novegro. Il minimo, 2.800 €/m², è il più alto del comune; il massimo, 4.400, è il tetto di Segrate, alla pari con il centro. Lo scarto interno resta 1.600 €/m².",
                1,
            ),
            (
                "Nessuna altra etichetta di Segrate parte da 3.000.",
                "Nessun’altra etichetta di Segrate parte da 2.800.",
                1,
            ),
            (
                "Il tetto, 4.400, è duecento euro sotto Milano 2; il pavimento, 2.600, è quattrocento euro sotto.",
                "Il tetto, 4.400, è lo stesso di Milano 2; il pavimento, 2.600, è duecento euro sotto.",
                1,
            ),
            (
                "Il minimo, 2.400, è sopra Lavanderie e Redecesio; il massimo, 3.800, è sotto.",
                "Il minimo, 2.500, è sopra Lavanderie e Redecesio; il massimo, 3.800, è sotto.",
                1,
            ),
            (
                "Il massimo, 2.950, non arriva al minimo di Milano 2 (3.000). È lo scarto più leggibile del comune: quasi duemila euro tra il tetto di Novegro e il tetto di Milano 2.",
                "Il massimo, 3.200, supera il minimo di Milano 2 (2.800). Tra il tetto di Novegro e il tetto di Milano 2 restano 1.200 euro.",
                1,
            ),
            (
                "accetta un minimo ufficiale di 3.000 €/m²",
                "accetta un minimo ufficiale di 2.800 €/m²",
                1,
            ),
            (
                "con un tetto di 3.800, non di 4.600.",
                "con un tetto di 3.800, non di 4.400.",
                1,
            ),
            (
                "e la fascia che non raggiunge i 3.000.",
                "e un massimo di 3.200, sotto i tetti di Milano 2 e del centro.",
                1,
            ),
            (
                "se si parla di 4.600 o di 1.800 €/m².",
                "se si parla di 4.400 o di 1.800 €/m².",
                1,
            ),
            (
                "né i 4.600 di Milano 2.",
                "né i 4.400 di Milano 2.",
                1,
            ),
            (
                "la scelta della fascia, qui, sposta il tetto di oltre 1.500 €/m².",
                "la scelta della fascia, qui, sposta il tetto di 1.200 €/m².",
                1,
            ),
            (
                "da <strong>€ 1.800</strong> a <strong>€ 4.600/m²</strong>",
                "da <strong>€ 1.800</strong> a <strong>€ 4.400/m²</strong>",
                1,
            ),
        ],
        "guide/index.html": [
            (
                "Milano 2 sta in cima all’intervallo; la periferia verso Idroscalo e Novegro sta in fondo, e il suo massimo non raggiunge il minimo di Milano 2. In mezzo ci sono il centro con il Villaggio Ambrosiano, l’asse delle Lavanderie e Redecesio, e San Felice.",
                "Milano 2 e il centro con il Villaggio Ambrosiano arrivano entrambi a 4.400 €/m²; Milano 2 parte da 2.800, il centro da 2.600. La periferia verso Idroscalo e Novegro ha il minimo più basso (1.800) e un massimo di 3.200, sopra il minimo di Milano 2. In mezzo restano l’asse delle Lavanderie e Redecesio, e San Felice.",
                1,
            ),
        ],
        "guide/prezzi-mq-milano/index.html": [
            (
                "da €1.850/m² a oltre €16.000",
                "da €1.900/m² a €16.000",
                3,
            ),
            (
                "dai €1.850/m² delle periferie agli oltre €16.000/m² del centro",
                "dai €1.900/m² delle periferie ai €16.000/m² del centro",
                1,
            ),
            (
                "vanno da circa 1.850 €/m² nelle zone periferiche a oltre 16.000 €/m² in centro, con un valore mediano di zona intorno ai 4.950 €/m².",
                "vanno da circa 1.900 €/m² nelle zone periferiche a 16.000 €/m² in centro, con un valore mediano di zona intorno ai 5.025 €/m².",
                1,
            ),
            (
                "Quarto Oggiaro parte da circa 1.850 €/m²",
                "Quarto Oggiaro parte da circa 1.900 €/m²",
                1,
            ),
            (
                "da circa <strong>€ 1.850/m²</strong> in periferia a oltre <strong>€ 16.000/m²</strong> in centro, con mediane di zona intorno ai € 4.950/m².",
                "da circa <strong>€ 1.900/m²</strong> in periferia a <strong>€ 16.000/m²</strong> in centro, con mediane di zona intorno ai € 5.025/m².",
                1,
            ),
            (
                "da circa <strong>€ 1.850/m²</strong> nelle zone più periferiche a oltre <strong>€ 16.000/m²</strong> nel centro storico, con un valore mediano di zona intorno ai <strong>€ 4.950/m²</strong>.",
                "da circa <strong>€ 1.900/m²</strong> nelle zone più periferiche a <strong>€ 16.000/m²</strong> nel centro storico, con un valore mediano di zona intorno ai <strong>€ 5.025/m²</strong>.",
                1,
            ),
            (
                "vanno da ~€ 1.850/m² (periferie) a oltre € 16.000/m² (centro), con mediana di zona intorno a € 4.950/m².",
                "vanno da ~€ 1.900/m² (periferie) a € 16.000/m² (centro), con mediana di zona intorno a € 5.025/m².",
                1,
            ),
            (
                "Quarto Oggiaro, da circa € 1.850/m².",
                "Quarto Oggiaro, da circa € 1.900/m².",
                1,
            ),
            ("Minimo (Missaglia)", "Minimo (Quarto Oggiaro)", 1),
        ],
        "guide/prezzi-mq-monza-brianza/index.html": [
            (
                "vanno da circa 1.600 €/m² a 5.100 €/m²",
                "vanno da circa 1.700 €/m² a 5.500 €/m²",
                2,
            ),
            ("fino a circa 5.100 €/m²", "fino a circa 5.500 €/m²", 2),
            (
                "da circa € 1.600 a € 5.100/m²",
                "da circa € 1.700 a € 5.500/m²",
                1,
            ),
            ("Seregno a 2.750 €/m²", "Seregno a 3.000 €/m²", 2),
            (
                "da circa <strong>€ 1.600/m²</strong> ai <strong>€ 5.100/m²</strong>",
                "da circa <strong>€ 1.700/m²</strong> ai <strong>€ 5.500/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-pavia/index.html": [
            (
                "vanno da circa 1.200 €/m² a 4.200 €/m²",
                "vanno da circa 1.200 €/m² a 4.300 €/m²",
                2,
            ),
            ("fino a circa 4.200 €/m²", "fino a circa 4.300 €/m²", 2),
            (
                "da circa 2.100 €/m² a 4.200 €/m²",
                "da circa 2.200 €/m² a 4.300 €/m²",
                2,
            ),
            (
                "ai <strong>€ 4.200/m²</strong>",
                "ai <strong>€ 4.300/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-lodi/index.html": [
            (
                "vanno da circa 1.200 €/m² a 2.850 €/m²",
                "vanno da circa 1.250 €/m² a 3.000 €/m²",
                2,
            ),
            ("fino a circa 2.250 €/m²", "fino a circa 2.300 €/m²", 2),
            ("tra 790 e 1.600 €/m²", "tra 890 e 1.800 €/m²", 2),
            (
                "da circa <strong>€ 1.200/m²</strong> ai <strong>€ 2.850/m²</strong>",
                "da circa <strong>€ 1.250/m²</strong> ai <strong>€ 3.000/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-lecco/index.html": [
            (
                "vanno da circa 1.050 €/m² a 2.850 €/m²",
                "vanno da circa 1.100 €/m² a 2.900 €/m²",
                2,
            ),
            (
                "da circa <strong>€ 1.050/m²</strong> ai <strong>€ 2.850/m²</strong>",
                "da circa <strong>€ 1.100/m²</strong> ai <strong>€ 2.900/m²</strong>",
                1,
            ),
        ],
        "guide/prezzi-mq-cremona/index.html": [
            (
                "ai <strong>€ 2.500/m²</strong> del centro storico",
                "ai <strong>€ 2.550/m²</strong> del centro storico",
                1,
            ),
            (
                "ai € 2.500/m² del centro storico",
                "ai € 2.550/m² del centro storico",
                1,
            ),
        ],
    }

    for rel, pairs in fixes.items():
        path = ROOT / rel
        html = path.read_text(encoding="utf-8")
        for old, new, n in pairs:
            html = must(html, old, new, n, path)
        path.write_text(html, encoding="utf-8")
        print("prose", rel)


if __name__ == "__main__":
    main()
