COINS = [1, 2, 5]
AMOUNT = 5


def _cell_color(S, r, k, v):
    """当前格黄色，它依赖的两格：上方 f[i][c]（蓝，不选）和左边 f[i+1][c-x]（粉，继续选）"""
    if 'c' not in S or 'i' not in S or S['_line'] not in (8, 9, 10, 11):
        return None
    i, c, x = S['i'], S['c'], S['x']
    if (r, k) == (i + 1, c):
        return 'yellow'
    if (r, k) == (i, c):
        return 'blue'
    if c >= x and (r, k) == (i + 1, c - x):
        return 'pink'
    return None


def _formula(S):
    if 'f' not in S:
        return ''
    if 'c' in S and 'i' in S and S['_line'] in (9, 11):
        i, c, x, f = S['i'], S['c'], S['x'], S['f']
        if c < x:
            return f'`c = {c} < x = {x}`：只能不选 → `f[{i + 1}][{c}] = f[{i}][{c}] = {f[i + 1][c]}`'
        return f'`f[{i + 1}][{c}] = f[{i}][{c}] + f[{i + 1}][{c - x}] = {f[i][c]} + {f[i + 1][c - x]} =` =={f[i + 1][c]}=='
    if 'x' in S and 'c' not in S:
        return f'第 `i = {S["i"]}` 种硬币 `x = {S["x"]}`：算第 `{S["i"] + 1}` 行'
    return '`f[i+1][c]`：用前 `i+1` 种硬币凑出 `c` 的方案数'


def _if(S, B, ret):
    c, x = S.c, S.x
    if c < x:
        return f'`c = {c} < x = {x}`：放不下这枚硬币 → ==只能不选=='
    return f'`c = {c} ≥ x = {x}`：可以不选，也可以==继续选一枚== `{x}`'


CONFIG = dict(
    num=518, title='零钱兑换 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='完全背包：记忆化搜索 1:1 翻译成递推',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        n = len(coins)
        f = [[0] * (amount + 1) for _ in range(n + 1)]
        f[0][0] = 1
        for i, x in enumerate(coins):
            for c in range(amount + 1):
                if c < x:
                    f[i + 1][c] = f[i][c]
                else:
                    f[i + 1][c] = f[i][c] + f[i + 1][c - x]
        return f[n][amount]
''',
    call=f'Solution().change({AMOUNT}, {COINS})',
    expect=4,
    skip=['n = len', 'for c in range'],
    views=[
        dict(type='text', fn=_formula, size=27),
        dict(type='text', fn=lambda S: '第 0 行：不用硬币；第 1/2/3 行：可用硬币 `[1]`、`[1,2]`、`[1,2,5]`', size=22),
        dict(type='table', var='f', h=470, cell=104, color=_cell_color,
             label='f[i+1][c]（黄 = 正在算，蓝 = 上方：不选，粉 = 左边：继续选）',
             rows=lambda S: ['f[0]'] + [f'f[{k + 1}]' for k in range(len(COINS))],
             cols=lambda S: [f'c={k}' for k in range(AMOUNT + 1)],
             cursors=[('i + 1', 'c', 'yellow', '')]),
    ],
    watch=[('i', 'i'), ('x', 'x', 'orange'), ('c', 'c', 'yellow')],
    captions={
        'f = [[0]': '`f` 有 `n + 1` 行：第 0 行表示==一种硬币都不用==',
        'f[0][0] = 1': '翻译自边界 `dfs(-1, 0) = 1`：不用任何硬币凑出 0，也算一种方案',
        'for i, x in enumerate(coins)': lambda S, B, ret: (f'考虑第 `i = {S.i}` 种硬币 `x = {S.x}`，填第 `{S.i + 1}` 行'
                                                           if B.get('i') != S.i else '所有硬币都考虑完了'),
        'if c < x': _if,
        9: '`f[{i + 1}][{c}] = f[{i}][{c}] = {f[i + 1][c]}`（照抄上一行）',
        11: lambda S, B, ret: (f'不选 `f[{S.i}][{S.c}] = {S.f[S.i][S.c]}` + 继续选 `f[{S.i + 1}][{S.c - S.x}] = {S.f[S.i + 1][S.c - S.x]}`'
                               f' → =={S.f[S.i + 1][S.c]}=='),
        'return f[n][amount]': '答案 `f[{n}][{amount}]` = =={ret}==',
    },
    cards=dict(
        one_liner='选或不选：不再选第 i 种 + 继续选一枚第 i 种（加法原理）',
        complexity='时间 `O(n·amount)`，空间 `O(n·amount)`',
        problem=['硬币面额 `coins`（==每种无限枚==），凑成总金额 `amount` 的==组合数==',
                 '凑不出返回 0；`[1,2]` 和 `[2,1]` 算同一种',
                 '示例：`amount = 5, coins = [1,2,5]` → `4`',
                 '`5=5`、`5=2+2+1`、`5=2+1+1+1`、`5=1+1+1+1+1`'],
        before=[dict(heading='第一步：选或不选，写出记忆化搜索', chapter='② 思路', lines=[
            '`dfs(i, c)`：用前 `i` 种硬币组成金额 `c` 的方案数',
            '不再选第 `i` 种：`dfs(i-1, c)`；继续选一枚：`dfs(i, c - coins[i])`',
            '边界：`dfs(-1, 0) = 1`，`dfs(-1, >0) = 0`；入口 `dfs(n-1, amount)`',
            '答疑：「不用任何硬币」也算一种方案，否则所有返回值都是 0',
        ])],
        quote='根据==加法原理==，二者相加得 dfs(i,c) = dfs(i−1,c) + dfs(i,c−coins[i])。……如果事件 A 和事件 B 是==互斥==的，那么发生事件 A 或事件 B 的总数等于两者数量之和。',
        quote_src='—— 灵茶山艾府题解',
        idea_heading='第二步：1:1 翻译成递推',
        idea=['`dfs(i, c)` → `f[i+1][c]`：多出的第 0 行对应 `i = -1`',
              '`c < x`：只能不选，`f[i+1][c] = f[i][c]`',
              '否则 `f[i+1][c] = f[i][c] + f[i+1][c-x]`（左边那格在==同一行==：还能继续选）'],
        result='`f[3][5] = 4` ✓',
        summary=['时间 `O(n·amount)`；二维空间 `O(n·amount)`，可压成一维 `O(amount)`',
                 '循环顺序：==外层物品、内层容量==算的是组合；反过来算的是排列（对比 377 题）',
                 '边界 `f[0][0] = 1`：不用任何硬币凑出 0 是一种方案',
                 '空间优化：`f = [1] + [0] * amount`，`for c in range(x, amount + 1): f[c] += f[c - x]`'],
    ),
)
