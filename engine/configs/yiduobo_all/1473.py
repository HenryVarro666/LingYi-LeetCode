def _fc(S, r, c, v):
    if S.get('i') is None or S.get('j') is None or S.get('k') is None:
        return None
    if r == S['j'] and c == S.get('hk', S['k']):
        return 'green'
    return None


def _gc(S, r, c, v):
    j, k = S.get('j'), S.get('k')
    if j is None or k is None or S.get('i', 0) == 0 or S.get('_line', 0) < 18 or S.get('_line', 0) > 33:
        return None
    if r == j and c == k:
        return 'yellow'
    if r == j - 1 and c != k:
        return 'blue'
    return None


CONFIG = dict(
    num=1473, title='粉刷房子 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='三维 DP：房子 × 街区数 × 最后颜色',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def minCost(self, houses, cost, m, n, target):

        houses = [x - 1 for x in houses]
        
        for i in range(m):
            f = [[None] * n for _ in range(target + 1)]
            if i == 0:
                if houses[i] == -1:
                    for k in range(n):
                        f[1][k] = cost[0][k]
                else:
                    f[1][houses[i]] = 0
            else:
                for j in range(1, target + 1):
                    if j > i + 1:
                        continue
                    if houses[i] == -1:
                        for k in range(n):
                            if g[j][k] is not None and f[j][k] is None:
                                f[j][k] = g[j][k] + cost[i][k]
                            for p in range(n):
                                if p != k:
                                    if g[j - 1][p] is not None and (f[j][k] is None or g[j - 1][p] + cost[i][k] < f[j][k]):
                                        f[j][k] = g[j - 1][p] + cost[i][k]
                    else:
                        for k in range(n):
                            if k == houses[i]:
                                if g[j][k] is not None and (f[j][houses[i]] is None or g[j][k] < f[j][houses[i]]):
                                    f[j][houses[i]] = g[j][k]
                            else:
                                if g[j - 1][k] is not None and (f[j][houses[i]] is None or g[j - 1][k] < f[j][houses[i]]):
                                    f[j][houses[i]] = g[j - 1][k]
        
            g = f[:]

        res = None
        for k in range(n):
            if f[-1][k] is not None and (res is None or res > f[-1][k]):
                res = f[-1][k]
        
        if res is None:
            res = -1
        
        return res
''',
    call='Solution().minCost([0, 2, 0], [[1, 10], [10, 1], [1, 1]], 3, 2, 2)',
    expect=2,
    skip=['for j in range', 'for k in range', 'for p in range', 'if j > i + 1', 'continue', 'if p != k'],
    views=[
        dict(type='array', var='houses', label='houses（已减 1：-1 = 没刷，0/1 = 颜色）', h=170, cell=90, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='table', var='g', label='g[j][k]：上一栋的状态（黄 = 同色，蓝 = 换色，• = 不合法）', h=240, cell=84,
             rows=lambda S: [f'{j}块' for j in range(len(S['g']))], cols=lambda S: [f'色{k}' for k in range(len(S['g'][0]))],
             color=_gc),
        dict(type='table', var='f', label='f[j][k]：这一栋的状态（绿 = 刚更新）', h=240, cell=84,
             rows=lambda S: [f'{j}块' for j in range(len(S['f']))], cols=lambda S: [f'色{k}' for k in range(len(S['f'][0]))],
             color=lambda S, r, c, v: 'green' if S.get('_line') in (21, 25, 30, 33) and S.get('j') == r and S.get('k') == c else None),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'blue'), ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        'houses = [x - 1': '颜色减 1，对齐数组下标：`houses` = `{houses}`，`-1` 表示还没刷',
        'for i in range(m)': lambda S, B, r: (f'处理第 `{S.i}` 栋房子；`f` 只依赖上一栋的 `g`' if S.i != B.get('i') or 'f' not in B else '所有房子都处理完了'),
        'f = [[None]': '`f[j][k]` 初始为 None（不合法）：行 = 街区数，列 = 最后一栋的颜色',
        'if i == 0': lambda S, B, r: ('第一栋：街区数只能是 1' if S.i == 0 else f'`i = {S.i} > 0`：第 {S.i} 栋要从上一栋的 `g` 转移'),
        'houses[i] == -1': lambda S, B, r: (f'`houses[{S.i}] = -1`：没刷，每种颜色都要试，要付 `cost`' if S.houses[S.i] == -1
                                            else f'`houses[{S.i}] = {S.houses[S.i]}`：已经刷好了，颜色固定，不用花钱'),
        'f[1][k] = cost[0][k]': '第 0 栋没刷：刷成色 `{k}` 花 `{cost[0][k]}` → `f[1][{k}] = {f[1][k]}`',
        'f[1][houses[i]] = 0': '第 0 栋已是色 `{houses[0]}`：`f[1][{houses[0]}] = 0`',
        'f[j][k] = g[j][k] + cost': '同色延续：街区数不变，`f[{j}][{k}] = g[{j}][{k}] + cost = {g[j][k]} + {cost[i][k]}` = =={f[j][k]}==',
        'f[j][k] = g[j - 1][p] + cost': '换色新开街区：`g[{j-1}][{p}] + cost[{i}][{k}]` = =={f[j][k]}==，取更小者',
        'if k == houses[i]': lambda S, B, r: ('颜色等于 `houses[i]`：和上一栋同色，街区数不变，看 `g[j][k]`' if S.k == S.houses[S.i]
                                              else '颜色不同：这栋是新街区，来自 `g[j-1][k]`'),
        'f[j][houses[i]] = g[j][k]': '同色，街区数 j 不变：`f[{j}][{houses[i]}]` = =={f[j][houses[i]]}==',
        'f[j][houses[i]] = g[j - 1][k]': '换色，街区数 +1：`f[{j}][{houses[i]}]` = =={f[j][houses[i]]}==',
        'g = f[:]': '这一栋算完，`f` 变成下一栋的 `g`',
        'res = f[-1][k]': '`res` 更新为 `f[-1][{k}]` = =={res}==（取各颜色里最小）',
        'if g[j][k] is not None and f[j][k] is None': '没刷：刷成色 `{k}`，若上一栋也是色 `{k}`，接在同一街区（街区数仍是 `{j}`）：候选 `g[{j}][{k}]`',
        'if g[j - 1][p] is not None and (f[j][k]': '没刷：刷成色 `{k}`，若上一栋是别的色 `{p}` → 新开街区，候选 `g[{j-1}][{p}]`（None 则不合法）',
        'res = -1': '没有合法方案 → -1',
        'return res': '恰好 `target` 个街区的最小代价 =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j][k]：前 i 栋、恰好 j 个街区、最后一栋颜色 k 的最小代价',
        complexity='时间 `O(m·target·n^2)`，空间 `O(target·n)`',
        problem=['`m` 栋房子排成一排，`houses[i] = 0` 表示还没刷，否则是已刷颜色（`1..n`）',
                 '`cost[i][c-1]` 是把第 `i` 栋刷成颜色 `c` 的花费，要刚好分出 `target` 个街区（连续同色算一块）',
                 '示例：`houses=[0,2,0]`，`target=2` → `2`；无解返回 `-1`'],
        quote='若此时houses[i]为-1，需要选择一种颜色，接下来同样是枚举每种颜色k，若在当前房子刷上这种颜色，那么此时也有两种情况：当前刷的颜色k与上一个街区的颜色一致……与上一个街区不同……',
        quote_src='—— yiduobo 题解原文',
        idea=['颜色减 1 对齐下标；第一栋只可能是 1 个街区',
              '没刷：枚举颜色 `k`，同色接 `g[j][k]`，换色接 `g[j-1][p]`，都要加 `cost`',
              '已刷：颜色固定，不花钱；同色接 `g[j][k]`，不同色接 `g[j-1][k]`'],
        summary=['时间 `O(m·target·n^2)`，空间 `O(target·n)`（`g`、`f` 滚动）',
                 '用 `None` 表示不合法，比较前必须先判断 `is not None`',
                 '街区数 `j` 最多是 `i+1`，超出直接跳过',
                 '原文称可用最小值/次小值把 `n^2` 降到 `n`，但文中没有实现',
                 '代码在 Python 3 下无需修改即可运行'],
    ),
)
