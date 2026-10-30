CONFIG = dict(
    num=1135, title='最低成本联通所有城市', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Kruskal 最小生成树 + 并查集',
    tags=['最小生成树'],
    code='''
class Solution(object):
    def minimumCost(self, n, connections):

        fa = list(range(n))

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        res = 0
        linked = 0
        for x, y, cost in sorted(connections, key=lambda d:d[2]):
            fa_x = find(x - 1)
            fa_y = find(y - 1)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                linked += 1
                res += cost
                if linked == n - 1:
                    return res
        
        return -1
''',
    call='Solution().minimumCost(5, [[1,2,5],[1,3,6],[2,3,1],[3,4,2],[4,5,7],[2,5,9]])',
    expect=15,
    views=[
        dict(type='array', var='fa', label='fa（并查集：fa[i] = i 的父节点，城市编号从 0 开始）', cell=84, h=240,
             pointers={'fa_x': 'blue', 'fa_y': 'pink'},
             color=lambda S, i, v: 'green' if S['fa'][i] == i else None),
        dict(type='text', h=90, size=30,
             fn=lambda S, B: ((lambda T: f"当前边：城市 {T['x']} — 城市 {T['y']}，造价 =={T['cost']}==" if 'cost' in T and 'x' in T else '按造价从小到大扫描所有道路')(B if ('x' in S['_inner'] and 'fa_x' not in S['_inner'] and 'cost' in B) else S))),
        dict(type='text', h=70, size=28,
             fn=lambda S: (f"已选 {S['linked']} 条边（需要 {S['n'] - 1} 条），总造价 =={S['res']}==" if 'linked' in S else '')),
    ],
    watch=[('linked', 'linked', 'orange'), ('res', 'res', 'green'), 'fa_x', 'fa_y'],
    skip=['def find', 'fa = list', 'if fa[x] != x:', 'fa[x] = find(fa[x])', 'return fa[x]'],
    captions={
        'res = 0': '`res` 累计造价，`linked` 记录已经连了几条边',
        'for x, y, cost in sorted': '最小生成树的 ==Kruskal==：道路按造价从小到大排序，依次尝试 → 当前边 `{x} - {y}` 造价 `{cost}`',
        'fa_x = find(x - 1)': '用并查集 `find` 找 `{B.x}` 号城市所在连通块的根（编号减 1 变成下标 `{B.x - 1}`）',
        'fa_y = find(y - 1)': '同样找 `{B.y}` 号城市所在连通块的根（下标 `{B.y - 1}`）',
        'if fa_x != fa_y': lambda S, B, r: (f'根不同（`{S.fa_x}` ≠ `{S.fa_y}`）→ 还没连通，这条边有用' if S.fa_x != S.fa_y
                                             else f'根相同（都是 `{S.fa_x}`）→ 已经连通，再连会成环，丢掉这条边'),
        'fa[fa_x] = fa_y': '合并两个连通块：把 `{fa_x}` 挂到 `{fa_y}` 下面，`fa = {fa}`',
        'linked += 1': '又连上一条边，`linked = {linked}`',
        'res += cost': '造价累加：`{B.res} + {cost}` = =={res}==',
        'if linked == n - 1': lambda S, B, r: (f'`linked = {S.linked}` = `n - 1`：{S.n} 座城市只需 {S.n - 1} 条边就连通 → 提前返回' if S.linked == S.n - 1
                                                else f'`linked = {S.linked}` < `{S.n - 1}`，还没连通，继续'),
        'return res': '全部连通，最低成本 `{res}`',
        'return -1': '扫完所有边仍没连通 → `-1`',
    },
    cards=dict(
        one_liner='最小生成树：边按造价排序，不成环就选',
        complexity='时间 `O(E log E)`，空间 `O(n)`',
        problem=['`n` 座城市（编号 1~n），`connections[i] = [x, y, cost]` 表示 x、y 之间修路的成本',
                 '求把所有城市连通的最低总成本，做不到返回 `-1`',
                 '本视频：`n=5`，6 条路 → `15`'],
        quote='非常标准的最小生成树问题，常规的处理方法有prim算法以及kruskal算法。我在这里使用的是后者。',
        quote_src='—— yiduobo 题解原文',
        idea=['Kruskal：造价从小到大扫描，==两端已连通的边直接跳过==，否则选中并合并',
              '用并查集 `fa` 判断连通：根相同就是已连通',
              '选满 `n - 1` 条边就一定连通，可以提前返回；扫完不足就是 `-1`'],
        summary=['时间 `O(E log E)`（排序），并查集带路径压缩近似常数',
                 '城市编号从 1 开始，`find(x - 1)` 要减 1',
                 '返回 `-1` 的情况：边不够，图本身不连通',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `fa = list(range(n))`（Python 3 的 range 不能赋值）'],
    ),
)
