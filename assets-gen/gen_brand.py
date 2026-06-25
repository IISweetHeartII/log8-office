"""
gen_brand.py — app icon + README covers, composed ONLY from log8-office's own
CC0 assets (the generated office_bg + sprites). No third-party art.

Outputs:
  out/icon-1024.png + out/icon-256.png/128/64/32 + out/icon.ico   (Tauri app icon)
  out/readme-cover-1.png  (preview banner, 1270x718)
  out/readme-cover-2.png  (cover w/ title, 1606x1216)
  out/office-preview.png   (1359x1220)
"""
from __future__ import annotations
import os
from PIL import Image, ImageDraw, ImageFont
import pixelkit as pk

OUT = os.path.join(os.path.dirname(__file__), "out")


def _frame(path, fw, fh, idx=0):
    im = Image.open(os.path.join(OUT, path)).convert("RGBA")
    cols = im.width // fw
    x = (idx % cols) * fw
    y = (idx // cols) * fh
    return im.crop((x, y, x + fw, y + fh))


def _font(size):
    for p in ("/System/Library/Fonts/SFNSRounded.ttf",
              "/System/Library/Fonts/SFNS.ttf",
              "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/Library/Fonts/Arial.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Composed office scene (the heart of the covers)
# ---------------------------------------------------------------------------
def build_scene() -> Image.Image:
    scene = Image.open(os.path.join(OUT, "office_bg_small.webp")).convert("RGBA")  # 1280x720
    W, H = scene.size

    def paste(img, cx, by, scale=1.0):
        if scale != 1.0:
            img = img.resize((int(img.width * scale), int(img.height * scale)), Image.NEAREST)
        scene.alpha_composite(img, (int(cx - img.width / 2), int(by - img.height)))

    # furniture & cast, roughly how the room reads
    paste(Image.open(os.path.join(OUT, "sofa-shadow-v1.png")).convert("RGBA"), 250, 660, 0.9)
    paste(Image.open(os.path.join(OUT, "sofa-idle-v3.png")).convert("RGBA"), 250, 650, 0.9)
    paste(Image.open(os.path.join(OUT, "desk-v3.webp")).convert("RGBA"), 980, 660, 1.4)
    paste(_frame("coffee-machine-v3-grid.webp", 230, 230, 40), 1140, 470, 0.7)
    paste(Image.open(os.path.join(OUT, "plants-spritesheet.webp")).convert("RGBA").crop((0, 0, 160, 160)), 120, 660, 1.0)
    paste(_frame("serverroom-spritesheet.webp", 180, 251, 0), 1190, 690, 0.55)
    # star mascot (idle) centre-stage
    paste(_frame("star-idle-v5.png", 256, 256, 0), 560, 660, 1.1)
    # a couple of cats
    paste(_frame("cats-spritesheet.webp", 160, 160, 0), 700, 660, 0.7)
    paste(_frame("cats-spritesheet.webp", 160, 160, 4), 410, 655, 0.7)
    # a guest walking in
    g = _frame("guest_anim_1.webp", 32, 32, 0)
    paste(g, 830, 655, 2.2)
    return scene


def fit(img: Image.Image, w: int, h: int, bg=(20, 21, 32, 255)) -> Image.Image:
    """contain-fit img into w x h on a brand-dark backdrop."""
    canvas = Image.new("RGBA", (w, h), bg)
    r = min(w / img.width, h / img.height)
    rs = img.resize((max(1, int(img.width * r)), max(1, int(img.height * r))), Image.LANCZOS)
    canvas.alpha_composite(rs, ((w - rs.width) // 2, (h - rs.height) // 2))
    return canvas


def save_jpg_like(img: Image.Image, name: str):
    """We output PNG (lossless, no jpg artefacts on pixel art); README refs are renamed to .png by caller."""
    img.convert("RGB").save(os.path.join(OUT, name))


# ---------------------------------------------------------------------------
# App icon
# ---------------------------------------------------------------------------
def build_icon(size_logical=64) -> pk.Canvas:
    c = pk.Canvas(size_logical, size_logical)
    s = size_logical
    # rounded brand tile background (gradient blue -> indigo)
    for y in range(s):
        t = y / s
        col = pk.shade("blue", 0.18 - 0.45 * t)
        c.hline(0, y, s, col)
    # round the corners (cut)
    r = s // 6
    for dx in range(r):
        for dy in range(r):
            if dx * dx + dy * dy > r * r:
                for (cx, cy) in ((dx, dy), (s - 1 - dx, dy), (dx, s - 1 - dy), (s - 1 - dx, s - 1 - dy)):
                    c.px(cx, cy, "clear")
    # mascot head: rounded dark screen-face with eyes + smile + antenna star
    bw, bh = int(s * 0.5), int(s * 0.42)
    bx, by = (s - bw) // 2, int(s * 0.34)
    # body plate (lighter blue)
    c.rrect(bx, by, bw, bh, pk.shade("blue_hi", 0.05), r=3)
    c.frame(bx, by, bw, bh, "ink")
    # screen
    sx, sy, sw, sh = bx + 3, by + 3, bw - 6, bh - 7
    c.rrect(sx, sy, sw, sh, "glass", r=2)
    # eyes + smile
    eye = max(1, s // 24)
    c.disc(sx + sw // 3, sy + sh // 2, eye, "teal_hi")
    c.disc(sx + 2 * sw // 3, sy + sh // 2, eye, "teal_hi")
    c.hline(sx + sw // 3, sy + sh - 3, sw // 3, "teal_hi")
    # antenna + star
    ax = s // 2
    c.vline(ax, by - 4, 4, "ink")
    c.disc(ax, by - 6, 2, "amber")
    c.px(ax, by - 9, "amber_hi")
    return c


def build_icon_master() -> Image.Image:
    c = build_icon(64)
    img = pk.outline_alpha(c.scaled(16))  # 1024
    return img


def main():
    os.makedirs(OUT, exist_ok=True)

    # ---- covers ----
    scene = build_scene()
    save_jpg_like(fit(scene, 1270, 718), "readme-cover-1.png")
    save_jpg_like(fit(scene, 1359, 1220), "office-preview.png")

    # cover-2: scene + title band
    cover2 = fit(scene, 1606, 1216)
    d = ImageDraw.Draw(cover2)
    # darken top band
    band = Image.new("RGBA", (1606, 300), (15, 16, 26, 180))
    cover2.alpha_composite(band, (0, 0))
    d.text((70, 70), "log8 office", font=_font(140), fill=(244, 246, 251, 255))
    d.text((76, 220), "free · multilingual · agent-ready pixel office",
           font=_font(46), fill=(154, 160, 191, 255))
    save_jpg_like(cover2, "readme-cover-2.png")

    # ---- app icon ----
    master = build_icon_master()  # 1024
    assert master.size == (1024, 1024), master.size
    master.save(os.path.join(OUT, "icon-1024.png"))
    for sz in (256, 128, 64, 32):
        master.resize((sz, sz), Image.NEAREST).save(os.path.join(OUT, f"icon-{sz}.png"))
    # multi-size .ico
    master.resize((256, 256), Image.NEAREST).save(
        os.path.join(OUT, "icon.ico"),
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

    # verify
    checks = {
        "readme-cover-1.png": (1270, 718),
        "office-preview.png": (1359, 1220),
        "readme-cover-2.png": (1606, 1216),
        "icon-1024.png": (1024, 1024),
        "icon-256.png": (256, 256),
        "icon-128.png": (128, 128),
        "icon-64.png": (64, 64),
        "icon-32.png": (32, 32),
    }
    allok = True
    for name, exp in checks.items():
        got = Image.open(os.path.join(OUT, name)).size
        ok = got == exp
        allok = allok and ok
        print(f"{'PASS' if ok else 'FAIL'} {name} {got} exp {exp}")
    print("ICO frames:", Image.open(os.path.join(OUT, "icon.ico")).size)
    print("ALL PASS" if allok else "FAILURES")


if __name__ == "__main__":
    main()
