"""Eyes roll in a full circle."""
import math

from ..spec import Gesture


def _motion(p, e):
    return math.cos(p * math.pi * 2) * 11 * e, math.sin(p * math.pi * 2) * 7 * e, 0.0, 1.0, 1.0


GESTURE = Gesture("roll", dur=0.9, motion=_motion)
