#!/usr/bin/env python3
"""Pass 3: fix remaining light-theme contrast issues across all pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    # Province grid cards (risorse) — dark-theme ghost bg
    (
        'background:rgba(255,255,255,.05);border:1px solid rgba(201,164,92,.15);border-radius:10px;padding:14px 16px;color:#c9a45c',
        'background:#fff;border:1px solid rgba(139,105,20,.22);border-radius:10px;padding:14px 16px;color:#8b6914;box-shadow:0 2px 10px rgba(12,35,52,.06)',
    ),
    # Verdict boxes — light green text on light green bg
    ('color:#bfe9dc', 'color:rgba(26,46,59,.88)'),
    ('color:#bdeee5', 'color:#1a5c52'),
    # Dark placeholders on light forms
    ('input::placeholder{color:rgba(255,255,255,.55)}', 'input::placeholder{color:rgba(58,42,26,.4)}'),
    ('.lc-grid input::placeholder{color:rgba(255,255,255,.55)}', '.lc-grid input::placeholder{color:rgba(58,42,26,.4)}'),
    # FAQ / category pills on light pages
    ('.faq-cat{background:rgba(255,255,255,.05);', '.faq-cat{background:#fff;'),
    ('details.faq{background:rgba(255,255,255,.04);', 'details.faq{background:#fff;'),
    # Value item cards still using dark glass
    (
        '.vitem{background:linear-gradient(165deg,rgba(255,255,255,.055),rgba(255,255,255,.02));',
        '.vitem{background:#fff;',
    ),
    # Affitto strip — nearly invisible on light
    ('.strip{position:relative;z-index:1;border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:rgba(255,255,255,.025);',
     '.strip{position:relative;z-index:1;border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--cream);'),
    # Section soft gradients
    ('.section.soft{background:linear-gradient(180deg,transparent,rgba(255,255,255,.02))}',
     '.section.soft{background:linear-gradient(180deg,transparent,var(--cream))}'),
    ('.score-section{background:linear-gradient(180deg,rgba(255,255,255,.02),transparent)}',
     '.score-section{background:linear-gradient(180deg,var(--cream),transparent)}'),
    # Guide link accent on risorse
    ('color:#41b3a4;font-weight:600', 'color:#1a7a6f;font-weight:600'),
    # Pill transitorio label contrast
    ('.pill.trans{background:rgba(47,148,136,.18);color:#bdeee5}', '.pill.trans{background:rgba(47,148,136,.18);color:#1a5c52}'),
    ('.pill.breve{background:rgba(190,95,59,.18);color:#ffc3ad}', '.pill.breve{background:rgba(190,95,59,.18);color:#8b3a1a}'),
]


def process_file(path: Path) -> list[str]:
    text = path.read_text(encoding='utf-8')
    original = text
    changes = []
    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
            changes.append(old[:40])
    if text != original:
        path.write_text(text, encoding='utf-8')
    return changes


def main():
    html_files = sorted(ROOT.rglob('*.html'))
    touched = 0
    for path in html_files:
        rel = path.relative_to(ROOT)
        changes = process_file(path)
        if changes:
            touched += 1
            print(f"  {rel}: {len(changes)} fix")
    print(f"\nDone: {touched}/{len(html_files)} files updated")


if __name__ == '__main__':
    main()
