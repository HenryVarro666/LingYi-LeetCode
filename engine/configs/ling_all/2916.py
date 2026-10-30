def _leafvals(S):
    """true f[k] (distinct count of a[k..i]) for k=1..n, reading the lazy tree"""
    sm, td, n = S.get('sum'), S.get('todo'), len(S['nums'])
    if sm is None:
        return None
    out = []
    for k in range(1, n + 1):
        o, l, r, acc = 1, 1, n, 0
        while l < r:
            acc += td[o]
            m = (l + r) // 2
            if k <= m:
                o, r = o * 2, m
            else:
                o, l = o * 2 + 1, m + 1
        out.append(sm[o] + acc)
    return out


def _nodes(n):
    out = []

    def go(o, l, r, d):
        out.append((o, l, r, d))
        if l < r:
            m = (l + r) // 2
            go(o * 2, l, m, d + 1)
            go(o * 2 + 1, m + 1, r, d + 1)
    go(1, 1, n, 0)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '线段树：每个节点 = 一段左端点的「不同计数」之和（上）和待下发的加法标记 todo（下）', 22, T['muted'], bold=True)
    sm, td = S.get('sum'), S.get('todo')
    if sm is None:
        return
    n = len(S['nums'])
    nodes = _nodes(n)
    maxd = max(d for *_, d in nodes)
    inn = S.get('_inner', {})
    cur = inn.get('o') if 'o' in inn else None
    rng = (inn['L'], inn['R']) if 'L' in inn else None
    W = x1 - x0 - 40
    cw = min(170, W / n)
    sx = x0 + 20 + (W - cw * n) / 2
    top, bottom = y0 + 80, y1 - 100
    dy = (bottom - top) / max(1, maxd)
    pos = {}
    for o, l, r, d in sorted(nodes, key=lambda t: -t[3]):
        cx = sx + (l - 1 + 0.5) * cw if l == r else (pos[o * 2][0] + pos[o * 2 + 1][0]) / 2
        pos[o] = (cx, top + d * dy)
    bw, bh = min(150, cw - 10), 66
    for o, l, r, d in nodes:
        if l < r:
            for ch in (o * 2, o * 2 + 1):
                cv.line([(pos[o][0], pos[o][1] + bh / 2), (pos[ch][0], pos[ch][1] - bh / 2)], T['border'], 2)
    for o, l, r, d in nodes:
        cx, cy = pos[o]
        inside = rng is not None and rng[0] <= l and r <= rng[1]
        fill = (30, 70, 45) if inside else T['panel2']
        cv.rect((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), fill=fill,
                outline=T['yellow'] if o == cur else T['border'], width=4 if o == cur else 2, r=8)
        cv.text((cx, cy - 21), f'[{l},{r}]', 18, T['muted'], anchor='mm', mono=True)
        cv.text((cx, cy + 1), f'sum={sm[o]}', 24, T['green'], anchor='mm', bold=True)
        tdv = td[o]
        cv.text((cx, cy + 22), f'todo={tdv}', 18, T['orange'] if tdv else T['dim'], anchor='mm', mono=True)
    if rng is not None:
        a, b = sx + (rng[0] - 1) * cw + 6, sx + rng[1] * cw - 6
        cv.line([(a, y1 - 40), (b, y1 - 40)], T['green'], 4)
        cv.text(((a + b) / 2, y1 - 32), f'操作区间 [{rng[0]}, {rng[1]}]', 20, T['green'], anchor='mt', bold=True)


def _formula(S):
    i = S.get('i')
    if i is None or 'last' not in S:
        return '`f[k]` = 以 i 为右端点、k 为左端点的子数组的不同计数；`s` = 它们的平方和'
    x = S['x']
    j = S['j'] if 'j' in S else S['last'].get(x, 0)
    return f'右端点 `i = {i}`，`a[i] = {x}` 上次出现在 `j = {j}`：左端点 `[{j + 1}, {i}]` 的不同计数都 +1'


CONFIG = dict(
    num=2916, title='子数组不同元素数目的平方和 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='Lazy 线段树：区间加一 + 区间求和',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def sumCounts(self, nums: List[int]) -> int:
        n = len(nums)
        sum = [0] * (n * 4)
        todo = [0] * (n * 4)

        def do(o: int, l: int, r: int, add: int) -> None:
            sum[o] += add * (r - l + 1)
            todo[o] += add

        # o=1  [l,r] 1<=l<=r<=n
        # 把 [L,R] 加一，同时返回加一之前的区间和
        def query_and_add1(o: int, l: int, r: int, L: int, R: int) -> int:
            if L <= l and r <= R:
                res = sum[o]
                do(o, l, r, 1)
                return res

            m = (l + r) // 2
            add = todo[o]
            if add:
                do(o * 2, l, m, add)
                do(o * 2 + 1, m + 1, r, add)
                todo[o] = 0

            res = 0
            if L <= m: res += query_and_add1(o * 2, l, m, L, R)
            if m < R:  res += query_and_add1(o * 2 + 1, m + 1, r, L, R)
            sum[o] = sum[o * 2] + sum[o * 2 + 1]
            return res

        ans = s = 0
        last = {}
        for i, x in enumerate(nums, 1):
            j = last.get(x, 0)
            s += query_and_add1(1, 1, n, j + 1, i) * 2 + i - j
            ans += s
            last[x] = i
        return ans % 1_000_000_007
''',
    call='Solution().sumCounts([1,2,1])',
    expect=15,
    views=[
        dict(type='text', fn=_formula, size=24, h=56),
        dict(type='array', var='nums', label='nums（蓝 = 当前 i）', h=165, cell=80,
             color=lambda S, k, v: 'blue' if S.get('i') == k + 1 else None),
        dict(type='array', var=_leafvals, label='f[k]：左端点为 k 的子数组 a[k..i] 的不同计数（框 = 本轮 +1 的区间）', h=180, cell=80,
             window=('j', 'i - 1'), index=True),
        dict(type='custom', draw=_draw, h=470),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s', 's', 'yellow'), ('ans', 'ans', 'green')],
    skip=['n = len(nums)', 'sum = [0]', 'todo = [0]', 'ans = s = 0', 'last = {}', 'res = 0', 'add = todo[o]', 'm = (l + r)',
          'return res', 'todo[o] += add', 'last[x] = i', 'todo[o] = 0', 'res = sum[o]'],
    captions={
        'j = last.get': '`{x}` 上次出现在 `j = {j}`（没出现过记 0）：只有左端点在 `[{j + 1}, {i}]` 的子数组会多出一个新数',
        's += query_and_add1(1, 1, n': '对左端点区间 `[{j + 1}, {i}]`：==先求和再整体 +1==，`s` 增加 `2×区间和 + 区间长度 {i - j}`',
        'ans += s': '`s = {s}`：此刻所有以 `{i}` 为右端点的子数组的 ==不同计数平方和==，累加进 `ans = {ans}`',
        'if L <= l and r <= R': lambda S, B, r: (f'`[{S.l}, {S.r}]` 完全落在 `[{S.L}, {S.R}]` 内 → ==整块一次处理==，不用往下' if S.L <= S.l and S.r <= S.R else f'`[{S.l}, {S.r}]` 只有一部分在 `[{S.L}, {S.R}]` 内 → 往下拆'),
        'do(o, l, r, 1)': '先把这块 ==加一之前== 的和 `sum[{o}] = {sum[o]}` 记作返回值；再整块 +1：`sum` 加 `长度 {r - l + 1}`，孩子的更新记在 `todo` 里先欠着',
        'sum[o] += add': '`sum[{o}] += {add} × {r - l + 1}` → =={sum[o]}==；`todo[{o}] += {add}`：孩子先欠着，不碰',
        'if add:': lambda S, B, r: (f'`todo[{S.o}] = {S.add}` 不为 0：这块欠着孩子的更新 → 先下发（pushdown）再往下' if S.add else f'`todo[{S.o}] = 0`：没有欠账，直接往下'),
        'do(o * 2, l, m, add)': '把 `+{add}` 下发给左孩子 `[{l}, {m}]`',
        'do(o * 2 + 1, m + 1, r, add)': '把 `+{add}` 下发给右孩子 `[{m + 1}, {r}]`；然后 `todo[{o}]` 清零',
        'if L <= m': lambda S, B, r: (f'`L = {S.L} <= 中点 {S.m}`：左半边有交集 → 递归进 `[{S.l}, {S.m}]`' if S.L <= S.m else f'`L = {S.L} > 中点 {S.m}`：左半边没有交集，跳过'),
        'if m < R': lambda S, B, r: (f'`中点 {S.m} < R = {S.R}`：右半边有交集 → 递归进 `[{S.m + 1}, {S.r}]`' if S.m < S.R else f'`中点 {S.m} >= R = {S.R}`：右半边没有交集，跳过'),
        'sum[o] = sum[o * 2]': '回溯：`sum[{o}]` = 左孩子 + 右孩子 = =={sum[o]}==（孩子此时已是最新）',
        'return ans': '`ans = {ans}`，对 `10^9+7` 取模后返回 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='右端点 i 往右走，每步只给一段左端点的不同计数 +1',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['子数组的「不同计数」= 里面不同数的个数；求==所有子数组不同计数的平方和==，对 `10^9+7` 取模','`n` 到 `10^5`，不能枚举子数组','示例：`[1,2,1]` → `15`'],
        quote='添加后，右端点为 i-1 的这些子数组的「不同计数的平方」之和增加了多少？……不同计数增加了 1，平方的增加量为 (x+1)² − x² = 2x+1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按右端点分组：`a[i]` 上次出现在 `j`，则只有左端点在 `[j+1, i]` 的子数组多了一个新数，不同计数 +1','平方的增量是 `2x+1`，所以 `s += 2×(区间和) + 区间长度`','需要「区间加一 + 区间求和」，用 lazy 线段树，查询和更新合成一次遍历'],
        summary=['时间 `O(n log n)`，空间 `O(n)`','`s` 是以当前 i 为右端点的平方和，`ans` 每轮累加一次 `s`','下标从 1 开始，`j = 0` 表示没出现过','`sum` 和 `todo` 开 `4n`；Python 里 `sum` 遮住了内置函数，但这里不影响','先做简单版 2262「字符串的总引力」更容易理解']
    ),
)
