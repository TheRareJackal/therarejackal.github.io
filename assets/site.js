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

  // lightbox
  const shots = $$(".gallery button");
  if (shots.length) {
    const lb = document.createElement("dialog");
    lb.className = "lb";
    lb.setAttribute("aria-label", "Screenshot viewer");
    lb.innerHTML = '<button class="x" aria-label="Close">×</button><img alt=""><footer><button class="pv" aria-label="Previous screenshot">‹</button><p aria-live="polite"></p><button class="nx" aria-label="Next screenshot">›</button></footer>';
    document.body.append(lb);
    let index = 0;
    const show = next => {
      index = (next + shots.length) % shots.length;
      const {full, cap} = shots[index].dataset;
      $("img", lb).src = full;
      $("img", lb).alt = cap || "";
      $("p", lb).textContent = cap || "";
    };
    shots.forEach((shot, n) => shot.addEventListener("click", () => {
      show(n);
      lb.showModal();
      document.body.style.overflow = "hidden";
    }));
    lb.addEventListener("close", () => { document.body.style.overflow = ""; });
    $(".x", lb).onclick = () => lb.close();
    $(".pv", lb).onclick = () => show(index - 1);
    $(".nx", lb).onclick = () => show(index + 1);
    lb.addEventListener("click", e => { if (e.target === lb) lb.close(); });
    lb.addEventListener("keydown", e => {
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });
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
