// ValoreCasaTua valuation engine - OMI locale Lombardia
// Regola: non mostrare valori numerici se indirizzo, coordinate o zona OMI non sono affidabili.
// Dati territoriali: Agenzia Entrate - OMI, semestre 2026/1.

const fs = require('fs');
const path = require('path');

const json = (statusCode, body) => ({
  statusCode,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'X-Robots-Tag': 'noindex, nofollow',
    'Cache-Control': 'no-store',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  },
  body: JSON.stringify(body)
});

function n(v, fallback = 0) {
  const raw = String(v ?? '').trim();
  const cleaned = raw.replace(',', '.').replace(/[^0-9.\-]/g, '');
  if (!cleaned || cleaned === '-' || cleaned === '.' || cleaned === '-.') return fallback;
  const x = Number(cleaned);
  return Number.isFinite(x) ? x : fallback;
}

function clean(v) { return String(v ?? '').trim(); }
function norm(v) { return clean(v).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }

function addressFromBody(b) {
  return [b.via, b.civico, b.citta, 'Italia'].map(clean).filter(Boolean).join(', ');
}

async function geocode(address) {
  const key = process.env.GOOGLE_MAPS_API_KEY;
  if (!key) return { ok: false, code: 'MISSING_API_KEY' };

  const url = new URL('https://maps.googleapis.com/maps/api/geocode/json');
  url.searchParams.set('address', address);
  url.searchParams.set('region', 'it');
  url.searchParams.set('components', 'country:IT');
  url.searchParams.set('language', 'it');
  url.searchParams.set('key', key);

  const resp = await fetch(url.toString());
  const data = await resp.json();

  if (data.status !== 'OK' || !data.results?.length) {
    return { ok: false, code: data.status || 'NO_RESULT', detail: data.error_message || '' };
  }
  return { ok: true, raw: data.results[0] };
}

function comp(components = [], type) {
  const item = components.find(c => c.types?.includes(type));
  return item ? item.long_name : '';
}

function assessGeocode(result) {
  const types = result.types || [];
  const comps = result.address_components || [];
  const locationType = result.geometry?.location_type || '';

  const checks = {
    hasRoute: !!comp(comps, 'route'),
    hasStreetNumber: !!comp(comps, 'street_number'),
    hasCity: !!(comp(comps, 'locality') || comp(comps, 'administrative_area_level_3')),
    isSpecificType: ['street_address','premise','subpremise','establishment'].some(t => types.includes(t)),
    isAcceptablePrecision: ['ROOFTOP','RANGE_INTERPOLATED'].includes(locationType),
    isPartial: !!result.partial_match
  };

  const score =
    (checks.hasRoute ? 1 : 0) +
    (checks.hasStreetNumber ? 1 : 0) +
    (checks.hasCity ? 1 : 0) +
    (checks.isSpecificType ? 1 : 0) +
    (checks.isAcceptablePrecision ? 1 : 0) +
    (!checks.isPartial ? 1 : 0);

  return {
    accepted: score >= 5,
    score,
    level: score >= 5 ? 'high' : score >= 4 ? 'medium' : 'low',
    checks,
    locationType,
    types
  };
}

function getCity(result) {
  const comps = result.address_components || [];
  return comp(comps, 'locality') || comp(comps, 'administrative_area_level_3') || '';
}

let cachedOmi = null;
function loadOmiData() {
  if (cachedOmi) return cachedOmi;

  const candidates = [
    path.join(process.cwd(), 'data', 'omi', 'lombardia-2026-1.json'),
    path.join(__dirname, '..', '..', 'data', 'omi', 'lombardia-2026-1.json'),
    path.join(__dirname, 'data', 'omi', 'lombardia-2026-1.json')
  ];

  for (const file of candidates) {
    if (fs.existsSync(file)) {
      cachedOmi = JSON.parse(fs.readFileSync(file, 'utf8'));
      return cachedOmi;
    }
  }

  try {
    cachedOmi = require('../../data/omi/lombardia-2026-1.json');
    return cachedOmi;
  } catch (e) {
    throw new Error('LOCAL_OMI_LOMBARDIA_FILE_NOT_FOUND');
  }
}

function pointInRing(point, ring) {
  const x = point[0], y = point[1];
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const xi = ring[i][0], yi = ring[i][1];
    const xj = ring[j][0], yj = ring[j][1];
    const intersects = ((yi > y) !== (yj > y)) &&
      (x < (xj - xi) * (y - yi) / ((yj - yi) || 1e-12) + xi);
    if (intersects) inside = !inside;
  }
  return inside;
}

function inBbox(lng, lat, bbox) {
  return lng >= bbox[0] && lng <= bbox[2] && lat >= bbox[1] && lat <= bbox[3];
}

function resolveZone(lng, lat, omi) {
  for (const f of omi.features || []) {
    if (!f.bbox || !inBbox(lng, lat, f.bbox)) continue;
    for (const ring of f.polygons || []) {
      if (pointInRing([lng, lat], ring)) return f;
    }
  }
  return null;
}

function residentialQuotes(feature) {
  return (feature.quotes || []).filter(q => norm(q.tipologia).includes('abitaz'));
}

function chooseQuote(feature, body) {
  const res = residentialQuotes(feature);
  if (!res.length) return null;

  const civili = res.filter(q => norm(q.tipologia).includes('civili'));
  const signorili = res.filter(q => norm(q.tipologia).includes('signorili'));
  const economiche = res.filter(q => norm(q.tipologia).includes('economico'));

  let pool = civili.length ? civili : (signorili.length ? signorili : (economiche.length ? economiche : res));

  const state = n(body.stato, 1);
  const normal = pool.filter(q => norm(q.stato).includes('normale'));
  const ottimo = pool.filter(q => norm(q.stato).includes('ottimo'));
  const scadente = pool.filter(q => norm(q.stato).includes('scad'));

  // OMI tende a essere una base territoriale prudente. 
  // Usiamo lo stato inserito per selezionare la fascia OMI più coerente, senza inventare una zona.
  let selected = null;
  if (state < 0.9 && scadente.length) selected = scadente[0];
  else if (state >= 1.12 && ottimo.length) selected = ottimo[0];
  else if (normal.length) selected = normal[0];
  else selected = pool[0];

  // Per immobili in "buono" stato in zone dove esiste anche OTTIMO,
  // posizioniamo il range tra normale e ottimo per evitare sottostime eccessive.
  if (state >= 1.08 && state < 1.25 && normal.length && ottimo.length) {
    return {
      tipologia: selected.tipologia,
      stato: 'NORMALE/OTTIMO',
      min: Math.round((normal[0].max + ottimo[0].min) / 2),
      max: ottimo[0].max,
      raw: { normal: normal[0], ottimo: ottimo[0] }
    };
  }

  return { ...selected, raw: selected };
}

function qualityMultiplier(body) {
  let m = 1;

  const stato = n(body.stato, 1);
  if (stato < 0.9) m *= 0.94;
  else if (stato >= 1.12 && stato < 1.25) m *= 1.04;
  else if (stato >= 1.25) m *= 1.08;

  const piano = norm(body.piano || '2');
  if (['t','terra','rialzato','0'].includes(piano)) m *= 0.96;
  if (['3','4'].includes(piano)) m *= 1.02;
  if (['u','ultimo'].includes(piano)) m *= 1.06;

  const asc = norm(body.ascensore);
  if (asc.includes('no') && !['t','terra','rialzato','0','1'].includes(piano)) m *= 0.93;

  const classe = norm(body.classe);
  if (classe.includes('a') || classe.includes('b')) m *= 1.05;
  else if (classe.includes('g')) m *= 0.95;
  else if (classe.includes('e') || classe.includes('f')) m *= 0.97;

  const est = norm(body.esterno);
  if (est.includes('terraz')) m *= 1.05;
  else if (est.includes('giardino')) m *= 1.06;
  else if (est.includes('balcon')) m *= 1.02;

  const box = norm(body.box);
  if (box.includes('doppio')) m *= 1.05;
  else if (box.includes('box')) m *= 1.035;
  else if (box.includes('posto')) m *= 1.018;

  const anno = norm(body.anno);
  if (anno.includes('nuovo') || anno.includes('post')) m *= 1.04;
  else if (anno.includes('ante')) m *= 0.97;

  const tipo = norm(body.tipo || body.tipo_immobile);
  if (tipo.includes('attico')) m *= 1.06;
  if (tipo.includes('villa')) m *= 1.04;

  return Math.max(0.78, Math.min(1.24, m));
}

function localMarketCalibration(feature) {
  // Coefficiente prudente per avvicinare la base OMI al mercato richiesto/effettivo urbano.
  // È intenzionalmente limitato per non trasformare il motore in una stima aggressiva.
  const code = String(feature.code || '');
  if (code.startsWith('B')) return 1.08;  // centro/semi-centro: OMI già alto
  if (code.startsWith('C')) return 1.18;
  if (code.startsWith('D')) return 1.16;  // zone semicentrali/periferiche: OMI spesso più prudente
  if (code.startsWith('E')) return 1.12;
  return 1.10;
}

function round1000(v) { return Math.round(v / 1000) * 1000; }

exports.handler = async function(event) {
  if (event.httpMethod === 'OPTIONS') {
    return json(200, { ok: true });
  }
  if (event.httpMethod !== 'POST' && event.httpMethod !== 'GET') {
    return json(405, { ok: false, code: 'METHOD_NOT_ALLOWED', allowed: ['GET','POST','OPTIONS'] });
  }

  let body = {};
  try {
    if (event.httpMethod === 'GET') {
      body = event.queryStringParameters || {};
    } else {
      body = JSON.parse(event.body || '{}');
    }
  } catch (_) {}

  const mq = Math.round(n(body.mq, 0));
  const citta = clean(body.citta);
  const address = addressFromBody(body);

  if (!clean(body.via) || !clean(body.civico) || !citta) {
    return json(200, {
      ok: false,
      code: 'ADDRESS_FIELDS_REQUIRED',
      message: 'Inserisci via, civico e città per calcolare un valore attendibile.'
    });
  }

  if (!mq || mq < 15) {
    return json(200, {
      ok: false,
      code: 'SURFACE_REQUIRED',
      message: 'Inserisci una superficie valida per calcolare la stima.'
    });
  }

  let result = null;
  let quality = null;
  let city = '';
  let loc = null;

  // Percorso preferito: il frontend chiama /api/geocode, che abbiamo verificato funzionante,
  // e passa coordinate + qualità a questa funzione. Così evitiamo un secondo geocoding
  // e riduciamo le possibilità di errore tra browser e funzione valuation.
  const latFromBody = Number(body.lat);
  const lngFromBody = Number(body.lng);
  const hasTrustedCoordinates =
    Number.isFinite(latFromBody) &&
    Number.isFinite(lngFromBody) &&
    String(body.geoAccepted ?? 'true') !== 'false';

  if (hasTrustedCoordinates) {
    loc = { lat: latFromBody, lng: lngFromBody };
    city = clean(body.geoCity || body.citta);
    quality = {
      accepted: true,
      level: body.geoQualityLevel || 'high',
      score: Number(body.geoQualityScore || 6),
      locationType: body.locationType || 'ROOFTOP',
      checks: { passedFromFrontendGeocode: true }
    };
    result = {
      formatted_address: body.formattedAddress || address,
      geometry: { location: loc },
      address_components: [],
      types: ['street_address']
    };
  } else {
    let geo;
    try {
      geo = await geocode(address);
    } catch (e) {
      return json(200, {
        ok: false,
        code: 'GEOCODING_UNAVAILABLE',
        message: 'Non siamo riusciti a verificare l’indirizzo. Riprova tra poco.',
        debug: { error: e.message }
      });
    }

    if (!geo.ok) {
      return json(200, {
        ok: false,
        code: 'GEOCODING_FAILED',
        technical: geo.code,
        message: 'Non siamo riusciti a riconoscere con precisione l’indirizzo. Controlla via, civico e città.'
      });
    }

    result = geo.raw;
    quality = assessGeocode(result);
    city = getCity(result);
    loc = result.geometry.location;

    if (!quality.accepted) {
      return json(200, {
        ok: false,
        code: 'ADDRESS_NOT_PRECISE',
        quality,
        message: 'L’indirizzo non è stato riconosciuto con precisione sufficiente. Controlla via e civico per ottenere un valore stimato affidabile.'
      });
    }
  }

  let omi;
  try {
    omi = loadOmiData();
  } catch (e) {
    return json(200, {
      ok: false,
      code: 'OMI_DATA_UNAVAILABLE',
      message: 'Indirizzo riconosciuto, ma i dati territoriali locali non sono disponibili. Meglio non mostrare una stima incompleta.',
      detail: e.message
    });
  }

  const zone = resolveZone(loc.lng, loc.lat, omi);
  if (!zone?.code) {
    return json(200, {
      ok: false,
      code: 'OMI_ZONE_NOT_FOUND',
      geocode: { lat: loc.lat, lng: loc.lng, formatted: result.formatted_address, city },
      message: 'Indirizzo riconosciuto, ma non è stato possibile associare l’immobile a una zona di mercato affidabile. Il valore numerico automatico è attivo progressivamente sulle aree coperte dai dati territoriali caricati.'
    });
  }

  const quote = chooseQuote(zone, body);
  if (!quote) {
    return json(200, {
      ok: false,
      code: 'OMI_QUOTE_NOT_FOUND',
      zone: { code: zone.code, name: zone.name },
      message: 'Zona riconosciuta, ma non sono disponibili valori di riferimento sufficienti per mostrare una stima attendibile.'
    });
  }

  const mult = qualityMultiplier(body);
  const market = localMarketCalibration(zone);
  // Base OMI 2026/1: niente ritocco di trascinamento, altrimenti l'aggiornamento è contato due volte.
  const territorial = Math.min(market, 1.22);

  const minMq = Math.max(500, quote.min * mult * territorial);
  const maxMq = Math.max(minMq, quote.max * mult * territorial);

  const vMin = round1000(minMq * mq);
  const vMax = round1000(maxMq * mq);
  const vMid = round1000((vMin + vMax) / 2);
  const pMq = Math.round((vMid / mq) / 100) * 100;

  return json(200, {
    ok: true,
    source: 'OMI_LOCALE_LOMBARDIA_2026_1',
    semester: omi.semester,
    geocode: {
      lat: loc.lat,
      lng: loc.lng,
      formatted: result.formatted_address,
      city,
      locationType: quality.locationType,
      quality
    },
    zone: {
      code: zone.code,
      name: zone.name || zone.code,
      source: 'Perimetro OMI locale Lombardia'
    },
    quote: {
      min: quote.min,
      max: quote.max,
      tipologia: quote.tipologia,
      stato: quote.stato,
      qualityMultiplier: Number(mult.toFixed(3)),
      marketCalibration: Number(market.toFixed(3))
    },
    result: { vMin, vMax, vMid, pMq, mq },
    disclaimer: 'I valori indicati sono elaborazioni orientative basate sulle quotazioni OMI del semestre 2026/1 e sulle caratteristiche inserite. Non sono una perizia.',
    message: 'Valore stimato calcolato su indirizzo riconosciuto, zona territoriale e caratteristiche inserite.'
  });
};
