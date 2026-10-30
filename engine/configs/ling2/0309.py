PRICES = [1, 2, 3, 0, 2]

CODE = '''
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        f = [[0] * 2 for _ in range(n + 2)]
        f[1][1] = -inf
        for i, p in enumerate(prices):
            f[i + 2][0] = max(f[i + 1][0], f[i + 1][1] + p)
            f[i + 2][1] = max(f[i + 1][1], f[i][0] - p)
        return f[-1][0]
'''
_LINES = CODE.strip('\n').split('\n')
L0 = [k + 1 for k, t in enumerate(_LINES) if 'f[i + 2][0] =' in t][0]
L1 = [k + 1 for k, t in enumerate(_LINES) if 'f[i + 2][1] =' in t][0]


def _table(S):
    f = S.get('f')
    if f is None:
        return None
    return [[r[0] for r in f], [r[1] for r in f]]


def _color(S, r, c, v):
    line = S.get('_line')
    i = S.get('i')
    if i is None or line not in (L0, L1):
        return None
    if line == L0:
        if (r, c) == (0, i + 2):
            return 'green'
        if c == i + 1:
            return 'blue'
    else:
        if (r, c) == (1, i + 2):
            return 'green'
        if (r, c) == (1, i + 1):
            return 'blue'
        if (r, c) == (0, i):
            return 'pink'
    return None


def _fmt(x):
    return '-∞' if x == float('-inf') else str(x)


def _formula(S):
    line = S.get('_line')
    i, f = S.get('i'), S.get('f')
    if i is None or line not in (L0, L1):
        return '列 = 第 i 天（`f[i+2]` 存第 i 天，前两列是边界）'
    p = S['p']
    if line == L0:
        a, b = f[i + 1][0], f[i + 1][1]
        return f"不持有：`max({_fmt(a)}, {_fmt(b)} + {p})` = =={f[i + 2][0]}==（休息 / 今天卖）"
    a, b = f[i + 1][1], f[i][0]
    return f"持有：`max({_fmt(a)}, {_fmt(b)} − {p})` = =={_fmt(f[i + 2][1])}==（粉色 = ==前天== 不持有，再买）"


def _c0(S, B, r):
    i, p, f = S.i, S.p, S.f
    a, b = f[i + 1][0], f[i + 1][1] + p
    why = '昨天就不持有，今天休息' if a >= b else f'昨天持有，今天以 {p} 卖出'
    return f'第 {i} 天结束==不持有==：{why} → `f[{i + 2}][0] = {f[i + 2][0]}`'


def _c1(S, B, r):
    i, p, f = S.i, S.p, S.f
    a, b = f[i + 1][1], f[i][0] - p
    why = '昨天就持有，今天休息' if a >= b else f'==前天==不持有（昨天不能卖），今天以 {p} 买入'
    return f'第 {i} 天结束==持有==：{why} → `f[{i + 2}][1] = {_fmt(f[i + 2][1])}`'


CONFIG = dict(
    num=309, title='买卖股票的最佳时机含冷冻期', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP（递推）',
    tags=['热题173'],
    code=CODE,
    call=f'Solution().maxProfit({PRICES})',
    expect=3,
    skip=['n = len'],
    views=[
        dict(type='array', var='prices', label='prices', cell=84, pointers={'i': 'blue'}, h=200),
        dict(type='text', fn=_formula, h=64),
        dict(type='table', var=_table, label='f（行：0 = 不持有 / 1 = 持有；列：第几天）', cell=96, h=330,
             rows=['不持有', '持有'], cols=list(range(-2, len(PRICES))), color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('p', 'p')],
    captions={
        'f = [[0] * 2': '`f[i+2][0/1]`：第 i 天结束时==不持有 / 持有==股票的最大利润（下标整体 +2）',
        'f[1][1] = -inf': '第 -1 天就持有股票是不可能的 → `-inf`；第 -1、-2 天不持有利润都是 0',
        'for i, p in enumerate': lambda S, B, r: (f'第 `{S.i}` 天，价格 `p = {S.p}`' if S.get('i') != B.get('i') else '所有天都算完了'),
        'f[i + 2][0] =': _c0,
        'f[i + 2][1] =': _c1,
        'return f[-1][0]': '最后一天==不持有==股票才是最大利润：=={ret}==',
    },
    cards=dict(
        one_liner='和 122 题只差一处：买入时从「前天不持有」转移过来',
        complexity='时间 `O(n)`，空间 `O(n)`（可优化到 `O(1)`）',
        problem=['`prices[i]` 是第 i 天的股价，可以多次买卖，但手里==最多一股==',
                 '卖出后的==第二天不能买入==（冷冻期 1 天），求最大利润',
                 '示例：`[1,2,3,0,2]` → `3`（买、卖、冷冻、买、卖）',
                 '示例：`[1]` → `0`'],
        quote='只需修改一处：在计算持有股票的状态时，把 dfs(i−1,0) 改成 ==dfs(i−2,0)==。道理和 198. 打家劫舍是一样的，因为第 i 天买股票的话第 i−1 天不能卖。',
        quote_src='—— 灵茶山艾府题解：教你一步步思考动态规划',
        idea=['状态：第 i 天结束时 ==持有 / 不持有== 股票的最大利润',
              '不持有 = max(昨天不持有, 昨天持有 + 今天卖)',
              '持有 = max(昨天持有, ==前天==不持有 − 今天买)'],
        summary=['时间 `O(n)`；滚动成 `pre0, f0, f1` 三个变量后空间 `O(1)`',
                 '`f[i-2][0]` 不代表前天一定卖了，而是前天不持有时的最优值',
                 '边界：多了 `dfs(-2,0) = 0`；`f[1][1] = -inf` 表示第 -1 天不可能持有',
                 '题解先写记忆化搜索，再 1:1 翻译成递推（本视频），最后空间优化',
                 '同系列：121 / 122 / 123 / 188 / 714'],
    ),
)
