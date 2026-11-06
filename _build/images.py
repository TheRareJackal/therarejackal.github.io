"""Build gallery images for game pages. Run: python _build/images.py"""
from PIL import Image
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "games"
S = ROOT / "_src" / "steam"
NW = Path("C:/Users/SLI/Documents/NightWinder/docs/v2/screens")
MV = Path("D:/meat-vector/audits/2026-10-18")
AW = Path("D:/a-thousand-wands")
CT = Path("D:/Games/Corpse Tide/maps")

CAP = Path("D:/site-capture/shots")
SMD = Path("D:/site-capture/stock-market-dynasty/game/evidence")
STUDIO = (52, 304, 2552, 1768)   # Roblox Studio play viewport (crops editor chrome)
# Real current gameplay only. Entries are a path or (path, crop box).
SHOTS = {
  "age-breaker": [S/f"ss{i}.jpg" for i in (1,2,3,4,5,6,7,8)],
  "stock-market-dynasty": [(SMD/"full-game-audit/live-v70-terminal.png", (0, 64, 2604, 1504)),
                           (SMD/"full-game-audit/desktop-property-final.png", STUDIO),
                           (SMD/"full-game-audit/desktop-trade-final.png", STUDIO),
                           (SMD/"full-game-audit/final-Bots.png", STUDIO),
                           ROOT/"_src"/"smd-a.png"],
  "corpse-tide": [CAP/"ct/z4.png", CAP/"ct/b10.png", CAP/"ct/z3.png", CAP/"ct/keep-plan.png", CAP/"ct/keep-briefing.png", CAP/"ct/b07.png"],
  "a-thousand-wands": [CAP/"aw/s11.png", CAP/"aw/s04.png", CAP/"aw/s09.png", CAP/"aw/s13.png", CAP/"aw/01.png", CAP/"wands/00-fresh-menu-tree.png"],
  "meat-vector": [CAP/"mv/g01.png", CAP/"mv/g04.png", CAP/"mv/g05.png", CAP/"mv/02.png", CAP/"mv/g02.png", CAP/"mv/keep-starter.png"],
  "nightwinder": [CAP/"nw/w5_6.png", CAP/"nw/w3_2.png", CAP/"nw/w5_4.png", CAP/"nw/w4_6.png", CAP/"nw/w4_end.png", CAP/"nw/keep-upgrade.png", CAP/"nw/01.png"],
}
def bg_fill(im):
    if im.mode in ("RGBA","LA","P"):
        im = im.convert("RGBA"); b = Image.new("RGB", im.size, (13,13,18)); b.paste(im, mask=im.split()[-1]); return b
    return im.convert("RGB")
for slug, files in SHOTS.items():
    d = OUT/slug; d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.jpg"): old.unlink()
    for i, f in enumerate(files, 1):
        box = None
        if isinstance(f, tuple): f, box = f
        if not f.exists(): print("missing", f); continue
        im = bg_fill(Image.open(f))
        if box: im = im.crop(box)
        full = im.copy(); full.thumbnail((1600, 1000), Image.LANCZOS)
        full.save(d/f"{i}.jpg", quality=84, optimize=True, progressive=True)
        th = im.copy(); th.thumbnail((720, 450), Image.LANCZOS)
        th.save(d/f"{i}-t.jpg", quality=80, optimize=True, progressive=True)
    print(slug, len(files))
# Card art: centre crop of each game's first gallery shot (except Age Breaker's key art)
for slug in ["stock-market-dynasty", "corpse-tide", "a-thousand-wands", "meat-vector", "nightwinder"]:
    im = Image.open(OUT/slug/"1.jpg").convert("RGB"); w, h = im.size; ch = int(w*430/920)
    top = max(0, (h - ch)//2)
    im.crop((0, top, w, min(h, top + ch))).resize((1380, 645), Image.LANCZOS).save(ROOT/"assets"/f"{slug}.jpg", quality=84, optimize=True, progressive=True)
