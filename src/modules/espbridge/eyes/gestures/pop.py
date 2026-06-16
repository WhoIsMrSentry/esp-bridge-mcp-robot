"""Eyes pop wide for a beat."""
from ..spec import Gesture


def _motion(p, e):
    return 0.0, 0.0, 0.0, 1.0 + 0.35 * e, 1.0 + 0.35 * e


GESTURE = Gesture("pop", dur=0.5, motion=_motion)
