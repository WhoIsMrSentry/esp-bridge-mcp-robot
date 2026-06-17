"""Looping task statuses. Add one: drop `<name>.py` here exposing `ACTION = Action(...)`, then
slot its name into the curated order below. ('idle' isn't an entry -- it's the resting stop:
set_activity('idle'), or any unknown name, just stops whatever's looping.)"""
from .._registry import load

# -- curated order; work, then links/holding, then a break --
_ORDER = (
    "thinking", "scanning", "searching", "processing",           # heads-down work
    "working", "editing", "debugging", "building", "testing", "deploying",
    "connecting", "listening", "waiting",                        # links & holding pattern
    "smoking",                                                    # a chilled break
    "glitch",                                                     # a crash / corruption fit
    "jackpot",                                                    # slot-machine reels + a coin shower
    "sponsor",                                                    # GitHub Sponsors QR + heart
)

ACTIONS = load(__name__, _ORDER, "ACTION")   # name -> Action, curated order (errors on a stray file)
