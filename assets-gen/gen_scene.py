"""
gen_scene.py — original CC0 pixel-art replacement assets for log8-office.

REPLACES former third-party guest sprites with original art. All art is original;
palette from pixelkit.PALETTE. Authoring philosophy (see pixelkit): draw at a small
logical resolution then upscale NEAREST so every pixel stays crisp.

Run:  python3 gen_scene.py   (cwd = assets-gen/)

Outputs (into out/), grouped A-G:
  A. office_bg.webp / office_bg_small.webp   1280x720 opaque  (160x90 logical x8)
  B. guest_anim_1..6.webp   128x64  frames 32x32  4x2=8 frames (24x24 logical x ? per frame)
  C. guest_role_1..6.png    128x64  single bust+nameplate
  D. cats-spritesheet.webp  640x640  frames 160x160  4x4=16 cats (16x16 logical x10)
  E. error-bug-spritesheet-grid.webp 1760x1980 frames 220x220 8x9=72 (22x22 logical x10)
  F. button skins (6 PNG horizontal 3-state strips)
  G. room-reference.png / .webp  1280x720 (downscaled office_bg)
"""
from __future__ import annotations

import math
import os

from PIL import Image

from pixelkit import (
    Canvas, Sheet, PALETTE, shade, outline_alpha,
    save_image, ease, wobble,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

P = PALETTE
ink = P["ink"]
clear = (0, 0, 0, 0)


# ===========================================================================
# A.  office_bg.webp / office_bg_small.webp   1280x720 opaque
#     Author at 160x90 logical, NEAREST x8 = 1280x720.
# ===========================================================================
def make_office_bg():
    LW, LH = 160, 90
    c = Canvas(LW, LH)

    # --- wall (upper ~62% of height) and floor (lower) -------------------
    wall_h = 56          # wall occupies y 0..55
    # base wall fill
    c.rect(0, 0, LW, wall_h, P["wall"])
    # vertical light gradient on the wall (lighter near top)
    for y in range(wall_h):
        t = y / wall_h
        if t < 0.4:
            c.hline(0, y, LW, shade("wall", 0.06 * (1 - t / 0.4)))
    # subtle wall paneling — faint vertical seams
    for x in range(0, LW, 20):
        c.vline(x, 2, wall_h - 4, shade("wall", -0.08))

    # --- floor -----------------------------------------------------------
    c.rect(0, wall_h, LW, LH - wall_h, P["floor"])
    # wood plank rows (horizontal bands, perspective-ish lighter toward back)
    for i, y in enumerate(range(wall_h + 1, LH, 4)):
        c.hline(0, y, LW, shade("floor", -0.10))
        c.hline(0, y + 1, LW, shade("floor", 0.05))
    # plank vertical seams (staggered)
    for row, y in enumerate(range(wall_h, LH, 4)):
        off = (row % 2) * 14
        for x in range(off, LW, 28):
            c.vline(x, y, 4, shade("floor", -0.14))

    # --- baseboard line where wall meets floor ---------------------------
    c.hline(0, wall_h - 1, LW, shade("wall_lo", -0.1))
    c.rect(0, wall_h, LW, 2, P["floor_lo"])
    c.hline(0, wall_h, LW, P["floor_hi"])

    # --- soft central rug area (keep mid/lower open but cozy) ------------
    rug_x, rug_y, rug_w, rug_h = 40, wall_h + 8, 80, 22
    c.rrect(rug_x, rug_y, rug_w, rug_h, P["rug"], r=3)
    c.rrect(rug_x + 2, rug_y + 2, rug_w - 4, rug_h - 4, P["rug_hi"], r=2)
    c.rrect(rug_x + 4, rug_y + 4, rug_w - 8, rug_h - 8, P["rug"], r=2)
    # rug accent border dashes
    for x in range(rug_x + 4, rug_x + rug_w - 4, 6):
        c.px(x, rug_y + 2, P["teal_hi"])
        c.px(x, rug_y + rug_h - 3, P["teal_hi"])

    # --- back window with sky (left of center) --------------------------
    win_x, win_y, win_w, win_h = 16, 10, 44, 30
    # frame
    c.rrect(win_x - 2, win_y - 2, win_w + 4, win_h + 4, P["wood_lo"], r=2)
    c.rect(win_x - 1, win_y - 1, win_w + 2, 1, P["wood_hi"])
    # sky gradient (top lighter)
    for y in range(win_h):
        t = y / win_h
        r = int(0x8f * (1 - t) + 0xbf * t)
        g = int(0xc8 * (1 - t) + 0xe2 * t)
        b = int(0xe8 * (1 - t) + 0xf2 * t)
        c.hline(win_x, win_y + y, win_w, (r, g, b, 255))
    # distant clouds
    for cxk, cyk, cw in [(26, 16, 8), (44, 22, 10), (34, 28, 6)]:
        c.rect(cxk, cyk, cw, 2, P["white"])
        c.rect(cxk + 1, cyk - 1, cw - 2, 1, P["white"])
    # sun glow top-right of window
    c.disc(win_x + win_w - 8, win_y + 6, 3, P["amber_hi"])
    c.disc(win_x + win_w - 8, win_y + 6, 2, P["amber"])
    # muntins (window cross bars)
    c.vline(win_x + win_w // 2, win_y, win_h, P["wood"])
    c.hline(win_x, win_y + win_h // 2, win_w, P["wood"])
    # sill
    c.rect(win_x - 3, win_y + win_h + 2, win_w + 6, 2, P["wood_hi"])
    c.rect(win_x - 3, win_y + win_h + 4, win_w + 6, 1, P["wood_lo"])

    # --- wall clock (right of center) -----------------------------------
    clk_cx, clk_cy = 118, 18
    c.disc(clk_cx, clk_cy, 7, P["wood_lo"])
    c.disc(clk_cx, clk_cy, 6, P["paper"])
    c.disc(clk_cx, clk_cy, 5, P["white"])
    # tick marks (12/3/6/9)
    c.px(clk_cx, clk_cy - 4, P["ink2"])
    c.px(clk_cx, clk_cy + 4, P["ink2"])
    c.px(clk_cx - 4, clk_cy, P["ink2"])
    c.px(clk_cx + 4, clk_cy, P["ink2"])
    # hands
    c.line(clk_cx, clk_cy, clk_cx + 2, clk_cy - 3, P["ink"])   # hour
    c.line(clk_cx, clk_cy, clk_cx, clk_cy - 4, P["ink"])       # minute
    c.px(clk_cx, clk_cy, P["rose"])

    # --- framed poster on the wall (between window & clock) -------------
    fr_x, fr_y, fr_w, fr_h = 78, 12, 22, 18
    c.rrect(fr_x, fr_y, fr_w, fr_h, P["metal"], r=1)
    c.rect(fr_x + 1, fr_y + 1, fr_w - 2, fr_h - 2, P["paper"])
    c.rect(fr_x + 2, fr_y + 2, fr_w - 4, fr_h - 4, P["glass"])
    # tiny "LOG8" star/agent motif on the poster
    pcx, pcy = fr_x + fr_w // 2, fr_y + fr_h // 2
    c.disc(pcx, pcy, 3, P["blue"])
    c.disc(pcx, pcy, 2, P["blue_hi"])
    c.px(pcx, pcy - 4, P["amber"])   # little antenna star
    c.px(pcx, pcy - 5, P["amber_hi"])

    # --- a leafy potted plant in the back corner (right) ----------------
    plx = 140
    ground = wall_h + 6
    c.rect(plx, ground, 8, 6, P["amber_lo"])      # pot
    c.rect(plx, ground, 8, 1, P["amber"])
    c.rect(plx - 1, ground, 10, 1, shade("amber", 0.2))
    c.disc(plx + 4, ground - 4, 4, P["leaf"])     # foliage
    c.disc(plx + 4, ground - 4, 3, P["leaf_hi"])
    c.vline(plx + 4, ground - 9, 5, P["leaf_lo"])
    c.px(plx + 2, ground - 6, P["leaf_hi"])
    c.px(plx + 6, ground - 5, P["leaf_hi"])

    # upscale + flatten onto an opaque background
    scaled = c.scaled(8)   # 1280x720
    bg = Image.new("RGB", (1280, 720), P["wall"][:3])
    bg.paste(scaled, (0, 0))
    final = bg.convert("RGBA")

    p1 = os.path.join(OUT, "office_bg.webp")
    p2 = os.path.join(OUT, "office_bg_small.webp")
    save_image(final, p1, 1280, 720)
    save_image(final, p2, 1280, 720)
    return final, [p1, p2]


# ===========================================================================
# B.  guest_anim_1..6.webp  128x64  frames 32x32  4x2=8 frames
#     Tiny pixel humans (~24px tall), bottom-aligned, 8-frame walk loop.
#     Author each frame at 16x16 logical, NEAREST x2 = 32x32.
# ===========================================================================
GUESTS = [
    # (skin, hair, top, bottom)
    ("skin1", "hair1", "blue",  "ink2"),
    ("skin2", "hair2", "teal",  "wood_lo"),
    ("skin3", "hair3", "amber", "blue_lo"),
    ("skin4", "hair4", "rose",  "ink2"),
    ("skin1", "hair3", "teal",  "rose"),
    ("skin2", "hair4", "amber", "teal_lo"),
]


def draw_guest_walk(spec, i, n=8):
    """One walk/idle frame. 16x16 logical, person ~12 tall bottom-aligned."""
    skin, hair, top, bottom = spec
    c = Canvas(16, 16)
    base_y = 15          # ground line
    t = i / n
    # gentle bob: up on mid-stride
    bob = -1 if i in (1, 3, 5, 7) else 0
    # leg swing phase (4 distinct positions, mirrored second half -> 8 loop)
    swing = math.sin(2 * math.pi * t)     # -1..1

    cx = 8

    # ground shadow
    c.ellipse(cx - 4, base_y, 8, 2, P["shadow"])

    by = base_y + bob

    # legs (two, swinging)
    lo = int(round(swing * 1.5))
    # left leg
    c.rect(cx - 2, by - 3, 2, 3, P[bottom])
    c.px(cx - 2 + lo, by, P[bottom])          # foot
    # right leg
    c.rect(cx + 1, by - 3, 2, 3, P[bottom])
    c.px(cx + 1 - lo, by, P[bottom])          # foot

    # torso / shirt
    ty = by - 8
    c.rrect(cx - 3, ty, 6, 6, P[top], r=1)
    c.rect(cx - 3, ty, 6, 1, shade(top, 0.2))     # shoulder highlight
    c.rect(cx - 3, ty + 5, 6, 1, shade(top, -0.18))

    # arms swinging opposite to legs
    arm = -lo
    c.rect(cx - 4, ty + 1 + max(0, arm), 1, 3, P[top])
    c.px(cx - 4, ty + 4 + max(0, arm), P[skin])    # hand
    c.rect(cx + 3, ty + 1 + max(0, -arm), 1, 3, P[top])
    c.px(cx + 3, ty + 4 + max(0, -arm), P[skin])   # hand

    # head
    hy = ty - 5
    c.rrect(cx - 2, hy, 5, 5, P[skin], r=1)
    # hair cap
    c.rect(cx - 2, hy - 1, 5, 2, P[hair])
    c.rect(cx - 2, hy + 0, 5, 1, P[hair])
    c.px(cx - 3, hy + 1, P[hair])
    c.px(cx + 3, hy + 1, P[hair])
    # eyes (look forward)
    c.px(cx - 1, hy + 2, P["ink"])
    c.px(cx + 1, hy + 2, P["ink"])
    # tiny smile
    c.px(cx, hy + 3, shade(skin, -0.25))

    return c


def make_guest_anims():
    paths = []
    for gi, spec in enumerate(GUESTS, start=1):
        sheet = Sheet(4, 2, 32, 32)
        for i in range(8):
            c = draw_guest_walk(spec, i, 8)
            scaled = c.scaled(2)               # 32x32
            scaled = outline_alpha(scaled)
            sheet.place(scaled, index=i, align="bottom", oy=-2)
        p = os.path.join(OUT, f"guest_anim_{gi}.webp")
        sheet.save(p, 128, 64)
        paths.append(p)
    return paths


# ===========================================================================
# C.  guest_role_1..6.png  128x64  single bust + nameplate
#     Head-and-shoulders bust on the left, role icon on the right.
#     Author at 32x16 logical, NEAREST x4 = 128x64.
# ===========================================================================
ROLE_ICONS = ["star", "coffee", "leaf", "chart", "gear", "heart"]


def draw_role_icon(c, kind, x, y):
    """Small 8x8-ish role icon at (x,y) top-left."""
    if kind == "star":
        c.disc(x + 4, y + 4, 3, P["amber"])
        c.disc(x + 4, y + 4, 2, P["amber_hi"])
        c.px(x + 4, y, P["amber_hi"]); c.px(x + 4, y + 8, P["amber_hi"])
        c.px(x, y + 4, P["amber_hi"]); c.px(x + 8, y + 4, P["amber_hi"])
        c.px(x + 4, y + 4, P["white"])
    elif kind == "coffee":
        c.rect(x + 1, y + 2, 6, 5, P["white"])
        c.rect(x + 1, y + 2, 6, 1, P["paper"])
        c.rect(x + 2, y + 3, 4, 3, P["amber_lo"])
        c.px(x + 7, y + 4, P["white"])           # handle
        c.px(x + 3, y, P["paper"]); c.px(x + 5, y, P["paper"])  # steam
    elif kind == "leaf":
        c.disc(x + 4, y + 4, 3, P["leaf"])
        c.disc(x + 4, y + 4, 2, P["leaf_hi"])
        c.vline(x + 4, y + 4, 4, P["leaf_lo"])
    elif kind == "chart":
        c.rect(x, y + 6, 2, 2, P["teal"])
        c.rect(x + 3, y + 3, 2, 5, P["blue"])
        c.rect(x + 6, y + 1, 2, 7, P["rose"])
    elif kind == "gear":
        c.disc(x + 4, y + 4, 3, P["metal"])
        c.disc(x + 4, y + 4, 1, P["glass"])
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            c.px(int(x + 4 + 4 * math.cos(rad)), int(y + 4 + 4 * math.sin(rad)), P["metal_hi"])
    else:  # heart
        for hx, hy in [(2, 2), (3, 2), (5, 2), (6, 2),
                       (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3),
                       (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                       (3, 5), (4, 5), (5, 5), (4, 6)]:
            c.px(x + hx, y + hy, P["rose"])


def draw_guest_bust(c, spec, x, y):
    """Head-and-shoulders bust at logical (x,y), ~12 wide x 14 tall."""
    skin, hair, top, bottom = spec
    cx = x + 6
    # shoulders / shirt
    c.rrect(cx - 5, y + 9, 11, 6, P[top], r=2)
    c.rect(cx - 5, y + 9, 11, 1, shade(top, 0.2))
    # collar
    c.rect(cx - 2, y + 9, 4, 1, P["white"])
    # neck
    c.rect(cx - 1, y + 7, 3, 2, shade(skin, -0.12))
    # head
    c.rrect(cx - 4, y, 9, 9, P[skin], r=2)
    c.rect(cx - 4, y + 1, 1, 4, shade(skin, -0.12))   # face shade left
    # hair
    c.rect(cx - 4, y - 1, 9, 3, P[hair])
    c.rect(cx - 5, y + 1, 1, 3, P[hair])
    c.rect(cx + 4, y + 1, 1, 3, P[hair])
    c.px(cx - 4, y + 1, P[hair])
    c.px(cx + 4, y + 1, P[hair])
    # eyes
    c.px(cx - 2, y + 4, P["ink"])
    c.px(cx + 2, y + 4, P["ink"])
    c.px(cx - 1, y + 4, shade(skin, 0.25))
    # cheeks
    c.px(cx - 3, y + 6, P["rose_hi"])
    c.px(cx + 3, y + 6, P["rose_hi"])
    # smile
    c.px(cx - 1, y + 7, shade(skin, -0.3))
    c.px(cx, y + 7, shade(skin, -0.3))
    c.px(cx + 1, y + 7, shade(skin, -0.3))


def make_guest_roles():
    paths = []
    for gi, spec in enumerate(GUESTS, start=1):
        c = Canvas(32, 16)
        icon = ROLE_ICONS[gi - 1]

        # nameplate panel on the right (where HTML role text would sit beside)
        c.rrect(15, 3, 15, 10, shade("paper", -0.04), r=2)
        c.rect(16, 4, 13, 1, P["white"])
        c.rect(16, 11, 13, 1, shade("paper", -0.18))
        # a divider tab in brand color
        c.rect(15, 3, 2, 10, P["blue"])
        c.rect(15, 3, 2, 1, P["blue_hi"])

        # role icon centered in the plate
        draw_role_icon(c, icon, 19, 4)

        # bust on the left
        draw_guest_bust(c, spec, 1, 1)

        scaled = c.scaled(4)               # 128x64
        scaled = outline_alpha(scaled)
        p = os.path.join(OUT, f"guest_role_{gi}.png")
        save_image(scaled, p, 128, 64)
        paths.append(p)
    return paths


# ===========================================================================
# D.  cats-spritesheet.webp  640x640  frames 160x160  4x4=16 cats
#     16 distinct cats; author at 16x16 logical, NEAREST x10 = 160x160.
# ===========================================================================
# fur palettes: (body, shade, belly/marking)  using cat1..4 + mixes
CAT_FURS = [
    ("cat1", "amber_lo", "paper"),    # 0 ginger
    ("cat2", "metal_lo", "metal_hi"), # 1 grey
    ("cat3", "paper",    "white"),    # 2 white
    ("cat4", "ink",      "metal_lo"), # 3 black
    ("cat1", "amber_lo", "ink2"),     # 4 tabby (ginger+stripes)
    ("cat2", "ink2",     "metal_hi"), # 5 grey tabby
    ("cat3", "amber_lo", "cat4"),     # 6 calico (white+ginger+black)
    ("cat4", "ink",      "white"),    # 7 tuxedo (black + white chest)
    ("cat1", "wood_lo",  "amber_hi"), # 8 warm ginger
    ("cat2", "glass",    "metal_hi"), # 9 blue-grey
    ("cat3", "rose_hi",  "white"),    # 10 white w/ pink ears
    ("cat4", "ink",      "amber"),    # 11 black w/ amber eyes accent
    ("cat1", "amber_lo", "white"),    # 12 ginger & white
    ("cat2", "metal_lo", "ink2"),     # 13 grey tabby dark
    ("cat3", "metal_hi", "amber_lo"), # 14 cream
    ("cat4", "ink2",     "teal"),     # 15 black w/ teal collar
]


def draw_cat(c, kind):
    """One cat on a 16x16 logical canvas, bottom-aligned, varied pose."""
    body, shd, mark = CAT_FURS[kind]
    pose = kind % 4   # 0 sit, 1 loaf, 2 tail-up sit, 3 looking back
    cx = 8
    gy = 15   # ground

    # ground shadow
    c.ellipse(cx - 5, gy, 11, 2, P["shadow"])

    if pose == 1:
        # loaf — low oval body, paws tucked
        c.rrect(cx - 5, gy - 6, 11, 6, P[body], r=2)
        c.rect(cx - 5, gy - 6, 11, 1, shade(body, 0.12))
        c.rect(cx - 4, gy - 1, 9, 1, P[shd])           # bottom shade
        c.rect(cx - 4, gy - 1, 9, 1, P[shd])
        # tail curled along side
        c.rect(cx + 4, gy - 4, 2, 4, P[body])
        c.px(cx + 5, gy - 5, P[body])
        head_y = gy - 11
        head_x = cx
    else:
        # sitting body (taller, narrower base)
        c.rrect(cx - 4, gy - 8, 8, 8, P[body], r=2)
        c.rect(cx - 4, gy - 8, 8, 1, shade(body, 0.12))
        c.rect(cx - 3, gy - 1, 6, 1, P[shd])
        # chest marking
        c.rect(cx - 1, gy - 5, 2, 4, P[mark])
        # front paws
        c.px(cx - 2, gy - 1, P[mark])
        c.px(cx + 1, gy - 1, P[mark])
        # tail
        if pose == 2:
            # tail up
            c.vline(cx + 4, gy - 7, 6, P[body])
            c.px(cx + 4, gy - 8, P[shd])
        else:
            # tail resting to the side / curled
            c.rect(cx + 3, gy - 2, 3, 2, P[body])
            c.px(cx + 5, gy - 3, P[body])
        head_y = gy - 14
        head_x = cx

    # head
    if pose == 3:
        head_x = cx + 2     # looking back -> head shifted
    c.rrect(head_x - 4, head_y, 8, 7, P[body], r=2)
    c.rect(head_x - 4, head_y, 8, 1, shade(body, 0.12))
    # cheeks/muzzle
    c.rect(head_x - 2, head_y + 4, 4, 2, P[mark])
    # ears
    c.px(head_x - 4, head_y - 1, P[body]); c.px(head_x - 3, head_y - 1, P[body])
    c.px(head_x + 2, head_y - 1, P[body]); c.px(head_x + 3, head_y - 1, P[body])
    c.px(head_x - 3, head_y - 2, P[body])
    c.px(head_x + 3, head_y - 2, P[body])
    # inner ear (pink)
    c.px(head_x - 3, head_y - 1, shade(mark, 0.0) if mark != "white" else P["rose_hi"])
    c.px(head_x + 3, head_y - 1, P["rose_hi"])

    if pose == 3:
        # looking back — eyes toward viewer's right, one ear edge
        c.px(head_x - 1, head_y + 2, P["teal_hi"])
        c.px(head_x + 2, head_y + 2, P["teal_hi"])
    else:
        # eyes
        c.px(head_x - 2, head_y + 2, P["teal_hi"])
        c.px(head_x + 2, head_y + 2, P["teal_hi"])
        c.px(head_x - 2, head_y + 2 - 0, P["teal_hi"])
    # nose
    c.px(head_x, head_y + 4, P["rose"])
    # whisker hint
    c.px(head_x - 4, head_y + 4, shade(body, -0.2))
    c.px(head_x + 3, head_y + 4, shade(body, -0.2))

    # tabby stripes for striped kinds (4,5,13)
    if kind in (4, 5, 13):
        for sx in range(head_x - 2, head_x + 3, 2):
            c.px(sx, head_y + 1, P[shd])
        c.hline(cx - 3, gy - 6, 6, P[shd])
        c.hline(cx - 3, gy - 4, 6, P[shd])
    # calico patch (6) — extra colored patch
    if kind == 6:
        c.rect(cx - 4, gy - 7, 3, 3, P["cat4"])
        c.px(head_x + 2, head_y + 1, P["amber_lo"])


def make_cats():
    sheet = Sheet(4, 4, 160, 160)
    for i in range(16):
        c = Canvas(16, 16)
        draw_cat(c, i)
        scaled = c.scaled(10)              # 160x160
        scaled = outline_alpha(scaled)
        sheet.place(scaled, index=i, align="center")
    p = os.path.join(OUT, "cats-spritesheet.webp")
    sheet.save(p, 640, 640)
    return p


# ===========================================================================
# E.  error-bug-spritesheet-grid.webp  1760x1980  frames 220x220  8x9=72
#     Glitchy bug creature skittering + glitch flicker. Seamless 0..71 loop.
#     Author at 22x22 logical, NEAREST x10 = 220x220.
# ===========================================================================
def draw_bug(c, i, n):
    """Glitchy red/amber bug, frame i of n. 22x22 logical."""
    t = i / n
    cx = 11
    # skitter: bug walks a small horizontal loop + bob
    walk = math.sin(2 * math.pi * t)
    bx = cx + int(round(walk * 2))
    by = 13 + int(round(abs(math.sin(2 * math.pi * t * 2)) * -1))  # tiny hop

    # ground shadow
    c.ellipse(bx - 5, 18, 11, 2, P["shadow"])

    # legs — 3 per side, scuttling (phase per leg)
    leg_phase = 2 * math.pi * t * 2
    for side in (-1, 1):
        for li in range(3):
            lp = leg_phase + li * 1.3 + (0 if side < 0 else math.pi)
            dx = side * (3 + li)
            dy = int(round(math.sin(lp) * 1.5))
            c.line(bx + side * 2, by, bx + dx, by + 3 + dy, P["red_lo"])
            c.px(bx + dx, by + 3 + dy, P["ink2"])   # foot

    # body — rounded, red with amber back segments
    c.rrect(bx - 4, by - 4, 9, 8, P["red"], r=2)
    c.rect(bx - 4, by - 4, 9, 1, P["red_lo"])
    # carapace segment lines (amber)
    c.hline(bx - 3, by - 2, 7, P["amber_lo"])
    c.hline(bx - 3, by, 7, P["amber_lo"])
    c.px(bx, by - 4, P["amber"])

    # head with big glitchy eyes
    hy = by - 6
    c.rrect(bx - 3, hy, 7, 4, P["red_lo"], r=1)
    # angry eyes (white/amber, flicker)
    eye_c = "white" if (i // 2) % 2 == 0 else "amber_hi"
    c.px(bx - 2, hy + 1, P[eye_c])
    c.px(bx + 2, hy + 1, P[eye_c])
    c.px(bx - 2, hy + 1, P[eye_c])
    # pupils
    c.px(bx - 2, hy + 2, P["ink"])
    c.px(bx + 2, hy + 2, P["ink"])

    # antennae waving
    aw = int(round(math.sin(2 * math.pi * t + 1) * 2))
    c.line(bx - 2, hy, bx - 3 + aw, hy - 4, P["red_lo"])
    c.line(bx + 2, hy, bx + 3 + aw, hy - 4, P["red_lo"])
    c.px(bx - 3 + aw, hy - 4, P["amber"])
    c.px(bx + 3 + aw, hy - 4, P["amber"])

    # --- glitch effects -------------------------------------------------
    # scanline flicker bands (every few frames, shifting)
    if i % 6 < 3:
        sy = (i * 3) % 22
        for yy in range(sy, 22, 6):
            c.hline(0, yy, 22, (P["teal_hi"][0], P["teal_hi"][1], P["teal_hi"][2], 60))
    # random-ish jitter blocks (deterministic per frame)
    seed = (i * 2654435761) & 0xFFFFFFFF
    for k in range(3):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        jx = seed % 22
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        jy = seed % 22
        if i % 4 == k % 4:
            c.rect(jx, jy, 2, 1, (P["red"][0], P["red"][1], P["red"][2], 140))

    # "!" alert pop on a beat (above bug)
    if i % 12 < 4:
        ay = hy - 8 - (i % 12)
        if ay > 1:
            c.vline(bx, ay, 2, P["amber_hi"])
            c.px(bx, ay + 3, P["amber_hi"])

    return c


def make_error_bug():
    sheet = Sheet(8, 9, 220, 220)
    N = 72
    for i in range(N):
        c = Canvas(22, 22)
        draw_bug(c, i, N)
        scaled = c.scaled(10)              # 220x220
        scaled = outline_alpha(scaled)
        sheet.place(scaled, index=i, align="center")
    p = os.path.join(OUT, "error-bug-spritesheet-grid.webp")
    sheet.save(p, 1760, 1980)
    return p


# ===========================================================================
# F.  Button skins — horizontal 3-state strips (NORMAL | PRESSED | DONE).
#     Each frame uses HORIZONTAL BANDS that survive horizontal stretch.
#     Authored 1:1 at target pixel size (16 tall) — no upscale needed.
# ===========================================================================
def _btn_frame(c, x0, fw, base, mode):
    """Draw one button state into canvas c at x-offset x0, width fw, height 16.
    mode: 0 normal, 1 pressed, 2 done."""
    h = 16
    if mode == 2:
        base = "teal"   # DONE -> green/teal tint regardless of theme
    body = P[base]
    hi = shade(base, 0.28)
    lo = shade(base, -0.28)

    if mode == 1:
        # pressed: darker, bands shifted down 1px, highlight/shade swapped
        body = shade(base, -0.12)
        hi = shade(base, -0.30)     # top now subdued
        lo = shade(base, 0.10)      # bottom slightly lighter (inset look)
        top_off = 1
    else:
        top_off = 0

    # rounded-ish ends: leave 1px in/out at extreme columns
    x = x0
    w = fw
    # mid fill
    c.rect(x, 0, w, h, body)
    # top highlight band (1-2px)
    c.rect(x, 0 + top_off, w, 2, hi)
    # bottom shadow band (1-2px)
    c.rect(x, h - 2 + (1 if mode == 1 else 0), w, 2, lo)
    # subtle 1px inner top line for sheen on normal/done
    if mode != 1:
        c.hline(x, 1, w, shade(base, 0.45))
    # rounded corner pixels (clear the very corners)
    for cx_, cy_ in [(x, 0), (x + w - 1, 0), (x, h - 1), (x + w - 1, h - 1)]:
        c.px(cx_, cy_, clear)
    # DONE: add a tiny check-tick sheen in the center-left as completion cue
    if mode == 2:
        midy = h // 2
        c.px(x + 3, midy, P["white"])
        c.px(x + 4, midy + 1, P["white"])
        c.px(x + 5, midy - 1, P["white"])
        c.px(x + 6, midy - 2, P["white"])


def make_button(fname, total_w, frame_w, base):
    """3 frames laid left-to-right in one strip (total_w x 16)."""
    c = Canvas(total_w, 16)
    for mode in range(3):
        _btn_frame(c, mode * frame_w, frame_w, base, mode)
    p = os.path.join(OUT, fname)
    # author at 1:1 — no scaling. Save PNG (transparent corners).
    save_image(c.img, p, total_w, 16)
    return p


def make_buttons():
    specs = [
        ("btn-move-house-sprite.png", 144, 48, "amber"),
        ("btn-back-home-sprite.png",  144, 48, "blue"),
        ("btn-broker-sprite.png",     144, 48, "teal"),
        ("btn-diy-sprite.png",        144, 48, "rose"),
        ("btn-open-drawer-sprite.png", 273, 91, "leaf"),
        ("btn-state-sprite.png",       78, 26, "metal"),
    ]
    paths = []
    for fname, tw, fw, base in specs:
        paths.append(make_button(fname, tw, fw, base))
    return paths


# ===========================================================================
# G.  room-reference.png / .webp  1280x720 (downscale of office_bg)
# ===========================================================================
def make_room_reference(office_img):
    # office_img already 1280x720; reference matches originals exactly.
    ref = office_img.copy()
    p_png = os.path.join(OUT, "room-reference.png")
    p_webp = os.path.join(OUT, "room-reference.webp")
    save_image(ref.convert("RGB").convert("RGBA"), p_png, 1280, 720)
    save_image(ref.convert("RGB").convert("RGBA"), p_webp, 1280, 720)
    return [p_png, p_webp]


# ===========================================================================
# VERIFY
# ===========================================================================
def verify(path, ew, eh, opaque=False):
    img = Image.open(path)
    w, h = img.size
    ok = (w == ew and h == eh)
    note = ""
    if opaque:
        rgba = img.convert("RGBA")
        # check for any fully transparent pixel
        alpha = rgba.getchannel("A")
        mn = alpha.getextrema()[0]
        if mn == 0:
            ok = False
            note = " (has transparent px!)"
        else:
            note = " (opaque)"
    status = "PASS" if ok else "FAIL"
    print(f"  {status}  {os.path.basename(path)}  {w}x{h} (exp {ew}x{eh}){note}")
    return ok


if __name__ == "__main__":
    print("Generating scene assets...")
    results = []

    # A
    office_img, bg_paths = make_office_bg()
    for p in bg_paths:
        results.append((p, 1280, 720, True))

    # B
    for p in make_guest_anims():
        results.append((p, 128, 64, False))

    # C
    for p in make_guest_roles():
        results.append((p, 128, 64, False))

    # D
    results.append((make_cats(), 640, 640, False))

    # E
    results.append((make_error_bug(), 1760, 1980, False))

    # F
    btn_sizes = {
        "btn-move-house-sprite.png": 144, "btn-back-home-sprite.png": 144,
        "btn-broker-sprite.png": 144, "btn-diy-sprite.png": 144,
        "btn-open-drawer-sprite.png": 273, "btn-state-sprite.png": 78,
    }
    for p in make_buttons():
        results.append((p, btn_sizes[os.path.basename(p)], 16, False))

    # G
    for p in make_room_reference(office_img):
        results.append((p, 1280, 720, False))

    print("\nVERIFY:")
    all_ok = True
    for p, ew, eh, opq in results:
        ok = verify(p, ew, eh, opaque=opq)
        all_ok = all_ok and ok

    print("\n" + "=" * 50)
    print("ALL PASS" if all_ok else "SOME FAILED")
    print("=" * 50)
