"""Generic data-structure views drawn from a trace snapshot.

Every view gets (cv, spec, st, box, vi, ctx):
  st['_S']  merged variables AFTER the highlighted line ran (innermost frame wins)
  st['_B']  merged variables BEFORE it ran
  st['_frames'] list of frames (outermost first) after the line
  st[f'p{vi}:{name}'] tweened float positions for pointers of this view
"""
import collections
import math

from engine import T, mix
import tracer

PALETTE = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange', 'red']


def col(c, default='blue'):
    if c is None:
        c = default
    if isinstance(c, str):
        return T.get(c, T['blue'])
    return tuple(c)


def ev(expr, S):
    if expr is None:
        return None
    if not isinstance(expr, str) and not callable(expr):
        return expr  # literal list/tuple/number given directly
    if callable(expr):
        try:
            return expr(S)
        except Exception:
            return None
    if expr in S:
        return S[expr]
    try:
        return eval(expr, {'__builtins__': __builtins__, 'inf': math.inf}, _Env(S))
    except Exception:
        return None


class _Env(dict):
    """lets eval see `self.x` style keys as attributes of a fake self; B.x works too"""
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __init__(self, S):
        super().__init__(S)
        attrs = {k[5:]: v for k, v in S.items() if k.startswith('self.')}
        if attrs:
            self['self'] = type('S', (), attrs)()


_PRIM = (int, float, str, bool, type(None))


def _attrs(x):
    names = []
    for c in type(x).__mro__:
        names += [n for n in getattr(c, '__slots__', ()) if isinstance(n, str)]
    if hasattr(x, '__dict__'):
        names += list(vars(x))
    out = []
    for n in names:
        if n.startswith('_') or n in [o[0] for o in out]:
            continue
        try:
            out.append((n, getattr(x, n)))
        except AttributeError:
            pass
    return out


def sig(x, d=0):
    """structural signature, safe on cycles; used to decide 'did this change?'"""
    if isinstance(x, _PRIM):
        return x
    if hasattr(x, '_uid'):
        return ('N', x._uid, getattr(x, 'val', None)) + tuple(
            getattr(getattr(x, a, None), '_uid', None) for a in ('next', 'left', 'right', 'random'))
    if d > 3:
        return type(x).__name__
    if isinstance(x, (list, tuple, collections.deque)):
        return (type(x).__name__,) + tuple(sig(y, d + 1) for y in x)
    if isinstance(x, dict):
        return ('D',) + tuple((sig(k, d + 1), sig(v, d + 1)) for k, v in x.items())
    if isinstance(x, (set, frozenset)):
        return ('S',) + tuple(sorted(repr(y) for y in x))
    return (type(x).__name__,) + tuple((n, sig(v, d + 2)) for n, v in _attrs(x))


def eq(a, b):
    try:
        return sig(a) == sig(b)
    except Exception:
        return repr(a) == repr(b)


def obj_label(x, maxlen=14):
    inner = ','.join(f'{n}={fmt(v, 5)}' for n, v in _attrs(x) if isinstance(v, _PRIM))[:maxlen]
    return f'{type(x).__name__}({inner})'


def fmt(x, maxlen=14):
    if x is None:
        return '·'
    if x is True:
        return 'T'
    if x is False:
        return 'F'
    if isinstance(x, float):
        if math.isinf(x):
            return '∞' if x > 0 else '-∞'
        return f'{x:g}'
    if isinstance(x, (tracer.ListNode, tracer.TreeNode, tracer.Node)):
        return f'({x.val})'
    if isinstance(x, (list, tuple)):
        inner = ','.join(fmt(y, 6) for y in x)
        s = ('[' + inner + ']') if isinstance(x, list) else ('(' + inner + ')')
    elif isinstance(x, str):
        s = x
    elif type(x).__repr__ is object.__repr__:
        s = obj_label(x, maxlen)
    else:
        s = str(x)
    return s if len(s) <= maxlen else s[:maxlen - 1] + '…'


def fmt_var(x, maxlen=22):
    if x is None:
        return 'None'
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, str):
        s = repr(x)
        return s if len(s) <= maxlen else s[:maxlen - 1] + '…'
    if isinstance(x, dict):
        s = '{' + ', '.join(f'{fmt(k, 6)}:{fmt(v, 6)}' for k, v in list(x.items())[:6]) + ('…' if len(x) > 6 else '') + '}'
        return s if len(s) <= maxlen else s[:maxlen - 1] + '…'
    if isinstance(x, (set, frozenset)):
        s = '{' + ','.join(fmt(v, 5) for v in list(x)[:8]) + '}'
        return s if len(s) <= maxlen else s[:maxlen - 1] + '…'
    if isinstance(x, (tracer.ListNode, tracer.TreeNode, tracer.Node)):
        return f'{type(x).__name__}({x.val})'
    return fmt(x, maxlen)


def all_vals(st):
    """every local of every frame (keys made unique) — so recursion doesn't hide outer nodes"""
    out = {}
    for k, fr in enumerate(st.get('_frames', [])):
        for name, v in fr['locals'].items():
            out[f'{k}:{name}'] = v
    if not out:
        out = dict(st['_S'])
    return out


def label(cv, box, text):
    cv.text((box[0] + 18, box[1] + 4), text, 24, T['muted'], bold=True)


def tween_ptr(st, vi, name, S):
    k = f'p{vi}:{name}'
    if k in st:
        return st[k]
    return ev(name, S)


def ptr_values(spec, S):
    """name -> int value for pointer exprs of a view (used to build tween keys)"""
    out = {}
    ps = spec.get('pointers') or {}
    for name in ps:
        v = ev(name, S)
        if isinstance(v, int) and not isinstance(v, bool):
            out[name] = v
    for k, name in enumerate(spec.get('window') or ()):
        v = ev(name, S)
        if isinstance(v, int) and not isinstance(v, bool):
            out[f'w{k}'] = v
    return out


def _draw_pointers(cv, spec, st, vi, S, xof, y, cell):
    ps = spec.get('pointers') or {}
    groups = {}
    for k, (name, c) in enumerate(ps.items()):
        v = tween_ptr(st, vi, name, S)
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        groups.setdefault(int(round(v)), []).append((name, col(c, PALETTE[k % len(PALETTE)]), v))
    for idx, items in groups.items():
        for r, (name, c, v) in enumerate(items):
            X = xof(v) + cell / 2
            if r == 0:
                cv.tri_up(X, y, 10, c)
            disp = spec.get('pointer_labels', {}).get(name, name)
            cv.text((X, y + 16 + r * 27), disp, 22, c, anchor='mt', bold=True)


# ------------------------------------------------------------------ array / bars
def v_array(cv, spec, st, box, vi, ctx):
    S, B = st['_S'], st['_B']
    x0, y0, x1, y1 = box
    name = spec.get('var')
    label(cv, box, spec.get('label', name))
    vals = ev(name, S)
    if vals is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    if isinstance(vals, str):
        vals = list(vals)
    vals = list(vals)
    bvals = ev(name, B)
    bvals = list(bvals) if isinstance(bvals, (list, tuple, str)) else None
    n = max(1, len(vals))
    n_slots = max(n, spec.get('min_slots', 0))
    width = x1 - x0 - 40
    cell = max(24, min(spec.get('cell', 84), width / n_slots))
    shown = min(len(vals), int(width // cell))
    sx = x0 + 20 + (width - cell * n_slots) / 2 if cell * n_slots <= width else x0 + 20

    def xof(i):
        return sx + i * cell

    bars = spec.get('bars', spec.get('type') == 'bars')
    nptr_rows = max(1, len(spec.get('pointers') or {}))
    ptr_h = 26 + 27 * min(3, nptr_rows)
    top = y0 + (48 if spec.get('window') else 40)
    if bars:
        base = y1 - ptr_h - 30
        nums = [v for v in vals if isinstance(v, (int, float)) and not isinstance(v, bool) and not math.isinf(v)]
        vmax = spec.get('vmax') or max([abs(v) for v in nums] + [1])
        scale = (base - top - 34) / vmax
        cell_top, cell_bot = top, base
    else:
        ch = min(cell * 0.92, spec.get('cell', 84) * 0.92)
        cell_top, cell_bot = top, top + ch
        base = cell_bot
    # window highlight
    win = spec.get('window')
    if win:
        a = tween_ptr(st, vi, 'w0', S) if f'p{vi}:w0' in st else ev(win[0], S)
        b = tween_ptr(st, vi, 'w1', S) if f'p{vi}:w1' in st else ev(win[1], S)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b >= a - 0.01:
            wc = col(spec.get('window_color', 'cyan'))
            cv.rect((xof(a) - 4, cell_top - 6, xof(b) + cell + 4, base + 6), fill=wc, alpha=40, r=10)
            cv.rect((xof(a) - 4, cell_top - 6, xof(b) + cell + 4, base + 6), outline=wc, width=3, r=10)
    color_fn = spec.get('color')
    dim_fn = spec.get('dim')
    fs = int(max(14, min(34, cell * 0.42)))
    for i in range(shown):
        v = vals[i]
        c = None
        if color_fn:
            try:
                c = color_fn(S, i, v)
            except Exception:
                c = None
        dimmed = False
        if dim_fn:
            try:
                dimmed = bool(dim_fn(S, i, v))
            except Exception:
                pass
        changed = bvals is not None and (i >= len(bvals) or not eq(bvals[i], v))
        fill = col(c) if c else (T['panel2'] if not bars else (110, 120, 132))
        if dimmed:
            fill = (40, 45, 53)
        X = xof(i)
        if bars:
            hv = v if isinstance(v, (int, float)) and not isinstance(v, bool) and not math.isinf(v) else 0
            hpx = max(3, abs(hv) * scale)
            bw = cell * 0.62
            cv.rect((X + (cell - bw) / 2, base - hpx, X + (cell + bw) / 2, base), fill=fill, r=5)
            if changed:
                cv.rect((X + (cell - bw) / 2 - 3, base - hpx - 3, X + (cell + bw) / 2 + 3, base + 1), outline=T['yellow'], width=3, r=6)
            cv.text((X + cell / 2, base - hpx - 6), fmt(v, 6), fs, T['dim'] if dimmed else T['text'], anchor='mb', bold=True)
        else:
            pad = max(2, cell * 0.06)
            cv.rect((X + pad, cell_top, X + cell - pad, cell_bot), fill=fill, r=8,
                    outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
            tc = T['bg'] if (c and not dimmed) else (T['dim'] if dimmed else T['text'])
            s = fmt(v, max(2, int(cell / (fs * 0.55))))
            cv.text((X + cell / 2, (cell_top + cell_bot) / 2), s, fs if len(s) < 4 else int(fs * 0.8), tc, anchor='mm', bold=True)
        if spec.get('index', True):
            cv.text((X + cell / 2, base + 6), i, 18, T['dim'], anchor='mt', mono=True)
    if shown < len(vals):
        cv.text((x1 - 20, cell_bot), f'…共{n}项', 20, T['muted'], anchor='rb')
    if bars:
        cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    _draw_pointers(cv, spec, st, vi, S, xof, base + 32, cell)


def h_array(spec):
    n = len(spec.get('pointers') or {})
    if spec.get('bars') or spec.get('type') == 'bars':
        return spec.get('h', 330)
    return spec.get('h', 40 + min(84, spec.get('cell', 84)) * 0.92 + 30 + (27 * min(3, n) + 16 if n else 0))


# ------------------------------------------------------------------ map / set
def v_map(cv, spec, st, box, vi, ctx):
    S, B = st['_S'], st['_B']
    x0, y0, x1, y1 = box
    name = spec['var']
    label(cv, box, spec.get('label', name))
    d = ev(name, S)
    bd = ev(name, B)
    if d is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    is_set = isinstance(d, (set, frozenset))
    items = sorted(d, key=_sortkey) if is_set else list(d.items())
    f = spec.get('fmt')
    x, y = x0 + 18, y0 + 42
    fs = spec.get('font', 24)
    rowh = fs + 22
    for it in items:
        if is_set:
            s = fmt(it, 16) if not f else f(it)
            changed = not isinstance(bd, (set, frozenset)) or it not in bd
        else:
            k, v = it
            s = (f'{fmt(k, 12)}: {fmt(v, 16)}') if not f else f(k, v)
            if isinstance(bd, dict):
                bmap = {sig(kk): vv for kk, vv in bd.items()}
                changed = sig(k) not in bmap or not eq(bmap[sig(k)], v)
            else:
                changed = True
        w = cv.tlen(s, fs, mono=True) + 24
        if x + w > x1 - 12:
            x = x0 + 18
            y += rowh
        if y + rowh > y1:
            cv.text((x, y - rowh + 8), '…', fs, T['muted'])
            break
        cv.rect((x, y, x + w, y + rowh - 8), fill=T['panel2'], outline=T['yellow'] if changed else T['border'],
                width=3 if changed else 1, r=10)
        cv.text((x + 12, y + (rowh - 8) / 2), s, fs, T['yellow'] if changed else T['text'], anchor='lm', mono=True)
        x += w + 10
    if not items:
        cv.text((x0 + 18, y0 + 44), '{ }  空', 24, T['dim'], mono=True)


def _sortkey(x):
    return (str(type(x)), x) if not isinstance(x, (list, dict, set)) else (str(type(x)), str(x))


def h_map(spec):
    return spec.get('h', 130)


# ------------------------------------------------------------------ stack / queue
def v_stack(cv, spec, st, box, vi, ctx):
    S, B = st['_S'], st['_B']
    x0, y0, x1, y1 = box
    name = spec['var']
    kind = spec.get('type')
    head = {'stack': '栈底 → 栈顶', 'queue': '队首 → 队尾', 'heap': '堆（数组形式，堆顶在最左）'}.get(kind, '')
    label(cv, box, f"{spec.get('label', name)}   {head}")
    d = ev(name, S)
    if d is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    items = list(d)
    bd = ev(name, B)
    bl = list(bd) if bd is not None else []
    f = spec.get('fmt')
    fs = spec.get('font', 26)
    x, y = x0 + 18, y0 + 44
    hgt = fs + 30
    # how many of the old items survive at the front (queue popleft shifts everything left)
    keep = 0
    for s in range(len(bl) + 1):
        tail = bl[s:]
        if len(tail) <= len(items) and all(eq(a, b) for a, b in zip(tail, items)):
            keep = len(tail)
            break
    for k, it in enumerate(items):
        s = f(it) if f else fmt(it, 14)
        w = max(56, cv.tlen(s, fs, mono=True) + 28)
        if x + w > x1 - 20:
            cv.text((x, y + hgt / 2), '…', fs, T['muted'], anchor='lm')
            break
        is_new = k >= keep
        top = (kind == 'stack' and k == len(items) - 1) or (kind in ('queue', 'heap') and k == 0)
        c = T['green'] if is_new else (col(spec.get('top_color', 'purple')) if top else T['panel2'])
        cv.rect((x, y, x + w, y + hgt), fill=c if c != T['panel2'] else T['panel2'], r=10,
                outline=T['border'], width=1)
        cv.text((x + w / 2, y + hgt / 2), s, fs, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', mono=True, bold=True)
        x += w + 8
    popped = len(bl) - len(items)
    if popped > 0 and kind == 'stack':
        cv.text((x + 10, y + hgt / 2), f'← 弹出 {popped} 个', 22, T['red'], anchor='lm', bold=True)
    if not items:
        cv.text((x0 + 18, y + hgt / 2), '空', 24, T['dim'], anchor='lm')
        if popped > 0 and kind == 'stack':
            cv.rect((x0 + 60, y, x0 + 280, y + hgt), fill=T['panel'])
            cv.text((x0 + 70, y + hgt / 2), f'← 弹出 {popped} 个', 22, T['red'], anchor='lm', bold=True)


def h_stack(spec):
    return spec.get('h', 120)


# ------------------------------------------------------------------ grid / dp table
def v_grid(cv, spec, st, box, vi, ctx):
    S, B = st['_S'], st['_B']
    x0, y0, x1, y1 = box
    name = spec['var']
    label(cv, box, spec.get('label', name))
    g = ev(name, S)
    if g is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    g = [list(r) if not isinstance(r, str) else list(r) for r in g]
    bg = ev(name, B)
    R = len(g)
    C = max([len(r) for r in g] + [1])
    rows_l = ev(spec.get('rows'), S) if spec.get('rows') is not None else None
    cols_l = ev(spec.get('cols'), S) if spec.get('cols') is not None else None
    hx = 40 if rows_l is not None else 0
    hy = 32 if cols_l is not None else 0
    cell = min(spec.get('cell', 72), (x1 - x0 - 40 - hx) / C, (y1 - y0 - 50 - hy) / max(1, R))
    sx = x0 + 20 + hx + ((x1 - x0 - 40 - hx) - cell * C) / 2
    sy = y0 + 40 + hy
    fs = int(max(12, min(30, cell * 0.42)))
    color_fn = spec.get('color')
    for j in range(C):
        if cols_l is not None and j < len(cols_l):
            cv.text((sx + j * cell + cell / 2, sy - 6), fmt(cols_l[j], 4), 18, T['muted'], anchor='mb', mono=True)
    for i in range(R):
        if rows_l is not None and i < len(rows_l):
            cv.text((sx - 10, sy + i * cell + cell / 2), fmt(rows_l[i], 4), 18, T['muted'], anchor='rm', mono=True)
        for j in range(len(g[i])):
            v = g[i][j]
            c = None
            if color_fn:
                try:
                    c = color_fn(S, i, j, v)
                except Exception:
                    c = None
            changed = False
            try:
                changed = bg is not None and bg[i][j] != v
            except Exception:
                changed = bg is not None
            X, Y = sx + j * cell, sy + i * cell
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=col(c) if c else T['panel2'], r=6,
                    outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
            if spec.get('values', True):
                s = fmt(v, 4)
                cv.text((X + cell / 2, Y + cell / 2), s, fs, T['bg'] if c else T['text'], anchor='mm', bold=True)
    for k, cur in enumerate(spec.get('cursors') or []):
        ri, ci = ev(cur[0], S), ev(cur[1], S)
        c = col(cur[2] if len(cur) > 2 else PALETTE[k])
        if isinstance(ri, int) and isinstance(ci, int) and 0 <= ri < R and 0 <= ci < C:
            X, Y = sx + ci * cell, sy + ri * cell
            cv.rect((X - 1, Y - 1, X + cell + 1, Y + cell + 1), outline=c, width=4, r=8)
            if len(cur) > 3:
                cv.text((X + cell / 2, Y - 2), cur[3], 18, c, anchor='mb', bold=True)


def h_grid(spec):
    return spec.get('h', 320)


# ------------------------------------------------------------------ linked list
def _all_nodes(S, cls=(tracer.ListNode, tracer.Node)):
    found = {}

    def walk(x, depth=0):
        if depth > 3:
            return
        if isinstance(x, cls):
            cur = x
            while cur is not None and cur._uid not in found:
                found[cur._uid] = cur
                if getattr(cur, 'random', None) is not None:
                    walk(cur.random, depth + 1)
                cur = cur.next
        elif isinstance(x, (list, tuple, set)):
            for y in x:
                walk(y, depth + 1)
        elif isinstance(x, dict):
            for k, y in x.items():
                walk(k, depth + 1); walk(y, depth + 1)
    for v in S.values():
        walk(v)
    return found


def v_linked(cv, spec, st, box, vi, ctx):
    S, B = st['_S'], st['_B']
    x0, y0, x1, y1 = box
    label(cv, box, spec.get('label', '链表'))
    nodes = _all_nodes(all_vals(st))
    pos = ctx.get('ll_pos', {})
    nrows = max([p[0] for p in pos.values()] + [0]) + 1
    ncols = max([p[1] for p in pos.values()] + [0]) + 1
    gap = min(130, (x1 - x0 - 60) / max(1, ncols))
    rowh = min(150, (y1 - y0 - 60) / max(1, nrows))
    nw, nh = min(70, gap * 0.62), 48

    def xy(uid):
        r, c = pos.get(uid, (nrows - 1, 0))
        return x0 + 30 + c * gap + nw / 2, y0 + 70 + r * rowh + nh / 2 + 20

    ptrs = spec.get('pointers') or {}
    hit = {}
    for k, (name, c) in enumerate(ptrs.items()):
        v = ev(name, S)
        if isinstance(v, (tracer.ListNode, tracer.Node)):
            hit.setdefault(v._uid, []).append((name, col(c, PALETTE[k % len(PALETTE)])))
    # arrows
    for uid, nd in nodes.items():
        X, Y = xy(uid)
        nx = nd.next
        if nx is not None:
            X2, Y2 = xy(nx._uid)
            if abs(Y2 - Y) < 1 and 0 < X2 - X <= gap * 1.01:
                cv.arrow((X + nw / 2, Y), (X2 - nw / 2 - 2, Y2), T['muted'], 3, 11)
            else:
                lift = 40 + abs(X2 - X) * 0.12 if Y2 <= Y else -40
                cv.arc_arrow((X, Y - nh / 2), (X2, Y2 - nh / 2) if Y2 <= Y + 1 else (X2, Y2 - nh / 2), lift,
                             T['muted'], 3, 11)
        else:
            cv.text((X + nw / 2 + 6, Y), '∅', 22, T['dim'], anchor='lm')
        rnd = getattr(nd, 'random', None)
        if rnd is not None:
            X2, Y2 = xy(rnd._uid)
            cv.arc_arrow((X, Y + nh / 2), (X2 + 6, Y2 + nh / 2), -(30 + abs(X2 - X) * 0.1), T['purple'], 2, 9)
    for uid, nd in nodes.items():
        X, Y = xy(uid)
        hs = hit.get(uid, [])
        c = hs[0][1] if hs else None
        cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=c if c else T['panel2'], r=10,
                outline=T['border'], width=2)
        cv.text((X, Y), fmt(nd.val, 5), 24, T['bg'] if c else T['text'], anchor='mm', bold=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X, Y - nh / 2 - 6 - r * 24), name, 20, cc, anchor='mb', bold=True)
    # pointers that are None
    nones = [n for n in ptrs if n in S and S[n] is None]
    if nones:
        cv.text((x1 - 20, y0 + 6), '  '.join(f'{n}=None' for n in nones), 20, T['muted'], anchor='ra', mono=True)


def h_linked(spec):
    return spec.get('h', 220)


def linked_positions(steps_S):
    """stable (row, col) for every list node seen in any snapshot"""
    pos = dict(tracer._origin)
    max_row = max([p[0] for p in pos.values()] + [-1])
    new_uids = set()
    for S in steps_S:
        for uid in _all_nodes(S):
            if uid not in pos:
                new_uids.add(uid)
    for c, uid in enumerate(sorted(new_uids)):
        pos[uid] = (max_row + 1, c)
    return pos


# ------------------------------------------------------------------ tree
def _tree_roots(A, spec, S):
    r = ev(spec.get('var'), S) if spec.get('var') else None
    if isinstance(r, tracer.TreeNode):
        return [r]
    nodes = {}

    def walk(x, d=0):
        if d > 3:
            return
        if isinstance(x, tracer.TreeNode):
            stack = [x]
            while stack:
                n = stack.pop()
                if n is None or n._uid in nodes:
                    continue
                nodes[n._uid] = n
                stack += [n.left, n.right]
        elif isinstance(x, (list, tuple)):
            for y in x:
                walk(y, d + 1)
        elif isinstance(x, dict):
            for y in x.values():
                walk(y, d + 1)
    for v in A.values():
        walk(v)
    kids = set()
    for n in nodes.values():
        for ch in (n.left, n.right):
            if ch is not None:
                kids.add(ch._uid)
    roots = [n for u, n in sorted(nodes.items()) if u not in kids]
    if not roots and nodes:  # temporary cycle (Morris traversal): fall back to the smallest uid
        roots = [nodes[min(nodes)]]
    return roots


def v_tree(cv, spec, st, box, vi, ctx):
    S = st['_S']
    x0, y0, x1, y1 = box
    label(cv, box, spec.get('label', spec.get('var') or '二叉树'))
    roots = _tree_roots(all_vals(st), spec, S)
    if not roots:
        cv.text((x0 + 18, y0 + 44), '（空树）', 24, T['dim'])
        return
    order, depth = [], {}

    def ino(n, d):
        if n is None or n._uid in depth:
            return
        depth[n._uid] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    for r in roots:
        ino(r, 0)
    xi = {n._uid: i for i, n in enumerate(order)}
    maxd = max(depth.values()) + 1
    sp = min(78, (x1 - x0 - 60) / max(1, len(order)))
    dy = min(95, (y1 - y0 - 80) / max(1, maxd))
    rad = max(14, min(26, sp * 0.4, dy * 0.32))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2

    def P(n):
        return sx + xi[n._uid] * sp, y0 + 60 + depth[n._uid] * dy + rad

    for n in order:
        X, Y = P(n)
        for ch in (n.left, n.right):
            if ch is not None and ch._uid in xi:
                X2, Y2 = P(ch)
                cv.line([(X, Y), (X2, Y2)], T['border'], 3)
    path = set()
    for fr in (st.get('_frames', []) if spec.get('path', True) else []):
        for a in fr['args']:
            v = fr['locals'].get(a)
            if isinstance(v, tracer.TreeNode):
                path.add(v._uid)
    ptrs = spec.get('pointers') or {}
    hit = {}
    for k, (name, c) in enumerate(ptrs.items()):
        v = ev(name, S)
        if isinstance(v, tracer.TreeNode):
            hit.setdefault(v._uid, []).append((name, col(c, PALETTE[k % len(PALETTE)])))
    color_fn = spec.get('color')
    for n in order:
        X, Y = P(n)
        c = None
        if color_fn:
            try:
                c = color_fn(S, n)
            except Exception:
                c = None
        fill = col(c) if c else ((70, 60, 30) if n._uid in path else T['panel2'])
        outline = T['yellow'] if n._uid in path else T['border']
        hs = hit.get(n._uid, [])
        if hs:
            outline = hs[0][1]
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outline, width=4 if (hs or n._uid in path) else 2)
        cv.text((X, Y), fmt(n.val, 4), int(rad * 0.95), T['bg'] if c else T['text'], anchor='mm', bold=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X + rad + 4, Y - rad - r * 22), name, 19, cc, anchor='lb', bold=True)
    if path:
        cv.text((x1 - 20, y0 + 6), '黄圈 = 当前递归路径', 19, T['yellow'], anchor='ra')


def h_tree(spec):
    return spec.get('h', 380)


# ------------------------------------------------------------------ call stack
def v_calls(cv, spec, st, box, vi, ctx):
    x0, y0, x1, y1 = box
    frames = st.get('_frames', [])
    label(cv, box, spec.get('label', f'调用栈（深度 {len(frames)}）'))
    show = list(reversed(frames))
    maxn = max(1, int((y1 - y0 - 44) // 34))
    y = y0 + 40
    for k, fr in enumerate(show[:maxn]):
        hide = set(spec.get('hide', ()))
        args = ', '.join(f'{a}={fmt_var(fr["locals"].get(a), 12)}' for a in fr['args'] if a != 'self' and a not in hide)
        s = f'{fr["name"]}({args})'
        while len(s) > 8 and cv.tlen(s, 20, mono=True) > (x1 - x0 - 60):
            s = s[:-2] + '…'
            s = s[:-2] + '…' if cv.tlen(s, 20, mono=True) > (x1 - x0 - 60) else s
            if cv.tlen(s, 20, mono=True) <= (x1 - x0 - 60):
                break
        cv.rect((x0 + 18, y, x1 - 18, y + 30), fill=T['panel2'] if k else (60, 52, 30), r=8)
        cv.text((x0 + 30, y + 15), s, 20, T['yellow'] if k == 0 else T['muted'], anchor='lm', mono=True)
        y += 34
    if len(show) > maxn:
        cv.text((x0 + 30, y), f'… 还有 {len(show) - maxn} 层', 18, T['dim'])


def h_calls(spec):
    return spec.get('h', 180)


# ------------------------------------------------------------------ intervals
def v_intervals(cv, spec, st, box, vi, ctx):
    S = st['_S']
    x0, y0, x1, y1 = box
    label(cv, box, spec.get('label', spec['var'] if isinstance(spec['var'], str) else '区间'))
    rows = [(spec['var'], T['blue'])] + ([(spec['out'], T['green'])] if spec.get('out') else [])
    allv = []
    for name, _ in rows:
        for it in (ev(name, S) or []):
            allv += list(it)
    if not allv:
        return
    lo, hi = min(allv), max(allv)
    span = max(1, hi - lo)
    L, R = x0 + 50, x1 - 40

    def X(v):
        return L + (v - lo) / span * (R - L)
    y = y0 + 50
    ptr = ev(spec.get('pointer'), S) if spec.get('pointer') else None
    for name, c in rows:
        arr = ev(name, S) or []
        cv.text((x0 + 18, y), name, 20, T['muted'])
        y += 26
        for k, (a, b) in enumerate(arr):
            cc = T['yellow'] if (name == spec['var'] and ptr == k) else c
            cv.rect((X(a), y, max(X(b), X(a) + 6), y + 18), fill=cc, r=9)
            cv.text((X(a) - 6, y + 9), str(a), 18, T['muted'], anchor='rm')
            cv.text((max(X(b), X(a) + 6) + 6, y + 9), str(b), 18, T['muted'], anchor='lm')
            y += 26
        y += 12
    for v in range(int(lo), int(hi) + 1):
        if span <= 20 or v % 2 == 0:
            cv.text((X(v), y1 - 26), str(v), 16, T['dim'], anchor='mt')


def h_intervals(spec):
    return spec.get('h', 300)


# ------------------------------------------------------------------ free text
def v_text(cv, spec, st, box, vi, ctx):
    S = st['_S']
    x0, y0, x1, y1 = box
    t = spec.get('text')
    if spec.get('fn'):
        try:
            fn = spec['fn']
            t = fn(S, st['_B']) if getattr(fn, '__code__', None) and fn.__code__.co_argcount == 2 else fn(S)
        except Exception:
            t = None
    if t:
        # shrink the font until the text fits the view's height (narrow panels used to wrap into the next view)
        from engine import Canvas
        size = spec.get('size', 28)
        lines = spec.get('lines', 2)
        avail = (y1 - y0) - 6
        scratch = Canvas()
        while size > 16:
            need = scratch.rich(0, 0, t, x1 - x0 - 44, size=size, line_gap=1.4)
            if need <= avail or need <= size * 1.4 * 1.01 and avail < size * 1.4:
                break
            size -= 2
        cv.rich(x0 + 22, y0 + 8, t, x1 - x0 - 44, size=size, accent=ctx['accent'], max_lines=lines, line_gap=1.4)


def h_text(spec):
    return spec.get('h', 56)


def v_custom(cv, spec, st, box, vi, ctx):
    """spec['draw'](cv, S, B, box, T) — free drawing with the Canvas API"""
    try:
        spec['draw'](cv, st['_S'], st['_B'], box, T)
    except Exception as ex:  # keep rendering even if a custom drawer hits a missing var
        pass


def h_custom(spec):
    return spec.get('h', 200)


VIEWS = {
    'custom': (v_custom, h_custom),
    'array': (v_array, h_array), 'bars': (v_array, h_array), 'string': (v_array, h_array),
    'map': (v_map, h_map), 'set': (v_map, h_map),
    'stack': (v_stack, h_stack), 'queue': (v_stack, h_stack), 'heap': (v_stack, h_stack),
    'grid': (v_grid, h_grid), 'table': (v_grid, h_grid),
    'linked': (v_linked, h_linked), 'tree': (v_tree, h_tree), 'calls': (v_calls, h_calls),
    'intervals': (v_intervals, h_intervals), 'text': (v_text, h_text),
}
