"""
pixelkit — tiny pixel-art authoring toolkit for log8-office.

Philosophy: author at a small *logical* resolution (one cell == one art pixel),
then upscale with NEAREST to the target frame size so every pixel stays crisp.
Everything here is original code; assets it produces are CC0 (see LICENSE).

This module is also the heart of the "make your own assets" skill shipped with
log8-office: tweak PALETTE / the generator scripts and run `make` to re-skin the
whole office without touching any third-party art.
"""
from __future__ import annotations

import json
import math
import os
from PIL import Image, ImageDraw

# ----------------------------------------------------------------------------
# Palette — cozy pixel office. Hex strings -> RGBA tuples.
# ----------------------------------------------------------------------------
_HEX = {
    "clear":   "00000000",
    # neutrals / ink
    "ink":     "23283bff",   # near-black outline
    "ink2":    "3a405fff",
    "white":   "f4f6fbff",
    "paper":   "e9ecf5ff",
    "shadow":  "1a1d2a55",    # soft translucent shadow
    # walls / floor
    "wall":    "454b6eff",
    "wallhi":  "525980ff",
    "wall_lo": "373c5aff",
    "floor":   "6d5a48ff",
    "floor_hi":"7d6a56ff",
    "floor_lo":"5b4a3bff",
    "rug":     "3f6f6eff",
    "rug_hi":  "4f8483ff",
    # brand accents
    "blue":    "7c83ffff",
    "blue_hi": "9aa0ffff",
    "blue_lo": "5b62e0ff",
    "teal":    "42d6a4ff",
    "teal_hi": "5fe9bbff",
    "teal_lo": "2fb389ff",
    "amber":   "ffc24bff",
    "amber_hi":"ffd87aff",
    "amber_lo":"e09a2bff",
    "rose":    "ff6b8bff",
    "rose_hi": "ff90a8ff",
    "red":     "ff5a5aff",
    "red_lo":  "d23b3bff",
    # plants / wood
    "leaf":    "57a85bff",
    "leaf_hi": "73c777ff",
    "leaf_lo": "3f8043ff",
    "wood":    "a9774aff",
    "wood_hi": "c08e5eff",
    "wood_lo": "855a36ff",
    "soil":    "5a3f2eff",
    # device / metal
    "metal":   "8a90a8ff",
    "metal_hi":"a7adc4ff",
    "metal_lo":"6b7088ff",
    "glass":   "2b3350ff",
    "glasshi": "3c466bff",
    "screen":  "1d6f63ff",
    "screen2": "2a8f7eff",
    # skin / fur tones for guests & cats
    "skin1":   "f1c9a5ff", "skin2": "d9a884ff", "skin3": "b9825eff", "skin4": "8a5a3cff",
    "hair1":   "2c2230ff", "hair2": "6b4a2eff", "hair3": "b8732eff", "hair4": "9aa0bfff",
    "cat1":    "e8a14cff", "cat2": "5b5f73ff", "cat3": "f0f0f4ff", "cat4": "33373fff",
}
def _rgba(h: str):
    h = h.strip().lstrip("#")
    if len(h) == 6:
        h += "ff"
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))


PALETTE = {k: _rgba(v) for k, v in _HEX.items()}


# ----------------------------------------------------------------------------
# Theme system — re-skin the whole office from one config.
# A theme overrides entries in PALETTE in place. Only keys that already exist in
# the built-in palette are honoured (unknown keys are ignored) so themes can't
# break generators that look up a fixed set of names.
# ----------------------------------------------------------------------------
def apply_theme(theme) -> int:
    """Override PALETTE in place from a theme dict or a path to a theme JSON.

    `theme` may be:
      - a dict shaped like {"name": ..., "palette": {"wall": "#rrggbb", ...}},
      - a flat dict of {paletteKey: "#rrggbb", ...},
      - a path (str) to a theme JSON file.
    Hex strings are parsed exactly like the built-in palette (#rgb hex, optional
    alpha byte). Returns the number of palette keys actually overridden.
    """
    if isinstance(theme, str):
        theme = load_theme(theme)
    if not isinstance(theme, dict):
        return 0
    name = theme.get("name")
    colors = theme.get("palette", theme)   # support both nested and flat forms
    if not isinstance(colors, dict):
        return 0
    applied = 0
    for key, val in colors.items():
        if key not in PALETTE:
            continue                       # only override existing palette keys
        try:
            PALETTE[key] = _rgba(val)
        except (ValueError, IndexError, TypeError):
            continue                       # skip malformed hex, keep built-in
        applied += 1
    label = f" '{name}'" if name else ""
    print(f"[pixelkit] theme{label} applied — {applied} palette colours overridden")
    return applied


def load_theme(path: str) -> dict:
    """Load a theme JSON. Path is absolute or relative to assets-gen/."""
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _auto_apply_env_theme():
    """If LOG8_THEME is set, apply that theme at import time."""
    env = os.environ.get("LOG8_THEME")
    if not env:
        return
    try:
        apply_theme(env)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[pixelkit] LOG8_THEME '{env}' could not be applied: {exc}")


_auto_apply_env_theme()


def shade(name: str, amt: float):
    """Return a darker(<0)/lighter(>0) RGBA of a palette colour. amt in [-1,1]."""
    r, g, b, a = PALETTE[name]
    if amt >= 0:
        r = int(r + (255 - r) * amt); g = int(g + (255 - g) * amt); b = int(b + (255 - b) * amt)
    else:
        f = 1 + amt
        r = int(r * f); g = int(g * f); b = int(b * f)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), a)


# ----------------------------------------------------------------------------
# Canvas — a small logical-pixel image with art helpers.
# ----------------------------------------------------------------------------
class Canvas:
    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def _col(self, c):
        return PALETTE[c] if isinstance(c, str) else c

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((int(x), int(y)), self._col(c))

    def rect(self, x, y, w, h, c):
        c = self._col(c)
        self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)

    def frame(self, x, y, w, h, c):
        c = self._col(c)
        self.d.rectangle([x, y, x + w - 1, y + h - 1], outline=c)

    def rrect(self, x, y, w, h, c, r=1):
        """rounded-corner filled rect (chamfered, pixel style)."""
        c = self._col(c)
        self.d.rectangle([x + r, y, x + w - 1 - r, y + h - 1], fill=c)
        self.d.rectangle([x, y + r, x + w - 1, y + h - 1 - r], fill=c)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c):
        self.d.line([x0, y0, x1, y1], fill=self._col(c))

    def ellipse(self, x, y, w, h, c, outline=None):
        self.d.ellipse([x, y, x + w - 1, y + h - 1], fill=self._col(c),
                       outline=self._col(outline) if outline else None)

    def disc(self, cx, cy, r, c):
        self.ellipse(cx - r, cy - r, 2 * r + 1, 2 * r + 1, c)

    def blit(self, other: "Canvas", x, y):
        self.img.alpha_composite(other.img, (int(x), int(y)))

    def copy(self):
        c = Canvas(self.w, self.h)
        c.img = self.img.copy()
        c.d = ImageDraw.Draw(c.img)
        return c

    def scaled(self, factor: int):
        return self.img.resize((self.w * factor, self.h * factor), Image.NEAREST)


def outline_alpha(img: Image.Image, color=None, width: int = 1) -> Image.Image:
    """Add a 1px (logical) hard outline around opaque pixels — classic pixel look."""
    if color is None:
        color = PALETTE["ink"]
    px = img.load()
    w, h = img.size
    out = img.copy()
    op = out.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0:
                touch = False
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] > 128:
                        touch = True
                        break
                if touch:
                    op[x, y] = color
    return out


# ----------------------------------------------------------------------------
# Sheet packer — place frames into a grid, export at exact target size.
# ----------------------------------------------------------------------------
class Sheet:
    """A spritesheet built from logical-resolution frames upscaled to cell size."""

    def __init__(self, cols: int, rows: int, cell_w: int, cell_h: int):
        self.cols, self.rows = cols, rows
        self.cw, self.ch = cell_w, cell_h
        self.img = Image.new("RGBA", (cols * cell_w, rows * cell_h), (0, 0, 0, 0))
        self._i = 0

    def place(self, frame_img: Image.Image, index: int | None = None,
              align="center", ox=0, oy=0):
        if index is None:
            index = self._i
            self._i += 1
        cx = (index % self.cols) * self.cw
        cy = (index // self.cols) * self.ch
        fw, fh = frame_img.size
        if align == "center":
            px = cx + (self.cw - fw) // 2 + ox
            py = cy + (self.ch - fh) // 2 + oy
        elif align == "bottom":
            px = cx + (self.cw - fw) // 2 + ox
            py = cy + (self.ch - fh) + oy
        else:  # topleft
            px, py = cx + ox, cy + oy
        self.img.alpha_composite(frame_img, (px, py))
        return index

    def place_canvas(self, canvas: Canvas, factor: int, **kw):
        return self.place(canvas.scaled(factor), **kw)

    def save(self, path: str, target_w: int | None = None, target_h: int | None = None):
        img = self.img
        if target_w and target_h and (img.size != (target_w, target_h)):
            img = img.resize((target_w, target_h), Image.NEAREST)
        _save(img, path)


def _save(img: Image.Image, path: str):
    if path.lower().endswith(".webp"):
        img.save(path, "WEBP", lossless=True, quality=100, method=6)
    else:
        img.save(path)


def save_image(img: Image.Image, path: str, target_w=None, target_h=None):
    if target_w and target_h and img.size != (target_w, target_h):
        img = img.resize((target_w, target_h), Image.NEAREST)
    _save(img, path)


def save_canvas(canvas: Canvas, factor: int, path: str, target_w=None, target_h=None):
    save_image(canvas.scaled(factor), path, target_w, target_h)


# ----------------------------------------------------------------------------
# Small helpers shared by generators
# ----------------------------------------------------------------------------
def ease(t: float) -> float:
    """smoothstep 0..1"""
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def wobble(i: int, n: int, amp: float = 1.0, phase: float = 0.0) -> float:
    """sine in art-pixels for a frame i of n."""
    return amp * math.sin(2 * math.pi * (i / n) + phase)


def soft_shadow(w: int, h: int, ew: int, eh: int, color=None) -> Image.Image:
    """A standalone soft elliptical ground shadow image (logical res)."""
    if color is None:
        color = PALETTE["shadow"]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2
    d.ellipse([cx - ew // 2, cy - eh // 2, cx + ew // 2, cy + eh // 2], fill=color)
    return img
