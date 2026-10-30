def _F(costs):
    f0 = f1 = f2 = 0
    out = [0]
    for c in costs:
        f0, f1, f2 = f1, f2, min(f0 + 9, f1 + 4, f2 + 1) + c
        out.append(f2)
    return out


def _idx(S):
    """当前正在处理的是第几个台阶（下标 0 起 = 台阶 idx+1），没有则 None"""
    if 'f2' not in S or 'costs' not in S:
        return None
    F = _F(S['costs'])
    if S['f2'] not in F:
        return None
    k = F.index(S['f2'])
    line = S.get('_line')
    if line == 4:
        return k if k < len(S['costs']) else None
    if line == 5:
        return k - 1
    return None


def _dp(S):
    if 'f2' not in S:
        return None
    F = _F(S['costs'])
    k = F.index(S['f2'])
    return [F[j] if j <= k else '?' for j in range(len(F))]


def _dp_color(S, j, v):
    k = _idx(S)
    if k is None:
        return None
    if j == k + 1:
        return 'yellow'
    if S.get('_line') == 4 and j in (k, k - 1, k - 2) and j >= 0:
        return 'green'
    return None


def _cost_color(S, j, v):
    k = _idx(S)
    return 'yellow' if k is not None and j == k + 1 else None


def _formula(S):
    k = _idx(S)
    if k is None or 'f0' not in S:
        return '`f2` = 到 i-1 级的最小成本，`f1` = 到 i-2 级，`f0` = 到 i-3 级'
    i = k + 1
    if S['_line'] == 4:
        return f'`dp[{i}] = min(dp[{i-3}] + 9, dp[{i-2}] + 4, dp[{i-1}] + 1) + costs[{i}]`（越界的台阶补 0，永远不是最优）'
    return f'`dp[{i}] = min(...) + {S["c"]}` = =={S["f2"]}=='


CONFIG = dict(
    num=3693, title='爬楼梯 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='三个变量滚动的线性 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1560'],
    code='''
class Solution:
    def climbStairs(self, _, costs: List[int]) -> int:
        f0 = f1 = f2 = 0
        for c in costs:
            f0, f1, f2 = f1, f2, min(f0 + 9, f1 + 4, f2 + 1) + c
        return f2
''',
    call='Solution().climbStairs(4, [5, 1, 6, 2])',
    expect=11,
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var=_dp, label='dp[i]：从 0 爬到第 i 级的最小成本（黄 = 正在算，绿 = 能跳过来的三级）', h=260, cell=110,
             color=_dp_color),
        dict(type='array', var=lambda S: ['-'] + list(S['costs']), label='costs[i]（下标 = 台阶号）', h=240, cell=110,
             color=_cost_color),
    ],
    watch=[('f0', 'f0', 'cyan'), ('f1', 'f1', 'blue'), ('f2', 'f2', 'green'), ('c', 'c', 'yellow')],
    captions={
        'f0 = f1 = f2 = 0': '`f2 = dp[0] = 0`：站在第 0 级不花钱；`f0, f1` 是越界的 `dp[-2], dp[-1]`，先补 0',
        'for c in costs': lambda S, B, r: ('取第 `%d` 级台阶的成本 `c = %d`' % (_idx(S) + 1, S.c) if _idx(S) is not None
                                           else '台阶都处理完了，`f2` 就是 `dp[n]`'),
        'f0, f1, f2 =': lambda S, B, r: ('跳 3 级距离平方 `9`、跳 2 级 `4`、跳 1 级 `1`：`min(%d+9, %d+4, %d+1) + %d` = ==%d==；三个变量整体左移一格' % (
            B.f0, B.f1, B.f2, S.c, S.f2)),
        'return f2': '最后一级 `dp[n]` = `f2` = =={ret}==',
    },
    cards=dict(
        one_liner='最后一步跳 1/2/3 级，平方成本是 1/4/9',
        complexity='时间 `O(n·K)`（K=3），空间 `O(K)`',
        problem=['`n+1` 级台阶，一步只能跳 `1~3` 级；从 `i` 跳到 `j` 的成本是 `costs[j] + (j-i)^2`',
                 '求从第 0 级到第 `n` 级的最小总成本',
                 '示例：`n=4, costs=[5,1,6,2]` → `11`（走 `0→2→4`）'],
        quote='类似 70. 爬楼梯，用三个变量滚动计算。',
        quote_src='—— 灵茶山艾府题解（空间优化）',
        idea=['`dp[i] = min(dp[j] + (i-j)^2) + costs[i]`，`j` 取 `i-3 ~ i-1`',
              '`(i-j)^2` 只会是 `1/4/9`，所以直接写成 `f2+1、f1+4、f0+9`',
              '只依赖前三个状态，用 `f0, f1, f2` 滚动，空间 `O(1)`'],
        summary=['时间 `O(nK)`，K = 3；空间 `O(K)`',
                 '易错：题目 `costs` 下标从 1 开始，传入数组从 0 开始，`for c in costs` 刚好按顺序取',
                 '`f0, f1` 初值取 0 不会出错：靠它们跳到第 1、2 级反而更贵',
                 '原文先给记忆化搜索，再 1:1 翻译成递推 `f[i]`，最后才滚动优化；去掉 K=3 要用斜率优化'],
    ),
)
