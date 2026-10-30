def _tree(S):
    seg = S.get('self.seg')
    if seg:
        return seg
    t = S.get('t')
    return getattr(t, 'seg', None)


def _cur_idx(S):
    ev = S.get('events')
    if not ev or 'delta' not in S or 'lx' not in S:
        return None
    try:
        return ev.index((S['y'], S['lx'], S['rx'], S['delta']))
    except ValueError:
        return None


def _applied(S):
    """sweep 扫到的事件里，已经 update 过的有几个（含当前这个，若 update 已执行）"""
    ev = S.get('events')
    if not ev:
        return 0
    idx = _cur_idx(S)
    if idx is None:
        return len(ev) if 'records' in S and 'i' in S else 0
    ln = S.get('_line', 0)
    mid = ln in (27, 28, 32, 33, 37, 38) or 57 <= ln <= 66 or 90 <= ln <= 93
    return idx + (0 if mid else 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    sq = S.get('squares')
    xs = S.get('xs')
    ev = S.get('events')
    if not sq or not xs or not ev:
        return
    cv.text((x0 + 18, y0 + 4), '扫描线 · 绿 = 已扫面积', 24, T['muted'], bold=True)
    X0, X1 = min(xs), max(xs)
    ys = sorted({e[0] for e in ev})
    Y0, Y1 = ys[0], ys[-1]
    side = 300
    sc = min(side / (X1 - X0), side / (Y1 - Y0))
    ox, oy = x0 + 60, y1 - 60
    px = lambda x: ox + (x - X0) * sc
    py = lambda y: oy - (y - Y0) * sc
    cur = _cur_idx(S)
    nap = _applied(S)
    ycur = ev[min(cur, len(ev) - 1)][0] if cur is not None else (Y1 if 'records' in S and 'tot_area' in S and 'i' in S else Y0)
    if nap == 0 and cur is None:
        ycur = Y0
    # 并集面积（只画 y < ycur 的部分），按 xs 的基本区间逐列算
    for k in range(len(xs) - 1):
        a, b = xs[k], xs[k + 1]
        segs = sorted((max(y, Y0), min(y + l, ycur)) for (x, y, l) in sq if x <= a and b <= x + l and y < ycur)
        cur_lo = cur_hi = None
        for lo, hi in segs:
            if hi <= lo:
                continue
            if cur_hi is None or lo > cur_hi:
                if cur_hi is not None:
                    cv.rect((px(a), py(cur_hi), px(b), py(cur_lo)), fill=T['green'], alpha=120)
                cur_lo, cur_hi = lo, hi
            else:
                cur_hi = max(cur_hi, hi)
        if cur_hi is not None:
            cv.rect((px(a), py(cur_hi), px(b), py(cur_lo)), fill=T['green'], alpha=120)
    cols = ['blue', 'pink', 'purple', 'cyan', 'orange']
    for i, (x, y, l) in enumerate(sq):
        cv.rect((px(x), py(y + l), px(x + l), py(y)), outline=T[cols[i % 5]], width=4)
    # 坐标轴刻度
    for x in xs:
        cv.text((px(x), oy + 10), x, 20, T['dim'], anchor='mt', mono=True)
    for y in ys:
        cv.text((ox - 12, py(y)), y, 20, T['dim'], anchor='rm', mono=True)
    cv.line([(ox, oy), (px(X1) + 10, oy)], T['border'], 2)
    # 扫描线
    if cur is not None or 'records' in S:
        cv.line([(ox - 6, py(ycur)), (px(X1) + 24, py(ycur))], T['yellow'], 4)
        cv.text((px(X1) + 30, py(ycur)), f'y={ycur}', 22, T['yellow'], anchor='lm', bold=True)
    # 线段树
    tr = _tree(S)
    if not tr:
        return
    tx0 = x0 + 400
    cv.text((tx0, y0 + 4), '线段树：min_cover / 长度 / todo', 22, T['muted'], bold=True)
    n = len(xs) - 1
    if tr[1].r <= 0 and n > 1:
        return
    pos = {}

    def lay(o, l, r, d, lo, hi):
        pos[o] = ((lo + hi) / 2, y0 + 90 + d * 120, l, r, hi - lo)
        if l == r:
            return
        m = (l + r) // 2
        mid = (lo + hi) / 2
        lay(o * 2, l, m, d + 1, lo, mid)
        lay(o * 2 + 1, m + 1, r, d + 1, mid, hi)

    lay(1, 0, n - 1, 0, tx0, x1 - 10)
    Bt = _tree(B)
    for o, (cx, cy, l, r, ww) in pos.items():
        if o * 2 in pos:
            for c in (o * 2, o * 2 + 1):
                cv.line([(cx, cy + 34), (pos[c][0], pos[c][1] - 34)], T['border'], 2)
    for o, (cx, cy, l, r, ww) in pos.items():
        nd = tr[o]
        ch = False
        if Bt is not None and o < len(Bt):
            b = Bt[o]
            ch = (b.min_cover, b.min_cover_len, b.todo) != (nd.min_cover, nd.min_cover_len, nd.todo)
        w = min(150, ww * 0.92)
        cv.rect((cx - w / 2, cy - 34, cx + w / 2, cy + 34), fill=(30, 36, 46),
                outline=T['yellow'] if ch else T['border'], width=4 if ch else 2, r=8)
        cv.text((cx, cy - 26), f'[{xs[l]},{xs[r + 1]})', 18, T['dim'], anchor='mt', mono=True)
        cv.text((cx, cy + 2), f'{nd.min_cover}/{nd.min_cover_len}/{nd.todo}', 24, T['text'], anchor='mt', bold=True, mono=True)


def _line_text(S):
    if 'sum_len' in S and 'tot_area' in S and 'e2' in S:
        y, y2 = S['y'], S['e2'][0]
        return f"本段 y∈[`{y}`, `{y2}`)：覆盖宽 `sum_len` = ==`{S['sum_len']}`==，新增面积 `{S['sum_len']} × {y2 - y}`，累计 `tot_area` = ==`{S['tot_area']}`=="
    if 'records' in S and 'tot_area' in S and 'area' in S:
        return f"`tot_area` = {S['tot_area']}，一半 = {S['tot_area'] / 2}；在 `area = {S['area']}`、`sum_len = {S['sum_len']}` 这一段里补足"
    if 'tot_area' in S:
        return f"第一遍扫描：累计并集面积 `tot_area` = ==`{S['tot_area']}`=="
    return '先建离散化后的线段树，再让扫描线从下往上走'


CONFIG = dict(
    num=3454, title='分割正方形 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='扫描线 + Lazy 线段树 + 二分',
    tags=['灵神题单', '常用数据结构', '难度分 2671'],
    code='''
class Node:
    __slots__ = 'l', 'r', 'min_cover_len', 'min_cover', 'todo'

    def __init__(self):
        self.l = 0
        self.r = 0
        self.min_cover_len = 0  # 区间内被矩形覆盖次数最少的底边长之和
        self.min_cover = 0      # 区间内被矩形覆盖的最小次数
        self.todo = 0           # 子树内的所有节点的 min_cover 需要增加的量，注意这可以是负数

class SegmentTree:
    def __init__(self, xs: List[int]):
        n = len(xs) - 1  # xs.size() 个横坐标有 xs.size()-1 个差值
        self.seg = [Node() for _ in range(2 << (n - 1).bit_length())]
        self.build(xs, 1, 0, n - 1)

    def get_uncovered_length(self) -> int:
        return 0 if self.seg[1].min_cover else self.seg[1].min_cover_len

    # 根据左右儿子的信息，更新当前节点的信息
    def maintain(self, o: int) -> None:
        lo = self.seg[o * 2]
        ro = self.seg[o * 2 + 1]
        mn = min(lo.min_cover, ro.min_cover)
        self.seg[o].min_cover = mn
        # 只统计等于 min_cover 的底边长之和
        self.seg[o].min_cover_len = (lo.min_cover_len if lo.min_cover == mn else 0) + \\
                                    (ro.min_cover_len if ro.min_cover == mn else 0)

    # 仅更新节点信息，不下传懒标记 todo
    def do(self, o: int, v: int) -> None:
        self.seg[o].min_cover += v
        self.seg[o].todo += v

    # 下传懒标记 todo
    def spread(self, o: int) -> None:
        v = self.seg[o].todo
        if v:
            self.do(o * 2, v)
            self.do(o * 2 + 1, v)
            self.seg[o].todo = 0

    # 建树
    def build(self, xs: List[int], o: int, l: int, r: int) -> None:
        self.seg[o].l = l
        self.seg[o].r = r
        if l == r:
            self.seg[o].min_cover_len = xs[l + 1] - xs[l]
            return
        m = (l + r) // 2
        self.build(xs, o * 2, l, m)
        self.build(xs, o * 2 + 1, m + 1, r)
        self.maintain(o)

    # 区间更新
    def update(self, o: int, l: int, r: int, v: int) -> None:
        if l <= self.seg[o].l and self.seg[o].r <= r:
            self.do(o, v)
            return
        self.spread(o)
        m = (self.seg[o].l + self.seg[o].r) // 2
        if l <= m:
            self.update(o * 2, l, r, v)
        if m < r:
            self.update(o * 2 + 1, l, r, v)
        self.maintain(o)

# 代码逻辑同 850 题，增加一个 records 数组记录关键数据
class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        xs = []
        events = []
        for lx, y, l in squares:
            rx = lx + l
            xs.append(lx)
            xs.append(rx)
            events.append((y, lx, rx, 1))
            events.append((y + l, lx, rx, -1))

        # 排序，方便离散化
        xs = sorted(set(xs))

        # 初始化线段树
        t = SegmentTree(xs)

        # 模拟扫描线从下往上移动
        events.sort(key=lambda e: e[0])
        records = []
        tot_area = 0
        for (y, lx, rx, delta), e2 in pairwise(events):
            l = bisect_left(xs, lx)  # 离散化
            r = bisect_left(xs, rx) - 1  # r 对应着 xs[r] 与 xs[r+1]=rx 的差值
            t.update(1, l, r, delta)  # 更新被 [lx, rx] 覆盖的次数
            sum_len = xs[-1] - xs[0] - t.get_uncovered_length()  # 减去没被矩形覆盖的长度
            records.append((tot_area, sum_len))  # 记录关键数据
            tot_area += sum_len * (e2[0] - y)  # 新增面积 = 被至少一个矩形覆盖的底边长之和 * 矩形高度

        # 二分找最后一个 < tot_area / 2 的面积
        i = bisect_left(records, tot_area, key=lambda r: r[0] * 2) - 1
        area, sum_len = records[i]
        return events[i][0] + (tot_area - area * 2) / (sum_len * 2)
''',
    call='Solution().separateSquares([[0, 0, 2], [1, 1, 1]])',
    expect=1.0,
    views=[
        dict(type='text', fn=_line_text, size=24, h=80),
        dict(type='custom', draw=_draw, h=470),
        dict(type='array', var='xs', label='xs（离散化后的横坐标）', h=110, cell=70),
    ],
    watch=['y', ('sum_len', 'sum_len', 'cyan'), ('tot_area', 'tot_area', 'green'), 'records', 'area'],
    skip=['self.seg[o].l = l', 'self.seg[o].r = r', 'self.l = 0', 'self.r = 0', 'self.min_cover_len = 0', 'self.min_cover = 0',
          'self.todo = 0', 'xs.append', 'rx = lx + l', 'lo = self.seg', 'ro = self.seg', 'mn = min', 'self.seg[o].min_cover = mn',
          'm = (l + r) // 2', 'm = (self.seg', 'v = self.seg[o].todo', 'self.seg = [Node()', 'if v:', 'self.do(o * 2', 'self.seg[o].todo = 0',
          'self.seg[o].todo += v', '(ro.min_cover_len if', 'self.spread(o)', 'self.build(xs, o * 2', 'self.do(o, v)', 'self.build(xs, 1, 0', 'self.maintain(o)', 'events.sort', 'records = []', 'tot_area = 0', 'xs = []', 'events = []'],
    max_steps=46,
    captions={
        'xs = sorted': '横坐标去重排序：`xs = {xs}`；相邻两个横坐标围成一个基本区间，就是线段树的叶子',
        'events.append((y, lx, rx, 1))': '正方形的==下边==：扫到 `y = {y}` 开始覆盖 `[{lx}, {rx}]` → 事件 `+1`',
        'events.append((y + l': '正方形的==上边==：扫到 `y = {y + l}` 结束覆盖 → 事件 `-1`',
        't.update(1, l, r, delta)': lambda S, B, r: f'扫描线到 `y = {S.y}`：叶子区间 `[{S.l}, {S.r}]` 的覆盖次数 =={"+1" if S.delta > 0 else "-1"}==',
        'sum_len = xs[-1]': lambda S, B, r: f'总宽 `{S.xs[-1] - S.xs[0]}` 减去没被盖住的 `{S.xs[-1] - S.xs[0] - S.sum_len}` → 被至少一个正方形盖住的宽 `sum_len` = =={S.sum_len}==',
        'records.append': '记下这一段开始前的面积 `{tot_area}` 和这一段的覆盖宽 `{sum_len}`，第二遍不用再跑线段树',
        'tot_area +=': '这一段 `y ∈ [{y}, {e2[0]})`：新增面积 = `{sum_len} × {e2[0] - y}`，`tot_area` → =={tot_area}==',
        'i = bisect_left': '二分：最后一个 `area × 2 < tot_area` 的记录（`tot_area = {tot_area}`）→ `i = {i}`，答案就落在这一段里',
        'area, sum_len = records': '这一段开始时下方面积 `area = {area}`，这一段的覆盖宽 `sum_len = {sum_len}`',
        'return events[i][0]': lambda S, B, r: f'`y = {S.events[S.i][0]} + ({S.tot_area} − 2×{S.area}) / (2×{S.sum_len})` = =={r}==：还差的面积除以覆盖宽，就是在这一段里再升多高',
        'self.seg[o].min_cover += v': '这个节点的区间被整段覆盖：`min_cover` 直接加 `{v}`，并记下懒标记 `todo`，不往下推',
        'self.seg[o].min_cover_len = (lo': '回溯合并：只累加 `min_cover` 等于较小值的那些底边长',
        'self.seg[o].min_cover_len = xs[l + 1]': '叶子：对应的基本区间长度 `xs[{l + 1}] - xs[{l}]` = {xs[l + 1] - xs[l]}',
        'return 0 if self.seg[1].min_cover': lambda S, B, r: (f'根的最小覆盖次数 `{S["self.seg"][1].min_cover}` > 0：整行都被盖住 → 没盖住的长度 =={r}=='
                                                           if S["self.seg"][1].min_cover else f'根的最小覆盖次数是 0：这部分就是没被盖住的，长度 =={r}=='),
    },
    cards=dict(
        one_liner='先扫一遍求并集总面积，再按面积一半找答案',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一些可能重叠的正方形 `[x, y, l]`，重叠部分只算一次',
                 '找最小的 `y`，使水平线下方的面积 = 上方的面积',
                 '本视频：`[[0,0,2],[1,1,1]]`（题目示例 2），并集面积 4，答案 `1.0`'],
        quote='首先用 850 题的扫描线方法，求出所有正方形的面积并 totArea。然后再次扫描，设扫描线下方的面积和为 area，那么扫描线上方的面积和为 totArea - area。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个正方形的下边/上边是事件，扫描线从下往上，用线段树维护「被覆盖的底边总长」',
              '线段树存的是覆盖次数的最小值及对应长度：最小值为 0 的那部分就是没被盖住的',
              '把每段的 (已有面积, 覆盖宽) 记下来，最后二分找到面积刚好过半的那一段，再补足'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '记录 `records` 是关键技巧：不用再跑第二遍线段树，直接二分',
                 '最后一步：`y + (totArea - 2·area) / (2·sum_len)`，在那一段里按比例补足',
                 '易错：`r = bisect_left(xs, rx) - 1`，线段树的叶子是相邻横坐标的间隔',
                 '同类题：850 矩形面积 II；灵神题单 §8.4 Lazy 线段树'],
    ),
)
