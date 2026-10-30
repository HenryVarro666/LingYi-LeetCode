def _fl(S):
    try:
        return S['f'][S['i'] + 1]
    except Exception:
        return None


def _costcolor(S, r, c, v):
    if 'i' not in S or 'n' not in S:
        return None
    if r == S['i']:
        return 'blue'
    if r == S['n'] - 1 - S['i']:
        return 'pink'
    return None


def _jk(S, B, ret):
    return (f'`(j,k)=({S.j},{S.k})` 合法：`{S.f[S.i][S.j][S.k]} + {S.c1} + {S.c2}` = {S.f[S.i][S.j][S.k] + S.c1 + S.c2} → `res` = =={S.res}==')


def _pre(S, B, ret):
    if 'pre_k' in B and B.pre_k == S.pre_k:
        return '这个 `pre_j` 的三种 `pre_k` 都算完'
    return f'里面一对颜色 `({S.pre_j}, {S.pre_k})`：要求 `j≠{S.pre_j}`，`k≠{S.pre_k}`，`j≠k`'


CONFIG = dict(
    num=3429, title='粉刷房子 IV', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='左右同时开工 · 多维 DP',
    tags=['灵神题单·动态规划', '难度分 2166'],
    code='''
class Solution:
    def minCost(self, n: int, cost: List[List[int]]) -> int:
        f = [[[0] * 3 for _ in range(3)] for _ in range(n // 2 + 1)]
        for i, row in enumerate(cost[:n // 2]):
            row2 = cost[-1 - i]
            for pre_j in range(3):
                for pre_k in range(3):
                    res = inf
                    for j, c1 in enumerate(row):
                        if j == pre_j:
                            continue
                        for k, c2 in enumerate(row2):
                            if k != pre_k and k != j:
                                res = min(res, f[i][j][k] + c1 + c2)
                    f[i + 1][pre_j][pre_k] = res
        # 枚举所有初始颜色，取最小值
        return min(map(min, f[-1]))
''',
    call='Solution().minCost(4, [[3,5,7],[6,2,9],[4,8,1],[7,3,5]])',
    expect=9,
    views=[
        dict(type='grid', var='cost', label='cost（蓝 = 第 i 行，粉 = 对称的第 n−1−i 行）', cell=64, h=270,
             color=_costcolor, cols=['色0', '色1', '色2']),
        dict(type='grid', var=_fl, label='f[i+1][pre_j][pre_k]（行 = pre_j，列 = pre_k，黄框 = 刚算出）', cell=64, h=260,
             rows=[0, 1, 2], cols=[0, 1, 2]),
        dict(type='text', fn=lambda S: (f"这一层涂 ==房子 {S['i']}== 和 ==房子 {S['n'] - 1 - S['i']}==；"
                                        f"里面一对的颜色是 `pre_j={S['pre_j']}`, `pre_k={S['pre_k']}`")
             if 'pre_j' in S and 'i' in S else '', h=60),
    ],
    watch=['i', 'pre_j', 'pre_k', 'j', 'k', ('res', 'res', 'green')],
    captions={
        'f = [[[0]': '`f[i]`：从外往里涂了 `i` 对；`pre_j, pre_k` 是==紧挨着里面那一对==的颜色。`f[0]` 全 0',
        'for i, row': lambda S, B, r: ('所有层都算完' if 'i' in B and B.i == S.i else f'第 `{S.i}` 层：同时涂房子 `{S.i}` 和房子 `{S.n - 1 - S.i}`（等距）'),
        'for pre_k': _pre,
        'res = min': _jk,
        'f[i + 1][pre_j][pre_k] = res': '`f[{i + 1}][{pre_j}][{pre_k}] = {res}`',
        'return min': '`f[-1]` 里取最小 → =={ret}==',
    },
    skip=['row2 = cost', 'for pre_j', 'res = inf', 'for j, c1', 'for k, c2', 'if j == pre_j', 'continue', 'if k != pre_k'],
    max_steps=50,
    cards=dict(
        one_liner='左右同时开工：涂 i 和 n−1−i，枚举这一对的颜色',
        complexity='时间 `O(nk^4)`（k=3），空间 `O(nk^2)`',
        problem=['`n` 栋房子排成一排，`cost[i][j]` 是把房子 `i` 涂成颜色 `j+1` 的成本',
                 '相邻不同色，==关于中点对称的两栋也不同色==，求最低总成本',
                 '示例：`n=4`，`cost=[[3,5,7],[6,2,9],[4,8,1],[7,3,5]]` → `9`'],
        quote='由于有等距异色的要求，考虑==左右同时开工==，涂 i 和 n-1-i 这两个房子。枚举房子 i 和 n-1-i 的颜色 j 和 k，问题变成涂剩余房子的最低成本。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每一步同时决定“左边一栋、右边一栋”，对称约束只发生在这一对内部（`j ≠ k`）',
              '相邻约束发生在这一对和更外一对之间（`j ≠ pre_j`，`k ≠ pre_k`）',
              '所以状态只需记住更外一对的颜色：`3 × 3`'],
        summary=['时间 `O(nk^4)`，`k = 3`；空间 `O(nk^2)`，可用滚动数组降到 `O(k^2)`',
                 '`f[0]` 全 0；答案是 `f[-1]` 里最小值，不是某个固定格子',
                 '易错：右边房子用 `cost[-1 - i]`，且 `k != j` 是对称约束',
                 '灵神另给了 `@cache` 记忆化写法，递推是它的 1:1 翻译'],
    ),
)
