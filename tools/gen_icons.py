"""Generate PWA icons for Kickoff. Pure Pillow, no external assets."""
import math
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
os.makedirs(OUT, exist_ok=True)

TEAL = (15, 118, 110, 255)   # #0f766e
WHITE = (255, 255, 255, 255)


def make(size, name):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # rounded-square background (generous padding keeps it maskable-safe)
    inset = int(size * 0.04)
    d.rounded_rectangle(
        [inset, inset, size - inset - 1, size - inset - 1],
        radius=int(size * 0.22),
        fill=TEAL,
    )

    # white progress ring
    pad = int(size * 0.29)
    width = max(6, int(size * 0.055))
    d.arc([pad, pad, size - pad, size - pad], start=0, end=360, fill=WHITE, width=width)

    # marker dot on the ring at about the 1-o'clock position
    cx = cy = size / 2
    radius = (size - 2 * pad) / 2
    angle = math.radians(-42)
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    dot = max(10, int(size * 0.085))
    d.ellipse([x - dot / 2, y - dot / 2, x + dot / 2, y + dot / 2], fill=WHITE)

    path = os.path.join(OUT, name)
    im.save(path)
    print("wrote", path)


make(192, "icon-192.png")
make(512, "icon-512.png")
make(180, "icon-180.png")  # apple-touch-icon

# Browser tab favicon: reuse the high-res icon and let Pillow rasterize sizes.
src = os.path.join(OUT, "icon-512.png")
Image.open(src).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote favicon.ico")
