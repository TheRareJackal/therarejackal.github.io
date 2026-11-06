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

  // count-up stats
  $$("[data-count]").forEach(el => {
    const n = +el.dataset.count; if (reduce) { el.textContent = n; return; }
    let t0; const step = t => { t0 ??= t; const p = Math.min(1, (t - t0) / 1200);
      el.textContent = Math.round(n * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    setTimeout(() => requestAnimationFrame(step), 700);
  });

  // card tilt + glow
  if (!reduce && matchMedia("(hover: hover)").matches) {
    $$(".card").forEach(c => {
      c.addEventListener("pointermove", e => {
        const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        c.style.setProperty("--mx", x * 100 + "%"); c.style.setProperty("--my", y * 100 + "%");
        c.style.transform = `rotateX(${(0.5 - y) * 6}deg) rotateY(${(x - 0.5) * 8}deg) translateY(-4px)`;
      });
      c.addEventListener("pointerleave", () => { c.style.transform = ""; });
    });
    // mark parallax
    const mark = $(".mark-wrap img");
    if (mark) addEventListener("pointermove", e => {
      const x = e.clientX / innerWidth - 0.5, y = e.clientY / innerHeight - 0.5;
      mark.style.transform = `translate(${x * -18}px, ${y * -18}px) rotate(${x * -4}deg)`;
    });
  }

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

  // ember field on the home hero
  const cv = $(".hero canvas");
  if (cv && !reduce) {
    const ctx = cv.getContext("2d"); let W, H, P = [];
    const size = () => { const d = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * d; cv.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0); };
    const spawn = (y) => ({ x: Math.random() * W, y: y ?? H + 10, r: Math.random() * 2 + .6, s: Math.random() * .5 + .2, w: Math.random() * 2 * Math.PI, a: Math.random() * .6 + .25 });
    size(); addEventListener("resize", size);
    const N = Math.round(Math.min(90, W / 14)); for (let k = 0; k < N; k++) P.push(spawn(Math.random() * H));
    let run = true; new IntersectionObserver(([e]) => run = e.isIntersecting).observe(cv);
    const tick = () => {
      if (run) { ctx.clearRect(0, 0, W, H);
        for (const p of P) { p.y -= p.s; p.w += .02; p.x += Math.sin(p.w) * .3;
          if (p.y < -10) Object.assign(p, spawn());
          const g = p.a * Math.min(1, p.y / H * 1.4);
          ctx.beginPath(); ctx.fillStyle = `rgba(255,${150 + (p.r * 30 | 0)},40,${g})`; ctx.shadowColor = "#ffb01f"; ctx.shadowBlur = 8;
          ctx.arc(p.x, p.y, p.r, 0, 7); ctx.fill(); } }
      requestAnimationFrame(tick); };
    tick();
  }
})();
