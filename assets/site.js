(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // nav turns solid after scrolling
  const nav = $(".nav");
  const onScroll = () => nav && nav.classList.toggle("solid", scrollY > 30);
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // scroll reveal
  if ("IntersectionObserver" in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    $$(".rv").forEach((el, i) => { el.style.transitionDelay = (el.dataset.d || 0) + "ms"; io.observe(el); });
  } else $$(".rv").forEach(el => el.classList.add("in"));

  // filters
  const fb = $(".filters");
  if (fb) {
    let cur = "all";
    try { cur = localStorage.getItem("trj-filter") || "all"; } catch (e) {}
    const apply = () => {
      $$("button", fb).forEach(b => b.setAttribute("aria-pressed", b.dataset.k === cur));
      $$(".grid .card").forEach(c => c.classList.toggle("hide", cur !== "all" && c.dataset.status !== cur));
    };
    if (!$(`button[data-k="${cur}"]`, fb)) cur = "all";
    fb.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return;
      cur = b.dataset.k; try { localStorage.setItem("trj-filter", cur); } catch (e) {} apply(); });
    apply();
  }

  // spotlight: loop preview, click for full trailer with sound
  $$("[data-trailer]").forEach(box => {
    const v = $("video", box), btn = $(".play", box);
    btn && btn.addEventListener("click", () => {
      v.src = box.dataset.trailer; v.muted = false; v.loop = false; v.controls = true;
      btn.remove(); v.play().catch(() => {});
    });
  });

  // lightbox
  const shots = $$(".gallery button");
  if (shots.length) {
    const lb = document.createElement("div"); lb.className = "lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true");
    lb.innerHTML = '<img alt=""><p></p><button class="x" aria-label="Close">✕</button><button class="pv" aria-label="Previous">‹</button><button class="nx" aria-label="Next">›</button>';
    document.body.append(lb);
    let i = 0, last;
    const show = n => { i = (n + shots.length) % shots.length; const s = shots[i];
      $("img", lb).src = s.dataset.full; $("img", lb).alt = s.dataset.cap || ""; $("p", lb).textContent = s.dataset.cap || ""; };
    const close = () => { lb.classList.remove("open"); document.body.style.overflow = ""; last && last.focus(); };
    shots.forEach((s, n) => s.addEventListener("click", () => { last = s; show(n); lb.classList.add("open"); document.body.style.overflow = "hidden"; $(".x", lb).focus(); }));
    $(".x", lb).onclick = close; $(".pv", lb).onclick = () => show(i - 1); $(".nx", lb).onclick = () => show(i + 1);
    lb.addEventListener("click", e => { if (e.target === lb) close(); });
    addEventListener("keydown", e => { if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close(); if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
  }

  // a few slow embers drifting up the home hero
  const cv = $(".hero canvas");
  if (cv && !reduce) {
    const ctx = cv.getContext("2d"); let W, H; const P = [];
    const size = () => { const d = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * d; cv.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0); };
    const spawn = y => ({ x: Math.random() * W, y: y ?? H + 10, r: Math.random() * 1.6 + .5, s: Math.random() * .3 + .12, w: Math.random() * 6.3, a: Math.random() * .45 + .15 });
    size(); addEventListener("resize", size);
    for (let k = 0, n = Math.round(Math.min(40, W / 30)); k < n; k++) P.push(spawn(Math.random() * H));
    let run = true; new IntersectionObserver(([e]) => run = e.isIntersecting).observe(cv);
    const tick = () => {
      if (run) { ctx.clearRect(0, 0, W, H);
        for (const p of P) { p.y -= p.s; p.w += .015; p.x += Math.sin(p.w) * .25;
          if (p.y < -10) Object.assign(p, spawn());
          ctx.beginPath(); ctx.fillStyle = `rgba(255,${160 + (p.r * 25 | 0)},50,${p.a * Math.min(1, p.y / H * 1.5)})`;
          ctx.arc(p.x, p.y, p.r, 0, 7); ctx.fill(); } }
      requestAnimationFrame(tick); };
    tick();
  }

  // pass ad UTM tags through to store links (Play via install referrer, Steam via query)
  const q = new URLSearchParams(location.search), utm = {};
  for (const k of ["utm_source", "utm_medium", "utm_campaign", "utm_content"]) if (q.get(k)) utm[k] = q.get(k);
  if (Object.keys(utm).length) {
    const tag = new URLSearchParams(utm).toString();
    document.querySelectorAll('a[href*="play.google.com/store/apps/details"]').forEach(a => {
      const u = new URL(a.href); u.searchParams.set("referrer", tag); a.href = u.toString(); });
    document.querySelectorAll('a[href*="store.steampowered.com/app/"]').forEach(a => {
      const u = new URL(a.href); for (const [k, v] of Object.entries(utm)) u.searchParams.set(k, v); a.href = u.toString(); });
  }
})();
