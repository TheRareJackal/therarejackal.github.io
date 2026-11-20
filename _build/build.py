"""Builds index.html and games/<slug>/index.html from _build/games.py.
Run from anywhere:  python _build/build.py
"""
import sys
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from games import GAMES  # noqa: E402
from software import SOFTWARE
import hashlib, re

_ASSET = re.compile(r"""((?:\.\./\.\./)?assets/[A-Za-z0-9_./-]+\.(?:jpg|png|svg|css|js|mp4))(?=["')\s])""")


def bust(html):
    """Append ?v=<content hash> to local asset links so CDN caches refresh on change."""
    def sub(m):
        path = ROOT / m.group(1).replace("../../", "")
        if not path.exists():
            return m.group(1)
        return m.group(1) + "?v=" + hashlib.md5(path.read_bytes()).hexdigest()[:8]
    return _ASSET.sub(sub, html)

SITE = "https://rarejackal.com"
SOCIALS = [
    ("YouTube", "https://www.youtube.com/@RareJackal"),
    ("X", "https://x.com/TheRareJackal"),
    ("Instagram", "https://www.instagram.com/therarejackaldev/"),
    ("TikTok", "https://www.tiktok.com/@rare.jackal"),
]
STATUS = {"out": "Out now", "soon": "Coming soon", "dev": "In development"}


def head(title, desc, url, image, root):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#101114">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Rare Jackal">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@TheRareJackal">
<link rel="icon" href="{root}assets/mark.svg" type="image/svg+xml">
<link rel="icon" href="{root}assets/icon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
"""


def nav(root, home):
    g = "#games" if home else f"{root}#games"
    s = "#studio" if home else f"{root}#studio"
    return f"""<a class="skip" href="#main">Skip to content</a>
<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a class="brand" href="{root or './'}" aria-label="The Rare Jackal home"><img src="{root}assets/mark.svg" alt="">The Rare Jackal</a>
    <ul>
      <li><a href="{g}">Games</a></li>
      <li><a href="{root}#software">Software</a></li>
      <li><a href="{s}">Studio</a></li>
    </ul>
  </div>
</nav>
"""


def footer(root):
    links = "\n".join(f'      <a href="{u}">{n}</a>' for n, u in SOCIALS)
    return f"""<footer id="follow">
  <div class="wrap">
    <span>© 2026 The Rare Jackal</span>
    <nav class="foot-social" aria-label="Social">
{links}
    </nav>
  </div>
</footer>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
"""


def link_btns(g, primary=True):
    out = []
    for l in g.get("links", []):
        if l.get("url"):
            cls = "btn-primary" if primary else "btn-ghost"
            out.append(f'<a class="btn {cls}" href="{e(l["url"])}">{e(l["label"])}</a>')
            primary = False
        else:
            out.append(f'<span class="btn btn-off" aria-disabled="true">{e(l["label"])}</span>')
    return "\n".join(out)


def chips(g):
    return "".join(f"<span>{e(p)}</span>" for p in g["platforms"])


def card(g):
    return f"""      <a class="card" data-status="{g['status']}" href="games/{g['slug']}/" style="--accent:{g['accent']}">
        <div class="art"><img src="{g['card']}" alt="" loading="lazy"></div>
        <div class="body">
          <div class="top"><span class="genre">{e(g['genre'])}</span><span class="tag {g['status']}">{STATUS[g['status']]}</span></div>
          <h3>{e(g['title'])}</h3>
          <p>{e(g['blurb'])}</p>
          <div class="chips">{chips(g)}</div>
        </div>
      </a>"""


def software_listing():
    rows = []
    for app in SOFTWARE:
        link = f'<a href="{e(app["url"])}">{e(app.get("link_label", "Visit project"))}</a>' if app.get("url") else ""
        rows.append(f"""<article class="software-entry">
          <img src="{e(app['icon'])}" width="100" height="100" alt="">
          <div><p class="kind">{e(app['kind'])}</p><h3>{e(app['name'])}</h3>
          <p>{e(app['description'])}</p>{link}</div>
          <p class="availability">{e(app['platform'])}<br>{e(app['status'])}</p>
        </article>""")
    return "\n".join(rows) or "<p>Software releases will appear here.</p>"


def build_home():
    spot = next(g for g in GAMES if g.get("spotlight"))
    store_links = " ".join(
        f'<a href="{e(link["url"])}">{e(link["label"].removeprefix("Buy on ").removeprefix("Free to start on "))}</a>'
        for link in spot.get("links", []) if link.get("url")
    )
    filters = [("all", "All")] + [(k, v) for k, v in STATUS.items() if any(g["status"] == k for g in GAMES)]
    fbtns = "".join(f'<button type="button" data-k="{k}" aria-pressed="{str(k == "all").lower()}">{v}</button>' for k, v in filters)
    cards = "\n".join(card(g) for g in GAMES)
    html = head("The Rare Jackal · Independent Development Studio",
                "Games, software, and original music from The Rare Jackal, the one-person studio behind the JStack browser, Age Breaker, and Nightwinder.",
                SITE + "/", SITE + "/assets/og.png", "")
    html += '<body class="home">\n' + nav("", True) + f"""<main id="main">
<header class="masthead" id="studio">
  <div class="wrap masthead-inner">
    <div class="studio-copy">
      <h1>The Rare<br>Jackal</h1>
    <p>I’m The Rare Jackal, a solo developer making software and games.</p>
    <nav class="project-links" aria-label="Browse projects"><a href="#games">Browse games</a><a href="#software">Explore software</a></nav>
    </div>
    <div class="studio-emblem" aria-hidden="true"><img src="assets/mark.svg" alt="" width="1024" height="1024"></div>
  </div>
</header>
<section class="release wrap" aria-labelledby="release-title">
  <div class="release-art">
    <video src="{spot['trailer']}" poster="assets/games/{spot['slug']}/1.jpg" controls preload="none" playsinline aria-label="{e(spot['title'])} trailer"></video>
  </div>
  <div class="release-copy">
    <p class="kind">Featured release</p>
    <h2 id="release-title">{e(spot['title'])}<small>{e(spot['subtitle'])}</small></h2>
    <p>{e(spot.get('feature_copy', spot['pitch']))}</p>
    <div class="release-links">
      <a href="games/{spot['slug']}/">Game details</a>
      {store_links}
    </div>
  </div>
</section>
<section class="software wrap" id="software">
  <h2>Software</h2>
  {software_listing()}
</section>
<section id="games">
  <div class="wrap">
    <div class="section-head">
      <h2>Games</h2>
    </div>
    <div class="filters" role="group" aria-label="Filter games">{fbtns}</div>
    <div class="grid">
{cards}
    </div>
  </div>
</section>

</main>

""" + footer("")
    (ROOT / "index.html").write_text(bust(html), encoding="utf-8")


def build_game(g, idx):
    root = "../../"
    slug = g["slug"]
    url = f"{SITE}/games/{slug}/"
    shots = g.get("shots", 0)
    hero_img = f"{root}assets/games/{slug}/1.jpg" if shots else root + g["card"]
    desc = g["blurb"]
    full_title = g["title"] + (f": {g['subtitle']}" if g.get("subtitle") else "")
    rel = f'<span class="when">Released {e(g["released"])}</span>' if g.get("released") else ""
    btns = link_btns(g)
    trailer = ""
    if g.get("trailer"):
        trailer = f"""<section style="padding-bottom:0">
  <div class="wrap">
    <div class="section-head"><h2>Trailer</h2></div>
    <div class="trailer"><video src="{root}{g['trailer']}" poster="{root}{g['poster']}" controls playsinline preload="metadata"></video></div>
  </div>
</section>
"""
    concept = "".join(f"<p>{e(p)}</p>" for p in g["concept"])
    feats = "\n".join(
        f'      <div class="feature"><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for t, d in g["features"])
    caps = g.get("captions", [])
    gal = "\n".join(
        f'      <button type="button" data-full="{root}assets/games/{slug}/{i + 1}.jpg" data-cap="{e(caps[i] if i < len(caps) else "")}" aria-label="View screenshot: {e(caps[i] if i < len(caps) else str(i + 1))}"><picture><source media="(min-resolution: 1.5dppx), (min-width: 65rem)" srcset="{root}assets/games/{slug}/{i + 1}.jpg"><img src="{root}assets/games/{slug}/{i + 1}-t.jpg" alt="{e(caps[i] if i < len(caps) else "")}" loading="lazy"></picture><span class="caption">{e(caps[i] if i < len(caps) else "")}</span></button>'
        for i in range(shots))
    wip = "" if g["status"] == "out" else '<div class="wip">These images are from development.</div>'
    prev = GAMES[idx - 1]
    nxt = GAMES[(idx + 1) % len(GAMES)]

    html = head(f"{full_title} · The Rare Jackal", desc, url, SITE + "/" + (f"assets/games/{slug}/1.jpg" if shots else g["card"]), root)
    html += f'<body style="--accent:{g["accent"]}">\n' + nav(root, False) + f"""<main id="main">
<header class="ghero">
  <div class="wrap game-intro">
    <div class="game-summary">
    <div class="crumb"><a href="{root}#games">Games</a> / {e(g['title'])}</div>
    <h1>{e(g['title'])}</h1>
    {f'<div class="sub">{e(g["subtitle"])}</div>' if g.get('subtitle') else ''}
    <p class="tagline">{e(g['tagline'])}</p>
    <div class="meta"><span class="tag {g['status']}">{STATUS[g['status']]}</span>{rel}<span class="genre">{e(g['genre'])}</span><div class="chips">{chips(g)}</div></div>
    <div class="btns">{btns}</div>
    </div>
    <figure class="game-preview"><img src="{hero_img}" alt="{e(caps[0] if caps else g['title'])}"></figure>
  </div>
</header>

{trailer}
<section class="concept">
  <div class="wrap">
    <h2>About the game</h2>
    <div class="copy">{concept}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><h2>Features</h2></div>
    <div class="features">
{feats}
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><h2>{e(g.get('shots_label', 'Screenshots'))}</h2></div>
    <div class="gallery{' few' if shots <= 2 else ''}">
{gal}
    </div>
    {wip}
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap pager">
    <a href="{root}games/{prev['slug']}/" style="--accent:{prev['accent']}"><span>Previous</span><b>{e(prev['title'])}</b></a>
    <a class="nxt" href="{root}games/{nxt['slug']}/" style="--accent:{nxt['accent']}"><span>Next</span><b>{e(nxt['title'])}</b></a>
  </div>
</section>
</main>

""" + footer(root)
    d = ROOT / "games" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(bust(html), encoding="utf-8")


if __name__ == "__main__":
    build_home()
    for i, g in enumerate(GAMES):
        build_game(g, i)
    print("built home +", len(GAMES), "game pages")
