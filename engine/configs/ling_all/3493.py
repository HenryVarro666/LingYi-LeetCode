import math

PAL = ['cyan', 'pink', 'green', 'purple', 'orange', 'yellow']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    sets = S.get('sets')
    uf = S.get('uf')
    if sets is None or uf is None:
        return
    n, k, fa = len(sets), S['k'], uf._fa
    line = S['_line']
    i, j = S.get('i'), S.get('j')
    if i is None:
        pairs, cur = [], None
    elif line == 28:
        pairs, cur = [(a, b) for a in range(i) for b in range(a)], None
    else:
        pairs = [(a, b) for a in range(i) for b in range(a)] + [(i, b) for b in range(j)]
        cur = (i, j)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 5
    Rx, Ry = (x1 - x0 - 300) / 2, (y1 - y0 - 230) / 2
    pos = [(cx + Rx * math.sin(2 * math.pi * t / n), cy - Ry * math.cos(2 * math.pi * t / n)) for t in range(n)]
    cv.text((x0 + 18, y0 + 4), '图：节点 = 下标，颜色 = 并查集中的连通块，线 = 交集 >= k 的边', 22, T['muted'], bold=True)
    for a, b in pairs:
        if len(sets[a] & sets[b]) >= k:
            cv.line([pos[a], pos[b]], T['green'], 4)
    if cur is not None:
        a, b = cur
        ok = len(sets[a] & sets[b]) >= k
        cv.line([pos[a], pos[b]], T['yellow'] if ok else T['pink'], 6 if ok else 3)
    for t in range(n):
        px, py = pos[t]
        r = _root(fa, t)
        col = T[PAL[r % len(PAL)]]
        ring = T['yellow'] if cur and t in cur else None
        cv.rect((px - 36, py - 36, px + 36, py + 36), fill=col, outline=ring, width=5, r=36)
        cv.text((px, py), t, 34, T['bg'], anchor='mm', bold=True)
        dx, dy = px - cx, py - cy
        d = math.hypot(dx, dy) or 1
        ox, oy = px + dx / d * 80, py + dy / d * 58
        cv.text((ox, oy), '{' + ','.join(map(str, sorted(sets[t]))) + '}', 26, T['text'], anchor='mm', mono=True)
    if cur is not None:
        a, b = cur
        inter = sorted(sets[a] & sets[b])
        cv.text((x0 + 18, y0 + 40), f'sets[{a}] & sets[{b}]', 22, T['muted'])
        cv.text((x0 + 18, y0 + 70), '{' + ','.join(map(str, inter)) + f'}} : {len(inter)} vs k={k}', 28,
                T['yellow'] if len(inter) >= k else T['pink'], bold=True, mono=True)


CONFIG = dict(
    num=3493, title='属性图', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='暴力枚举 + 并查集',
    tags=['灵神题单', '难度分 1565'],
    code='''
class UnionFind:
    def __init__(self, n: int):
        # 一开始有 n 个集合 {0}, {1}, ..., {n-1}
        # 集合 i 的代表元是自己
        self._fa = list(range(n))  # 代表元
        self.cc = n  # 连通块个数

    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        # 如果 fa[x] == x，则表示 x 是代表元
        if self._fa[x] != x:
            self._fa[x] = self.find(self._fa[x])  # fa 改成代表元
        return self._fa[x]

    # 把 from 所在集合合并到 to 所在集合中
    def merge(self, from_: int, to: int) -> None:
        x, y = self.find(from_), self.find(to)
        if x == y:  # from 和 to 在同一个集合，不做合并
            return
        self._fa[x] = y  # 合并集合。修改后就可以认为 from 和 to 在同一个集合了
        self.cc -= 1  # 合并后，连通块个数减少了 1

class Solution:
    def numberOfComponents(self, properties: List[List[int]], k: int) -> int:
        sets = list(map(set, properties))
        uf = UnionFind(len(properties))
        for i, a in enumerate(sets):
            for j, b in enumerate(sets[:i]):
                if len(a & b) >= k:
                    uf.merge(j, i)
        return uf.cc
''',
    call='Solution().numberOfComponents([[1,2],[1,1],[3,4],[4,5],[7,7]], 1)',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='array', var=lambda S: S['uf']._fa if 'uf' in S else [], label='uf._fa（代表元数组）',
             pointers={'i': 'blue', 'j': 'pink'}, cell=90, h=170),
    ],
    max_steps=110,
    watch=['i', 'j', 'k', ('cc', 'uf.cc', 'green')],
    captions={
        5: '每个点先自成一个集合：`_fa = {self._fa}`',
        6: '连通块个数一开始是 `n = {self.cc}`',
        12: lambda S, B, r: ('`_fa[x] != x`：x 不是代表元 → 顺着 fa 往上找' if S.self._fa[S.x] != S.x else f'`_fa[{S.x}] == {S.x}`：x 就是代表元，直接返回'),
        13: '路径压缩：`_fa[x]` 直接改成代表元',
        18: '先分别找 from 和 to 的代表元：`x = {x}`，`y = {y}`',
        19: lambda S, B, r: ('代表元相同：本来就连通，不能让 cc 多减一次' if S.x == S.y else f'代表元不同（`{S.x}` != `{S.y}`）：两个连通块要合并'),
        21: '把 x 的集合挂到 y 下：`_fa[{x}] = {y}`',
        22: '合并成功，连通块少一个：`cc = {self.cc}`',
        26: '把每个属性数组变成集合，求交集更方便：`sets = {sets}`',
        27: '`uf` 初始有 `n = {uf.cc}` 个连通块',
        28: lambda S, B, r: f'枚举 `i = {S.i}`，和前面的 `j < {S.i}` 逐个配对',
        29: lambda S, B, r: (f'`i = {S.i}` 的所有 j 都配完了' if S.j == S.i - 1 and B.get('j') == S.j else f'配对 `sets[{S.j}]` 与 `sets[{S.i}]`'),
        30: lambda S, B, r: (f'交集 `{sorted(S.a & S.b)}` 大小 `{len(S.a & S.b)}` '
                              + ('>=' if len(S.a & S.b) >= S.k else '<') + f' `k = {S.k}` → '
                              + ('==有边==，合并 j 和 i' if len(S.a & S.b) >= S.k else '没边，跳过')),
        31: '合并 `{j}` 和 `{i}` 所在集合',
        32: '没有更多配对了：连通块个数 `uf.cc = {uf.cc}`',
    },
    cards=dict(
        one_liner='两两求交集，够大就并查集合并，数连通块',
        complexity='时间 `O(n^2 m)`，空间 `O(nm)`',
        problem=['`properties[i]` 是第 i 个节点的属性；两节点交集的不同整数个数 `>= k` 就连边',
                 '求图的连通分量个数',
                 '本视频：`[[1,2],[1,1],[3,4],[4,5],[7,7]]`，`k = 1` → `3`'],
        quote='暴力枚举所有 properties[i] 和 properties[j]，如果交集大小 >= k，那么用并查集合并 i 和 j。初始连通块个数 cc=n，每成功合并一次，就把 cc 减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把每行转成集合，`a & b` 一步得到交集',
              '`n <= 100`，枚举所有 `j < i` 的点对就够了',
              '并查集的 `cc` 跟着合并次数递减，最后直接返回 `cc`，不用再数代表元'],
        summary=['时间 `O(n^2 m)`，空间 `O(nm)`',
                 '`merge` 里两点代表元相同时直接返回，不能让 `cc` 多减',
                 '提示：集合去重，所以 `[1,1]` 的交集大小最多是 1',
                 '另一种写法：用位运算把集合压成整数，`(a & b).bit_count()` 求交集大小，时间 `O(n^2 m/w)`'],
    ),
)
