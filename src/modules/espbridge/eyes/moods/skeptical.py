"""One eye narrowed + angled, the other barely lidded."""
from ..painters import lids
from ..spec import Mood


def _paint(d, x, y, w, h, r, ir):   # one eye narrowed+angled, the other barely lidded
    if ir:
        lids(d, x, y, w, h, top=0.14)
    else:
        d.polygon([(x - 2, y - 2), (x + w + 2, y - 2),
                   (x + w + 2, y + h * 0.5), (x - 2, y + h * 0.66)], fill=0)


MOOD = Mood("skeptical", paint=_paint)
