#!/usr/bin/env python3
"""Convert source photos to the two webp sizes the site uses.

Usage: python photos.py <source-folder>

Files are matched by order after sorting on filename, and renamed to the
names in TARGETS. Each one is written twice: <name>.webp at 1600 px wide
and <name>-800.webp at 800 px wide, the pair that img() in build.py expects.
"""
import os, sys
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), "..", "site", "images")
WIDTHS = [(1600, "{}.webp"), (800, "{}-800.webp")]
QUALITY = 82

TARGETS = [
    "breakfast-bacsilog",
    "breakfast-tosilog",
    "breakfast-american",
    "breakfast-tosilog-mango",
]

def convert(src, name):
    im = Image.open(src)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    for width, pattern in WIDTHS:
        w = min(width, im.width)
        h = round(im.height * w / im.width)
        out = os.path.join(OUT, pattern.format(name))
        im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=QUALITY, method=6)
        print("wrote", os.path.basename(out), f"{w}x{h}", f"{os.path.getsize(out) // 1024} KB")

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    folder = sys.argv[1]
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    if len(files) != len(TARGETS):
        sys.exit(f"expected {len(TARGETS)} images in {folder}, found {len(files)}: {files}")
    os.makedirs(OUT, exist_ok=True)
    for src, name in zip(files, TARGETS):
        print(f"{src} -> {name}")
        convert(os.path.join(folder, src), name)

if __name__ == "__main__":
    main()
