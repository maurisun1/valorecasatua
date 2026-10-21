/*! ValoreCasaTua — A/B tests (sticky assignment + GA) */
(function () {
  if (window.__vctAbReady) return;
  window.__vctAbReady = true;

  function getBucket(key) {
    try {
      var stored = localStorage.getItem(key);
      if (stored === "A" || stored === "B") return stored;
      var b = Math.random() < 0.5 ? "A" : "B";
      localStorage.setItem(key, b);
      return b;
    } catch (e) {
      return Math.random() < 0.5 ? "A" : "B";
    }
  }

  /** A = control, B = variant */
  var navBucket = getBucket("vct_ab_nav_cta");
  var phoneBucket = getBucket("vct_ab_checkup_phone");

  window.VCT_AB = {
    nav_cta: navBucket,
    checkup_phone: phoneBucket
  };

  function trackAssign() {
    if (typeof window.vctTrack !== "function") return;
    window.vctTrack("ab_assign", {
      ab_nav_cta: navBucket,
      ab_checkup_phone: phoneBucket
    });
  }

  /**
   * Nav CTA A/B
   * A (control): always "Valuta gratis" → /#form
   * B (variant): contextual CTA (default vct-conversion behavior)
   */
  function applyNavAb() {
    document.querySelectorAll("a.nav-cta").forEach(function (a) {
      if (navBucket === "A") {
        a.textContent = "Valuta gratis";
        a.setAttribute("href", location.pathname.replace(/\/$/, "") === "" || location.pathname === "/" ? "#form" : "/#form");
      }
      a.setAttribute("data-ab-nav", navBucket);
      a.addEventListener("click", function () {
        if (typeof window.vctTrack === "function") {
          window.vctTrack("nav_cta_click", {
            cta_text: (a.textContent || "").trim(),
            destination: a.getAttribute("href") || "",
            ab_nav_cta: navBucket
          });
        }
      });
    });
  }

  /**
   * Check-Up phone A/B (only on /verifica-casa)
   * A (control): telefono required
   * B (variant): email required, telefono optional
   */
  function applyCheckupPhoneAb() {
    var path = (location.pathname || "").replace(/\/+$/, "");
    if (path !== "/verifica-casa") return;
    var form = document.querySelector('form[name="verifica-casa"]');
    if (!form) return;
    var tel = form.querySelector('input[name="telefono"]');
    var email = form.querySelector('input[name="email"]');
    if (!tel || !email) return;

    if (phoneBucket === "B") {
      tel.required = false;
      email.required = true;
      var telLab = tel.closest("label");
      if (telLab) {
        telLab.innerHTML = telLab.innerHTML
          .replace(/WhatsApp \* \(per inviarti il riepilogo\)/i, "WhatsApp (consigliato)")
          .replace(/Telefono\s*\/\s*WhatsApp\s*\*?/i, "WhatsApp (consigliato)");
      }
      var emailLab = email.closest("label");
      if (emailLab && emailLab.childNodes[0]) {
        var t = emailLab.childNodes[0];
        if (t.nodeType === 3) t.textContent = "Email *";
      }
      var hint = form.querySelector(".vct-field-hint");
      if (hint) {
        hint.textContent = "Variante B: puoi lasciare solo l’email. WhatsApp aiuta a risponderti più in fretta.";
      }
      form.setAttribute("data-ab-phone", "B");
    } else {
      form.setAttribute("data-ab-phone", "A");
    }

    form.addEventListener("submit", function () {
      if (typeof window.vctTrack === "function") {
        window.vctTrack("lead_submit_attempt", {
          form_id: "verifica-casa",
          ab_checkup_phone: phoneBucket,
          has_phone: !!(tel.value || "").trim(),
          has_email: !!(email.value || "").trim()
        });
      }
    });
  }

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    // Run after conversion.js nav rewrite
    setTimeout(function () {
      applyNavAb();
      applyCheckupPhoneAb();
      trackAssign();
    }, 0);
  });
})();
