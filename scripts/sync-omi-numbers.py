#!/usr/bin/env python3
"""Riporta nelle pagine i numeri di data/omi-2026.json (unica fonte).

Come funziona:
  * ogni numero "agganciato" nell'HTML è scritto così:
        <span data-omi="comuni.milano.min">1.900</span>
    lo script rilegge il valore dal JSON e lo riscrive (formato 1.900);
    si possono usare espressioni semplici:  data-omi="milano.mediana*90|r10000"
  * il nastro dei valori in homepage è rigenerato tra
        <!-- omi:ticker:start --> ... <!-- omi:ticker:end -->
  * con --check (default anche dopo la scrittura) controlla le guide e segnala
    i numeri scritti a mano che non coincidono con il JSON.

Non tocca mai <head> (title, meta description, og:*): quelli si aggiornano a mano.
Uso:  python3 scripts/sync-omi-numbers.py           (scrive + controlla)
      python3 scripts/sync-omi-numbers.py --check   (solo controllo)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT / "data/omi-2026.json").read_text(encoding="utf-8"))

TICKER = [  # (etichetta, chiave nel JSON)
    ("Milano città", "comuni.milano"),
    ("Milano centro", "milano.centro_fascia_B"),
    ("Monza", "comuni.monza-brianza"),
    ("Bergamo", "comuni.bergamo"),
    ("Brescia", "comuni.brescia"),
    ("Como", "comuni.como"),
    ("Varese", "comuni.varese"),
    ("Lecco", "comuni.lecco"),
    ("Lodi", "comuni.lodi"),
    ("Pavia", "comuni.pavia"),
    ("Cremona", "comuni.cremona"),
    ("Mantova", "comuni.mantova"),
    ("Sondrio", "comuni.sondrio"),
]


def euro(n) -> str:
    return f"{int(round(n)):,}".replace(",", ".")


def get(path: str):
    node = D
    for part in path.split("."):
        node = node[part]
    return node


def evaluate(expr: str):
    expr, _, fmt = expr.partition("|")
    m = re.fullmatch(r"([\w.\-]+)(?:\*(\d+(?:\.\d+)?))?", expr.strip())
    if not m:
        raise ValueError(f"espressione data-omi non valida: {expr}")
    val = get(m.group(1))
    if m.group(2):
        val = val * float(m.group(2))
    if fmt.startswith("r"):
        step = int(fmt[1:])
        val = round(val / step) * step
    return euro(val)


def ticker_html() -> str:
    items = []
    for label, key in TICKER:
        v = get(key)
        items.append(f'    <div class="pv"><span class="pvd"></span>{label} <span class="pvv">{euro(v["min"])}–{euro(v["max"])} €/mq</span></div>')
    body = "\n".join(items)
    note = f'    <!-- Fonte: {D["fonte"]}, semestre {D["semestre"]}. Abitazioni civili, min stato normale – max stato ottimo. Generato da scripts/sync-omi-numbers.py -->'
    return f"<!-- omi:ticker:start -->\n{note}\n{body}\n{body}\n    <!-- omi:ticker:end -->"


def split_head(html: str):
    i = html.find("</head>")
    return (html[: i + 7], html[i + 7 :]) if i >= 0 else ("", html)


def write() -> int:
    changed = 0
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("scripts/", "docs/", "node_modules/")):
            continue
        html = path.read_text(encoding="utf-8")
        head, body = split_head(html)
        new = re.sub(r'(<span data-omi="([^"]+)">)[^<]*(</span>)', lambda m: m.group(1) + evaluate(m.group(2)) + m.group(3), body)
        if rel == "index.html":
            new = re.sub(r"<!-- omi:ticker:start -->.*?<!-- omi:ticker:end -->", lambda m: ticker_html(), new, flags=re.S)
        if new != body:
            path.write_text(head + new, encoding="utf-8")
            changed += 1
            print("aggiornato", rel)
    return changed


def check() -> int:
    problems = []
    for slug, c in D["comuni"].items():
        p = ROOT / f"guide/prezzi-mq-{slug}/index.html"
        if not p.exists():
            continue
        _, body = split_head(p.read_text(encoding="utf-8"))
        vs = [re.sub(r"<[^>]+>", "", v) for v in re.findall(r'<div class="v">(.*?)</div>', body)[:3]]
        want = [f"€ {euro(c['min'])}", f"€ {euro(c['mediana'])}", f"€ {euro(c['max'])}"]
        if vs and vs != want:
            problems.append(f"{slug}: riquadri {vs} ≠ OMI {want}")
    # Milano: tabella zone e minimo citato nel testo
    p = ROOT / "guide/prezzi-mq-milano/index.html"
    full = p.read_text(encoding="utf-8")
    m = D["milano"]
    lo = euro(m["min"])
    for wrong in re.findall(r"(\d\.\d{3}) (?:€/m² )?in periferia", full):
        if wrong != lo:
            problems.append(f"milano: minimo in periferia {wrong} ≠ OMI {lo}")
    rows = re.findall(r'<tr><td>([^<]+)</td><td class="num">€ ([\d.]+) – ([\d.]+)</td></tr>', full)
    pairs = {(euro(z["min"]), euro(z["max"])) for z in m["zone_dettaglio"]}
    for name, a, b in rows:
        if (a, b) not in pairs:
            problems.append(f"milano tabella: {name} € {a} – {b} non trovato nei dati OMI")
    if len(rows) != m["zone"]:
        problems.append(f"milano tabella: {len(rows)} righe, zone OMI {m['zone']}")
    for line in problems:
        print("!!", line)
    print(f"controllo: {len(problems)} incongruenze")
    return len(problems)


if __name__ == "__main__":
    if "--check" not in sys.argv:
        write()
    sys.exit(1 if check() else 0)
