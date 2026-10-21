# valorecasatua

Codice completo del sito [ValoreCasaTua.it](https://valorecasatua.it/): portale informativo per chi vende o valuta casa in Lombardia, basato sui dati ufficiali OMI dell'Agenzia delle Entrate.

Sito statico (HTML/CSS/JS) pubblicato su **Netlify**, con alcune Netlify Functions per il motore di valutazione. Ogni pagina è una cartella con il suo `index.html`, così gli URL restano puliti (es. `/valuta/`).

## Struttura

### Pagine principali
| Percorso | Contenuto |
|---|---|
| `index.html` | Home page |
| `valuta/` | Strumento "Quanto vale la mia casa?" (analisi OMI gratuita) |
| `verifica-casa/` | Score gratuito sui documenti per vendere |
| `guide/` | Indice guide + 22 pagine `prezzi-mq-<città>/` con i prezzi al m² per comune/provincia |
| `risorse/` | Centro risorse |
| `report-omi-lombardia-2026/`, `mercato-immobiliare-lombardia-2026/` | Report e analisi di mercato |
| `per-la-stampa/` | Pagina stampa del Report OMI |
| `glossario/`, `chi-siamo/` | Glossario e presentazione |
| `privacy/`, `cookie/`, `404.html`, `grazie-checklist/` | Pagine legali, errore e conferma |

### Situazioni di vendita
Guide dedicate a casi specifici, una cartella ciascuna, ad esempio:
`vendere-casa-con-mutuo/`, `vendere-casa-affittata-inquilino/`, `vendere-casa-diritto-superficie/`, `vendere-nuda-proprieta-usufrutto/`, `casa-ereditata-divisione-eredi-lombardia/`, `casa-separazione-divorzio-lombardia/`, `plusvalenza-vendita-casa/`, `quanto-costa-vendere-casa/`, `conviene-ristrutturare/`, `classe-energetica-valore-casa/` e le altre cartelle `vendere-casa-*` nella root.

### Risorse e dati
| Percorso | Contenuto |
|---|---|
| `assets/` | CSS, JS, logo, foto, copertine (`covers/`), immagini social (`og/`, `og-*.webp`), PDF scaricabili e `print-kit/` per i materiali stampa |
| `brand.css` | Stili e colori del brand |
| `data/omi/` | Quotazioni OMI (Lombardia e Milano, semestri 2025-2 e 2026-1) in JSON, più le fonti |
| `data/lombardia-province.geojson` | Confini delle province per le mappe |

### Backend (Netlify Functions)
In `netlify/functions/`, raggiungibili tramite `/api/...` (vedi `netlify.toml`):
- `valuation.js` — motore di valutazione
- `geocode.js`, `places.js` — Google Maps (geocoding e indirizzi)
- `anthropic.js` — proxy verso l'API di Claude
- `analizza.js` — stima dei costi di ristrutturazione per provincia

Le chiavi API **non sono nel codice**: si impostano come variabili d'ambiente su Netlify (`ANTHROPIC_API_KEY`, `GOOGLE_MAPS_API_KEY`).

### Configurazione e SEO
- `netlify.toml`, `_redirects` — build, funzioni e redirect (www → dominio principale)
- `sitemap.xml`, `sitemap-images.xml`, `robots.txt`, `llms.txt`, `ai.txt`
- `BingSiteAuth.xml` e il file `.txt` in root — verifica Bing/Google
- `site.webmanifest`, favicon e icone

### Strumenti di lavoro
- `scripts/` — script Python per aggiornare le pagine in blocco (SEO, temi, footer, immagini OG, rigenerazione guide dai dati OMI)
- `docs/nuovi-argomenti/` — brief degli argomenti in preparazione

## Cosa non è nel repo
Escluso tramite `.gitignore`: `node_modules/`, file `.env` e chiavi, `.DS_Store`, cartella locale `.netlify/`, file `.zip` di deploy e report `.lighthouse/`.
