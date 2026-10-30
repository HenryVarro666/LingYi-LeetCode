"""Tiny animation engine: PIL frames piped into ffmpeg.

A video is a list of keyframes (state dicts). Between consecutive keyframes of the
same scene, numeric values are tweened (keys starting with '_' snap instantly).
Between different scenes the two frames cross-fade.
"""
import math
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont
from pygments.lexers import PythonLexer
from pygments.token import Token

W, H, FPS = 1920, 1080, 25
FONT_DIR = '/usr/share/fonts/opentype/noto/'

T = dict(
    bg=(13, 17, 23), panel=(22, 27, 34), panel2=(32, 38, 48), border=(48, 54, 61),
    text=(230, 237, 243), muted=(139, 148, 158), dim=(72, 79, 88),
    blue=(88, 166, 255), pink=(247, 120, 186), green=(63, 185, 80), yellow=(227, 179, 65),
    red=(248, 81, 73), orange=(255, 166, 87), purple=(188, 140, 255), cyan=(57, 197, 207),
    water=(56, 139, 253), code=(255, 203, 107),
)

_fc = {}


def font(size, bold=False, mono=False):
    key = (int(size), bold, mono)
    if key not in _fc:
        f = 'NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'
        _fc[key] = ImageFont.truetype(FONT_DIR + f, int(size), index=7 if mono else 2)
    return _fc[key]


def mix(c1, c2, a):
    """a=1 -> c1, a=0 -> c2"""
    a = max(0.0, min(1.0, a))
    return tuple(int(round(x * a + y * (1 - a))) for x, y in zip(c1, c2))


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self):
        self.im = Image.new('RGBA', (W, H), T['bg'] + (255,))
        self.d = ImageDraw.Draw(self.im)

    def rect(self, xy, fill=None, outline=None, width=1, r=0, alpha=255):
        x0, y0, x1, y1 = [float(v) for v in xy]
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if x1 - x0 < 1 or y1 - y0 < 1:
            return
        r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
        if alpha >= 255:
            self.d.rounded_rectangle((x0, y0, x1, y1), int(r), fill=fill, outline=outline, width=width)
            return
        if alpha <= 0:
            return
        ix0, iy0 = int(x0), int(y0)
        w, h = int(math.ceil(x1)) - ix0, int(math.ceil(y1)) - iy0
        layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((x0 - ix0, y0 - iy0, x1 - ix0 - 1, y1 - iy0 - 1), int(r),
                             fill=(fill + (int(alpha),)) if fill else None,
                             outline=(outline + (int(alpha),)) if outline else None, width=width)
        self.im.alpha_composite(layer, (ix0, iy0))

    def line(self, pts, color, width=2):
        self.d.line(pts, fill=color, width=width)

    def dashed(self, p0, p1, color, width=2, dash=12, gap=8):
        (x0, y0), (x1, y1) = p0, p1
        L = math.hypot(x1 - x0, y1 - y0)
        if L < 1:
            return
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        t = 0
        while t < L:
            t2 = min(L, t + dash)
            self.d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t2, y0 + uy * t2)], fill=color, width=width)
            t = t2 + gap

    def poly(self, pts, fill):
        self.d.polygon(pts, fill=fill)

    def tri_up(self, x, y, s, color):  # tip at (x,y) pointing up
        self.d.polygon([(x, y), (x - s, y + s * 1.3), (x + s, y + s * 1.3)], fill=color)

    def tri_down(self, x, y, s, color):  # tip at (x,y) pointing down
        self.d.polygon([(x, y), (x - s, y - s * 1.3), (x + s, y - s * 1.3)], fill=color)

    def text(self, xy, s, size=28, color=None, anchor='la', bold=False, mono=False):
        self.d.text(xy, str(s), font=font(size, bold, mono), fill=color or T['text'], anchor=anchor)

    def tlen(self, s, size=28, bold=False, mono=False):
        return font(size, bold, mono).getlength(str(s))

    def arrow(self, p0, p1, color, width=3, head=12):
        (x0, y0), (x1, y1) = p0, p1
        self.d.line([p0, p1], fill=color, width=width)
        ang = math.atan2(y1 - y0, x1 - x0)
        a1, a2 = ang + math.pi * 0.83, ang - math.pi * 0.83
        self.d.polygon([(x1, y1), (x1 + head * math.cos(a1), y1 + head * math.sin(a1)),
                        (x1 + head * math.cos(a2), y1 + head * math.sin(a2))], fill=color)

    def arc_arrow(self, p0, p1, lift, color, width=3, head=13, frac=1.0):
        """quadratic bezier from p0 to p1 bulging up by `lift`; draw first `frac` of it"""
        (x0, y0), (x1, y1) = p0, p1
        cx, cy = (x0 + x1) / 2, min(y0, y1) - lift
        n = 40
        m = max(2, int(n * frac))
        pts = []
        for i in range(m + 1):
            t = i / n
            pts.append(((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
                        (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1))
        self.d.line(pts, fill=color, width=width, joint='curve')
        if frac >= 0.99:
            (xa, ya), (xb, yb) = pts[-2], pts[-1]
            ang = math.atan2(yb - ya, xb - xa)
            a1, a2 = ang + math.pi * 0.83, ang - math.pi * 0.83
            self.d.polygon([(xb, yb), (xb + head * math.cos(a1), yb + head * math.sin(a1)),
                            (xb + head * math.cos(a2), yb + head * math.sin(a2))], fill=color)
        return pts[len(pts) // 2] if pts else (cx, cy)

    # ---- rich text: `code` and ==emphasis==
    def rich(self, x, y, s, width, size=32, color=None, accent=None, line_gap=1.55, max_lines=None, align='left'):
        color = color or T['text']
        accent = accent or T['orange']
        units = _rich_units(s)
        lines, cur, cw = [], [], 0.0
        for u in units:
            txt, kind = u
            f = font(size, kind == 'em', kind == 'code')
            w = f.getlength(txt) + (10 if kind == 'code' else 0)
            if txt == '\n':
                lines.append((cur, cw)); cur, cw = [], 0.0; continue
            if cw + w > width and cur:
                if txt.strip() == '':
                    lines.append((cur, cw)); cur, cw = [], 0.0; continue
                lines.append((cur, cw)); cur, cw = [], 0.0
            cur.append((txt, kind, w)); cw += w
        if cur:
            lines.append((cur, cw))
        if max_lines:
            lines = lines[:max_lines]
        lh = size * line_gap
        for li, (ln, lw) in enumerate(lines):
            cx = x if align == 'left' else x + (width - lw) / 2
            cy = y + li * lh
            for txt, kind, w in ln:
                if kind == 'code':
                    self.rect((cx + 1, cy - 2, cx + w - 1, cy + size * 1.22), fill=T['panel2'], r=6)
                    self.text((cx + 5, cy + size * 0.06), txt, size, T['code'], mono=True)
                elif kind == 'em':
                    self.text((cx, cy), txt, size, accent, bold=True)
                else:
                    self.text((cx, cy), txt, size, color)
                cx += w
        return len(lines) * lh


_TOK = re.compile(r'[A-Za-z0-9_\.\-\+\*/%<>=!\[\]\(\)\'",:]+|\s|.', re.S)


def _rich_units(s):
    out = []
    for part in re.split(r'(`[^`]+`|==(?=[^\s=])[^=]*?[^\s=]==)', s):
        if not part:
            continue
        if part.startswith('`'):
            out.append((part[1:-1], 'code'))
        elif part.startswith('=='):
            for sub in re.split(r'(`[^`]+`)', part[2:-2]):
                if not sub:
                    continue
                if sub.startswith('`') and sub.endswith('`') and len(sub) > 1:
                    out.append((sub[1:-1], 'code'))
                else:
                    for t in _TOK.findall(sub):
                        out.append((t, 'em'))
        else:
            for t in _TOK.findall(part):
                out.append((t, 'text'))
    # glue CJK punctuation to previous unit so lines never start with it
    glued = []
    for t, k in out:
        if glued and t in '，。、；：！？）」』》,.;:!?)' and glued[-1][1] == k:
            glued[-1] = (glued[-1][0] + t, k)
        else:
            glued.append((t, k))
    return glued


# ---------------------------------------------------------------- code panel
_COLORS = [
    (Token.Comment, (125, 133, 144)),
    (Token.Keyword, (255, 123, 114)),
    (Token.Operator.Word, (255, 123, 114)),
    (Token.Name.Function, (210, 168, 255)),
    (Token.Name.Class, (255, 166, 87)),
    (Token.Name.Builtin, (121, 192, 255)),
    (Token.Literal.Number, (121, 192, 255)),
    (Token.Literal.String, (165, 214, 255)),
]


def _tcolor(tt):
    for base, c in _COLORS:
        if tt in base:
            return c
    return (220, 226, 232)


def _uw(s):
    """display width in half-width units"""
    return sum(2 if ord(ch) > 0x2E7F else 1 for ch in s)


class Code:
    def __init__(self, src):
        self.src = src.strip('\n')
        self.raw = self.src.split('\n')
        toks = list(PythonLexer().get_tokens(self.src))
        lines, cur = [], []
        for tt, v in toks:
            parts = v.split('\n')
            for i, p in enumerate(parts):
                if i > 0:
                    lines.append(cur); cur = []
                if p:
                    cur.append((tt, p))
        if cur:
            lines.append(cur)
        self.lines = lines[:len(self.raw)]
        while len(self.lines) < len(self.raw):
            self.lines.append([])
        self._cache = {}

    def find(self, needle, start=0):
        for i, ln in enumerate(self.raw):
            if i >= start and needle in ln:
                return i
        raise KeyError(needle)

    def _layout(self, box):
        x0, y0, x1, y1 = box
        maxu = max([_uw(l) for l in self.raw] + [20])
        avail_w = (x1 - x0) - 62 - 20
        avail_h = (y1 - y0) - 70
        size_w = min(22, int(avail_w / (0.5 * maxu)))
        size_h = int(avail_h / (1.62 * len(self.raw)))
        size = min(size_w, size_h)
        if size < 15:
            size = max(13, min(size_w, 17))
        size = max(13, size)
        scroll = len(self.raw) * size * 1.62 > avail_h
        return size, size * 1.62, scroll

    def _text_layer(self, box):
        key = tuple(box)
        if key in self._cache:
            return self._cache[key]
        x0, y0, x1, y1 = box
        size, lh, scroll = self._layout(box)
        hgt = int(max(y1 - y0, 70 + lh * len(self.raw) + 20))
        layer = Image.new('RGBA', (int(x1 - x0), hgt), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        mono = font(size, mono=True)
        small = font(size - 3, mono=True)
        for i, toks in enumerate(self.lines):
            yy = i * lh
            d.text((46, yy), str(i + 1), font=small, fill=T['dim'], anchor='ra')
            cx = 62
            for tt, v in toks:
                d.text((cx, yy), v, font=mono, fill=_tcolor(tt))
                cx += mono.getlength(v)
        self._cache[key] = (layer, size, lh, scroll)
        return self._cache[key]

    def draw(self, cv, box, hl=None, hl_color=None, size=None, title='Python', hl2=None):
        x0, y0, x1, y1 = box
        cv.rect(box, fill=T['panel'], outline=T['border'], width=2, r=16)
        cv.text((x0 + 22, y0 + 16), title, 20, T['muted'])
        for k, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
            cv.d.ellipse((x1 - 90 + k * 24, y0 + 22, x1 - 76 + k * 24, y0 + 36), fill=c)
        layer, size, lh, scroll = self._text_layer(box)
        top = y0 + 62
        view_h = (y1 - 14) - top
        off = 0.0
        if scroll and hl is not None and hl >= 0:
            off = max(0.0, min(len(self.raw) * lh - view_h, hl * lh - view_h * 0.4))
        hl_color = hl_color or T['blue']
        if hl2:
            for ln in hl2:
                yy = top + ln * lh - off
                if top - 4 <= yy <= y1 - lh:
                    cv.rect((x0 + 8, yy - 4, x1 - 8, yy + lh - 4), fill=T['yellow'], alpha=28, r=6)
        if hl is not None and hl >= 0:
            yy = top + hl * lh - off
            cv.rect((x0 + 8, yy - 4, x1 - 8, yy + lh - 4), fill=hl_color, alpha=52, r=6)
            cv.rect((x0 + 8, yy - 4, x0 + 14, yy + lh - 4), fill=hl_color, r=3)
        crop = layer.crop((0, int(off), layer.width, int(off + view_h)))
        cv.im.alpha_composite(crop, (int(x0), int(top)))
        if scroll:
            total = len(self.raw) * lh
            th = max(40, view_h * view_h / total)
            ty = top + (view_h - th) * (off / max(1, total - view_h))
            cv.rect((x1 - 12, ty, x1 - 6, ty + th), fill=T['border'], r=3)


# ---------------------------------------------------------------- video
class Video:
    def __init__(self, num, title, author, accent, tags, code=None, draw_viz=None, difficulty=''):
        self.num, self.title, self.author, self.accent = num, title, author, accent
        self.tags, self.code, self.draw_viz, self.difficulty = tags, code, draw_viz, difficulty
        self.keys = []  # (state, hold, trans)

    def add(self, state, hold=1.2, trans=0.4):
        self.keys.append((dict(state), hold, trans))

    # ---- frame composition
    def header(self, cv, st):
        cv.text((48, 30), f'LeetCode {self.num}' if self.num not in ('', None) else 'LeetCode Hot100 · 分类概念', 26, T['muted'], bold=True)
        cv.text((48, 62), self.title, 40, T['text'], bold=True)
        tx = 48 + cv.tlen(self.title, 40, True) + 24
        for tg in ([self.difficulty] if self.difficulty else []) + self.tags:
            w = cv.tlen(tg, 20) + 24
            col = {'Easy': T['green'], 'Medium': T['yellow'], 'Hard': T['red']}.get(tg, T['muted'])
            cv.rect((tx, 76, tx + w, 108), outline=col, width=2, r=16)
            cv.text((tx + 12, 79), tg, 20, col)
            tx += w + 10
        badge = '分类概念讲解' if self.author == '概念讲解' else f'{self.author} 题解'
        bw = cv.tlen(badge, 26, True) + 40
        cv.rect((W - 48 - bw, 40, W - 48, 92), fill=self.accent, r=26)
        cv.text((W - 48 - bw / 2, 66), badge, 26, T['bg'], anchor='mm', bold=True)
        ch = st.get('_chapter')
        if ch:
            cv.text((W - 48 - bw - 24, 66), ch, 24, T['muted'], anchor='rm')

    def code_x0(self):
        """code panel grows (up to ~1060px) when the code has long lines, so the font stays readable"""
        if not self.code:
            return 1880
        maxu = max([_uw(l) for l in self.code.raw] + [20])
        need = 62 + 26 + maxu * 0.5 * 18
        return 1880 - int(min(1060, max(800, need)))

    def frame(self, st):
        cv = Canvas()
        self.header(cv, st)
        sc = st.get('_scene', 'sim')
        if sc == 'card':
            draw_card(cv, st, self.accent)
        else:
            cx0 = self.code_x0()
            vb = (40, 130, cx0 - 20, 860)
            cv.rect(vb, fill=T['panel'], outline=T['border'], width=2, r=16)
            self.draw_viz(cv, st, vb)
            if self.code:
                self.code.draw(cv, (cx0, 130, 1880, 860), st.get('hl'), self.accent, hl2=st.get('_hl2'))
            draw_vars(cv, st.get('_vars', []), (60, 790, cx0 - 40, 845), self.accent)
            cap = st.get('_cap', '')
            cv.rect((40, 878, 1880, 1048), fill=T['panel'], outline=T['border'], width=2, r=16)
            cv.rect((40, 878, 50, 1048), fill=self.accent, r=4)
            step = st.get('_step')
            if step:
                cv.text((76, 892), step, 22, self.accent, bold=True)
            cv.rich(76, 926 if step else 906, cap, 1780, size=33, accent=self.accent, max_lines=3, line_gap=1.45)
        return cv.im

    def render(self, out, crf=22, preset='veryfast'):
        """Encode only the frames that change (variable frame rate) when PyAV is available — 3–5x faster."""
        try:
            import av  # noqa: F401
        except ImportError:
            return self._render_ffmpeg_pipe(out, crf, preset)
        return self._render_vfr(out, crf, preset)

    def _schedule(self):
        """yield (pts, image_or_None_for_repeat) where only changing frames carry an image"""
        prev = None
        pts = 0
        for st, hold, trans in self.keys:
            nt = int(round(trans * FPS))
            if prev is not None and nt > 0:
                same = prev.get('_scene', 'sim') == st.get('_scene', 'sim') and not st.get('_cut')
                if same:
                    for i in range(nt):
                        yield pts, (lambda p=prev, s=st, k=(i + 1) / nt: self.frame(lerp_state(p, s, ease(k))))
                        pts += 1
                else:
                    a, b = self.frame(prev), self.frame(st)
                    for i in range(nt):
                        yield pts, (lambda a=a, b=b, k=(i + 1) / nt: Image.blend(a, b, ease(k)))
                        pts += 1
            elif nt > 0:
                yield pts, (lambda s=st: self.frame(s))
                pts += nt
            nh = int(round(hold * FPS))
            if nh:
                yield pts, (lambda s=st: self.frame(s))
                pts += nh
            prev = st
        yield pts, None  # end marker

    def _render_vfr(self, out, crf, preset):
        import av
        from fractions import Fraction
        total = sum(int(round(h * FPS)) + int(round(t * FPS)) for _, h, t in self.keys)
        container = av.open(out, mode='w', options={'movflags': '+faststart'})
        stream = container.add_stream('libx264', rate=FPS)
        stream.width, stream.height = W, H
        stream.pix_fmt = 'yuv420p'
        stream.time_base = Fraction(1, FPS)
        stream.codec_context.time_base = Fraction(1, FPS)
        stream.options = {'preset': preset, 'crf': str(crf), 'bf': '0'}
        last_img = None
        for pts, make in self._schedule():
            if make is None:
                # repeat the last image at the very end so the final hold keeps its duration
                if last_img is not None and pts > 0:
                    fr = av.VideoFrame.from_image(last_img)
                    fr.pts = pts - 1
                    for pkt in stream.encode(fr):
                        container.mux(pkt)
                break
            im = make().convert('RGB')
            d = ImageDraw.Draw(im)
            d.rectangle((0, H - 6, W, H), fill=T['panel'])
            d.rectangle((0, H - 6, int(W * pts / max(1, total)), H), fill=self.accent)
            last_img = im
            fr = av.VideoFrame.from_image(im)
            fr.pts = pts
            for pkt in stream.encode(fr):
                container.mux(pkt)
        for pkt in stream.encode():
            container.mux(pkt)
        container.close()
        return total / FPS

    def _render_ffmpeg_pipe(self, out, crf=22, preset='veryfast'):
        total = 0
        for _, hold, trans in self.keys:
            total += int(round(hold * FPS)) + int(round(trans * FPS))
        proc = subprocess.Popen(
            ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
             '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', preset, '-crf', str(crf),
             '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        fi = [0]

        def finish(im):
            im = im.convert('RGB')
            d = ImageDraw.Draw(im)
            d.rectangle((0, H - 6, W, H), fill=T['panel'])
            d.rectangle((0, H - 6, int(W * fi[0] / max(1, total)), H), fill=self.accent)
            return im.tobytes()

        def emit(buf, n=1):
            for _ in range(n):
                proc.stdin.write(buf)
            fi[0] += n

        prev = None
        for st, hold, trans in self.keys:
            nt = int(round(trans * FPS))
            if prev is not None and nt > 0:
                same = prev.get('_scene', 'sim') == st.get('_scene', 'sim') and not st.get('_cut')
                if same:
                    for i in range(nt):
                        emit(finish(self.frame(lerp_state(prev, st, ease((i + 1) / nt)))))
                else:
                    a, b = self.frame(prev), self.frame(st)
                    for i in range(nt):
                        emit(finish(Image.blend(a, b, ease((i + 1) / nt))))
            elif nt > 0:
                emit(finish(self.frame(st)), nt)
            nh = int(round(hold * FPS))
            if nh:
                emit(finish(self.frame(st)), nh)
            prev = st
        proc.stdin.close()
        proc.wait()
        return total / FPS


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def lerp_state(a, b, p):
    out = dict(b)
    for k, v in b.items():
        if k.startswith('_'):
            continue
        av = a.get(k)
        if _num(v) and _num(av):
            out[k] = av + (v - av) * p
        elif isinstance(v, list) and isinstance(av, list) and len(v) == len(av) and all(_num(x) for x in v + av):
            out[k] = [x + (y - x) * p for x, y in zip(av, v)]
    return out


def draw_vars(cv, items, box, accent):
    x0, y0, x1, y1 = box
    x = x0
    for name, val, *rest in items:
        col = rest[0] if rest else T['text']
        s1 = f'{name} = '
        w = cv.tlen(s1, 24, mono=True) + cv.tlen(str(val), 24, bold=True, mono=True) + 28
        if x + w > x1:
            break
        cv.rect((x, y0, x + w, y1), fill=T['panel2'], r=12)
        cv.text((x + 14, (y0 + y1) / 2), s1, 24, T['muted'], anchor='lm', mono=True)
        cv.text((x + 14 + cv.tlen(s1, 24, mono=True), (y0 + y1) / 2), str(val), 24, col, anchor='lm', bold=True, mono=True)
        x += w + 12


def draw_card(cv, st, accent):
    c = st['_card']
    reveal = st.get('reveal', 99)
    kind = c.get('kind', 'text')
    if kind == 'title':
        cv.text((W / 2, 330), c['big'], 96, T['text'], anchor='mm', bold=True)
        cv.text((W / 2, 440), c.get('sub', ''), 40, accent, anchor='mm', bold=True)
        y = 540
        for i, ln in enumerate(c.get('lines', [])):
            a = max(0, min(1, reveal - i))
            if a <= 0:
                break
            cv.rich(260, y, ln, 1400, size=34, color=mix(T['text'], T['bg'], a), accent=accent, align='center')
            y += 64
        return
    x, y = 200, 180
    cv.text((x, y), c['heading'], 54, T['text'], bold=True)
    cv.rect((x, y + 84, x + 120, y + 92), fill=accent, r=4)
    y += 140
    q = c.get('quote')
    if q:
        a = max(0, min(1, reveal))
        qh = 0
        # measure height by drawing into scratch canvas
        scratch = Canvas()
        qh = scratch.rich(0, 0, q, 1400, size=32, line_gap=1.5)
        cv.rect((x, y - 20, x + 1520, y + qh + 50), fill=T['panel'], r=14)
        cv.rect((x, y - 20, x + 8, y + qh + 50), fill=accent, r=4)
        cv.rich(x + 50, y, q, 1400, size=32, color=mix(T['text'], T['panel'], a), accent=accent, line_gap=1.5)
        src = c.get('src')
        if src:
            cv.text((x + 1490, y + qh + 16), src, 22, T['muted'], anchor='ra')
        y += qh + 100
        reveal -= 1
    for i, ln in enumerate(c.get('lines', [])):
        a = max(0, min(1, reveal - i))
        if a <= 0:
            break
        col = mix(T['text'], T['bg'], a)
        cv.d.ellipse((x + 4, y + 18, x + 18, y + 32), fill=mix(accent, T['bg'], a))
        hh = cv.rich(x + 44, y, ln, 1460, size=34, color=col, accent=accent, line_gap=1.5)
        y += hh + 22
