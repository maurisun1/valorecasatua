#!/usr/bin/env python3
"""Rigenera tabelle/fasce delle guide prezzi mq dai JSON OMI AdE (2025/2)."""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OMI_MI = json.loads((ROOT / "data/omi/milano-2025-2.json").read_text(encoding="utf-8"))
OMI_LO = json.loads((ROOT / "data/omi/lombardia-2025-2.json").read_text(encoding="utf-8"))
SEMESTER_LABEL = "2° semestre 2025"
ELAB = OMI_MI.get("elaborated", "23/05/2026")
UPDATE_LABEL = "4 agosto 2026"
DATE_MOD = "2026-08-04"

# Capoluoghi / comuni guida → (prov code in OMI, comuneName UPPER)
GUIDES = {
    "prezzi-mq-milano": {"comune": "MILANO", "prov": "MI", "use_milano_file": True, "full_table": True},
    "prezzi-mq-bergamo": {"comune": "BERGAMO", "prov": "BG"},
    "prezzi-mq-brescia": {"comune": "BRESCIA", "prov": "BS"},
    "prezzi-mq-como": {"comune": "COMO", "prov": "CO"},
    "prezzi-mq-cremona": {"comune": "CREMONA", "prov": "CR"},
    "prezzi-mq-lecco": {"comune": "LECCO", "prov": "LC"},
    "prezzi-mq-lodi": {"comune": "LODI", "prov": "LO"},
    "prezzi-mq-mantova": {"comune": "MANTOVA", "prov": "MN"},
    "prezzi-mq-monza-brianza": {"comune": "MONZA", "prov": "MI"},
    "prezzi-mq-pavia": {"comune": "PAVIA", "prov": "PV"},
    "prezzi-mq-sondrio": {"comune": "SONDRIO", "prov": "SO"},
    "prezzi-mq-varese": {"comune": "VARESE", "prov": "VA"},
    "prezzi-mq-seregno": {"comune": "SEREGNO", "prov": "MI", "city": True},
    "prezzi-mq-vimercate": {"comune": "VIMERCATE", "prov": "MI", "city": True},
    "prezzi-mq-treviglio": {"comune": "TREVIGLIO", "prov": "BG", "city": True},
    "prezzi-mq-sesto-san-giovanni": {"comune": "SESTO SAN GIOVANNI", "prov": "MI", "city": True},
    "prezzi-mq-legnano": {"comune": "LEGNANO", "prov": "MI", "city": True},
    "prezzi-mq-cinisello-balsamo": {"comune": "CINISELLO BALSAMO", "prov": "MI", "city": True},
    "prezzi-mq-rho": {"comune": "RHO", "prov": "MI", "city": True},
    "prezzi-mq-lissone": {"comune": "LISSONE", "prov": "MI", "city": True},
    "prezzi-mq-paderno-dugnano": {"comune": "PADERNO DUGNANO", "prov": "MI", "city": True},
    "prezzi-mq-segrate": {"comune": "SEGRATE", "prov": "MI", "city": True},

}


def euro(n: int) -> str:
    return f"{int(n):,}".replace(",", ".")


def nice_name(name: str) -> str:
    s = name.replace("`", "'").strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("SANBABILA", "SAN BABILA")
    keep_upper = {"XX", "IBM", "OMI", "USA", "UE"}
    small = {"E", "DI", "DEL", "DELLA", "DELLE", "DEI", "DA", "A", "AL", "ALLA", "PER", "CON"}
    special = {
        "VIA": "Via", "VIALE": "Viale", "V.LE": "V.le", "P.LE": "P.le", "C.NA": "C.na",
        "CITTA": "Città", "CITTÀ": "Città", "CENTRO": "Centro", "STORICO": "Storico", "ZONA": "Zona",
        "SANT'AMBROGIO": "Sant'Ambrogio", "UNIVERSITA": "Università",
    }

    def fix_token(tok: str, idx: int) -> str:
        comma = tok.endswith(",")
        raw = tok[:-1] if comma else tok
        if not raw:
            return "," if comma else ""
        up = raw.upper()
        if up in keep_upper or re.fullmatch(r"[A-Z]\d+", up):
            out = up
        elif up in special:
            out = special[up]
        elif up.replace("À", "A") in small and idx > 0:
            out = raw.lower()
        elif re.fullmatch(r"X{1,3}|IX|IV|V?I{0,3}", up) and len(raw) <= 4:
            out = up
        else:
            out = raw[:1].upper() + raw[1:].lower()
        return out + ("," if comma else "")

    parts = [fix_token(w, i) for i, w in enumerate(s.split(" "))]
    out = " ".join(p for p in parts if p)
    out = out.replace(" - ", " – ").replace(" :", ":")
    out = re.sub(r"\s+,", ",", out)
    out = re.sub(r"Centro Storico\s*[–-]\s*([a-z])", lambda m: "Centro Storico – " + m.group(1).upper(), out)
    out = re.sub(r"\s{2,}", " ", out)
    return out


def zone_range(feat: dict) -> tuple[int, int] | None:
    norms, otts = [], []
    for q in feat.get("quotes", []):
        if q.get("tipologia") != "Abitazioni civili":
            continue
        if q.get("stato") == "NORMALE":
            norms.append((q["min"], q["max"]))
        elif q.get("stato") == "OTTIMO":
            otts.append((q["min"], q["max"]))
    if not norms and not otts:
        return None
    lo = min(x[0] for x in (norms or otts))
    hi = max(x[1] for x in (otts or norms))
    return int(lo), int(hi)


def features_for(cfg: dict) -> list[dict]:
    if cfg.get("use_milano_file"):
        return list(OMI_MI["features"])
    return [
        f
        for f in OMI_LO["features"]
        if f.get("comuneName") == cfg["comune"] and f.get("prov") == cfg["prov"]
    ]


def civil_zones(feats: list[dict]) -> list[tuple[str, int, int]]:
    rows = []
    for f in feats:
        r = zone_range(f)
        if not r:
            continue
        rows.append((nice_name(f["name"]), r[0], r[1]))
    rows.sort(key=lambda x: (-x[2], -x[1], x[0]))
    return rows


def comune_range(comune: str, prov: str | None = None) -> tuple[int, int, int] | None:
    feats = [
        f
        for f in OMI_LO["features"]
        if f.get("comuneName") == comune.upper() and (prov is None or f.get("prov") == prov)
    ]
    if comune.upper() == "MILANO":
        feats = OMI_MI["features"]
    zs = civil_zones(feats)
    if not zs:
        return None
    return zs[-1][1] if False else (min(z[1] for z in zs), max(z[2] for z in zs), len(zs))


def stats(rows: list[tuple[str, int, int]]) -> dict:
    lo = min(r[1] for r in rows)
    hi = max(r[2] for r in rows)
    mids = [(r[1] + r[2]) / 2 for r in rows]
    med = int(statistics.median(mids))
    return {"lo": lo, "hi": hi, "med": med, "n": len(rows)}


def build_tbody(rows: list[tuple[str, int, int]]) -> str:
    parts = []
    for name, lo, hi in rows:
        parts.append(f'<tr><td>{name}</td><td class="num">€ {euro(lo)} – {euro(hi)}</td></tr>')
    return "".join(parts)


def replace_tbody(html: str, tbody_inner: str) -> str:
    # Replace first omi-table tbody
    def repl(m):
        return m.group(1) + tbody_inner + m.group(3)

    new, n = re.subn(
        r'(<table class="omi-table">\s*<thead>.*?</thead>\s*<tbody>)(.*?)(</tbody>\s*</table>)',
        repl,
        html,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("omi-table tbody not found/unique")
    return new


def replace_stat_cards(html: str, st: dict, labels: tuple[str, str, str]) -> str:
    block = (
        f'<div class="stat-cards">\n'
        f'    <div class="sc"><div class="v">€ {euro(st["lo"])}</div><div class="l">{labels[0]}</div></div>\n'
        f'    <div class="sc"><div class="v">€ {euro(st["med"])}</div><div class="l">{labels[1]}</div></div>\n'
        f'    <div class="sc"><div class="v">€ {euro(st["hi"])}</div><div class="l">{labels[2]}</div></div>\n'
        f'  </div>'
    )
    new, n = re.subn(r'<div class="stat-cards">.*?</div>\s*</div>\s*(?=\s*<p class="src-note">)', block + "\n  ", html, count=1, flags=re.S)
    # fallback simpler
    if n != 1:
        new, n = re.subn(r'<div class="stat-cards">.*?</div>\n  </div>', block, html, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("stat-cards not replaced")
    return new


def update_qa_comuni(html: str) -> tuple[str, int]:
    """Aggiorna i range € nei box .qa quando il comune esiste nel JSON."""
    count = 0

    def repl(m):
        nonlocal count
        full = m.group(0)
        inner_h3 = m.group(1)
        # extract plain comune name
        name = re.sub(r"<[^>]+>", "", inner_h3).strip()
        # drop trailing notes
        name_clean = re.sub(r"\s+", " ", name)
        key = name_clean.upper()
        # special accents / aliases
        aliases = {
            "ROMANO DI LOMBARDIA": "ROMANO DI LOMBARDIA",
            "CARATE BRIANZA": "CARATE BRIANZA",
        }
        key = aliases.get(key, key)
        rng = None
        # try exact
        for fprov in (None,):
            feats = [f for f in OMI_LO["features"] if f.get("comuneName") == key]
            zs = civil_zones(feats)
            if zs:
                rng = (min(z[1] for z in zs), max(z[2] for z in zs))
                break
        if not rng:
            return full
        lo, hi = rng
        # replace first € a – b pattern in the <p>
        def prep(pm):
            return f"€ {euro(lo)} – {euro(hi)}"

        new_full, n = re.subn(r"€\s*[\d\.]+\s*[–\-]\s*[\d\.]+", prep, full, count=1)
        if n:
            count += 1
        return new_full

    html2 = re.sub(
        r'<div class="qa"><h3>(.*?)</h3><p>(.*?)</p></div>',
        repl,
        html,
        flags=re.S,
    )
    return html2, count


def patch_ranges_in_text(html: str, st: dict, display_name: str) -> str:
    """Aggiorna le fasce tipiche da X a Y nei testi principali (lead, quick, FAQ, meta)."""
    lo, hi, med, n = st["lo"], st["hi"], st["med"], st["n"]

    # dateModified in JSON-LD Article if present
    html = re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"', f'"dateModified":"{DATE_MOD}"', html, count=2)

    # Aggiornamento footer quick answer
    html = re.sub(
        r"Aggiornamento:\s*\d{1,2} agosto 2026",
        f"Aggiornamento: {UPDATE_LABEL}",
        html,
    )

    # Zone count notes
    html = re.sub(
        r"Le \d+ zone residenziali",
        f"Le {n} zone residenziali",
        html,
    )
    html = re.sub(
        r"su \d+ zone",
        f"su {n} zone",
        html,
    )
    html = re.sub(
        r"\d+ zone residenziali rilevate",
        f"{n} zone residenziali rilevate",
        html,
    )
    html = re.sub(
        r"Selezione di \d+ zone rappresentative sulle \d+ residenziali rilevate\.",
        f"Tutte le {n} zone OMI con quotazione abitazioni civili. Dati OMI {display_name}, {SEMESTER_LABEL}.",
        html,
    )
    html = re.sub(
        r"Dati OMI ufficiali su \d+ zone",
        f"Dati OMI ufficiali su {n} zone",
        html,
    )

    # Common min–max patterns with euro formatting variants
    # Prefer conservative replacements for the overall comune range in strong/lead
    # Pattern: da circa € X/m² ... € Y/m²  OR tra circa € X e € Y
    def sub_pair(pattern, repl, text, flags=0):
        return re.sub(pattern, repl, text, flags=flags)

    # Quick/lead style "da circa € 1.400/m² ... € 4.300/m²"
    html = sub_pair(
        r"da circa €\s*[\d\.]+/m²([^€]{0,80})€\s*[\d\.]+/m²",
        lambda m: f"da circa € {euro(lo)}/m²{m.group(1)}€ {euro(hi)}/m²",
        html,
        flags=re.I,
    )
    html = sub_pair(
        r"tra circa €\s*[\d\.]+\s*e\s*€\s*[\d\.]+/m²",
        f"tra circa € {euro(lo)} e € {euro(hi)}/m²",
        html,
        flags=re.I,
    )
    html = sub_pair(
        r"indicativamente tra circa €\s*[\d\.]+\s*e\s*€\s*[\d\.]+/m²",
        f"indicativamente tra circa € {euro(lo)} e € {euro(hi)}/m²",
        html,
        flags=re.I,
    )
    html = sub_pair(
        r"fascia OMI indicativa tra circa €\s*[\d\.]+\s*e\s*€\s*[\d\.]+/m²",
        f"fascia OMI indicativa tra circa € {euro(lo)} e € {euro(hi)}/m²",
        html,
        flags=re.I,
    )

    # Meta descriptions: da €X a €Y/m²
    html = sub_pair(
        r"da €\s*[\d\.]+\s*a\s*€\s*[\d\.]+/m²",
        f"da €{euro(lo)} a €{euro(hi)}/m²",
        html,
    )
    html = sub_pair(
        r"fasce indicative da circa €\s*[\d\.]+/m² a €\s*[\d\.]+/m²",
        f"fasce indicative da circa €{euro(lo)}/m² a €{euro(hi)}/m²",
        html,
    )

    # FAQ plain numbers without thousand sep sometimes
    html = sub_pair(
        r"vanno da circa [\d\.]+ €/m²([^0-9]{0,60})[\d\.]+ €/m²",
        lambda m: f"vanno da circa {euro(lo)} €/m²{m.group(1)}{euro(hi)} €/m²",
        html,
    )
    html = sub_pair(
        r"tra circa [\d\.]+\s*e\s*[\d\.]+\s*€/m²",
        f"tra circa {euro(lo)} e {euro(hi)} €/m²",
        html,
    )
    html = sub_pair(
        r"si colloca indicativamente tra circa [\d\.]+\s*e\s*[\d\.]+\s*€/m²",
        f"si colloca indicativamente tra circa {euro(lo)} e {euro(hi)} €/m²",
        html,
    )

    # Mediana mentions
    html = sub_pair(
        r"mediane di zona intorno ai €\s*[\d\.]+/m²",
        f"mediane di zona intorno ai € {euro(med)}/m²",
        html,
    )
    html = sub_pair(
        r"valore mediano di zona intorno ai <strong>€\s*[\d\.]+/m²</strong>",
        f'valore mediano di zona intorno ai <strong>€ {euro(med)}/m²</strong>',
        html,
    )

    # Source elaborazione note for city pages missing it
    if "elaborazione 23/05/2026" not in html and "tipologia \"abitazioni civili\"" in html:
        html = html.replace(
            'tipologia "abitazioni civili". Elaborazione informativa ValoreCasaTua.it.',
            f'tipologia "abitazioni civili" · elaborazione {ELAB}.',
        )

    # Table header for city pages that said Ambito
    html = html.replace(
        "<th>Ambito</th><th class=\"num\">€/m² (indicativo)</th>",
        '<th>Zona OMI</th><th class="num">€/m² (normale → ottimo)</th>',
    )
    html = re.sub(
        r"Lettura sintetica a partire dalle fasce OMI comunali/provinciali\.[^<]*",
        f"Le {n} zone OMI del comune con quotazione abitazioni civili · {SEMESTER_LABEL}. ",
        html,
    )

    return html


def process(folder: str, cfg: dict) -> None:
    path = ROOT / "guide" / folder / "index.html"
    html = path.read_text(encoding="utf-8")
    feats = features_for(cfg)
    rows = civil_zones(feats)
    if not rows:
        raise RuntimeError(f"No civil zones for {folder}")
    st = stats(rows)
    display = cfg["comune"].title()

    html = replace_tbody(html, build_tbody(rows))

    if cfg.get("city"):
        labels = ("Fascia bassa OMI", "Mediana di zona", "Fascia alta OMI")
    elif folder == "prezzi-mq-milano":
        labels = (f"Minimo ({rows[-1][0].split(',')[0].split('–')[0].strip()})", "Mediana di zona", f"Massimo ({rows[0][0].split(',')[0].split('–')[0].strip()})")
    else:
        labels = (f"Minimo {display} città", "Mediana di zona", f"Massimo {display} città")

    html = replace_stat_cards(html, st, labels)
    html = patch_ranges_in_text(html, st, display)
    html, n_qa = update_qa_comuni(html)

    # Note under table
    html = re.sub(
        r'(<p class="src-note">)(Le \d+ zone residenziali di [^·]+· quotazioni OMI 2° semestre 2025\.)(</p>)',
        rf'\1Le {st["n"]} zone OMI di {display} con abitazioni civili · quotazioni {SEMESTER_LABEL} · elaborazione {ELAB}.\3',
        html,
        count=1,
    )

    path.write_text(html, encoding="utf-8")
    print(
        f"OK {folder}: {st['n']} zone · €{euro(st['lo'])}–{euro(st['hi'])} · med €{euro(st['med'])} · qa_updated={n_qa}"
    )


def main():
    for folder, cfg in GUIDES.items():
        process(folder, cfg)


if __name__ == "__main__":
    main()
