"""Eyes squeeze to a wary slit, then ease open."""
from ..spec import Gesture


def _motion(p, e):
    return 0.0, 0.0, 0.0, 1.0, 1.0 - 0.6 * e


GESTURE = Gesture("squint", dur=1.3, motion=_motion)
