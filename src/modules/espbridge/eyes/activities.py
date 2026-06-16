"""ACTIVITIES -- a looping task status: a gaze pose + an overlay prop (from decor.py).
Each also wears a fitting face (ACT_MOOD). Use for an ongoing task; idle to stop."""
from __future__ import annotations

import math

from . import decor

ACTIVITIES = ("idle",                                                  # stop -- back to resting
              "thinking", "scanning", "searching", "processing",       # heads-down work
              "working", "editing", "debugging", "building", "testing", "deploying",
              "connecting", "listening", "waiting",                    # links & holding pattern
              "smoking")                                               # a chilled break
# each busy activity wears a fitting face; listening just stays attentive (neutral)
ACT_MOOD = {"thinking": "focused", "scanning": "neutral", "searching": "focused",
            "working": "focused", "editing": "chill", "processing": "focused",
            "debugging": "suspicious", "building": "focused", "testing": "focused",
            "deploying": "neutral", "connecting": "attentive", "listening": "neutral",
            "waiting": "bored", "smoking": "chill"}


def pose(act, now):
    """Eased gaze target (x, y) + height multiplier for a looping activity."""
    if act == "thinking":   # gaze up at the floating symbols, slow wander
        return math.sin(now * 0.7) * 7, -9 + math.sin(now * 0.4) * 2, 1.0
    if act == "scanning":   # step left->right then down a line, settling each stop
        line = now * 1.0
        return (int(line % 1.0 * 4) / 3 * 2 - 1) * 13, (int(line) % 3 - 1) * 5, 1.0
    if act == "searching":  # quick wandering glances -- scanning results
        return math.sin(now * 2.2) * 11 + math.sin(now * 1.3) * 5, math.sin(now * 1.7) * 5, 1.0
    if act == "working":    # heads-down smithing; the eyes brace + squint with each hammer blow
        hit = max(0.0, 1.0 - abs((now * 0.95) % 1.0 - 0.61) / 0.14)   # peaks at the strike (synced to hammer)
        return math.sin(now * 1.1) * 3, 3 + hit * 5, 0.85 - hit * 0.3
    if act == "listening":  # attentive, gently nodding along under the headphones
        return math.sin(now * 1.8) * 2, math.sin(now * 3.6) * 2, 1.0
    if act == "processing": # locked-in, computing -- a tight steady focus
        return math.sin(now * 1.4) * 4, -2 + math.sin(now * 0.7), 0.92
    if act == "debugging":  # eyes track the bug skittering along the bottom, squinting
        return math.sin(now * 1.4) * 12 + math.sin(now * 3.1) * 3, 5 + math.sin(now * 4.0), 0.9
    if act == "building":   # watching the cubes fly in and stack up in the centre
        return math.sin(now * 1.5) * 1.5, 4 + math.sin(now * 2.0) * 1.5, 0.92
    if act == "testing":    # eyeing the test tube bubbling away in the bottom-right corner
        return 5 + math.sin(now * 1.6) * 1.5, 5 + math.sin(now * 1.1) * 1.5, 0.95
    if act == "deploying":  # natural eyes, gaze drifting up to watch the launch
        return math.sin(now * 0.8) * 4, -3 + math.sin(now * 0.5) * 4, 1.0
    if act == "connecting": # expectant, waiting on the link
        return math.sin(now * 1.5) * 3, math.sin(now * 2.0) * 2, 1.0
    if act == "waiting":    # idle stare at the blinking prompt, the odd lazy drift
        return math.sin(now * 0.4) * 2, 2 + math.sin(now * 0.6), 1.0
    if act == "smoking":    # leaned back, gaze drifting lazily -- a break
        return math.sin(now * 0.5) * 5, -2 + math.sin(now * 0.3) * 3, 1.0
    return 0.0, 0.0, 1.0


# act name -> its looping prop, drawn from decor.py (activities without one just move the gaze)
OVERLAYS = {"thinking": decor.formulas, "searching": decor.magnifier,
            "working": decor.hammer, "editing": decor.typing,
            "debugging": decor.bug, "building": decor.cubes, "testing": decor.flask,
            "deploying": decor.rocket, "processing": decor.spinner,
            "connecting": decor.link_dots, "listening": decor.headphones,
            "waiting": decor.prompt, "smoking": decor.cigarette}
