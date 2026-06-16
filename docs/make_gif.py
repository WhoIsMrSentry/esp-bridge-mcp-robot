"""Render Pip's faces headlessly off the real eye engine (no hardware).

    uv run docs/make_gif.py            # writes docs/pip-eyes.gif (every face, labelled)
    uv run docs/make_gif.py zen        # writes docs/zen_preview.png (one face, 5 frames)

No args -> the full showcase GIF. A face name (mood / gesture / activity) ->
a 5-frame contact sheet for eyeballing that one face during development.
Both drive the engine with a capture callback and sample its latest frame.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from modules.espbridge.eyes import ACTIVITIES, EMOTIONS, GESTURES, EyeEngine  # noqa: E402
from modules.espbridge.eyes.gestures import BLINKS, GESTURES_FN  # noqa: E402

W, H = 128, 64
SCALE = 3          # pixel zoom for the eyes
BAR = 28           # caption strip height (px, unscaled)
SAMPLE_FPS = 14    # frames sampled per second for the GIF
MOOD_SEC = 0.9     # dwell per mood
ACT_SEC = 1.6      # dwell per activity
GEST_PAD = 0.4     # extra time after a gesture's own duration
OUT = ROOT / "docs" / "pip-eyes.gif"

PREVIEW_N = 5      # frames per single-face preview sheet
PREVIEW_SCALE = 2  # pixel zoom for a preview frame
PREVIEW_FRACS = (0.1, 0.3, 0.5, 0.7, 0.9)   # where in the window each frame is grabbed

_latest = {}
_frames = []       # (eye image, caption)


def _gesture_dur(name):
    if name in BLINKS:
        return BLINKS[name][1]
    return GESTURES_FN[name][0]


def _load_font(size=16):
    for name in ("arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _record(caption, seconds):
    """Sample the latest rendered frame at SAMPLE_FPS for `seconds`."""
    for _ in range(max(1, int(seconds * SAMPLE_FPS))):
        time.sleep(1.0 / SAMPLE_FPS)
        f = _latest.get("f")
        if f is not None:
            _frames.append((f, caption))


def _compose(eye, caption, font):
    big = eye.convert("L").resize((W * SCALE, H * SCALE), Image.NEAREST)
    canvas = Image.new("L", (W * SCALE, H * SCALE + BAR), 0)
    canvas.paste(big, (0, 0))
    d = ImageDraw.Draw(canvas)
    tw = d.textlength(caption, font=font)
    d.text(((W * SCALE - tw) / 2, H * SCALE + (BAR - 16) / 2), caption, fill=255, font=font)
    return canvas


def main():
    eyes = EyeEngine(lambda img: _latest.__setitem__("f", img.copy()), fps=30)
    eyes.start()
    try:
        eyes.set_activity("idle")
        eyes.set_mood("neutral")
        _record("Pip", 1.0)

        for m in EMOTIONS:                       # static expressions
            eyes.set_mood(m)
            _record(f"mood: {m}", MOOD_SEC)

        for g in GESTURES:                       # one-shot motions
            if g == "none":
                continue
            eyes.set_mood("neutral")             # turn back to a natural face first...
            time.sleep(0.4)                      # ...and let it settle so the gesture isn't shown on the last mood
            eyes.play_gesture(g)
            _record(f"gesture: {g}", max(0.8, _gesture_dur(g) + GEST_PAD))

        for a in ACTIVITIES:                     # looping statuses
            if a == "idle":
                continue
            eyes.set_activity(a)
            _record(f"activity: {a}", ACT_SEC)
        eyes.set_activity("idle")
    finally:
        eyes.stop()

    print(f"composing {len(_frames)} frames...")
    font = _load_font()
    imgs = [_compose(eye, cap, font) for eye, cap in _frames]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    imgs[0].save(OUT, save_all=True, append_images=imgs[1:], optimize=True,
                 duration=int(1000 / SAMPLE_FPS), loop=0)
    kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(imgs)} frames, {kb:.0f} KB)")


# ----------------------------------------------------------- single-face preview
def _kind(name):
    """Which layer a face name belongs to (None if unknown)."""
    if name in EMOTIONS:
        return "mood"
    if name in GESTURES and name != "none":
        return "gesture"
    if name in ACTIVITIES and name != "idle":
        return "activity"
    return None


def _sample(eyes, name, kind):
    """Drive the one face, then grab PREVIEW_N frames spread across its arc/loop."""
    if kind == "gesture":
        eyes.set_mood("neutral")
        time.sleep(0.4)                      # settle to a plain face first
        window = _gesture_dur(name)          # the gesture's own in-and-out arc
        eyes.play_gesture(name)
    elif kind == "activity":
        eyes.set_activity(name)
        window = ACT_SEC
        time.sleep(0.3)
    else:
        eyes.set_mood(name)
        window = MOOD_SEC + 0.3
        time.sleep(0.3)
    t0 = time.monotonic()
    frames = []
    for frac in PREVIEW_FRACS:
        while time.monotonic() < t0 + frac * window:
            time.sleep(0.005)
        f = _latest.get("f")
        if f is not None:
            frames.append(f.copy())
    return frames


def _compose_preview(frames, name, kind, font, small):
    """Stack the frames into one labelled filmstrip (name header + per-frame index)."""
    fw, fh, head, gap = W * PREVIEW_SCALE, H * PREVIEW_SCALE, 22, 4
    canvas = Image.new("L", (fw, head + len(frames) * (fh + gap)), 0)
    d = ImageDraw.Draw(canvas)
    d.text((6, 3), f"{name}  ({kind})", fill=255, font=font)
    for i, f in enumerate(frames):
        y = head + i * (fh + gap)
        canvas.paste(f.convert("L").resize((fw, fh), Image.NEAREST), (0, y))
        d.text((4, y + 2), f"n={i}", fill=255, font=small)
    return canvas


def preview(name):
    name = name.lower()
    kind = _kind(name)
    if not kind:
        print(f"unknown face: {name!r}", file=sys.stderr)
        print("moods:      " + " ".join(EMOTIONS), file=sys.stderr)
        print("gestures:   " + " ".join(g for g in GESTURES if g != "none"), file=sys.stderr)
        print("activities: " + " ".join(a for a in ACTIVITIES if a != "idle"), file=sys.stderr)
        return 2

    eyes = EyeEngine(lambda img: _latest.__setitem__("f", img.copy()), fps=30)
    eyes.start()
    try:
        eyes.set_activity("idle")
        eyes.set_mood("neutral")
        time.sleep(0.3)
        frames = _sample(eyes, name, kind)
    finally:
        eyes.stop()

    out = ROOT / "docs" / f"{name}_preview.png"
    _compose_preview(frames, name, kind, _load_font(), _load_font(12)).save(out, optimize=True)
    print(f"wrote {out.relative_to(ROOT)}  ({len(frames)} frames)")
    return 0


if __name__ == "__main__":
    sys.exit(preview(sys.argv[1]) if len(sys.argv) > 1 else main())
