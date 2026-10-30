EDGES = [[0, 1, 2], [1, 2, 5], [3, 4, 3], [2, 3, 7], [4, 5, 4]]
COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange', 'red']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _fa(S):
    u = S.get('u')
    return list(u._fa) if u is not None else None


def _color(S, i, v):
    fa = _fa(S)
    if fa is None:
        return None
    r = _root(fa, i)
    return COLS[r % len(COLS)] if fa.count(r) > 1 or any(_root(fa, j) == r and j != i for j in range(len(fa))) else None


def _info(S):
    u = S.get('u')
    if u is None:
        return '边按 `time` 从大到小排序，再逐条加入并查集'
    fa = list(u._fa)
    roots = sorted({_root(fa, i) for i in range(len(fa))})
    groups = ' '.join('{' + ','.join(str(i) for i in range(len(fa)) if _root(fa, i) == r) + '}' for r in roots)
    return f'连通块 `cc = {u.cc}`，目标 `k = {S["k"]}`：{groups}'


def _edge(S):
    es = S.get('edges')
    if es is None:
        return ''
    t = S.get('t')
    if t is None:
        return '边（x, y, time）：' + '  '.join(f'({a},{b},{c})' for a, b, c in es)
    return '边（降序）：' + '  '.join((f'=={a},{b},{c}==' if (a, b, c) == (S['x'], S['y'], t) else f'({a},{b},{c})') for a, b, c in es)


CONFIG = dict(
    num=3608, title='包含 K 个连通分量需要的最小时间', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='离线倒序加边 + 并查集',
    tags=['七、并查集', '难度分 1893'],
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
        self.cc -= 1  # 成功合并，连通块个数减一

class Solution:
    def minTime(self, n: int, edges: List[List[int]], k: int) -> int:
        edges.sort(key=lambda e: -e[2])  # 按照 time 降序排列
    
        u = UnionFind(n)
        for x, y, t in edges:
            u.merge(x, y)
            if u.cc < k:  # 这条边不能留，即移除所有 time <= t 的边
                return t
        return 0  # 无需移除任何边
''',
    call=f'Solution().minTime(6, {EDGES}, 3)',
    expect=3,
    views=[
        dict(type='text', fn=_edge, size=24, h=60),
        dict(type='array', var=lambda S: _fa(S), label='fa（同色 = 同一个连通块）', color=_color, h=200,
             pointers={'x': 'blue', 'y': 'pink'}),
        dict(type='text', fn=_info, size=26, h=70),
    ],
    watch=[('cc', "u.cc if 'u' in locals() else None", 'green'), ('k', 'k', 'orange'), ('t', 't', 'yellow')],
    skip=['self._fa = list', 'self.cc = n'],
    captions={
        'edges.sort': '`time` 降序排列：==时间越大的边越晚被删==，倒着看就是先加',
        'u = UnionFind': '一开始每个点自成一块，`cc = {n}`（相当于所有边都已删完）',
        'u.merge(x, y)': '倒序把边 `({x}, {y}, time={t})` 加回来：合并两个端点所在集合',
        'self._fa[x] = y': '`{B.x}` 和 `{B.y}` 不在同一集合 → 把 `{B.x}` 的代表元挂到 `{B.y}` 下',
        'self.cc -= 1': '成功合并，连通块个数减一：`cc` = =={self.cc}==',
        'x, y = self.find': '分别找 `{from_}` 和 `{to}` 所在集合的代表元（路径压缩）',
        'if x == y': lambda S, B, r: f'代表元 `{S.x}` 与 `{S.y}`：' + ('同一集合 → ==直接返回==，`cc` 不变' if S.x == S.y else '不同集合 → 需要合并'),
        'if u.cc < k': lambda S, B, r: (f'`cc = {S.u.cc} < k = {S.k}`：块数从 ≥ k 掉到 < k → ==这条边不能留==' if S.u.cc < S.k
                                         else f'`cc = {S.u.cc} ≥ k = {S.k}`：块数还够，继续加更早删的边'),
        'return t': '必须移除所有 `time <= {t}` 的边，剩下的边才能凑出 ≥ k 块 → 答案 =={t}==',
        'return 0': '全部边都加回来了块数仍 ≥ k：无需删边，返回 0',
    },
    cards=dict(
        one_liner='并查集只会合并不会拆分：把删边倒过来，变成从大到小加边',
        complexity='时间 `O(n + m log m + m log n)`，空间 `O(n)`',
        problem=['无向图有 `n` 个点，边 `[u, v, time]` 会在 `time` 时刻被删除',
                 '求最小的 `t`：删掉所有 `time <= t` 的边后，连通块个数 `>= k`',
                 '本视频：`n=6`，5 条边，`k=3` → `3`'],
        quote='由于并查集加边容易，删边难，按照 time 从大到小的顺序加边，用并查集合并边的两个端点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`t` 越大，删的边越多，连通块越多：答案满足==单调性==，只需枚举边的 `time`',
              '倒着加边：连通块个数从 `n` 慢慢减少',
              '某条边（时间 `t`）加入后块数从 `>= k` 变成 `< k`：这条边不能留，答案就是 `t`'],
        summary=['时间 `O(n + m log m + m log n)`，空间 `O(n)`',
                 '块数是在==合并成功==时才减一，`merge` 里同集合直接 `return`',
                 '全部加完仍 `cc >= k`（如示例 3）返回 `0`',
                 '代码先 `edges.sort`，会改动入参；并查集带路径压缩'],
    ),
)
