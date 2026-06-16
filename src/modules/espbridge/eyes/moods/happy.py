"""Cheeks-up smile."""
from ..spec import Mood


def _paint(d, x, y, w, h, r, ir):   # cheeks-up smile: arc carved into the bottom
    d.ellipse([x - w * 0.25, y + h * 0.45, x + w * 1.25, y + h * 2.1], fill=0)


MOOD = Mood("happy", paint=_paint)
