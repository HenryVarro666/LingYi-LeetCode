CONFIG = dict(
    num=1168, title='水资源分配优化', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='改造 Kruskal：合并时去掉较大的打井成本',
    tags=['最小生成树'],
    code='''
class Solution(object):
    def minCostToSupplyWater(self, n, wells, pipes):

        fa = list(range(n))
        res = sum(wells)

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for x, y, c in sorted(pipes, key=lambda d:d[2]):
            x -= 1
            y -= 1

            fa_x = find(x)
            fa_y = find(y)

            if fa_x != fa_y and (wells[fa_x] >= c or wells[fa_y] >= c):
                res += c
                if wells[fa_x] < wells[fa_y]:
                    fa[fa_y] = fa_x
                    res -= wells[fa_y]
                else:
                    fa[fa_x] = fa_y
                    res -= wells[fa_x]

        return res
''',
    call='Solution().minCostToSupplyWater(4, [4, 3, 5, 2], [[1,2,2],[2,3,4],[3,4,3],[1,4,6]])',
    expect=10,
    views=[
        dict(type='array', var='wells', label='wells（打井成本；绿 = 所在连通块的代表井）', cell=84, h=220,
             pointers={'fa_x': 'blue', 'fa_y': 'pink'},
             color=lambda S, i, v: 'green' if S['fa'][i] == i else None),
        dict(type='array', var='fa', label='fa（并查集父节点；连通块的根就是块里最便宜的井）', cell=84, h=190),
        dict(type='text', h=80, size=30,
             fn=lambda S, B: ((lambda T: f"当前管道：村庄 {T['x'] + 1} — 村庄 {T['y'] + 1}，造价 =={T['c']}==" if 'c' in T and 'y' in T else '管道按造价从小到大扫描')(B if ('x' in S['_inner'] and 'fa_x' not in S['_inner']) else S))),
    ],
    watch=[('res', 'res', 'green'), 'fa_x', 'fa_y'],
    skip=['def find', 'fa = list', 'if fa[x] != x:', 'fa[x] = find(fa[x])', 'return fa[x]'],
    captions={
        'res = sum(wells)': '一开始每个村子都自己打井：`res = sum(wells)` = =={res}==（每个连通块各有一口井）',
        'for x, y, c in sorted': lambda S, B, r: ('管道全部扫完' if 'x' in B and (S.x, S.y, S.c) == (B.x, B.y, B.c)
                                                  else f'把它看成 ==Kruskal==：管道按造价从小到大排序 → 当前管道 `{S.x} - {S.y}` 造价 `{S.c}`'),
        'x -= 1': '题目村庄编号从 1 开始，减 1 变成下标：`x = {x}`',
        'y -= 1': '`y = {y}`',
        'fa_x = find(x)': '找下标 `{B.x}` 的村庄所在连通块的根 `fa_x`',
        'fa_y = find(y)': '找下标 `{B.y}` 的村庄所在连通块的根 `fa_y`',
        'if fa_x != fa_y and': lambda S, B, r: (
            f'根不同，且某一块的井成本 ≥ 管道 `{S.c}`（`wells[{S.fa_x}]={S.wells[S.fa_x]}`，`wells[{S.fa_y}]={S.wells[S.fa_y]}`）→ 通管道比打井划算，合并' if (S.fa_x != S.fa_y and (S.wells[S.fa_x] >= S.c or S.wells[S.fa_y] >= S.c))
            else (f'已在同一块（根 `{S.fa_x}`）→ 跳过' if S.fa_x == S.fa_y
                  else f'两块的井都比管道 `{S.c}` 便宜（`{S.wells[S.fa_x]}`、`{S.wells[S.fa_y]}`）→ 通管道反而更贵，不合并')),
        'res += c': '先付管道费：`res` = =={res}==',
        'if wells[fa_x] < wells[fa_y]': lambda S, B, r: f'比两块的井成本：`{S.wells[S.fa_x]}` vs `{S.wells[S.fa_y]}`，==保留便宜的井，贵的那口井不要了==',
        'fa[fa_y] = fa_x': '`fa_x` 的井更便宜，当根：`fa[{fa_y}] = {fa_x}`',
        'fa[fa_x] = fa_y': '`fa_y` 的井不贵于对方，当根：`fa[{fa_x}] = {fa_y}`',
        'res -= wells[fa_y]': '去掉贵井的成本 `{wells[fa_y]}` → `res` = =={res}==',
        'res -= wells[fa_x]': '去掉贵井的成本 `{wells[fa_x]}` → `res` = =={res}==',
        'return res': '最小总成本 `{res}`',
    },
    cards=dict(
        one_liner='每个连通块保留最便宜的一口井，其余靠管道',
        complexity='时间 `O(E log E)`，空间 `O(n)`',
        problem=['`n` 个村庄，第 `i` 个村庄打井成本 `wells[i-1]`',
                 '`pipes[j] = [a, b, c]` 表示在 a、b 之间铺管道成本 c，求让所有村庄有水的最小总成本',
                 '本视频：`wells=[4,3,5,2]`，4 条管道'],
        quote='初始化答案为所有节点值之和，表示在一开始每棵树都是独立的。……将这两个连通块合并，同时将这条边的权重累加到答案中并将这两个连通块中最小值较大的一方从答案中移除。',
        quote_src='—— yiduobo 题解原文',
        idea=['不引入虚拟点，直接在 Kruskal 上改：一开始每个村子各自打井，`res = sum(wells)`',
              '管道造价 `c` 从小到大扫；两块不连通、且至少一块的井 `≥ c` 才值得合并',
              '合并后只需要一口井：付管道费 `c`，扣掉两口井里较贵的那口；根始终是便宜的井'],
        summary=['时间 `O(E log E)`，并查集近似常数；空间 `O(n)`',
                 '关键判断：`wells[fa_x] >= c or wells[fa_y] >= c`，两口井都比管道便宜就不合并',
                 '`fa` 的根下标同时是该块最便宜井的下标，所以 `wells[根]` 就是块内最小值',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `fa = list(range(n))`'],
    ),
)
