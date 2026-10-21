#!/usr/bin/env python3
"""Second pass: fix inline styles and page-specific dark remnants."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

DARK_OVERRIDE_OLD = """/* ===== DARK OVERRIDE ECOSISTEMA (vince sulle superfici chiare) ===== */
body{background:#0a1d2b!important;color:#eef4f3!important;font-family:'Hanken Grotesk',system-ui,sans-serif!important}
.hero{padding-top:48px!important}
.form-card{background:linear-gradient(165deg,rgba(255,255,255,.06),rgba(255,255,255,.02))!important;border-color:rgba(255,255,255,.12)!important;box-shadow:0 40px 90px rgba(0,0,0,.45)!important}
.fc-body{background:transparent!important}
.fg label{color:#e7ddca!important}
.fg input,.fg select{background:rgba(0,0,0,.24)!important;color:#eef4f3!important;border-color:rgba(255,255,255,.16)!important}
.fg input::placeholder{color:rgba(238,244,243,.4)!important}
.tcard{background:rgba(255,255,255,.04)!important;border-color:rgba(255,255,255,.12)!important}
.tcard span{color:#e7ddca!important}.tcard i{color:rgba(238,244,243,.55)!important}
.tcard.on{background:rgba(47,148,136,.16)!important;border-color:#2f9488!important}
.tcard.on i,.tcard.on span{color:#41b3a4!important}
.gdpr span{color:rgba(238,244,243,.6)!important}
.section-title,h1,h2,h3{color:#eef4f3!important}
.how-step h3{color:#eef4f3!important}.how-step p{color:rgba(238,244,243,.6)!important}
.fq-q{background:rgba(255,255,255,.04)!important;color:#eef4f3!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:12px!important;margin-bottom:8px!important}
.fq-q.open{background:rgba(47,148,136,.12)!important;color:#41b3a4!important}
.fq-a{background:transparent!important;color:rgba(238,244,243,.72)!important;border-top-color:rgba(255,255,255,.1)!important}
.fq-a strong{color:#fff!important}
.zcard-mobile{background:rgba(255,255,255,.05)!important;border-color:rgba(255,255,255,.12)!important;color:#eef4f3!important}
.benchmark-card,.proof-card,.panel-metric,.report-copy,.result,.tcard,.floating-chip{color:#eef4f3}
.benchmark-card,.proof-card,.result{background:rgba(255,255,255,.05)!important;border-color:rgba(255,255,255,.12)!important}
.hero-trust-row{color:rgba(238,244,243,.86)}
section{background:transparent!important}
/* la mappa Leaflet resta chiara: incorniciata, fa contrasto col navy */
.panel-map,#map,.leaflet-container{border:1px solid rgba(255,255,255,.14)!important;border-radius:18px!important}
/* --- PATCH: contenitori rimasti chiari --- */
.faq,.how,.map-section,.form-section,.form-card-section{background:transparent!important}
.fq{background:rgba(255,255,255,.05)!important;border-color:rgba(255,255,255,.12)!important}
.fq:hover{border-color:#2f9488!important}
.fq-q{background:transparent!important;color:#eef4f3!important}
.fq-q.open{background:rgba(47,148,136,.12)!important;color:#41b3a4!important}
.fq-q i{color:rgba(238,244,243,.55)!important}
.fq-a{background:transparent!important;color:rgba(238,244,243,.74)!important;border-top-color:rgba(255,255,255,.1)!important}
.fq-a strong{color:#fff!important}
.rm,.ai-box{background:rgba(255,255,255,.05)!important;border-color:rgba(255,255,255,.12)!important;color:#eef4f3!important}
.pill{background:rgba(255,255,255,.08)!important;color:#e7ddca!important;border-color:rgba(255,255,255,.14)!important}
.map-legend,.ms-pill{background:rgba(10,29,43,.92)!important;border-color:rgba(255,255,255,.16)!important;color:#eef4f3!important}
.ms-l{color:rgba(238,244,243,.6)!important}
/* card "report" dell'hero: restano chiare ma testo scuro leggibile */
.panel-card,.report-mock,.mock-cell,.panel-metric,.premium-strip,.floating-chip,.benchmark-card{color:#16242f!important}
.map-section-label{background:transparent!important;color:rgba(238,244,243,.6)!important}"""

DARK_OVERRIDE_NEW = """/* ===== LIGHT THEME — sezioni sotto il form ===== */
body{background:#faf8f4!important;color:#1a2e3b!important;font-family:'Hanken Grotesk',system-ui,sans-serif!important}
.hero{padding-top:48px!important}
.section-title,h1,h2,h3{color:#0c2334!important}
.how-step h3{color:#0c2334!important}.how-step p{color:rgba(26,46,59,.72)!important}
.fq-q{background:#fff!important;color:#1a2e3b!important;border:1px solid rgba(12,35,52,.10)!important;border-radius:12px!important;margin-bottom:8px!important}
.fq-q.open{background:rgba(47,148,136,.10)!important;color:#1a7a6f!important}
.fq-a{background:transparent!important;color:rgba(26,46,59,.78)!important;border-top-color:rgba(12,35,52,.10)!important}
.fq-a strong{color:#0c2334!important}
.benchmark-card,.proof-card,.result{background:#fff!important;border-color:rgba(12,35,52,.10)!important;color:#1a2e3b!important}
.hero-trust-row{color:rgba(26,46,59,.82)}
section{background:transparent!important}
.panel-map,#map,.leaflet-container{border:1px solid rgba(12,35,52,.12)!important;border-radius:18px!important}
.faq,.how,.map-section,.form-section,.form-card-section{background:transparent!important}
.fq{background:#fff!important;border-color:rgba(12,35,52,.10)!important}
.fq:hover{border-color:#2f9488!important}
.fq-q{background:transparent!important;color:#1a2e3b!important}
.fq-q.open{background:rgba(47,148,136,.10)!important;color:#1a7a6f!important}
.fq-q i{color:rgba(26,46,59,.55)!important}
.rm,.ai-box{background:#fff!important;border-color:rgba(12,35,52,.10)!important;color:#1a2e3b!important}
.pill{background:#fff!important;color:#1a2e3b!important;border-color:rgba(12,35,52,.12)!important}
.map-legend,.ms-pill{background:#fff!important;border-color:rgba(12,35,52,.12)!important;color:#1a2e3b!important;box-shadow:0 4px 16px rgba(12,35,52,.08)!important}
.ms-l{color:rgba(26,46,59,.65)!important}
.panel-card,.report-mock,.mock-cell,.panel-metric,.premium-strip,.floating-chip,.benchmark-card{color:#16242f!important}
.map-section-label{background:transparent!important;color:rgba(26,46,59,.65)!important}"""

REPLACEMENTS = [
    (DARK_OVERRIDE_OLD, DARK_OVERRIDE_NEW),
    (".scroll-hint{color:rgba(238,244,243,.74)!important", ".scroll-hint{color:rgba(26,46,59,.72)!important"),
    (".guide-hero h1{font-family:var(--ff-serif,'Playfair Display',Georgia,serif);font-size:clamp(30px,5.2vw,52px);font-weight:600;line-height:1.1;color:#fff;margin-bottom:20px}",
     ".guide-hero h1{font-family:var(--ff-serif,'Playfair Display',Georgia,serif);font-size:clamp(30px,5.2vw,52px);font-weight:600;line-height:1.1;color:var(--ink);margin-bottom:20px}"),
    (".guide-hero .lead{max-width:780px;font-size:clamp(16px,2.2vw,19px);line-height:1.7;color:rgba(238,244,243,.84)}",
     ".guide-hero .lead{max-width:780px;font-size:clamp(16px,2.2vw,19px);line-height:1.7;color:var(--text-soft)}"),
    (".stat-cards .sc{background:#0f2636;border:1px solid rgba(201,164,92,.22);border-radius:14px;padding:22px 16px;text-align:center}",
     ".stat-cards .sc{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px 16px;text-align:center;box-shadow:0 4px 16px rgba(12,35,52,.06)}"),
    (".stat-cards .v{font-family:var(--ff-serif,'Playfair Display',serif);font-size:clamp(22px,3.4vw,30px);color:#c9a45c;font-weight:600;line-height:1.1}",
     ".stat-cards .v{font-family:var(--ff-serif,'Playfair Display',serif);font-size:clamp(22px,3.4vw,30px);color:var(--gold-bright);font-weight:600;line-height:1.1}"),
    (".stat-cards .l{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#8aa0ac;margin-top:8px}",
     ".stat-cards .l{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-top:8px}"),
    (".omi-table{width:100%;border-collapse:collapse;margin-top:18px;font-size:15px;overflow:hidden;border-radius:14px;border:1px solid rgba(255,255,255,.08)}",
     ".omi-table{width:100%;border-collapse:collapse;margin-top:18px;font-size:15px;overflow:hidden;border-radius:14px;border:1px solid var(--line)}"),
    (".omi-table th{background:#0f2636;color:#eef4f3;text-align:left;padding:13px 16px;font-weight:600;font-size:13px;letter-spacing:.04em;text-transform:uppercase}",
     ".omi-table th{background:var(--cream);color:var(--ink);text-align:left;padding:13px 16px;font-weight:600;font-size:13px;letter-spacing:.04em;text-transform:uppercase}"),
    (".omi-table td{padding:12px 16px;border-top:1px solid rgba(255,255,255,.06);color:rgba(238,244,243,.86)}",
     ".omi-table td{padding:12px 16px;border-top:1px solid var(--line);color:var(--text)}"),
    (".omi-table td.num{text-align:right;color:#fff;white-space:nowrap;font-variant-numeric:tabular-nums}",
     ".omi-table td.num{text-align:right;color:var(--ink);white-space:nowrap;font-variant-numeric:tabular-nums}"),
    (".omi-table tr:nth-child(even) td{background:rgba(255,255,255,.02)}",
     ".omi-table tr:nth-child(even) td{background:rgba(242,237,228,.5)}"),
    (".guide-prose p{color:rgba(238,244,243,.84);font-size:16px;line-height:1.8;margin-bottom:16px}",
     ".guide-prose p{color:var(--text-soft);font-size:16px;line-height:1.8;margin-bottom:16px}"),
    (".guide-prose strong{color:#fff;font-weight:600}",
     ".guide-prose strong{color:var(--ink);font-weight:600}"),
    (".qa h3{color:#fff;font-size:18px;margin-bottom:8px;font-weight:600}",
     ".qa h3{color:var(--ink);font-size:18px;margin-bottom:8px;font-weight:600}"),
    (".qa p{color:rgba(238,244,243,.8);line-height:1.75;margin:0}",
     ".qa p{color:var(--text-soft);line-height:1.75;margin:0}"),
    (".cap-box{background:linear-gradient(160deg,#0a1d2b,#143247);border:1px solid rgba(201,164,92,.28);border-radius:22px;padding:38px 28px;text-align:center;max-width:720px;margin:0 auto}",
     ".cap-box{background:linear-gradient(160deg,#f4efe6,#ebe5d9);border:1px solid rgba(139,105,20,.22);border-radius:22px;padding:38px 28px;text-align:center;max-width:720px;margin:0 auto}"),
    (".cap-box h2{font-family:var(--ff-serif,'Playfair Display',serif);font-weight:500;font-size:clamp(22px,3.2vw,30px);color:#f4efe6;margin-bottom:10px}",
     ".cap-box h2{font-family:var(--ff-serif,'Playfair Display',serif);font-weight:500;font-size:clamp(22px,3.2vw,30px);color:var(--ink);margin-bottom:10px}"),
    (".cap-box p{color:rgba(238,244,243,.78);max-width:540px;margin:0 auto 22px;line-height:1.7}",
     ".cap-box p{color:var(--text-soft);max-width:540px;margin:0 auto 22px;line-height:1.7}"),
    (".cap-box input{width:100%;padding:13px 15px;border-radius:11px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04);color:#fff;font-size:15px;font-family:inherit}",
     ".cap-box input{width:100%;padding:13px 15px;border-radius:11px;border:1px solid rgba(12,35,52,.14);background:#fff;color:var(--ink);font-size:15px;font-family:inherit}"),
    (".cap-box input::placeholder{color:#8aa0ac}",
     ".cap-box input::placeholder{color:var(--muted)}"),
    (".cap-box .priv{font-size:12px;color:#8aa0ac;margin:4px 0 0}",
     ".cap-box .priv{font-size:12px;color:var(--muted);margin:4px 0 0}"),
    (".guide-disc{max-width:780px;margin-top:14px;font-size:12.5px;line-height:1.6;color:#7d93a0}",
     ".guide-disc{max-width:780px;margin-top:14px;font-size:12.5px;line-height:1.6;color:var(--muted)}"),
    (".official-box p{color:rgba(238,244,243,.82);line-height:1.7;margin:0;font-size:15px}",
     ".official-box p{color:var(--text-soft);line-height:1.7;margin:0;font-size:15px}"),
    (".src-note{margin-top:18px;font-size:13px;color:#8aa0ac}",
     ".src-note{margin-top:18px;font-size:13px;color:var(--muted)}"),
    ('style="background:rgba(10,29,43,.6);border-top:1px solid rgba(201,164,92,.15)"',
     'style="background:var(--cream);border-top:1px solid var(--line)"'),
    ('style="display:block;text-decoration:none;background:rgba(255,255,255,.04);border:1px solid rgba(201,164,92,.18);border-radius:12px;padding:14px 18px"',
     'style="display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 18px;box-shadow:0 2px 12px rgba(12,35,52,.06)"'),
    ('<span style="color:#c9a45c;font-weight:600;font-size:14.5px">',
     '<span style="color:var(--gold-bright);font-weight:600;font-size:14.5px">'),
    ('style="color:#e0bd72;font-size:28px;letter-spacing:3px;line-height:1"',
     'style="color:var(--gold-bright);font-size:28px;letter-spacing:3px;line-height:1"'),
    ('style="background:linear-gradient(160deg,#0a1d2b,#143247);border:1px solid rgba(201,164,92,.28);border-radius:22px;padding:40px 30px;text-align:center"',
     'style="background:linear-gradient(160deg,#f4efe6,#ebe5d9);border:1px solid rgba(139,105,20,.22);border-radius:22px;padding:40px 30px;text-align:center"'),
    ('<h3 style="font-family:\'Playfair Display\',Georgia,serif;font-weight:500;font-size:clamp(24px,3.4vw,32px);color:#f4efe6;margin-bottom:12px">',
     '<h3 style="font-family:\'Playfair Display\',Georgia,serif;font-weight:500;font-size:clamp(24px,3.4vw,32px);color:var(--ink);margin-bottom:12px">'),
    ('<p style="color:rgba(238,244,243,.8);max-width:600px;margin:0 auto 24px;line-height:1.7"',
     '<p style="color:var(--text-soft);max-width:600px;margin:0 auto 24px;line-height:1.7"'),
    (".lead-form input::placeholder{color:rgba(238,244,243,.35)}",
     ".lead-form input::placeholder{color:rgba(26,46,59,.45)}"),
]

LIGHT_TEXT_MAP = {
    ".86": "rgba(26,46,59,.82)",
    ".84": "rgba(26,46,59,.80)",
    ".82": "rgba(26,46,59,.78)",
    ".8)": "rgba(26,46,59,.78)",
    ".78": "rgba(26,46,59,.76)",
    ".74": "rgba(26,46,59,.72)",
    ".72": "rgba(26,46,59,.70)",
    ".7)": "rgba(26,46,59,.68)",
    ".62": "rgba(26,46,59,.62)",
    ".6)": "rgba(26,46,59,.60)",
    ".55": "rgba(26,46,59,.58)",
    ".5)": "rgba(26,46,59,.55)",
    ".4)": "rgba(26,46,59,.50)",
    ".35": "rgba(26,46,59,.45)",
}


def fix_light_text_rgba(text: str) -> str:
    for suffix, replacement in LIGHT_TEXT_MAP.items():
        text = text.replace(f"rgba(238,244,243,{suffix}", replacement)
    text = text.replace("color:#eef4f3", "color:var(--text)")
    text = text.replace("color:#e7ddca", "color:var(--ink)")
    return text


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = fix_light_text_rgba(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for html in sorted(ROOT.rglob("*.html")):
        if process_file(html):
            changed.append(html.relative_to(ROOT))
    print(f"Pass 2 updated {len(changed)} files")


if __name__ == "__main__":
    main()
