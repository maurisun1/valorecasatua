#!/usr/bin/env python3
"""Propagate dropdown navigation from index.html to all pages."""

import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

NAV_CSS = """.vct-nav{display:flex;gap:8px;align-items:center}
.vct-nav>a:not(.nav-cta){font-weight:700;font-size:13.5px;color:var(--ink);transition:color .2s,background .2s;padding:8px 12px;border-radius:999px;white-space:nowrap}
.vct-nav>a:not(.nav-cta):hover{color:var(--teal-bright);background:rgba(47,148,136,.08)}
.vct-nav>a[aria-current="page"]:not(.nav-cta){color:var(--teal-bright);background:rgba(47,148,136,.10)}
.vct-nav .nav-cta{background:linear-gradient(135deg,var(--gold),var(--gold-bright));
  color:#231a07!important;padding:10px 18px;border-radius:999px;transition:transform .25s;font-size:13.5px;font-weight:800;margin-left:4px;white-space:nowrap}
.vct-nav .nav-cta:hover{transform:translateY(-2px)}
.vct-nav-drop{position:relative}
.vct-nav-drop-btn{position:relative;font-family:inherit;font-size:13.5px;font-weight:700;color:var(--ink);background:none;border:0;cursor:pointer;padding:8px 28px 8px 12px;border-radius:999px;display:inline-flex;align-items:center;gap:6px;white-space:nowrap;transition:color .2s,background .2s}
.vct-nav-drop-btn::after{content:'';position:absolute;right:12px;top:50%;width:6px;height:6px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:translateY(-65%) rotate(45deg);opacity:.55;pointer-events:none}
.vct-nav-drop:hover .vct-nav-drop-btn,.vct-nav-drop:focus-within .vct-nav-drop-btn{color:var(--teal-bright);background:rgba(47,148,136,.08)}
.vct-nav-drop-panel{position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(-50%) translateY(-6px);min-width:232px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:8px;box-shadow:0 18px 44px rgba(12,35,52,.14);opacity:0;visibility:hidden;pointer-events:none;transition:opacity .2s,visibility .2s,transform .2s;z-index:60}
.vct-nav-drop-panel::before{content:'';position:absolute;top:-8px;left:0;right:0;height:8px}
.vct-nav-drop:hover .vct-nav-drop-panel,.vct-nav-drop:focus-within .vct-nav-drop-panel{opacity:1;visibility:visible;pointer-events:auto;transform:translateX(-50%) translateY(0)}
.vct-nav-drop-panel a{display:block;padding:10px 12px;border-radius:10px;font-size:13.5px;font-weight:600;color:var(--ink);border:0!important;white-space:normal;line-height:1.35}
.vct-nav-drop-panel a:hover{background:rgba(47,148,136,.08);color:var(--teal-bright)}
.vct-nav-drop-panel a[aria-current="page"]{color:var(--teal-bright);background:rgba(47,148,136,.10)}
.vct-nav-drop-label{display:none;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:800;padding:16px 4px 6px}"""

MOBILE_NAV_SNIPPET = (
    ".vct-nav.open{display:flex}.vct-nav>a:not(.nav-cta){color:var(--ink);padding:13px 4px;border-bottom:1px solid var(--line);border-radius:0;background:none!important}"
    ".vct-nav>a.nav-cta{margin-top:12px;text-align:center;border-bottom:none;color:#04201c!important;padding:14px 18px}"
    ".vct-nav-drop-btn{display:none}.vct-nav-drop-label{display:block}"
    ".vct-nav-drop-panel{position:static;transform:none;opacity:1;visibility:visible;pointer-events:auto;box-shadow:none;border:0;padding:0 0 4px;min-width:0}"
    ".vct-nav-drop-panel a{padding:10px 4px 10px 14px;border-bottom:1px solid var(--line)!important;border-radius:0}"
)

# href -> label for aria-current inside dropdowns or top nav
CURRENT_MAP = {
    "index.html": ("/", None),
    "verifica-casa": ("/verifica-casa/", None),
    "conviene-ristrutturare": ("/conviene-ristrutturare/", None),
    "classe-energetica-valore-casa": ("/classe-energetica-valore-casa/", None),
    "affitto-breve-vs-transitorio": ("/affitto-breve-vs-transitorio/", None),
    "vendere-casa-ricevuta-in-donazione": ("/vendere-casa-ricevuta-in-donazione/", None),
    "guide/index.html": ("/guide/", None),
    "mercato-immobiliare-lombardia-2026": ("/mercato-immobiliare-lombardia-2026/", None),
    "quanto-costa-vendere-casa": ("/quanto-costa-vendere-casa/", None),
    "risorse": ("/risorse/", None),
}

STRUMENTI = [
    ("/verifica-casa/", "Check-Up Casa"),
    ("/conviene-ristrutturare/", "Ristrutturazione"),
    ("/classe-energetica-valore-casa/", "Classe Energetica"),
    ("/affitto-breve-vs-transitorio/", "Affitti"),
]

GUIDE = [
    ("/vendere-casa-ricevuta-in-donazione/", "Donazioni"),
    ("/guide/", "Prezzi al m² Lombardia"),
    ("/mercato-immobiliare-lombardia-2026/", "Mercato 2026"),
    ("/quanto-costa-vendere-casa/", "Quanto costa vendere"),
]

SITUAZIONI = [
    ("/#situazioni", "Tutte le situazioni"),
    ("/vendere-casa-con-mutuo/", "Mutuo in corso"),
    ("/casa-separazione-divorzio-lombardia/", "Separazione / divorzio"),
    ("/casa-ereditata-divisione-eredi-lombardia/", "Casa ereditata"),
    ("/vendere-casa-da-soli/", "Vendere da soli"),
    ("/vendere-casa-affittata-inquilino/", "Casa con inquilino"),
    ("/comprare-casa-prima-di-vendere/", "Comprare prima di vendere"),
    ("/pensione-cambiare-casa/", "Pensione e cambio casa"),
]

for slug in [
    "casa-separazione-divorzio-lombardia",
    "casa-ereditata-divisione-eredi-lombardia",
    "comprare-casa-prima-di-vendere",
    "casa-vuota-sfitta-cosa-fare",
    "trasferimento-lavoro-vendere-affittare-casa",
    "pensione-cambiare-casa",
    "vendere-casa-con-mutuo",
    "vendere-nuda-proprieta-usufrutto",
    "vendere-casa-non-conforme-difformita",
    "vendere-casa-da-soli",
    "vendere-casa-affittata-inquilino",
    "vendere-casa-comproprieta-disaccordo",
    "plusvalenza-vendita-casa",
]:
    CURRENT_MAP[slug] = (f"/{slug}/", None)

DEFAULT_CTA = '<a class="nav-cta" href="/#form">Valuta gratis</a>'
HOME_CTA = '<a class="nav-cta" href="#form">Valuta gratis</a>'
WHATSAPP_LINK = '<a href="https://wa.me/393516292353" target="_blank" rel="noopener">WhatsApp</a>'
CONTATTI_LINK = '<a href="#contatti">Contatti</a>'


def get_cta(key: str) -> str:
    if key == "index.html":
        return HOME_CTA
    return DEFAULT_CTA


def page_key(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "index.html"
    if rel.startswith("guide/prezzi-mq-"):
        return "guide/prezzi"
    return rel.replace("/index.html", "")


def current_href(key: str) -> Optional[str]:
    if key in CURRENT_MAP:
        return CURRENT_MAP[key][0]
    if key == "guide/prezzi":
        return "/guide/"
    return None


def link(href: str, label: str, current: Optional[str]) -> str:
    ac = ' aria-current="page"' if current == href else ""
    return f'<a href="{href}"{ac}>{label}</a>'


def build_nav(current: Optional[str], cta: str) -> str:
    home_ac = ' aria-current="page"' if current == "/" else ""
    risorse_ac = ' aria-current="page"' if current == "/risorse/" else ""

    strumenti = "\n    ".join(link(h, l, current) for h, l in STRUMENTI)
    guide = "\n    ".join(link(h, l, current) for h, l in GUIDE)
    situazioni = "\n    ".join(link(h, l, current) for h, l in SITUAZIONI)

    return f"""<nav class="vct-nav" aria-label="Navigazione ecosistema">
<a href="/"{home_ac}>Valore Casa</a>
<div class="vct-nav-drop">
  <button type="button" class="vct-nav-drop-btn" aria-haspopup="true">Situazioni</button>
  <span class="vct-nav-drop-label">Situazioni</span>
  <div class="vct-nav-drop-panel">
    {situazioni}
  </div>
</div>
<div class="vct-nav-drop">
  <button type="button" class="vct-nav-drop-btn" aria-haspopup="true">Strumenti</button>
  <span class="vct-nav-drop-label">Strumenti</span>
  <div class="vct-nav-drop-panel">
    {strumenti}
  </div>
</div>
<div class="vct-nav-drop">
  <button type="button" class="vct-nav-drop-btn" aria-haspopup="true">Guide</button>
  <span class="vct-nav-drop-label">Guide</span>
  <div class="vct-nav-drop-panel">
    {guide}
  </div>
</div>
<a href="/risorse/"{risorse_ac}>Risorse</a>
{CONTATTI_LINK}
{WHATSAPP_LINK}
{cta}</nav>"""


def update_css(text: str) -> str:
    # Replace nav CSS block (various legacy patterns)
    nav_css_pat = re.compile(
        r"\.vct-nav\{display:flex;[^}]+\}.*?"
        r"\.vct-nav(?:\s+a|>a:not\(\.nav-cta\)|\s+\.nav-cta)[^{]*\{[^}]*\}.*?"
        r"\.vct-nav\s+\.nav-cta:hover\{[^}]+\}",
        re.DOTALL,
    )
    if nav_css_pat.search(text):
        text = nav_css_pat.sub(NAV_CSS, text, count=1)
    elif ".vct-nav-drop{" not in text:
        # Fallback: insert after .vct-brand .pay block
        text = re.sub(
            r"(\.vct-brand \.pay\{[^}]+\})",
            r"\1\n" + NAV_CSS,
            text,
            count=1,
        )

    # Update mobile nav rules
    old_mobile = re.compile(
        r"\.vct-nav\.open\{display:flex\}\.vct-nav a\{[^}]+\}\.vct-nav a\.nav-cta\{[^}]+\}"
    )
    text = old_mobile.sub(MOBILE_NAV_SNIPPET, text)

    # index.html may already have partial mobile rules — ensure dropdown mobile styles
    if ".vct-nav-drop-btn{display:none}" not in text:
        text = text.replace(
            ".vct-nav.open{display:flex}.vct-nav>a:not(.nav-cta){",
            MOBILE_NAV_SNIPPET + ".vct-nav>a:not(.nav-cta){",
            1,
        )

    # Ensure max-height on mobile nav (index has it)
    text = re.sub(
        r"(\.vct-nav\{position:absolute[^}]+box-shadow:[^;]+;)(?![^}]*max-height)",
        r"\1max-height:calc(100vh - 72px);overflow-y:auto;",
        text,
    )
    return text


NAV_CLOSE_SCRIPT = """<script>
(function(){
  function closeVctNav(){
    var b=document.querySelector('.vct-burger');
    var n=document.querySelector('.vct-nav');
    if(!b||!n||!window.matchMedia('(max-width:900px)').matches)return;
    b.classList.remove('open');
    n.classList.remove('open');
    b.setAttribute('aria-expanded','false');
  }
  document.querySelectorAll('.vct-nav a').forEach(function(a){
    a.addEventListener('click', closeVctNav);
  });
})();
</script>"""


def inject_nav_script(text: str) -> str:
    if "closeVctNav" in text:
        return text
    if "</body>" in text:
        return text.replace("</body>", NAV_CLOSE_SCRIPT + "\n</body>", 1)
    return text


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if '<nav class="vct-nav"' not in text:
        return False

    nav_m = re.search(r"<nav class=\"vct-nav\".*?</nav>", text, re.DOTALL)
    if not nav_m:
        return False

    old_nav = nav_m.group(0)
    key = page_key(path)
    cta = get_cta(key)
    current = current_href(key)
    new_nav = build_nav(current, cta)

    if old_nav == new_nav and ".vct-nav-drop{" in text:
        new_text = inject_nav_script(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            return True
        return False

    text = text.replace(old_nav, new_nav, 1)
    text = update_css(text)
    text = inject_nav_script(text)
    path.write_text(text, encoding="utf-8")
    return True


def main():
    updated = []
    for html in sorted(ROOT.rglob("*.html")):
        if process_file(html):
            updated.append(html.relative_to(ROOT).as_posix())
    print(f"Updated {len(updated)} pages:")
    for p in updated:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
