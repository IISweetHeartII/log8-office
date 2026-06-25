"""
gen_office_bg.py — finer office room backdrop (CC0).

Re-authors office_bg at 320x180 logical (NEAREST x4 = 1280x720) so the pixels are
half the size of the old 160x90 (x8) version — much finer/denser. Walls + window +
framed art + wood floor only (furniture/cats are separate sprites composited on top).
"""
from __future__ import annotations
import os
from PIL import Image
import pixelkit as pk

OUT = os.path.join(os.path.dirname(__file__), "out")
LW, LH = 320, 180          # logical res; x4 -> 1280x720
FLOOR_Y = 104              # wall/floor boundary (logical)

def rgba(h):
    h = h.lstrip("#"); return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), 255)

WALL   = rgba("#3b4166")
WALL_D = rgba("#333a5c")
WALL_L = rgba("#454c74")
MOLD   = rgba("#2c3250")
FLOOR  = rgba("#7a5a3c")
FLOOR2 = rgba("#6d4f34")
FLOOR_L= rgba("#8a6747")
SEAM   = rgba("#5b4128")
BASE   = rgba("#2a2030")
SKY1   = rgba("#7ec8f0"); SKY2 = rgba("#bfe6fb")
WOODF  = rgba("#9a6a3e"); WOODF_D = rgba("#7c5430")


def build():
    c = pk.Canvas(LW, LH)
    # ---- wall ----
    c.rect(0, 0, LW, FLOOR_Y, WALL)
    # subtle vertical panels (calm, wide)
    for x in range(0, LW, 44):
        c.vline(x, 0, FLOOR_Y, WALL_D)
    # top molding
    c.rect(0, 0, LW, 4, MOLD)
    c.hline(0, 4, LW, WALL_L)

    # ---- window (left) ----
    wx, wy, ww, wh = 26, 22, 104, 66
    c.rect(wx - 3, wy - 3, ww + 6, wh + 6, WOODF_D)          # outer frame
    c.rect(wx - 2, wy - 2, ww + 4, wh + 4, WOODF)
    # sky gradient
    for i in range(wh):
        t = i / wh
        col = tuple(int(SKY1[k] + (SKY2[k] - SKY1[k]) * t) for k in range(3)) + (255,)
        c.hline(wx, wy + i, ww, col)
    # sun + clouds
    c.disc(wx + ww - 22, wy + 16, 7, rgba("#ffd96b"))
    c.disc(wx + ww - 22, wy + 16, 5, rgba("#ffe89a"))
    for (cxx, cyy, cw) in [(wx + 18, wy + 40, 22), (wx + 60, wy + 26, 18)]:
        c.rect(cxx, cyy, cw, 5, rgba("#f4fbff")); c.rect(cxx + 4, cyy - 3, cw - 10, 4, rgba("#f4fbff"))
    # mullions (cross bars)
    c.vline(wx + ww // 2, wy, wh, WOODF)
    c.hline(wx, wy + wh // 2, ww, WOODF)
    c.rect(wx, wy + wh, ww, 3, WOODF_D)                      # sill

    # ---- framed picture (center wall) ----
    fx, fy, fw, fh = 158, 14, 46, 40
    c.rect(fx - 2, fy - 2, fw + 4, fh + 4, rgba("#c9a36a"))  # gold frame
    c.rect(fx, fy, fw, fh, rgba("#26304f"))
    # tiny abstract art
    c.disc(fx + 14, fy + 16, 6, rgba("#7c83ff"))
    c.disc(fx + 28, fy + 22, 7, rgba("#42d6a4"))
    c.disc(fx + 22, fy + 12, 5, rgba("#ff6b8b"))

    # ---- floor ----
    c.rect(0, FLOOR_Y, LW, LH - FLOOR_Y, FLOOR)
    # baseboard
    c.rect(0, FLOOR_Y, LW, 3, BASE)
    c.hline(0, FLOOR_Y + 3, LW, FLOOR_L)
    # wood planks: long horizontal boards, thin seams, sparse staggered butt-joints
    ph = 12
    row = 0
    for y in range(FLOOR_Y + 4, LH, ph):
        shade = FLOOR if row % 2 == 0 else FLOOR2
        c.rect(0, y, LW, ph - 1, shade)
        c.hline(0, y + ph - 1, LW, SEAM)            # thin seam between boards
        off = (row % 2) * 110                         # stagger butt-joints every other row
        for x in range(off + 55, LW, 220):
            c.vline(x, y, ph - 1, SEAM)
        row += 1

    img = c.scaled(4)   # 1280x720
    return img.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    img = build()
    for name in ("office_bg.webp", "office_bg_small.webp"):
        pk.save_image(img, os.path.join(OUT, name), 1280, 720)
    for name in ("office_bg.webp", "office_bg_small.webp"):
        sz = Image.open(os.path.join(OUT, name)).size
        print(("PASS" if sz == (1280, 720) else "FAIL"), name, sz)


if __name__ == "__main__":
    main()
