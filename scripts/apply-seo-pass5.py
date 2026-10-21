#!/usr/bin/env python3
"""SEO pass 5: fix OG HTML, legal pages, grazie-checklist, sitemap, AI meta."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_MOD = "2026-07-05"
AI_META = (
    '<meta name="GPTBot" content="index, follow">'
    '<meta name="ClaudeBot" content="index, follow">'
    '<meta name="PerplexityBot" content="index, follow">'
    '<meta name="Google-Extended" content="index, follow">'
)
AI_META_NOINDEX = (
    '<meta name="GPTBot" content="noindex, nofollow">'
    '<meta name="ClaudeBot" content="noindex, nofollow">'
    '<meta name="PerplexityBot" content="noindex, nofollow">'
    '<meta name="Google-Extended" content="noindex, nofollow">'
)

BROKEN_OG_IMAGE = re.compile(
    r'(<meta\s+property="og:image"\s+content="[^"]*")\s*\n'
    r'(<meta\s+property="og:image:width")',
    re.I,
)
BROKEN_OG_TYPE = re.compile(
    r'(<meta\s+property="og:image:type"\s+content="image/jpeg")>>',
    re.I,
)

LEGAL_PAGES = {
    "privacy/index.html": {
        "webpage_name": "Privacy Policy | ValoreCasaTua.it",
        "webpage_desc": (
            "Informativa sul trattamento dei dati personali di ValoreCasaTua.it "
            "ai sensi del Regolamento UE 2016/679 (GDPR). Titolare: Maurizio Piraino, P.IVA 14597560961."
        ),
        "robots": "index, follow",
    },
    "cookie/index.html": {
        "webpage_name": "Cookie Policy | ValoreCasaTua.it",
        "webpage_desc": (
            "Informativa sull'uso dei cookie di ValoreCasaTua.it. "
            "Attualmente il sito utilizza solo cookie tecnici necessari al funzionamento. "
            "Nessun cookie di profilazione."
        ),
        "robots": "index, follow",
    },
}

GRAZIE_DESC = (
    "Grazie per la richiesta: scarica la checklist PDF con i documenti essenziali "
    "per vendere casa in Lombardia senza blocchi al rogito."
)
GRAZIE_TITLE = "La tua checklist è pronta | ValoreCasaTua.it™"


def fix_og_image_html(text: str) -> tuple[str, bool]:
    orig = text
    text = BROKEN_OG_IMAGE.sub(r"\1>\n\2", text)
    text = BROKEN_OG_TYPE.sub(r"\1>", text)
    return text, text != orig


def add_ai_meta(text: str, noindex: bool = False) -> tuple[str, bool]:
    if "GPTBot" in text:
        return text, False
    block = AI_META_NOINDEX if noindex else AI_META
    if 'name="viewport"' in text:
        return re.sub(
            r'(<meta\s+name="viewport"[^>]*>)',
            rf"\1\n{block}",
            text,
            count=1,
            flags=re.I,
        ), True
    return text, False


def add_webpage_schema(text: str, url: str, name: str, description: str) -> tuple[str, bool]:
    if '"dateModified"' in text:
        return text, False
    payload = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": url,
        "name": name,
        "description": description,
        "datePublished": "2026-06-20",
        "dateModified": DATE_MOD,
        "publisher": {"@id": "https://valorecasatua.it/#org"},
    }
    script = (
        '<script type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )
    if "</head>" in text:
        return text.replace("</head>", script + "\n</head>", 1), True
    return text, False


def fix_legal_page(text: str, rel: str, info: dict) -> tuple[str, list[str]]:
    changes = []
    text, c = fix_og_image_html(text)
    if c:
        changes.append("og-html")

    if info["robots"] not in text:
        text = re.sub(
            r'<meta\s+name="robots"\s+content="[^"]*">',
            f'<meta name="robots" content="{info["robots"]}">',
            text,
            count=1,
            flags=re.I,
        )
        changes.append("robots-index")

    text, c = add_ai_meta(text)
    if c:
        changes.append("ai-meta")

    url = f"https://valorecasatua.it/{rel.replace('/index.html', '/')}"
    text, c = add_webpage_schema(text, url, info["webpage_name"], info["webpage_desc"])
    if c:
        changes.append("schema-webpage")

    return text, changes


def fix_grazie(text: str) -> tuple[str, list[str]]:
    changes = []
    text, c = fix_og_image_html(text)
    if c:
        changes.append("og-html")

    text = re.sub(
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        rf"\1{GRAZIE_DESC}\2",
        text,
        count=1,
        flags=re.I,
    )
    changes.append("meta-desc")

    og_block = (
        '<meta property="og:site_name" content="ValoreCasaTua.it™">\n'
        f'<meta property="og:title" content="{GRAZIE_TITLE}">\n'
        f'<meta property="og:description" content="{GRAZIE_DESC}">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:locale" content="it_IT">\n'
        '<meta property="og:url" content="https://valorecasatua.it/grazie-checklist/">'
    )
    if 'property="og:title"' not in text:
        text = text.replace(
            '<link rel="canonical" href="https://valorecasatua.it/grazie-checklist/">',
            '<link rel="canonical" href="https://valorecasatua.it/grazie-checklist/">\n' + og_block,
        )
        changes.append("og-meta")

    twitter_block = (
        '<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{GRAZIE_TITLE}">\n'
        f'<meta name="twitter:description" content="{GRAZIE_DESC}">\n'
        '<meta name="twitter:image" content="https://valorecasatua.it/assets/og-valorecasatua.jpg">'
    )
    if 'name="twitter:card"' not in text:
        text = text.replace(
            '<meta property="og:image:alt" content="ValoreCasaTua.it — checklist documenti vendita casa">',
            '<meta property="og:image:alt" content="ValoreCasaTua.it — checklist documenti vendita casa">\n'
            + twitter_block,
        )
        changes.append("twitter")

    text, c = add_ai_meta(text, noindex=True)
    if c:
        changes.append("ai-meta")

    text, c = add_webpage_schema(
        text,
        "https://valorecasatua.it/grazie-checklist/",
        GRAZIE_TITLE,
        GRAZIE_DESC,
    )
    if c:
        changes.append("schema-webpage")

    return text, changes


def update_sitemap() -> bool:
    """Keep sitemap aligned: never include noindex legal/thank-you pages."""
    path = ROOT / "sitemap.xml"
    txt = path.read_text(encoding="utf-8")
    original = txt
    for slug in ("privacy/", "cookie/", "grazie-checklist/"):
        txt = re.sub(
            rf"\s*<url><loc>https://valorecasatua\.it/{re.escape(slug)}</loc>.*?</url>",
            "",
            txt,
            flags=re.S,
        )
    if txt != original:
        path.write_text(txt, encoding="utf-8")
        return True
    return False

def main() -> None:
    n = 0
    for html_path in sorted(ROOT.rglob("index.html")):
        rel = str(html_path.relative_to(ROOT))
        text = html_path.read_text(encoding="utf-8")
        orig = text
        changes: list[str] = []

        if rel in LEGAL_PAGES:
            text, changes = fix_legal_page(text, rel, LEGAL_PAGES[rel])
        elif rel == "grazie-checklist/index.html":
            text, changes = fix_grazie(text)
        else:
            text, c = fix_og_image_html(text)
            if c:
                changes.append("og-html")

        if text != orig:
            html_path.write_text(text, encoding="utf-8")
            n += 1
            print(f"{rel}: {', '.join(changes)}")

    if update_sitemap():
        print("sitemap.xml: removed noindex URLs if present")

    print(f"\nUpdated {n} HTML files.")


if __name__ == "__main__":
    main()
