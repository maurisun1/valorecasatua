// ══════════════════════════════════════════════════════
//  DATI ZONE — aggiornati maggio 2026
//  Valori interni di riferimento
// ══════════════════════════════════════════════════════
const ZONES=[
  // MILANO CITTÀ
  {id:'centro',   name:'Duomo · Centro Storico',  city:'Milano',     lat:45.4654,lng:9.1859, tag:'milano',
   appt:{min:8500,max:13000,mid:9400},villa:{min:10000,max:16000,mid:11700},domanda:'Altissima',tempi:'25–50 gg',trend:'+3,2%'},
  {id:'brera',    name:'Brera · Moscova',          city:'Milano',     lat:45.4770,lng:9.1880, tag:'milano',
   appt:{min:7500,max:11000,mid:8300}, villa:{min:9000,max:13000,mid:9900},domanda:'Altissima',tempi:'28–52 gg',trend:'+3,5%'},
  {id:'pnuova',   name:'Porta Nuova · CityLife',   city:'Milano',     lat:45.4846,lng:9.1908, tag:'milano',
   appt:{min:7000,max:11500,mid:8100}, villa:{min:8500,max:13500,mid:9900},domanda:'Altissima',tempi:'30–55 gg',trend:'+3,8%'},
  {id:'navigli',  name:'Navigli · Tortona',        city:'Milano',     lat:45.4504,lng:9.1718, tag:'milano',
   appt:{min:5500,max:7500,mid:5800},  villa:{min:6000,max:9000,mid:6800}, domanda:'Alta',     tempi:'40–65 gg',trend:'+2,8%'},
  {id:'romana',   name:'Porta Romana · P.Vittoria',city:'Milano',     lat:45.4558,lng:9.2009, tag:'milano',
   appt:{min:5000,max:7200,mid:5500},  villa:{min:5500,max:8500,mid:6300}, domanda:'Alta',     tempi:'45–70 gg',trend:'+2,5%'},
  {id:'forl',     name:'Forlanini · Lambrate',     city:'Milano',     lat:45.4870,lng:9.2520, tag:'milano',
   appt:{min:4500,max:5500,mid:4400},  villa:{min:5000,max:6500,mid:5100}, domanda:'Alta',     tempi:'50–75 gg',trend:'+9,9%'},
  {id:'nolo',     name:'NoLo · Greco · Turro',     city:'Milano',     lat:45.4873,lng:9.2225, tag:'milano',
   appt:{min:4000,max:5500,mid:4200},  villa:{min:4500,max:6200,mid:4800}, domanda:'Alta',     tempi:'48–75 gg',trend:'+8,7%'},
  {id:'bicocca',  name:'Bicocca · Comasina',       city:'Milano',     lat:45.5088,lng:9.1600, tag:'milano',
   appt:{min:3800,max:4800,mid:3800},  villa:{min:4200,max:5500,mid:4300}, domanda:'Media',    tempi:'65–95 gg',trend:'+8,0%'},
  {id:'citastud', name:'Città Studi · Argonne',    city:'Milano',     lat:45.4680,lng:9.2270, tag:'milano',
   appt:{min:3800,max:5200,mid:4000},  villa:{min:4200,max:6000,mid:4600}, domanda:'Media',    tempi:'60–90 gg',trend:'+3,0%'},
  {id:'baggio',   name:'Baggio · Lorenteggio',     city:'Milano',     lat:45.4580,lng:9.1060, tag:'milano',
   appt:{min:2900,max:3700,mid:2900},  villa:{min:3200,max:4300,mid:3300}, domanda:'Media',    tempi:'90–130 gg',trend:'+10,6%'},
  {id:'qoggiaro', name:'Q.Oggiaro · Vialba',       city:'Milano',     lat:45.5210,lng:9.1780, tag:'milano',
   appt:{min:2800,max:3500,mid:2800},  villa:{min:3000,max:4000,mid:3200}, domanda:'Media',    tempi:'95–140 gg',trend:'+2,5%'},
  {id:'milanoavg',name:'Milano — area da verificare',       city:'Milano',     lat:45.4642,lng:9.1900, tag:'milano',
   appt:{min:4300,max:6200,mid:5180},  villa:{min:4800,max:7200,mid:5900}, domanda:'Alta',     tempi:'55–90 gg',trend:'+2,9%'},
  {id:'corvetto', name:'Corvetto · Brenta · Rogoredo',city:'Milano',    lat:45.4385,lng:9.2246, tag:'milano',
   appt:{min:3800,max:5400,mid:4550},  villa:{min:4300,max:6200,mid:5200}, domanda:'Alta',     tempi:'55–85 gg',trend:'+3,0%'},
  {id:'bocconi',  name:'Bocconi · Ticinese',          city:'Milano',     lat:45.4495,lng:9.1880, tag:'milano',
   appt:{min:5700,max:7800,mid:6500},  villa:{min:6500,max:9000,mid:7600}, domanda:'Alta',     tempi:'38–65 gg',trend:'+3,1%'},
  {id:'venezia',  name:'Porta Venezia · Buenos Aires',city:'Milano',    lat:45.4768,lng:9.2070, tag:'milano',
   appt:{min:6000,max:8500,mid:7100},  villa:{min:7000,max:9800,mid:8200}, domanda:'Altissima',tempi:'32–58 gg',trend:'+3,3%'},
  {id:'sansemp',  name:'Sempione · Arco della Pace',  city:'Milano',     lat:45.4775,lng:9.1695, tag:'milano',
   appt:{min:6200,max:8800,mid:7300},  villa:{min:7200,max:10500,mid:8500},domanda:'Altissima',tempi:'35–60 gg',trend:'+3,0%'},
  {id:'sansiro',  name:'San Siro · De Angeli',        city:'Milano',     lat:45.4700,lng:9.1350, tag:'milano',
   appt:{min:4200,max:6200,mid:5000},  villa:{min:5000,max:8000,mid:6200}, domanda:'Media',    tempi:'60–95 gg',trend:'+2,6%'},
  // HINTERLAND MILANO
  {id:'sesto',    name:'Sesto San Giovanni',        city:'Prov. Milano',lat:45.5318,lng:9.2310,tag:'milano',
   appt:{min:2000,max:3300,mid:2400},  villa:{min:2300,max:3900,mid:2700}, domanda:'Media',    tempi:'85–135 gg',trend:'+2,2%'},
  {id:'monza',    name:'Monza',                     city:'Monza-Brianza',lat:45.5845,lng:9.2744,tag:'monza',
   appt:{min:2500,max:3300,mid:2500},  villa:{min:2800,max:4000,mid:3100}, domanda:'Media',    tempi:'80–125 gg',trend:'+5,0%'},
  {id:'cinisello',name:'Cinisello Balsamo',          city:'Prov. Milano',lat:45.5497,lng:9.2100,tag:'milano',
   appt:{min:1800,max:2800,mid:2100},  villa:{min:2000,max:3300,mid:2400}, domanda:'Media',    tempi:'100–150 gg',trend:'+1,9%'},
  {id:'segrate',  name:'Segrate · San Donato',      city:'Prov. Milano',lat:45.4950,lng:9.2780,tag:'milano',
   appt:{min:2000,max:3200,mid:2400},  villa:{min:2300,max:3900,mid:2800}, domanda:'Media',    tempi:'88–138 gg',trend:'+2,3%'},
  // BERGAMO
  {id:'bgalta',   name:'Bergamo Alta (Colli)',       city:'Bergamo',    lat:45.7057,lng:9.6622, tag:'bergamo',
   appt:{min:3500,max:5800,mid:4100},  villa:{min:4200,max:7500,mid:5200}, domanda:'Alta',     tempi:'70–110 gg',trend:'+1,9%'},
  {id:'bgcitta',  name:'Bergamo Città',              city:'Bergamo',    lat:45.6981,lng:9.6774, tag:'bergamo',
   appt:{min:2400,max:3300,mid:2500},  villa:{min:2700,max:4000,mid:3000}, domanda:'Media',    tempi:'88–128 gg',trend:'+1,9%'},
  {id:'bgprov',   name:'Provincia di Bergamo',       city:'Prov. Bergamo',lat:45.5218,lng:9.5898,tag:'bergamo',
   appt:{min:1500,max:2200,mid:1600},  villa:{min:1700,max:2700,mid:2000}, domanda:'Media',    tempi:'100–155 gg',trend:'+6,9%'},
  {id:'iseo',     name:"Lago d'Iseo · Sarnico",      city:'Prov. Bergamo',lat:45.6602,lng:9.9588,tag:'bergamo',
   appt:{min:2000,max:3800,mid:2600},  villa:{min:2500,max:5000,mid:3300}, domanda:'Media',    tempi:'80–130 gg',trend:'+2,8%'},
  // BRESCIA
  {id:'bscentro', name:'Brescia Città',              city:'Brescia',    lat:45.5416,lng:10.2118,tag:'brescia',
   appt:{min:1800,max:2700,mid:1900},  villa:{min:2000,max:3300,mid:2300}, domanda:'Media',    tempi:'88–130 gg',trend:'+1,7%'},
  {id:'sirmione', name:'Sirmione · Desenzano',       city:'Lago di Garda',lat:45.4800,lng:10.5700,tag:'brescia',
   appt:{min:3200,max:7500,mid:4700},  villa:{min:4000,max:10000,mid:6300},domanda:'Alta',     tempi:'55–95 gg', trend:'+3,6%'},
  {id:'garda',    name:'Lago di Garda · Salò',       city:'Prov. Brescia',lat:45.6000,lng:10.5500,tag:'brescia',
   appt:{min:2800,max:6000,mid:3800},  villa:{min:3500,max:8500,mid:5200}, domanda:'Alta',     tempi:'60–100 gg',trend:'+3,1%'},
  // COMO
  {id:'como',     name:'Como Città',                 city:'Como',       lat:45.8082,lng:9.0852, tag:'como',
   appt:{min:2500,max:3800,mid:2700},  villa:{min:3000,max:5500,mid:3800}, domanda:'Alta',     tempi:'70–110 gg',trend:'+0,4%'},
  {id:'comolago', name:'Lago di Como · Bellagio',    city:'Prov. Como', lat:45.9600,lng:9.2000, tag:'como',
   appt:{min:2200,max:6000,mid:3600},  villa:{min:3000,max:10000,mid:5800},domanda:'Alta',     tempi:'60–100 gg',trend:'+2,5%'},
  // VARESE
  {id:'varese',   name:'Varese · Lago Maggiore',     city:'Varese',     lat:45.8206,lng:8.8257, tag:'varese',
   appt:{min:1600,max:2500,mid:1700},  villa:{min:1900,max:3500,mid:2400}, domanda:'Media',    tempi:'90–140 gg',trend:'+1,2%'},
  // LECCO
  {id:'lecco',    name:'Lecco · Lago di Como (LC)',  city:'Lecco',      lat:45.8560,lng:9.3987, tag:'lecco',
   appt:{min:2200,max:3000,mid:2200},  villa:{min:2500,max:4000,mid:2900}, domanda:'Media',    tempi:'88–135 gg',trend:'+6,4%'},
  // PAVIA
  {id:'pavia',    name:'Pavia',                      city:'Pavia',      lat:45.1847,lng:9.1582, tag:'pavia',
   appt:{min:2100,max:3000,mid:2200},  villa:{min:2400,max:3800,mid:2800}, domanda:'Media',    tempi:'110–165 gg',trend:'+1,0%'},
  {id:'pvprov',   name:'Provincia di Pavia',          city:'Prov. Pavia',lat:45.2000,lng:9.0000, tag:'pavia',
   appt:{min:900,max:1500,mid:1000},   villa:{min:1100,max:2000,mid:1400}, domanda:'Bassa',    tempi:'130–200 gg',trend:'+0,9%'},
  // LODI
  {id:'lodi',     name:'Lodi',                       city:'Lodi',       lat:45.3141,lng:9.5036, tag:'lodi',
   appt:{min:1300,max:1900,mid:1400},  villa:{min:1500,max:2500,mid:1800}, domanda:'Media',    tempi:'100–160 gg',trend:'+4,3%'},
  // CREMONA
  {id:'cremona',  name:'Cremona · Crema',            city:'Cremona',    lat:45.1333,lng:10.0241,tag:'cremona',
   appt:{min:1200,max:1800,mid:1300},  villa:{min:1400,max:2400,mid:1700}, domanda:'Bassa',    tempi:'120–185 gg',trend:'+2,2%'},
  // MANTOVA
  {id:'mantova',  name:'Mantova',                    city:'Mantova',    lat:45.1564,lng:10.7914,tag:'mantova',
   appt:{min:1100,max:1800,mid:1300},  villa:{min:1300,max:2400,mid:1600}, domanda:'Bassa',    tempi:'120–185 gg',trend:'+0,1%'},
  // SONDRIO
  {id:'sondrio',  name:'Sondrio · Valtellina',       city:'Sondrio',    lat:46.1699,lng:9.8785, tag:'sondrio',
   appt:{min:1600,max:3000,mid:2000},  villa:{min:1900,max:4000,mid:2600}, domanda:'Media',    tempi:'100–160 gg',trend:'+4,0%'},
  {id:'livigno',  name:'Livigno · Bormio',           city:'Sondrio',    lat:46.5000,lng:10.2500,tag:'sondrio',
   appt:{min:4500,max:9000,mid:5800},  villa:{min:6000,max:12000,mid:7600},domanda:'Alta',     tempi:'50–90 gg', trend:'+4,8%'},
];

const PROV_PRICE={'Milano':5181,'Monza e della Brianza':2819,'Bergamo':2796,'Brescia':2127,'Como':2956,'Varese':1850,'Lecco':2457,'Pavia':2429,'Lodi':1504,'Cremona':1450,'Mantova':1450,'Sondrio':2200};
const CTIPO={appartamento:1.0,villa:1.05,attico:1.12};
const CPIANO={T:0.94,'1':0.97,'2':1.0,'3':1.02,'4':1.04,U:1.09};
const VIEWS={all:{c:[45.65,9.90],z:8.5},milano:{c:[45.48,9.19],z:12},bergamo:{c:[45.70,9.67],z:10.5},brescia:{c:[45.54,10.22],z:10.5},como:{c:[45.86,9.12],z:10.5},cremona:{c:[45.13,10.02],z:10.5},lecco:{c:[45.86,9.40],z:10.5},lodi:{c:[45.31,9.50],z:10.5},mantova:{c:[45.16,10.79],z:10.5},monza:{c:[45.58,9.27],z:11},pavia:{c:[45.18,9.16],z:10.5},sondrio:{c:[46.17,9.88],z:9.5},varese:{c:[45.82,8.83],z:10.5}};
const SCALE=[[800,'#1a7a3a'],[1800,'#44ab5e'],[2800,'#d4e157'],[4000,'#ffb300'],[6000,'#f4511e'],[9500,'#c62828']];

let tipo='appartamento',mapInst,geoLayer,mMarkers=[],mTag='all';

// ── Utils ──
function priceColor(p){for(let i=0;i<SCALE.length-1;i++){const[p0,c0]=SCALE[i],[p1,c1]=SCALE[i+1];if(p<=p1){const t=(p-p0)/(p1-p0);return lerpHex(c0,c1,Math.max(0,Math.min(1,t)));}}return SCALE[SCALE.length-1][1];}
function lerpHex(c0,c1,t){const h=s=>parseInt(s.replace('#',''),16);const r0=h(c0)>>16,g0=(h(c0)>>8)&255,b0=h(c0)&255;const r1=h(c1)>>16,g1=(h(c1)>>8)&255,b1=h(c1)&255;const r=Math.round(r0+(r1-r0)*t),g=Math.round(g0+(g1-g0)*t),b=Math.round(b0+(b1-b0)*t);return`#${((r<<16)|(g<<8)|b).toString(16).padStart(6,'0')}`;}
function getD(z){return tipo==='villa'?z.villa:z.appt;}
function fmt(n){return'€ '+Math.round(n).toLocaleString('it-IT')}
function fmtK(n){return n>=1000?(n/1000).toFixed(1).replace('.',',')+'k':n}

// ── Form valutazione ──
function cleanText(v){
  return (v||'').toString().trim();
}

function normalizeText(v){
  return cleanText(v).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
}

function normalizeAddress(via, civico, citta){
  return [cleanText(via), cleanText(civico), cleanText(citta), 'Italia']
    .filter(Boolean)
    .join(', ')
    .replace(/\bv\.?le\b/gi,'Viale')
    .replace(/\bp\.zza\b/gi,'Piazza')
    .replace(/\bc\.so\b/gi,'Corso')
    .replace(/\bs\.\s/gi,'San ');
}

function updateAddr(){
  const c=cleanText(document.getElementById('citta')?.value);
  const v=cleanText(document.getElementById('via')?.value);
  const n=cleanText(document.getElementById('civico')?.value);
  const addr=document.getElementById('addr');
  if(addr) addr.value=normalizeAddress(v,n,c).replace(', Italia','');
}

function setTipo(el){
  document.querySelectorAll('.tcard').forEach(c=>c.classList.remove('on'));
  el.classList.add('on');
  tipo=el.dataset.v;
}

(function(){
  var links=document.querySelectorAll('a.hero-main-cta[href="#form"]');
  if(!links.length) return;
  links.forEach(function(link){
    link.addEventListener('click', function(e){
      var form=document.getElementById('form');
      if(!form) return;
      e.preventDefault();
      var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      form.scrollIntoView({behavior:reduce?'auto':'smooth', block:'start'});
      var first=form.querySelector('#indirizzo');
      if(first) window.setTimeout(function(){ first.focus({preventScroll:true}); }, reduce?0:450);
      if(history.replaceState) history.replaceState(null, '', '#form');
    });
  });
})();

(function(){
  var range=document.getElementById('mqR');
  var show=document.getElementById('mqShow');
  var field=document.getElementById('mqV');
  var minus=document.getElementById('mqMinus');
  var plus=document.getElementById('mqPlus');
  if(!range||!field) return;
  var min=parseInt(range.min,10)||20;
  var max=parseInt(range.max,10)||500;
  var frame=0;
  function clamp(n){
    if(isNaN(n)) return parseInt(range.value,10)||min;
    return Math.min(max, Math.max(min, n));
  }
  function paint(n){
    if(show) show.textContent=n+' mq';
  }
  function setMq(n){
    var v=clamp(n);
    range.value=String(v);
    field.value=String(v);
    paint(v);
  }
  range.addEventListener('input', function(){
    if(frame) return;
    frame=requestAnimationFrame(function(){
      frame=0;
      field.value=range.value;
      paint(range.value);
    });
  });
  field.addEventListener('input', function(){
    var raw=String(field.value).trim();
    if(raw==='') return;
    var n=parseInt(raw,10);
    if(isNaN(n)||n<min||n>max) return;
    range.value=String(n);
    paint(n);
  });
  field.addEventListener('blur', function(){
    setMq(parseInt(field.value,10));
  });
  if(minus) minus.addEventListener('click', function(){ setMq((parseInt(range.value,10)||min)-5); });
  if(plus) plus.addEventListener('click', function(){ setMq((parseInt(range.value,10)||min)+5); });
})();

document.getElementById('via')?.addEventListener('input',updateAddr);
document.getElementById('civico')?.addEventListener('input',updateAddr);
document.getElementById('citta')?.addEventListener('input',updateAddr);

function zoneById(id){return ZONES.find(z=>z.id===id)||null;}

function zoneByAddressKeywords(via, citta){
  const text = normalizeText(`${via||''} ${citta||''}`);

  const rules = [
    {id:'corvetto', words:['corvetto','brenta','bacchiglione','rogoredo','porto di mare','mecenate','bonfadini','san donato milanese']},
    {id:'romana', words:['porta romana','piazzale lodi','viale lodi','ripamonti','fondazione prada','scalo romana','cadore','plebisciti','porta vittoria','medaglie d oro','montenero']},
    {id:'bocconi', words:['bocconi','ticinese','bligny','tabacchi','porta lodovica','ascanio sforza']},
    {id:'navigli', words:['navigli','darsena','tortona','solari','savona','ripa di porta ticinese','porta genova']},
    {id:'brera', words:['brera','moscova','garibaldi','solferino','fiori chiari','fiori oscuri','largo la foppa']},
    {id:'pnuova', words:['porta nuova','citylife','city life','tre torri','gae aulenti','isola','gioia','repubblica','melchiorre gioia','monte rosa']},
    {id:'venezia', words:['porta venezia','buenos aires','lima','palestro','indipendenza','regina giovanna']},
    {id:'sansemp', words:['sempione','arco della pace','procaccini','canonizzazione','sarpi','paolo sarpi']},
    {id:'citastud', words:['citta studi','argonne','piola','romagna','porpora','politecnico','teodosio']},
    {id:'forl', words:['lambrate','forlanini','ortica','rubattino','udine','rimembranze di lambrate']},
    {id:'nolo', words:['nolo','turro','pasteur','rovereto','greco','precotto','viale monza']},
    {id:'bicocca', words:['bicocca','bovisa','affori','comasina','dergano','maciachini']},
    {id:'sansiro', words:['san siro','de angeli','gambara','bande nere','washington','fiera','lotto']},
    {id:'baggio', words:['baggio','lorenteggio','giambellino','inganni','bisceglie']},
    {id:'qoggiaro', words:['quarto oggiaro','vialba','certosa','espinasse']},
    {id:'centro', words:['duomo','centro storico','san babila','montenapoleone','missori','cordusio','cadorna']},
    {id:'bgalta', words:['bergamo alta','citta alta','colli bergamo']},
    {id:'bgcitta', words:['bergamo']},
    {id:'bscentro', words:['brescia']},
    {id:'como', words:['como']},
    {id:'monza', words:['monza']},
    {id:'varese', words:['varese']},
    {id:'lecco', words:['lecco']},
    {id:'lodi', words:['lodi']},
    {id:'pavia', words:['pavia']},
    {id:'cremona', words:['cremona','crema']},
    {id:'mantova', words:['mantova']},
    {id:'sondrio', words:['sondrio']}
  ];

  for(const rule of rules){
    if(rule.words.some(w => text.includes(normalizeText(w)))) return zoneById(rule.id);
  }
  return null;
}

function getZona(addr){
  const a=normalizeText(addr);
  if(!a) return zoneById('milanoavg');

  const keyword=zoneByAddressKeywords(addr,'');
  if(keyword) return keyword;

  const CITY_MAP = {
    'milano':'milanoavg','mi':'milanoavg',
    'bergamo':'bgcitta','bg':'bgcitta','brescia':'bscentro','bs':'bscentro',
    'como':'como','co':'como','monza':'monza','mb':'monza','varese':'varese','va':'varese',
    'lecco':'lecco','lc':'lecco','lodi':'lodi','lo':'lodi','pavia':'pavia','pv':'pavia',
    'cremona':'cremona','cr':'cremona','mantova':'mantova','mn':'mantova','sondrio':'sondrio','so':'sondrio',
    'livigno':'livigno','bormio':'livigno','garda':'garda','desenzano':'garda','sirmione':'sirmione','salo':'garda','bellagio':'comolago'
  };

  for(const [key,id] of Object.entries(CITY_MAP)){
    if(a===key || a.includes(key)) return zoneById(id)||zoneById('milanoavg');
  }
  return zoneById('milanoavg');
}

function haversine(lat1, lon1, lat2, lon2){
  const R = 6371;
  const dLat = (lat2-lat1) * Math.PI / 180;
  const dLon = (lon2-lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

async function geocodeAddress(via, civico, citta){
  const q=normalizeAddress(via,civico,citta);
  try{
    const res=await fetch('/api/geocode',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({address:q})
    });
    const data=await res.json();
    if(data.found){
      return{
        lat:Number(data.lat), lng:Number(data.lng),
        suburb:normalizeText(data.suburb||''),
        city:normalizeText(data.city||citta||''),
        display:data.formatted||q,
        locationType:data.locationType||'',
        partialMatch:!!data.partialMatch,
        status:data.status||'OK'
      };
    }
    console.warn('Geocoding non trovato:', data);
  }catch(e){
    console.warn('Geocoding fallback:',e);
  }
  return null;
}

function findNearestZone(lat,lng,suburb,city){
  if(!Number.isFinite(lat) || !Number.isFinite(lng)) return null;

  const cityLow=normalizeText(city);
  let candidates=ZONES;

  if(cityLow.includes('milano') || cityLow.includes('milan')){
    candidates=ZONES.filter(z=>z.tag==='milano' && normalizeText(z.city).includes('milano'));
  }else if(cityLow.includes('bergamo')){
    candidates=ZONES.filter(z=>normalizeText(z.city).includes('bergamo') || z.id.startsWith('bg'));
  }else if(cityLow.includes('brescia')){
    candidates=ZONES.filter(z=>normalizeText(z.city).includes('brescia') || z.id.startsWith('bs') || z.id==='garda' || z.id==='sirmione');
  }else if(cityLow.includes('monza')){
    candidates=ZONES.filter(z=>z.id==='monza');
  }

  if(suburb){
    for(const z of candidates){
      const zname=normalizeText(z.name);
      const terms=zname.split(/[\s·,\/\-]+/).filter(t=>t.length>3);
      if(terms.some(t=>suburb.includes(t))) return z;
    }
  }

  let nearest=null,minDist=Infinity;
  for(const z of candidates){
    const d=haversine(lat,lng,z.lat,z.lng);
    if(d<minDist){minDist=d;nearest=z;}
  }

  if(minDist>15 && (cityLow.includes('milano') || cityLow.includes('milan'))) return zoneById('milanoavg');
  return nearest;
}


function nextFormStep(){
  document.querySelectorAll('.err-msg').forEach(e=>e.classList.remove('on'));
  if(typeof window.parseAddrParts==='function'){
    const parts=window.parseAddrParts(document.getElementById('indirizzo')?.value||'');
    const C=document.getElementById('citta'),V=document.getElementById('via'),N=document.getElementById('civico');
    if(C && !cleanText(C.value) && parts.citta) C.value=parts.citta;
    if(V && !cleanText(V.value) && parts.via) V.value=parts.via;
    if(N && !cleanText(N.value) && parts.civico) N.value=parts.civico;
  }
  const citta=cleanText(document.getElementById('citta')?.value);
  if(!citta){
    document.getElementById('e-citta')?.classList.add('on');
    document.getElementById('indirizzo')?.focus();
    return;
  }
  document.getElementById('formStep1')?.classList.remove('active');
  document.getElementById('formStep2')?.classList.add('active');
  document.getElementById('fp1')?.classList.remove('active');
  document.getElementById('fp2')?.classList.add('active');
  document.getElementById('fpl')?.classList.add('active');
  document.getElementById('form')?.scrollIntoView({behavior:'smooth',block:'start'});
  if (window.vctTrack) vctTrack('stima_start', { citta: citta });
}

function prevFormStep(){
  document.getElementById('formStep2')?.classList.remove('active');
  document.getElementById('formStep1')?.classList.add('active');
  document.getElementById('fp2')?.classList.remove('active');
  document.getElementById('fp1')?.classList.add('active');
  document.getElementById('fpl')?.classList.remove('active');
  document.getElementById('form')?.scrollIntoView({behavior:'smooth',block:'start'});
}

function selectedText(id){
  const el=document.getElementById(id);
  return el?.options ? el.options[el.selectedIndex]?.text || '' : '';
}

function extraValuationMultiplier(piano){
  const asc=document.getElementById('ascensoreS')?.value || 'si';
  const locali=document.getElementById('localiS')?.value || '3';
  const classe=document.getElementById('classeS')?.value || 'ns';
  const anno=document.getElementById('annoS')?.value || 'ns';
  const esterno=document.getElementById('esternoS')?.value || 'no';
  const box=document.getElementById('boxS')?.value || 'no';

  let m=1;

  const localiM={1:1.06,2:1.03,3:1,4:.98,5:.96};
  m*=localiM[locali] || 1;

  if(asc==='no' && !['T','1'].includes(String(piano))) m*=.94;
  if(asc==='si' && ['3','4','U'].includes(String(piano))) m*=1.03;

  const classeM={ab:1.08,cd:1.02,ef:.97,g:.93,ns:1};
  m*=classeM[classe] || 1;

  const annoM={ante60:.97,'60_80':.98,'80_00':1,post00:1.05,nuovo:1.10,ns:1};
  m*=annoM[anno] || 1;

  const esternoM={no:1,balcone:1.03,terrazzo:1.07,giardino:1.08};
  m*=esternoM[esterno] || 1;

  const boxM={no:1,posto:1.03,box:1.06,doppio:1.09};
  m*=boxM[box] || 1;

  return m;
}

function calcolaConZona(z){
  z = z || zoneById('milanoavg');
  const mq=parseInt(document.getElementById('mqR').value)||90;
  const piano=document.getElementById('pianoS')?.value || '2';
  const stato=parseFloat(document.getElementById('statoS')?.value)||1.0;
  const extra=extraValuationMultiplier(piano);
  const d=getD(z);
  const cT=CTIPO[tipo]||1,cP=CPIANO[piano]||1;
  const coeff=cT*cP*stato*extra;
  const vMin=Math.round(d.min*mq*coeff/1000)*1000;
  const vMax=Math.round(d.max*mq*coeff/1000)*1000;
  const vMid=Math.round((vMin+vMax)/2/1000)*1000;
  const pMq=Math.round(vMid/mq/100)*100;
  return{
    vMin,vMax,vMid,pMq,z,mq,tipo,
    locali:selectedText('localiS'),
    piano:selectedText('pianoS'),
    stato:selectedText('statoS'),
    ascensore:selectedText('ascensoreS'),
    anno:selectedText('annoS'),
    classe:selectedText('classeS'),
    esterno:selectedText('esternoS'),
    box:selectedText('boxS'),
    occupazione:selectedText('occupazioneS')
  };
}

function calcola(addr){ return calcolaConZona(getZona(addr)); }


function readValuationPayload(){
  return{
    nome:cleanText(document.getElementById('gNome')?.value || ''),
    telefono:cleanText(document.getElementById('gTel')?.value || ''),
    email:cleanText(document.getElementById('gEmail')?.value || ''),
    citta:cleanText(document.getElementById('citta').value),
    via:cleanText(document.getElementById('via').value),
    civico:cleanText(document.getElementById('civico').value),
    mq:parseInt(document.getElementById('mqR').value)||0,
    tipo:tipo,
    locali:selectedText('localiS'),
    piano:document.getElementById('pianoS')?.value || '',
    piano_label:selectedText('pianoS'),
    ascensore:document.getElementById('ascensoreS')?.value || '',
    ascensore_label:selectedText('ascensoreS'),
    stato:document.getElementById('statoS')?.value || '',
    stato_label:selectedText('statoS'),
    anno:document.getElementById('annoS')?.value || '',
    anno_label:selectedText('annoS'),
    classe:document.getElementById('classeS')?.value || '',
    classe_label:selectedText('classeS'),
    esterno:document.getElementById('esternoS')?.value || '',
    esterno_label:selectedText('esternoS'),
    box:document.getElementById('boxS')?.value || '',
    box_label:selectedText('boxS'),
    occupazione:document.getElementById('occupazioneS')?.value || '',
    occupazione_label:selectedText('occupazioneS')
  };
}

async function submitForm(){
  const payload=readValuationPayload();
  // Contatto non richiesto per vedere la fascia: si chiede dopo, per il riepilogo.
  payload.nome = payload.nome || '';
  payload.telefono = payload.telefono || '';
  payload.email = payload.email || '';
  const fullAddress=normalizeAddress(payload.via,payload.civico,payload.citta).replace(', Italia','');
  document.getElementById('addr').value=fullAddress;

  let ok=true;
  document.querySelectorAll('.err-msg').forEach(e=>e.classList.remove('on'));
  ['via','civico'].forEach(id=>document.getElementById(id)?.classList.remove('field-error'));

  // Re-parse address from visible field if autocomplete was skipped
  if(typeof window.parseAddrParts==='function'){
    const parts=window.parseAddrParts(document.getElementById('indirizzo')?.value||'');
    if(!payload.citta && parts.citta){ payload.citta=parts.citta; document.getElementById('citta').value=parts.citta; }
    if(!payload.via && parts.via){ payload.via=parts.via; document.getElementById('via').value=parts.via; }
    if(!payload.civico && parts.civico){ payload.civico=parts.civico; document.getElementById('civico').value=parts.civico; }
  }
  if(!payload.citta){document.getElementById('e-citta').classList.add('on');ok=false;}
  if(!payload.via){document.getElementById('via').classList.add('field-error');ok=false;}
  if(!payload.civico){document.getElementById('civico').classList.add('field-error');ok=false;}
  if(!ok){
    if(!payload.via||!payload.civico||!payload.citta){
      document.getElementById('e-citta').textContent='Per calcolare servono via, numero civico e città. Scegli un suggerimento o digita es. Via Roma 10, Brescia.';
      document.getElementById('e-citta').classList.add('on');
      document.getElementById('formStep2')?.classList.remove('active');
      document.getElementById('formStep1')?.classList.add('active');
      document.getElementById('fp2')?.classList.remove('active');
      document.getElementById('fp1')?.classList.add('active');
      document.getElementById('fpl')?.classList.remove('active');
      const body=document.querySelector('.fc-body');
      if(body) body.style.display='';
      document.getElementById('indirizzo')?.focus();
      document.getElementById('form')?.scrollIntoView({behavior:'smooth',block:'start'});
    }
    return;
  }

  if (window.vctTrack) vctTrack('stima_submit', { citta: payload.citta || '', mq: payload.mq || 0 });
  const btn=document.getElementById('btnSubmit');
  btn.disabled=true;
  btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> Verifica indirizzo e zona…';

  try{
    // Flusso verificato: prima usiamo /api/geocode, che nel sito live funziona,
    // poi passiamo coordinate e qualità al motore OMI.
    // Così /api/valuation NON deve rifare il geocoding e non può bloccarsi su GEOCODING_FAILED.
    const geoResp=await fetch('/api/geocode',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({address:fullAddress})
    });

    const geo=await geoResp.json();

    if(!geo.found || (geo.quality?.score ?? 0) < 4){
      const geocodeError={
        ok:false,
        code:'ADDRESS_NOT_RECOGNIZED',
        technical:geo.error || geo.status || 'GEOCODE_NOT_ACCEPTED',
        geocode:geo,
        message:'Non siamo riusciti a riconoscere con precisione l’indirizzo. Controlla via, civico e città.'
      };
      window.__lastValuationPayload = payload;
      window.__lastFullAddress = fullAddress;
      window.__lastValuationData = geocodeError;
      mostraErroreValutazione(geocodeError.message, geocodeError);
      return;
    }

    const payloadForEngine={
      ...payload,
      lat:geo.lat,
      lng:geo.lng,
      geoAccepted:true,
      geoCity:geo.city || payload.citta,
      geoQualityScore:geo.quality?.score || 6,
      geoQualityLevel:geo.quality?.level || 'high',
      locationType:geo.locationType || 'ROOFTOP',
      formattedAddress:geo.formatted || fullAddress
    };

    const resp=await fetch('/api/valuation',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payloadForEngine)
    });

    const data=await resp.json();

    window.__lastValuationPayload = payloadForEngine;
    window.__lastFullAddress = fullAddress;
    window.__lastValuationData = data;

    if(!data.ok){
      mostraErroreValutazione(data.message || 'Non ci sono dati sufficienti per mostrare un valore affidabile.', data);
      return;
    }

    const r={
      vMin:data.result.vMin,
      vMax:data.result.vMax,
      vMid:data.result.vMid,
      pMq:data.result.pMq,
      mq:data.result.mq,
      tipo:payload.tipo,
      locali:payload.locali,
      piano:payload.piano_label,
      stato:payload.stato_label,
      ascensore:payload.ascensore_label,
      anno:payload.anno_label,
      classe:payload.classe_label,
      esterno:payload.esterno_label,
      box:payload.box_label,
      occupazione:payload.occupazione_label,
      z:{name:data.zone.name,city:(data.geocode?.city || payload.citta || 'Lombardia'),trend:'mercato locale',tempi:'variabili in base al prezzo e allo stato',domanda:'attiva',code:data.zone.code},
      geoMetodo:data.source,
      fullAddress:data.geocode.formatted,
      dataSource:'OMI',
      quote:data.quote
    };

    mostraRisultato(r,payload.nome);

  }catch(err){
    console.error('Errore motore valutazione:',err);
    window.__lastValuationPayload = payload;
    window.__lastFullAddress = fullAddress;
    window.__lastValuationData = {ok:false, code:'NETWORK_OR_ENGINE_ERROR', technical:String(err?.message||err)};
    mostraErroreValutazione('Non siamo riusciti a completare la verifica in questo momento. Nessun valore è stato calcolato per evitare un valore poco affidabile.', {code:'NETWORK_OR_ENGINE_ERROR', technical:String(err?.message||err)});
  }finally{
    btn.disabled=false;
    btn.innerHTML='<i class="fa-solid fa-magnifying-glass-chart"></i> Mostra il valore indicativo';
  }
}

async function inviaLead(payload, fullAddress, valuation){
  const ok=valuation?.ok;
  const body={
    _subject: ok ? '🏠 Nuova valutazione — '+payload.nome : '🏠 Richiesta da verificare — '+payload.nome,
    nome:payload.nome,
    telefono:payload.telefono,
    email:payload.email||'',
    citta:payload.citta,
    indirizzo:fullAddress,
    indirizzo_google:valuation?.geocode?.formatted || '',
    coordinate:valuation?.geocode ? `${valuation.geocode.lat}, ${valuation.geocode.lng}` : '',
    esito_motore: ok ? 'valore_calcolato' : (valuation?.code || 'non_calcolato'),
    messaggio_motore: valuation?.message || '',
    zona:valuation?.zone?.name || '',
    zona_codice:valuation?.zone?.code || '',
    sorgente_dati:valuation?.source || '',
    semestre:valuation?.semester || '',
    tipo_immobile:payload.tipo,
    mq:payload.mq,
    locali:payload.locali,
    piano:payload.piano_label,
    stato:payload.stato_label,
    ascensore:payload.ascensore_label,
    anno_indicativo:payload.anno_label,
    classe_energetica:payload.classe_label,
    spazio_esterno:payload.esterno_label,
    box_posto_auto:payload.box_label,
    situazione_immobile:payload.occupazione_label,
    valore_stimato: ok ? `${fmt(valuation.result.vMin)} – ${fmt(valuation.result.vMax)}` : '',
    prezzo_mq: ok ? `${fmtK(valuation.result.pMq)} €/mq` : '',
    sorgente:'ValoreCasaTua.it — motore valutazione controllato'
  };
  return fetch('https://formspree.io/f/xnjrqgro',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(body)});
}

function mostraErroreValutazione(message, data){
  if (window.vctTrack) vctTrack('stima_error', { code: (data && data.code) || 'unknown' });
  const ris=document.getElementById('risultato');
  document.getElementById('resGreet').textContent='Dati ricevuti';
  document.getElementById('resRange').textContent='Indirizzo da verificare';
  document.getElementById('resMid').textContent='Non mostriamo un valore se la zona non è riconosciuta con sufficiente affidabilità.';
  document.querySelector('.res-discl').innerHTML='<i class="fa-solid fa-circle-info"></i> Meglio nessun valore che un dato generico o poco attendibile.';
  document.getElementById('resMetrics').innerHTML=`
    <div class="rm"><div class="rm-l">Esito</div><div class="rm-v">Da verificare</div></div>
    <div class="rm"><div class="rm-l">Motivo</div><div class="rm-v">${escapeHtml(data?.code || 'zona non certa')}</div></div>
    <div class="rm"><div class="rm-l">Azione</div><div class="rm-v">Controlla indirizzo</div></div>`;
  document.getElementById('aiContent').innerHTML=`<p>${escapeHtml(message)}</p><p>Controlla che via, numero civico e città siano corretti. Se l’indirizzo non è riconosciuto con sufficiente precisione o non è associabile a una zona OMI disponibile, la richiesta viene comunque raccolta ma il valore numerico automatico viene mostrato solo quando i dati territoriali sono sufficientemente affidabili.</p>`;
  const waMsg=encodeURIComponent(`Ciao, ho inserito i dati su ValoreCasaTua.it ma l'indirizzo è da verificare. Indirizzo: ${document.getElementById('addr').value}`);
  document.getElementById('waBtn').href=`https://wa.me/393516292353?text=${waMsg}`;
  const leadAfter=document.getElementById('leadAfter');
  if(leadAfter) leadAfter.style.display='block';
  const leadFields=document.getElementById('leadFields');
  if(leadFields) leadFields.hidden=true;
  const btnShow=document.getElementById('btnShowLead');
  if(btnShow) btnShow.style.display='';
  const body=document.querySelector('.fc-body');
  if(body) body.style.display='none';
  ris.hidden=false;
  ris.classList.add('is-open');
  ris.style.display='block';
  ris.scrollIntoView({behavior:'smooth',block:'start'});
}


function showLeadForm(){
  if (window.vctTrack) vctTrack('riepilogo_open');
  const fields=document.getElementById('leadFields');
  const btn=document.getElementById('btnShowLead');
  if(fields){ fields.hidden=false; }
  if(btn){ btn.style.display='none'; }
  document.getElementById('gNome')?.focus();
}

async function submitLeadRiepilogo(){
  const payload = Object.assign({}, window.__lastValuationPayload || readValuationPayload(), {
    nome: cleanText(document.getElementById('gNome').value),
    telefono: cleanText(document.getElementById('gTel').value),
    email: cleanText(document.getElementById('gEmail').value)
  });
  const gdpr = document.getElementById('gGdpr')?.checked;
  document.querySelectorAll('#leadAfter .err-msg').forEach(e=>e.classList.remove('on'));
  let ok=true;
  if(!payload.nome){document.getElementById('e-nome')?.classList.add('on');ok=false;}
  if(!payload.telefono||payload.telefono.replace(/\D/g,'').length<9){document.getElementById('e-tel')?.classList.add('on');ok=false;}
  if(payload.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email)){document.getElementById('e-email')?.classList.add('on');ok=false;}
  if(!gdpr){document.getElementById('e-gdpr')?.classList.add('on');ok=false;}
  if(!ok) return;

  const btn=document.getElementById('btnLead');
  if(btn){btn.disabled=true;btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> Invio…';}
  const fullAddress = window.__lastFullAddress || document.getElementById('addr')?.value || '';
  const valuation = window.__lastValuationData || {ok:false, code:'lead_only'};
  try{
    await inviaLead(payload, fullAddress, valuation);
    if (window.vctTrack) vctTrack('lead_submit_success',{form_id:'home_riepilogo'});vctTrack('riepilogo_lead');
    const thanks=document.getElementById('leadThanks');
    if(thanks){ thanks.hidden=false; thanks.style.display='block'; }
    if(btn) btn.style.display='none';
    const wa=document.getElementById('waBtn');
    if(wa){
      const range = valuation?.ok && valuation?.result
        ? `${fmt(valuation.result.vMin)} – ${fmt(valuation.result.vMax)}`
        : 'da approfondire';
      const zona = valuation?.zone?.name || payload.citta || '';
      wa.href = `https://wa.me/393516292353?text=${encodeURIComponent(`Ciao, sono ${payload.nome}. Ho calcolato il valore indicativo su ValoreCasaTua.it (${zona}: ${range}) e vorrei il quadro completo.`)}`;
    }
  }catch(err){
    console.error(err);
    if(btn){btn.disabled=false;btn.innerHTML='<i class="fa-solid fa-paper-plane"></i> Ricevi il riepilogo';}
    alert('Invio non riuscito. Riprova o scrivici su WhatsApp.');
  }
}

function escapeHtml(str){
  return String(str||'').replace(/[&<>'"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

function mostraRisultato(r,nome){
  if (window.vctTrack) vctTrack('stima_result', { zona: (r.z && r.z.name) || '', v_mid: r.vMid || 0 });
  const greet = nome
    ? `Ciao ${nome}! Ecco il valore indicativo del tuo immobile in zona ${r.z.name}.`
    : `Ecco il valore indicativo del tuo immobile in zona ${r.z.name}.`;
  document.getElementById('resGreet').textContent=greet;
  const leadAfter=document.getElementById('leadAfter');
  if(leadAfter) leadAfter.style.display='block';
  const leadFields=document.getElementById('leadFields');
  if(leadFields) leadFields.hidden=true;
  const thanks=document.getElementById('leadThanks');
  if(thanks){ thanks.hidden=true; thanks.style.display='none'; }
  const btnShow=document.getElementById('btnShowLead');
  if(btnShow) btnShow.style.display='';
  const btnLead=document.getElementById('btnLead');
  if(btnLead){ btnLead.disabled=false; btnLead.style.display=''; }
  document.getElementById('resRange').textContent=`${fmt(r.vMin)} – ${fmt(r.vMax)}`;
  document.getElementById('resMid').textContent='Valore indicativo: '+fmt(r.vMid);
  document.querySelector('.res-discl').innerHTML='<i class="fa-solid fa-circle-info"></i> Elaborazione automatica a fini informativi, basata su indirizzo riconosciuto, zona territoriale e dati inseriti.';
  document.getElementById('resMetrics').innerHTML=`
    <div class="rm"><div class="rm-l">Prezzo al m²</div><div class="rm-v">${fmtK(r.pMq)} €/mq</div></div>
    <div class="rm"><div class="rm-l">Zona</div><div class="rm-v">${escapeHtml(r.z.code||'rilevata')}</div></div>
    <div class="rm"><div class="rm-l">Fonte dati</div><div class="rm-v">${escapeHtml(r.dataSource||'territoriale')}</div></div>`;
  const waMsg=encodeURIComponent(`Ciao, ho calcolato il valore indicativo su ValoreCasaTua.it per un immobile in zona ${r.z.name}: ${fmt(r.vMin)} – ${fmt(r.vMax)}. Vorrei il quadro completo sui numeri.`);
  document.getElementById('waBtn').href=`https://wa.me/393516292353?text=${waMsg}`;
  const body=document.querySelector('.fc-body');
  if(body) body.style.display='none';
  const ris=document.getElementById('risultato');
  ris.hidden=false;
  ris.classList.add('is-open');
  ris.style.display='block';
  ris.scrollIntoView({behavior:'smooth',block:'start'});
  generaRiepilogo(r,nome);
}

function generaRiepilogo(r,nome){
  const box=document.getElementById('aiContent');
  box.innerHTML=`
    <p>Il valore indicativo è stato calcolato solo dopo il riconoscimento dell’indirizzo e l’associazione a una zona territoriale di riferimento. La fascia ottenuta è ${fmt(r.vMin)} – ${fmt(r.vMax)}, con valore centrale pari a ${fmt(r.vMid)}.</p>
    <p>Il calcolo tiene conto della superficie inserita (${r.mq} mq), della tipologia, dello stato dell’immobile e dei principali elementi dichiarati: piano, ascensore, classe energetica, spazi esterni e pertinenze.</p>
    <p>Il valore finale può variare dopo verifiche su stato reale, esposizione, documentazione, pertinenze e confronto con immobili simili effettivamente presenti nella stessa area.</p>`;
}

// ── Mappa ──
function fillAndScroll(city){
  // Prova a capire provincia dalla zona
  const provMap={
    'Milano':'Milano','Navigli':'Milano','Brera':'Milano','Sesto San Giovanni':'Milano',
    'Monza':'Monza e Brianza','Bergamo':'Bergamo','Brescia':'Brescia',
    'Como':'Como','Varese':'Varese','Lecco':'Lecco','Lodi':'Lodi',
    'Pavia':'Pavia','Cremona':'Cremona','Mantova':'Mantova','Sondrio':'Sondrio',
    'Lago di Garda':'Brescia','Desenzano':'Brescia','Sirmione':'Brescia',
    'Lago di Como':'Como','Bellagio':'Como','Livigno':'Sondrio','Bormio':'Sondrio',
  };
  let prov='';
  for(const[k,v] of Object.entries(provMap)){
    if(city.toLowerCase().includes(k.toLowerCase())){prov=v;break;}
  }
  document.getElementById('citta').value=city;
  document.getElementById('addr').value=city;
  document.getElementById('form').scrollIntoView({behavior:'smooth'});
}
function styleProv(f){
  const nm=f.properties.prov_name;const p=PROV_PRICE[nm]||2000;
  return{fillColor:priceColor(p),color:'rgba(255,255,255,.7)',weight:1.5,fillOpacity:0.6,opacity:1};
}
async function loadGeo(){
  try{const r=await fetch('/data/lombardia-province.geojson');return await r.json();}catch(e){return null;}
}
function renderMarkers(){
  mMarkers.forEach(m=>m.remove());mMarkers=[];let n=0;
  const visible=ZONES.filter(z=>mTag==='all'||z.tag===mTag);
  visible.forEach(z=>{
    const d=getD(z);if(!d)return;
    const col=priceColor(d.mid);
    // Cerchio più grande su mobile
    const circ=L.circleMarker([z.lat,z.lng],{radius:13,fillColor:col,color:'white',weight:2.5,fillOpacity:0.92,opacity:1}).addTo(mapInst);
    const lbl=L.divIcon({className:'',html:`<div style="font-family:'Hanken Grotesk',system-ui,sans-serif;font-size:8.5px;font-weight:700;color:white;text-shadow:0 1px 3px rgba(0,0,0,.8);pointer-events:none;text-align:center;margin-top:-2px;">${fmtK(d.mid)}</div>`,iconSize:[50,14],iconAnchor:[25,17]});
    const lm=L.marker([z.lat,z.lng],{icon:lbl,interactive:false}).addTo(mapInst);
    circ.on('mouseover click',function(){
      this.setStyle({radius:17,fillOpacity:1,weight:3});
      selectZone(z);
    });
    circ.on('mouseout',function(){this.setStyle({radius:13,fillOpacity:0.92,weight:2.5});});
    mMarkers.push(circ,lm);n++;
  });
  // Aggiorna stats
  const mids=visible.map(z=>getD(z)?.mid||0).filter(Boolean);
  if(mids.length){
    document.getElementById('sAvg').textContent=fmt(Math.round(mids.reduce((a,b)=>a+b,0)/mids.length));
    document.getElementById('sZones').textContent=n;
  }
  // Render zone cards
  renderZoneCards(visible);
}

function selectZone(z){
  const d=getD(z);if(!d)return;
  const col=priceColor(d.mid);
  // Aggiorna info bar
  document.getElementById('mapInfo').innerHTML=`<strong style="color:${col}">${z.name}</strong> — ${fmt(d.mid)}/mq · ▲ ${z.trend}`;
  // Fly to
  mapInst.flyTo([z.lat,z.lng],13,{duration:0.8});
  // Highlight card
  document.querySelectorAll('.zcard-mobile').forEach(c=>c.classList.remove('active'));
  const card=document.getElementById('zc-'+z.id);
  if(card){card.classList.add('active');card.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'});}
}

function renderZoneCards(zones){
  const container=document.getElementById('zoneCards');
  const hint=document.getElementById('scrollHint');
  if(!container)return;
  container.innerHTML=zones.map(z=>{
    const d=getD(z);if(!d)return'';
    const col=priceColor(d.mid);
    return `<div class="zcard-mobile" id="zc-${z.id}" onclick="selectZone(${JSON.stringify(z).replace(/"/g,"'").replace(/'/g,'"')})" style="border-color:${col}33">
      <div class="zcard-accent" style="background:${col}"></div>
      <div style="padding-left:8px">
        <div class="zcard-city">${z.city}</div>
        <div class="zcard-name">${z.name}</div>
        <div class="zcard-price">${fmtK(d.mid)} <span style="font-size:.65rem;font-weight:400;color:var(--muted)">€/mq</span></div>
        <div class="zcard-trend">▲ ${z.trend}</div>
      </div>
    </div>`;
  }).join('');
  // Mostra/nascondi scroll hint
  if(hint)hint.style.display=zones.length>3?'flex':'none';
  // Re-bind click sulle card per fill form
  document.querySelectorAll('.zcard-mobile').forEach(card=>{
    card.addEventListener('dblclick',()=>{
      fillAndScroll(card.querySelector('.zcard-name').textContent);
    });
  });
}
function flyCity(tag,btn){
  mTag=tag;document.querySelectorAll('.ctab').forEach(b=>b.classList.remove('on'));if(btn)btn.classList.add('on');
  if(!mapInst){ initMapWhenReady(); return; }
  const v=VIEWS[tag]||VIEWS.all;mapInst.flyTo(v.c,v.z,{duration:1});
  renderMarkers();if(geoLayer)geoLayer.setStyle(f=>styleProv(f));
}

// ── FAQ ──
function toggleFaq(btn){
  const isOpen=btn.classList.contains('open');
  document.querySelectorAll('.fq-q').forEach(q=>{q.classList.remove('open');q.setAttribute('aria-expanded','false');if(q.nextElementSibling)q.nextElementSibling.classList.remove('open');});
  if(!isOpen){btn.classList.add('open');btn.setAttribute('aria-expanded','true');if(btn.nextElementSibling)btn.nextElementSibling.classList.add('open');}
}

// ── Init mappa (lazy: Leaflet + tiles solo quando #zone è vicino) ──
function loadLeafletAssets(){
  if(window.__vctLeafletReady) return window.__vctLeafletReady;
  window.__vctLeafletReady = new Promise(function(resolve, reject){
    if(typeof L !== 'undefined'){ resolve(); return; }
    var css=document.createElement('link');
    css.rel='stylesheet';
    css.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(css);
    var s=document.createElement('script');
    s.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    s.onload=function(){ resolve(); };
    s.onerror=reject;
    document.head.appendChild(s);
  });
  return window.__vctLeafletReady;
}
async function initMapWhenReady(){
  try{
    var mapEl=document.getElementById('map');
    var details=document.getElementById('zoneCollapse');
    // Non inizializzare se il pannello è chiuso (altezza 0 → mappa bianca)
    if(details && !details.open) return;
    if(typeof L==='undefined') await loadLeafletAssets();
    if(typeof L==='undefined' || !mapEl) return;
    if(!window.__vctMapStarted){
      window.__vctMapStarted=true;
      mapInst=L.map('map',{center:[45.65,9.90],zoom:8.5,zoomControl:false,scrollWheelZoom:false});
      L.control.zoom({position:'topright'}).addTo(mapInst);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>',maxZoom:19,className:'vct-osm-tiles'}).addTo(mapInst);
      
      const geo=await loadGeo();
      if(geo){geoLayer=L.geoJSON(geo,{style:styleProv,onEachFeature:(f,layer)=>{layer.on({mouseover(){this.setStyle({fillOpacity:0.85,weight:2.5,color:'white'});this.bringToFront();},mouseout(){geoLayer.resetStyle(this);}});}}).addTo(mapInst);}
      renderMarkers();
    }
    var loader=document.getElementById('mapLoader');
    if(loader) loader.style.display='none';
    // Ricalcola dimensioni dopo l'apertura del <details>
    if(mapInst){
      setTimeout(function(){ try{ mapInst.invalidateSize(true); }catch(e){} }, 80);
      setTimeout(function(){ try{ mapInst.invalidateSize(true); }catch(e){} }, 320);
    }
  }catch(e){ console.warn('Map init skipped', e); }
}
(function(){
  var details=document.getElementById('zoneCollapse');
  var target=document.getElementById('zone') || document.getElementById('map');
  function tryInit(){
    if(details && !details.open) return;
    loadLeafletAssets().then(initMapWhenReady);
  }
  function openZonePanel(scroll){
    if(!details) return;
    details.open=true;
    tryInit();
    if(scroll && target){
      requestAnimationFrame(function(){
        target.scrollIntoView({behavior:'smooth', block:'start'});
      });
    }
  }
  if(details){
    details.addEventListener('toggle', function(){
      if(details.open) tryInit();
    });
    if(details.open) tryInit();
  }
  if(target && 'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
      if(entries.some(function(e){ return e.isIntersecting; })){
        tryInit();
      }
    },{rootMargin:'200px 0px'});
    io.observe(target);
  }else if(!details && document.getElementById('map')){
    window.addEventListener('load', tryInit, {once:true});
  }
  function isZoneHash(h){
    return h==='#zone' || h==='#zoneCollapse';
  }
  // Deep link / click #zone → apri il pannello e avvia la mappa
  if(details && isZoneHash(location.hash)){
    openZonePanel(false);
  }
  window.addEventListener('hashchange', function(){
    if(isZoneHash(location.hash)) openZonePanel(true);
  });
  document.addEventListener('click', function(e){
    var a=e.target && e.target.closest ? e.target.closest('a[href="#zone"], a[href="#zoneCollapse"]') : null;
    if(!a) return;
    e.preventDefault();
    if(location.hash!=='#zone') history.pushState(null,'','#zone');
    openZonePanel(true);
  });
})();
