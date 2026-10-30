CONFIG = dict(
    num=3515, title='带权树中的最短路径', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='DFS 时间戳 + 差分树状数组',
    tags=['树状数组', 'DFS 时间戳', '难度分 2312'],
    code='''
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    def update(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] += val
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    def pre(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.tree[i]
            i &= i - 1
        return res

class Solution:
    def treeQueries(self, n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n + 1)]
        for x, y, _ in edges:
            g[x].append(y)
            g[y].append(x)

        in_ = [0] * (n + 1)
        out = [0] * (n + 1)
        clock = 0
        def dfs(x: int, fa: int) -> None:
            nonlocal clock
            clock += 1
            in_[x] = clock  # 进来的时间
            for y in g[x]:
                if y != fa:
                    dfs(y, x)
            out[x] = clock  # 离开的时间
        dfs(1, 0)

        weight = [0] * (n + 1)
        diff = FenwickTree(n)
        def update(x: int, y: int, w: int) -> None:
            # 保证 y 是 x 的儿子
            if in_[x] > in_[y]:
                y = x
            d = w - weight[y]  # 边权的增量
            weight[y] = w
            # 把子树 y 中的最短路长度都增加 d（用差分树状数组维护）
            diff.update(in_[y], d)
            diff.update(out[y] + 1, -d)

        for e in edges:
            update(*e)

        ans = []
        for q in queries:
            if q[0] == 1:
                update(*q[1:])
            else:
                ans.append(diff.pre(in_[q[1]]))
        return ans
''',
    call='Solution().treeQueries(4, [[1,2,2],[1,3,4],[3,4,1]], [[2,4],[1,1,3,7],[2,4]])',
    expect=[5, 8],
    views=[
        dict(type='array', var='in_', label='in_[x]：进入时间（子树 x = [in_[x], out[x]]）', h=140,
             color=lambda S, i, v: 'blue' if i == S.get('x') and S.get('_line', 0) in range(33, 39) else None),
        dict(type='array', var='out', label='out[x]：子树里最大的进入时间', h=140),
        dict(type='array', var='weight', label='weight[y]：y 与父亲那条边的权', h=140,
             color=lambda S, i, v: 'yellow' if i == S.get('y') and S.get('_line', 0) in range(45, 52) else None),
        dict(type='array', var='diff.tree', label='diff.tree：差分树状数组（下标 1..n）', h=150),
        dict(type='text', fn=lambda S: (f"子树 `{S['y']}` = 时间戳区间 [{S['in_'][S['y']]}, {S['out'][S['y']]}]：区间加 `{S['d']}` = 在 {S['in_'][S['y']]} 加，在 {S['out'][S['y']]+1} 减" if S.get('_line', 0) in (50, 51) and 'd' in S and 'y' in S else ''), h=60),
    ],
    watch=['x', 'y', 'd', ('ans', 'ans', 'green')],
    captions={
        'g[x].append(y)': '无向边：`{x}` 和 `{y}` 互相加入邻接表',
        'clock += 1': '时钟 +1：`clock = {clock}`',
        'in_[x] = clock': '`in_[{x}] = {clock}`：进入节点 {x} 的时间戳',
        'dfs(y, x)': '递归进入儿子 `{x}`（父亲是 `{fa}`，不回头）',
        'out[x] = clock': '`out[{x}] = {clock}`：子树 {x} 的时间戳最大值（子树 = `[in_, out]`）',
        'if in_[x] > in_[y]': lambda S, B, r: (f'`in_[{S.x}] = {S.in_[S.x]}` > `in_[{S.y}] = {S.in_[S.y]}`：x 更晚进入 → ==x 才是儿子==，边权存在儿子上' if S.in_[S.x] > S.in_[S.y] else f'`in_[{S.x}] = {S.in_[S.x]}` < `in_[{S.y}] = {S.in_[S.y]}`：y 是儿子，不用换'),
        'y = x': '换成 `y = {y}`：保证 y 是儿子',
        'd = w - weight[y]': '边权增量 `d = {w} - {B.weight[y]}` = =={d}==',
        'weight[y] = w': '记下新边权：`weight[{y}] = {w}`',
        'diff.update(in_[y], d)': '差分：从时间戳 `{in_[y]}` 起往后都 +`{d}`',
        'diff.update(out[y] + 1': '子树结束后（时间戳 `{out[y]+1}`）抵消，只影响子树 y',
        'ans.append': '查询节点 `{q[1]}`：到根距离 = 差分前缀和 `diff.pre(in_[{q[1]}])`，进去数一数',
        'return res': '前缀和 `{res}` = 到根距离，追加进 `ans`',
        'if q[0] == 1': lambda S, B, r: ('操作 1：改边权 → 区间更新' if S.q[0] == 1 else '操作 2：查询到根距离 → 单点查询'),
        'update(*q[1:])': '修改边 `({q[1]}, {q[2]})` 为 `{q[3]}`',
        'self.tree[i] += val': '`tree[{i}]` += `{val}`',
        'i += i & -i': '`i += i & -i` → {i}',
        'res += self.tree[i]': '累加 `tree[{i}]`，`res` = {res}',
        'i &= i - 1': '`i &= i - 1` → {i}',
        'return ans': '所有查询结果 `{ans}`',
    },
    skip=['while i', 'res = 0', 'def ', 'nonlocal', 'for e in edges', 'self.tree = [0]', 'g = [[]', 'in_ = [0]', 'out = [0]', 'clock = 0',
          'weight = [0]', 'diff = Fenwick', 'ans = []', 'for x, y, _', 'g[y].append', 'for y in g[x]', 'clock += 1'],
    max_steps=95,
    cards=dict(
        one_liner='改一条边 = 一整棵子树的距离同时加 d：时间戳变区间，差分树状数组区间加',
        complexity='时间 `O((n+q) log n)`，空间 `O(n)`',
        problem=['以 1 为根的带权树，`[1,u,v,w]` 把边 `(u,v)` 改成 `w`',
                 '`[2,x]` 查根 1 到 x 的距离，按顺序返回所有查询结果',
                 '本视频：`n=4`，`edges=[[1,2,2],[1,3,4],[3,4,1]]` → `[5,8]`'],
        quote='如果把 x 到 y（y 是 x 的儿子）的边权增加 d，那么节点 1 到子树 y 中的所有节点的距离都会增加 d。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 给每个点记进入/离开时间戳，子树 y 的点 = 区间 `[in_[y], out[y]]`',
              '改边权 = 区间加 d；查询 = 单点读 `in_[x]`',
              '区间加用差分：`in_[y]` 处 +d，`out[y]+1` 处 −d；单点值 = 差分前缀和'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`',
                 '边权存在儿子节点上：`in_[x] > in_[y]` 说明 x 是儿子，换成 `y = x`',
                 '初始化也当作「把边权从 0 改成 w」，复用同一个 `update`',
                 '`out[y]+1` 可能等于 `n+1`，树状数组 `update` 的 `while` 会直接跳过',
                 '其他实现：Lazy 线段树、重链剖分（本视频演示差分树状数组）'],
    ),
)
