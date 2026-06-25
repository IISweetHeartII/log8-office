"""
gen_cats.py — background-removed pixel sprites of the 8 real agent avatars.

Each agent (rosie / navi / kkami / cheese / hermes / buffett / luna / gamjaring)
has its own AI-made cat avatar. This cuts out the subject (rembg), pixelates it,
and bottom-anchors it so the cat stands on the office floor as a real character
(transparent background, gentle idle bob). All distinct, all faithful.

Deps (only for regenerating): pip install pillow rembg onnxruntime
Source images: ~/Pictures/openclaw-cat-avatars/<name>.{png,jpg}
Output:
  out/cat_<name>.webp       256x128, 64x64 frames, 4x2 = 8-frame idle bob
  out/cat_<name>_role.png   128x64 cutout portrait (guest-list avatar)
"""
from __future__ import annotations
import os, math
from PIL import Image
import pixelkit as pk
from rembg import remove, new_session

OUT = os.path.join(os.path.dirname(__file__), "out")
SRC = os.path.expanduser("~/Pictures/openclaw-cat-avatars")
FW = 64                       # frame size (office renders at scale 1.5 ≈ 96px)
FIT = 60                      # max sprite extent inside the frame (leaves bob room)
COLORS = 30                   # palette size for the pixel-art look
ORDER = ["rosie", "navi", "kkami", "cheese", "hermes", "buffett", "luna", "gamjaring"]
_SESS = new_session("u2net")


def _find(name):
    for f in sorted(os.listdir(SRC)):
        if f.lower().startswith(name.lower()) and f.lower().rsplit(".", 1)[-1] in ("png", "jpg", "jpeg", "webp"):
            return os.path.join(SRC, f)
    raise FileNotFoundError(f"avatar for {name} not found in {SRC}")


def cutout_sprite(name):
    """rembg cut-out → tight-cropped, pixelated RGBA sprite that fits in FIT×FIT."""
    im = Image.open(_find(name)).convert("RGBA")
    cut = remove(im, session=_SESS)            # transparent background
    bbox = cut.getbbox()
    if bbox:
        cut = cut.crop(bbox)
    w, h = cut.size
    scale = FIT / max(w, h)
    pw, ph = max(1, round(w * scale)), max(1, round(h * scale))
    small = cut.resize((pw, ph), Image.LANCZOS)
    # quantize RGB, keep a crisp thresholded alpha
    alpha = small.getchannel("A").point(lambda a: 255 if a > 110 else 0)
    rgb = small.convert("RGB").quantize(colors=COLORS, method=Image.FASTOCTREE).convert("RGBA")
    rgb.putalpha(alpha)
    return pk.outline_alpha(rgb, color=pk.PALETTE["ink"])


def frame(sprite, i, n=8):
    """Bottom-anchored placement in a 64x64 frame with a gentle vertical bob."""
    f = Image.new("RGBA", (FW, FW), (0, 0, 0, 0))
    bob = round(1.4 * math.sin(2 * math.pi * i / n))
    x = (FW - sprite.width) // 2
    y = FW - sprite.height + bob - 1            # feet at the bottom edge
    f.alpha_composite(sprite, (max(0, x), max(0, min(y, FW - sprite.height))))
    return f


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = {}
    for name in ORDER:
        spr = cutout_sprite(name)
        sheet = pk.Sheet(4, 2, FW, FW)
        for i in range(8):
            sheet.place(frame(spr, i), index=i, align="topleft")
        sheet.save(os.path.join(OUT, f"cat_{name}.webp"), FW * 4, FW * 2)   # 256x128
        checks[f"cat_{name}.webp"] = (FW * 4, FW * 2)
        # portrait: cutout centered in 128x64 (bottom-anchored)
        port = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
        big = cutout_sprite(name)
        port.alpha_composite(big, ((128 - big.width) // 2, max(0, 64 - big.height)))
        pk.save_image(port, os.path.join(OUT, f"cat_{name}_role.png"), 128, 64)
        checks[f"cat_{name}_role.png"] = (128, 64)

    ok = True
    for fn, exp in checks.items():
        got = Image.open(os.path.join(OUT, fn)).size
        good = got == exp; ok = ok and good
        print(f"{'PASS' if good else 'FAIL'} {fn} {got} exp {exp}")
    print("ALL PASS" if ok else "FAILURES")


if __name__ == "__main__":
    main()
