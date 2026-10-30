import re
from engine import T


def read_time(s, lo=1.0, hi=6.0, cps=9.0):
    plain = re.sub(r'[`=]', '', s or '')
    return max(lo, min(hi, len(plain) / cps))


class Builder:
    def __init__(self, video, base):
        self.v = video
        self.s = dict(base)
        self.last_cap = None

    def step(self, hold=None, trans=0.45, min_hold=0.9, **kw):
        self.s.update(kw)
        self.s['_scene'] = 'sim'
        cap = self.s.get('_cap', '')
        if hold is None:
            hold = read_time(cap, lo=min_hold) if cap != self.last_cap else min_hold
        self.last_cap = cap
        self.v.add(self.s, hold, trans)

    def card(self, card, chapter, extra=0.5, per_line=None):
        st = {'_scene': 'card', '_card': card, '_chapter': chapter, 'reveal': 0}
        self.v.add(st, 0.25, 0.6)
        items = ([card['quote']] if card.get('quote') else []) + card.get('lines', [])
        for i, ln in enumerate(items):
            st = dict(st, reveal=i + 1)
            self.v.add(st, per_line or read_time(ln, lo=1.3, hi=6.0, cps=11.0), 0.45)
        if not items:
            self.v.add(st, 2.0, 0.1)
        self.v.add(st, extra, 0)
        self.last_cap = None


def bar_geom(box, n, maxv, pad_x=70, top=200, base_off=170, min_h=0):
    x0, y0, x1, y1 = box
    slot = (x1 - x0 - 2 * pad_x) / n
    base = y1 - base_off
    scale = (base - (y0 + top)) / maxv

    def cx(i):
        return x0 + pad_x + slot * (i + 0.5)

    def hy(v):
        return base - (v * scale + min_h)
    return slot, base, scale, cx, hy
