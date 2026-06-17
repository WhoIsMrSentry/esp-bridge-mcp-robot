"""A live clock -- HH:MM with a colon that blinks once a second."""
from datetime import datetime

from PIL import ImageFont

from ..spec import Action

try:
    _F = ImageFont.load_default(size=16)
except TypeError:                       # ancient Pillow
    _F = ImageFont.load_default()


def _overlay(d, W, H, now, ox=0.0, oy=0.0):
    t = datetime.now()                                 # wall-clock, not the engine's monotonic `now`
    s = f"{t.hour:02d}{':' if t.microsecond < 500000 else ' '}{t.minute:02d}"
    d.text(((W - d.textlength(s, font=_F)) / 2, H - 17), s, font=_F, fill=1)


ACTION = Action("clock", mood="standby", overlay=_overlay)
