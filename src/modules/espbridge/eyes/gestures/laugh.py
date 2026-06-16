"""Bouncing chuckle -- the eyes hop and squash."""
import math

from ..spec import Gesture


def _motion(p, e):
    return 0.0, -abs(math.sin(p * math.pi * 4)) * 7 * e, 0.0, 1.0, 1.0 - 0.4 * e


GESTURE = Gesture("laugh", dur=1.4, motion=_motion)
