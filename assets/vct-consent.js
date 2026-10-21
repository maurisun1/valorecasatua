/*! ValoreCasaTua — consenso cookie. GA4 e Clarity partono solo dopo Accetta. */
(function () {
  var GA_ID = "G-K3J7XYVDCE";
  var CLARITY_ID = "yru9irlvs0";
  var KEY = "vct_cookie_consent";

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() { window.dataLayer.push(arguments); };
  window.gtag("consent", "default", {
    analytics_storage: "denied",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied"
  });

  function readChoice() {
    var raw;
    try { raw = localStorage.getItem(KEY); } catch (e) { return null; }
    if (!raw) return null;
    if (raw === "accepted" || raw === "rejected") {
      try { localStorage.removeItem(KEY); } catch (e) {}
      return null;
    }
    try {
      var data = JSON.parse(raw);
      if (!data || (data.choice !== "accepted" && data.choice !== "rejected") || !data.exp || Date.now() > data.exp) {
        localStorage.removeItem(KEY);
        return null;
      }
      return data.choice;
    } catch (e) {
      try { localStorage.removeItem(KEY); } catch (err) {}
      return null;
    }
  }

  function writeChoice(choice) {
    var exp = new Date();
    exp.setMonth(exp.getMonth() + 6);
    try {
      localStorage.setItem(KEY, JSON.stringify({ choice: choice, exp: exp.getTime() }));
    } catch (e) {}
  }

  function injectStyles() {
    if (document.getElementById("vct-ck-style")) return;
    var style = document.createElement("style");
    style.id = "vct-ck-style";
    style.textContent = [
      "#cookieBanner{position:fixed;left:10px;right:10px;bottom:10px;z-index:99999;max-height:25vh;overflow:auto;background:#0f172a;color:rgba(255,255,255,.92);border-radius:16px;box-shadow:0 -8px 28px rgba(0,0,0,.28);font-family:'Hanken Grotesk',system-ui,sans-serif}",
      "#cookieBanner .vct-ck{position:relative;padding:12px 14px 12px}",
      "#cookieBanner .vct-ck-x{position:absolute;top:4px;right:4px;width:44px;height:44px;border:0;background:transparent;color:#fff;font-size:22px;line-height:1;cursor:pointer}",
      "#cookieBanner .vct-ck-text{margin:0 40px 10px 0;font-size:13px;line-height:1.35}",
      "#cookieBanner .vct-ck-actions{display:flex;gap:8px}",
      "#cookieBanner .vct-ck-btn{flex:1;min-height:44px;padding:10px 12px;border-radius:10px;border:1.5px solid #2f9488;background:#2f9488;color:#fff;font:700 14px/1.2 'Hanken Grotesk',system-ui,sans-serif;cursor:pointer}",
      "#cookieBanner .vct-ck-btn:active{background:#0f5c54}",
      "#cookieBanner .vct-ck-links{margin:8px 0 0;font-size:13px;line-height:1.4}",
      "#cookieBanner .vct-ck-links button,#cookieBanner .vct-ck-links a{background:none;border:0;padding:8px 0;color:#5eead4;font:700 13px/1.2 'Hanken Grotesk',system-ui,sans-serif;text-decoration:underline;cursor:pointer}",
      "#cookieBanner .vct-ck-panel[hidden]{display:none}#cookieBanner .vct-ck-panel{margin-top:8px;display:flex;flex-direction:column;gap:6px}",
      "#cookieBanner .vct-ck-panel label{display:flex;align-items:center;gap:8px;font-size:13px;min-height:32px}",
      "body.vct-ck-open{padding-bottom:var(--vct-ck-h,120px)}",
      "body.vct-ck-open .wa-float{bottom:calc(var(--vct-ck-h,120px) + 8px)!important}",
      "body.vct-ck-open .btn-next,body.vct-ck-open .hero-main-cta{scroll-margin-bottom:calc(var(--vct-ck-h,120px) + 12px)}"
    ].join("");
    document.head.appendChild(style);
  }

  function syncOffset() {
    var banner = document.getElementById("cookieBanner");
    if (!banner || banner.hidden) {
      document.body.classList.remove("vct-ck-open");
      document.body.style.removeProperty("--vct-ck-h");
      return;
    }
    document.body.classList.add("vct-ck-open");
    document.body.style.setProperty("--vct-ck-h", (banner.offsetHeight + 20) + "px");
  }

  function hideBanner() {
    var banner = document.getElementById("cookieBanner");
    if (banner) banner.hidden = true;
    syncOffset();
  }

  function showBanner() {
    ensureBanner();
    var banner = document.getElementById("cookieBanner");
    if (!banner) return;
    banner.hidden = false;
    var panel = document.getElementById("vctCkPanel");
    if (panel) panel.hidden = true;
    syncOffset();
  }

  function ensureBanner() {
    injectStyles();
    var old = document.getElementById("cookieBanner");
    if (old) old.parentNode.removeChild(old);
    var banner = document.createElement("div");
    banner.id = "cookieBanner";
    banner.hidden = true;
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-label", "Preferenze cookie");
    banner.innerHTML = ''
      + '<div class="vct-ck">'
      + '<button type="button" class="vct-ck-x" id="vctCloseCookies" aria-label="Chiudi e rifiuta i cookie di analisi">&times;</button>'
      + '<p class="vct-ck-text">Usiamo cookie tecnici necessari e, con il tuo consenso, cookie di analisi per migliorare il sito.</p>'
      + '<div class="vct-ck-actions">'
      + '<button type="button" class="vct-ck-btn" id="vctRejectCookies">Rifiuta</button>'
      + '<button type="button" class="vct-ck-btn" id="vctAcceptCookies">Accetta</button>'
      + '</div>'
      + '<p class="vct-ck-links"><button type="button" id="vctCustomizeCookies">Personalizza</button> · <a href="/cookie/">Cookie policy</a></p>'
      + '<div class="vct-ck-panel" id="vctCkPanel" hidden>'
      + '<label><input type="checkbox" checked disabled> Cookie tecnici, sempre attivi</label>'
      + '<label><input type="checkbox" id="vctAnalyticsOpt"> Cookie di analisi</label>'
      + '<button type="button" class="vct-ck-btn" id="vctSaveCookies">Salva</button>'
      + '</div></div>';
    document.body.appendChild(banner);
    document.getElementById("vctAcceptCookies").onclick = function () { window.vctConsentChoice("accepted"); };
    document.getElementById("vctRejectCookies").onclick = function () { window.vctConsentChoice("rejected"); };
    document.getElementById("vctCloseCookies").onclick = function () { window.vctConsentChoice("rejected"); };
    document.getElementById("vctCustomizeCookies").onclick = function () {
      var panel = document.getElementById("vctCkPanel");
      if (panel) panel.hidden = !panel.hidden;
      syncOffset();
    };
    document.getElementById("vctSaveCookies").onclick = function () {
      var box = document.getElementById("vctAnalyticsOpt");
      window.vctConsentChoice(box && box.checked ? "accepted" : "rejected");
    };
  }

  window.vctConsentChoice = function (choice) {
    writeChoice(choice);
    hideBanner();
    if (choice === "accepted") window.vctLoadAnalytics();
  };
  window.acceptCookies = function () { window.vctConsentChoice("accepted"); };
  window.rejectCookies = function () { window.vctConsentChoice("rejected"); };

  window.vctLoadAnalytics = function () {
    if (window.__vctAnalyticsLoaded) return;
    window.__vctAnalyticsLoaded = true;
    window.gtag("consent", "update", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied"
    });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_ID);
    document.head.appendChild(s);
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true, send_page_view: true });

    window.clarity = window.clarity || function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r);
      t.async = 1;
      t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0];
      y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", CLARITY_ID);
    window.clarity("consent");
  };

  window.vctManageCookies = function () {
    try { localStorage.removeItem(KEY); } catch (e) {}
    showBanner();
    return false;
  };

  function boot() {
    if (readChoice() === "accepted") window.vctLoadAnalytics();
    else if (readChoice() !== "rejected") showBanner();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
