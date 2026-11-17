/* Rastreio dos cliques no WhatsApp.
   1. Guarda a origem da visita (UTM, gclid ou site de onde veio) por 90 dias,
      valendo o último toque que não foi direto.
   2. No clique em a[data-wa], acrescenta "(ref. NNNNN)" ao texto da mensagem
      e avisa clique.php por sendBeacon. O painel liga a conversa ao clique
      pelo código.
   Nada aqui pode impedir o WhatsApp de abrir: toda falha é engolida. */
(function () {
  "use strict";

  var CHAVE = "an_origem";
  var VALIDADE = 90 * 864e5;
  var CAMPOS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "gclid", "gbraid", "wbraid"];
  var SITE = "anitaodontologia.com.br";

  var R = {
    /* Conversão "Clique no WhatsApp" na conta do Google Ads da Dra.
       Preencher quando a conta existir; vazio = não dispara. */
    ADS: { id: "", rotulo: "" },
    endpoint: null,
    origemAtual: null
  };

  R.ref = function (rand) {
    var n = Math.floor((rand || Math.random)() * 100000);
    if (n > 99999) n = 99999;
    return ("0000" + n).slice(-5);
  };

  R.comRef = function (href, ref) {
    var m = /^(.*[?&]text=)([^&#]*)(.*)$/.exec(href);
    if (!m) return href + (href.indexOf("?") < 0 ? "?" : "&") + "text=" + encodeURIComponent("(ref. " + ref + ")");
    var txt;
    try { txt = decodeURIComponent(m[2].replace(/\+/g, " ")); } catch (e) { txt = ""; }
    txt = txt.replace(/\s*\(ref\. \d{5}\)\s*$/, "");
    txt = (txt ? txt + " " : "") + "(ref. " + ref + ")";
    return m[1] + encodeURIComponent(txt) + m[3];
  };

  function hostDe(url) {
    try { return new URL(url).hostname.toLowerCase(); } catch (e) { return ""; }
  }

  function interno(host) {
    return host === SITE || host.slice(-(SITE.length + 1)) === "." + SITE;
  }

  R.capturaOrigem = function (url, referrer, agora, salvo) {
    var params;
    try { params = new URL(url).searchParams; } catch (e) { params = null; }
    var nova = {};
    var tem = false;
    if (params) {
      CAMPOS.forEach(function (c) {
        var v = params.get(c);
        if (v) { nova[c] = v.slice(0, 300); tem = true; }
      });
    }
    var host = referrer ? hostDe(referrer) : "";
    var atual = hostDe(url);
    if (host && !interno(host) && host !== atual) {
      nova.referrer = referrer.slice(0, 500);
      tem = true;
    }
    if (tem) { nova.ts = agora; return nova; }
    if (salvo && typeof salvo.ts === "number" && agora - salvo.ts < VALIDADE) return salvo;
    return null;
  };

  function envia(dados) {
    if (!R.endpoint) return;
    var corpo = JSON.stringify(dados);
    try {
      if (typeof navigator !== "undefined" && navigator.sendBeacon) {
        if (navigator.sendBeacon(R.endpoint, corpo)) return;
      }
    } catch (e) { /* segue para o fetch */ }
    try {
      if (typeof fetch === "function") {
        fetch(R.endpoint, { method: "POST", body: corpo, keepalive: true, credentials: "omit" }).catch(function () {});
      }
    } catch (e) { /* sem rastreio, o WhatsApp abre do mesmo jeito */ }
  }

  R.aoClicar = function (ev) {
    var a = ev && ev.target && ev.target.closest ? ev.target.closest("a[data-wa]") : null;
    if (!a) return;
    try {
      var ref = R.ref();
      a.href = R.comRef(a.href, ref);
      var m = /[?&]text=([^&#]*)/.exec(a.href);
      var texto = "";
      try { texto = m ? decodeURIComponent(m[1]) : ""; } catch (e) { texto = ""; }
      var o = R.origemAtual || {};
      var dados = { ref: ref, pagina: location.pathname, texto: texto, referrer: o.referrer || "" };
      CAMPOS.forEach(function (c) { if (o[c]) dados[c] = o[c]; });
      envia(dados);
      if (R.ADS.id && typeof globalThis.gtag === "function") {
        globalThis.gtag("event", "conversion", { send_to: R.ADS.id + "/" + R.ADS.rotulo });
      }
    } catch (e) { /* nunca bloquear o clique */ }
  };

  function lerSalvo() {
    try { return JSON.parse(localStorage.getItem(CHAVE) || "null"); } catch (e) { return null; }
  }

  function gravar(o) {
    try {
      if (o) localStorage.setItem(CHAVE, JSON.stringify(o));
      else localStorage.removeItem(CHAVE);
    } catch (e) { /* aba anônima ou bloqueio: segue sem guardar */ }
  }

  R.iniciar = function () {
    var salvo = lerSalvo();
    R.origemAtual = R.capturaOrigem(location.href, document.referrer || "", Date.now(), salvo);
    if (R.origemAtual !== salvo) gravar(R.origemAtual);
    var s = document.currentScript;
    var github = /\.github\.io$/.test(location.hostname);
    if (s && s.src && !github) {
      try { R.endpoint = new URL("../clique.php", s.src).href; } catch (e) { R.endpoint = null; }
    }
    document.addEventListener("click", R.aoClicar, true);
  };

  globalThis.AnRastreio = R;
  if (typeof document !== "undefined") R.iniciar();
})();
