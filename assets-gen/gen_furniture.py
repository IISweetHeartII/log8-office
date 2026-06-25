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
    # Author at 32×32 logical, scale to 256 (×8)
    LW, LH = 32, 32
    c = Canvas(LW, LH)

    sofa_color   = P["blue"]
    sofa_hi      = P["blue_hi"]
    sofa_lo      = P["blue_lo"]
    cushion      = shade("blue", 0.15)
    leg          = P["wood_lo"]
    piping       = P["ink2"]

    # legs (2 px wide, 2 px tall)
    c.rect(4, 28, 2, 3, leg)
    c.rect(26, 28, 2, 3, leg)

    # sofa base / seat
    c.rect(3, 22, 26, 8, sofa_lo)   # base body
    c.rect(3, 22, 26, 1, piping)    # top edge piping

    # back cushion strip
    c.rect(3, 14, 26, 9, sofa_color)
    c.rect(3, 14, 26, 1, sofa_hi)   # highlight top

    # armrests
    c.rect(1, 15, 3, 14, sofa_lo)
    c.rect(28, 15, 3, 14, sofa_lo)
    c.rect(1, 15, 3, 1, sofa_hi)
    c.rect(28, 15, 3, 1, sofa_hi)

    # seat cushions (two)
    c.rect(4, 23, 11, 6, cushion)
    c.rect(17, 23, 11, 6, cushion)
    c.vline(16, 23, 6, piping)     # seam between cushions

    # cushion highlight dots
    c.px(8, 24, sofa_hi)
    c.px(22, 24, sofa_hi)

    # small back pillow left
    c.rect(5, 16, 8, 6, P["amber"])
    c.rect(5, 16, 8, 1, P["amber_hi"])
    c.px(9, 19, P["amber_hi"])

    # small back pillow right
    c.rect(19, 16, 8, 6, P["rose"])
    c.rect(19, 16, 8, 1, P["rose_hi"])
    c.px(23, 19, P["rose_hi"])

    # outline
    scaled = c.scaled(8)
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
    # Logical 46×36 → ×6 = 276×216, then trim to 276×214
    LW, LH = 46, 36
    c = Canvas(LW, LH)

    wood   = P["wood"]
    wood_h = P["wood_hi"]
    wood_l = P["wood_lo"]
    leg    = P["wood_lo"]

    # legs (front)
    c.rect(2, 24, 3, 12, leg)
    c.rect(41, 24, 3, 12, leg)
    # back legs (shorter visible)
    c.rect(6, 22, 2, 5, wood_l)
    c.rect(38, 22, 2, 5, wood_l)

    # desk surface (isometric-ish flat top)
    c.rect(1, 18, 44, 7, wood)
    c.hline(1, 18, 44, wood_h)   # top highlight
    c.hline(1, 24, 44, wood_l)   # bottom edge

    # under-desk shelf
    c.rect(5, 28, 36, 3, wood_l)

    # monitor (small, on desk)
    # screen base
    c.rect(17, 8, 14, 11, P["metal_lo"])
    c.rect(18, 9, 12, 9, P["screen"])   # screen area
    c.rect(18, 9, 12, 1, P["screen2"])  # screen hi
    # teal glow pixels
    for px_x in range(19, 29, 2):
        c.px(px_x, 11, P["teal"])
        c.px(px_x + 1, 13, P["teal_lo"])
    # monitor stand
    c.rect(22, 19, 4, 1, P["metal"])
    c.rect(20, 20, 8, 1, P["metal_lo"])

    # keyboard (flat on desk)
    c.rect(10, 20, 16, 3, P["metal"])
    c.rect(10, 20, 16, 1, P["metal_hi"])
    # key dots
    for kx in range(11, 26, 2):
        c.px(kx, 21, P["metal_hi"])

    # mug (right of keyboard)
    c.rect(30, 17, 5, 5, P["amber"])
    c.rect(30, 17, 5, 1, P["amber_hi"])
    c.rect(31, 18, 3, 3, P["amber_lo"])   # mug inside
    c.px(35, 19, P["amber_lo"])           # handle nub
    # steam wisps
    c.px(31, 15, shade("white", -0.1))
    c.px(33, 14, shade("white", -0.1))

    # small plant / pencil cup top-left
    c.rect(3, 15, 4, 4, P["teal_lo"])
    c.rect(3, 15, 4, 1, P["teal"])
    c.vline(4, 12, 3, P["leaf"])
    c.vline(6, 11, 4, P["leaf_hi"])

    scaled = c.scaled(6)
    scaled = outline_alpha(scaled)

    # Crop to 276x214
    scaled = scaled.crop((0, 2, 276, 216))
    # Ensure exact 276x214
    final = Image.new("RGBA", (276, 214), (0, 0, 0, 0))
    final.alpha_composite(scaled, (0, 0))

    path = os.path.join(OUT, "desk-v3.webp")
    save_image(final, path, 276, 214)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 4. coffee-machine-v3-grid.webp  2760×1840  frames 230×230  12×8=96 frames
# ─────────────────────────────────────────────────────────────────────────────
def draw_coffee_machine_base(c: Canvas):
    """Draw static machine body on a 23×23 canvas (upscaled ×10 → 230)."""
    # machine body
    c.rect(4, 4, 15, 16, P["metal"])
    c.rect(4, 4, 15, 1, P["metal_hi"])
    c.rect(4, 19, 15, 1, P["metal_lo"])

    # panel face
    c.rect(6, 6, 11, 10, P["metal_lo"])
    c.rect(6, 6, 11, 1, P["glass"])

    # brand stripe (teal)
    c.rect(6, 7, 11, 2, P["teal_lo"])

    # water tank (right side bump)
    c.rect(18, 5, 2, 12, P["glass"])
    c.rect(18, 5, 2, 1, P["glasshi"])

    # drip tray
    c.rect(3, 20, 17, 2, P["metal_lo"])
    c.rect(3, 20, 17, 1, P["metal"])

    # base feet
    c.rect(4, 22, 3, 1, P["metal_lo"])
    c.rect(16, 22, 3, 1, P["metal_lo"])

    # nozzle / brew head (centered top of tray)
    c.rect(10, 16, 3, 4, P["metal_lo"])
    c.px(11, 20, P["metal"])

    # buttons row
    c.rect(7, 10, 2, 2, P["amber"])
    c.rect(10, 10, 2, 2, P["blue_lo"])
    c.rect(13, 10, 2, 2, P["rose"])


def draw_cup(c: Canvas, fill_level: int):
    """Draw cup with fill_level (0-5) rows of coffee filled."""
    # cup body
    c.rect(8, 18, 7, 5, P["white"])
    c.rect(8, 18, 7, 1, P["paper"])
    c.rect(8, 22, 7, 1, P["paper"])    # cup base
    c.px(15, 20, P["paper"])           # handle
    # fill (amber = coffee)
    if fill_level > 0:
        fill_y = 22 - fill_level
        c.rect(9, fill_y, 5, fill_level, P["amber_lo"])


def draw_steam(c: Canvas, frame: int, n: int):
    """Animated steam wisps above nozzle."""
    t = frame / n
    # two wisps offset in phase
    for i, (sx, phase) in enumerate([(10, 0.0), (12, 0.5)]):
        for row in range(4):
            alpha_row = 1.0 - row / 4.0
            offset = int(math.sin(2 * math.pi * (t + phase + row * 0.1)) * 1)
            sy = 12 - row * 2 - int(t * 4) % 4
            if 0 <= sy < c.h and 0 <= sx + offset < c.w:
                alpha = int(180 * alpha_row * (0.5 + 0.5 * math.sin(2 * math.pi * t + phase)))
                if alpha > 20:
                    col = (244, 246, 251, alpha)
                    c.px(sx + offset, sy, col)


def draw_drip(c: Canvas, frame: int, n: int):
    """A droplet falling from nozzle into cup."""
    # drip appears mid-cycle
    t = (frame / n) % 1.0
    drip_y_start = 17
    drip_y_end   = 18
    drip_t = (t * 2) % 1.0   # twice per cycle
    dy = drip_y_start + int(drip_t * (drip_y_end - drip_y_start + 1))
    if drip_t < 0.8:
        c.px(11, dy, P["amber"])


def draw_status_light(c: Canvas, frame: int, n: int):
    """Blinking green status LED."""
    t = frame / n
    on = math.sin(2 * math.pi * t * 2) > 0
    color = P["teal"] if on else P["teal_lo"]
    c.px(14, 8, color)


def make_coffee_machine():
    COLS, ROWS = 12, 8
    N_FRAMES   = COLS * ROWS   # 96
    CELL       = 23            # logical size
    SCALE      = 10            # 23*10=230
    sheet = Sheet(COLS, ROWS, 230, 230)

    for f in range(N_FRAMES):
        # fill level ramps up over first ~60 frames then resets
        fill = min(5, int(f / (N_FRAMES - 1) * 6))

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
    """Draw static rack body on 18×26 logical canvas."""
    W, H = c.w, c.h
    # rack cabinet body
    c.rect(1, 0, W - 2, H - 1, P["metal_lo"])
    c.rect(1, 0, W - 2, 1, P["metal"])        # top edge
    c.rect(1, H - 1, W - 2, 1, P["metal_lo"]) # base

    # door panel (front face)
    c.rect(2, 1, W - 4, H - 3, P["metal"])
    c.rect(2, 1, W - 4, 1, P["metal_hi"])

    # rack units (horizontal lines dividing units)
    for ry in range(3, H - 4, 3):
        c.hline(3, ry, W - 6, P["metal_lo"])

    # ventilation slots right edge
    for vy in range(2, H - 3, 2):
        c.px(W - 2, vy, P["metal_hi"])

    # rack ears (mounting rails)
    c.vline(2, 2, H - 4, P["metal_hi"])
    c.vline(W - 3, 2, H - 4, P["metal_hi"])

    # brand strip top
    c.rect(3, 2, W - 6, 2, P["blue_lo"])
    c.rect(3, 2, W - 6, 1, P["blue"])


def draw_rack_leds(c: Canvas, frame: int, n: int):
    """Animate LEDs across rack units."""
    W, H = c.w, c.h
    t = frame / n

    # 8 rack units, each with 3 LEDs
    for unit in range(8):
        uy = 4 + unit * 3
        # Active/idle pattern shifts per frame
        for li in range(3):
            lx = 4 + li * 3
            phase = (unit * 0.3 + li * 0.15 + t * 2.5)
            val = math.sin(2 * math.pi * phase)
            if lx < W - 4:
                if li == 0:   # power/status: green
                    color = P["teal"] if val > -0.3 else P["teal_lo"]
                elif li == 1: # activity: amber blink
                    color = P["amber"] if val > 0.2 else P["metal_lo"]
                else:          # error: red (rare)
                    color = P["red"] if val > 0.85 else P["metal_lo"]
                c.px(lx, uy, color)

    # scrolling activity bar at top panel
    bar_x = int((t * (W - 8)) % (W - 8)) + 4
    if bar_x < W - 3:
        c.px(bar_x, 3, P["teal"])
        if bar_x + 1 < W - 3:
            c.px(bar_x + 1, 3, P["teal_lo"])


def make_server_rack():
    N_FRAMES = 40
    # Logical: 18 wide × 26 tall → ×10 = 180×260, but target cell is 180×251
    # Author at 18×26, scale ×10=180×260, then crop to 180×251
    LOG_W, LOG_H = 18, 26
    SCALE = 10
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
def draw_plant(c: Canvas, kind: int):
    """Draw one of 16 distinct plants on a 16×16 logical canvas."""
    # Pot (shared base, slight color variation)
    pot_colors = [
        P["amber_lo"], P["soil"], P["metal_lo"], P["rose"],
        P["teal_lo"],  P["amber"], P["blue_lo"],  P["wood_lo"],
        P["amber_lo"], P["metal"], P["rose"],      P["teal"],
        P["soil"],     P["blue_lo"], P["amber_lo"], P["wood"],
    ]
    pot_c = pot_colors[kind % len(pot_colors)]
    c.rect(5, 11, 6, 4, pot_c)
    c.rect(4, 10, 8, 2, pot_c)
    c.rect(4, 10, 8, 1, shade("white", -0.15))  # rim highlight
    c.rect(5, 14, 6, 1, shade("wood_lo", -0.2)) # base shadow

    if kind == 0:   # tall leafy
        c.rect(7, 3, 2, 8, P["leaf_lo"])
        c.rect(5, 4, 5, 4, P["leaf"])
        c.rect(4, 6, 8, 3, P["leaf_hi"])
        c.px(7, 3, P["leaf_hi"])

    elif kind == 1: # round bush
        c.disc(8, 7, 4, P["leaf"])
        c.disc(8, 7, 3, P["leaf_hi"])
        c.px(9, 6, P["white"])

    elif kind == 2: # cactus
        c.rect(7, 4, 2, 7, P["teal_lo"])
        c.rect(5, 6, 2, 3, P["teal_lo"])
        c.rect(9, 7, 2, 3, P["teal_lo"])
        c.vline(7, 4, 7, P["teal"])
        c.px(5, 6, P["teal_hi"])
        c.px(9, 7, P["teal_hi"])

    elif kind == 3: # hanging vine
        c.rect(6, 3, 4, 3, P["leaf"])
        c.rect(5, 5, 6, 2, P["leaf_hi"])
        # vines hanging
        for vx, phase in [(5, 0), (7, 1), (9, 0.5)]:
            for vy in range(7, 12):
                c.px(vx, vy, P["leaf"] if (vy + phase) % 2 == 0 else P["leaf_lo"])

    elif kind == 4: # flowering
        c.rect(7, 5, 2, 6, P["leaf_lo"])
        c.rect(5, 7, 6, 3, P["leaf"])
        # flowers
        c.disc(6, 5, 2, P["rose"])
        c.disc(10, 6, 2, P["amber"])
        c.px(6, 5, P["white"])
        c.px(10, 6, P["white"])

    elif kind == 5: # fern
        c.vline(8, 4, 7, P["leaf_lo"])
        for i in range(5):
            fry = 5 + i
            c.px(8 - i, fry, P["leaf"])
            c.px(8 + i, fry, P["leaf_hi"])

    elif kind == 6: # succulent
        c.disc(8, 9, 3, P["teal_lo"])
        c.disc(8, 9, 2, P["teal"])
        c.disc(8, 9, 1, P["teal_hi"])
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            lx = int(8 + 3 * math.cos(rad))
            ly = int(9 + 3 * math.sin(rad))
            c.px(lx, ly, P["leaf"])

    elif kind == 7: # bonsai
        c.rect(7, 8, 2, 3, P["wood_lo"])
        c.rect(5, 5, 6, 4, P["leaf"])
        c.rect(6, 4, 4, 2, P["leaf"])
        c.rect(4, 6, 3, 2, P["leaf_lo"])
        c.rect(9, 6, 3, 2, P["leaf_lo"])
        c.px(8, 4, P["leaf_hi"])

    elif kind == 8: # snake plant (tall spikes)
        for sx, sw in [(6, 2), (9, 2), (7, 2)]:
            c.rect(sx, 3, sw, 8, P["leaf"])
            c.vline(sx, 3, 8, P["leaf_hi"])
            c.vline(sx + sw - 1, 3, 8, P["leaf_lo"])

    elif kind == 9: # round cactus (barrel)
        c.disc(8, 8, 4, P["teal_lo"])
        c.disc(8, 8, 3, P["teal"])
        for i in range(-3, 4):
            c.px(8 + i, 8 - abs(i), P["teal_hi"])
        # spines
        for si in range(0, 360, 45):
            r2 = math.radians(si)
            c.px(int(8 + 4 * math.cos(r2)), int(8 + 4 * math.sin(r2)), P["paper"])

    elif kind == 10: # ivy trailing right
        c.rect(7, 4, 3, 5, P["leaf_lo"])
        for iy in range(5, 11):
            c.px(9 + (iy - 5), iy, P["leaf"])
            c.px(10 + (iy - 5), iy + 1, P["leaf_hi"])

    elif kind == 11: # palm / tropical
        c.rect(7, 6, 2, 5, P["wood"])
        for angle, length in [(210, 4), (170, 5), (130, 4), (250, 3), (290, 4)]:
            rad = math.radians(angle)
            for s in range(1, length + 1):
                lx = int(8 + s * math.cos(rad))
                ly = int(6 + s * math.sin(rad))
                if 0 <= lx < c.w and 0 <= ly < c.h:
                    c.px(lx, ly, P["leaf"] if s % 2 == 0 else P["leaf_hi"])

    elif kind == 12: # air plant (no soil, bare)
        for angle in range(0, 360, 40):
            rad = math.radians(angle)
            for s in range(2, 5):
                lx = int(8 + s * math.cos(rad))
                ly = int(8 + s * math.sin(rad))
                if 0 <= lx < c.w and 0 <= ly < c.h:
                    c.px(lx, ly, P["teal"] if s == 4 else P["leaf"])

    elif kind == 13: # mushroom cluster
        c.rect(7, 9, 2, 2, P["wood"])
        c.disc(8, 7, 3, P["rose"])
        c.px(8, 6, P["white"])
        c.px(7, 8, P["white"])
        c.px(9, 8, P["white"])
        # small mushroom next to
        c.px(11, 10, P["wood"])
        c.disc(11, 8, 2, P["amber"])
        c.px(11, 7, P["white"])

    elif kind == 14: # cherry blossom mini
        c.rect(7, 7, 2, 4, P["wood_lo"])
        c.rect(5, 4, 6, 4, P["rose"])
        c.disc(8, 5, 3, P["rose_hi"])
        for px_coords in [(6, 4), (10, 5), (7, 7), (9, 7)]:
            c.px(px_coords[0], px_coords[1], P["white"])

    else:            # 15 — zen rock garden (novelty)
        # rocks
        c.disc(6, 10, 2, P["metal"])
        c.disc(10, 11, 2, P["metal_hi"])
        c.disc(8, 9, 1, P["metal_lo"])
        # rake lines
        for rl in range(4, 14, 2):
            c.hline(3, rl + 1, 10, (P["paper"][0], P["paper"][1], P["paper"][2], 80))
        # tiny plant
        c.vline(12, 7, 3, P["leaf"])
        c.px(11, 7, P["leaf_hi"])
        c.px(13, 8, P["leaf_hi"])


def make_plants():
    sheet = Sheet(4, 4, 160, 160)
    for i in range(16):
        c = Canvas(16, 16)
        draw_plant(c, i)
        scaled = c.scaled(10)    # 160×160
        scaled = outline_alpha(scaled)
        sheet.place(scaled)
    path = os.path.join(OUT, "plants-spritesheet.webp")
    sheet.save(path, 640, 640)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 8. posters-spritesheet.webp  640×1280  frames 160×160  4×8=32 frames
# ─────────────────────────────────────────────────────────────────────────────
def draw_poster(c: Canvas, kind: int):
    """Draw one of 32 framed wall posters on a 16×16 logical canvas."""
    # Frame (consistent across all posters)
    frame_colors = [
        P["wood"], P["metal"], P["ink2"], P["amber_lo"],
        P["wood_lo"], P["metal_hi"], P["rose"], P["teal_lo"],
    ]
    fc = frame_colors[kind % len(frame_colors)]
    c.rect(0, 0, 16, 16, fc)    # frame body
    c.rect(1, 1, 14, 14, P["paper"])  # mat / inner
    c.rect(2, 2, 12, 12, P["white"])  # canvas

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
        c = Canvas(16, 16)
        draw_poster(c, i)
        scaled = c.scaled(10)    # 160×160
        scaled = outline_alpha(scaled)
        sheet.place(scaled)
    path = os.path.join(OUT, "posters-spritesheet.webp")
    sheet.save(path, 640, 1280)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 9. flowers-bloom-v2.webp  512×512  frames 128×128  4×4=16 frames
# ─────────────────────────────────────────────────────────────────────────────
def make_flowers_bloom():
    # Logical 13×13, scaled ×10 = 130×130 → fit in 128 cell
    # Actually: 128/10 = 12.8, so author at 12×12, scale ×10 = 120×120, center in 128
    LW = 12
    sheet = Sheet(4, 4, 128, 128)

    for f in range(16):
        t = f / 15.0   # 0..1 bloom progress
        c = Canvas(LW, LW)

        # stem
        stem_h = max(1, int(5 * min(t * 2, 1.0)))
        c.rect(5, LW - stem_h - 1, 2, stem_h + 1, P["leaf_lo"])
        c.px(5, LW - stem_h - 1, P["leaf"])

        # leaves (appear from t=0.2)
        if t > 0.2:
            lt = min(1.0, (t - 0.2) / 0.3)
            lw = max(1, int(3 * lt))
            c.rect(3, LW - 4, lw, 1, P["leaf"])
            c.rect(8, LW - 5, lw, 1, P["leaf"])

        # bud / bloom
        if t < 0.3:
            # tight bud
            bud_h = max(1, int(3 * (t / 0.3)))
            c.rect(5, LW - stem_h - 1 - bud_h, 2, bud_h, P["leaf"])
        elif t < 0.6:
            # opening: petals emerge
            pt = (t - 0.3) / 0.3
            petal_r = max(1, int(4 * pt))
            c.disc(6, LW - stem_h - 2 - petal_r, petal_r, P["rose"])
            c.px(6, LW - stem_h - 2 - petal_r, P["amber"])  # center
        elif t < 0.85:
            # full bloom
            pt = min(1.0, (t - 0.6) / 0.25)
            pr = max(1, int(4 + pt * 1))
            c.disc(6, LW - stem_h - pr - 1, pr, P["rose"])
            c.disc(6, LW - stem_h - pr - 1, max(1, pr - 2), P["amber_hi"])
            c.px(6, LW - stem_h - pr - 1, P["white"])
            # petal tips
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                tx2 = int(6 + (pr + 1) * math.cos(rad))
                ty2 = int(LW - stem_h - pr - 1 + (pr + 1) * math.sin(rad))
                if 0 <= tx2 < LW and 0 <= ty2 < LW:
                    c.px(tx2, ty2, P["rose_hi"])
        else:
            # gentle sway — full bloom with slight lean
            sway = int(math.sin(2 * math.pi * (t - 0.85) / 0.15) * 1)
            pr = 5
            bx = 6 + sway
            c.disc(bx, LW - stem_h - pr - 1, pr, P["rose"])
            c.disc(bx, LW - stem_h - pr - 1, pr - 2, P["amber_hi"])
            c.px(bx, LW - stem_h - pr - 1, P["white"])
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                tx2 = int(bx + (pr + 1) * math.cos(rad))
                ty2 = int(LW - stem_h - pr - 1 + (pr + 1) * math.sin(rad))
                if 0 <= tx2 < LW and 0 <= ty2 < LW:
                    c.px(tx2, ty2, P["rose_hi"])

        scaled = c.scaled(10)   # 120×120
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
