OFF = 10001
STONES = [[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]
PAL = ['blue', 'pink', 'green', 'orange', 'purple', 'cyan']


def _nm(k):
    return f'行{k}' if k < OFF else f'列{k - OFF}'


def _root(fa, k):
    n = 0
    while fa.get(k, k) != k and n < 50:
        k = fa[k]
        n += 1
    return k


def _info(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    touched = set(fa) | set(fa.values())
    done = [p for p in S['stones'] if p[0] in touched]
    roots = {_root(fa, p[0]) for p in done}
    s = f'已连入 ==`{len(done)}`== 块石头，当前连通块 ==`{len(roots)}`== 个'
    if 'st' in S:
        s = f'连通块（不同代表元）共 ==`{len(S["st"])}`== 个 → 能移除 `{len(S["stones"])} − {len(S["st"])}` = =={len(S["stones"]) - len(S["st"])}=='
    return s


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    stones = S['stones']
    fa = S.get('fa', {})
    touched = set(fa) | set(fa.values())
    R = max(p[0] for p in stones) + 1
    C = max(p[1] for p in stones) + 1
    cell = min(130, (x1 - x0 - 200) / max(C, 1), (y1 - y0 - 150) / max(R, 1))
    gx = x0 + (x1 - x0 - cell * (C - 1)) / 2
    gy = y0 + 112
    cv.text((x0 + 18, y0 + 4), '石头（同行 / 同列相连；同色 = 同一连通块，白圈 = 正在处理的石头）', 22, T['muted'], bold=True)
    roots = sorted({_root(fa, p[0]) for p in stones if p[0] in touched})
    col = {}
    for i, r in enumerate(roots):
        col[r] = T[PAL[i % len(PAL)]]
    pos = lambda p: (gx + p[1] * cell, gy + p[0] * cell)
    for r in range(R):
        cv.text((gx - 60, gy + r * cell), f'行{r}', 20, T['dim'], anchor='rm', bold=True)
    for c in range(C):
        cv.text((gx + c * cell, gy - 40), f'列{c}', 20, T['dim'], anchor='mb', bold=True)
    done = [p for p in stones if p[0] in touched]
    for i, a in enumerate(done):
        for b in done[i + 1:]:
            if a[0] == b[0] or a[1] == b[1]:
                cv.line([pos(a), pos(b)], col.get(_root(fa, a[0]), T['muted']), 5)
    cur = [S.get('x'), S.get('y')] if isinstance(S.get('y'), int) and S.get('x') is not None and S.get('x') < OFF else None
    for p in stones:
        X, Y = pos(p)
        ok = p[0] in touched
        c = col.get(_root(fa, p[0])) if ok else T['panel2']
        cv.d.ellipse((X - 26, Y - 26, X + 26, Y + 26), fill=c, outline=T['border'])
        cv.text((X, Y), f'{p[0]},{p[1]}', 20, T['bg'] if ok else T['muted'], anchor='mm', bold=True)
        if cur is not None and list(p) == cur:
            cv.d.ellipse((X - 33, Y - 33, X + 33, Y + 33), outline=T['text'], width=4)


CONFIG = dict(
    num=947, title='移除最多的同行或同列石头', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='中介并查集 · 行列当节点',
    tags=['七、并查集', '§7.3 中介并查集', '难度分 2035'],
    code='''
class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        # 哈希表并查集
        fa = {}

        def find(x: int) -> int:
            if x not in fa:
                return x
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        OFFSET = 10001
        for x, y in stones:
            fa[find(x)] = find(y + OFFSET)

        # 记录不同的代表元
        st = {find(p[0]) for p in stones}

        return len(stones) - len(st)
''',
    call=f'Solution().removeStones({STONES})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='map', var='fa', label='fa：行 / 列中介 → 父亲（行 x 与 列 y + OFFSET 分开编号）',
             fmt=lambda k, v: f'{_nm(k)} → {_nm(v)}', h=130, font=28),
        dict(type='text', fn=_info, size=30, h=70),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('OFFSET', 'OFFSET'), ('连通块', 'len(st)', 'green')],
    skip=['fa = {}', 'if fa[x] != x', 'def find', 'if x not in fa', 'return x', 'return fa[x]'],
    captions={
        'OFFSET = 10001': '行号 `x` 和列号 `y` 都从 0 起，会撞号 → ==列号加 `OFFSET`== 错开，这样行、列能放进同一个并查集',
        'for x, y in stones': lambda S, B, r: (f'取一块石头 `({S.x}, {S.y})`：它把「行 {S.x}」和「列 {S.y}」连起来'
                                               if 'x' not in B or (B.x, B.y) != (S.x, S.y) else '所有石头都连完了'),
        'fa[find(x)] = find(y + OFFSET)': lambda S, B, r: (
            f'行 {B.x} 与列 {B.y} 已在同一个连通块（代表元相同），这块石头不改变连通性'
            if _root(B.fa, B.x) == _root(B.fa, B.y + OFF)
            else f'行 {B.x} 与列 {B.y} 的代表元不同 → `fa[find(x)] = find(y + OFFSET)`，==两个连通块并成一个=='),
        'fa[x] = find(fa[x])': '路径压缩：`x` 不是代表元 → 递归找到代表元，让 `fa[x]` 直接指向它，下次一步到位',
        'st = {find(p[0])': '每块石头找一次代表元放进集合 `st`：不同代表元的个数 = ==连通块个数==',
        'return len(stones) - len(st)': '每个连通块必留 1 块 → 可移除 `{len(stones)} − {len(st)}` = =={len(stones) - len(st)}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='每个连通块留 1 块，其余都能移除：答案 = n − 连通块数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['石头放在整数坐标上，==同行或同列有别的石头== 就能把它移走',
                 '求最多能移走几块石头',
                 '示例：`[[0,0],[0,2],[1,1],[2,0],[2,2]]` → `3`'],
        quote='大小为 k 的连通块，可以移除其中 k-1 块石头。移除后，剩下的 1 块石头由于没有同行或同列的其他石头，所以不能移除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同行同列的石头相连，得到一张图；每个连通块留 1 块',
              '两两连边是 `O(n²)`，改成==行和列当中介==：石头 `(x, y)` 只连 行 `x` 与 列 `y`',
              '用哈希表并查集，所以坐标再大也不怕；不同代表元个数 = 连通块数'],
        summary=['移除数 = `n` − 连通块数',
                 '易错：行号和列号要用 `OFFSET` 错开，否则行 1 与列 1 会被当成同一个点',
                 '并查集只写路径压缩，均摊 `O(log n)`；建图 + DFS 可做到 `O(n)`',
                 '同类题：3873 题（找最大的两个连通块）'],
    ),
)
