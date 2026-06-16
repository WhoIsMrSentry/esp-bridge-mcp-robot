"""Droopy slits + drifting Zzz."""
from ..painters import lids
from ..spec import Mood


def _paint(d, x, y, w, h, r, ir):   # droopy slits
    lids(d, x, y, w, h, 0.5, 0.82)


def _decor(d, W, H, now, ox=0.0, oy=0.0):  # "z z Z" drift up and grow -- sleepy
    for i in range(3):
        t = (now * 0.5 + i / 3) % 1.0
        x, y = W // 2 + 16 + i * 6 + int(ox), H // 2 - 2 - t * 22
        d.text((x, y), "Z" if i == 2 else "z", fill=1)


MOOD = Mood("sleepy", dh=-20, paint=_paint, decor=_decor)
