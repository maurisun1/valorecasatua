const province = {
  milano: { label: 'Milano e provincia', factor: 1.20, note: 'area con costi di manodopera e logistica più elevati' },
  monza: { label: 'Monza e Brianza', factor: 1.12, note: 'mercato vicino a Milano, costi medio-alti' },
  como: { label: 'Como / lago', factor: 1.10, note: 'possibili maggiorazioni per immobili di pregio o lacustri' },
  varese: { label: 'Varese', factor: 1.03, note: 'costi generalmente intermedi' },
  lecco: { label: 'Lecco', factor: 1.06, note: 'costi intermedi, con variabili su immobili lacustri o collinari' },
  bergamo: { label: 'Bergamo', factor: 1.00, note: 'mercato equilibrato rispetto alla media lombarda' },
  brescia: { label: 'Brescia', factor: 0.98, note: 'mercato generalmente equilibrato, con variazioni per zona e pregio' },
  pavia: { label: 'Pavia', factor: 0.90, note: 'costi mediamente più contenuti rispetto all’area milanese' },
  lodi: { label: 'Lodi', factor: 0.90, note: 'costi mediamente contenuti' },
  cremona: { label: 'Cremona', factor: 0.86, note: 'costi tendenzialmente più contenuti' },
  mantova: { label: 'Mantova', factor: 0.86, note: 'costi tendenzialmente più contenuti' },
  sondrio: { label: 'Sondrio / Valtellina', factor: 0.94, note: 'possibili maggiorazioni per logistica e immobili montani' },
  altro: { label: 'Lombardia', factor: 1.00, note: 'stima media regionale da verificare con sopralluogo' }
};

const baseItems = {
  bagno: {
    label: 'Rifacimento bagno completo', type: 'fixed', basic: [5200, 7600], medio: [7600, 11800], alto: [11800, 18500], weeks: [2, 4], note: 'demolizioni, impianti bagno, massetti, rivestimenti, sanitari e rubinetteria inclusi come fascia orientativa'
  },
  cucina: {
    label: 'Rifacimento cucina / area impianti', type: 'fixed', basic: [4500, 7600], medio: [7600, 13500], alto: [13500, 26000], weeks: [2, 4], note: 'impianti, predisposizioni, rivestimenti e opere edili; arredo cucina escluso salvo indicazione diversa'
  },
  appartamento_light: {
    label: 'Restyling appartamento', type: 'sqm', basic: [320, 520], medio: [480, 720], alto: [650, 950], weeks: [4, 8], note: 'pavimenti, tinteggiature, porte, finiture e opere leggere senza rifacimento completo degli impianti'
  },
  appartamento_completo: {
    label: 'Ristrutturazione completa appartamento', type: 'sqm', basic: [680, 930], medio: [880, 1250], alto: [1180, 1750], weeks: [8, 16], note: 'impianti, bagno, cucina, pavimenti, finiture, porte e opere murarie principali'
  },
  impianti: {
    label: 'Rifacimento impianti', type: 'sqm', basic: [170, 260], medio: [230, 340], alto: [320, 460], weeks: [3, 7], note: 'impianto elettrico e idraulico con assistenze murarie; termico da verificare in base al caso'
  },
  pavimenti: {
    label: 'Pavimenti e rivestimenti', type: 'sqm', basic: [85, 135], medio: [130, 210], alto: [210, 360], weeks: [2, 5], note: 'rimozione o posa, materiali e complessità incidono molto sul prezzo'
  },
  serramenti: {
    label: 'Serramenti', type: 'fixed', basic: [6500, 10500], medio: [9000, 15500], alto: [14500, 28000], weeks: [2, 6], note: 'stima indicativa per appartamento medio; numero e dimensione dei serramenti sono decisivi'
  },
  tinteggiatura: {
    label: 'Tinteggiatura e finiture leggere', type: 'sqm', basic: [24, 38], medio: [34, 55], alto: [55, 90], weeks: [1, 3], note: 'preparazione fondi, rasature e pitture speciali possono aumentare la fascia'
  }
};

function normalizeCity(input='') {
  const s = input.toLowerCase();
  const keys = Object.keys(province).filter(k => k !== 'altro');
  return keys.find(k => s.includes(k)) || 'altro';
}
function qualityKey(q='medio') {
  const s = q.toLowerCase();
  if (s.includes('alto') || s.includes('premium')) return 'alto';
  if (s.includes('base') || s.includes('econom')) return 'basic';
  return 'medio';
}
function ageFactor(anno='') {
  if (anno.includes('1960')) return 1.10;
  if (anno.includes('Prima')) return 1.16;
  if (anno.includes('1980')) return 1.05;
  if (anno.includes('Dopo')) return 0.96;
  return 1.05;
}
function round100(n) { return Math.round(n / 100) * 100; }
function detectItems(interventi=[], tipoIntervento='') {
  const text = [...interventi, tipoIntervento].join(' ').toLowerCase();
  const items = [];
  if (text.includes('bagno')) items.push('bagno');
  if (text.includes('cucina')) items.push('cucina');
  if (text.includes('completa') || text.includes('totale') || text.includes('appartamento completo')) items.push('appartamento_completo');
  if (text.includes('restyling') || text.includes('leggera')) items.push('appartamento_light');
  if (text.includes('impianti') || text.includes('elettrico') || text.includes('idraulico')) items.push('impianti');
  if (text.includes('pavimenti') || text.includes('rivestimenti')) items.push('pavimenti');
  if (text.includes('serramenti') || text.includes('infissi')) items.push('serramenti');
  if (text.includes('tinteggiatura') || text.includes('imbiancatura')) items.push('tinteggiatura');
  if (!items.length) items.push('appartamento_completo');
  if (items.includes('appartamento_completo')) return ['appartamento_completo'];
  return [...new Set(items)];
}

exports.handler = async function(event) {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };
  if (event.httpMethod === 'OPTIONS') return { statusCode: 204, headers, body: '' };
  if (event.httpMethod !== 'POST') return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method Not Allowed' }) };

  try {
    const body = JSON.parse(event.body || '{}');
    const mq = Math.max(8, Number(body.mq || 80));
    const cityKey = normalizeCity(body.citta || '');
    const zone = province[cityKey];
    const q = qualityKey(body.finiture || body.qualita || 'medio');
    const aFactor = ageFactor(body.anno || '');
    const items = detectItems(body.interventi || [], body.tipoIntervento || '');
    const complexity = (body.complessita || '').toLowerCase().includes('abitato') ? 1.08 : 1;
    const factor = zone.factor * aFactor * complexity;

    const dettaglio = items.map(key => {
      const item = baseItems[key];
      const range = item[q];
      let min, max;
      if (item.type === 'sqm') {
        min = range[0] * mq;
        max = range[1] * mq;
      } else {
        min = range[0];
        max = range[1];
      }
      return {
        key,
        voce: item.label,
        min: round100(min * factor),
        max: round100(max * factor),
        note: item.note,
        settimane_min: item.weeks[0],
        settimane_max: item.weeks[1]
      };
    });

    const subtotalMin = dettaglio.reduce((s, x) => s + x.min, 0);
    const subtotalMax = dettaglio.reduce((s, x) => s + x.max, 0);
    const tecnicoMin = Math.max(1200, subtotalMin * 0.055);
    const tecnicoMax = Math.max(2200, subtotalMax * 0.085);
    const imprevistiMin = subtotalMin * 0.07;
    const imprevistiMax = subtotalMax * 0.12;
    const costoMin = round100(subtotalMin + tecnicoMin + imprevistiMin);
    const costoMax = round100(subtotalMax + tecnicoMax + imprevistiMax);
    const detrazioneBase = Math.min(costoMax, 96000) * 0.50;
    const hasEnergy = items.includes('serramenti') || items.includes('impianti') || items.includes('appartamento_completo');
    const detrazioni = [
      { nome: 'Bonus ristrutturazione', percentuale: '50%', desc: 'stima su massimale ordinario, da verificare con tecnico/fiscalista' }
    ];
    if (hasEnergy) detrazioni.push({ nome: 'Possibile Ecobonus', percentuale: '50–65%', desc: 'solo se gli interventi rispettano requisiti tecnici e asseverazioni previste' });

    const tMin = Math.max(...dettaglio.map(x => x.settimane_min));
    const tMax = dettaglio.reduce((s, x) => s + x.settimane_max, 0);
    const classeAttuale = body.classe && body.classe !== 'Non lo so' ? body.classe : 'da verificare';
    const salto = hasEnergy ? 'possibile miglioramento se si interviene su serramenti/impianti' : 'miglioramento energetico limitato se non si interviene su impianti o involucro';

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        costo_min: costoMin,
        costo_max: costoMax,
        costo_mq_min: round100(costoMin / mq),
        costo_mq_max: round100(costoMax / mq),
        lavori_base_min: round100(subtotalMin),
        lavori_base_max: round100(subtotalMax),
        spese_tecniche_min: round100(tecnicoMin),
        spese_tecniche_max: round100(tecnicoMax),
        imprevisti_min: round100(imprevistiMin),
        imprevisti_max: round100(imprevistiMax),
        detrazione_totale: round100(detrazioneBase),
        costo_netto_indicativo: round100(costoMax - detrazioneBase),
        tempi: `${Math.max(1, tMin)}–${Math.max(tMin + 1, tMax)} settimane`,
        zona: zone.label,
        analisi_zona: `${zone.label}: ${zone.note}. La stima applica un coefficiente territoriale e un correttivo per epoca dell’immobile, ma va confermata con sopralluogo e computo metrico.`,
        detrazioni,
        interventi_dettaglio: dettaglio,
        classe_attuale: classeAttuale,
        impatto_energetico: salto,
        consigli: [
          'Prima di chiedere preventivi, definire capitolato e livello finiture: evita offerte non confrontabili.',
          'Prevedere una voce imprevisti: negli immobili datati emergono spesso tracce, sottofondi o impianti non visibili.',
          'Per bagno, cucina e impianti il sopralluogo tecnico è indispensabile: le misure da sole non bastano.'
        ],
        disclaimer: 'Stima orientativa pre-sopralluogo. Non è computo metrico, preventivo contrattuale o parere fiscale.'
      })
    };
  } catch (err) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: err.message }) };
  }
};
