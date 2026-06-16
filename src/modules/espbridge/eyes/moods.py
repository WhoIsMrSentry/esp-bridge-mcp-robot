"""MOODS -- static expressions: a size delta + optional lid painter + optional decor.
Painters carve lids (fill=0) onto a rounded-rect eye. Adding one = a line in MOODS."""
from __future__ import annotations

from . import decor


# ---- shared lid shapes carved (fill=0) onto an eye drawn as a rounded rect ------
def _brow(d, x, y, w, h, inner, outer, is_right):
    """Slanted top lid: covers to inner*h toward the nose, outer*h on the outside."""
    rt = y + h * (outer if is_right else inner)
    lt = y + h * (inner if is_right else outer)
    d.polygon([(x - 2, y - 2), (x + w + 2, y - 2), (x + w + 2, rt), (x - 2, lt)], fill=0)


def _glare(d, x, y, w, h, depth, is_right):
    """Inner-down brow: a triangle whose tip drops to depth*h toward the nose."""
    tip = (x - 2, y + h * depth) if is_right else (x + w + 2, y + h * depth)
    d.polygon([(x - 2, y - 2), (x + w + 2, y - 2), tip], fill=0)


def _lids(d, x, y, w, h, top=0.0, bottom=1.0):
    """Flat lids: cover down to top*h and up from bottom*h."""
    if top:
        d.rectangle([x - 1, y - 1, x + w + 1, y + h * top], fill=0)
    if bottom < 1:
        d.rectangle([x - 1, y + h * bottom, x + w + 1, y + h + 1], fill=0)


# ---- painters: signature (d, x, y, w, h, r, is_right). Static -- no motion. -----
def _happy(d, x, y, w, h, r, ir):  # cheeks-up smile: arc carved into the bottom
    d.ellipse([x - w * 0.25, y + h * 0.45, x + w * 1.25, y + h * 2.1], fill=0)


def _sad(d, x, y, w, h, r, ir):       _brow(d, x, y, w, h, 0.30, 0.66, ir)  # downcast droop
def _tired(d, x, y, w, h, r, ir):     _brow(d, x, y, w, h, 0.38, 0.52, ir)  # hooded, peering out
def _worried(d, x, y, w, h, r, ir):   _brow(d, x, y, w, h, 0.02, 0.26, ir)  # raised inner brow
def _angry(d, x, y, w, h, r, ir):     _glare(d, x, y, w, h, 0.60, ir)       # glare
def _furious(d, x, y, w, h, r, ir):   _glare(d, x, y, w, h, 0.78, ir)       # rage (angry++)
def _bored(d, x, y, w, h, r, ir):     _lids(d, x, y, w, h, top=0.5)         # flat half-lids
def _focused(d, x, y, w, h, r, ir):   _lids(d, x, y, w, h, 0.24, 0.76)      # determined band
def _sleepy(d, x, y, w, h, r, ir):    _lids(d, x, y, w, h, 0.5, 0.82)       # droopy slits
def _despair(d, x, y, w, h, r, ir):   _lids(d, x, y, w, h, 0.42, 0.62)      # drained slit
def _attentive(d, x, y, w, h, r, ir): _lids(d, x, y, w, h, top=0.12)        # crisp top lid -- locked on
def _chill(d, x, y, w, h, r, ir):     _lids(d, x, y, w, h, top=0.45)        # heavy-lidded, mellow -- at ease


def _skeptical(d, x, y, w, h, r, ir):  # one eye narrowed+angled, the other barely lidded
    if ir:
        _lids(d, x, y, w, h, top=0.14)
    else:
        d.polygon([(x - 2, y - 2), (x + w + 2, y - 2),
                   (x + w + 2, y + h * 0.5), (x - 2, y + h * 0.66)], fill=0)


def _confused(d, x, y, w, h, r, ir):  # only the lower (right) eye squints
    if ir:
        _lids(d, x, y, w, h, top=0.28)


def _dumb(d, x, y, w, h, r, ir):  # punch a glint out of each eye
    g = max(2.0, w * 0.2)
    d.ellipse([x + w * 0.22, y + h * 0.2, x + w * 0.22 + g, y + h * 0.2 + g], fill=0)


def _dead(d, x, y, w, h, r, ir):  # KO -- an X carved across the eye
    lw = max(2, int(w * 0.16))
    d.line([x + 3, y + 3, x + w - 4, y + h - 4], fill=0, width=lw)
    d.line([x + w - 4, y + 3, x + 3, y + h - 4], fill=0, width=lw)


def _suspicious(d, x, y, w, h, r, ir): _lids(d, x, y, w, h, 0.40, 0.88)      # heavy slit + pinched bottom -- side-eye
def _zen(d, x, y, w, h, r, ir):        _lids(d, x, y, w, h, 0.46, 0.56)      # eyes softly shut -- a calm centered line


# spec (all optional): dw/dh size delta, tilt y-offset, sway (amp, speed) animated tilt,
# bias size skew, paint lid carver, decor extras, bright 0..255, bare no-eyes, still pin-gaze
MOODS = {
    # -- baseline & system --
    "neutral":     {},
    "alert":       {"dw": -18},                              # two upright bars -- attention
    "attentive":   {"dw": 2, "dh": 2, "paint": _attentive},  # leaned in, locked on -- "go ahead"
    "standby":     {"dw": -2, "dh": -24, "bright": 1},       # low dashes + dimmed panel -- low-power sleep

    # -- positive / warm --
    "happy":       {"paint": _happy},
    "lovely":      {"dw": 2, "dh": 2, "decor": decor.lovely},
    "kawaii":      {"dw": 2, "dh": 0, "decor": decor.kawaii},             # round eyes + blush below + twinkles
    "awe":         {"dw": 4, "dh": 14},                                  # huge open eyes -- pure wonder
    "cool":        {"bare": True, "decor": decor.cool},                  # just the aviators -- no eyes drawn

    # -- focus / calm --
    "focused":     {"paint": _focused},
    "zen":         {"dh": -2, "paint": _zen, "decor": decor.zen, "still": True},  # calmly shut + orbiting droplets -- in flow
    "wired":       {"dw": 2, "dh": 2, "decor": decor.coffee},            # caffeinated -- steaming mug
    "chill":       {"dh": -4, "paint": _chill},                          # heavy-lidded, mellow -- at ease

    # -- sad / anxious / low --
    "sad":         {"dw": -4, "dh": -6, "paint": _sad},                  # small + downcast
    "gloomy":      {"dw": -2, "dh": -4, "paint": _sad, "decor": decor.cloud},  # downcast + little rain cloud
    "worried":     {"dh": 2, "paint": _worried},                         # open eyes + concerned brow
    "nervous":     {"dw": -2, "paint": _worried, "decor": decor.sweat},  # anxious brow + sweat bead
    "despair":     {"dw": -8, "dh": -6, "paint": _despair},
    "scared":      {"dw": -10, "dh": -4},
    "tired":       {"paint": _tired},
    "sleepy":      {"dh": -20, "paint": _sleepy, "decor": decor.sleep},  # droopy slits + drifting Zzz

    # -- angry / wary --
    "angry":       {"paint": _angry},
    "furious":     {"dw": 2, "dh": 2, "paint": _furious, "decor": decor.vein},  # rage + popping vein
    "devil":       {"paint": _angry, "decor": decor.devil},              # evil glare + horns & tail
    "suspicious":  {"dw": -2, "paint": _suspicious},                     # narrow slit eyes -- side-eye
    "skeptical":   {"paint": _skeptical},

    # -- dazed / goofy / off --
    "surprised":   {"dw": -4, "dh": 10},
    "dumb":        {"dw": 4, "dh": 4, "paint": _dumb},
    "confused":    {"tilt": 4, "paint": _confused},
    "disoriented": {"tilt": 4, "bias": 0.3, "sway": (3.0, 2.2)},  # mismatched sizes + a slow woozy seesaw rock
    "bored":       {"paint": _bored},
    "dead":        {"paint": _dead},
}
EMOTIONS = tuple(MOODS)
