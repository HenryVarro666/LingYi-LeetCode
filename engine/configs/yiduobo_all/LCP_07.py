CONFIG = dict(
    num='LCP 07', title='传递信息', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='按步数 DP · 滚动数组',
    tags=['图论算法', '动态规划'],
    code='''
class Solution(object):
    def numWays(self, n, relation, k):

        m = {}
        for x, y in relation:
            if x not in m:
                m[x] = set()
            m[x].add(y)
        
        f = [0] * n
        f[0] = 1
        for _ in range(k):
            g = [0] * n
            for x in range(n):
                if f[x] > 0:
                    for y in m.get(x, set()):
                        g[y] += f[x]
            f = g[:]
        
        return f[-1]
''',
    call='Solution().numWays(5, [[0,2],[2,1],[3,4],[2,3],[1,4],[2,0],[0,4]], 3)',
    expect=3,
    views=[
        dict(type='map', var='m', fmt=lambda k, v: f'{k} → {sorted(v)}', label='m（邻接表：谁能把信息传给谁）', h=210),
        dict(type='array', var='f', label='f[j]：走了当前步数后，停在 j 的路径条数', pointers={'x': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='g', label='g[j]：再多走一步后的条数（正在累加）', pointers={'y': 'pink'}, h=170,
             color=lambda S, i, v: 'yellow' if v else None),
    ],
    watch=[('_', '_', 'cyan'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('k', 'k')],
    captions={
        'm = {}': '用字典 `m` 存每个人能传给谁',
        'm[x] = set()': '`{x}` 还没有出边 → 先建一个空集合',
        'm[x].add(y)': '`{x}` 能传给 `{y}`：`m[{x}] = {sorted(m[x])}`',
        'f = [0] * n': '`f[j]` = 恰好传 `i` 次、到达 `j` 的方案数',
        'f[0] = 1': '传 0 次时只在 `0` 号，方案数 1',
        'for _ in range(k)': '第 `{_ + 1}` 轮：在每条路径的终点上再传一步（共 `k = {k}` 轮）',
        'g = [0] * n': '新一轮的 `g` 清零；每轮只依赖上一轮 `f`，所以用滚动数组省掉 `i` 维',
        'for x in range(n)': '看起点 `x = {x}`',
        'if f[x] > 0': lambda S, B, r: (f'`f[{S.x}] = {S.f[S.x]} > 0`：有 {S.f[S.x]} 条路径停在 `{S.x}`，可以继续传' if S.f[S.x] > 0 else f'`f[{S.x}] = 0`：没有路径停在 `{S.x}`，跳过'),
        'for y in m.get': '`{x}` 能传给 `{sorted(m.get(x, set()))}`',
        'g[y] += f[x]': '`{x} → {y}`：停在 `{x}` 的 `{f[x]}` 条路径都能走到 `{y}` → `g[{y}] = {g[y]}`',
        'f = g[:]': '这一轮结束：`f` 换成 `g` = `{f}`',
        'return f[-1]': '传 `k` 次后停在 `n−1` 的方案数：`{f[-1]}`',
    },
    skip=['for x in range(n)', 'g = [0] * n', 'for y in m.get'],
    max_steps=120,
    cards=dict(
        one_liner='f[j] 记录走了 i 步停在 j 的路径数，每轮再走一步',
        complexity='时间 `O(k·(n+m))`，空间 `O(n + m)`',
        problem=['有向图：`relation[i] = [a, b]` 表示 `a` 能把信息传给 `b`',
                 '从编号 `0` 出发，恰好传 `k` 次，最后到达 `n−1` 的方案数（可重复经过同一人）',
                 '示例：`n=5, k=3`，边 `[[0,2],[2,1],[3,4],[2,3],[1,4],[2,0],[0,4]]` → `3`'],
        quote='我在这里采用的是动态规划的做法，令f[i][j]表示长度为i，终点为j的所有可行路径条数。对于f[i][j]，可以认为从某条长度为i - 1的路径终点再走一步来到j',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` = 长度 `i`、终点 `j` 的路径条数，转移：上一轮的终点再走一步',
              '本轮只依赖上一轮，用滚动数组去掉 `i` 维',
              '原文的写法是「刷表」：从 `x` 出发把 `f[x]` 加到所有 `y` 上'],
        summary=['时间 `O(k·(n+m))`，空间 `O(n+m)`',
                 '路径可重复经过节点，所以不用记 visited',
                 '每轮必须用新数组 `g`，不能原地改 `f`，否则同一轮会多走几步',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '数据规模小，也可以直接 DFS 暴力枚举所有路径'],
    ),
)
