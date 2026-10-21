/*! ValoreCasaTua — tracking eventi funnel */
(function () {
  if (window.__vctTrackReady) return;
  window.__vctTrackReady = true;

  window.dataLayer = window.dataLayer || [];
  function gtag(){ window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  /**
   * vctTrack("nome_evento", { chiave: valore })
   * Eventi:
   *  - stima_start / stima_submit / stima_result / stima_error
   *  - riepilogo_open / riepilogo_lead
   *  - tool_start / tool_result_view
   *  - lead_form_start / lead_submit_attempt / lead_submit_success
   *  - cta_click / nav_cta_click / whatsapp_click
   *  - checklist_download
   */
  window.vctTrack = function (name, params) {
    try {
      var p = params || {};
      p.page_path = location.pathname;
      if (window.__vctAnalyticsLoaded && typeof window.gtag === "function") {
        window.gtag("event", name, p);
      }
    } catch (e) {}
  };
})();
