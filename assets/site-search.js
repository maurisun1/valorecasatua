/*! ValoreCasaTua — cerca sito (lente in header) */
(function () {
  if (window.__vctSearchInit) return;
  window.__vctSearchInit = true;

  var PAGES = [
    { t: "Stima valore casa", u: "/", k: "valutazione omi milano lombardia" },
    { t: "Check-Up Casa", u: "/verifica-casa/", k: "documenti ape planimetria" },
    { t: "Conviene ristrutturare?", u: "/conviene-ristrutturare/", k: "ristrutturazione costi" },
    { t: "Affitto breve vs transitorio", u: "/affitto-breve-vs-transitorio/", k: "affitto rendimento" },
    { t: "Classe energetica", u: "/classe-energetica-valore-casa/", k: "ape energia" },
    { t: "Casa ricevuta in donazione", u: "/vendere-casa-ricevuta-in-donazione/", k: "donazione casa donata vendita" },
    { t: "Centro Risorse", u: "/risorse/", k: "guide" },
    { t: "Prezzi al m² Lombardia", u: "/guide/", k: "prezzi metro quadro" },
    { t: "Prezzi Milano", u: "/guide/prezzi-mq-milano/", k: "milano omi valutazione immobile prezzi mq" },
    { t: "Prezzi Brescia", u: "/guide/prezzi-mq-brescia/", k: "brescia valore casa" },
    { t: "Prezzi Lecco", u: "/guide/prezzi-mq-lecco/", k: "lecco stima immobiliare" },
    { t: "Prezzi Bergamo", u: "/guide/prezzi-mq-bergamo/", k: "bergamo" },
    { t: "Prezzi Como", u: "/guide/prezzi-mq-como/", k: "como" },
    { t: "Prezzi Monza", u: "/guide/prezzi-mq-monza-brianza/", k: "monza" },
    { t: "Prezzi Varese", u: "/guide/prezzi-mq-varese/", k: "varese" },
    { t: "Separazione / divorzio", u: "/casa-separazione-divorzio-lombardia/", k: "separazione" },
    { t: "Casa ereditata", u: "/casa-ereditata-divisione-eredi-lombardia/", k: "eredità" },
    { t: "Comprare prima di vendere", u: "/comprare-casa-prima-di-vendere/", k: "acquisto" },
    { t: "Casa vuota o sfitta", u: "/casa-vuota-sfitta-cosa-fare/", k: "sfitta" },
    { t: "Trasferimento lavoro", u: "/trasferimento-lavoro-vendere-affittare-casa/", k: "trasferimento" },
    { t: "Pensione e cambio casa", u: "/pensione-cambiare-casa/", k: "pensione" },
    { t: "Mercato Lombardia 2026", u: "/mercato-immobiliare-lombardia-2026/", k: "mercato" },
    { t: "Quanto costa vendere", u: "/quanto-costa-vendere-casa/", k: "costi" },
    { t: "Vendere con mutuo", u: "/vendere-casa-con-mutuo/", k: "mutuo in corso vendere" },
    { t: "Nuda proprietà", u: "/vendere-nuda-proprieta-usufrutto/", k: "usufrutto" },
    { t: "Difformità edilizie", u: "/vendere-casa-non-conforme-difformita/", k: "difformità conformità catasto" },
    { t: "Vendere da soli", u: "/vendere-casa-da-soli/", k: "senza agenzia" },
    { t: "Casa con inquilino", u: "/vendere-casa-affittata-inquilino/", k: "inquilino" },
    { t: "Comproprietà in disaccordo", u: "/vendere-casa-comproprieta-disaccordo/", k: "comproprietà" },
    { t: "Plusvalenza vendita", u: "/plusvalenza-vendita-casa/", k: "plusvalenza tassa prima casa" },
    { t: "Checklist documenti PDF", u: "/checklist-documenti-vendere-casa/", k: "checklist" },
    { t: "Chi siamo", u: "/chi-siamo/", k: "progetto" }
  ];

  var CSS =
    ".vct-search-btn{display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;width:40px;height:40px;padding:0;margin:0 4px 0 8px;border:1px solid rgba(12,35,52,.12);border-radius:999px;background:#fff;color:#0c2334;cursor:pointer;transition:.2s}.vct-search-btn:hover,.vct-search-btn[aria-expanded=true]{background:rgba(47,148,136,.1);border-color:rgba(47,148,136,.4);color:#1a7a6f}.vct-search-btn svg{width:18px;height:18px}.vct-search-overlay{position:fixed;inset:0;z-index:2000;background:rgba(12,35,52,.42);display:none;align-items:flex-start;justify-content:center;padding:14vh 16px 20px}.vct-search-overlay.open{display:flex}.vct-search-panel{width:100%;max-width:520px;background:#fff;border-radius:16px;box-shadow:0 24px 70px rgba(12,35,52,.2);overflow:hidden}.vct-search-bar{display:flex;align-items:center;gap:10px;padding:14px 14px;border-bottom:1px solid rgba(12,35,52,.08)}.vct-search-bar svg{width:20px;height:20px;color:#1a7a6f;flex:none}.vct-search-bar input{flex:1;border:0;outline:0;font:inherit;font-size:16px;color:#0c2334;background:transparent}.vct-search-close{border:0;background:rgba(12,35,52,.06);width:32px;height:32px;border-radius:8px;cursor:pointer;font-size:18px;color:#0c2334}.vct-search-results{max-height:min(48vh,380px);overflow:auto;padding:8px}.vct-search-item{display:block;padding:11px 12px;border-radius:10px;text-decoration:none;color:#0c2334;font-size:14.5px;font-weight:650}.vct-search-item:hover{background:rgba(47,148,136,.1)}.vct-search-empty{padding:24px 14px;text-align:center;color:rgba(26,46,59,.5);font-size:14px}@media(max-width:900px){.vct-search-btn{margin:0 4px 0 auto;order:3}.vct-burger{order:4}}";

  function norm(s) {
    return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  function lens() {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>';
  }

  function render(q) {
    var box = document.getElementById("vctSearchResults");
    if (!box) return;
    var hits = PAGES.filter(function (p) {
      if (!q) return true;
      var hay = norm(p.t + " " + p.k);
      return q.split(/\s+/).every(function (w) { return !w || hay.indexOf(w) > -1; });
    }).slice(0, 10);
    if (!hits.length) {
      box.innerHTML = '<div class="vct-search-empty">Nessun risultato. Prova «mutuo» o «difformità»</div>';
      return;
    }
    box.innerHTML = hits.map(function (p) {
      return '<a class="vct-search-item" href="' + p.u + '">' + p.t + "</a>";
    }).join("");
  }

  function open() {
    var ov = document.getElementById("vctSearchOverlay");
    var btn = document.getElementById("vctSearchBtn");
    if (!ov) return;
    ov.classList.add("open");
    if (btn) btn.setAttribute("aria-expanded", "true");
    var inp = document.getElementById("vctSearchInput");
    if (inp) { inp.value = ""; render(""); setTimeout(function () { inp.focus(); }, 20); }
    document.documentElement.style.overflow = "hidden";
  }

  function close() {
    var ov = document.getElementById("vctSearchOverlay");
    var btn = document.getElementById("vctSearchBtn");
    if (ov) ov.classList.remove("open");
    if (btn) btn.setAttribute("aria-expanded", "false");
    document.documentElement.style.overflow = "";
  }

  function init() {
    if (!document.getElementById("vct-search-css")) {
      var st = document.createElement("style");
      st.id = "vct-search-css";
      st.textContent = CSS;
      document.head.appendChild(st);
    }

    var header = document.querySelector(".vct-header-inner");
    if (!header || document.getElementById("vctSearchBtn")) return;

    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = "vctSearchBtn";
    btn.className = "vct-search-btn";
    btn.setAttribute("aria-label", "Cerca nel sito");
    btn.setAttribute("aria-expanded", "false");
    btn.innerHTML = lens();

    // Sempre nell'header (prima del burger): visibile anche su mobile.
    // L'ordine CSS (order) la sposta a destra su desktop.
    var burger = header.querySelector(".vct-burger");
    if (burger) header.insertBefore(btn, burger);
    else header.appendChild(btn);

    var ov = document.createElement("div");
    ov.id = "vctSearchOverlay";
    ov.className = "vct-search-overlay";
    ov.innerHTML =
      '<div class="vct-search-panel" role="dialog" aria-label="Cerca">' +
      '<div class="vct-search-bar">' + lens() +
      '<input id="vctSearchInput" type="search" placeholder="Cerca: mutuo, Milano, difformità…" autocomplete="off">' +
      '<button type="button" class="vct-search-close" id="vctSearchClose" aria-label="Chiudi">×</button></div>' +
      '<div class="vct-search-results" id="vctSearchResults"></div></div>';
    document.body.appendChild(ov);

    btn.addEventListener("click", open);
    document.getElementById("vctSearchClose").addEventListener("click", close);
    ov.addEventListener("click", function (e) { if (e.target === ov) close(); });
    document.getElementById("vctSearchInput").addEventListener("input", function () {
      render(norm(this.value));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
