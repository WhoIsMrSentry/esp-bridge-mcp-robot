"""Nods settling -- yes."""
import math

from ..spec import Gesture


def _motion(p, e):   # nods settling -- yes
    return 0.0, math.sin(p * math.pi * 4) * 7 * e * (1.0 - 0.42 * p), 0.0, 1.0, 1.0


GESTURE = Gesture("nod", dur=1.4, motion=_motion)
