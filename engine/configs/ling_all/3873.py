OFF = 3 * 10 ** 9
PTS = [[2, 3], [2, 2], [1, 1], [4, 5]]
PAL = ['blue', 'pink', 'green', 'orange', 'purple', 'cyan']


def _nm(k):
    return f'行{k}' if k < OFF else f'列{k - OFF}'


def _root(fa, k):
    n = 0
    while fa.get(k, k) != k and n < 50:
        k = fa[k]
        n += 1
    return k


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    fa = S.get('fa', {})
    touched = set(fa) | set(fa.values())
    xs = sorted({p[0] for p in pts})
    ys = sorted({p[1] for p in pts})
    R, C = len(xs), len(ys)
    cell = min(130, (x1 - x0 - 220) / max(C - 1, 1), (y1 - y0 - 200) / max(R - 1, 1))
    gx = x0 + (x1 - x0 - cell * (C - 1)) / 2
    gy = y0 + 112
    cv.text((x0 + 18, y0 + 4), '点（同行 / 同列相连；同色 = 同一连通块，白圈 = 正在处理的点）', 22, T['muted'], bold=True)
    roots = sorted({_root(fa, p[0]) for p in pts if p[0] in touched})
    col = {r: T[PAL[i % len(PAL)]] for i, r in enumerate(roots)}
    pos = lambda p: (gx + ys.index(p[1]) * cell, gy + xs.index(p[0]) * cell)
    for i, r in enumerate(xs):
        cv.text((gx - 60, gy + i * cell), f'x={r}', 20, T['dim'], anchor='rm', bold=True)
    for i, c in enumerate(ys):
        cv.text((gx + i * cell, gy - 40), f'y={c}', 20, T['dim'], anchor='mb', bold=True)
    done = [p for p in pts if p[0] in touched]
    for i, a in enumerate(done):
        for b in done[i + 1:]:
            if a[0] == b[0] or a[1] == b[1]:
                cv.line([pos(a), pos(b)], col.get(_root(fa, a[0]), T['muted']), 5)
    cur = None
    if S.get('_line') == 13 and 'x' in S and S['x'] < OFF:
        cur = [S['x'], S['y']]
    elif S.get('_line') == 14 and 'x' in B:
        cur = [B['x'], B['y']]
    for p in pts:
        X, Y = pos(p)
        ok = p[0] in touched
        c = col.get(_root(fa, p[0])) if ok else T['panel2']
        cv.d.ellipse((X - 28, Y - 28, X + 28, Y + 28), fill=c, outline=T['border'])
        cv.text((X, Y), f'{p[0]},{p[1]}', 20, T['bg'] if ok else T['muted'], anchor='mm', bold=True)
        if cur is not None and list(p) == cur:
            cv.d.ellipse((X - 35, Y - 35, X + 35, Y + 35), outline=T['text'], width=4)


def _info(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    if 'mx1' in S:
        return f'最大两块：`mx1 = {S["mx1"]}`，`mx2 = {S["mx2"]}` → 再加新点的 1 → =={S["mx1"] + S["mx2"] + 1}=='
    if 'size' in S:
        return '各连通块大小 `size` = ' + '，'.join(f'=={v}==' for v in S['size'].values()) + '（按代表元计数）'
    done = [p for p in S['points'] if p[0] in set(fa) | set(fa.values())]
    return f'已连入 =={len(done)}== 个点，当前连通块 =={len({_root(fa, p[0]) for p in done})}== 个'


CONFIG = dict(
    num=3873, title='添加一个点后可激活的最大点数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='中介并查集 · 最大两个连通块',
    tags=['七、并查集', '§7.3 中介并查集'],
    code='''
class Solution:
    def maxActivated(self, points: List[List[int]]) -> int:
        # 哈希表并查集
        fa = {}

        def find(x: int) -> int:
            if x not in fa:
                return x
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        OFFSET = 3 * 10 ** 9
        for x, y in points:
            fa[find(x)] = find(y + OFFSET)

        # 统计连通块的大小
        size = Counter(find(p[0]) for p in points)

        mx1 = mx2 = 0
        for sz in size.values():
            if sz > mx1:
                mx2 = mx1
                mx1 = sz
            elif sz > mx2:
                mx2 = sz

        return mx1 + mx2 + 1
''',
    call=f'Solution().maxActivated({PTS})',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='map', var='fa', label='fa：行 / 列中介 → 父亲（行 x 与 列 y + OFFSET 分开编号）',
             fmt=lambda k, v: f'{_nm(k)} → {_nm(v)}', h=130, font=26),
        dict(type='text', fn=_info, size=30, h=70),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('sz', 'sz', 'cyan'), ('mx1', 'mx1', 'green'), ('mx2', 'mx2', 'orange')],
    skip=['fa = {}', 'if fa[x] != x', 'if x not in fa', 'return x', 'return fa[x]', 10],
    captions={
        'OFFSET = 3': '行号 `x` 与列号 `y` 可能相等 → ==列号加 `OFFSET`== 错开，坐标最大 10^9，取 3×10^9 足够',
        'for x, y in points': lambda S, B, r: (f'取点 `({S.x}, {S.y})`：它连起「行 {S.x}」和「列 {S.y}」'
                                               if 'x' not in B or (B.x, B.y) != (S.x, S.y) else '所有点都连完了'),
        'fa[find(x)] = find(y + OFFSET)': lambda S, B, r: (
            f'行 {B.x} 与列 {B.y} 已在同一块，无需合并'
            if _root(B.fa, B.x) == _root(B.fa, B.y + OFF)
            else '代表元不同 → `fa[find(x)] = find(y + OFFSET)`，==两个连通块并成一个==（find 会顺便做路径压缩）'),
                'size = Counter': '按代表元统计：每个点所在块的代表元计数 → ==每个连通块有多少个点==',
        'mx1 = mx2 = 0': '准备找最大和次大的连通块：`mx1`、`mx2` 初始为 0',
        'for sz in size.values()': '取下一个连通块的大小（取完了就结束遍历）',
        'if sz > mx1': lambda S, B, r: (f'块大小 `{S.sz}` > 当前最大 `{S.mx1}`？成立 → 它成为新的最大' if S.sz > S.mx1 else f'块大小 `{S.sz}` 没超过最大 `{S.mx1}`，再看能不能当次大'),
        'mx2 = mx1': '原来的最大退居次大：`mx2 = {mx2}`',
        'mx1 = sz': '最大更新为 `{mx1}`',
        'elif sz > mx2': lambda S, B, r: (f'`{S.sz}` > 次大 `{S.mx2}`，成立 → 更新次大' if S.sz > S.mx2 else f'`{S.sz}` 不超过次大 `{S.mx2}`，忽略'),
        'mx2 = sz': '次大更新为 `{mx2}`',
        'return mx1 + mx2 + 1': '新点放在最大两块之间把它们连起来：`{mx1} + {mx2} + 1` = =={mx1 + mx2 + 1}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='新点连起最大的两个连通块：答案 = 最大 + 次大 + 1',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['点被激活后，==同 x 或同 y 的点也会被激活==，一直传下去',
                 '可以额外加一个不在 `points` 里的整数点，从它开始激活',
                 '求最多激活多少个点（含新点）',
                 '示例：`[[2,3],[2,2],[1,1],[4,5]]` → `4`'],
        quote='激活点 (x,y)，也同时激活了 x 这一行，y 这一列。……找到图中最大的两个连通块。这两个连通块可以通过额外添加一个坐标点相连。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同行同列的点属于同一个连通块；新点只能把==两个==连通块接起来',
              '行和列当中介：点 `(x, y)` 连 行 `x` 与 列 `y + OFFSET`，只要 `n` 条边',
              '数据范围到 10^9，用==哈希表并查集==；`Counter` 统计各块大小，扫一遍取最大、次大'],
        summary=['答案 = 最大块 + 次大块 + 1；只有一个块时 `mx2 = 0`，结果就是 `mx1 + 1`',
                 '易错：列号要加 `OFFSET`，否则行 2 与列 2 会混成一个点',
                 '并查集只写路径压缩，均摊 `O(log n)`；建图 + DFS 可做到 `O(n)`',
                 '同类题：947 题（那题数的是连通块个数）'],
    ),
)
