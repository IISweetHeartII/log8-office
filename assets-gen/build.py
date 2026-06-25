"""
build.py — one-command CC0 asset pipeline for log8-office.

Usage:
    python3 build.py [--theme NAME_or_PATH] [--install] [--cats]

  --theme NAME   apply a theme before generating. NAME resolves to
                 themes/NAME.json; a path (containing '/' or ending '.json')
                 is used as-is. Sets LOG8_THEME for the generator subprocesses.
  --install      after generating, copy out/* to their in-repo destinations
                 (frontend/, assets/room-reference.*). NEVER overwrites the
                 named cat sprites (cat_*.webp / cat_*_role.png) which only
                 gen_cats.py produces.
  --cats         also run gen_cats.py (needs rembg + onnxruntime + source
                 avatars — excluded by default).

Generators run via subprocess so each gets a fresh interpreter that re-reads
LOG8_THEME at import. gen_office_bg runs LAST so its fine 320x180 background
always wins over the coarse one gen_scene.py also emits.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
ROOT = os.path.dirname(HERE)                       # repo root
FRONTEND = os.path.join(ROOT, "frontend")
ASSETS = os.path.join(ROOT, "assets")

# Order matters: gen_office_bg LAST so its fine office_bg wins over gen_scene's.
GENERATORS = [
    "gen_scene.py",
    "gen_furniture.py",
    "gen_decor.py",
    "gen_star.py",
    "gen_brand.py",
    "gen_office_bg.py",     # canonical office_bg — must run after gen_scene
]

# Files gen_cats.py owns — install must never clobber these from out/.
def _is_named_cat(fname: str) -> bool:
    return (fname.startswith("cat_") and
            (fname.endswith(".webp") or fname.endswith("_role.png")))

# Install destinations. Most generated files land in frontend/ by name; the
# room-reference pair also goes to assets/. Brand covers/icons have no checked-in
# home, so they are skipped unless a same-named file already exists there.
ROOM_REFERENCE = {"room-reference.png", "room-reference.webp"}
BRAND_ONLY = {
    "icon-1024.png", "icon-256.png", "icon-128.png", "icon-64.png",
    "icon-32.png", "icon.ico", "readme-cover-1.png", "readme-cover-2.png",
    "office-preview.png",
}


def resolve_theme(theme: str | None) -> str | None:
    """Resolve a theme NAME or path to an absolute themes JSON path."""
    if not theme:
        return None
    if "/" in theme or theme.endswith(".json"):
        path = theme if os.path.isabs(theme) else os.path.join(HERE, theme)
    else:
        path = os.path.join(HERE, "themes", f"{theme}.json")
    if not os.path.exists(path):
        sys.exit(f"build: theme not found: {path}")
    return path


def run_generators(env, generators):
    print("Generating assets into out/ …\n")
    for gen in generators:
        print(f"── {gen} " + "─" * (50 - len(gen)))
        r = subprocess.run([sys.executable, gen], cwd=HERE, env=env)
        if r.returncode != 0:
            sys.exit(f"build: {gen} failed (exit {r.returncode})")
        print()


def install():
    """Copy out/* to their in-repo destinations, protecting cat sprites."""
    copied, skipped = [], []
    for fname in sorted(os.listdir(OUT)):
        src = os.path.join(OUT, fname)
        if not os.path.isfile(src):
            continue
        if _is_named_cat(fname):
            skipped.append((fname, "named-cat (gen_cats only)"))
            continue
        if fname in BRAND_ONLY:
            # only install if a same-named destination already exists somewhere
            placed = False
            for dest_dir in (FRONTEND, ASSETS, ROOT):
                dst = os.path.join(dest_dir, fname)
                if os.path.exists(dst):
                    shutil.copy2(src, dst)
                    copied.append(os.path.relpath(dst, ROOT))
                    placed = True
            if not placed:
                skipped.append((fname, "brand asset, no checked-in destination"))
            continue
        # room-reference goes to assets/ (and frontend/ if present there)
        if fname in ROOM_REFERENCE:
            dst = os.path.join(ASSETS, fname)
            os.makedirs(ASSETS, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(os.path.relpath(dst, ROOT))
            continue
        # everything else: frontend/
        dst = os.path.join(FRONTEND, fname)
        shutil.copy2(src, dst)
        copied.append(os.path.relpath(dst, ROOT))
    return copied, skipped


def main():
    ap = argparse.ArgumentParser(description="Build log8-office CC0 assets.")
    ap.add_argument("--theme", help="theme NAME (themes/NAME.json) or path")
    ap.add_argument("--install", action="store_true",
                    help="copy generated assets into the app")
    ap.add_argument("--cats", action="store_true",
                    help="also run gen_cats.py (needs rembg + source avatars)")
    args = ap.parse_args()

    env = os.environ.copy()
    theme_path = resolve_theme(args.theme)
    if theme_path:
        env["LOG8_THEME"] = theme_path
        print(f"Theme: {os.path.relpath(theme_path, HERE)}\n")
    else:
        env.pop("LOG8_THEME", None)
        print("Theme: default (built-in palette)\n")

    gens = list(GENERATORS)
    if args.cats:
        gens.append("gen_cats.py")

    run_generators(env, gens)

    print("=" * 56)
    out_files = sorted(f for f in os.listdir(OUT)
                       if os.path.isfile(os.path.join(OUT, f)))
    print(f"Generated {len(out_files)} files in out/")

    if args.install:
        copied, skipped = install()
        print(f"\nInstalled {len(copied)} files:")
        for c in copied:
            print(f"  + {c}")
        if skipped:
            print(f"\nSkipped {len(skipped)} files (by design):")
            for name, why in skipped:
                print(f"  - {name}  ({why})")
    else:
        print("\n(not installed — pass --install to copy into the app)")
    print("=" * 56)
    print("DONE")


if __name__ == "__main__":
    main()
