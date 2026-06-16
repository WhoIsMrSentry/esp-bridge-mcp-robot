"""Held expressions. Add one: drop `<name>.py` here exposing `MOOD = Mood(...)`, then slot
its name into the curated order below (the order drives the menu, the showcase, the LLM enum)."""
from importlib import import_module

# -- curated display order, grouped by feel --
_ORDER = (
    # baseline & system
    "neutral", "alert", "attentive", "standby",
    # positive / warm
    "happy", "lovely", "kawaii", "awe", "cool",
    # focus / calm
    "focused", "zen", "wired", "chill",
    # sad / anxious / low
    "sad", "gloomy", "worried", "nervous", "despair", "scared", "tired", "sleepy",
    # angry / wary
    "angry", "furious", "devil", "suspicious", "skeptical",
    # dazed / goofy / off
    "surprised", "dumb", "confused", "disoriented", "bored", "dead",
)

MOODS = {n: import_module(f"{__name__}.{n}").MOOD for n in _ORDER}   # name -> Mood, in order
