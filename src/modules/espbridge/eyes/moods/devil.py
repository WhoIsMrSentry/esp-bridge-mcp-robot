"""Evil glare + horns & a swaying tail."""
import math

from ..painters import glare
from ..spec import Mood


def _paint(d, x, y, w, h, r, ir):   # glare
    glare(d, x, y, w, h, 0.60, ir)


def _decor(d, W, H, now, ox=0.0, oy=0.0):  # two sharply-angled horns + a clean swaying tail -- "devil"
    d.polygon([(30, 21), (41, 18), (18, 2)], fill=1)          # left horn, angled up-left
    d.polygon([(W - 30, 21), (W - 41, 18), (W - 18, 2)], fill=1)  # right horn, angled up-right
    bx, by = W - 6, H - 1                                      # tail from the bottom-right corner
    tx, ty = W - 13 + math.sin(now * 2.2) * 3, H - 23          # tip sways gently
    d.line([(bx, by), (W - 16, H - 12), (tx, ty)], fill=1, width=2, joint="curve")
    d.polygon([(tx - 3, ty + 2), (tx + 3, ty + 2), (tx, ty - 5)], fill=1)  # spade barb


MOOD = Mood("devil", paint=_paint, decor=_decor)
