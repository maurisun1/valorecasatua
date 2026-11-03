#!/usr/bin/env python3
"""Crea data/omi-2026.json: l'UNICA fonte dei numeri €/m² mostrati sul sito.

Legge i file OMI completi (data/omi/*-2026-1.json, con poligoni) e salva un
riassunto leggero: province, comuni delle guide e zone di Milano.

Convenzione (la stessa delle guide): abitazioni civili; minimo = valore più
basso in stato NORMALE, massimo = valore più alto in stato OTTIMO; la mediana è
la mediana dei valori centrali delle zone del comune.

Dopo ogni nuovo semestre OMI: aggiornare i file in data/omi/, rilanciare questo
script e poi scripts/sync-omi-numbers.py.
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LO = json.loads((ROOT / "data/omi/lombardia-2026-1.json").read_text(encoding="utf-8"))
MI = json.loads((ROOT / "data/omi/milano-2026-1.json").read_text(encoding="utf-8"))
OUT = ROOT / "data/omi-2026.json"

PROVINCE = {"MI": "Milano (città metropolitana e Monza e Brianza, codifica OMI)", "BG": "Bergamo", "BS": "Brescia",
            "CO": "Como", "CR": "Cremona", "LC": "Lecco", "LO": "Lodi", "MN": "Mantova", "PV": "Pavia",
            "SO": "Sondrio", "VA": "Varese"}
CAPOLUOGHI = {"MI": "MILANO", "BG": "BERGAMO", "BS": "BRESCIA", "CO": "COMO", "CR": "CREMONA", "LC": "LECCO",
              "LO": "LODI", "MN": "MANTOVA", "PV": "PAVIA", "SO": "SONDRIO", "VA": "VARESE"}
# slug guida -> (prov OMI, comune)
GUIDE = {
    "milano": ("MI", "MILANO"), "bergamo": ("BG", "BERGAMO"), "brescia": ("BS", "BRESCIA"), "como": ("CO", "COMO"),
    "cremona": ("CR", "CREMONA"), "lecco": ("LC", "LECCO"), "lodi": ("LO", "LODI"), "mantova": ("MN", "MANTOVA"),
    "monza-brianza": ("MI", "MONZA"), "pavia": ("PV", "PAVIA"), "sondrio": ("SO", "SONDRIO"), "varese": ("VA", "VARESE"),
    "seregno": ("MI", "SEREGNO"), "vimercate": ("MI", "VIMERCATE"), "treviglio": ("BG", "TREVIGLIO"),
    "sesto-san-giovanni": ("MI", "SESTO SAN GIOVANNI"), "legnano": ("MI", "LEGNANO"),
    "cinisello-balsamo": ("MI", "CINISELLO BALSAMO"), "rho": ("MI", "RHO"), "lissone": ("MI", "LISSONE"),
    "paderno-dugnano": ("MI", "PADERNO DUGNANO"), "segrate": ("MI", "SEGRATE"),
}


def civil(feat):
    norms = [(q["min"], q["max"]) for q in feat.get("quotes") or [] if q.get("tipologia") == "Abitazioni civili" and q.get("stato") == "NORMALE"]
    otts = [(q["min"], q["max"]) for q in feat.get("quotes") or [] if q.get("tipologia") == "Abitazioni civili" and q.get("stato") == "OTTIMO"]
    if not norms and not otts:
        return None
    return int(min(p[0] for p in (norms or otts))), int(max(p[1] for p in (otts or norms)))


def summary(spans):
    if not spans:
        return None
    return {"min": min(s[0] for s in spans), "max": max(s[1] for s in spans),
            "mediana": int(statistics.median([(a + b) / 2 for a, b in spans])), "zone": len(spans)}


def clean(name):
    name = name.replace("`", "'")
    name = re.sub(r"\s*,\s*,\s*", ", ", name)   # "LIBIA, ,XXII MARZO" -> "LIBIA, XXII MARZO"
    name = re.sub(r"\s*,\s*", ", ", name)
    return re.sub(r"\s+", " ", name).strip()


def main():
    by_comune = {}
    for f in LO["features"]:
        s = civil(f)
        if s:
            by_comune.setdefault((f["prov"], f["comuneName"]), []).append((f, s))

    province = {}
    for prov, label in PROVINCE.items():
        spans = [s for (p, _), lst in by_comune.items() if p == prov for _, s in lst]
        cap = CAPOLUOGHI[prov]
        resto = [s for (p, c), lst in by_comune.items() if p == prov and c != cap for _, s in lst]
        province[prov] = {"nome": label, "tutta": summary(spans), "capoluogo": summary([s for _, s in by_comune.get((prov, cap), [])]),
                          "resto_provincia": summary(resto)}

    comuni = {}
    for slug, (prov, com) in GUIDE.items():
        lst = by_comune.get((prov, com), [])
        comuni[slug] = {"comune": com.title(), "prov": prov, **summary([s for _, s in lst])}

    fascia = {f["code"]: f.get("fascia") for f, _ in by_comune.get(("MI", "MILANO"), [])}
    zone = []
    for f in MI["features"]:
        s = civil(f)
        if not s:
            continue
        q = {x["stato"].lower(): [x["min"], x["max"]] for x in f["quotes"] if x["tipologia"] == "Abitazioni civili"}
        zone.append({"code": f["code"], "nome": clean(f["name"]), "fascia": fascia.get(f["code"]) or f["code"][0],
                     "min": s[0], "max": s[1], **q})
    zone.sort(key=lambda z: -z["max"])
    spans = [(z["min"], z["max"]) for z in zone]
    centro = [(z["min"], z["max"]) for z in zone if z["fascia"] == "B"]
    lo_z = min(zone, key=lambda z: z["min"])
    hi_z = max(zone, key=lambda z: z["max"])
    milano = {**summary(spans), "zona_min": lo_z["nome"], "zona_max": hi_z["nome"],
              "centro_fascia_B": summary(centro), "zone_dettaglio": zone}

    out = {
        "fonte": "Agenzia Entrate - OMI",
        "semestre": LO.get("semester"),
        "elaborazione": LO.get("elaborated"),
        "convenzione": "Abitazioni civili, €/m². min = valore più basso in stato NORMALE; max = valore più alto in stato OTTIMO; mediana = mediana dei valori centrali delle zone.",
        "province": province,
        "comuni": comuni,
        "milano": milano,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("scritto", OUT.relative_to(ROOT), f"({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
