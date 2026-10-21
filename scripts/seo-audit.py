#!/usr/bin/env python3
"""SEO + SEO-AI audit for ValoreCasaTua.it static site."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = sorted(ROOT.rglob("index.html"))

# --- helpers ---
def get_meta(html: str, name: str, prop: bool = False):
    if prop:
        m = re.search(rf'<meta\s+property="{re.escape(name)}"\s+content="([^"]*)"', html, re.I)
    else:
        m = re.search(rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"', html, re.I)
    return m.group(1) if m else None

def get_tag(html: str, tag: str):
    m = re.search(rf"<{tag}[^>]*>([^<]*)</{tag}>", html, re.I | re.S)
    return m.group(1).strip() if m else None

def count_tag(html: str, tag: str) -> int:
    return len(re.findall(rf"<{tag}\b", html, re.I))

def has_jsonld_type(html: str, t: str) -> bool:
    return f'"@type": "{t}"' in html or f'"@type":"{t}"' in html

def imgs_without_alt(html: str) -> int:
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    html = re.sub(r"/\*.*?\*/", "", html, flags=re.S)
    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    bad = 0
    for img in imgs:
        if re.search(r'\balt\s*=\s*"[^"]+"', img, re.I):
            continue
        if re.search(r"\balt\s*=\s*''", img, re.I):
            bad += 1
        elif "alt=" not in img.lower():
            bad += 1
    return bad

# --- per-page SEO ---
page_results = []
seo_checks = {
    "title": 0,
    "title_len_ok": 0,
    "meta_desc": 0,
    "meta_desc_len_ok": 0,
    "canonical": 0,
    "canonical_https": 0,
    "viewport": 0,
    "lang_it": 0,
    "h1_one": 0,
    "og_title": 0,
    "og_desc": 0,
    "og_image": 0,
    "og_url": 0,
    "og_dims": 0,
    "twitter_card": 0,
    "twitter_title": 0,
    "twitter_desc": 0,
    "twitter_image": 0,
    "twitter_desc_sync": 0,
    "schema_jsonld": 0,
    "schema_date_modified": 0,
    "img_alt_ok": 0,
}

issues = []

for f in HTML_FILES:
    html = f.read_text(encoding="utf-8", errors="replace")
    rel = str(f.relative_to(ROOT))
    r = {"path": rel}

    title = get_tag(html, "title")
    desc = get_meta(html, "description")
    canon = None
    cm = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html, re.I)
    if cm:
        canon = cm.group(1)

    lang = re.search(r'<html[^>]*\slang="([^"]*)"', html, re.I)
    h1c = count_tag(html, "h1")
    imgs_bad = imgs_without_alt(html)

    og_t = get_meta(html, "og:title", prop=True)
    og_d = get_meta(html, "og:description", prop=True)
    og_i = get_meta(html, "og:image", prop=True)
    og_u = get_meta(html, "og:url", prop=True)
    og_w = get_meta(html, "og:image:width", prop=True)
    og_h = get_meta(html, "og:image:height", prop=True)

    tw_c = get_meta(html, "twitter:card")
    tw_t = get_meta(html, "twitter:title")
    tw_d = get_meta(html, "twitter:description")
    tw_i = get_meta(html, "twitter:image")

    has_schema = "application/ld+json" in html
    has_dm = bool(re.search(r'"dateModified"\s*:', html))

    checks = {
        "title": bool(title),
        "title_len_ok": bool(title and 30 <= len(title) <= 70),
        "meta_desc": bool(desc),
        "meta_desc_len_ok": bool(desc and 100 <= len(desc) <= 165),
        "canonical": bool(canon),
        "canonical_https": bool(canon and canon.startswith("https://valorecasatua.it")),
        "viewport": 'name="viewport"' in html,
        "lang_it": bool(lang and lang.group(1).startswith("it")),
        "h1_one": h1c == 1,
        "og_title": bool(og_t),
        "og_desc": bool(og_d),
        "og_image": bool(og_i),
        "og_url": bool(og_u),
        "og_dims": bool(og_w and og_h),
        "twitter_card": bool(tw_c),
        "twitter_title": bool(tw_t),
        "twitter_desc": bool(tw_d),
        "twitter_image": bool(tw_i),
        "twitter_desc_sync": bool(tw_d and desc and tw_d.strip() == desc.strip()),
        "schema_jsonld": has_schema,
        "schema_date_modified": has_dm,
        "img_alt_ok": imgs_bad == 0,
    }

    for k, v in checks.items():
        if v:
            seo_checks[k] += 1
        else:
            issues.append(f"{rel}: missing/fail {k}")

    page_results.append({"path": rel, **checks})

n_pages = len(HTML_FILES)

# --- site-level SEO ---
sitemap_urls = set()
sitemap_ok = False
try:
    tree = ET.parse(ROOT / "sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for loc in tree.findall(".//sm:loc", ns):
        sitemap_urls.add(loc.text.rstrip("/") if loc.text else "")
    sitemap_ok = True
except ET.ParseError:
    pass

expected_paths = set()
indexable_pages = 0
for f in HTML_FILES:
    html = f.read_text(encoding="utf-8", errors="replace")
    head = html.split("</head>")[0] if "</head>" in html else html[:15000]
    robots = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', head, re.I)
    if robots and "noindex" in robots.group(1).lower():
        continue
    indexable_pages += 1
    rel_dir = f.parent.relative_to(ROOT)
    if str(rel_dir) == ".":
        expected_paths.add("https://valorecasatua.it/")
    else:
        expected_paths.add(f"https://valorecasatua.it/{rel_dir.as_posix()}/")

in_sitemap = sum(1 for u in expected_paths if u.rstrip("/") in {x.rstrip("/") for x in sitemap_urls})
sitemap_coverage = in_sitemap / len(expected_paths) if expected_paths else 0

site_seo = {
    "robots_txt": (ROOT / "robots.txt").exists(),
    "sitemap_xml": (ROOT / "sitemap.xml").exists(),
    "sitemap_valid": sitemap_ok,
    "sitemap_coverage_pct": round(sitemap_coverage * 100, 1),
    "bing_auth": (ROOT / "BingSiteAuth.xml").exists(),
    "netlify_toml": (ROOT / "netlify.toml").exists(),
    "redirects": (ROOT / "_redirects").exists(),
    "favicon": (ROOT / "favicon.ico").exists() or (ROOT / "favicon.svg").exists(),
    "brand_css": (ROOT / "brand.css").exists(),
}

# --- SEO AI ---
llms = (ROOT / "llms.txt").read_text(encoding="utf-8") if (ROOT / "llms.txt").exists() else ""
ai = (ROOT / "ai.txt").read_text(encoding="utf-8") if (ROOT / "ai.txt").exists() else ""
robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT / "robots.txt").exists() else ""

ai_bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "OAI-SearchBot"]
ai_bot_allow = sum(1 for b in ai_bots if re.search(rf"User-agent:\s*{re.escape(b)}.*?Allow:\s*/", robots, re.S | re.I))

llms_links = len(re.findall(r"https://valorecasatua\.it/", llms))
llms_sections = llms.count("\n## ")

ai_checks = {
    "llms_txt_exists": bool(llms),
    "ai_txt_exists": bool(ai),
    "llms_has_about": "chi-siamo" in llms,
    "llms_has_legal": "Informazioni legali" in llms or "Privacy" in llms,
    "llms_has_disclaimer": "mediazione" in llms.lower(),
    "llms_link_count_ok": llms_links >= 35,
    "ai_txt_llms_ref": "llms.txt" in ai,
    "ai_txt_sitemap_ref": "sitemap.xml" in ai,
    "ai_txt_policy": "informational" in ai.lower() or "informativ" in ai.lower(),
    "ai_txt_no_brokerage": "brokerage" in ai.lower() or "mediazione" in ai.lower(),
    "robots_ai_bots": ai_bot_allow >= 5,
    "robots_sitemap": "Sitemap:" in robots,
    "robots_llms_comment": "llms.txt" in robots,
}

# --- scoring ---
def pct(num, den):
    return round(100 * num / den, 1) if den else 0

# SEO page score: average of key checks (20 items)
key_checks = list(seo_checks.keys())
page_score = sum(seo_checks[k] / n_pages for k in key_checks) / len(key_checks) * 100

# Site infra bonus (max 10 points scaled)
site_items = sum(1 for v in site_seo.values() if v is True or (isinstance(v, (int, float)) and v >= 95))
site_score_component = min(100, site_seo.get("sitemap_coverage_pct", 0))

# Weighted SEO total
seo_total = round(page_score * 0.85 + site_score_component * 0.10 + (10 if site_seo["bing_auth"] else 0) * 0.05, 1)
# Normalize - recalc cleaner
infra_pts = 0
for k, v in [("robots", site_seo["robots_txt"]), ("sitemap", site_seo["sitemap_xml"]),
             ("bing", site_seo["bing_auth"]), ("redirects", site_seo["redirects"]),
             ("netlify", site_seo["netlify_toml"])]:
    infra_pts += 4 if v else 0
infra_pts += min(20, site_seo["sitemap_coverage_pct"] / 5)  # up to 20 for sitemap

seo_total = round(min(100, page_score * 0.80 + infra_pts * 0.20), 1)

ai_total = round(sum(1 for v in ai_checks.values() if v) / len(ai_checks) * 100, 1)

# Category breakdown SEO
categories = {
    "Meta & title": ["title", "title_len_ok", "meta_desc", "meta_desc_len_ok", "canonical", "canonical_https"],
    "Social (OG/Twitter)": ["og_title", "og_desc", "og_image", "og_url", "og_dims",
                              "twitter_card", "twitter_title", "twitter_desc", "twitter_image", "twitter_desc_sync"],
    "Struttura HTML": ["viewport", "lang_it", "h1_one", "img_alt_ok"],
    "Schema.org": ["schema_jsonld", "schema_date_modified"],
}

cat_scores = {}
for cat, keys in categories.items():
    cat_scores[cat] = round(sum(seo_checks[k] / n_pages for k in keys) / len(keys) * 100, 1)

# Compare to previous pass targets
summary = {
    "pages": n_pages,
    "seo_score": seo_total,
    "seo_ai_score": ai_total,
    "seo_categories": cat_scores,
    "page_pass_rates": {k: f"{seo_checks[k]}/{n_pages} ({pct(seo_checks[k], n_pages)}%)" for k in key_checks},
    "site_level": site_seo,
    "seo_ai_checks": {k: ("OK" if v else "FAIL") for k, v in ai_checks.items()},
    "open_issues_count": len(issues),
    "sample_issues": issues[:25],
}

print(json.dumps(summary, indent=2, ensure_ascii=False))
