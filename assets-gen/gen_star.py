"""
gen_star.py — original CC0 pixel-art replacement assets for log8-office.

Produces 3 exact-size spritesheets of the "Star" mascot, a cute pixel AI agent:
  1) out/star-idle-v5.png            2048x1536  256x256 x (8x6=48)  idle breathing
  2) out/star-working-spritesheet-grid.webp 2400x1500 300x300 x(8x5=40) typing
  3) out/sync-animation-v3-grid.webp 1792x1792  256x256 x (7x7=49)  sync orbit

Authoring philosophy (see pixelkit): draw at small logical res, upscale NEAREST.
  File 1: 64x64 logical -> x4 = 256
  File 2: 60x60 logical -> x5 = 300
  File 3: 64x64 logical -> x4 = 256
"""
from __future__ import annotations

import math
import os

from PIL import Image

from pixelkit import (
    Canvas, Sheet, PALETTE, shade, outline_alpha, ease, wobble,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


# ---------------------------------------------------------------------------
# Shared mascot drawing — "Star": rounded body/head with a screen-face.
# Drawn into a 64x64 logical canvas. Params drive the breathing animation.
# ---------------------------------------------------------------------------
def draw_star(squash=0.0, bob=0.0, blink=0.0, mouth=0, arm=0.0, look=0):
    """
    squash: -1..1   negative = squashed (wider/shorter), positive = stretched
    bob:    vertical offset in logical px (negative = up)
    blink:  0..1    1 = eyes fully closed
    mouth:  0=smile, 1=open 'o', 2=flat
    arm:    -1..1   arm raise factor (for working pose)
    look:   horizontal pupil offset in px
    """
    C = Canvas(64, 64)

    # body geometry — a rounded square "head/body" combo
    base_w, base_h = 36, 34
    bw = int(round(base_w * (1 - squash * 0.10)))
    bh = int(round(base_h * (1 + squash * 0.10)))
    cx = 32
    # feet/base near vertical center-low: bottom of body ~ y=46
    body_bottom = 46 + int(round(bob))
    by = body_bottom - bh
    bx = cx - bw // 2

    # ground shadow (under feet) — subtle, scales inverse to bob
    sh_w = bw + 6 - abs(int(bob))
    sh = Canvas(64, 64)
    sh.ellipse(cx - sh_w // 2, body_bottom + 1, sh_w, 5, PALETTE["shadow"])
    C.blit(sh, 0, 0)

    # antenna + star on top
    top_y = by
    C.vline(cx, top_y - 5, 5, shade("metal_lo", 0))
    # little 4-point star bauble
    sxx, syy = cx, top_y - 7
    C.disc(sxx, syy, 2, PALETTE["amber"])
    C.px(sxx, syy - 2, PALETTE["amber_hi"])
    C.px(sxx, syy + 2, PALETTE["amber_hi"])
    C.px(sxx - 2, syy, PALETTE["amber_hi"])
    C.px(sxx + 2, syy, PALETTE["amber_hi"])
    C.px(sxx, syy, PALETTE["white"])

    # main body — rounded rect, brand blue, with rounded top corners
    C.rrect(bx, by, bw, bh, PALETTE["blue"], r=4)
    # shading: lighter top-left, darker bottom band
    C.rrect(bx, by, bw, 6, PALETTE["blue_hi"], r=2)
    C.rect(bx + 2, by + bh - 5, bw - 4, 4, PALETTE["blue_lo"])
    # teal accent stripe (belly band)
    C.rect(bx + 3, by + bh - 12, bw - 6, 3, PALETTE["teal"])
    C.rect(bx + 3, by + bh - 12, bw - 6, 1, PALETTE["teal_hi"])

    # side "ear" nubs (teal)
    C.rect(bx - 2, by + 10, 2, 6, PALETTE["teal"])
    C.rect(bx + bw, by + 10, 2, 6, PALETTE["teal"])
    C.px(bx - 2, by + 10, PALETTE["teal_hi"])
    C.px(bx + bw + 1, by + 10, PALETTE["teal_hi"])

    # screen-face panel (dark glass) inset
    fx, fy = bx + 5, by + 7
    fw_, fh_ = bw - 10, 16
    C.rrect(fx, fy, fw_, fh_, PALETTE["glass"], r=2)
    C.rect(fx + 1, fy + 1, fw_ - 2, 1, PALETTE["glasshi"])  # screen glare top

    # eyes
    eye_y = fy + 6
    elx = fx + 5
    erx = fx + fw_ - 6
    if blink > 0.5:
        # closed — a flat line
        C.hline(elx - 1, eye_y, 3, PALETTE["screen2"])
        C.hline(erx - 1, eye_y, 3, PALETTE["screen2"])
    else:
        for ex in (elx, erx):
            C.disc(ex, eye_y, 1, PALETTE["screen2"])
            C.px(ex + look, eye_y, PALETTE["teal_hi"])
            C.px(ex, eye_y - 1, PALETTE["white"])  # tiny highlight

    # mouth
    my = eye_y + 4
    if mouth == 0:  # smile
        C.px(cx - 2, my, PALETTE["screen2"])
        C.px(cx - 1, my + 1, PALETTE["screen2"])
        C.px(cx, my + 1, PALETTE["screen2"])
        C.px(cx + 1, my + 1, PALETTE["screen2"])
        C.px(cx + 2, my, PALETTE["screen2"])
    elif mouth == 1:  # open 'o'
        C.disc(cx, my + 1, 1, PALETTE["screen2"])
    else:  # flat
        C.hline(cx - 2, my + 1, 5, PALETTE["screen2"])

    # little arms on the sides
    arm_y = by + bh - 14
    al = int(round(arm * 3))
    # left arm
    C.rect(bx - 2, arm_y - al, 2, 5, PALETTE["blue_lo"])
    C.px(bx - 2, arm_y - al, PALETTE["blue"])
    # right arm
    C.rect(bx + bw, arm_y - al, 2, 5, PALETTE["blue_lo"])
    C.px(bx + bw + 1, arm_y - al, PALETTE["blue"])

    # feet
    C.rect(cx - 8, body_bottom - 2, 5, 3, PALETTE["blue_lo"])
    C.rect(cx + 3, body_bottom - 2, 5, 3, PALETTE["blue_lo"])

    return C


def finalize(canvas: Canvas) -> Image.Image:
    """Apply crisp ink outline at logical res."""
    return outline_alpha(canvas.img, PALETTE["ink"], 1)


# ---------------------------------------------------------------------------
# FILE 1 — idle breathing, 48 frames, 64x64 -> x4 = 256, grid 8x6
# ---------------------------------------------------------------------------
def gen_idle():
    sheet = Sheet(8, 6, 256, 256)
    N = 48
    # blink window: a couple frames near 1/3 and 5/6 of loop
    blink_frames = {16, 17, 40}
    for i in range(N):
        t = i / N
        # one full breathing cycle over the loop -> seamless
        breath = math.sin(2 * math.pi * t)
        squash = breath * 0.5
        bob = -abs(math.sin(math.pi * t * 2)) * 1.0  # gentle 1px bob, twice
        bob = round(math.sin(2 * math.pi * t) * 1.2)
        blink = 1.0 if i in blink_frames else 0.0
        cv = draw_star(squash=squash, bob=bob, blink=blink, mouth=0)
        frame = finalize(cv)
        sheet.place(frame.resize((256, 256), Image.NEAREST), index=i, align="center")
    sheet.save(os.path.join(OUT, "star-idle-v5.png"), 2048, 1536)


# ---------------------------------------------------------------------------
# FILE 2 — working/typing, 40 frames (anim 0..37), 60x60 -> x5 = 300, grid 8x5
# ---------------------------------------------------------------------------
def draw_working(i, n=38):
    """Seated star typing on a floating screen. Logical 60x60."""
    C = Canvas(60, 60)
    t = i / n
    cx = 30

    # ground shadow
    C.ellipse(cx - 13, 50, 26, 5, PALETTE["shadow"])

    # desk slab in front (wood)
    C.rrect(8, 44, 44, 7, PALETTE["wood"], r=2)
    C.rect(9, 44, 42, 1, PALETTE["wood_hi"])
    C.rect(9, 50, 42, 1, PALETTE["wood_lo"])

    # floating screen above desk with code glyphs / cursor
    sx, sy, sw, sh = 18, 16, 24, 16
    C.rrect(sx, sy, sw, sh, PALETTE["metal_lo"], r=2)
    C.rrect(sx + 1, sy + 1, sw - 2, sh - 2, PALETTE["screen"], r=1)
    # code lines
    glyph = (i // 3) % 4
    for li, ly in enumerate((sy + 3, sy + 6, sy + 9)):
        ll = [6, 9, 5, 7][(glyph + li) % 4]
        C.hline(sx + 3, ly, min(ll, sw - 6), PALETTE["teal_hi"])
    # blinking cursor
    if (i // 2) % 2 == 0:
        C.rect(sx + 4, sy + 12, 1, 2, PALETTE["amber"])
    # popping code-glyph above screen on some frames
    if i % 8 < 3:
        gy = sy - 2 - (i % 8)
        C.px(sx + sw - 4, gy, PALETTE["teal_hi"])
        C.px(sx + sw - 3, gy, PALETTE["teal"])

    # body (seated — slightly squat) brand blue
    bw, bh = 26, 22
    bx = cx - bw // 2
    by = 30
    C.rrect(bx, by, bw, bh, PALETTE["blue"], r=4)
    C.rrect(bx, by, bw, 5, PALETTE["blue_hi"], r=2)
    C.rect(bx + 2, by + bh - 4, bw - 4, 3, PALETTE["blue_lo"])
    C.rect(bx + 3, by + bh - 9, bw - 6, 2, PALETTE["teal"])

    # ear nubs
    C.rect(bx - 2, by + 6, 2, 5, PALETTE["teal"])
    C.rect(bx + bw, by + 6, 2, 5, PALETTE["teal"])

    # face panel
    fx, fy = bx + 4, by + 4
    fw_, fh_ = bw - 8, 11
    C.rrect(fx, fy, fw_, fh_, PALETTE["glass"], r=2)
    C.rect(fx + 1, fy + 1, fw_ - 2, 1, PALETTE["glasshi"])
    # focused eyes (look down at keyboard a touch)
    ey = fy + 5
    blink = 1.0 if (i % 19 == 5) else 0.0
    for ex in (fx + 4, fx + fw_ - 5):
        if blink > 0.5:
            C.hline(ex - 1, ey, 3, PALETTE["screen2"])
        else:
            C.disc(ex, ey, 1, PALETTE["screen2"])
            C.px(ex, ey - 1, PALETTE["white"])
    # small concentrated mouth
    C.hline(cx - 1, ey + 3, 3, PALETTE["screen2"])

    # arms tapping — alternate up/down, hands on desk edge
    phase = math.sin(2 * math.pi * t * 2)  # two taps per loop
    lh = 0 if phase > 0 else 1   # left hand down when phase<=0
    rh = 1 if phase > 0 else 0
    # left arm
    C.rect(bx + 2, by + bh - 2, 3, 4 - lh, PALETTE["blue_lo"])
    C.rect(bx + 2, 44 - 1 - lh, 4, 2, PALETTE["blue_hi"])  # hand on desk
    # right arm
    C.rect(bx + bw - 5, by + bh - 2, 3, 4 - rh, PALETTE["blue_lo"])
    C.rect(bx + bw - 6, 44 - 1 - rh, 4, 2, PALETTE["blue_hi"])

    return C


def gen_working():
    sheet = Sheet(8, 5, 300, 300)
    N = 40       # 8x5
    ANIM = 38    # app plays 0..37
    for i in range(N):
        # frames 0..37 animate; 38..39 = graceful hold copies of frame 0-ish
        src = i if i < ANIM else (ANIM - 1 - (i - ANIM) * (ANIM // 2))
        if i >= ANIM:
            src = 0 if i == ANIM else 0  # both tail frames mirror frame 0 -> seamless
        cv = draw_working(src, ANIM)
        frame = outline_alpha(cv.img, PALETTE["ink"], 1)
        sheet.place(frame.resize((300, 300), Image.NEAREST), index=i, align="center")
    sheet.save(os.path.join(OUT, "star-working-spritesheet-grid.webp"), 2400, 1500)


# ---------------------------------------------------------------------------
# FILE 3 — sync orbit, 49 frames (anim 1..47), 64x64 -> x4 = 256, grid 7x7
# ---------------------------------------------------------------------------
def draw_sync(i, n):
    """Data orbs + sync arrows orbiting a central node. Logical 64x64."""
    C = Canvas(64, 64)
    cx, cy = 32, 32
    ang = 2 * math.pi * (i / n)

    # central node — a small blue core with teal ring
    C.disc(cx, cy, 5, PALETTE["blue_lo"])
    C.disc(cx, cy, 4, PALETTE["blue"])
    C.disc(cx, cy, 2, PALETTE["blue_hi"])
    C.px(cx - 1, cy - 1, PALETTE["white"])

    # faint orbit ring (dotted, static) for readability
    R = 20
    for k in range(0, 360, 30):
        a = math.radians(k)
        ox = cx + int(round(math.cos(a) * R))
        oy = cy + int(round(math.sin(a) * R * 0.7))  # slight perspective squash
        C.px(ox, oy, shade("blue_lo", -0.2))

    # rotating sync arrows — two arc heads 180deg apart (blue + teal)
    for j, col in ((0, "blue_hi"), (1, "teal_hi")):
        a = ang + j * math.pi
        # orb position
        ox = cx + int(round(math.cos(a) * R))
        oy = cy + int(round(math.sin(a) * R * 0.7))
        base = "blue" if j == 0 else "teal"
        C.disc(ox, oy, 3, PALETTE[base])
        C.disc(ox, oy, 2, PALETTE[col])
        C.px(ox, oy, PALETTE["white"])
        # comet trail behind (3 fading dots)
        for tdot in range(1, 4):
            ta = a - tdot * 0.28
            tx = cx + int(round(math.cos(ta) * R))
            ty = cy + int(round(math.sin(ta) * R * 0.7))
            C.disc(tx, ty, max(1, 3 - tdot), shade(base, -0.05 * tdot))
        # arrow head pointing along motion (tangent)
        ta = a + math.pi / 2
        hx = ox + int(round(math.cos(ta) * 3))
        hy = oy + int(round(math.sin(ta) * 3 * 0.7))
        C.px(hx, hy, PALETTE[col])

    # tiny converging pulses toward center on a beat
    pulse = (i * 2) % n
    pr = 14 - (pulse % 14)
    if pr < 12:
        for a in (ang * 0.5, ang * 0.5 + math.pi):
            px_ = cx + int(round(math.cos(a) * pr))
            py_ = cy + int(round(math.sin(a) * pr * 0.7))
            C.px(px_, py_, PALETTE["teal_hi"])

    return C


def gen_sync():
    sheet = Sheet(7, 7, 256, 256)
    N = 49
    # app animates frames 1..47 -> make those a continuous full rotation.
    # frame 0 and 48 = bookend copies that match the loop seam.
    period = 47  # frames 1..47 inclusive = 47 distinct positions back to start
    for i in range(N):
        if i == 0:
            phase_i, phase_n = 0, period
        elif i == 48:
            phase_i, phase_n = 0, period   # mirror seam
        else:
            phase_i, phase_n = (i - 1), period
        cv = draw_sync(phase_i, phase_n)
        frame = outline_alpha(cv.img, PALETTE["ink"], 1)
        sheet.place(frame.resize((256, 256), Image.NEAREST), index=i, align="center")
    sheet.save(os.path.join(OUT, "sync-animation-v3-grid.webp"), 1792, 1792)


if __name__ == "__main__":
    gen_idle()
    gen_working()
    gen_sync()
    print("generated 3 assets into", OUT)
