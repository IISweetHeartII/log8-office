"""
gen_decor.py — extra CC0 pixel-art office props for log8-office.
Run: python3 gen_decor.py  (cwd = assets-gen/)

All art is original; colours come from pixelkit.PALETTE so themes recolour them.
Authoring philosophy (see pixelkit): draw at a small logical resolution then
upscale NEAREST so every pixel stays crisp. Each prop gets a soft ground shadow
where it sits on the floor; wall props (clock, whiteboard) do not.

Outputs (into out/):
  wall-clock-v1.webp     96x96    (12x12 logical x8)
  bookshelf-v1.webp      160x200  (20x25 logical x8)
  floor-lamp-v1.webp     96x224   (12x28 logical x8)
  small-rug-v1.webp      192x96   (24x12 logical x8)
  whiteboard-v1.webp     200x144  (25x18 logical x8)
  water-cooler-v1.webp   96x176   (12x22 logical x8)
"""
from __future__ import annotations

import os

from PIL import Image

from pixelkit import (
    Canvas, PALETTE, shade, outline_alpha, save_image, soft_shadow,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

P = PALETTE
SCALE = 8


def verify(path, ew, eh, label):
    img = Image.open(path)
    w, h = img.size
    status = "PASS" if (w == ew and h == eh) else "FAIL"
    print(f"  {status}  {label}: {os.path.basename(path)}  ({w}x{h}, expected {ew}x{eh})")
    return status == "PASS"


def _compose(canvas: Canvas, shadow_canvas: Canvas | None, tw, th):
    """Upscale + outline the prop, optionally over a soft shadow, fit to (tw,th)."""
    art = outline_alpha(canvas.scaled(SCALE))
    if shadow_canvas is not None:
        base = shadow_canvas.scaled(SCALE)
        base.alpha_composite(art, (0, 0))
        art = base
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    out.alpha_composite(art, (0, 0))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 1. wall-clock-v1.webp  96x96  (12x12 logical)  — round wall clock
# ─────────────────────────────────────────────────────────────────────────────
def make_wall_clock():
    LW = 12
    c = Canvas(LW, LW)
    cx, cy = 6, 6
    c.disc(cx, cy, 5, P["wood_lo"])      # outer rim
    c.disc(cx, cy, 4, P["wood"])
    c.disc(cx, cy, 3, P["white"])        # dial
    # tick marks at 12 / 3 / 6 / 9
    c.px(cx, cy - 3, P["ink2"])
    c.px(cx, cy + 3, P["ink2"])
    c.px(cx - 3, cy, P["ink2"])
    c.px(cx + 3, cy, P["ink2"])
    # hands (hour short, minute long)
    c.line(cx, cy, cx + 1, cy - 2, P["ink"])
    c.line(cx, cy, cx, cy - 3, P["ink"])
    c.px(cx, cy, P["rose"])              # centre pin

    # no ground shadow (hangs on the wall)
    out = _compose(c, None, 96, 96)
    path = os.path.join(OUT, "wall-clock-v1.webp")
    save_image(out, path, 96, 96)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 2. bookshelf-v1.webp  160x200  (20x25 logical)  — wooden bookshelf w/ books
# ─────────────────────────────────────────────────────────────────────────────
def make_bookshelf():
    LW, LH = 20, 25
    c = Canvas(LW, LH)
    wood, wood_h, wood_l = P["wood"], P["wood_hi"], P["wood_lo"]

    # carcass
    c.rect(1, 1, 18, 22, wood_l)
    c.rect(2, 2, 16, 20, shade("wood", -0.25))   # interior recess
    c.rect(1, 1, 18, 1, wood_h)                  # top highlight
    # side panels
    c.rect(1, 1, 2, 22, wood)
    c.rect(17, 1, 2, 22, wood)
    # three shelves
    for sy in (7, 13, 19):
        c.rect(2, sy, 16, 1, wood_h)
        c.rect(2, sy + 1, 16, 1, wood_l)

    # books on each shelf — varied colours from the palette
    book_cols = [
        ["blue", "teal", "rose", "amber", "blue_lo"],
        ["amber", "rose", "teal_lo", "blue", "leaf"],
        ["teal", "amber_lo", "rose_hi", "blue_hi", "leaf"],
    ]
    for row, top in enumerate((2, 8, 14)):
        x = 3
        for ci, name in enumerate(book_cols[row]):
            bw = 2 + (ci % 2)            # alternate spine widths
            if x + bw > 17:
                break
            bh = 5 - (ci % 2)            # alternate heights
            by = top + (5 - bh)
            c.rect(x, by, bw, bh, P[name])
            c.rect(x, by, bw, 1, shade(name, 0.25))   # top cap
            x += bw + 1

    # base/legs
    c.rect(2, 23, 3, 2, wood_l)
    c.rect(15, 23, 3, 2, wood_l)

    sh = Canvas(LW, LH)
    sh.ellipse(2, 23, 16, 3, P["shadow"])
    out = _compose(c, sh, 160, 200)
    path = os.path.join(OUT, "bookshelf-v1.webp")
    save_image(out, path, 160, 200)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 3. floor-lamp-v1.webp  96x224  (12x28 logical)  — standing lamp w/ warm glow
# ─────────────────────────────────────────────────────────────────────────────
def make_floor_lamp():
    LW, LH = 12, 28
    c = Canvas(LW, LH)
    cx = 6
    metal, metal_h, metal_l = P["metal"], P["metal_hi"], P["metal_lo"]

    # base
    c.rect(cx - 3, 25, 7, 2, metal_l)
    c.rect(cx - 3, 25, 7, 1, metal_h)
    # pole
    c.vline(cx, 8, 18, metal)
    c.vline(cx + 1, 8, 18, metal_l)

    # shade (trapezoid) — warm amber
    c.rect(cx - 4, 4, 9, 1, P["amber_lo"])
    c.rect(cx - 3, 5, 7, 1, P["amber"])
    c.rect(cx - 2, 6, 5, 1, P["amber"])
    c.rect(cx - 4, 4, 9, 3, P["amber"])
    c.rect(cx - 4, 4, 9, 1, P["amber_hi"])    # rim highlight
    c.rect(cx - 3, 7, 7, 1, P["amber_lo"])    # underside

    # warm glow pooling under the shade
    glow = (P["amber_hi"][0], P["amber_hi"][1], P["amber_hi"][2], 70)
    c.rect(cx - 3, 8, 7, 1, glow)
    c.px(cx, 8, P["amber_hi"])

    sh = Canvas(LW, LH)
    sh.ellipse(cx - 4, 25, 9, 3, P["shadow"])
    out = _compose(c, sh, 96, 224)
    path = os.path.join(OUT, "floor-lamp-v1.webp")
    save_image(out, path, 96, 224)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 4. small-rug-v1.webp  192x96  (24x12 logical)  — accent floor rug
# ─────────────────────────────────────────────────────────────────────────────
def make_small_rug():
    LW, LH = 24, 12
    c = Canvas(LW, LH)
    # rounded rug body in two tones
    c.rrect(1, 2, 22, 8, P["rug"], r=2)
    c.rrect(3, 4, 18, 4, P["rug_hi"], r=1)
    c.rect(5, 5, 14, 2, P["rug"])
    # fringe (top & bottom edges)
    for x in range(2, 22, 2):
        c.px(x, 1, P["rug_hi"])
        c.px(x, 10, P["rug_hi"])
    # accent dashes along the inner border
    for x in range(4, 20, 3):
        c.px(x, 3, P["teal_hi"])
        c.px(x, 8, P["teal_hi"])
    # a couple of amber diamonds in the centre
    for dx in (9, 14):
        c.px(dx, 6, P["amber"])
        c.px(dx - 1, 6, P["amber_lo"])
        c.px(dx + 1, 6, P["amber_lo"])
        c.px(dx, 5, P["amber_hi"])
        c.px(dx, 7, P["amber_lo"])

    out = _compose(c, None, 192, 96)
    path = os.path.join(OUT, "small-rug-v1.webp")
    save_image(out, path, 192, 96)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 5. whiteboard-v1.webp  200x144  (25x18 logical)  — wall whiteboard w/ scribbles
# ─────────────────────────────────────────────────────────────────────────────
def make_whiteboard():
    LW, LH = 25, 18
    c = Canvas(LW, LH)
    # frame
    c.rect(0, 0, LW, 15, P["metal_lo"])
    c.rect(0, 0, LW, 1, P["metal_hi"])
    # board surface
    c.rect(1, 1, 23, 13, P["white"])
    c.rect(1, 1, 23, 1, P["paper"])

    # marker scribbles (teal headline, blue bullet lines, an amber arrow)
    c.hline(3, 3, 12, P["teal_lo"])          # title underline
    c.rect(3, 3, 8, 1, P["teal"])            # title bar
    for ly, lw in ((6, 14), (8, 11), (10, 16)):
        c.hline(4, ly, lw, P["blue_lo"])
        c.px(3, ly, P["rose"])               # bullet dot
    # a tiny chart in the corner
    c.rect(18, 8, 1, 4, P["teal"])
    c.rect(20, 6, 1, 6, P["blue"])
    c.rect(22, 9, 1, 3, P["amber"])

    # marker tray + two markers
    c.rect(2, 15, 21, 2, P["metal"])
    c.rect(2, 15, 21, 1, P["metal_hi"])
    c.rect(5, 14, 4, 1, P["rose"])           # red marker
    c.rect(11, 14, 4, 1, P["blue"])          # blue marker

    out = _compose(c, None, 200, 144)
    path = os.path.join(OUT, "whiteboard-v1.webp")
    save_image(out, path, 200, 144)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 6. water-cooler-v1.webp  96x176  (12x22 logical)  — office water cooler
# ─────────────────────────────────────────────────────────────────────────────
def make_water_cooler():
    LW, LH = 12, 22
    c = Canvas(LW, LH)
    cx = 6
    metal, metal_h, metal_l = P["metal"], P["metal_hi"], P["metal_lo"]

    # cabinet body
    c.rect(2, 8, 8, 12, metal_l)
    c.rect(2, 8, 8, 1, metal_h)
    c.rect(3, 9, 6, 9, metal)
    # spigots
    c.rect(4, 12, 1, 2, P["red_lo"])         # hot (red)
    c.rect(7, 12, 1, 2, P["blue"])           # cold (blue)
    # drip tray / grille
    c.rect(3, 16, 6, 1, metal_l)
    for gx in range(4, 9, 2):
        c.px(gx, 16, P["ink2"])
    # base
    c.rect(2, 20, 8, 2, metal_l)

    # inverted water bottle on top — translucent blue
    c.rect(3, 2, 6, 6, P["glass"])
    c.rect(4, 1, 4, 1, P["glasshi"])         # neck/cap
    water = (P["teal_hi"][0], P["teal_hi"][1], P["teal_hi"][2], 150)
    c.rect(3, 3, 6, 5, water)                # water fill
    c.rect(3, 2, 6, 1, P["glasshi"])         # surface shine
    c.px(4, 4, P["white"])                   # glint

    sh = Canvas(LW, LH)
    sh.ellipse(2, 20, 9, 3, P["shadow"])
    out = _compose(c, sh, 96, 176)
    path = os.path.join(OUT, "water-cooler-v1.webp")
    save_image(out, path, 96, 176)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("Generating decor props…")
    tasks = [
        (make_wall_clock,    "wall-clock-v1.webp",    96, 96),
        (make_bookshelf,     "bookshelf-v1.webp",     160, 200),
        (make_floor_lamp,    "floor-lamp-v1.webp",    96, 224),
        (make_small_rug,     "small-rug-v1.webp",     192, 96),
        (make_whiteboard,    "whiteboard-v1.webp",    200, 144),
        (make_water_cooler,  "water-cooler-v1.webp",  96, 176),
    ]
    all_ok = True
    for fn, fname, ew, eh in tasks:
        path = fn()
        all_ok = verify(path, ew, eh, fname) and all_ok
    print("=" * 50)
    print("ALL PASS" if all_ok else "SOME FAILED")
    print("=" * 50)
    return all_ok


if __name__ == "__main__":
    main()
