"""Capture a single face to a GIF, headless -- develop the eyes with no OLED.

Drives a fresh EyeEngine off a virtual clock (no thread, no sleep) so a 30-second
clip renders as fast as the CPU allows. One-shot gestures are re-fired to fill the
clip. See docs/make_gif.py for the labelled showcase of every face.
"""
from __future__ import annotations

from pathlib import Path

from .engine import EyeEngine
from .gestures import GESTURES

W, H = 128, 64
FPS = 24      # capture / playback frame rate (matches the real panel)
SCALE = 3     # pixel zoom of the output GIF


def record_gif(kind, name, *, seconds=30.0, fps=FPS, scale=SCALE, out=None):
    """Render `seconds` of one face to a looping GIF; returns the written path."""
    try:
        from PIL import Image
    except ImportError:  # docs/dev extra; the robot itself never needs it
        raise SystemExit("GIF capture needs Pillow:  uv add pillow")

    clock = [0.0]
    eyes = EyeEngine(lambda _img: None, width=W, height=H, fps=fps, clock=lambda: clock[0])
    eyes.reset_timers(clock[0])
    eyes.set_activity("idle")
    eyes.set_mood("neutral")

    if kind == "mood":
        eyes.set_mood(name)
    elif kind == "activity":
        eyes.set_activity(name)
    else:
        eyes.play_gesture(name)

    period = GESTURES[name].dur if kind == "gesture" else None   # re-fire one-shots
    next_fire = period
    frames = []
    for _ in range(max(1, round(seconds * fps))):
        clock[0] += 1.0 / fps
        if period and clock[0] >= next_fire:
            eyes.play_gesture(name)
            next_fire += period
        frame = eyes.step(clock[0]).convert("L").resize((W * scale, H * scale), Image.NEAREST)
        frames.append(frame)

    out = Path(out) if out else Path.cwd() / f"{name}.gif"
    frames[0].save(out, save_all=True, append_images=frames[1:], optimize=True,
                   duration=int(1000 / fps), loop=0)
    return out
