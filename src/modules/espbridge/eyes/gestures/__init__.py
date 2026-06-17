"""One-shot moves. Add one: drop `<name>.py` here exposing `GESTURE = Gesture(...)`, then slot
its name into the curated order below. A gesture is either a `blink` (lid-only) or a `motion`."""
from .._registry import load

# -- curated order; blinks first, then enveloped motions --
_ORDER = (
    # blinks (lid-only)
    "blink", "double_blink", "wink_left", "wink_right",
    # gaze glances + directional blinks + sweeps
    "look_left", "look_right", "look_up", "look_down", "blink_down", "blink_up",
    "scan", "scan_sweep",
    # affirm / deny / acknowledge
    "nod", "refuse", "acknowledge",
    # expressive wobbles
    "laugh", "excited", "roll", "shiver", "pop", "squint", "cross_eyes",
)

GESTURES = load(__name__, _ORDER, "GESTURE")   # name -> Gesture, curated order (errors on a stray file)
