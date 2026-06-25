"""
gen_office_bg.py — bright, finely-detailed office room backdrop (CC0).

Authored at 640x360 logical (NEAREST x2 = 1280x720) so the pixels are HALF the
size of the older 320x180 (x4) version — finer/denser, more detail. Daytime, warm
and bright (not a dark "night" room). Walls + window + framed art + wood floor only
(furniture/cats are separate sprites composited on top).

The wall/floor boundary stays at screen-y 416 (logical FLOOR_Y 208) so existing
furniture/cat placement coordinates in the frontend keep lining up.
"""
from __future__ import annotations
import os
from PIL import Image
import pixelkit as pk

OUT = os.path.join(os.path.dirname(__file__), "out")
LW, LH = 640, 360          # logical res; x2 -> 1280x720 (half-size pixels vs old)
FLOOR_Y = 208              # wall/floor boundary (logical) -> screen 416


def rgba(h):
    h = h.lstrip("#"); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


# ---- bright daytime palette (warm, cozy, NOT dark) ----
WALL    = rgba("#c8b694")   # warm light tan wall
WALL_D  = rgba("#b6a079")   # panel seam (slightly darker)
WALL_L  = rgba("#dccaa8")   # wall highlight
WALL_DOT= rgba("#d0c0a0")   # faint wallpaper texture dot
MOLD    = rgba("#efe7d2")   # crown molding (cream)
MOLD_D  = rgba("#cdbf9f")
RAIL    = rgba("#b39e7a")   # chair rail
FLOOR   = rgba("#b6884f")   # light warm wood
FLOOR2  = rgba("#a97c45")
FLOOR_L = rgba("#caa069")   # plank highlight
GRAIN   = rgba("#9a6f3c")   # wood grain
SEAM    = rgba("#7c5a30")   # plank seam
BASE    = rgba("#9a8763")   # baseboard
BASE_L  = rgba("#c7b78f")
SKY1    = rgba("#7ec8f0"); SKY2 = rgba("#d2efff")   # bright sky
SUN     = rgba("#ffe070"); SUN_H = rgba("#fff3b8")
CLOUD   = rgba("#ffffff")
WOODF   = rgba("#a9774a"); WOODF_D = rgba("#855a36")   # window/picture frame
GOLD    = rgba("#cfa863")
CANVAS  = rgba("#28304a")


def build():
    c = pk.Canvas(LW, LH)

    # ---- wall ----
    c.rect(0, 0, LW, FLOOR_Y, WALL)
    # subtle wallpaper texture: sparse dots
    for y in range(14, FLOOR_Y - 6, 16):
        for x in range((y // 16 % 2) * 8 + 6, LW, 16):
            c.px(x, y, WALL_DOT)
    # vertical wall panels (calm, wide)
    for x in range(0, LW, 84):
        c.vline(x, 0, FLOOR_Y, WALL_D)
        c.vline(x + 1, 0, FLOOR_Y, WALL_L)
    # crown molding (top)
    c.rect(0, 0, LW, 7, MOLD)
    c.hline(0, 7, LW, MOLD_D)
    c.hline(0, 8, LW, WALL_L)
    # chair rail
    c.rect(0, FLOOR_Y - 40, LW, 3, RAIL)
    c.hline(0, FLOOR_Y - 37, LW, WALL_L)

    # ---- window (left), bright daytime ----
    wx, wy, ww, wh = 52, 40, 212, 132
    c.rect(wx - 6, wy - 6, ww + 12, wh + 12, WOODF_D)        # outer frame
    c.rect(wx - 4, wy - 4, ww + 8, wh + 8, WOODF)
    # sky gradient
    for i in range(wh):
        t = i / wh
        col = tuple(int(SKY1[k] + (SKY2[k] - SKY1[k]) * t) for k in range(3)) + (255,)
        c.hline(wx, wy + i, ww, col)
    # sun + glow
    sx, sy = wx + ww - 40, wy + 30
    c.disc(sx, sy, 15, SUN)
    c.disc(sx, sy, 10, SUN_H)
    # clouds
    for (cxx, cyy, cw) in [(wx + 30, wy + 78, 44), (wx + 110, wy + 52, 36), (wx + 60, wy + 104, 30)]:
        c.rect(cxx, cyy, cw, 9, CLOUD)
        c.rect(cxx + 8, cyy - 6, cw - 18, 7, CLOUD)
    # mullions (cross bars) — finer grid
    c.vline(wx + ww // 2, wy, wh, WOODF)
    c.hline(wx, wy + wh // 2, ww, WOODF)
    c.vline(wx + ww // 4, wy, wh, WOODF_D)
    c.vline(wx + 3 * ww // 4, wy, wh, WOODF_D)
    c.rect(wx - 4, wy + wh, ww + 8, 6, WOODF_D)             # sill

    # ---- framed picture (center wall) ----
    fx, fy, fw, fh = 320, 28, 92, 80
    c.rect(fx - 4, fy - 4, fw + 8, fh + 8, GOLD)            # frame
    c.rect(fx - 2, fy - 2, fw + 4, fh + 4, WOODF_D)
    c.rect(fx, fy, fw, fh, CANVAS)
    c.disc(fx + 28, fy + 32, 12, rgba("#7c83ff"))
    c.disc(fx + 56, fy + 44, 14, rgba("#42d6a4"))
    c.disc(fx + 44, fy + 24, 10, rgba("#ff6b8b"))

    # ---- floor ----
    c.rect(0, FLOOR_Y, LW, LH - FLOOR_Y, FLOOR)
    # baseboard
    c.rect(0, FLOOR_Y, LW, 5, BASE)
    c.hline(0, FLOOR_Y + 5, LW, BASE_L)
    # wood planks: finer boards, grain dashes, thin seams, staggered butt-joints
    ph = 16
    row = 0
    for y in range(FLOOR_Y + 6, LH, ph):
        shade = FLOOR if row % 2 == 0 else FLOOR2
        c.rect(0, y, LW, ph - 1, shade)
        c.hline(0, y, LW, FLOOR_L)                       # top highlight of each board
        c.hline(0, y + ph - 1, LW, SEAM)                 # seam between boards
        # grain: short horizontal dashes scattered along the board
        for gx in range((row * 37) % 24, LW, 48):
            c.hline(gx, y + 5, 14, GRAIN)
            c.hline(gx + 24, y + 10, 9, GRAIN)
        # staggered vertical butt-joints
        off = (row % 2) * 160
        for x in range(off + 80, LW, 320):
            c.vline(x, y, ph - 1, SEAM)
        row += 1

    img = c.scaled(2)   # 1280x720
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
