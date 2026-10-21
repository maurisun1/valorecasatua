#!/usr/bin/env python3
"""Apply light theme across all ValoreCasaTua HTML pages."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    ("Tema: scuro luxury", "Tema: chiaro luminoso"),
    (
        """  --navy:#0a1d2b;
  --navy-2:#06141d;
  --navy-3:#0e2536;
  --teal:#2f9488;
  --teal-bright:#41b3a4;
  --teal-soft:#e3d6bd;
  --gold:#c9a45c;
  --gold-bright:#e0bd72;
  --cream:#f4efe6;
  --ink:#0c2334;
  --text:#eef4f3;
  --text-soft:rgba(238,244,243,.74);
  --text-mute:rgba(238,244,243,.5);
  --muted:#5d7682;
  --line:rgba(255,255,255,.12);""",
        """  --navy:#faf8f4;
  --navy-2:#f2ede4;
  --navy-3:#ebe5d9;
  --teal:#2f9488;
  --teal-bright:#1a7a6f;
  --teal-soft:#0f5c54;
  --gold:#8b6914;
  --gold-bright:#a67c1a;
  --cream:#f4efe6;
  --ink:#0c2334;
  --text:#1a2e3b;
  --text-soft:rgba(26,46,59,.78);
  --text-mute:rgba(26,46,59,.58);
  --muted:#6b7c87;
  --line:rgba(12,35,52,.10);""",
    ),
    (
        '/* Grana sottile su tutto lo sfondo: dà profondità "tessuto" al navy */',
        '/* Grana sottile su sfondo chiaro */',
    ),
    ("pointer-events:none;opacity:.5;", "pointer-events:none;opacity:.25;"),
    (
        "background:rgba(10,29,43,.82);border-bottom:1px solid var(--line)",
        "background:rgba(250,248,244,.94);border-bottom:1px solid var(--line)",
    ),
    (
        ".vct-nav a{font-weight:800;font-size:14px;color:#e7ddca;transition:color .2s}",
        ".vct-nav a{font-weight:800;font-size:14px;color:var(--ink);transition:color .2s}",
    ),
    (
        ".vct-btn-ghost{color:#e7ddca;border:1px solid var(--line);background:none}",
        ".vct-btn-ghost{color:var(--ink);border:1px solid var(--line);background:#fff}",
    ),
    (
        ".vct-eco-card{position:relative;background:rgba(255,255,255,.055);border:1px solid var(--line);border-radius:20px;",
        ".vct-eco-card{position:relative;background:#fff;border:1px solid var(--line);border-radius:20px;",
    ),
    (
        ".vct-eco-card{background:rgba(255,255,255,.05);border:1px solid var(--line);border-radius:18px;",
        ".vct-eco-card{background:#fff;border:1px solid var(--line);border-radius:18px;",
    ),
    (
        "min-height:252px;box-shadow:0 18px 50px rgba(0,0,0,.10)}",
        "min-height:252px;box-shadow:0 8px 28px rgba(12,35,52,.08)}",
    ),
    (
        "font-size:13px;font-weight:900;color:rgba(232,216,177,.78);border:1px solid rgba(232,216,177,.22)",
        "font-size:13px;font-weight:900;color:rgba(139,105,20,.75);border:1px solid rgba(139,105,20,.25)",
    ),
    (
        ".vct-eco-card:hover{transform:translateY(-4px);border-color:rgba(65,179,164,.4);background:rgba(255,255,255,.075)}",
        ".vct-eco-card:hover{transform:translateY(-4px);border-color:rgba(47,148,136,.45);background:#fff}",
    ),
    (
        ".vct-eeat-card{background:linear-gradient(165deg,rgba(255,255,255,.07),rgba(255,255,255,.02));\n  border:1px solid var(--line);border-radius:24px;padding:32px;box-shadow:0 40px 90px rgba(0,0,0,.42)}",
        ".vct-eeat-card{background:#fff;\n  border:1px solid var(--line);border-radius:24px;padding:32px;box-shadow:0 12px 40px rgba(12,35,52,.08)}",
    ),
    (
        "border-bottom:1px dashed rgba(255,255,255,.1)}",
        "border-bottom:1px dashed rgba(12,35,52,.12)}",
    ),
    (
        ".vct-disclaimer{margin-top:24px;font-size:12px;color:rgba(238,244,243,.4);line-height:1.7;max-width:1000px}",
        ".vct-disclaimer{margin-top:24px;font-size:12px;color:rgba(26,46,59,.55);line-height:1.7;max-width:1000px}",
    ),
    (
        "font-size:12.5px;color:rgba(238,244,243,.45)}",
        "font-size:12.5px;color:rgba(26,46,59,.5)}",
    ),
    (
        ".vct-nav{position:absolute;top:100%;left:0;right:0;flex-direction:column;align-items:stretch;gap:0;background:#0a1d2b;border-top:1px solid rgba(255,255,255,.12);padding:8px 18px 18px;display:none;box-shadow:0 24px 48px rgba(0,0,0,.35)}.vct-nav.open{display:flex}.vct-nav a{color:#eef4f3;padding:13px 4px;border-bottom:1px solid rgba(255,255,255,.07)}.vct-nav a.nav-cta{margin-top:12px;text-align:center;border-bottom:none;color:#0a1d2b}",
        ".vct-nav{position:absolute;top:100%;left:0;right:0;flex-direction:column;align-items:stretch;gap:0;background:#fff;border-top:1px solid var(--line);padding:8px 18px 18px;display:none;box-shadow:0 16px 40px rgba(12,35,52,.12)}.vct-nav.open{display:flex}.vct-nav a{color:var(--ink);padding:13px 4px;border-bottom:1px solid var(--line)}.vct-nav a.nav-cta{margin-top:12px;text-align:center;border-bottom:none;color:#04201c}",
    ),
    (
        ".start-card{display:flex;gap:16px;background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:18px;padding:24px;transition:.25s}",
        ".start-card{display:flex;gap:16px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px;transition:.25s;box-shadow:0 4px 20px rgba(12,35,52,.06)}",
    ),
    (
        ".about-prose p{color:rgba(238,244,243,.82);font-size:16px;line-height:1.78;margin-bottom:16px}",
        ".about-prose p{color:var(--text-soft);font-size:16px;line-height:1.78;margin-bottom:16px}",
    ),
    (
        ".about-prose strong{color:#fff;font-weight:600}",
        ".about-prose strong{color:var(--ink);font-weight:600}",
    ),
    # PATCH 2026
    (
        ":root{--vct-navy:#0a1d2b;--vct-navy2:#06141d;--vct-teal:#2f9488;--vct-teal2:#41b3a4;--vct-gold:#c9a45c;--vct-cream:#f4efe6;--vct-text:#eef4f3;--vct-soft:rgba(238,244,243,.75);--vct-line:rgba(255,255,255,.13)}",
        ":root{--vct-navy:#faf8f4;--vct-navy2:#f2ede4;--vct-teal:#2f9488;--vct-teal2:#1a7a6f;--vct-gold:#8b6914;--vct-cream:#f4efe6;--vct-text:#1a2e3b;--vct-soft:rgba(26,46,59,.78);--vct-line:rgba(12,35,52,.10)}",
    ),
    (
        "body{background:radial-gradient(circle at 20% 0%,#10354b 0%,var(--vct-navy) 38%,var(--vct-navy2) 100%)!important;color:var(--vct-text)!important}",
        "body{background:linear-gradient(180deg,#faf8f4 0%,#fff 100%)!important;color:var(--vct-text)!important}",
    ),
    (
        ".hero{background:radial-gradient(circle at 18% 0%,rgba(47,148,136,.20),transparent 34%),linear-gradient(180deg,rgba(10,29,43,.98),rgba(6,20,29,.98))!important;border-bottom:1px solid var(--vct-line)!important}",
        ".hero{background:radial-gradient(circle at 18% 0%,rgba(47,148,136,.12),transparent 40%),linear-gradient(170deg,#faf6ee 0%,#fff 65%)!important;border-bottom:1px solid var(--vct-line)!important}",
    ),
    (
        "color:#fff!important;margin:14px 0 18px!important;max-width:980px!important}",
        "color:var(--vct-ink)!important;margin:14px 0 18px!important;max-width:980px!important}",
    ),
    (
        ".btn-ghost,.vct-btn-ghost,.btn-secondary{border-color:rgba(238,244,243,.18)!important;color:#e7ddca!important}",
        ".btn-ghost,.vct-btn-ghost,.btn-secondary{border-color:var(--vct-line)!important;color:var(--vct-ink)!important;background:#fff!important}",
    ),
    (
        ".vct-header,.topbar{background:rgba(6,20,29,.90)!important;border-bottom:1px solid var(--vct-line)!important}",
        ".vct-header,.topbar{background:rgba(250,248,244,.94)!important;border-bottom:1px solid var(--vct-line)!important}",
    ),
    # PASSO 2
    (
        ":root{--vct-deep:#06141d;--vct-navy:#0a1d2b;--vct-teal:#2f9488;--vct-teal2:#41b3a4;--vct-gold:#c9a45c;--vct-cream:#f4efe6;--vct-ink:#0c2334;}",
        ":root{--vct-deep:#f2ede4;--vct-navy:#faf8f4;--vct-teal:#2f9488;--vct-teal2:#1a7a6f;--vct-gold:#8b6914;--vct-cream:#f4efe6;--vct-ink:#0c2334;}",
    ),
    (
        ".topbar,.vct-header{box-shadow:0 8px 26px rgba(0,0,0,.18)!important}",
        ".topbar,.vct-header{box-shadow:0 4px 20px rgba(12,35,52,.08)!important}",
    ),
    (
        ".links a:hover{background:rgba(65,179,164,.10)!important;color:#fff!important}",
        ".links a:hover{background:rgba(47,148,136,.10)!important;color:var(--vct-teal2)!important}",
    ),
    (
        ".hero{padding:32px 0 22px!important;background:radial-gradient(circle at 16% 0%,rgba(65,179,164,.22),transparent 32%),linear-gradient(180deg,#0a2433 0%,#06141d 100%)!important}",
        ".hero{padding:32px 0 22px!important;background:radial-gradient(circle at 16% 0%,rgba(47,148,136,.12),transparent 38%),linear-gradient(170deg,#faf6ee 0%,#fff 65%)!important}",
    ),
    # OVERRIDE KIT — restore light cream sections
    (
        """h1,h2,h3,h4{font-family:var(--ff-serif)!important;color:#fff!important}
/* sezioni "cream" convertite al dark del kit */
.cream{background:rgba(255,255,255,.04)!important;color:var(--text)!important}
.cream .card{background:rgba(255,255,255,.06)!important;border-color:rgba(255,255,255,.12)!important}
.cream h2,.cream h3,.cream .kicker{color:#fff!important}
.cream .lead,.cream p,.cream li{color:rgba(238,244,243,.78)!important}""",
        """h1,h2,h3,h4{font-family:var(--ff-serif)!important;color:var(--ink)!important}
.cream{background:var(--cream)!important;color:var(--ink)!important}
.cream .card{background:#fff!important;border-color:var(--line)!important;box-shadow:0 4px 20px rgba(12,35,52,.06)!important}
.cream h2,.cream h3,.cream .kicker{color:var(--ink)!important}
.cream .lead,.cream p,.cream li{color:var(--text-soft)!important}""",
    ),
    # Minified page block
    (
        ":root{--navy:#0a1d2b;--navy2:#06141d;--teal:#2f9488;--teal2:#41b3a4;--gold:#c9a45c;--cream:#f4efe6;--text:#eef4f3;--soft:rgba(238,244,243,.75);--line:rgba(255,255,255,.13);--card:rgba(255,255,255,.055);",
        ":root{--navy:#faf8f4;--navy2:#f2ede4;--teal:#2f9488;--teal2:#1a7a6f;--gold:#8b6914;--cream:#f4efe6;--text:#1a2e3b;--soft:rgba(26,46,59,.78);--line:rgba(12,35,52,.10);--card:#fff;",
    ),
    (
        "background:radial-gradient(circle at 20% 0%,#10354b 0%,var(--navy) 38%,var(--navy2) 100%);color:var(--text)",
        "background:linear-gradient(180deg,#faf8f4 0%,#fff 100%);color:var(--text)",
    ),
    (
        "background:rgba(6,20,29,.9);backdrop-filter:blur(14px)",
        "background:rgba(250,248,244,.94);backdrop-filter:blur(14px)",
    ),
    (".logo b{color:#fff}", ".logo b{color:#0c2334}"),
    (".links a:hover{color:white}", ".links a:hover{color:var(--teal2)}"),
    ("h3{font-size:25px;color:#fff}", "h3{font-size:25px;color:#0c2334}"),
    (
        ".toc a{border:1px solid var(--line);border-radius:15px;padding:12px 14px;color:var(--soft);background:rgba(255,255,255,.04)}",
        ".toc a{border:1px solid var(--line);border-radius:15px;padding:12px 14px;color:var(--soft);background:#fff}",
    ),
    (".toc a:hover{color:white;border-color:rgba(65,179,164,.7)}", ".toc a:hover{color:var(--teal2);border-color:rgba(47,148,136,.5)}"),
    (
        "table{width:100%;border-collapse:collapse;margin:20px 0;background:rgba(255,255,255,.04);border-radius:16px;overflow:hidden}",
        "table{width:100%;border-collapse:collapse;margin:20px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(12,35,52,.06)}",
    ),
    (
        ".faq details{background:rgba(255,255,255,.055);border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin:12px 0}",
        ".faq details{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin:12px 0}",
    ),
    (".source-list a{text-decoration:underline;text-underline-offset:3px;color:#d8c28d}", ".source-list a{text-decoration:underline;text-underline-offset:3px;color:#8b6914}"),
    # Form buttons
    (
        "background:linear-gradient(135deg,#0f1f2b,#1a3a4a);color:#fff;font-family:inherit;font-size:16px;font-weight:800;border:none;border-radius:12px;cursor:pointer;transition:.2s;letter-spacing:.02em}",
        "background:linear-gradient(135deg,var(--teal),var(--teal-bright));color:#04201c;font-family:inherit;font-size:16px;font-weight:800;border:none;border-radius:12px;cursor:pointer;transition:.2s;letter-spacing:.02em}",
    ),
    (
        ".fc-header{background:linear-gradient(135deg,#0f172a,#134e4a);padding:24px;color:#fff;text-align:center}",
        ".fc-header{background:linear-gradient(135deg,#2f9488,#1a7a6f);padding:24px;color:#fff;text-align:center}",
    ),
    # Meta
    ('content="#0a1d2b"', 'content="#faf8f4"'),
    ('content="#0c2334"', 'content="#faf8f4"'),
    ('content="dark"', 'content="light"'),
]

REGEX_REPLACEMENTS = [
    (
        re.compile(r"\.card\{background:var\(--card\);border:1px solid var\(--line\);border-radius:var\(--radius\);padding:24px;box-shadow:0 24px 70px rgba\(0,0,0,\.16\)\}"),
        ".card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:24px;box-shadow:0 8px 28px rgba(12,35,52,.08)}",
    ),
    (
        re.compile(r"box-shadow:0 14px 38px rgba\(0,0,0,\.13\)!important"),
        "box-shadow:0 6px 24px rgba(12,35,52,.08)!important",
    ),
    (
        re.compile(r"\.vct-lead-card\{background:#f5efe3;border-radius:24px;padding:44px 48px;box-shadow:0 28px 72px rgba\(0,0,0,\.38\)\}"),
        ".vct-lead-card{background:#f5efe3;border-radius:24px;padding:44px 48px;box-shadow:0 12px 40px rgba(12,35,52,.12)}",
    ),
]


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    for pattern, repl in REGEX_REPLACEMENTS:
        text = pattern.sub(repl, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for html in sorted(ROOT.rglob("*.html")):
        if process_file(html):
            changed.append(html.relative_to(ROOT))
    print(f"Updated {len(changed)} files:")
    for p in changed:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
