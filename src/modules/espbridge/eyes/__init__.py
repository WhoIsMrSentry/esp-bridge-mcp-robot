"""Procedural robot eyes for a 128x64 OLED (PIL).

Each effect is ONE self-contained file in a folder, named by what it IS:
  moods/     a held expression       (size + lid paint + decor)   -> MOODS    {name: Mood}
  gestures/  a one-shot reaction     (blink or enveloped motion)  -> GESTURES {name: Gesture}
  actions/   a looping task status   (gaze pose + face + overlay)  -> ACTIONS  {name: Action}
Each registry is an ordered dict (curated in its folder's __init__). Shared bits: spec.py
(the schema), painters.py (lid carvers + the twinkle motif), engine.py (the renderer AND the
shared eye math -- ease/smoothstep/lid_openness/rounded_rect/look/rand). Reach for those shared
helpers rather than re-rolling them per file: e.g. all pseudo-randomness goes through one
`rand()`. Single-use helpers live in their own effect file. Add an effect by dropping a file
in a folder + one line in its __init__
order list -- see spec.py. The whole package is self-contained (relative imports only), so it
drops into any app: copy the eyes/ folder, `pip install pillow`, and drive EyeEngine."""
from .actions import ACTIONS
from .engine import EyeEngine
from .gestures import GESTURES
from .moods import MOODS

__all__ = ["EyeEngine", "MOODS", "GESTURES", "ACTIONS"]
