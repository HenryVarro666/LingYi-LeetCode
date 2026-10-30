CONFIG = dict(
    num=261, title='以图判树', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='边数检查 · 并查集判环',
    tags=['图论算法'],
    code='''
class Solution(object):
    def validTree(self, n, edges):

        if len(edges) != n - 1:
            return False
        
        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        fa = list(range(n))
        for x, y in edges:
            fa_x = find(x)
            fa_y = find(y)
            if fa_x == fa_y:
                return False
            fa[fa_x] = fa_y
        
        return True
''',
    call='Solution().validTree(5, [[0,1],[1,2],[2,3],[1,3]])',
    expect=False,
    views=[
        dict(type='array', var='fa', label='fa（并查集：fa[i] 是 i 的父亲）', pointers={'fa_x': 'blue', 'fa_y': 'pink'}, h=200,
             color=lambda S, i, v: 'green' if v != i else None),
        dict(type='array', var='edges', label='edges（按顺序逐条加入）', h=190, cell=110,
             pointers={}, color=lambda S, i, v: None),
        dict(type='calls', h=140),
    ],
    watch=[('n', 'n'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('fa_x', 'fa_x', 'blue'), ('fa_y', 'fa_y', 'pink')],
    captions={
        'if len(edges) != n - 1': lambda S, B, r: (f'一棵 `n={S.n}` 个点的树恰有 `n − 1 = {S.n - 1}` 条边；现有 `{len(S.edges)}` 条 → ' + ('不等，直接 False' if len(S.edges) != S.n - 1 else '相等，只需再保证无环')),
        'fa = list(range(n))': '初始每个点自成一个集合：`fa[i] = i`',
        'for x, y in edges': '依次加入边 `{x} — {y}`',
        'fa_x = find(x)': '调用 `find({x})`：沿父亲往上找 `{x}` 所在集合的代表元',
        'fa_y = find(y)': '调用 `find({y})`：找 `{y}` 所在集合的代表元',
        'if fa_x == fa_y': lambda S, B, r: (f'`fa_x = {S.fa_x}` ==等于== `fa_y = {S.fa_y}`：两点已连通，再加这条边就==成环== → 返回 False' if S.fa_x == S.fa_y else f'`fa_x = {S.fa_x}` ≠ `fa_y = {S.fa_y}`：还不连通，这条边不会成环'),
        'fa[fa_x] = fa_y': '合并两个集合：`fa[{fa_x}] = {fa_y}`',
        'if fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] = {S.fa[S.x]}` ≠ `{S.x}`：`{S.x}` 不是代表元，继续往上找' if S.fa[S.x] != S.x else f'`fa[{S.x}] == {S.x}`：`{S.x}` 就是代表元'),
        'fa[x] = find(fa[x])': '路径压缩：`fa[{x}]` 直接指向代表元 `{fa[x]}`',
        'return False': lambda S, B, r: '边数不对或有环 → ==不是树==',
        'return True': '没有出现环，边数又是 `n−1` → 是树',
    },
    skip=['def find', 'return fa[x]'],
    cards=dict(
        one_liner='边数必须是 n−1，再用并查集保证加边不成环',
        complexity='时间 `O(n α(n))`，空间 `O(n)`',
        problem=['给 `n` 个点（编号 `0..n-1`）和无向边列表 `edges`，判断它们能否构成一棵树',
                 '树 = 连通且无环；本视频示例：`n=5, edges=[[0,1],[1,2],[2,3],[1,3]]`',
                 '边数 `4 = n − 1` 但 `1—2—3—1` 成环，点 `4` 也没连上 → `False`'],
        quote='首先，如果给出的图是一棵树，那么图中边的数量必须恰好等于节点数量减去1，因此可以先检测数组edges的长度是否恰好等于n - 1',
        quote_src='—— yiduobo 题解原文',
        idea=['边数 `n − 1` 是必要条件，先用它快速排除',
              '再逐条加边：两端代表元相同说明已经连通，再连就==形成环==',
              '边数 `n − 1` 且无环，就保证了连通，所以一定是树'],
        summary=['时间近似 `O(n)`，空间 `O(n)`',
                 '先判边数再判环：边数 `n−1` + 无环 ⇒ 连通',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `fa = list(range(n))`（Python 3 的 range 不能赋值）',
                 '也可以建图后用 BFS/DFS 判环；并查集代码更短',
                 '同类题：323 无向图中连通分量的数目'],
    ),
)
