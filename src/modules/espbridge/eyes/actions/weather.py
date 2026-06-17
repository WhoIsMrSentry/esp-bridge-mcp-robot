"""Live weather widget -- a sky glyph plus the current temperature.

Free, no API key: location from the device IP (ipapi.co), conditions from Open-Meteo. The fetch
runs in a daemon thread (never blocks the render loop), caches the last good reading, refreshes
every 15 min, and falls back to a 'no signal' glyph when offline."""
import json
import math
import threading
import urllib.request

from PIL import ImageFont

from ..spec import Action

_GEO = "https://ipapi.co/json/"
_API = ("https://api.open-meteo.com/v1/forecast"
        "?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,is_day")
_REFRESH = 900.0        # s between refetches once we have data
_RETRY = 30.0           # s between retries while still offline
_TIMEOUT = 6            # s per request

try:
    _F = ImageFont.load_default(size=12)
except TypeError:                       # ancient Pillow
    _F = ImageFont.load_default()

_lock = threading.Lock()
_state = {"temp": None, "code": 0, "day": 1, "at": None, "fetching": False}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "pip-robot"})
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as r:
        return json.load(r)


def _fetch():
    try:
        geo = _get(_GEO)
        cur = _get(_API.format(lat=geo["latitude"], lon=geo["longitude"]))["current"]
        with _lock:
            _state.update(temp=round(cur["temperature_2m"]), code=int(cur["weather_code"]),
                          day=int(cur.get("is_day", 1)))
    except Exception:
        pass                # keep the last good reading; overlay shows offline until one lands
    finally:
        with _lock:
            _state["fetching"] = False


def _maybe_refresh(now):
    with _lock:
        interval = _REFRESH if _state["temp"] is not None else _RETRY
        due = _state["at"] is None or now - _state["at"] >= interval
        if due and not _state["fetching"]:
            _state["fetching"], _state["at"] = True, now
            threading.Thread(target=_fetch, name="weather", daemon=True).start()


# ----------------------------------------------------------- sky glyphs (~14px)
def _cloud(d, cx, cy):
    d.ellipse([cx - 7, cy - 2, cx - 1, cy + 4], fill=1)
    d.ellipse([cx - 3, cy - 5, cx + 4, cy + 3], fill=1)
    d.ellipse([cx + 1, cy - 2, cx + 7, cy + 4], fill=1)
    d.rectangle([cx - 7, cy + 2, cx + 7, cy + 5], fill=1)


def _sun(d, cx, cy):
    for k in range(8):
        a = k * math.pi / 4
        d.line([cx + math.cos(a) * 4, cy + math.sin(a) * 4,
                cx + math.cos(a) * 7, cy + math.sin(a) * 7], fill=1)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=1)


def _moon(d, cx, cy):
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=1)
    d.ellipse([cx - 1, cy - 5, cx + 6, cy + 3], fill=0)        # carve the crescent


def _icon(d, cx, cy, code, day):
    if code in (95, 96, 99):                                   # thunder
        _cloud(d, cx, cy - 2)
        d.line([cx, cy + 3, cx - 2, cy + 7], fill=1)
        d.line([cx - 2, cy + 7, cx + 1, cy + 7], fill=1)
        d.line([cx + 1, cy + 7, cx - 1, cy + 11], fill=1)
    elif code in (71, 73, 75, 77, 85, 86):                     # snow
        _cloud(d, cx, cy - 2)
        for k in range(3):
            d.point((cx - 4 + k * 4, cy + 8), fill=1)
    elif code in (45, 48):                                     # fog
        for k in range(4):
            d.line([cx - 7, cy - 3 + k * 3, cx + 7, cy - 3 + k * 3], fill=1)
    elif code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):   # rain
        _cloud(d, cx, cy - 2)
        for k in range(3):
            d.line([cx - 4 + k * 4, cy + 6, cx - 6 + k * 4, cy + 10], fill=1)
    elif code in (1, 2):                                       # partly cloudy
        (_sun if day else _moon)(d, cx - 2, cy - 2)
        _cloud(d, cx + 2, cy + 1)
    elif code == 3:                                            # overcast
        _cloud(d, cx, cy)
    else:                                                      # clear (0)
        (_sun if day else _moon)(d, cx, cy)


def _overlay(d, W, H, now, ox=0.0, oy=0.0):
    _maybe_refresh(now)
    with _lock:
        temp, code, day = _state["temp"], _state["code"], _state["day"]
    cy = H - 8
    if temp is None:                                           # offline -> slashed cloud + dashes
        _cloud(d, 22, cy - 2)
        d.line([13, cy + 6, 31, cy - 8], fill=1)
        d.text((44, H - 13), "--°C", font=_F, fill=1)
        return
    _icon(d, 22, cy, code, day)
    d.text((44, H - 13), f"{temp}°C", font=_F, fill=1)


ACTION = Action("weather", mood="chill", overlay=_overlay)
