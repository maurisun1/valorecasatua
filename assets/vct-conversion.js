/*! ValoreCasaTua — nav CTA contestuale, WA prefill, tracking form */
(function () {
  if (window.__vctConversionReady) return;
  window.__vctConversionReady = true;

  var path = (location.pathname || "/").replace(/\/+$/, "") || "/";

  var NAV = {
    "/verifica-casa": { text: "Verifica gratis", href: "#score" },
    "/conviene-ristrutturare": { text: "Scopri se conviene", href: "#calcolatore" },
    "/affitto-breve-vs-transitorio": { text: "Calcola rendimento", href: "#calcolatore" },
    "/checklist-documenti-vendere-casa": { text: "Scarica la checklist", href: "#form" },
    "/classe-energetica-valore-casa": { text: "Valuta gratis", href: "/#form" },
    "/vendere-casa-ricevuta-in-donazione": { text: "Verifica situazione", href: "#form" },
    "/risorse": { text: "Valuta gratis", href: "/#form" },
    "/": { text: "Valuta gratis", href: "#form" }
  };

  var WA_MSG = {
    "/verifica-casa": "Ciao, vorrei il Check-Up Pre Vendita per il mio immobile.",
    "/conviene-ristrutturare": "Ciao, vorrei un orientamento su se conviene ristrutturare prima di vendere.",
    "/affitto-breve-vs-transitorio": "Ciao, vorrei confrontare affitto breve, transitorio e 4+4 per il mio immobile.",
    "/checklist-documenti-vendere-casa": "Ciao, vorrei la checklist documenti per vendere casa.",
    "/classe-energetica-valore-casa": "Ciao, vorrei capire quanto la classe energetica incide sul valore della mia casa.",
    "/vendere-casa-ricevuta-in-donazione": "Ciao, vorrei verificare la vendita di una casa ricevuta in donazione.",
    "/casa-separazione-divorzio-lombardia": "Ciao, vorrei un orientamento su valore e scenari della casa in separazione.",
    "/casa-ereditata-divisione-eredi-lombardia": "Ciao, vorrei un orientamento su casa ereditata e divisione tra eredi.",
    "/vendere-casa-da-soli": "Ciao, vorrei capire se sto vendendo al valore giusto da solo.",
    "/": "Ciao, vorrei una stima orientativa del valore della mia casa."
  };

  function navConfig() {
    if (NAV[path]) return NAV[path];
    if (path.indexOf("/guide/") === 0) return { text: "Valuta gratis", href: "/#form" };
    if (document.querySelector("#form, .vct-lead-section form, form.lead-form")) {
      return { text: "Ricevi orientamento", href: "#form" };
    }
    return { text: "Valuta gratis", href: "/#form" };
  }

  function waMessage() {
    if (WA_MSG[path]) return WA_MSG[path];
    var h1 = (document.querySelector("h1") || {}).textContent || "";
    h1 = h1.replace(/\s+/g, " ").trim().slice(0, 80);
    if (h1) return "Ciao, scrivo da ValoreCasaTua.it riguardo: " + h1;
    return WA_MSG["/"];
  }

  function enhanceNavCta() {
    var cfg = navConfig();
    document.querySelectorAll("a.nav-cta").forEach(function (a) {
      a.textContent = cfg.text;
      a.setAttribute("href", cfg.href);
      a.setAttribute("data-vct-cta", "nav");
    });
  }

  function enhanceWhatsApp() {
    var msg = encodeURIComponent(waMessage());
    var base = "https://wa.me/393516292353";
    document.querySelectorAll('a[href*="wa.me/393516292353"], a[href*="whatsapp"]').forEach(function (a) {
      var href = a.getAttribute("href") || "";
      if (href.indexOf("text=") !== -1) return;
      if (href === "#" || href.indexOf("javascript:") === 0) return;
      a.setAttribute("href", base + "?text=" + msg);
      a.setAttribute("data-vct-cta", "whatsapp");
    });
  }

  function trackClicks() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a, button");
      if (!a || typeof window.vctTrack !== "function") return;
      var href = a.getAttribute("href") || "";
      var text = (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80);
      if (a.classList.contains("nav-cta") || a.getAttribute("data-vct-cta") === "nav") {
        window.vctTrack("nav_cta_click", { cta_text: text, destination: href });
      }
      if (/wa\.me|whatsapp/i.test(href) || a.classList.contains("wa-float") || a.classList.contains("wa-btn")) {
        window.vctTrack("whatsapp_click", { location: a.className || "link", cta_text: text });
      }
      if (a.matches(".hero-main-cta, .btn-primary, .vct-bridge-cta, .vct-lead-btn, .cta, .btn-calc, .btn-next")) {
        window.vctTrack("cta_click", {
          cta_id: a.id || "",
          cta_text: text,
          location: (a.className || "").toString().slice(0, 60)
        });
      }
    }, true);
  }

  function trackForms() {
    document.querySelectorAll("form").forEach(function (form) {
      form.addEventListener("submit", function () {
        if (typeof window.vctTrack !== "function") return;
        var name = form.getAttribute("name") || form.id || "lead_form";
        window.vctTrack("lead_submit_attempt", { form_id: name });
      });
      var first = form.querySelector("input:not([type=hidden]), select, textarea");
      if (first) {
        first.addEventListener("focus", function once() {
          if (typeof window.vctTrack === "function") {
            window.vctTrack("lead_form_start", {
              form_id: form.getAttribute("name") || form.id || "lead_form",
              first_field: first.name || first.id || ""
            });
          }
          first.removeEventListener("focus", once);
        });
      }
    });
  }

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    enhanceNavCta();
    enhanceWhatsApp();
    trackClicks();
    trackForms();
    if (typeof window.vctTrack === "function") {
      window.vctTrack("page_context", { tool_path: path });
    }
  });
})();
