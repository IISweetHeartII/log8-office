"""
gen_furniture.py — CC0 pixel-art assets for log8-office.
Run: python3 gen_furniture.py  (cwd = assets-gen/)
All art is original; palette from pixelkit.PALETTE.
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter
from pixelkit import (
    Canvas, Sheet, PALETTE, shade, outline_alpha,
    save_canvas, save_image, soft_shadow, ease, wobble
)

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)

P = PALETTE
ink   = P["ink"]
clear = (0, 0, 0, 0)


# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────
def verify(path, expected_w, expected_h, label):
    from PIL import Image as Im
    img = Im.open(path)
    w, h = img.size
    status = "PASS" if (w == expected_w and h == expected_h) else "FAIL"
    print(f"  {status}  {label}: {path}  ({w}x{h}, expected {expected_w}x{expected_h})")
    return status == "PASS"


def blurred_shadow(img_size, ex, ey, color=None, blur=4):
    """Soft gaussian-blurred elliptical shadow."""
    if color is None:
        color = P["shadow"]
    base = Image.new("RGBA", img_size, (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    cx, cy = img_size[0] // 2, img_size[1] // 2
    d.ellipse([cx - ex, cy - ey, cx + ex, cy + ey], fill=color)
    return base.filter(ImageFilter.GaussianBlur(radius=blur))


# ─────────────────────────────────────────────────────────────────────────────
# 1. sofa-idle-v3.png  256×256  single image
# ─────────────────────────────────────────────────────────────────────────────
def make_sofa():
    # Author at 64×64 logical (double old 32×32) → ×4 = 256×256.
    LW, LH = 64, 64
    c = Canvas(LW, LH)

    sofa_color   = P["blue"]
    sofa_hi      = P["blue_hi"]
    sofa_lo      = P["blue_lo"]
    cushion      = shade("blue", 0.15)
    cushion_hi   = shade("blue", 0.3)
    leg          = P["wood_lo"]
    piping       = P["ink2"]

    # legs
    c.rect(8, 56, 4, 6, leg)
    c.rect(8, 56, 2, 6, P["wood"])
    c.rect(52, 56, 4, 6, leg)
    c.rect(52, 56, 2, 6, P["wood"])

    # sofa base / seat body
    c.rect(6, 44, 52, 16, sofa_lo)
    c.rect(6, 44, 52, 2, piping)            # top edge piping
    c.rect(6, 58, 52, 2, shade("blue_lo", -0.25))   # base shadow

    # back cushion strip
    c.rect(6, 28, 52, 18, sofa_color)
    c.rect(6, 28, 52, 2, sofa_hi)           # highlight top
    # tufting seams on the backrest (finer detail)
    for sx in (18, 32, 46):
        c.vline(sx, 30, 14, shade("blue_lo", -0.2))
        c.px(sx, 36, shade("blue", 0.2))    # tuft button glint

    # armrests with rounded top
    for ax in (2, 56):
        c.rect(ax, 30, 6, 28, sofa_lo)
        c.rect(ax, 30, 6, 2, sofa_hi)
        c.rect(ax, 31, 2, 26, shade("blue", 0.1))   # inner highlight
    c.rect(2, 30, 6, 1, shade("blue_hi", 0.2))
    c.rect(56, 30, 6, 1, shade("blue_hi", 0.2))

    # seat cushions (two) with fabric fold shading
    for cx0 in (8, 33):
        c.rect(cx0, 46, 22, 12, cushion)
        c.rect(cx0, 46, 22, 2, cushion_hi)          # cushion top sheen
        c.rect(cx0, 56, 22, 1, shade("blue_lo", -0.15))  # fold shadow
        c.px(cx0 + 4, 49, cushion_hi)
    c.vline(31, 46, 12, piping)             # seam between cushions
    c.vline(32, 46, 12, shade("blue_lo", -0.2))

    # small back pillow left (amber) with corner seams
    c.rrect(10, 32, 16, 12, P["amber"], r=2)
    c.rect(10, 32, 16, 2, P["amber_hi"])
    c.frame(11, 33, 14, 10, shade("amber_lo", -0.15))
    c.px(18, 38, P["amber_hi"])

    # small back pillow right (rose)
    c.rrect(38, 32, 16, 12, P["rose"], r=2)
    c.rect(38, 32, 16, 2, P["rose_hi"])
    c.frame(39, 33, 14, 10, shade("rose", -0.2))
    c.px(46, 38, P["rose_hi"])

    scaled = c.scaled(4)
    scaled = outline_alpha(scaled)

    path = os.path.join(OUT, "sofa-idle-v3.png")
    save_image(scaled, path, 256, 256)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 2. sofa-shadow-v1.png  256×256  single soft ellipse
# ─────────────────────────────────────────────────────────────────────────────
def make_sofa_shadow():
    img = blurred_shadow((256, 256), 90, 18, blur=10)
    # shift shadow slightly to bottom center
    final = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    final.alpha_composite(img, (0, 30))
    path = os.path.join(OUT, "sofa-shadow-v1.png")
    save_image(final, path, 256, 256)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 3. desk-v3.webp  276×214  WEBP lossless single
# ─────────────────────────────────────────────────────────────────────────────
def make_desk():
    # Author at 92×72 logical (double old 46×36) → ×3 = 276×216, trim to 276×214.
    LW, LH = 92, 72
    c = Canvas(LW, LH)

    wood   = P["wood"]
    wood_h = P["wood_hi"]
    wood_l = P["wood_lo"]
    leg    = P["wood_lo"]

    # legs (front) — with a highlight edge
    c.rect(4, 48, 6, 24, leg)
    c.rect(4, 48, 2, 24, wood)
    c.rect(82, 48, 6, 24, leg)
    c.rect(82, 48, 2, 24, wood)
    # back legs (shorter visible)
    c.rect(12, 44, 4, 10, shade("wood_lo", -0.15))
    c.rect(76, 44, 4, 10, shade("wood_lo", -0.15))

    # desk surface (flat top slab) with finer grain
    c.rect(2, 36, 88, 14, wood)
    c.hline(2, 36, 88, wood_h)            # top highlight
    c.hline(2, 37, 88, shade("wood_hi", 0.15))
    c.rect(2, 48, 88, 2, wood_l)          # front lip / edge shadow
    # subtle wood grain streaks
    for gy, gx0, gx1 in ((40, 6, 40), (43, 20, 60), (46, 50, 84), (41, 60, 86)):
        c.hline(gx0, gy, gx1 - gx0, shade("wood", -0.12))
    c.hline(8, 38, 70, shade("wood", 0.08))

    # under-desk shelf
    c.rect(10, 56, 72, 6, wood_l)
    c.hline(10, 56, 72, wood)
    c.rect(14, 58, 64, 2, shade("wood_lo", -0.2))   # shelf recess

    # monitor (on desk) — finer bezel + screen
    mb_x, mb_y, mb_w, mb_h = 34, 14, 28, 24
    c.rect(mb_x, mb_y, mb_w, mb_h, P["metal_lo"])
    c.rect(mb_x, mb_y, mb_w, 1, P["metal_hi"])           # bezel top hi
    c.rect(mb_x, mb_y + mb_h - 1, mb_w, 1, P["glass"])   # bezel bottom
    # screen
    c.rect(mb_x + 2, mb_y + 2, mb_w - 4, mb_h - 5, P["screen"])
    c.rect(mb_x + 2, mb_y + 2, mb_w - 4, 1, P["screen2"])   # screen top glow
    # finer UI on screen: code-ish lines + teal accent rows
    for i, ry in enumerate(range(mb_y + 5, mb_y + mb_h - 5, 3)):
        lw = (mb_w - 10) if i % 2 == 0 else (mb_w - 16)
        c.hline(mb_x + 4, ry, lw, P["teal_lo"] if i % 3 else P["teal"])
        c.px(mb_x + 4 + lw, ry, P["amber"])
    c.rect(mb_x + 4, mb_y + 4, 6, 2, P["teal_hi"])        # window title bar
    # monitor stand
    c.rect(mb_x + mb_w // 2 - 2, mb_y + mb_h, 4, 2, P["metal"])
    c.rect(mb_x + mb_w // 2 - 6, mb_y + mb_h + 2, 12, 2, P["metal_lo"])

    # keyboard (flat on desk)
    c.rect(20, 40, 32, 6, P["metal"])
    c.rect(20, 40, 32, 1, P["metal_hi"])
    c.rect(20, 45, 32, 1, shade("metal_lo", -0.2))
    # key rows (finer dots)
    for ky in (42, 44):
        for kx in range(22, 51, 2):
            c.px(kx, ky, P["metal_hi"])

    # mouse beside keyboard
    c.rrect(54, 42, 5, 4, P["metal"], r=1)
    c.px(56, 43, P["metal_hi"])

    # mug (right side) — finer body + handle + steam
    c.rect(62, 32, 9, 10, P["amber"])
    c.rect(62, 32, 9, 1, P["amber_hi"])
    c.rect(63, 33, 7, 6, P["amber_lo"])     # mug inside / coffee
    c.rect(63, 33, 7, 1, shade("amber_lo", -0.25))
    c.frame(71, 34, 3, 5, P["amber"])       # handle
    # steam wisps
    c.px(64, 29, shade("white", -0.1))
    c.px(66, 27, shade("white", -0.05))
    c.px(67, 30, shade("white", -0.15))

    # small plant / pencil cup top-left — finer pot + leaves
    c.rect(6, 28, 9, 8, P["teal_lo"])
    c.rect(6, 28, 9, 1, P["teal"])
    c.rect(6, 35, 9, 1, shade("teal_lo", -0.25))
    c.vline(8, 22, 7, P["leaf"])
    c.vline(10, 20, 9, P["leaf_hi"])
    c.vline(12, 23, 6, P["leaf_lo"])
    c.px(8, 22, P["leaf_hi"]); c.px(10, 20, shade("leaf_hi", 0.2))

    # a few loose papers + pen on the desk
    c.rect(20, 50, 12, 4, P["paper"])
    c.hline(22, 51, 8, shade("ink", 0.4))
    c.hline(22, 52, 6, shade("ink", 0.45))
    c.line(34, 53, 40, 49, P["rose"])       # pen

    scaled = c.scaled(3)
    scaled = outline_alpha(scaled)

    # Crop to 276x214 (drop 2px top, matching old composition)
    scaled = scaled.crop((0, 2, 276, 216))
    final = Image.new("RGBA", (276, 214), (0, 0, 0, 0))
    final.alpha_composite(scaled, (0, 0))

    path = os.path.join(OUT, "desk-v3.webp")
    save_image(final, path, 276, 214)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 4. coffee-machine-v3-grid.webp  2760×1840  frames 230×230  12×8=96 frames
# ─────────────────────────────────────────────────────────────────────────────
def draw_coffee_machine_base(c: Canvas):
    """Draw static machine body on a 46×46 canvas (×5 → 230). Double-res, with
    finer panel seams, button bezels, a portafilter group head and water tank."""
    # machine body
    c.rect(8, 8, 30, 32, P["metal"])
    c.rect(8, 8, 30, 2, P["metal_hi"])           # top sheen
    c.rect(8, 38, 30, 2, P["metal_lo"])          # bottom shade
    c.vline(8, 8, 32, P["metal_hi"])             # left edge light
    c.vline(37, 8, 32, shade("metal_lo", -0.15)) # right edge shade

    # rounded top cap
    c.rrect(10, 6, 26, 4, P["metal_hi"], r=1)

    # inset front panel face
    c.rect(12, 12, 22, 20, P["metal_lo"])
    c.rect(12, 12, 22, 1, P["glass"])
    c.vline(12, 12, 20, shade("metal_lo", -0.25))

    # brand stripe (teal) with a thin highlight
    c.rect(12, 14, 22, 4, P["teal_lo"])
    c.rect(12, 14, 22, 1, P["teal"])
    c.rect(12, 17, 22, 1, shade("teal_lo", -0.3))

    # pressure gauge dial on the panel
    c.disc(30, 24, 3, P["white"])
    c.disc(30, 24, 2, P["paper"])
    c.line(30, 24, 31, 22, P["red_lo"])
    c.px(30, 24, P["ink"])

    # water tank (right side, translucent)
    c.rect(38, 10, 4, 24, P["glass"])
    c.rect(38, 10, 4, 2, P["glasshi"])
    water = (P["teal_hi"][0], P["teal_hi"][1], P["teal_hi"][2], 130)
    c.rect(38, 18, 4, 16, water)
    c.px(39, 20, P["white"])                      # glint

    # drip tray
    c.rect(6, 40, 34, 4, P["metal_lo"])
    c.rect(6, 40, 34, 1, P["metal"])
    for gx in range(10, 36, 3):                   # tray grille slots
        c.px(gx, 42, shade("metal_lo", -0.3))

    # base feet
    c.rect(8, 44, 5, 2, shade("metal_lo", -0.3))
    c.rect(33, 44, 5, 2, shade("metal_lo", -0.3))

    # group head / brew nozzle (portafilter)
    c.rect(20, 32, 6, 6, P["metal_lo"])
    c.rect(20, 32, 6, 1, P["metal_hi"])
    c.rect(22, 38, 2, 2, P["metal"])              # spout
    c.px(22, 39, shade("metal_lo", -0.3))
    c.px(23, 39, shade("metal_lo", -0.3))

    # buttons row (finer, with bezels)
    for bx, bc in ((14, "amber"), (20, "blue_lo"), (26, "rose")):
        c.rect(bx, 20, 4, 4, shade(bc, -0.3))     # bezel
        c.rect(bx + 1, 21, 2, 2, P[bc])           # cap
        c.px(bx + 1, 21, shade(bc, 0.3))


def draw_cup(c: Canvas, fill_level: int):
    """Draw cup (46×46 logical) with fill_level (0-10) of coffee filled."""
    # cup body
    c.rect(16, 36, 14, 9, P["white"])
    c.rect(16, 36, 14, 2, P["paper"])           # rim
    c.rect(16, 43, 14, 2, P["paper"])           # base
    c.vline(16, 37, 8, shade("white", -0.1))    # left shade
    c.frame(30, 38, 4, 5, P["paper"])           # handle
    # fill (amber = coffee)
    if fill_level > 0:
        fill_y = 44 - fill_level
        c.rect(18, fill_y, 10, fill_level, P["amber_lo"])
        c.rect(18, fill_y, 10, 1, P["amber"])    # crema surface


def draw_steam(c: Canvas, frame: int, n: int):
    """Animated steam wisps above the brew head."""
    t = frame / n
    for i, (sx, phase) in enumerate([(20, 0.0), (24, 0.5)]):
        for row in range(7):
            alpha_row = 1.0 - row / 7.0
            offset = int(math.sin(2 * math.pi * (t + phase + row * 0.1)) * 2)
            sy = 24 - row * 2 - int(t * 8) % 6
            if 0 <= sy < c.h and 0 <= sx + offset < c.w:
                alpha = int(170 * alpha_row * (0.5 + 0.5 * math.sin(2 * math.pi * t + phase)))
                if alpha > 20:
                    c.px(sx + offset, sy, (244, 246, 251, alpha))


def draw_drip(c: Canvas, frame: int, n: int):
    """Droplets falling from the spout into the cup."""
    t = (frame / n) % 1.0
    drip_t = (t * 2) % 1.0
    dy = 33 + int(drip_t * 4)
    if drip_t < 0.8:
        c.px(22, dy, P["amber"])
        c.px(23, dy, P["amber"])


def draw_status_light(c: Canvas, frame: int, n: int):
    """Blinking green status LED on the panel."""
    t = frame / n
    on = math.sin(2 * math.pi * t * 2) > 0
    c.rect(15, 28, 2, 2, P["teal"] if on else shade("teal_lo", -0.3))


def make_coffee_machine():
    COLS, ROWS = 12, 8
    N_FRAMES   = COLS * ROWS   # 96
    CELL       = 46            # logical size (double old 23)
    SCALE      = 5             # 46*5=230
    sheet = Sheet(COLS, ROWS, 230, 230)

    for f in range(N_FRAMES):
        # fill level ramps up over the cycle then resets
        fill = min(10, int(f / (N_FRAMES - 1) * 11))

        c = Canvas(CELL, CELL)
        draw_coffee_machine_base(c)
        draw_cup(c, fill)
        draw_drip(c, f, N_FRAMES)
        draw_steam(c, f, N_FRAMES)
        draw_status_light(c, f, N_FRAMES)

        scaled = c.scaled(SCALE)
        scaled = outline_alpha(scaled)
        sheet.place(scaled)

    path = os.path.join(OUT, "coffee-machine-v3-grid.webp")
    sheet.save(path, 2760, 1840)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 5. coffee-machine-shadow-v1.png  230×230
# ─────────────────────────────────────────────────────────────────────────────
def make_coffee_shadow():
    img = blurred_shadow((230, 230), 55, 12, blur=8)
    final = Image.new("RGBA", (230, 230), (0, 0, 0, 0))
    final.alpha_composite(img, (0, 20))
    path = os.path.join(OUT, "coffee-machine-shadow-v1.png")
    save_image(final, path, 230, 230)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 6. serverroom-spritesheet.webp  7200×251  frames 180×251  40×1=40 frames
# ─────────────────────────────────────────────────────────────────────────────
def draw_server_rack_base(c: Canvas):
    """Draw static rack body on a 36×52 logical canvas (×5 → 180×260).

    Authored at double the old resolution so panel seams, vents, mounting
    screws and bezels are crisp and fine instead of chunky 10px blocks.
    """
    W, H = c.w, c.h

    # cabinet outer shell
    c.rect(2, 0, W - 4, H - 1, P["metal_lo"])
    c.rect(2, 0, W - 4, 1, P["metal"])          # top edge highlight
    c.rect(2, 1, W - 4, 1, P["metal_hi"])
    c.rect(2, H - 2, W - 4, 2, shade("metal_lo", -0.2))   # base shadow

    # side frame rails (left/right) with subtle bevel
    c.rect(2, 1, 3, H - 3, P["metal"])
    c.rect(2, 1, 1, H - 3, P["metal_hi"])
    c.rect(W - 5, 1, 3, H - 3, P["metal"])
    c.rect(W - 4, 1, 1, H - 3, shade("metal_lo", -0.15))

    # inset front face (where the units live)
    fx, fw = 6, W - 12
    c.rect(fx, 3, fw, H - 7, shade("metal_lo", -0.12))
    c.rect(fx, 3, fw, 1, shade("metal_lo", -0.3))   # top inner shadow
    c.vline(fx, 3, H - 7, shade("metal_lo", -0.3))  # left inner shadow

    # brand strip header
    c.rect(fx, 4, fw, 3, P["blue_lo"])
    c.rect(fx, 4, fw, 1, P["blue"])
    c.rect(fx, 6, fw, 1, shade("blue_lo", -0.3))
    # tiny logo notch
    c.rect(fx + 2, 5, 2, 1, P["blue_hi"])

    # 8 rack units, each a thin bezel + dark slot — finer seams
    unit_top = 9
    unit_h = 5
    for u in range(8):
        uy = unit_top + u * unit_h
        # unit faceplate
        c.rect(fx + 1, uy, fw - 2, unit_h - 1, P["metal"])
        c.rect(fx + 1, uy, fw - 2, 1, P["metal_hi"])      # top highlight
        c.rect(fx + 1, uy + unit_h - 2, fw - 2, 1, shade("metal_lo", -0.2))  # seam
        # handle slot on the left of each unit
        c.rect(fx + 2, uy + 1, 3, 1, P["glass"])
        # mounting screws (left + right rail)
        c.px(fx, uy + 1, P["metal_hi"])
        c.px(fx + fw - 1, uy + 1, P["metal_hi"])

    # ventilation grille (fine vertical slats) on right portion of each unit
    for u in range(8):
        uy = unit_top + u * unit_h + 1
        for vx in range(fx + fw - 9, fx + fw - 2, 2):
            c.vline(vx, uy, 2, shade("metal_lo", -0.25))

    # side exhaust vents (right outer rail)
    for vy in range(4, H - 4, 2):
        c.px(W - 3, vy, shade("metal_lo", -0.3))
        c.px(W - 4, vy, P["metal_hi"])

    # feet
    c.rect(4, H - 2, 4, 2, shade("metal_lo", -0.35))
    c.rect(W - 8, H - 2, 4, 2, shade("metal_lo", -0.35))


def draw_rack_leds(c: Canvas, frame: int, n: int):
    """Animate fine LEDs across the rack units (36×52 logical)."""
    W, H = c.w, c.h
    t = frame / n
    fx, fw = 6, W - 12
    unit_top = 9
    unit_h = 5

    # each unit gets a small cluster of tiny status LEDs near its left edge
    for unit in range(8):
        uy = unit_top + unit * unit_h + 1
        for li in range(4):
            lx = fx + 7 + li * 2
            phase = (unit * 0.3 + li * 0.15 + t * 2.5)
            val = math.sin(2 * math.pi * phase)
            if li == 0:        # power: steady-ish green
                color = P["teal"] if val > -0.5 else P["teal_lo"]
            elif li == 1:      # activity: green blink
                color = P["teal_hi"] if val > 0.2 else shade("teal_lo", -0.3)
            elif li == 2:      # io: amber blink
                color = P["amber"] if val > 0.3 else shade("amber_lo", -0.4)
            else:              # error: red (rare)
                color = P["red"] if val > 0.88 else shade("metal_lo", -0.3)
            c.px(lx, uy, color)

    # scrolling activity sweep across the brand header
    bar_x = int((t * (fw - 4)) % (fw - 4)) + fx + 2
    c.px(bar_x, 5, P["teal_hi"])
    if bar_x + 1 < fx + fw - 1:
        c.px(bar_x + 1, 5, P["teal"])


def make_server_rack():
    N_FRAMES = 40
    # Author at 36×52 logical (double old 18×26) → ×5 = 180×260, crop to 180×251.
    LOG_W, LOG_H = 36, 52
    SCALE = 5
    sheet = Sheet(N_FRAMES, 1, 180, 251)

    for f in range(N_FRAMES):
        c = Canvas(LOG_W, LOG_H)
        draw_server_rack_base(c)
        draw_rack_leds(c, f, N_FRAMES)

        scaled = c.scaled(SCALE)   # 180×260
        scaled = outline_alpha(scaled)
        # Crop top 9px to get 180×251
        scaled = scaled.crop((0, 9, 180, 260))
        frame_img = Image.new("RGBA", (180, 251), (0, 0, 0, 0))
        frame_img.alpha_composite(scaled, (0, 0))
        sheet.place(frame_img)

    path = os.path.join(OUT, "serverroom-spritesheet.webp")
    sheet.save(path, 7200, 251)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 7. plants-spritesheet.webp  640×640  frames 160×160  4×4=16 frames
#    16 DISTINCT potted plants
# ─────────────────────────────────────────────────────────────────────────────
def _plant_pot(c: Canvas, pot_c):
    """Shared finely-detailed pot on a 32×32 logical canvas (rim, body, soil)."""
    # tapered pot body
    c.rect(10, 22, 12, 8, pot_c)
    c.rect(9, 20, 14, 3, pot_c)              # rim band
    c.rect(9, 20, 14, 1, shade("white", -0.12))     # rim highlight
    c.vline(10, 22, 8, shade("white", -0.18))        # left highlight edge
    c.vline(21, 22, 8, shade("wood_lo", -0.25))      # right shadow edge
    c.rect(10, 29, 12, 1, shade("wood_lo", -0.3))    # base shadow
    # soil line
    c.rect(11, 21, 10, 1, P["soil"])


def draw_plant(c: Canvas, kind: int):
    """Draw one of 16 distinct plants on a 32×32 logical canvas (double-res)."""
    pot_colors = [
        P["amber_lo"], P["soil"], P["metal_lo"], P["rose"],
        P["teal_lo"],  P["amber"], P["blue_lo"],  P["wood_lo"],
        P["amber_lo"], P["metal"], P["rose"],      P["teal"],
        P["soil"],     P["blue_lo"], P["amber_lo"], P["wood"],
    ]
    pot_c = pot_colors[kind % len(pot_colors)]
    _plant_pot(c, pot_c)

    if kind == 0:   # tall leafy
        c.rect(14, 6, 4, 16, P["leaf_lo"])      # central mass / stems
        for lx, ly, lw, lh in ((10, 8, 10, 8), (8, 12, 14, 6)):
            c.rect(lx, ly, lw, lh, P["leaf"])
        c.rect(9, 13, 14, 4, P["leaf_hi"])
        # leaf tips
        for tx in (10, 14, 18, 22):
            c.px(tx, 7, P["leaf_hi"]); c.px(tx, 6, P["leaf"])
        c.vline(16, 8, 12, shade("leaf_lo", -0.2))   # midrib

    elif kind == 1: # round bush
        c.disc(16, 14, 8, P["leaf"])
        c.disc(16, 14, 6, P["leaf_hi"])
        c.disc(15, 12, 3, shade("leaf_hi", 0.2))
        # dappled texture
        for dx, dy in ((12, 16), (20, 15), (16, 18), (18, 11)):
            c.px(dx, dy, P["leaf_lo"])
        c.px(18, 11, P["white"])

    elif kind == 2: # cactus
        c.rect(14, 8, 4, 14, P["teal_lo"])
        c.rect(10, 12, 4, 6, P["teal_lo"])
        c.rect(18, 14, 4, 6, P["teal_lo"])
        c.vline(15, 8, 14, P["teal"])           # ridges
        c.vline(16, 8, 14, P["teal_hi"])
        c.vline(11, 12, 6, P["teal"])
        c.vline(20, 14, 6, P["teal"])
        # spines
        for sy in range(9, 21, 2):
            c.px(13, sy, P["paper"]); c.px(18, sy, P["paper"])

    elif kind == 3: # hanging vine
        c.rect(12, 6, 8, 6, P["leaf"])
        c.rect(10, 9, 12, 4, P["leaf_hi"])
        c.disc(16, 8, 3, shade("leaf_hi", 0.15))
        for vx, phase in [(10, 0), (14, 1), (18, 0.5), (22, 0)]:
            for vy in range(13, 22):
                c.px(vx, vy, P["leaf"] if (vy + phase) % 2 == 0 else P["leaf_lo"])
            c.px(vx, 22, P["leaf_hi"])          # vine tip

    elif kind == 4: # flowering
        c.rect(14, 10, 4, 12, P["leaf_lo"])
        c.rect(10, 14, 12, 6, P["leaf"])
        c.vline(16, 10, 10, shade("leaf_lo", -0.2))
        # flowers
        for fx, fy, fc in ((12, 10, P["rose"]), (20, 12, P["amber"]), (16, 8, P["blue"])):
            c.disc(fx, fy, 2, fc)
            c.px(fx, fy, P["white"])
            c.disc(fx, fy, 1, shade(("rose" if fc==P["rose"] else "amber" if fc==P["amber"] else "blue"), 0.25))

    elif kind == 5: # fern
        c.vline(16, 8, 14, P["leaf_lo"])
        for i in range(10):
            fry = 9 + i
            w = max(1, 9 - i)
            c.hline(16 - w // 2, fry, w, P["leaf"] if i % 2 else P["leaf_hi"])
        c.px(16, 8, P["leaf_hi"])

    elif kind == 6: # succulent rosette
        c.disc(16, 17, 6, P["teal_lo"])
        c.disc(16, 17, 4, P["teal"])
        c.disc(16, 17, 2, P["teal_hi"])
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            lx = int(16 + 6 * math.cos(rad))
            ly = int(17 + 6 * math.sin(rad))
            c.px(lx, ly, P["leaf"])
            c.px(int(16 + 4 * math.cos(rad)), int(17 + 4 * math.sin(rad)), shade("teal", 0.2))

    elif kind == 7: # bonsai
        c.rect(14, 14, 4, 8, P["wood_lo"])
        c.vline(14, 14, 8, P["wood"])           # trunk highlight
        for lx, ly, lw, lh in ((9, 8, 14, 6), (11, 6, 10, 4), (7, 11, 7, 4), (18, 11, 7, 4)):
            c.rect(lx, ly, lw, lh, P["leaf"])
        c.rect(11, 7, 10, 3, P["leaf_hi"])
        c.px(16, 6, P["leaf_hi"])

    elif kind == 8: # snake plant (tall spikes)
        for sx, sw in [(11, 3), (18, 3), (14, 4)]:
            c.rect(sx, 5, sw, 17, P["leaf"])
            c.vline(sx, 5, 17, P["leaf_hi"])
            c.vline(sx + sw - 1, 5, 17, P["leaf_lo"])
            c.px(sx + sw // 2, 5, P["amber"])    # variegated tip
        c.rect(15, 5, 1, 17, shade("leaf", 0.25))

    elif kind == 9: # round cactus (barrel)
        c.disc(16, 16, 8, P["teal_lo"])
        c.disc(16, 16, 6, P["teal"])
        for i in range(-6, 7):
            c.px(16 + i, 16 - abs(i) // 2, shade("teal", 0.18))   # ridges
        for si in range(0, 360, 30):
            r2 = math.radians(si)
            c.px(int(16 + 8 * math.cos(r2)), int(16 + 8 * math.sin(r2)), P["paper"])
        c.disc(16, 11, 1, P["amber"])           # tiny flower bud

    elif kind == 10: # ivy trailing right
        c.rect(14, 8, 6, 10, P["leaf_lo"])
        c.rect(13, 10, 8, 5, P["leaf"])
        for iy in range(10, 22):
            off = (iy - 10)
            c.px(18 + off // 2, iy, P["leaf"])
            c.px(19 + off // 2, iy + 1, P["leaf_hi"])
            if iy % 3 == 0:
                c.px(17 + off // 2, iy, P["leaf_hi"])   # little leaf

    elif kind == 11: # palm / tropical
        c.rect(14, 12, 4, 10, P["wood"])
        c.vline(15, 12, 10, P["wood_hi"])
        for angle, length in [(210, 8), (170, 10), (130, 8), (250, 6), (290, 8), (200, 9)]:
            rad = math.radians(angle)
            for s in range(1, length + 1):
                lx = int(16 + s * math.cos(rad))
                ly = int(12 + s * math.sin(rad))
                if 0 <= lx < c.w and 0 <= ly < c.h:
                    c.px(lx, ly, P["leaf"] if s % 2 == 0 else P["leaf_hi"])

    elif kind == 12: # air plant (no soil, bare)
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            for s in range(3, 9):
                lx = int(16 + s * math.cos(rad))
                ly = int(16 + s * math.sin(rad))
                if 0 <= lx < c.w and 0 <= ly < c.h:
                    c.px(lx, ly, P["teal"] if s >= 7 else P["leaf"])

    elif kind == 13: # mushroom cluster
        c.rect(13, 17, 4, 5, P["white"])        # stem
        c.vline(13, 17, 5, P["paper"])
        c.disc(15, 13, 6, P["rose"])
        c.disc(15, 13, 4, shade("rose", 0.15))
        for sx, sy in ((13, 11), (17, 12), (15, 14), (18, 14)):
            c.px(sx, sy, P["white"])             # spots
        # small mushroom
        c.rect(21, 19, 2, 3, P["white"])
        c.disc(22, 16, 3, P["amber"])
        c.px(22, 15, P["white"]); c.px(23, 17, P["white"])

    elif kind == 14: # cherry blossom mini
        c.rect(14, 14, 4, 8, P["wood_lo"])
        c.vline(14, 14, 8, P["wood"])
        c.disc(15, 9, 6, P["rose"])
        c.disc(15, 9, 4, P["rose_hi"])
        for bx, by in ((11, 8), (20, 9), (14, 5), (18, 13), (13, 13)):
            c.px(bx, by, P["white"])
            c.px(bx, by + 1, shade("rose_hi", 0.2))

    else:            # 15 — zen rock garden (novelty)
        c.disc(11, 20, 3, P["metal"])
        c.disc(11, 19, 2, P["metal_hi"])
        c.disc(20, 21, 3, P["metal_hi"])
        c.disc(16, 18, 2, P["metal_lo"])
        # rake lines (raked sand)
        sand = (P["paper"][0], P["paper"][1], P["paper"][2], 90)
        for rl in range(8, 27, 3):
            c.hline(7, rl, 18, sand)
        # tiny plant
        c.vline(24, 13, 6, P["leaf"])
        c.px(23, 13, P["leaf_hi"]); c.px(25, 15, P["leaf_hi"])


def make_plants():
    sheet = Sheet(4, 4, 160, 160)
    for i in range(16):
        c = Canvas(32, 32)
        draw_plant(c, i)
        scaled = c.scaled(5)     # 160×160
        scaled = outline_alpha(scaled)
        sheet.place(scaled)
    path = os.path.join(OUT, "plants-spritesheet.webp")
    sheet.save(path, 640, 640)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 8. posters-spritesheet.webp  640×1280  frames 160×160  4×8=32 frames
# ─────────────────────────────────────────────────────────────────────────────
class _ScaleCanvas:
    """Coordinate-scaling proxy: forwards drawing to a real Canvas, multiplying
    every coordinate/size by `s`. Lets us run art code authored for a 16×16 grid
    on a 32×32 canvas unchanged, so each old art-pixel becomes an s×s block while
    the surrounding frame/mat is drawn finer directly on the real canvas."""

    def __init__(self, canvas: Canvas, s: int):
        self._c = canvas
        self.s = s
        self.w = canvas.w // s
        self.h = canvas.h // s

    def px(self, x, y, c):
        self._c.rect(int(x) * self.s, int(y) * self.s, self.s, self.s, c)

    def rect(self, x, y, w, h, c):
        self._c.rect(int(x) * self.s, int(y) * self.s, w * self.s, h * self.s, c)

    def frame(self, x, y, w, h, c):
        s = self.s
        self._c.rect(x * s, y * s, w * s, s, c)
        self._c.rect(x * s, (y + h - 1) * s, w * s, s, c)
        self._c.rect(x * s, y * s, s, h * s, c)
        self._c.rect((x + w - 1) * s, y * s, s, h * s, c)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c):
        self._c.line(x0 * self.s, y0 * self.s, x1 * self.s, y1 * self.s, c)

    def disc(self, cx, cy, r, c):
        s = self.s
        self._c.disc(cx * s + s // 2, cy * s + s // 2, r * s + s // 2 - 1, c)


def draw_poster(c32: Canvas, kind: int):
    """Draw one of 32 framed wall posters on a 32×32 logical canvas.

    The shared frame/mat/canvas are drawn finely at full 32-res; the per-kind
    artwork runs through a ×2 coordinate proxy so all 32 original designs are
    preserved while bezels/edges are crisp at the finer pixel density."""
    frame_colors = [
        P["wood"], P["metal"], P["ink2"], P["amber_lo"],
        P["wood_lo"], P["metal_hi"], P["rose"], P["teal_lo"],
    ]
    fc = frame_colors[kind % len(frame_colors)]
    # fine outer frame (2px), mat (2px), then canvas
    c32.rect(0, 0, 32, 32, fc)                      # frame body
    c32.rect(0, 0, 32, 1, shade("white", -0.2))    # frame top highlight
    c32.rect(0, 31, 32, 1, shade("wood_lo", -0.3)) # frame bottom shadow
    c32.frame(1, 1, 30, 30, shade("white", -0.25)) # inner bevel line
    c32.rect(2, 2, 28, 28, P["paper"])             # mat
    c32.rect(4, 4, 24, 24, P["white"])             # canvas
    c32.rect(4, 4, 24, 1, shade("white", 0.05))    # canvas top sheen

    # per-kind artwork via ×2 proxy (operates on the 16×16 inner art region)
    c = _ScaleCanvas(c32, 2)

    if kind == 0:   # abstract — colored circles
        c.disc(7, 7, 4, P["blue"])
        c.disc(9, 9, 3, P["teal"])
        c.disc(5, 9, 2, P["rose"])

    elif kind == 1: # mountain landscape
        c.rect(2, 9, 12, 5, P["blue_lo"])    # sky
        c.rect(2, 11, 12, 3, P["leaf_lo"])   # grass
        # mountains
        for mx, mh, mc in [(4, 5, P["metal"]), (8, 7, P["metal_hi"]), (12, 4, P["metal_lo"])]:
            for row in range(mh):
                width = 2 * (mh - row) // 2 + 1
                c.hline(mx - width // 2, 13 - row, width, mc)

    elif kind == 2: # bar chart
        c.rect(2, 2, 12, 12, P["paper"])
        for bi, (bh, bc) in enumerate([(6, P["teal"]), (9, P["blue"]), (4, P["rose"]), (8, P["amber"])]):
            bx = 3 + bi * 3
            c.rect(bx, 13 - bh, 2, bh, bc)

    elif kind == 3: # pixel mascot cat face
        c.rect(2, 2, 12, 12, P["floor"])
        c.disc(8, 8, 4, P["amber"])
        c.px(6, 7, P["ink"]); c.px(10, 7, P["ink"])  # eyes
        c.rect(7, 9, 3, 1, P["ink"])                  # mouth
        c.px(5, 5, P["amber"]); c.px(11, 5, P["amber"])  # ears

    elif kind == 4: # gradient sky
        for gy in range(12):
            t = gy / 11
            r = int(P["blue_lo"][0] * (1 - t) + P["rose"][0] * t)
            g = int(P["blue_lo"][1] * (1 - t) + P["rose"][1] * t)
            b = int(P["blue_lo"][2] * (1 - t) + P["rose"][2] * t)
            c.hline(2, 2 + gy, 12, (r, g, b, 255))

    elif kind == 5: # pixel grid / blueprint
        c.rect(2, 2, 12, 12, P["glass"])
        for gx in range(2, 14, 2):
            c.vline(gx, 2, 12, P["glasshi"])
        for gy in range(2, 14, 2):
            c.hline(2, gy, 12, P["glasshi"])
        c.rect(4, 4, 8, 4, P["teal_lo"])

    elif kind == 6: # sunset horizon
        for sy in range(6):
            t = sy / 5
            r = int(P["amber"][0] * (1 - t) + P["rose"][0] * t)
            g2= int(P["amber"][1] * (1 - t) + P["rose"][1] * t)
            b2= int(P["amber"][2] * (1 - t) + P["rose"][2] * t)
            c.hline(2, 2 + sy, 12, (r, g2, b2, 255))
        c.rect(2, 8, 12, 6, P["blue_lo"])
        # sun
        c.disc(8, 8, 2, P["amber_hi"])

    elif kind == 7: # "LOG8" text block
        c.rect(2, 2, 12, 12, P["ink"])
        # simple pixel letters L O G 8
        # L
        c.vline(3, 3, 5, P["teal"])
        c.hline(3, 7, 3, P["teal"])
        # O
        c.frame(6, 3, 3, 5, P["teal"])
        # G
        c.vline(10, 3, 5, P["teal"])
        c.hline(10, 7, 3, P["teal"])
        c.hline(10, 3, 3, P["teal"])
        c.px(12, 5, P["teal"])
        c.px(12, 6, P["teal"])
        # 8 (bottom row)
        c.frame(3, 9, 3, 4, P["amber"])
        c.hline(3, 11, 3, P["amber"])

    elif kind == 8: # space / stars
        c.rect(2, 2, 12, 12, (10, 10, 30, 255))
        import random; rng = random.Random(8)
        for _ in range(15):
            sx = rng.randint(2, 13); sy = rng.randint(2, 13)
            c.px(sx, sy, P["white"])
        c.disc(10, 4, 2, P["amber_hi"])   # planet

    elif kind == 9: # line graph
        c.rect(2, 2, 12, 12, P["paper"])
        pts = [7, 5, 9, 4, 8, 6, 3, 7, 5, 4, 6, 8]
        for xi, yv in enumerate(pts):
            c.px(3 + xi, 13 - yv, P["teal"])
            if xi > 0:
                c.px(3 + xi - 1, 13 - pts[xi - 1], P["teal"])

    elif kind == 10: # geometric pattern
        c.rect(2, 2, 12, 12, P["paper"])
        for gi in range(6):
            c.rect(2 + gi, 2 + gi, 12 - 2 * gi, 12 - 2 * gi, P["clear"])
            c.frame(2 + gi, 2 + gi, 12 - 2 * gi, 12 - 2 * gi,
                    [P["blue"], P["teal"], P["rose"], P["amber"], P["blue_lo"], P["teal_lo"]][gi])

    elif kind == 11: # pixel sushi
        c.rect(2, 2, 12, 12, P["floor"])
        c.disc(8, 9, 4, P["white"])
        c.disc(8, 9, 3, P["rose_hi"])
        c.hline(5, 9, 6, P["ink2"])   # nori band
        c.disc(8, 9, 1, P["amber"])   # roe

    elif kind == 12: # ocean wave
        c.rect(2, 2, 12, 12, P["blue_lo"])
        for wx in range(2, 14):
            wy = 7 + int(2 * math.sin((wx - 2) * 0.8))
            c.rect(wx, 2, 1, wy - 2, P["teal_lo"])
            c.px(wx, wy - 2, P["white"])

    elif kind == 13: # coffee cup close-up
        c.rect(2, 2, 12, 12, P["floor"])
        c.rect(5, 6, 6, 6, P["amber_lo"])
        c.rect(5, 6, 6, 1, P["amber"])
        c.px(11, 8, P["amber_lo"])   # handle
        # steam
        c.px(7, 4, P["white"]); c.px(9, 3, P["white"]); c.px(8, 5, P["white"])

    elif kind == 14: # pixel tree
        c.rect(2, 2, 12, 12, P["blue_lo"])
        c.rect(7, 10, 2, 3, P["wood"])
        c.rect(4, 7, 8, 5, P["leaf"])
        c.rect(5, 4, 6, 5, P["leaf_hi"])
        c.rect(6, 2, 4, 4, P["leaf"])
        c.px(8, 2, P["leaf_hi"])

    elif kind == 15: # retro robot face
        c.rect(2, 2, 12, 12, P["metal_lo"])
        c.rect(4, 4, 8, 8, P["metal"])
        c.rect(5, 5, 3, 3, P["teal"])   # eye L
        c.rect(9, 5, 3, 3, P["teal"])   # eye R
        c.rect(5, 9, 6, 1, P["ink"])    # mouth
        c.px(8, 3, P["amber"])          # antenna

    elif kind == 16: # spiral / vortex
        c.rect(2, 2, 12, 12, P["ink"])
        for r in range(5, 0, -1):
            colors = [P["blue"], P["teal"], P["rose"], P["amber"], P["blue_lo"]]
            c.frame(8 - r, 8 - r, 2 * r, 2 * r, colors[r - 1])

    elif kind == 17: # pixel pizza
        c.rect(2, 2, 12, 12, P["floor_lo"])
        c.disc(8, 8, 5, P["amber"])
        c.disc(8, 8, 4, P["amber_hi"])
        # toppings
        for tx, ty in [(7, 7), (9, 8), (8, 10), (6, 9)]:
            c.px(tx, ty, P["rose"])
        c.disc(8, 8, 1, P["amber_lo"])

    elif kind == 18: # pixel house
        c.rect(2, 2, 12, 12, P["blue_lo"])
        # house body
        c.rect(4, 8, 8, 5, P["wood"])
        # roof
        for ri in range(4):
            c.hline(4 + ri, 8 - ri, 8 - 2 * ri, P["rose"])
        # door
        c.rect(7, 10, 2, 3, P["amber_lo"])
        # window
        c.rect(5, 9, 2, 2, P["teal"])

    elif kind == 19: # music notes
        c.rect(2, 2, 12, 12, P["glass"])
        c.vline(7, 4, 5, P["amber"])
        c.disc(6, 9, 1, P["amber"])
        c.vline(11, 3, 5, P["amber"])
        c.disc(10, 8, 1, P["amber"])
        c.hline(7, 4, 4, P["amber_lo"])  # beam

    elif kind == 20: # pixel heart
        c.rect(2, 2, 12, 12, P["ink2"])
        heart_pixels = [
            (5,4),(6,4),(9,4),(10,4),
            (4,5),(5,5),(6,5),(7,5),(8,5),(9,5),(10,5),(11,5),
            (4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(11,6),
            (5,7),(6,7),(7,7),(8,7),(9,7),(10,7),
            (6,8),(7,8),(8,8),(9,8),
            (7,9),(8,9),
        ]
        for hx, hy in heart_pixels:
            c.px(hx, hy, P["rose"])

    elif kind == 21: # DNA helix
        c.rect(2, 2, 12, 12, P["glass"])
        for ry in range(10):
            t = ry / 9
            lx = int(4 + 3 * math.sin(t * 2 * math.pi))
            rx = int(12 - 3 * math.sin(t * 2 * math.pi))
            c.px(lx, 3 + ry, P["teal"])
            c.px(rx, 3 + ry, P["rose"])
            if ry % 3 == 0:
                c.hline(min(lx, rx), 3 + ry, abs(rx - lx) + 1, P["metal"])

    elif kind == 22: # city skyline
        c.rect(2, 2, 12, 12, P["ink2"])
        # buildings
        for bx, bh, bw in [(2,5,2),(4,8,2),(6,4,2),(8,7,3),(11,5,2)]:
            c.rect(bx, 13 - bh, bw, bh, P["metal"])
            c.px(bx + 1, 13 - bh - 1, P["amber"])  # light
        c.rect(2, 10, 12, 3, P["floor_lo"])  # ground

    elif kind == 23: # pixel sun
        c.rect(2, 2, 12, 12, P["amber_lo"])
        c.disc(8, 8, 4, P["amber"])
        c.disc(8, 8, 3, P["amber_hi"])
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            c.px(int(8 + 5 * math.cos(rad)), int(8 + 5 * math.sin(rad)), P["amber_hi"])

    elif kind == 24: # pixel fish bowl
        c.rect(2, 2, 12, 12, P["paper"])
        c.disc(8, 8, 5, P["blue_lo"])
        c.disc(8, 8, 4, (100, 150, 220, 200))
        c.px(8, 8, P["rose"])        # fish body
        c.px(7, 8, P["amber_hi"])    # fish tail
        c.px(9, 8, P["rose_hi"])     # fish head
        c.px(9, 7, P["ink"])         # eye

    elif kind == 25: # constellation map
        c.rect(2, 2, 12, 12, (10, 10, 30, 255))
        stars = [(3,3),(5,5),(9,4),(12,6),(7,8),(4,10),(11,11),(8,12)]
        for sx, sy in stars:
            c.px(sx, sy, P["white"])
        for i in range(len(stars) - 1):
            c.line(stars[i][0], stars[i][1], stars[i+1][0], stars[i+1][1], P["glasshi"])

    elif kind == 26: # pie chart
        c.rect(2, 2, 12, 12, P["paper"])
        # draw wedges manually with pixels
        cx, cy = 8, 8
        for angle in range(360):
            rad = math.radians(angle)
            for r in range(1, 5):
                px_x = int(cx + r * math.cos(rad))
                px_y = int(cy + r * math.sin(rad))
                if 0 <= px_x < 16 and 0 <= px_y < 16:
                    if angle < 130:
                        c.px(px_x, px_y, P["teal"])
                    elif angle < 230:
                        c.px(px_x, px_y, P["blue"])
                    elif angle < 310:
                        c.px(px_x, px_y, P["rose"])
                    else:
                        c.px(px_x, px_y, P["amber"])

    elif kind == 27: # pixel dinosaur (simple)
        c.rect(2, 2, 12, 12, P["leaf_lo"])
        # dino body
        c.rect(5, 7, 6, 5, P["teal"])
        c.rect(7, 5, 3, 3, P["teal"])   # head
        c.px(9, 5, P["ink"])            # eye
        c.px(10, 7, P["teal_lo"])       # mouth
        # legs
        c.px(6, 12, P["teal"]); c.px(7, 12, P["teal"])
        c.px(9, 12, P["teal"]); c.px(10, 12, P["teal"])
        # tail
        c.px(4, 8, P["teal"]); c.px(3, 9, P["teal_lo"])

    elif kind == 28: # retro TV
        c.rect(2, 2, 12, 12, P["metal"])
        c.rect(3, 3, 9, 8, P["glass"])
        c.rect(3, 3, 9, 1, P["glasshi"])
        # static / show on screen
        import random; rng2 = random.Random(28)
        for _ in range(10):
            sx2 = rng2.randint(3, 11); sy2 = rng2.randint(3, 10)
            c.px(sx2, sy2, P["white"] if rng2.random() > 0.5 else P["metal_lo"])
        # antenna
        c.px(8, 2, P["metal"]); c.px(9, 2, P["metal"])
        # knobs
        c.px(13, 5, P["amber"]); c.px(13, 7, P["amber"])

    elif kind == 29: # beach / palm silhouette
        c.rect(2, 2, 12, 12, P["amber_lo"])
        c.rect(2, 9, 12, 5, P["teal_lo"])   # sea
        c.vline(8, 4, 7, P["wood_lo"])       # trunk
        c.hline(5, 4, 7, P["leaf"])          # fronds
        c.hline(6, 5, 5, P["leaf_hi"])
        c.disc(7, 8, 1, P["amber_hi"])       # sun reflection

    elif kind == 30: # pixel gem / diamond
        c.rect(2, 2, 12, 12, P["ink2"])
        # diamond shape
        pts2 = [
            (8, 4), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7),
            (6, 8), (7, 8), (8, 8), (9, 8), (10, 8),
            (7, 9), (8, 9), (9, 9),
            (8, 11),
        ]
        for gx, gy in pts2:
            c.px(gx, gy, P["teal_hi"])
        c.px(8, 4, P["white"])
        c.px(6, 7, P["blue_hi"])
        c.px(10, 7, P["blue"])

    else:            # 31 — pixel aurora
        c.rect(2, 2, 12, 12, (5, 5, 20, 255))
        for ay in range(4):
            for ax in range(10):
                t2 = (ax + ay * 0.3) / 9.0
                r3 = int(P["teal"][0] * t2 + P["blue"][0] * (1 - t2))
                g3 = int(P["teal"][1] * t2 + P["blue"][1] * (1 - t2))
                b3 = int(P["teal"][2] * t2 + P["blue"][2] * (1 - t2))
                wave_y = 4 + ay + int(2 * math.sin(ax * 0.7 + ay))
                if 2 <= wave_y < 14:
                    c.px(3 + ax, wave_y, (r3, g3, b3, 200 - ay * 30))


def make_posters():
    sheet = Sheet(4, 8, 160, 160)
    for i in range(32):
        c = Canvas(32, 32)
        draw_poster(c, i)
        scaled = c.scaled(5)     # 160×160
        scaled = outline_alpha(scaled)
        sheet.place(scaled)
    path = os.path.join(OUT, "posters-spritesheet.webp")
    sheet.save(path, 640, 1280)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 9. flowers-bloom-v2.webp  512×512  frames 128×128  4×4=16 frames
# ─────────────────────────────────────────────────────────────────────────────
def make_flowers_bloom():
    # Author at 24×24 logical (double old 12×12) → ×5 = 120×120, center in 128.
    LW = 24
    sheet = Sheet(4, 4, 128, 128)

    for f in range(16):
        t = f / 15.0   # 0..1 bloom progress
        c = Canvas(LW, LW)

        # stem (finer, with a highlight edge)
        stem_h = max(2, int(10 * min(t * 2, 1.0)))
        sy = LW - stem_h - 2
        c.rect(11, sy, 3, stem_h + 2, P["leaf_lo"])
        c.vline(11, sy, stem_h + 2, P["leaf"])      # lit edge
        c.px(11, sy, P["leaf_hi"])

        # leaves (appear from t=0.2) — pointed, two-tone
        if t > 0.2:
            lt = min(1.0, (t - 0.2) / 0.3)
            lw = max(1, int(6 * lt))
            for ly, sgn, x0 in ((LW - 8, -1, 10), (LW - 11, 1, 13)):
                for k in range(lw):
                    c.px(x0 + sgn * k, ly - k // 2, P["leaf"] if k % 2 else P["leaf_hi"])
                c.px(x0 + sgn * (lw - 1), ly - (lw - 1) // 2, P["leaf_lo"])

        # bud / bloom
        if t < 0.3:
            bud_h = max(1, int(6 * (t / 0.3)))
            c.rect(11, sy - bud_h, 3, bud_h, P["leaf"])
            c.px(12, sy - bud_h, P["leaf_hi"])
        elif t < 0.6:
            pt = (t - 0.3) / 0.3
            petal_r = max(1, int(7 * pt))
            cy = sy - 2 - petal_r
            c.disc(12, cy, petal_r, P["rose"])
            c.disc(12, cy, max(1, petal_r - 2), P["rose_hi"])
            c.disc(12, cy, max(1, petal_r - 4), P["amber"])   # center
        else:
            if t < 0.85:
                pt = min(1.0, (t - 0.6) / 0.25)
                pr = max(2, int(8 + pt * 2))
                bx = 12
            else:
                # gentle sway — full bloom with slight lean
                pr = 10
                bx = 12 + int(math.sin(2 * math.pi * (t - 0.85) / 0.15) * 2)
            cy = sy - pr - 1
            # layered petals
            c.disc(bx, cy, pr, P["rose"])
            c.disc(bx, cy, pr - 2, P["rose_hi"])
            c.disc(bx, cy, max(1, pr - 5), P["amber_hi"])
            c.disc(bx, cy, max(1, pr - 7), P["amber"])
            c.px(bx, cy, P["white"])
            # 8 petal tips + inner shading
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                tx2 = int(bx + (pr + 1) * math.cos(rad))
                ty2 = int(cy + (pr + 1) * math.sin(rad))
                if 0 <= tx2 < LW and 0 <= ty2 < LW:
                    c.px(tx2, ty2, P["rose_hi"])
                # petal seam shading
                ix = int(bx + (pr - 1) * math.cos(rad + 0.39))
                iy = int(cy + (pr - 1) * math.sin(rad + 0.39))
                if 0 <= ix < LW and 0 <= iy < LW:
                    c.px(ix, iy, shade("rose", -0.2))

        scaled = c.scaled(5)    # 120×120
        scaled = outline_alpha(scaled)
        # center in 128×128 cell
        frame_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        frame_img.alpha_composite(scaled, (4, 4))
        sheet.place(frame_img)

    path = os.path.join(OUT, "flowers-bloom-v2.webp")
    sheet.save(path, 512, 512)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 10. memo-bg.webp  400×300  WEBP lossless (no transparency)
# ─────────────────────────────────────────────────────────────────────────────
def make_memo_bg():
    img = Image.new("RGBA", (400, 300), P["paper"])
    d = ImageDraw.Draw(img)

    # subtle dot grid
    dot_color = (*P["ink"][:3], 25)
    for gy in range(20, 285, 20):
        for gx in range(20, 385, 20):
            d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=dot_color)

    # subtle horizontal lines (rule lines)
    line_color = (*P["ink"][:3], 18)
    for ly in range(40, 280, 24):
        d.line([16, ly, 384, ly], fill=line_color, width=1)

    # left margin line (faint rose/pink)
    margin_color = (*P["rose"][:3], 35)
    d.line([45, 10, 45, 290], fill=margin_color, width=1)

    # top colored stripe (sticky note style)
    stripe_color = (*P["amber"][:3], 80)
    d.rectangle([0, 0, 400, 8], fill=stripe_color)

    # folded corner (bottom-right)
    fold_size = 24
    fold_color = (*P["amber_lo"][:3], 120)
    # triangle fold shadow
    d.polygon([
        (400 - fold_size, 300),
        (400, 300 - fold_size),
        (400, 300),
    ], fill=fold_color)
    # fold line
    fold_line_color = (*P["ink"][:3], 40)
    d.line([400 - fold_size, 300, 400, 300 - fold_size], fill=fold_line_color, width=1)

    # slight drop shadow effect (inner border darkening)
    border_color = (*P["ink"][:3], 10)
    d.rectangle([0, 0, 399, 299], outline=border_color, width=2)

    path = os.path.join(OUT, "memo-bg.webp")
    save_image(img, path, 400, 300)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating assets…")
    results = []

    tasks = [
        (make_sofa,           "sofa-idle-v3.png",              256, 256),
        (make_sofa_shadow,    "sofa-shadow-v1.png",            256, 256),
        (make_desk,           "desk-v3.webp",                  276, 214),
        (make_coffee_machine, "coffee-machine-v3-grid.webp",  2760, 1840),
        (make_coffee_shadow,  "coffee-machine-shadow-v1.png",  230, 230),
        (make_server_rack,    "serverroom-spritesheet.webp",  7200, 251),
        (make_plants,         "plants-spritesheet.webp",       640, 640),
        (make_posters,        "posters-spritesheet.webp",      640, 1280),
        (make_flowers_bloom,  "flowers-bloom-v2.webp",         512, 512),
        (make_memo_bg,        "memo-bg.webp",                  400, 300),
    ]

    for fn, fname, exp_w, exp_h in tasks:
        print(f"\n→ {fname}")
        path = fn()
        ok = verify(path, exp_w, exp_h, fname)
        results.append((fname, path, exp_w, exp_h, ok))

    print("\n" + "=" * 60)
    all_pass = all(r[4] for r in results)
    for fname, path, ew, eh, ok in results:
        print(f"  {'✓' if ok else '✗'}  {fname}  {ew}×{eh}")
    print("=" * 60)
    print(f"{'ALL PASS' if all_pass else 'SOME FAILED'}")
