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
SCALE = 4   # author at double the old logical res, half the scale → same output dims


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
    LW = 24                                  # double old 12 (×4 → 96)
    c = Canvas(LW, LW)
    cx, cy = 12, 12
    c.disc(cx, cy, 11, P["wood_lo"])         # outer rim
    c.disc(cx, cy, 10, P["wood"])
    c.disc(cx, cy, 9, P["wood_hi"])          # bezel highlight
    c.disc(cx, cy, 8, P["white"])            # dial
    # hour ticks all around (finer)
    import math
    for h in range(12):
        a = math.radians(h * 30 - 90)
        r = 7
        long = (h % 3 == 0)
        c.px(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)),
             P["ink2"] if not long else P["ink"])
        if long:
            c.px(int(cx + (r - 1) * math.cos(a)), int(cy + (r - 1) * math.sin(a)), P["ink"])
    # hands (hour short, minute long)
    c.line(cx, cy, cx + 3, cy - 4, P["ink"])     # hour
    c.line(cx, cy, cx - 1, cy - 6, P["ink2"])    # minute
    c.disc(cx, cy, 1, P["rose"])                 # centre pin

    # no ground shadow (hangs on the wall)
    out = _compose(c, None, 96, 96)
    path = os.path.join(OUT, "wall-clock-v1.webp")
    save_image(out, path, 96, 96)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 2. bookshelf-v1.webp  160x200  (20x25 logical)  — wooden bookshelf w/ books
# ─────────────────────────────────────────────────────────────────────────────
def make_bookshelf():
    LW, LH = 40, 50                              # double old 20×25 (×4 → 160×200)
    c = Canvas(LW, LH)
    wood, wood_h, wood_l = P["wood"], P["wood_hi"], P["wood_lo"]

    # carcass
    c.rect(2, 2, 36, 44, wood_l)
    c.rect(4, 4, 32, 40, shade("wood", -0.25))   # interior recess
    c.rect(2, 2, 36, 2, wood_h)                  # top highlight
    # side panels with grain
    c.rect(2, 2, 4, 44, wood)
    c.rect(34, 2, 4, 44, wood)
    c.vline(3, 4, 40, wood_h)
    c.vline(35, 4, 40, wood_l)
    # four shelves (finer planks)
    for sy in (14, 25, 36, 44):
        c.rect(4, sy, 32, 2, wood_h)
        c.rect(4, sy + 1, 32, 1, wood_l)

    # books on each shelf — varied colours, finer spines
    book_cols = [
        ["blue", "teal", "rose", "amber", "blue_lo", "leaf", "rose_hi"],
        ["amber", "rose", "teal_lo", "blue", "leaf", "blue_hi", "teal"],
        ["teal", "amber_lo", "rose_hi", "blue_hi", "leaf", "amber", "blue_lo"],
    ]
    for row, top in enumerate((4, 16, 27)):
        x = 6
        for ci, name in enumerate(book_cols[row]):
            bw = 3 + (ci % 2)            # alternate spine widths
            if x + bw > 34:
                break
            bh = 9 - 2 * (ci % 2)        # alternate heights
            by = top + (10 - bh)
            c.rect(x, by, bw, bh, P[name])
            c.rect(x, by, bw, 1, shade(name, 0.3))    # top cap
            c.vline(x, by, bh, shade(name, 0.15))     # spine highlight
            c.px(x + bw // 2, by + 2, shade(name, -0.25))  # spine label notch
            x += bw + 1

    # a couple of items lying flat / a small plant on top shelf
    c.rect(8, 38, 10, 4, P["amber_lo"])           # stacked books lying down
    c.rect(8, 38, 10, 1, P["amber_hi"])
    c.rect(22, 39, 6, 3, P["teal_lo"])            # little pot
    c.vline(24, 36, 3, P["leaf"]); c.vline(26, 35, 4, P["leaf_hi"])

    # base/legs
    c.rect(4, 46, 6, 4, wood_l)
    c.rect(30, 46, 6, 4, wood_l)

    sh = Canvas(LW, LH)
    sh.ellipse(4, 46, 32, 6, P["shadow"])
    out = _compose(c, sh, 160, 200)
    path = os.path.join(OUT, "bookshelf-v1.webp")
    save_image(out, path, 160, 200)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 3. floor-lamp-v1.webp  96x224  (12x28 logical)  — standing lamp w/ warm glow
# ─────────────────────────────────────────────────────────────────────────────
def make_floor_lamp():
    LW, LH = 24, 56                              # double old 12×28 (×4 → 96×224)
    c = Canvas(LW, LH)
    cx = 12
    metal, metal_h, metal_l = P["metal"], P["metal_hi"], P["metal_lo"]

    # base (weighted disc)
    c.rect(cx - 6, 50, 14, 4, metal_l)
    c.rect(cx - 6, 50, 14, 1, metal_h)
    c.rect(cx - 4, 53, 10, 1, shade("metal_lo", -0.3))
    # pole (two-tone for roundness)
    c.vline(cx - 1, 16, 36, metal_h)
    c.vline(cx, 16, 36, metal)
    c.vline(cx + 1, 16, 36, metal_l)
    # small collar where pole meets shade
    c.rect(cx - 2, 16, 5, 2, metal_h)

    # shade (trapezoid) — warm amber, finer slope
    for i, w in enumerate((9, 11, 13, 14)):
        c.rect(cx - w // 2, 8 + i, w, 1, P["amber"] if i else P["amber_lo"])
    c.rect(cx - 4, 8, 9, 1, P["amber_hi"])       # rim highlight
    c.rect(cx - 7, 11, 14, 1, P["amber_hi"])     # bottom rim
    c.rect(cx - 6, 12, 12, 1, P["amber_lo"])     # underside shade
    c.vline(cx - 5, 9, 3, shade("amber", 0.2))   # lit side
    c.vline(cx + 5, 9, 3, shade("amber_lo", -0.2))  # shadow side

    # warm glow pooling under the shade
    glow = (P["amber_hi"][0], P["amber_hi"][1], P["amber_hi"][2], 70)
    c.rect(cx - 5, 13, 11, 2, glow)
    c.rect(cx - 2, 13, 5, 1, P["amber_hi"])

    sh = Canvas(LW, LH)
    sh.ellipse(cx - 8, 50, 18, 5, P["shadow"])
    out = _compose(c, sh, 96, 224)
    path = os.path.join(OUT, "floor-lamp-v1.webp")
    save_image(out, path, 96, 224)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 4. small-rug-v1.webp  192x96  (24x12 logical)  — accent floor rug
# ─────────────────────────────────────────────────────────────────────────────
def make_small_rug():
    LW, LH = 48, 24                              # double old 24×12 (×4 → 192×96)
    c = Canvas(LW, LH)
    # rounded rug body in two tones
    c.rrect(2, 4, 44, 16, P["rug"], r=4)
    c.rrect(4, 6, 40, 12, shade("rug", -0.12), r=3)   # border band
    c.rrect(7, 9, 34, 6, P["rug_hi"], r=2)            # inner field
    c.rect(10, 10, 28, 4, P["rug"])
    # fringe (top & bottom edges)
    for x in range(4, 45, 2):
        c.px(x, 2, P["rug_hi"])
        c.px(x, 21, P["rug_hi"])
    # accent dashes along the inner border
    for x in range(8, 41, 3):
        c.px(x, 6, P["teal_hi"])
        c.px(x, 17, P["teal_hi"])
    # row of amber diamonds in the centre
    for dx in range(14, 36, 7):
        c.px(dx, 12, P["amber"])
        c.px(dx - 1, 12, P["amber_lo"]); c.px(dx + 1, 12, P["amber_lo"])
        c.px(dx, 11, P["amber_hi"]); c.px(dx, 13, P["amber_lo"])
        c.px(dx - 2, 12, shade("amber_lo", -0.2)); c.px(dx + 2, 12, shade("amber_lo", -0.2))

    out = _compose(c, None, 192, 96)
    path = os.path.join(OUT, "small-rug-v1.webp")
    save_image(out, path, 192, 96)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 5. whiteboard-v1.webp  200x144  (25x18 logical)  — wall whiteboard w/ scribbles
# ─────────────────────────────────────────────────────────────────────────────
def make_whiteboard():
    LW, LH = 50, 36                              # double old 25×18 (×4 → 200×144)
    c = Canvas(LW, LH)
    # frame
    c.rect(0, 0, LW, 30, P["metal_lo"])
    c.rect(0, 0, LW, 2, P["metal_hi"])
    c.frame(1, 1, LW - 2, 28, P["metal"])        # bezel inner line
    # board surface
    c.rect(2, 2, 46, 26, P["white"])
    c.rect(2, 2, 46, 1, P["paper"])
    c.vline(2, 2, 26, P["paper"])                # faint sheen

    # marker scribbles (teal headline, blue bullet lines, a chart)
    c.rect(6, 5, 18, 2, P["teal"])               # title bar
    c.hline(6, 7, 22, P["teal_lo"])              # title underline
    for ly, lw in ((11, 28), (15, 22), (19, 32), (23, 18)):
        c.hline(9, ly, lw, P["blue_lo"])
        c.disc(6, ly, 1, P["rose"])              # bullet dot
    # a tiny bar chart in the corner
    for bx, bh, bc in ((37, 8, "teal"), (40, 12, "blue"), (43, 6, "amber"), (46, 10, "rose")):
        c.rect(bx, 24 - bh, 2, bh, P[bc])
    c.hline(36, 24, 12, P["ink2"])               # chart axis

    # marker tray + markers
    c.rect(4, 30, 42, 3, P["metal"])
    c.rect(4, 30, 42, 1, P["metal_hi"])
    c.rect(10, 28, 8, 2, P["rose"]); c.px(17, 28, P["white"])   # red marker
    c.rect(22, 28, 8, 2, P["blue"]); c.px(29, 28, P["white"])   # blue marker
    c.rect(34, 28, 6, 2, P["teal"])                             # teal marker

    out = _compose(c, None, 200, 144)
    path = os.path.join(OUT, "whiteboard-v1.webp")
    save_image(out, path, 200, 144)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 6. water-cooler-v1.webp  96x176  (12x22 logical)  — office water cooler
# ─────────────────────────────────────────────────────────────────────────────
def make_water_cooler():
    LW, LH = 24, 44                              # double old 12×22 (×4 → 96×176)
    c = Canvas(LW, LH)
    metal, metal_h, metal_l = P["metal"], P["metal_hi"], P["metal_lo"]

    # cabinet body
    c.rect(4, 16, 16, 24, metal_l)
    c.rect(4, 16, 16, 2, metal_h)               # top sheen
    c.rect(6, 18, 12, 18, metal)                # front panel
    c.vline(6, 18, 18, metal_h)                 # panel left light
    c.vline(17, 18, 18, shade("metal_lo", -0.2))# panel right shade
    c.frame(6, 18, 12, 18, shade("metal_lo", -0.15))

    # spigots with push-paddles
    c.rect(8, 24, 2, 4, P["red_lo"])            # hot (red)
    c.rect(7, 23, 4, 1, shade("red_lo", -0.2))
    c.rect(14, 24, 2, 4, P["blue"])             # cold (blue)
    c.rect(13, 23, 4, 1, shade("blue", -0.2))
    # drip tray / grille
    c.rect(6, 32, 12, 2, metal_l)
    c.rect(6, 32, 12, 1, metal_h)
    for gx in range(8, 17, 2):
        c.px(gx, 33, P["ink2"])
    # base
    c.rect(4, 40, 16, 4, metal_l)
    c.rect(5, 42, 14, 2, shade("metal_lo", -0.3))

    # inverted water bottle on top — translucent blue, rounded
    c.rrect(6, 4, 12, 12, P["glass"], r=2)
    c.rect(8, 2, 8, 2, P["glasshi"])            # neck/cap
    c.rect(9, 1, 6, 1, P["glass"])
    water = (P["teal_hi"][0], P["teal_hi"][1], P["teal_hi"][2], 150)
    c.rect(7, 6, 10, 9, water)                  # water fill
    c.rect(7, 6, 10, 1, P["glasshi"])           # surface shine
    c.vline(8, 6, 9, P["white"])                # left glint
    c.px(15, 12, shade("teal_lo", -0.1))        # bubble

    sh = Canvas(LW, LH)
    sh.ellipse(4, 40, 18, 5, P["shadow"])
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
