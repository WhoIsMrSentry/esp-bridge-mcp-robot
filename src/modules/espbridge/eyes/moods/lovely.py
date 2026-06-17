"""Little hearts & sparkles scattered around -- smitten."""
import math

from ..painters import sparkle
from ..spec import Mood


def _heart(d, cx, cy, s):   # smooth parametric heart centred at (cx, cy), ~s px wide
    sc = s / 33.0
    pts = [(cx + 16 * math.sin(t) ** 3 * sc,
            cy - (13 * math.cos(t) - 5 * math.cos(2 * t)
                  - 2 * math.cos(3 * t) - math.cos(4 * t)) * sc + 2 * sc)
           for t in (i * math.pi / 18 for i in range(36))]
    d.polygon(pts, fill=1)


def _decor(d, W, H, now, ox=0.0, oy=0.0):  # little hearts & sparkles scattered around -- smitten
    spots = ((0.50, 0.07), (0.24, 0.14), (0.76, 0.12), (0.05, 0.40), (0.95, 0.42),
             (0.07, 0.74), (0.93, 0.72), (0.28, 0.90), (0.72, 0.88))
    for i, (fx, fy) in enumerate(spots):
        even = i % 2 == 0
        (_heart if even else sparkle)(d, fx * W, fy * H, 9 if even else 4)


MOOD = Mood("lovely", dw=2, dh=2, decor=_decor)
