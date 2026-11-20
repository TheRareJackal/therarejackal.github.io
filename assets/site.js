(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // filters
  const fb = $(".filters");
  if (fb) {
    let cur = "all";
    try { cur = localStorage.getItem("trj-filter") || "all"; } catch (e) {}
    const apply = () => {
      $$("button", fb).forEach(b => b.setAttribute("aria-pressed", b.dataset.k === cur));
      $$(".grid .card").forEach(c => c.classList.toggle("hide", cur !== "all" && c.dataset.status !== cur));
    };
    if (!$$("button", fb).some(b => b.dataset.k === cur)) cur = "all";
    fb.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return;
      cur = b.dataset.k; try { localStorage.setItem("trj-filter", cur); } catch (e) {} apply(); });
    apply();
  }

  // Play the trailer only when requested.
  $$(".spot .screen").forEach(box => {
    const v = $("video", box), btn = $(".play", box);
    btn && btn.addEventListener("click", () => {
      v.controls = true;
      btn.remove(); v.focus(); v.play().catch(() => {});
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
