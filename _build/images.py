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

SHOTS = {
  "age-breaker": [S/f"ss{i}.jpg" for i in (1,2,3,4,5,6,7,8)],
  "stock-market-dynasty": [ROOT/"_src"/"smd-a.png", ROOT/"assets"/"stock-market-dynasty.jpg"],
  "corpse-tide": [CT/"bogaz/bogaz_s4.png", CT/"halic/halic_s3.png", CT/"kara_surlari/kara_surlari_s4.png", CT/"kapalicarsi/kapalicarsi_s3.png", CT/"beyoglu/beyoglu_s3.png"],
  "a-thousand-wands": [AW/"art/concepts/caster-painted-0.52.png", AW/"art/concepts/conservatory-painted-background-v2.png", AW/"game/assets/bellroot_fen_pixel.png", AW/"art/concepts/aegis_beast_front-simple-v3.png", AW/"art/concepts/choirwarden_boss-simple-v3.png", AW/"game/assets/ember_foundry_pixel.png"],
  "meat-vector": [MV/"pressure-cover/actions/first-carry.png", MV/"pressure-cover/actions/flight-0-12.png", MV/"pressure-cover/initial/first-damage.png", MV/"pressure-cover/carry-detail/settled-carry-1.png", MV/"windows-movement-review-14/title.jpg"],
  "nightwinder": [NW/"boss-snuffer-lights-out.png", NW/"true-ending-s21-vesper-in-lucs-hands.png", NW/"sunday-s04-keep-over-not.png", NW/"the-stair-s17b-odiles-score.png", NW/"true-ending-s17-lucs-face.png"],
}
def bg_fill(im):
    if im.mode in ("RGBA","LA","P"):
        im = im.convert("RGBA"); b = Image.new("RGB", im.size, (13,13,18)); b.paste(im, mask=im.split()[-1]); return b
    return im.convert("RGB")
for slug, files in SHOTS.items():
    d = OUT/slug; d.mkdir(parents=True, exist_ok=True)
    for i, f in enumerate(files, 1):
        if not f.exists(): print("missing", f); continue
        im = bg_fill(Image.open(f))
        full = im.copy(); full.thumbnail((1600, 1000), Image.LANCZOS)
        full.save(d/f"{i}.jpg", quality=84, optimize=True, progressive=True)
        th = im.copy(); th.thumbnail((720, 450), Image.LANCZOS)
        th.save(d/f"{i}-t.jpg", quality=80, optimize=True, progressive=True)
    print(slug, len(files))
# Corpse Tide card art from a real map
im = Image.open(CT/"bogaz/bogaz_s4.png").convert("RGB"); w,h = im.size
c = im.crop((0, (h - int(w*430/920))//2, w, (h + int(w*430/920))//2)).resize((1380,645), Image.LANCZOS)
c.save(ROOT/"assets"/"corpse-tide.jpg", quality=84, optimize=True, progressive=True)
