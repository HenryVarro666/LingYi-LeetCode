CODE = '''
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
        self.seg[o].min_cover_len = (lo.min_cover_len if lo.min_cover == mn else 0) + \
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

class Solution:
    def rectangleArea(self, rectangles: List[List[int]]) -> int:
        xs = []
        events = []
        for lx, ly, rx, ry in rectangles:
            xs.append(lx)
            xs.append(rx)
            events.append((ly, lx, rx, 1))
            events.append((ry, lx, rx, -1))

        # 排序，方便离散化
        xs = sorted(set(xs))

        # 初始化线段树
        t = SegmentTree(xs)

        # 模拟扫描线从下往上移动
        events.sort(key=lambda e: e[0])
        ans = 0
        for (y, lx, rx, delta), e2 in pairwise(events):
            l = bisect_left(xs, lx)  # 离散化
            r = bisect_left(xs, rx) - 1  # r 对应着 xs[r] 与 xs[r+1]=rx 的差值
            t.update(1, l, r, delta)  # 更新被 [lx, rx] 覆盖的次数
            sum_len = xs[-1] - xs[0] - t.get_uncovered_length()  # 减去没被矩形覆盖的长度
            ans += sum_len * (e2[0] - y)  # 新增面积 = 被至少一个矩形覆盖的底边长之和 * 矩形高度
        return ans % 1_000_000_007
'''
LINE_ANS = CODE.split('\n').index(next(l for l in CODE.split('\n') if 'ans += sum_len' in l))

RECTS = [[0, 0, 2, 2], [1, 1, 2, 3]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '扫描线从下往上：蓝框 = 矩形，绿 = 已统计的面积，黄线 = 扫描线', 22, T['muted'], bold=True)
    W, H = 2, 3
    cell = min((x1 - x0 - 140) / W, (y1 - y0 - 110) / H, 110)
    ox, oy = x0 + 70, y1 - 50
    P = lambda x, y: (ox + x * cell, oy - y * cell)
    for k in range(W + 1):
        cv.line([P(k, 0), P(k, H)], T['border'], 1)
        cv.text((P(k, 0)[0], oy + 8), k, 18, T['dim'], anchor='mt')
    for k in range(H + 1):
        cv.line([P(0, k), P(W, k)], T['border'], 1)
        cv.text((ox - 10, P(0, k)[1]), k, 18, T['dim'], anchor='rm')
    ys = None
    if 'y' in S:
        ys = S['e2'][0] if (S.get('_line', 0) >= LINE_ANS and 'e2' in S) else S['y']
    if ys is not None:
        for i in range(W):
            if any(r[0] <= i < r[2] for r in RECTS):
                for j in range(H):
                    if j < ys and any(r[0] <= i < r[2] and r[1] <= j < r[3] for r in RECTS):
                        a, b = P(i, j + 1), P(i + 1, j)
                        cv.rect((a[0] + 1, a[1] + 1, b[0] - 1, b[1] - 1), fill=T['green'], alpha=140)
    for r in RECTS:
        a, b = P(r[0], r[3]), P(r[2], r[1])
        cv.rect((a[0], a[1], b[0], b[1]), outline=T['blue'], width=4)
    if 'y' in S:
        a, b = P(0, S['y']), P(W, S['y'])
        cv.line([a, b], T['yellow'], 4)
        cv.text((b[0] + 8, b[1]), f"y={S['y']}", 22, T['yellow'], anchor='lm', bold=True)
        if 'lx' in S:
            c = T['red'] if S['delta'] < 0 else T['orange']
            cv.line([P(S['lx'], S['y']), P(S['rx'], S['y'])], c, 8)


def _nodes(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '线段树节点：[横坐标区间]  min_cover / min_cover_len / todo', 22, T['muted'], bold=True)
    t = S.get('t')
    if t is None and 'self' in S and hasattr(S['self'], 'seg'):
        t = S['self']
    if t is None:
        return
    xs = S.get('xs')
    y = y0 + 44
    for o in range(1, 4):
        nd = t.seg[o]
        if nd.r < nd.l:
            continue
        depth = o.bit_length() - 1
        txt = f"seg[{o}]  [{nd.l},{nd.r}]  cover={nd.min_cover}  len={nd.min_cover_len}  todo={nd.todo}"
        cv.text((x0 + 24 + depth * 40, y), txt, 22, T['yellow'] if nd.min_cover > 0 else T['text'], mono=True)
        y += 32


CONFIG = dict(
    num=850, title='矩形面积 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='扫描线 + Lazy 线段树',
    tags=['常用数据结构', '难度分 2236'],
    code=CODE,
    call='Solution().rectangleArea([[0,0,2,2],[1,1,2,3]])',
    expect=5,
    skip=[48, 58, 'self.seg[o].todo = 0', 'n = len(xs) - 1', 'events.append', 'ans = 0', 'self.do(o * 2', 'self.seg = [Node()', 'l = bisect_left', 'r = bisect_left', 'xs.append', 'xs = []', 'events = []', 'self.l = 0', 'self.r = 0', 'self.min_cover_len = 0', 'self.min_cover = 0', 'self.todo = 0',
          'self.seg[o].l = l', 'self.seg[o].r = r', 'self.seg[o].min_cover += v', 'self.seg[o].todo += v',
          'mn = min', 'self.seg[o].min_cover = mn', 'lo = ', 'ro = ', 'm = (', 'v = self.seg[o].todo'],
    max_steps=110,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='custom', draw=_nodes, h=250),
    ],
    watch=[('y', 'y', 'yellow'), ('delta', 'delta', 'orange'), ('sum_len', 'sum_len', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'xs = sorted(set(xs))': '横坐标太大，==离散化==：去重排序得 `xs = {xs}`，相邻两个横坐标围成一段底边',
        'n = len(xs) - 1': '`xs` 有 `{len(xs)}` 个横坐标 → `{n}` 段底边，线段树的叶子 = 一段底边（并开好节点数组）',
        'self.build(xs, 1, 0, n - 1)': '建树：根节点 `seg[1]` 管 `[0, {n - 1}]` 这几段底边',
        'if l == r': lambda S, B, r: ('叶子：只管一段底边，把 `min_cover_len` 设成这段的长度' if S.l == S.r else f'`[{S.l}, {S.r}]` 不是叶子，==分成左右两半建树=='),
        'self.seg[o].min_cover_len = xs[l + 1] - xs[l]': '叶子 `[{l}]` 的底边长 `{xs[l+1]} − {xs[l]}` = =={xs[l+1]-xs[l]}==，初始覆盖次数 0',
        62: '去左儿子：`update({B.o*2}, {B.l}, {B.r}, {B.v})`',
        64: '去右儿子：`update({B.o*2+1}, {B.l}, {B.r}, {B.v})`',
        'self.maintain(o)': '回溯时用左右儿子重算 `seg[{o}]`：==取较小的 min_cover，只累加等于它的那几段长度==',
        'self.seg[o].min_cover_len = (lo': lambda S, B, r: f'`seg[{S.o}]` = `[{S.self.seg[S.o].l}, {S.self.seg[S.o].r}]`：min_cover = =={S.self.seg[S.o].min_cover}==，min_cover_len = =={S.self.seg[S.o].min_cover_len}==',
        'events.sort': '事件按纵坐标 y 从小到大排序：`{[e[0] for e in events]}`，==扫描线==就按这个顺序往上走',
        'for (y, lx, rx, delta), e2 in pairwise(events)': lambda S, B, r: ('所有相邻事件都处理完了（最后一个事件后面没有高度，不用处理）' if B.get('y') == S.y and B.get('e2') == S.e2 else f'扫描线在 `y = {S.y}`，遇到' + ('==下边界==（+1）' if S.delta > 0 else '==上边界==（−1）') + f' `[{S.lx}, {S.rx}]`；下一个事件在 `y = {S.e2[0]}`'),
        'for lx, ly, rx, ry in rectangles': '每个矩形拆成两个事件：下边界 `(ly, lx, rx, +1)`、上边界 `(ry, lx, rx, -1)`；目前 `{len(events)}` 个事件',
        't.update(1, l, r, delta)': '离散化：`lx = {lx}` → `l = {l}`，`rx = {rx}` → `r = {r}`（叶子 `[{l}, {r}]`）。这几段覆盖次数 ==加 `{delta}`==（下边界 +1，上边界 −1）',
        'if l <= self.seg[o].l and': lambda S, B, r: (f'`seg[{S.o}]` 的区间 `[{S.self.seg[S.o].l}, {S.self.seg[S.o].r}]` ==完全落在== `[{S.l}, {S.r}]` 内 → 直接整体更新' if S.l <= S.self.seg[S.o].l and S.self.seg[S.o].r <= S.r else f'`seg[{S.o}]` 的区间 `[{S.self.seg[S.o].l}, {S.self.seg[S.o].r}]` 只有一部分在更新范围内 → 往下走'),
        'self.do(o, v)': '==Lazy==：只改这个节点 `min_cover += {v}` 并记 `todo`，不往子树里推',
        'self.spread(o)': '要进入子节点了，先把本节点的 `todo` 下传',
        'if v:': lambda S, B, r: ('有没下传的 `todo = ' + str(S.v) + '` → 子节点要补上') if S.v else '`todo = 0`，没有要下传的',
        'self.seg[o].todo = 0': '下传完毕，本节点 `todo` 清零',
        'if l <= m': lambda S, B, r: f'`l = {S.l} ≤ m = {S.m}`？' + ('更新范围伸到左半边 → 递归左儿子' if S.l <= S.m else '更新范围不在左半边，跳过'),
        'if m < r': lambda S, B, r: f'`m = {S.m} < r = {S.r}`？' + ('更新范围伸到右半边 → 递归右儿子' if S.m < S.r else '更新范围不在右半边，跳过'),
        'return 0 if self.seg[1].min_cover': lambda S, B, r: (f'根节点 `min_cover = {S.self.seg[1].min_cover} > 0`：整条底边都被覆盖 → 没覆盖的长度是 ==0==' if S.self.seg[1].min_cover else f'根节点 `min_cover = 0`：取到最小值（0）的底边长 `{S.self.seg[1].min_cover_len}` 就是==没被覆盖的长度=='),
        'sum_len = xs[-1]': lambda S, B, r: f'被覆盖的底边长 = 总长 `{S.xs[-1] - S.xs[0]}` − 没被覆盖的长度 `{S.t.get_uncovered_length()}` = =={S.xs[-1] - S.xs[0] - S.t.get_uncovered_length()}==',
        'ans += sum_len': '新增面积 = `sum_len × 高度` = `{sum_len} × ({e2[0]} − {y})` = =={sum_len * (e2[0] - y)}==，`ans = {ans}`',
        'return ans %': '答案 `{ans}` 对 `10^9+7` 取模：返回 `{ret}`',
    },
    cards=dict(
        one_liner='水平扫描线从下往上走，Lazy 线段树维护被覆盖的底边长',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给出若干轴对齐矩形，求它们覆盖的==总面积==（重叠只算一次），结果对 `10^9+7` 取模',
                 '示例：`[[0,0,2,2],[1,0,2,3],[1,0,3,1]]` → `6`',
                 '本视频用 `[[0,0,2,2],[1,1,2,3]]` → `5`（两矩形重叠一格）'],
        quote='想象有一根水平扫描线在从下往上扫描……面积的增加量等于 sumLen·(y′−y)，其中 sumLen 是被至少一个矩形覆盖的底边长之和。考虑用 Lazy 线段树维护。',
        quote_src='—— 灵茶山艾府题解',
        idea=['扫描线遇到下边界 `+1`、上边界 `−1`：记录每段横坐标被几个矩形覆盖',
              '线段树只存「最小覆盖次数 `min_cover`」和「取到最小值的底边长之和」',
              '`min_cover > 0` 说明整段都被覆盖；否则 `总长 − min_cover_len` 就是被覆盖的长度'],
        summary=['时间 `O(n log n)`，空间 `O(n)`；先离散化横坐标',
                 '`r = bisect_left(xs, rx) - 1`：叶子是 `xs[r]` 与 `xs[r+1]` 之间那一段',
                 '`todo` 可以是负数；要先 `spread` 再递归，递归完再 `maintain`',
                 '`for ... in pairwise(events)`：最后一个事件后面没有高度，不需要处理',
                 '题解的另一个角度：用「没被覆盖」的长度来算，更好维护最小值'],
    ),
)
