#!/usr/bin/env python3
"""Costruisce i JSON OMI 2026/1 a partire dallo zip AdE e dalle geometrie 2025/2.

Le quotazioni arrivano dal CSV. I poligoni restano quelli già usati dal form,
perché lo zip non contiene i confini. L'unico riaggancio esplicito: la zona
B1 di Lirio (comune soppresso) diventa B2 di Montalto Pavese, «abitato ex
comune di Lirio», con lo stesso poligono.
"""

from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "data/omi/lombardia-2025-2.json"
OUT = ROOT / "data/omi/lombardia-2026-1.json"
OUT_MI = ROOT / "data/omi/milano-2026-1.json"
ZIP = Path("/Users/mauriziopiraino/Downloads/QI1452126_PRNMZN64H30F205V.zip")

# Vecchio link Lirio B1 → nuova zona Montalto Pavese B2.
REMAP_POLYGON = {"PV00040487": "PV00000313"}


def rows(text: str) -> list[dict]:
    lines = text.splitlines()
    reader = csv.reader(lines[1:], delimiter=";")
    header = [cell.strip() for cell in next(reader)]
    return [dict(zip(header, row)) for row in reader if any(row)]


def num(raw: str) -> int | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    if "," in raw:
        raw = raw.replace(".", "").replace(",", ".")
    return int(round(float(raw)))


def clean_name(raw: str) -> str:
    name = (raw or "").strip()
    if len(name) >= 2 and name[0] == "'" and name[-1] == "'":
        name = name[1:-1]
    return " ".join(name.split())


def main() -> None:
    with zipfile.ZipFile(ZIP) as archive:
        valori = rows(archive.read("QI_1452126_1_20261_VALORI.csv").decode("latin-1"))
        zone = rows(archive.read("QI_1452126_1_20261_ZONE.csv").decode("latin-1"))

    old = json.loads(OLD.read_text(encoding="utf-8"))
    by_link = {feature["linkZona"]: feature for feature in old["features"]}
    zone_by_link = {row["LinkZona"]: row for row in zone}

    quotes: dict[str, list[dict]] = {}
    meta: dict[str, dict] = {}
    for row in valori:
        link = row["LinkZona"]
        meta[link] = row
        lo, hi = num(row["Compr_min"]), num(row["Compr_max"])
        if lo is None or hi is None:
            continue
        quotes.setdefault(link, []).append(
            {
                "tipologia": row["Descr_Tipologia"].strip(),
                "stato": row["Stato"].strip(),
                "statoPrev": row["Stato_prev"].strip(),
                "min": lo,
                "max": hi,
                "codTip": row["Cod_Tip"].strip(),
            }
        )

    features = []
    for feature in old["features"]:
        link = feature["linkZona"]
        if link not in zone_by_link and link not in REMAP_POLYGON.values():
            continue
        if link in REMAP_POLYGON.values():
            continue
        updated = dict(feature)
        if link in zone_by_link:
            info = zone_by_link[link]
            updated["name"] = clean_name(info["Zona_Descr"])
            updated["fascia"] = info["Fascia"].strip()
            updated["code"] = info["Zona"].strip()
        if link in quotes:
            updated["quotes"] = quotes[link]
        features.append(updated)

    for new_link, old_link in REMAP_POLYGON.items():
        source = by_link[old_link]
        info = zone_by_link[new_link]
        row = meta[new_link]
        features.append(
            {
                "prov": row["Prov"].strip(),
                "comuneCode": row["Comune_amm"].strip(),
                "comuneName": row["Comune_descrizione"].strip(),
                "code": info["Zona"].strip(),
                "name": clean_name(info["Zona_Descr"]),
                "fascia": info["Fascia"].strip(),
                "linkZona": new_link,
                "bbox": source["bbox"],
                "polygons": source["polygons"],
                "quotes": quotes.get(new_link, []),
            }
        )

    payload = {
        "source": "Agenzia Entrate - OMI",
        "semester": "2026/1",
        "elaborated": "18/10/2026",
        "scope": "LOMBARDIA",
        "features": features,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    milano = {
        "source": "Agenzia Entrate - OMI",
        "semester": "2026/1",
        "elaborated": "18/10/2026",
        "scope": "Comune di Milano",
        "comuneCat": "F205",
        "features": [
            {
                "code": feature["code"],
                "name": feature["name"],
                "bbox": feature["bbox"],
                "polygons": feature["polygons"],
                "quotes": feature["quotes"],
            }
            for feature in features
            if feature.get("comuneName") == "MILANO"
        ],
    }
    OUT_MI.write_text(json.dumps(milano, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"lombardia {len(features)} zone -> {OUT.name}")
    print(f"milano {len(milano['features'])} zone -> {OUT_MI.name}")


if __name__ == "__main__":
    main()
