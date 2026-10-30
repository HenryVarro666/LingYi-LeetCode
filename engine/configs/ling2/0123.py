PRICES = [3, 5, 1, 4]


def _cur_cell(S):
    if S.get('_line') == 9:
        return 0
    if S.get('_line') == 10:
        return 1
    return None


def _src(S, i, j, v):
    """紫 = 这一步转移用到的格子"""
    ln, jj = S.get('_line'), S.get('j')
    if jj is None or 'p' not in S:
        return None
    if ln == 9 and (i, j) == (jj, 1):
        return 'purple'
    if ln == 10 and (i, j) == (jj - 1, 0):
        return 'purple'
    return None


def _formula(S):
    if 'p' not in S or S.get('_line') not in (9, 10):
        return '`f[j][0]` 不持有，`f[j][1]` 持有（`j` 行 = 至多买入 `j − 1` 次）'
    j, p, f = S['j'], S['p'], S['f']
    F = lambda v: '-∞' if v == float('-inf') else str(v)  # noqa: E731
    if S['_line'] == 9:
        return f'`f[{j}][0] = max(f[{j}][0], f[{j}][1] + {p})` = =={F(f[j][0])}=='
    return f'`f[{j}][1] = max(f[{j}][1], f[{j - 1}][0] − {p})` = =={F(f[j][1])}=='


def _day(S, B, ret):
    if 'p' in S and (B.get('p') != S.p or 'p' not in B) and S.p in S.prices:
        d = S.prices.index(S.p)
        return f'第 `{d}` 天，价格 `p = {S.p}`；`j` 从 `k + 1 = 3` ==倒着==更新到 1'
    return '所有天都处理完了'


def _hold(S, B, ret):
    j, p = S.j, S.p
    old, buy = B.f[j][1], S.f[j - 1][0]
    F = lambda v: '-∞' if v == float('-inf') else str(v)  # noqa: E731
    if j == 1 and p != S.prices[0]:
        return '`f[1][1]` 仍是 `-∞`：至多买入 0 次，永远不可能持有股票'
    s = f'持有 `f[{j}][1]` = max(不动 `{F(old)}`, 今天买入 `{F(buy)} − {p}`) = =={F(S.f[j][1])}=='
    if j == 1:
        s += '（`f[0]` 是 `-∞`：一次都不能买）'
    return s


def _sell(S, B, ret):
    j, p = S.j, S.p
    F = lambda v: '-∞' if v == float('-inf') else str(v)  # noqa: E731
    if j == 1 and p != S.prices[0]:
        return '`f[1][0]` 仍是 0：一笔都不交易，利润就是 0'
    return f'不持有 `f[{j}][0]` = max(不动 `{F(B.f[j][0])}`, 今天卖出 `{F(B.f[j][1])} + {p}`) = =={F(S.f[j][0])}=='


CONFIG = dict(
    num=123, title='买卖股票的最佳时机 III', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP（188 题 k = 2）',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        k = 2
        f = [[-inf] * 2 for _ in range(k + 2)]
        for j in range(1, k + 2):
            f[j][0] = 0
        for p in prices:
            for j in range(k + 1, 0, -1):
                f[j][0] = max(f[j][0], f[j][1] + p)
                f[j][1] = max(f[j][1], f[j - 1][0] - p)
        return f[-1][0]
''',
    call=f'Solution().maxProfit({PRICES})',
    expect=5,
    skip=['for j in range'],
    views=[
        dict(type='array', var='prices', label='prices（每天的股价）', cell=96, h=215,
             pointers={'prices.index(p)': 'blue'}, pointer_labels={'prices.index(p)': 'p'},
             color=lambda S, i, v: 'blue' if 'p' in S and v == S['p'] else None),
        dict(type='text', fn=_formula, size=27),
        dict(type='table', var='f', label='f（行 j：j=0 哨兵 / j=1 至多 0 次 / j=2 至多 1 次 / j=3 至多 2 次）', cell=104, h=430,
             rows=['j=0', 'j=1', 'j=2', 'j=3'], cols=['不持有', '持有'],
             cursors=[('j', _cur_cell, 'yellow')], color=_src),
    ],
    watch=[('p', 'p', 'blue'), ('j', 'j', 'yellow'), ('答案 f[3][0]', lambda S: S['f'][3][0], 'green')],
    captions={
        'k = 2': '本题 = 188 题 `k = 2` 的情况：==至多完成 2 笔交易==（买入 + 卖出才算一笔）',
        'f = [[-inf]': '`f[j][0/1]`：至多买入 `j − 1` 次，当天结束时==不持有 / 持有==股票的最大利润，先全是 `-∞`',
        'f[j][0] = 0': lambda S, B, ret: (f'`f[{S.j}][0] = 0`：还没开始交易、手里没股票 → 利润 0；`j = 0` 行（交易 −1 次）==不合法==，保持 `-∞`'
                                          if S.j == 1 else f'`f[{S.j}][0] = 0`'),
        'for p in prices': _day,
        'f[j][0] = max(': _sell,
        'f[j][1] = max(': _hold,
        'return f[-1][0]': '答案 `f[3][0]`：至多 2 笔交易、最后==不持有==股票 → =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='188 题 k = 2：f[j][是否持有] 状态机 DP，j 倒序更新',
        complexity='时间 `O(nk)`，空间 `O(k)`（k = 2 时就是 `O(n)` / `O(1)`）',
        problem=['`prices[i]` 是股票第 `i` 天的价格，你==最多完成两笔交易==',
                 '不能同时参与多笔交易：再次买入前必须卖掉手里的股票',
                 '示例：`[3,3,5,0,0,3,1,4]` → `6`；本视频：`[3,5,1,4]` → `5`'],
        quote='本题相当于 188. 买卖股票的最佳时机 IV 的 k=2 的情况，做法是完全一样的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['188 题：`dfs(i, j, hold)` = 在 `[0,i]` 中至多买入 `j` 次、第 i 天结束时是否持有',
              '持有 ← 昨天就持有，或==今天买入==（用掉一次：`f[j−1][0] − p`）；不持有 ← 昨天就不持有，或==今天卖出== `f[j][1] + p`',
              '翻译成递推再空间优化：`j = 0` 行对应交易 −1 次，初始 `-∞`；`j` 倒序，用到的都是昨天的值'],
        result='`f[3][0] = 5`：`3` 买 `5` 卖赚 2，`1` 买 `4` 卖赚 3 ✓',
        summary=['时间 `O(nk)`，空间 `O(k)`；本题 `k = 2`',
                 '第二维开 `k + 2`：多出的 `f[0]` 是==哨兵==，表示不合法（-∞）',
                 '易错：`j` 要==倒序==，`f[j][1]` 用的 `f[j−1][0]` 必须还是昨天的',
                 '答案取 `f[-1][0]`：最后手里不能有股票',
                 '188 题解还有记忆化搜索、二维递推写法；「恰好 / 至少 k 次」只需改初始值'],
    ),
)
