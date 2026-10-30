CONFIG = dict(
    num=323, title='无向图中连通分量的数目', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='并查集 · 合并一次减一',
    tags=['图论算法'],
    code='''
class Solution(object):
    def countComponents(self, n, edges):

        res = n
        fa = list(range(n))

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for x, y in edges:
            fa_x = find(x)
            fa_y = find(y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                res -= 1
        
        return res
''',
    call='Solution().countComponents(6, [[0,1],[1,2],[3,4],[0,2]])',
    expect=3,
    views=[
        dict(type='array', var='fa', label='fa（并查集：fa[i] 是 i 的父亲，绿色 = 已并入别人）', pointers={'fa_x': 'blue', 'fa_y': 'pink'}, h=200,
             color=lambda S, i, v: 'green' if v != i else None),
        dict(type='array', var='edges', label='edges', h=190, cell=110),
        dict(type='calls', h=140),
    ],
    watch=[('res', 'res', 'green'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('fa_x', 'fa_x', 'blue'), ('fa_y', 'fa_y', 'pink')],
    captions={
        'res = n': '一开始 `n = {n}` 个点各自是一个连通分量：`res = {res}`',
        'fa = list(range(n))': '并查集：每个点的父亲是自己 `fa[i] = i`',
        'for x, y in edges': '枚举边 `{x} — {y}`',
        'fa_x = find(x)': '调用 `find({x})`：沿父亲往上找 `{x}` 所在集合的代表元',
        'fa_y = find(y)': '调用 `find({y})`：找 `{y}` 所在集合的代表元',
        'if fa_x != fa_y': lambda S, B, r: (f'`fa_x = {S.fa_x}` ≠ `fa_y = {S.fa_y}`：属于==不同分量== → 要合并' if S.fa_x != S.fa_y else f'`fa_x = {S.fa_x}` == `fa_y = {S.fa_y}`：本来就连通，这条边什么都不改变'),
        'fa[fa_x] = fa_y': '合并两个分量：`fa[{fa_x}] = {fa_y}`',
        'res -= 1': '两个分量变成一个：`res` {B.res} → =={res}==',
        'if fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] = {S.fa[S.x]}` ≠ `{S.x}`：不是代表元，继续往上找' if S.fa[S.x] != S.x else f'`fa[{S.x}] == {S.x}`：`{S.x}` 就是代表元'),
        'fa[x] = find(fa[x])': '路径压缩：`fa[{x}]` 直接指向代表元 `{fa[x]}`',
        'return res': '所有边处理完，剩下 `{res}` 个连通分量',
    },
    skip=['def find', 'return fa[x]'],
    cards=dict(
        one_liner='n 个分量起步，每成功合并一次就少一个',
        complexity='时间 `O((n+m) α(n))`，空间 `O(n)`',
        problem=['`n` 个点（编号 `0..n-1`）和无向边 `edges`，求图中连通分量的个数',
                 '本视频示例：`n=6, edges=[[0,1],[1,2],[3,4],[0,2]]`',
                 '分量为 `{0,1,2}`、`{3,4}`、`{5}` → `3`'],
        quote='一开始图中n个节点将形成n个连通分量，接下来枚举所有的边。对于当前的边(x, y)，若x和y属于不同的连通分量，那么就需要将这两个连通分量合并，此时连通分量的总数应该减去一。',
        quote_src='—— yiduobo 题解原文',
        idea=['先假设没有边：`n` 个点就是 `n` 个分量',
              '每条边查两端的代表元：不同才合并，`res` 减一',
              '代表元相同的边是多余的（成环），不改变分量数'],
        summary=['时间近似 `O(n + m)`，空间 `O(n)`',
                 '只有合并成功才 `res -= 1`；边 `0—2` 已连通，不能减',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `fa = list(range(n))`（Python 3 的 range 不能赋值）',
                 '也可以 DFS/BFS 数连通块；并查集写法更短',
                 '同类题：261 以图判树'],
    ),
)
