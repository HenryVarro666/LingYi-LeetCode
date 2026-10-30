LINES = [[1, 0], [2, 1], [2, 0], [3, 1], [3, 0]]


def _pts():
    out = []
    for i in range(len(LINES)):
        for j in range(i + 1, len(LINES)):
            (k1, b1), (k2, b2) = LINES[i], LINES[j]
            if k1 != k2:
                x = (b1 - b2) / (k2 - k1)
                out.append((x, k1 * x + b1))
    return out


PTS = _pts()
XMIN, XMAX = min(p[0] for p in PTS) - 1, max(p[0] for p in PTS) + 1
YMIN, YMAX = min(p[1] for p in PTS) - 1, max(p[1] for p in PTS) + 1
COLS = ['blue', 'pink', 'green', 'orange', 'purple']


def _fmt(v):
    return ('%g' % v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '直线（同色同斜率）· 灰点=全部交点 · 绿框=当前外接矩形', 21, T['muted'], bold=True)
    top, bot = y0 + 84, y1 - 22
    left, right = x0 + 60, x1 - 30
    sx = (right - left) / (XMAX - XMIN)
    sy = (bot - top) / (YMAX - YMIN)

    def P(x, y):
        return left + (x - XMIN) * sx, bot - (y - YMIN) * sy

    for gx in range(int(XMIN), int(XMAX) + 1):
        X = P(gx, 0)[0]
        cv.line([(X, top), (X, bot)], T['border'], 1)
        cv.text((X, bot + 2), gx, 16, T['dim'], anchor='mt', mono=True)
    for gy in range(int(YMIN), int(YMAX) + 1):
        Y = P(0, gy)[1]
        cv.line([(left, Y), (right, Y)], T['border'], 1)
        cv.text((left - 8, Y), gy, 16, T['dim'], anchor='rm', mono=True)
    ks = sorted(set(k for k, _ in LINES))
    cur = None
    if 'sorted_k' in S and 'index' in S and S['index'] + 1 < len(S['sorted_k']):
        cur = (S['sorted_k'][S['index']], S['sorted_k'][S['index'] + 1])
    for k, b in LINES:
        c = T[COLS[ks.index(k)]]
        if cur and k in cur:
            w = 4
        else:
            w = 2 if not cur else 1
        pa, pb = P(XMIN, k * XMIN + b), P(XMAX, k * XMAX + b)
        # 按画布裁剪
        pts = [pa, pb]
        try:
            from PIL import Image  # noqa
        except Exception:
            pass
        (ax, ay), (bx, by) = pts
        dx = bx - ax
        t0, t1_ = 0.0, 1.0
        dy = by - ay
        for p, q in ((-dx, ax - left), (dx, right - ax), (-dy, ay - top), (dy, bot - ay)):
            if p == 0:
                if q < 0:
                    t0, t1_ = 1, 0
            else:
                r = q / p
                if p < 0:
                    t0 = max(t0, r)
                else:
                    t1_ = min(t1_, r)
        if t0 < t1_:
            cv.line([(ax + dx * t0, ay + dy * t0), (ax + dx * t1_, ay + dy * t1_)], c, w)
    for x, y in PTS:
        X, Y = P(x, y)
        cv.d.ellipse((X - 5, Y - 5, X + 5, Y + 5), fill=T['muted'])
    if S.get('left_x') is not None:
        a, b = P(S['left_x'], S['top_y'])
        c, d = P(S['right_x'], S['botton_y'])
        cv.rect((a, b, c, d), fill=T['green'], alpha=40, outline=T['green'], width=3)
        cv.text((x0 + 18, y0 + 32), f"x∈[{_fmt(S['left_x'])}, {_fmt(S['right_x'])}]  y∈[{_fmt(S['botton_y'])}, {_fmt(S['top_y'])}]", 20, T['green'], bold=True)
    if cur:
        for k in cur:
            c = T[COLS[ks.index(k)]]
        kk = f'当前处理相邻斜率 k={cur[0]} 与 k={cur[1]}'
        cv.text((right, y0 + 32), kk, 20, T['yellow'], anchor='ra', bold=True)


def _cand(S):
    k1, k2 = S.k1, S.k2
    return dict(
        lx=(S.min_b[k1] - S.max_b[k2]) * 1.0 / (k2 - k1),
        rx=(S.max_b[k1] - S.min_b[k2]) * 1.0 / (k2 - k1),
    )


def _cap_left(S, B, ret):
    k1, k2 = S.k1, S.k2
    v = _cand(S)['lx']
    old = S.left_x
    tag = '更新' if (old is None or old > v) else '不更新'
    return (f'x 最小要 `b[k1]` 取最小、`b[k2]` 取最大：`({S.min_b[k1]} − {S.max_b[k2]}) / ({k2} − {k1}) = {_fmt(v)}`；'
            f'当前 `left_x = {old if old is None else _fmt(old)}` → =={tag}==')


def _cap_right(S, B, ret):
    k1, k2 = S.k1, S.k2
    v = _cand(S)['rx']
    old = S.right_x
    tag = '更新' if (old is None or old < v) else '不更新'
    return (f'x 最大要 `b[k1]` 取最大、`b[k2]` 取最小：`({S.max_b[k1]} − {S.min_b[k2]}) / ({k2} − {k1}) = {_fmt(v)}`；'
            f'当前 `right_x = {old if old is None else _fmt(old)}` → =={tag}==')


def _cap_top(S, B, ret):
    k1, k2 = S.k1, S.k2
    x = _cand(S)['rx']
    v = x * k1 + S.max_b[k1]
    old = S.top_y
    tag = '更新' if (old is None or old < v) else '不更新'
    return (f'y 最大：把最大的 x 代回 `k1 · x + max_b[k1] = {k1} × {_fmt(x)} + {S.max_b[k1]} = {_fmt(v)}`；'
            f'当前 `top_y = {old if old is None else _fmt(old)}` → =={tag}==')


def _cap_bot(S, B, ret):
    k1, k2 = S.k1, S.k2
    x = _cand(S)['lx']
    v = x * k1 + S.min_b[k1]
    old = S.botton_y
    tag = '更新' if (old is None or old > v) else '不更新'
    return (f'y 最小：把最小的 x 代回 `k1 · x + min_b[k1] = {k1} × {_fmt(x)} + {S.min_b[k1]} = {_fmt(v)}`；'
            f'当前 `botton_y = {old if old is None else _fmt(old)}` → =={tag}==')


CONFIG = dict(
    num='LCP 37', title='最小矩形面积', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='斜率排序 · 只看相邻直线',
    tags=['计算几何'],
    code='''
class Solution(object):
    def minRecSize(self, lines):

        if len(lines) <= 2:
            return 0.0
        
        k_set = set()
        max_b = {}
        min_b = {}
        for k, b in lines:
            if k not in k_set:
                k_set.add(k)
                max_b[k] = b
                min_b[k] = b
            else:
                max_b[k] = max(max_b[k], b)
                min_b[k] = min(min_b[k], b)

        if len(k_set) == 1:
            return 0.0

        left_x = right_x = top_y = botton_y = None
        sorted_k = sorted(list(k_set))
        for index in range(len(sorted_k) - 1):
            k1 = sorted_k[index]
            k2 = sorted_k[index + 1]
            if left_x is None or left_x > (min_b[k1] - max_b[k2]) * 1.0 / (k2 - k1):
                left_x = (min_b[k1] - max_b[k2]) * 1.0 / (k2 - k1)
            if right_x is None or right_x < (max_b[k1] - min_b[k2]) * 1.0 / (k2 - k1):
                right_x = (max_b[k1] - min_b[k2]) * 1.0 / (k2 - k1)
            if top_y is None or top_y < (max_b[k1] - min_b[k2]) * 1.0 / (k2 - k1) * k1 + max_b[k1]:
                top_y = (max_b[k1] - min_b[k2]) * 1.0 / (k2 - k1) * k1 + max_b[k1]
            if botton_y is None or botton_y > (min_b[k1] - max_b[k2]) * 1.0 / (k2 - k1) * k1 + min_b[k1]:
                botton_y = (min_b[k1] - max_b[k2]) * 1.0 / (k2 - k1) * k1 + min_b[k1]

        return (right_x - left_x) * (top_y - botton_y)
''',
    call=f'Solution().minRecSize({LINES})',
    expect=10.0,
    views=[dict(type='custom', draw=_draw, h=420),
           dict(type='map', var='max_b', h=95, fmt=lambda k, v: f'k={k}: b={v}', label='max_b（每个斜率下最大的 b）'),
           dict(type='map', var='min_b', h=95, fmt=lambda k, v: f'k={k}: b={v}', label='min_b（每个斜率下最小的 b）')],
    watch=[('index', 'index if "index" in S else "-"', 'blue'),
           ('left_x', '"-" if S.get("left_x") is None else "%g" % left_x', 'cyan'),
           ('right_x', '"-" if S.get("right_x") is None else "%g" % right_x', 'orange'),
           ('top_y', '"-" if S.get("top_y") is None else "%g" % top_y', 'pink'),
           ('botton_y', '"-" if S.get("botton_y") is None else "%g" % botton_y', 'purple')],
    captions={
        'if len(lines) <= 2': '`{len(lines)}` 条直线：至少 3 条才可能有多个交点；这里不止两条 → 继续',
        'k_set = set()': '`k_set` 存出现过的斜率',
        'max_b = {}': '`max_b[k]`：斜率为 k 的直线里最大的截距',
        'min_b = {}': '`min_b[k]`：斜率为 k 的直线里最小的截距',
        'for k, b in lines': lambda S, B, r: ('所有直线都统计完了' if 'b' in B and B.k == S.k and B.b == S.b else f'取直线 `y = {S.k}x + {S.b}`'),
        'if k not in k_set': lambda S, B, r: (f'斜率 `{S.k}` 是第一次出现' if S.k not in S.k_set else f'斜率 `{S.k}` 已经有直线了 → 只需比较截距'),
        'k_set.add(k)': '记下斜率 `{k}`',
        'max_b[k] = b': lambda S, B, r: f'第一条：`max_b[{S.k}] = {S.b}`',
        'min_b[k] = b': lambda S, B, r: f'第一条：`min_b[{S.k}] = {S.b}`',
        'max_b[k] = max': lambda S, B, r: f'同斜率平行线：只有 b 最大的和最小的会产生极端交点 → `max_b[{S.k}] = {S.max_b[S.k]}`',
        'min_b[k] = min': lambda S, B, r: f'`min_b[{S.k}] = {S.min_b[S.k]}`',
        'if len(k_set) == 1': lambda S, B, r: (f'只有 `{len(S.k_set)}` 种斜率，直线全平行 → 面积 0' if len(S.k_set) == 1 else f'共 `{len(S.k_set)}` 种斜率，不全平行 → 继续'),
        'left_x = right_x': '四个边界先置空：横坐标的最小/最大、纵坐标的最大/最小',
        'sorted_k = sorted': lambda S, B, r: f'斜率排序：`{S.sorted_k}` → 极端交点只会出现在==相邻斜率==之间',
        'for index in range': lambda S, B, r: ('所有相邻斜率对都处理完了' if 'index' in B and B.index == S.index else f'处理第 `{S.index}` 对相邻斜率'),
        'k1 = sorted_k': '`k1` = {k1}',
        'k2 = sorted_k': '`k2` = {k2}（相邻斜率）',
        'if left_x is None': _cap_left,
        'left_x = (': '`left_x` → =={left_x}==',
        'if right_x is None': _cap_right,
        'right_x = (': '`right_x` → =={right_x}==',
        'if top_y is None': _cap_top,
        'top_y = (': '`top_y` → =={top_y}==',
        'if botton_y is None': _cap_bot,
        'botton_y = (': '`botton_y` → =={botton_y}==',
        'return (right_x': '宽 `{right_x} − ({left_x}) = {right_x - left_x}`，高 `{top_y} − ({botton_y}) = {top_y - botton_y}` → 面积 =={ret}==',
    },
    cards=dict(
        one_liner='把直线按斜率排序，极端交点只会出现在相邻斜率之间',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给 `n` 条直线 `y = kx + b`（`k` 为正），求包住所有交点的==最小==轴平行矩形面积',
                 '只有一个交点或所有直线平行时，面积为 `0`',
                 '本视频：`[[1,0],[2,1],[2,0],[3,1],[3,0]]` → `10.0`'],
        quote='可以发现，横坐标最大和最小的点要么是k1和k2的交点，要么是k2和k3的交点。那么在这里可以大胆猜测，横坐标的最大值和最小值是否必然出现在k值相邻的直线中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先画图找规律：三条线相交于同一点再上下平移，极端点总在相邻斜率之间，并用代数分三种情况证明',
              '斜率相同的直线，只需保留 `b` 最大和最小的两条',
              '枚举相邻斜率：`x` 极大用 `max_b[k1]` 与 `min_b[k2]`，极小用 `min_b[k1]` 与 `max_b[k2]`；`k` 为正，`y` 与 `x` 同向变化'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`；暴力两两求交点是 `O(n²)` 会超时',
                 '易错：直线数 `≤ 2` 或斜率只有一种，要先返回 `0.0`',
                 'k1 < k2，所以最大 x 用「k1 取最大 b、k2 取最小 b」，别搞反',
                 '原文为 Python 2 风格，用 `* 1.0` 做浮点除，Python 3 下本就正确，代码未改动'],
    ),
)
