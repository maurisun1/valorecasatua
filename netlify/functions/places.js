// ════════════════════════════════════════════
//  ValoreCasaTua.it — Google Places Autocomplete (Places API New)
// ════════════════════════════════════════════
const https = require('https');

function httpsPostJson(hostname, path, extraHeaders, bodyObj) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(bodyObj);
    const req = https.request({
      hostname, path, method: 'POST',
      headers: Object.assign({
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }, extraHeaders)
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => { try { resolve({ status: res.statusCode, json: JSON.parse(data || '{}') }); } catch (e) { reject(e); } });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

exports.handler = async (event) => {
  const headers = { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Robots-Tag': 'noindex, nofollow' };
  if (event.httpMethod === 'OPTIONS') return { statusCode: 204, headers };

  const q = event.queryStringParameters || {};
  const input = q.input || '';
  const rawTypes = q.types || 'address';
  if (!input || input.length < 2) {
    return { statusCode: 200, headers, body: JSON.stringify({ predictions: [] }) };
  }

  const key = process.env.GOOGLE_MAPS_API_KEY;
  const reqBody = { input, includedRegionCodes: ['it'], languageCode: 'it' };
  if (rawTypes === '(cities)') {
    reqBody.includedPrimaryTypes = ['locality', 'administrative_area_level_3'];
  }

  try {
    const { status, json } = await httpsPostJson(
      'places.googleapis.com',
      '/v1/places:autocomplete',
      { 'X-Goog-Api-Key': key },
      reqBody
    );
    const predictions = (json.suggestions || [])
      .filter(s => s.placePrediction)
      .slice(0, 5)
      .map(s => {
        const p = s.placePrediction;
        const sf = p.structuredFormat || {};
        return {
          description: (p.text && p.text.text) || '',
          place_id: p.placeId || '',
          main_text: (sf.mainText && sf.mainText.text) || (p.text && p.text.text) || '',
          secondary_text: (sf.secondaryText && sf.secondaryText.text) || ''
        };
      });
    const out = { predictions };
    if (!predictions.length && (json.error || status >= 400)) {
      out.status = (json.error && json.error.status) || ('HTTP_' + status);
      out.error_message = (json.error && json.error.message) || '';
      console.error('Places API (New) error:', out.status, '|', out.error_message);
    }
    return { statusCode: 200, headers, body: JSON.stringify(out) };
  } catch (err) {
    return { statusCode: 500, headers, body: JSON.stringify({ predictions: [], error: err.message }) };
  }
};
