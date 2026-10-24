// Restituisce la chiave Google Maps per il browser (mappa interattiva).
// Usa una chiave DEDICATA, limitata al dominio valorecasatua.it:
// variabile d'ambiente Netlify GOOGLE_MAPS_BROWSER_KEY.
// Se la variabile non esiste, la mappa usa OpenStreetMap.
exports.handler = async () => ({
  statusCode: 200,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'X-Robots-Tag': 'noindex, nofollow',
    'Cache-Control': 'public, max-age=300'
  },
  body: JSON.stringify({ key: process.env.GOOGLE_MAPS_BROWSER_KEY || '' })
});
