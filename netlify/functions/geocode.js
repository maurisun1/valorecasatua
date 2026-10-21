// Robust Google Geocoding endpoint for ValoreCasaTua
// Requires Netlify environment variable: GOOGLE_MAPS_API_KEY

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

function component(components = [], type) {
  const item = components.find(c => Array.isArray(c.types) && c.types.includes(type));
  return item ? item.long_name : '';
}

function hasType(types = [], wanted = []) {
  return wanted.some(t => types.includes(t));
}

function assessQuality(result, requestedAddress = '') {
  const types = result?.types || [];
  const comps = result?.address_components || [];
  const locationType = result?.geometry?.location_type || '';
  const hasRoute = !!component(comps, 'route');
  const hasStreetNumber = !!component(comps, 'street_number');
  const hasCity = !!(component(comps, 'locality') || component(comps, 'administrative_area_level_3'));
  const isSpecificType = hasType(types, ['street_address', 'premise', 'subpremise', 'establishment']);
  const isAcceptablePrecision = ['ROOFTOP', 'RANGE_INTERPOLATED'].includes(locationType);
  const isPartial = !!result.partial_match;

  const score = [hasRoute, hasStreetNumber, hasCity, isSpecificType, isAcceptablePrecision, !isPartial]
    .reduce((sum, v) => sum + (v ? 1 : 0), 0);

  return {
    score,
    level: score >= 5 ? 'high' : score >= 4 ? 'medium' : 'low',
    accepted: score >= 5,
    checks: {
      hasRoute,
      hasStreetNumber,
      hasCity,
      isSpecificType,
      isAcceptablePrecision,
      isPartial
    },
    requestedAddress
  };
}

exports.handler = async function(event) {
  if (event.httpMethod === 'OPTIONS') {
    return json(200, { found: false, ok: true });
  }
  if (event.httpMethod !== 'POST' && event.httpMethod !== 'GET') {
    return json(405, { found: false, error: 'METHOD_NOT_ALLOWED' });
  }

  const key = process.env.GOOGLE_MAPS_API_KEY;
  if (!key) return json(500, { found: false, error: 'MISSING_API_KEY' });

  let address = '';
  try {
    if (event.httpMethod === 'GET') {
      address = event.queryStringParameters?.address || '';
    } else {
      const body = JSON.parse(event.body || '{}');
      address = body.address || [body.via, body.civico, body.citta, 'Italia'].filter(Boolean).join(', ');
    }
  } catch (_) {}

  address = String(address || '').trim();
  if (!address || address.length < 5) return json(400, { found: false, error: 'ADDRESS_REQUIRED' });

  const url = new URL('https://maps.googleapis.com/maps/api/geocode/json');
  url.searchParams.set('address', address);
  url.searchParams.set('region', 'it');
  url.searchParams.set('components', 'country:IT');
  url.searchParams.set('language', 'it');
  url.searchParams.set('key', key);

  try {
    const resp = await fetch(url.toString(), { timeout: 9000 });
    const data = await resp.json();

    if (data.status !== 'OK' || !data.results?.length) {
      return json(200, { found: false, status: data.status, error: data.error_message || data.status });
    }

    const r = data.results[0];
    const loc = r.geometry.location;
    const comps = r.address_components || [];
    const quality = assessQuality(r, address);

    return json(200, {
      found: true,
      status: data.status,
      lat: loc.lat,
      lng: loc.lng,
      formatted: r.formatted_address,
      locationType: r.geometry.location_type,
      partialMatch: !!r.partial_match,
      types: r.types || [],
      route: component(comps, 'route'),
      streetNumber: component(comps, 'street_number'),
      suburb: component(comps, 'sublocality_level_1') || component(comps, 'sublocality') || component(comps, 'neighborhood') || '',
      city: component(comps, 'locality') || component(comps, 'administrative_area_level_3') || '',
      province: component(comps, 'administrative_area_level_2') || '',
      region: component(comps, 'administrative_area_level_1') || '',
      postalCode: component(comps, 'postal_code') || '',
      quality
    });
  } catch (err) {
    return json(502, { found: false, error: 'GEOCODE_FETCH_FAILED', detail: err.message });
  }
};
