# Nuovo argomento: Affitti brevi e stress abitativo a Milano

## Dove inserirlo sul sito

- **Sezione consigliata:** Guide → Mercato (accanto a `mercato-immobiliare-lombardia-2026` e alle guide prezzi)
- **URL:** `/affitti-brevi-milano-stress-abitativo/`
- **Cartella da copiare nel progetto locale:** `affitti-brevi-milano-stress-abitativo/`

Non è una pagina “politica”: tono ValoreCasaTua = informativo per proprietari (valore, affitto, strategia).

## Tema (dati del dibattito pubblico)

- Soglia UE stress abitativo: prezzo casa > **8×** reddito medio
- Milano: **9,9** (dato 2024) → **10,5** (dato 2025) — pagina etichettata **2026**
- Case vuote: **13%**
- Affitti brevi: da **10.200** a **oltre 16.300** annunci in meno di 4 anni

## Integrazione via CLI (sul PC)

Dalla root del sito locale:

```bash
# 1) Copia la cartella pagina (dopo pull di questo branch)
cp -R affitti-brevi-milano-stress-abitativo /percorso/al/sito-locale/

# 2) Aggiorna i collegamenti (se non usi già l’HTML di questa bozza):
#    - nav "Guide" → link "Affitti brevi Milano"
#    - footer "Guide Lombardia"
#    - homepage / risorse / guide hub (card o elenco)
#    - sitemap.xml

# 3) Deploy come fai di solito (Netlify CLI o pipeline)
```

## File correlati da aggiornare in locale

1. `index.html` (o hub Guide) — card “Guide aggiornate”
2. `guide/index.html` — voce in elenco
3. `risorse/index.html` — se presente
4. `sitemap.xml` — nuova URL
5. Eventuale link “Leggi anche” in `affitto-breve-vs-transitorio/`

## CTA della pagina

- Stima gratuita → `/`
- Confronto affitti → `/affitto-breve-vs-transitorio/`
- Prezzi Milano → `/guide/prezzi-mq-milano/`
