"""Builds index.html and games/<slug>/index.html from _build/games.py.
Run from anywhere:  python _build/build.py
"""
import sys
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from games import GAMES  # noqa: E402

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
<meta name="theme-color" content="#0b0b10">
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
"""


def nav(root, home):
    g = "#games" if home else f"{root}#games"
    s = "#studio" if home else f"{root}#studio"
    f = "#follow"
    return f"""<a class="skip" href="#main">Skip to content</a>
<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a class="brand" href="{root or './'}" aria-label="The Rare Jackal home"><img src="{root}assets/mark.svg" alt="">The Rare Jackal</a>
    <ul>
      <li><a href="{g}">Games</a></li>
      <li class="wide"><a href="{s}">Studio</a></li>
      <li><a href="{f}">Follow</a></li>
      <li class="wide"><a href="https://www.youtube.com/@RareJackal">YouTube</a></li>
    </ul>
  </div>
</nav>
"""


def follow(root):
    btns = "\n".join(f'      <a class="btn cut" href="{u}">{n}</a>' for n, u in SOCIALS)
    return f"""<div class="follow" id="follow">
  <img class="ghost" src="{root}assets/mark.svg" alt="">
  <div class="wrap">
    <div class="rv">
      <h2>Be first to the next one</h2>
      <p>New games, trailers, devlogs and playtest invites. Pick your feed.</p>
    </div>
    <div class="socials rv" data-d="120">
{btns}
    </div>
  </div>
</div>
"""


def footer(root):
    links = "\n".join(f'      <a href="{u}">{n}</a>' for n, u in SOCIALS)
    return f"""<footer>
  <div class="wrap">
    <span>© 2026 The Rare Jackal · Strategy games with teeth.</span>
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
            out.append(f'<a class="btn {cls} cut" href="{e(l["url"])}">{e(l["label"])}</a>')
            primary = False
        else:
            out.append(f'<span class="btn btn-off cut" aria-disabled="true">{e(l["label"])}</span>')
    return "\n".join(out)


def chips(g):
    return "".join(f"<span>{e(p)}</span>" for p in g["platforms"])


def card(g, i):
    rel = f'<div class="when">Released {e(g["released"])}</div>' if g.get("released") else ""
    return f"""      <a class="card cut rv" data-d="{(i % 3) * 90}" data-status="{g['status']}" href="games/{g['slug']}/" style="--accent:{g['accent']}">
        <div class="art"><img src="{g['card']}" alt="{e(g['title'])}" loading="lazy"></div>
        <div class="body">
          <span class="tag {g['status']}">{STATUS[g['status']]}</span>
          <h3>{e(g['title'])}</h3>
          <div class="genre">{e(g['genre'])}</div>
          {rel}
          <p>{e(g['blurb'])}</p>
          <div class="chips">{chips(g)}</div>
          <div class="more">Explore</div>
        </div>
      </a>"""


def build_home():
    spot = next(g for g in GAMES if g.get("spotlight"))
    n_out = sum(g["status"] == "out" for g in GAMES)
    marquee = "".join(f"<span>{e(g['title'])}</span><span>✦</span>" for g in GAMES) * 2
    filters = [("all", "All")] + [(k, v) for k, v in STATUS.items() if any(g["status"] == k for g in GAMES)]
    fbtns = "".join(f'<button type="button" data-k="{k}" aria-pressed="{str(k == "all").lower()}">{v}</button>' for k, v in filters)
    cards = "\n".join(card(g, i) for i, g in enumerate(GAMES))
    html = head("The Rare Jackal · Strategy games with teeth",
                "The Rare Jackal is a one-person game studio. Age Breaker: Six Eras is out now on Steam for PC and Mac; more games on the way.",
                SITE + "/", SITE + "/assets/og.png", "")
    html += "<body>\n" + nav("", True) + f"""<main id="main">
<header class="hero">
  <canvas aria-hidden="true"></canvas>
  <div class="wrap">
    <div>
      <div class="eyebrow">Independent game studio <b>· Est. 2026</b></div>
      <h1><span class="line"><span>Strategy</span></span><span class="line"><span>games</span></span><span class="line"><span>with teeth.</span></span></h1>
      <p class="lede">One developer making every game, from the code to the soundtrack. Original worlds, original music, no ads, ever.</p>
      <div class="stats">
        <div><b data-count="{len(GAMES)}">{len(GAMES)}</b><span>Games</span></div>
        <div><b data-count="{n_out}">{n_out}</b><span>Out now</span></div>
        <div><b data-count="{len(GAMES) - n_out}">{len(GAMES) - n_out}</b><span>On the way</span></div>
      </div>
    </div>
    <div class="mark-wrap" aria-hidden="true"><div class="halo"></div><div class="ring"></div><div class="ring r2"></div><img src="assets/mark.svg" alt=""></div>
  </div>
  <a class="scroll-cue" href="#games">Scroll</a>
</header>

<div class="marquee-clip" aria-hidden="true"><div class="marquee"><div class="track">{marquee}</div></div></div>

<section id="games">
  <div class="wrap">
    <div class="section-head rv">
      <div><div class="eyebrow">01 <b>Spotlight</b></div><h2>Latest release</h2></div>
    </div>
    <article class="spot cut rv" style="--accent:{spot['accent']}">
      <div class="screen" data-trailer="{spot['trailer']}">
        <video src="{spot['loop']}" poster="{spot['poster']}" autoplay muted loop playsinline aria-label="{e(spot['title'])} gameplay"></video>
        <button class="play" type="button" aria-label="Watch the {e(spot['title'])} trailer with sound"><i class="cut">Watch trailer</i></button>
      </div>
      <div class="body">
        <span class="tag {spot['status']}">{STATUS[spot['status']]}</span>
        <h3>{e(spot['title'])}</h3>
        <div class="genre">{e(spot.get('subtitle', ''))} · {e(spot['genre'])}</div>
        <div class="when">Released {e(spot['released'])} · {e(', '.join(spot['platforms']))}</div>
        <p>{e(spot['pitch'])}</p>
        <div class="btns">
{link_btns(spot)}
          <a class="btn btn-ghost cut" href="games/{spot['slug']}/">Learn more</a>
        </div>
      </div>
    </article>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="section-head rv">
      <div><div class="eyebrow">02 <b>The catalog</b></div><h2>Every game</h2></div>
      <p>Released, coming soon and still in the den. Tap a game to see what it's about.</p>
    </div>
    <div class="filters rv" role="group" aria-label="Filter games">{fbtns}</div>
    <div class="grid">
{cards}
      <div class="next rv"><img src="assets/mark.svg" alt=""><div><h3>Next game</h3><p>Something new is always in the den. Follow along to see it first.</p></div><a class="btn btn-ghost cut" href="#follow">Follow along</a></div>
    </div>
  </div>
</section>

<section class="studio" id="studio">
  <div class="wrap">
    <div class="rv">
      <div class="eyebrow">03 <b>The studio</b></div>
      <h2>One jackal.<br><em>No pack.</em></h2>
    </div>
    <div class="copy rv" data-d="120">
      <p><strong>The Rare Jackal is a one-person game studio.</strong> Design, code, art and music all come from the same desk, so every game ships the way it was meant to.</p>
      <p>The focus is games you can sink your teeth into: lane battles, horde defense, spellcraft, rhythm, tycoons and the occasional strange experiment. Every PC game runs on Windows and Mac.</p>
      <div class="promises">
        <div class="promise cut"><b>No ads</b><span>Not now, not later.</span></div>
        <div class="promise cut"><b>No gacha</b><span>No loot boxes or energy timers.</span></div>
        <div class="promise cut"><b>Original</b><span>Every world and soundtrack is ours.</span></div>
      </div>
    </div>
  </div>
</section>
</main>

""" + follow("") + footer("")
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def build_game(g, idx):
    root = "../../"
    slug = g["slug"]
    url = f"{SITE}/games/{slug}/"
    shots = g.get("shots", 0)
    hero_img = f"{root}assets/games/{slug}/1.jpg" if shots else root + g["card"]
    desc = f"{g['title']}: {g['blurb']}"
    full_title = g["title"] + (f": {g['subtitle']}" if g.get("subtitle") else "")
    rel = f'<span class="when">Released {e(g["released"])}</span>' if g.get("released") else ""
    btns = link_btns(g)
    trailer = ""
    if g.get("trailer"):
        trailer = f"""<section style="padding-bottom:0">
  <div class="wrap">
    <div class="section-head rv"><div><div class="eyebrow">Trailer</div><h2>See it move</h2></div></div>
    <div class="trailer cut rv"><video src="{root}{g['trailer']}" poster="{root}{g['poster']}" controls playsinline preload="metadata"></video></div>
  </div>
</section>
"""
    concept = "".join(f"<p>{e(p)}</p>" for p in g["concept"])
    feats = "\n".join(
        f'      <div class="feature cut rv" data-d="{(i % 3) * 80}"><div class="n">{i + 1:02d}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for i, (t, d) in enumerate(g["features"]))
    caps = g.get("captions", [])
    # fill the 4-column gallery: first shot is 2x2, stretch the last one over any gap
    rem = (4 + max(shots - 1, 0)) % 4
    last_span = f' style="grid-column:span {4 - rem + 1}"' if shots > 2 and rem else ""

    gal = "\n".join(
        f'      <button type="button" class="rv"{last_span if i == shots - 1 else ""} data-d="{(i % 4) * 60}" data-full="{root}assets/games/{slug}/{i + 1}.jpg" data-cap="{e(caps[i] if i < len(caps) else "")}" aria-label="View screenshot: {e(caps[i] if i < len(caps) else str(i + 1))}"><img src="{root}assets/games/{slug}/{i + 1}-t.jpg" alt="{e(caps[i] if i < len(caps) else "")}" loading="lazy"><figcaption>{e(caps[i] if i < len(caps) else "")}</figcaption></button>'
        for i in range(shots))
    wip = "" if g["status"] == "out" else '<div class="wip">Work-in-progress captures and concept art. Things will change before launch.</div>'
    prev = GAMES[idx - 1]
    nxt = GAMES[(idx + 1) % len(GAMES)]

    html = head(f"{full_title} · The Rare Jackal", desc, url, SITE + "/" + (f"assets/games/{slug}/1.jpg" if shots else g["card"]), root)
    html += f'<body style="--accent:{g["accent"]}">\n' + nav(root, False) + f"""<main id="main">
<header class="ghero">
  <div class="bg" style="background-image:url('{hero_img}')"></div>
  <div class="wrap">
    <div class="crumb"><a href="{root}#games">Games</a> / {e(g['title'])}</div>
    <h1>{e(g['title'])}</h1>
    {f'<div class="sub">{e(g["subtitle"])}</div>' if g.get('subtitle') else ''}
    <p class="tagline">{e(g['tagline'])}</p>
    <div class="meta"><span class="tag {g['status']}">{STATUS[g['status']]}</span>{rel}<span class="genre">{e(g['genre'])}</span><div class="chips">{chips(g)}</div></div>
    <div class="btns">{btns}</div>
  </div>
</header>

{trailer}
<section class="concept">
  <div class="wrap">
    <div class="rv">
      <div class="eyebrow">The concept</div>
      <blockquote style="margin-top:22px">{e(g['tagline'])}</blockquote>
    </div>
    <div class="copy rv" data-d="120">{concept}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="section-head rv"><div><div class="eyebrow">What's inside</div><h2>Features</h2></div></div>
    <div class="features">
{feats}
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="section-head rv"><div><div class="eyebrow">{e(g.get('shots_label', 'Screenshots'))}</div><h2>{'Screenshots' if g['status'] == 'out' else 'In the workshop'}</h2></div></div>
    <div class="gallery{' few' if shots <= 2 else ''}">
{gal}
    </div>
    {wip}
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap pager">
    <a class="cut rv" href="{root}games/{prev['slug']}/" style="--accent:{prev['accent']}"><span>← Previous</span><b>{e(prev['title'])}</b></a>
    <a class="cut rv nxt" href="{root}games/{nxt['slug']}/" style="--accent:{nxt['accent']}"><span>Next →</span><b>{e(nxt['title'])}</b></a>
  </div>
</section>
</main>

""" + follow(root) + footer(root)
    d = ROOT / "games" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build_home()
    for i, g in enumerate(GAMES):
        build_game(g, i)
    print("built home +", len(GAMES), "game pages")
