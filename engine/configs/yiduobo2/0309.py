PRICES = [1, 4, 0, 5, 2, 6]  # 价格互不相同，方便由 price 反推是第几天

CODE = '''
class Solution(object):
    def maxProfit(self, prices):
        if len(prices) < 2:
            return 0

        hold = -prices[0]
        cold = 0
        sell = None

        for price in prices[1:]:
            tmp_hold = hold
            hold = max(hold, cold - price)
            if sell is not None:
                cold = max(cold, sell)
            sell = tmp_hold + price

        return max(sell, cold)
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(s):
    return [k + 1 for k, t in enumerate(_LINES) if s in t][0]


L_FOR, L_TMP, L_HOLD, L_IF, L_COLD, L_SELL, L_RET = (
    _ln('for price in'), _ln('tmp_hold = hold'), _ln('hold = max('), _ln('if sell is not None'),
    _ln('cold = max('), _ln('sell = tmp_hold'), _ln('return max('))


def _dp():
    n = len(PRICES)
    hold, sell, cold = [None] * n, [None] * n, [None] * n
    hold[0], cold[0] = -PRICES[0], 0
    for i in range(1, n):
        hold[i] = max(hold[i - 1], cold[i - 1] - PRICES[i])
        cold[i] = max(cold[i - 1], sell[i - 1]) if sell[i - 1] is not None else cold[i - 1]
        sell[i] = hold[i - 1] + PRICES[i]
    return hold, sell, cold


HOLD, SELL, COLD = _dp()


def _day(S):
    if 'price' not in S:
        return 0
    return PRICES.index(S['price'])


def _table(S):
    if 'hold' not in S:
        return None
    n, line = len(PRICES), S.get('_line')
    rows = [[None] * n for _ in range(3)]
    if 'price' not in S:  # 第 0 天的初始化
        rows[0][0] = S['hold']
        rows[2][0] = S.get('cold')
        return rows
    d = _day(S)
    for k in range(d):
        rows[0][k], rows[1][k], rows[2][k] = HOLD[k], SELL[k], COLD[k]
    finished = line == L_RET or (line == L_FOR and S['sell'] == SELL[d] and d == n - 1)
    done = {L_HOLD: {0}, L_IF: {0}, L_COLD: {0, 2}, L_SELL: {0, 1, 2}}.get(line, set())
    if finished:
        done = {0, 1, 2}
    cur = {0: S['hold'], 1: S['sell'], 2: S['cold']}
    for r in done:
        rows[r][d] = cur[r]
    return rows


def _color(S, r, c, v):
    if 'price' not in S:
        return None
    d, line = _day(S), S.get('_line')
    src = {L_HOLD: [(0, d - 1), (2, d - 1)], L_COLD: [(2, d - 1), (1, d - 1)], L_SELL: [(0, d - 1)]}.get(line, [])
    tgt = {L_HOLD: (0, d), L_COLD: (2, d), L_SELL: (1, d)}.get(line)
    if (r, c) == tgt:
        return 'green'
    if (r, c) in src:
        return 'blue'
    if line == L_TMP and (r, c) == (0, d - 1):
        return 'purple'
    return None


def _hold(S, B, r):
    a, b = B.hold, B.cold - S.price
    if b > a:
        return f'hold：前一天是冷冻期，今天以 {S.price} 买入 `{B.cold} − {S.price} = {b}` 更优 → `hold = {S.hold}`'
    return f'hold：`max({a}, {B.cold} − {S.price})`，继续持仓更优 → `hold = {S.hold}`'


def _if(S, B, r):
    if B.sell is None:
        return '`sell` 还是 `None`（第 0 天不可能卖出）→ 冷冻期只能从冷冻期转移，`cold` 不变'
    return f'前一天的 `sell = {B.sell}` 有效 → 更新 cold'


def _cold(S, B, r):
    if B.sell > B.cold:
        return f'cold：前一天卖出，今天被迫冷冻 `{B.sell}` 更优 → `cold = {S.cold}`'
    return f'cold：`max({B.cold}, {B.sell})`，前一天就是冷冻期 → `cold = {S.cold}`'


CONFIG = dict(
    num=309, title='买卖股票的最佳时机含冷冻期', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='三状态 DP（hold / sell / cold）+ 滚动变量',
    tags=['热题173'],
    code=CODE,
    call=f'Solution().maxProfit({PRICES})',
    expect=7,
    skip=['if len(prices) < 2'],
    views=[
        dict(type='array', var='prices', label='prices', cell=96,
             pointers={'prices.index(price)': 'blue'}, pointer_labels={'prices.index(price)': '今天'}, h=200),
        dict(type='table', var=_table, label='每天三种状态的最佳收益（蓝 = 转移来源，绿 = 正在更新）', cell=96, h=380,
             rows=['hold', 'sell', 'cold'], cols=list(range(len(PRICES))), color=_color),
    ],
    watch=[('price', 'price', 'blue'), ('tmp_hold', 'tmp_hold', 'purple'), ('hold', 'hold'), ('sell', 'sell'), ('cold', 'cold')],
    captions={
        'hold = -prices[0]': '第 0 天：买入 → `hold = -prices[0] = {hold}`',
        'cold = 0': '第 0 天什么都不做：`cold = 0`',
        'sell = None': '第 0 天不可能卖出：`sell = None`',
        'for price in prices[1:]': lambda S, B, r: (f'第 `{PRICES.index(S.price)}` 天，价格 `{S.price}`' if S.price != B.get('price') else '所有天都处理完了'),
        'tmp_hold = hold': lambda S, B, r: (f'三种状态互相交织：先用 `tmp_hold` 存下==前一天==的 hold（`{S.tmp_hold}`）'
                                            if PRICES.index(S.price) == 1 else f'`tmp_hold = {S.tmp_hold}`：记下前一天的 hold'),
        'hold = max(': _hold,
        'if sell is not None': _if,
        'cold = max(': _cold,
        'sell = tmp_hold + price': 'sell：前一天必须持仓 → `sell = tmp_hold + price = {tmp_hold} + {price}` = =={sell}==',
        'return max(': '最后一天要么刚卖出、要么在冷冻期：`max({sell}, {cold})` = =={ret}==',
    },
    cards=dict(
        one_liner='每天三种状态：持仓 hold、当天卖出 sell、冷冻期 cold',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`prices[i]` 是第 i 天的股价，可以多次交易，但必须先卖再买',
                 '卖出后==第二天不能买入==（冷冻期 1 天），求最大利润',
                 '示例：`[1,2,3,0,2]` → `3`（买、卖、冷冻、买、卖）',
                 '本视频：`[1,4,0,5,2,6]` → `7`（不限冷冻期的话是 12）'],
        quote='使用三个数组hold，sell，cold来分别表示持有股票、卖出股票以及冷冻期……==三种状态与前一天的状态都互相交织，因此需要使用临时变量储存前一天的状态==才能更新今天的状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['`hold[i] = max(hold[i-1], cold[i-1] − prices[i])`',
              '`sell[i] = hold[i-1] + prices[i]`（前一天必须持仓）',
              '`cold[i] = max(cold[i-1], sell[i-1])`，答案 `max(sell, cold)`'],
        summary=['时间 `O(n)`，空间 `O(1)`：只依赖前一天 → 滚动变量',
                 '易错：sell 要用==更新前==的 hold，所以先存 `tmp_hold`',
                 '边界：`hold[0] = -prices[0]`，`sell[0] = None`，`cold[0] = 0`',
                 '对比灵神：两状态 + 买入时看「前天不持有」，本质相同',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
