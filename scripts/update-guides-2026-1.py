#!/usr/bin/env python3
"""Aggiorna fasce e tabelle delle guide al semestre OMI 2026/1.

Non riscrive i testi. Sostituisce gli intervalli che coincidono con una zona
o con la fascia del comune, le tre cifre in evidenza e la data di aggiornamento.
"""

from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = json.loads((ROOT / "data/omi/lombardia-2025-2.json").read_text(encoding="utf-8"))
NEW = json.loads((ROOT / "data/omi/lombardia-2026-1.json").read_text(encoding="utf-8"))
OLD_MI = json.loads((ROOT / "data/omi/milano-2025-2.json").read_text(encoding="utf-8"))
NEW_MI = json.loads((ROOT / "data/omi/milano-2026-1.json").read_text(encoding="utf-8"))
DATE_ISO = "2026-10-19"
DATE_IT = "19 ottobre 2026"

GUIDES = {
    "prezzi-mq-milano": ("MILANO", "MI", True),
    "prezzi-mq-bergamo": ("BERGAMO", "BG", False),
    "prezzi-mq-brescia": ("BRESCIA", "BS", False),
    "prezzi-mq-como": ("COMO", "CO", False),
    "prezzi-mq-cremona": ("CREMONA", "CR", False),
    "prezzi-mq-lecco": ("LECCO", "LC", False),
    "prezzi-mq-lodi": ("LODI", "LO", False),
    "prezzi-mq-mantova": ("MANTOVA", "MN", False),
    "prezzi-mq-monza-brianza": ("MONZA", "MI", False),
    "prezzi-mq-pavia": ("PAVIA", "PV", False),
    "prezzi-mq-sondrio": ("SONDRIO", "SO", False),
    "prezzi-mq-varese": ("VARESE", "VA", False),
    "prezzi-mq-seregno": ("SEREGNO", "MI", False),
    "prezzi-mq-vimercate": ("VIMERCATE", "MI", False),
    "prezzi-mq-treviglio": ("TREVIGLIO", "BG", False),
    "prezzi-mq-sesto-san-giovanni": ("SESTO SAN GIOVANNI", "MI", False),
    "prezzi-mq-legnano": ("LEGNANO", "MI", False),
    "prezzi-mq-cinisello-balsamo": ("CINISELLO BALSAMO", "MI", False),
    "prezzi-mq-rho": ("RHO", "MI", False),
    "prezzi-mq-lissone": ("LISSONE", "MI", False),
    "prezzi-mq-paderno-dugnano": ("PADERNO DUGNANO", "MI", False),
    "prezzi-mq-segrate": ("SEGRATE", "MI", False),
}


def euro(n: int) -> str:
    return f"{int(n):,}".replace(",", ".")


def civil(feat: dict) -> tuple[int, int] | None:
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


def index(data: dict, milano: bool = False) -> dict[tuple, tuple[int, int]]:
    out = {}
    for feat in data["features"]:
        span = civil(feat)
        if not span:
            continue
        if milano:
            key = ("MI", "MILANO", feat["code"])
        else:
            key = (feat["prov"], feat["comuneName"], feat["code"])
        out[key] = span
    return out


OLD_IX = index(OLD)
OLD_IX.update(index(OLD_MI, True))
NEW_IX = index(NEW)
NEW_IX.update(index(NEW_MI, True))


def spans(comune: str, prov: str, milano: bool) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    keys = [key for key in NEW_IX if key[1] == comune and (milano or key[0] == prov)]
    pairs = []
    for key in keys:
        new_span = NEW_IX[key]
        old_span = OLD_IX.get(key)
        if old_span:
            pairs.append((old_span, new_span))
    return pairs


def formats(lo: int, hi: int) -> list[str]:
    a, b = euro(lo), euro(hi)
    return [
        f"€ {a} – {b} /m²",
        f"€ {a} – {b}/m²",
        f"€ {a}–{b}/m²",
        f"€{a}/m² a €{b}/m²",
        f"€ {a}/m² a € {b}/m²",
        f"€ {a}/m² e € {b}/m²",
        f"€{a}/m² e €{b}/m²",
        f"da circa €{a}/m² a €{b}/m²",
        f"da circa € {a}/m² a € {b}/m²",
        f"da €{a} a €{b}",
        f"da € {a} a € {b}",
        f"tra circa {a} e {b}",
        f"tra circa € {a} e € {b}",
        f"€ {a} – {b}",
        f"€{a} – {b}",
        f"{a}–{b}",
        f"{a} – {b}",
    ]


def stats(pairs_new: list[tuple[int, int]]) -> tuple[int, int, int]:
    lo = min(span[0] for span in pairs_new)
    hi = max(span[1] for span in pairs_new)
    mids = [(span[0] + span[1]) / 2 for span in pairs_new]
    med = int(statistics.median(mids))
    return lo, hi, med


def replace_ranges(html: str, mapping: list[tuple[tuple[int, int], tuple[int, int]]]) -> tuple[str, int]:
    jobs = []
    for old_span, new_span in mapping:
        if old_span == new_span:
            continue
        for old_fmt, new_fmt in zip(formats(*old_span), formats(*new_span)):
            jobs.append((old_fmt, new_fmt))
    jobs.sort(key=lambda item: len(item[0]), reverse=True)
    count = 0
    seen = set()
    for old_fmt, new_fmt in jobs:
        if old_fmt in seen or old_fmt == new_fmt:
            continue
        seen.add(old_fmt)
        found = html.count(old_fmt)
        if found:
            html = html.replace(old_fmt, new_fmt)
            count += found
    return html, count


def replace_stats(html: str, old_stats: tuple[int, int, int], new_stats: tuple[int, int, int]) -> str:
    old_lo, old_med, old_hi = old_stats
    new_lo, new_med, new_hi = new_stats
    pattern = re.compile(
        r'(<div class="stat-cards">\s*<div class="sc"><div class="v">)€ [\d\.]+'
        r'(</div>.*?<div class="v">)€ [\d\.]+'
        r'(</div>.*?<div class="v">)€ [\d\.]+'
        r'(</div>)',
        re.S,
    )
    match = pattern.search(html)
    if not match:
        return html
    block = match.group(0)
    if f"€ {euro(old_lo)}" not in block or f"€ {euro(old_hi)}" not in block:
        return html
    updated = (
        match.group(1) + f"€ {euro(new_lo)}"
        + match.group(2) + f"€ {euro(new_med)}"
        + match.group(3) + f"€ {euro(new_hi)}"
        + match.group(4)
    )
    return html[: match.start()] + updated + html[match.end() :]


def bump_dates(html: str) -> str:
    html = re.sub(r"Aggiornato il \d{1,2} [a-zà]+ 2026", f"Aggiornato il {DATE_IT}", html)
    html = re.sub(r'"dateModified"\s*:\s*"\d{4}-\d{2}-\d{2}"', f'"dateModified":"{DATE_ISO}"', html)
    html = html.replace("aggiornamento 2026", "1° semestre 2026")
    return html


def page_pairs(comune: str, prov: str, milano: bool) -> tuple[list, tuple, tuple]:
    zone_pairs = spans(comune, prov, milano)
    old_spans = [old for old, _new in zone_pairs]
    new_spans = [new for _old, new in zone_pairs]
    return zone_pairs, stats(old_spans), stats(new_spans)


def main() -> None:
    page_map = {}
    for folder, (comune, prov, milano) in GUIDES.items():
        path = ROOT / "guide" / folder / "index.html"
        html = path.read_text(encoding="utf-8")
        zone_pairs, old_stats, new_stats = page_pairs(comune, prov, milano)
        mapping = list(zone_pairs)
        if old_stats[:2] != new_stats[:2]:
            mapping.append((old_stats[:2], new_stats[:2]))
        html, n = replace_ranges(html, mapping)
        html = replace_stats(html, old_stats, new_stats)
        html = bump_dates(html)
        path.write_text(html, encoding="utf-8")
        page_map[folder] = (old_stats, new_stats, n)
        print(f"{folder}: {n} sostituzioni · € {euro(new_stats[0])}–{euro(new_stats[1])}")

    hub = ROOT / "guide" / "index.html"
    html = hub.read_text(encoding="utf-8")
    mapping = []
    for _folder, (old_stats, new_stats, _n) in page_map.items():
        if old_stats[:2] != new_stats[:2]:
            mapping.append((old_stats[:2], new_stats[:2]))
    html, n = replace_ranges(html, mapping)
    html = bump_dates(html)
    hub.write_text(html, encoding="utf-8")
    print(f"guide hub: {n} sostituzioni")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = ["https://valorecasatua.it/guide/"] + [
        f"https://valorecasatua.it/guide/{folder}/" for folder in GUIDES
    ]
    for loc in locs:
        sitemap = re.sub(
            rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)\d{{4}}-\d{{2}}-\d{{2}}(</lastmod>)",
            rf"\g<1>{DATE_ISO}\2",
            sitemap,
            count=1,
        )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("sitemap aggiornata")


if __name__ == "__main__":
    main()
