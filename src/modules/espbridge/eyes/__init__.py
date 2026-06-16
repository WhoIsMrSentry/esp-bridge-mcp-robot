"""Procedural robot eyes for a 128x64 OLED (PIL). Pick a file by what a thing IS:
moods.py held expression, gestures.py one-shot reaction, activities.py looping status,
decor.py props, engine.py renderer, primitives.py helpers. Adding one = a line."""
from .activities import ACTIVITIES
from .engine import EyeEngine
from .gestures import GESTURES
from .moods import EMOTIONS

__all__ = ["EyeEngine", "EMOTIONS", "GESTURES", "ACTIVITIES"]
