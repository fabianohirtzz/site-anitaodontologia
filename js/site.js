/* Dra. Anita Nogiri | site.js (sem dependências) */
(() => {
  const doc = document.documentElement;
  doc.classList.add("js");
  const reduz = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- página ativa no menu ---------- */
  const pagina = document.body.dataset.pagina;
  document.querySelectorAll(`[data-nav="${pagina}"]`).forEach((a) => a.setAttribute("aria-current", "page"));

  /* ---------- pílula deslizante ---------- */
  const links = document.querySelector("[data-links]");
  if (links) {
    const pilula = links.querySelector(".capsula__pilula");
    const ativo = links.querySelector('[aria-current="page"]');
    const mover = (el) => {
      if (!el) { pilula.style.opacity = 0; return; }
      pilula.style.opacity = 1;
      pilula.style.width = el.offsetWidth + "px";
      pilula.style.transform = `translateX(${el.offsetLeft}px)`;
    };
    requestAnimationFrame(() => {
      pilula.style.transition = "none"; mover(ativo);
      requestAnimationFrame(() => (pilula.style.transition = ""));
    });
    links.querySelectorAll("a").forEach((a) => {
      a.addEventListener("mouseenter", () => mover(a));
      a.addEventListener("focus", () => mover(a));
    });
    links.addEventListener("mouseleave", () => mover(ativo));
    addEventListener("resize", () => mover(ativo), { passive: true });
  }

  /* ---------- scroll: cápsula compacta, dock, WhatsApp ---------- */
  const topo = document.querySelector("[data-topo]");
  const dock = document.querySelector("[data-dock]");
  const waF = document.querySelector("[data-wa-flutuante]");
  let ultimo = scrollY, pendente = false;
  const noScroll = () => {
    const y = scrollY;
    topo?.classList.toggle("is-compact", y > 120);
    if (dock) dock.classList.toggle("is-escondido", y > ultimo && y > 300);
    if (waF) waF.classList.toggle("is-expandido", y > (document.body.scrollHeight - innerHeight) * 0.4);
    ultimo = y; pendente = false;
  };
  addEventListener("scroll", () => { if (!pendente) { pendente = true; requestAnimationFrame(noScroll); } }, { passive: true });
  noScroll();

  /* ---------- overlay do menu ---------- */
  const overlay = document.querySelector("[data-overlay]");
  const abrir = document.querySelectorAll("[data-abrir-menu]");
  const fechar = overlay?.querySelector("[data-fechar-menu]");
  let origem = null;
  if (overlay) {
    overlay.querySelectorAll(".overlay__principal li, .overlay__lado > *").forEach((el, i) => {
      el.classList.add("js-stagger"); el.style.setProperty("--i", i);
    });
    const setAberto = (aberto, botao) => {
      abrir.forEach((b) => b.setAttribute("aria-expanded", String(aberto)));
      const fora = document.querySelectorAll("main, footer, [data-topo], [data-dock], [data-wa-flutuante]");
      if (aberto) {
        origem = botao || null;
        if (botao) {
          const r = botao.getBoundingClientRect();
          overlay.style.setProperty("--ox", `${r.left + r.width / 2}px`);
          overlay.style.setProperty("--oy", `${r.top + r.height / 2}px`);
        }
        overlay.hidden = false;
        requestAnimationFrame(() => overlay.classList.add("is-open"));
        fora.forEach((el) => (el.inert = true));
        doc.style.overflow = "hidden";
        setTimeout(() => fechar?.focus(), 60);
      } else {
        overlay.classList.remove("is-open");
        fora.forEach((el) => (el.inert = false));
        doc.style.overflow = "";
        setTimeout(() => { overlay.hidden = true; }, reduz ? 0 : 550);
        origem?.focus();
      }
    };
    abrir.forEach((b) => b.addEventListener("click", () => setAberto(true, b)));
    fechar?.addEventListener("click", () => setAberto(false));
    overlay.addEventListener("click", (e) => { if (e.target.closest("a")) setAberto(false); });
    addEventListener("keydown", (e) => { if (e.key === "Escape" && overlay.classList.contains("is-open")) setAberto(false); });
  }

  /* ---------- reveal + traços ---------- */
  const alvos = document.querySelectorAll("[data-reveal], .traco-anim, [data-rodape], [data-contar]");
  if ("IntersectionObserver" in window && !reduz) {
    const io = new IntersectionObserver((ents) => {
      ents.forEach((en) => {
        if (!en.isIntersecting) return;
        en.target.classList.add("is-in");
        if (en.target.dataset.contar !== undefined) contar(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
    alvos.forEach((el) => io.observe(el));
  } else {
    alvos.forEach((el) => el.classList.add("is-in"));
  }

  /* ---------- count-up ---------- */
  function contar(el) {
    const fim = parseFloat(el.dataset.contar);
    const casas = (el.dataset.contar.split(".")[1] || "").length;
    const fmt = (v) => v.toLocaleString("pt-BR", { minimumFractionDigits: casas, maximumFractionDigits: casas });
    const alvoTxt = el.querySelector("[data-valor]") || el;
    const t0 = performance.now(), dur = 1200;
    const passo = (t) => {
      const p = Math.min(1, (t - t0) / dur);
      alvoTxt.textContent = fmt(fim * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(passo);
    };
    requestAnimationFrame(passo);
  }

  /* ---------- status aberto/fechado (seg a sex, 9h às 19h, America/Sao_Paulo) ---------- */
  const partes = new Intl.DateTimeFormat("en-US", { timeZone: "America/Sao_Paulo", weekday: "short", hour: "numeric", minute: "numeric", hour12: false }).formatToParts(new Date());
  const v = Object.fromEntries(partes.map((p) => [p.type, p.value]));
  const dia = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(v.weekday);
  const min = (parseInt(v.hour, 10) % 24) * 60 + parseInt(v.minute, 10);
  const util = dia >= 1 && dia <= 5;
  const aberto = util && min >= 540 && min < 1140;
  let txt;
  if (aberto) txt = "Aberto agora · atende até as 19h";
  else if (util && min < 540) txt = "Fechado · abre hoje às 9h";
  else if (dia >= 1 && dia <= 4) txt = "Fechado · abre amanhã às 9h";
  else txt = "Fechado · abre segunda às 9h";
  document.querySelectorAll("[data-status]").forEach((s) => {
    s.classList.toggle("is-aberto", aberto);
    const t = s.querySelector("[data-status-texto]"); if (t) t.textContent = txt;
  });

  /* ---------- rodapé-cortina: só no desktop e se couber na tela ---------- */
  const rodape = document.querySelector("[data-rodape]");
  if (rodape) {
    const ajustaCortina = () => {
      const cabe = innerWidth >= 1024 && rodape.offsetHeight <= innerHeight - 24;
      doc.classList.toggle("rodape-cortina", cabe);
    };
    ajustaCortina();
    addEventListener("resize", ajustaCortina, { passive: true });
    if (waF && "IntersectionObserver" in window) {
      new IntersectionObserver(([en]) => waF.classList.toggle("is-oculto", en.isIntersecting), { threshold: 0.05 }).observe(rodape);
    }
  }

  document.querySelectorAll("[data-ano]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
