P0 = [1, 7, 6, 2]
K0 = 2


def _idx(S):
    return S['prices'].index(S['p']) if 'p' in S and S.get('p') in S['prices'] else -1


def _fmt(v):
    return '-' if v is None else str(v)


def _txt(S):
    if 'long_hold' not in S:
        return '三个数组，下标 = 已完成的交易笔数：`unhold` 空仓、`long_hold` 持多单、`short_hold` 持空单（`-` = 还不可能）'
    return None


def _cell(S, r, c, v):
    ix = S.get('index')
    if ix is None or S.get('_line') not in (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22):
        return None
    if c == ix:
        return 'yellow'
    if c == ix - 1:
        return 'blue'
    return None


CONFIG = dict(
    num=3573, title='买卖股票的最佳时机 V', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='空仓 / 多单 / 空单三个状态',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1777'],
    code='''
class Solution(object):
    def maximumProfit(self, prices, k):
        
        long_hold = [None] * (k + 1)
        short_hold = [None] * (k + 1)
        unhold = [None] * (k + 1)
        unhold[0] = 0

        for p in prices:
            for index in range(k, 0, -1):
                if index < k and unhold[index] is not None:
                    if long_hold[index] is None or long_hold[index] < unhold[index] - p:
                        long_hold[index] = unhold[index] - p
                    if short_hold[index] is None or short_hold[index] < unhold[index] + p:
                        short_hold[index] = unhold[index] + p
                
                if short_hold[index - 1] is not None:
                    if unhold[index] is None or unhold[index] < short_hold[index - 1] - p:
                        unhold[index] = short_hold[index - 1] - p
                
                if long_hold[index - 1] is not None:
                    if unhold[index] is None or unhold[index] < long_hold[index - 1] + p:
                        unhold[index] = long_hold[index - 1] + p

            if long_hold[0] is None or long_hold[0] < -p:
                long_hold[0] = -p
            if short_hold[0] is None or short_hold[0] < p:
                short_hold[0] = p

        return max(unhold)
''',
    call=f'Solution().maximumProfit({P0}, {K0})',
    expect=10,
    skip=['if '],
    max_steps=90,
    views=[
        dict(type='array', var='prices', label='prices（蓝 = 今天）', h=160, cell=80,
             color=lambda S, i, v: 'blue' if i == _idx(S) else None,
             dim=lambda S, i, v: _idx(S) >= 0 and i < _idx(S)),
        dict(type='array', var='unhold', label='unhold[j]：完成 j 笔，空仓', h=150, cell=80, pointers={'index': 'yellow'}),
        dict(type='array', var='long_hold', label='long_hold[j]：完成 j 笔，持多单', h=150, cell=80, pointers={'index': 'yellow'}),
        dict(type='array', var='short_hold', label='short_hold[j]：完成 j 笔，持空单', h=150, cell=80, pointers={'index': 'yellow'}),
    ],
    watch=[('index', 'index', 'yellow'), 'p', ('unhold', 'unhold', 'green')],
    captions={
        'long_hold = [None]': '`long_hold[j]`：已完成 `j` 笔交易，目前持多单的最大收益；`None` = 不可能',
        'short_hold = [None]': '`short_hold[j]`：已完成 `j` 笔交易，目前持空单的最大收益',
        'unhold = [None]': '`unhold[j]`：已完成 `j` 笔交易，目前空仓的最大收益',
        'unhold[0] = 0': '一笔都没做、手里没东西：收益 ==0==',
        'for p in prices': lambda S, B, r: ('所有天都处理完了' if 'p' in B and B['p'] == S['p'] else f"第 `{S['prices'].index(S['p'])}` 天，价格 `p = {S['p']}`；`index` 从大到小，先更新旧的、不被今天覆盖"),
        'for index in range': lambda S, B, r: ('今天所有交易笔数都更新完了，接着更新第 0 笔的开仓' if B.get('index') == S.get('index') else f"`index = {S['index']}`"),
        'long_hold[index] = unhold[index] - p': '空仓时今天买入：`long_hold[{index}] = {unhold[index]} - {p}` = =={long_hold[index]}==（开多单）',
        'short_hold[index] = unhold[index] + p': '空仓时今天卖出：`short_hold[{index}] = {unhold[index]} + {p}` = =={short_hold[index]}==（开空单）',
        'unhold[index] = short_hold[index - 1] - p': '昨天持空单、今天买回：`unhold[{index}] = {short_hold[index-1]} - {p}` = =={unhold[index]}==（做完第 {index} 笔）',
        'unhold[index] = long_hold[index - 1] + p': '昨天持多单、今天卖出：`unhold[{index}] = {long_hold[index-1]} + {p}` = =={unhold[index]}==（做完第 {index} 笔）',
        'long_hold[0] = -p': '第 0 笔的多单：`long_hold[0] = -{p}`，保持更大者',
        'short_hold[0] = p': '第 0 笔的空单：`short_hold[0] = {p}`，保持更大者',
        'return max(unhold)': '答案取所有交易笔数中空仓收益的最大值：`max(unhold)` = =={ret}==',
    },
    cards=dict(
        one_liner='三个状态：空仓、持多单、持空单，下标记交易笔数',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['`prices[i]` 是第 `i` 天股价，最多做 `k` 笔交易',
                 '普通交易：先买后卖；做空交易：先卖后买回',
                 '一笔交易没结束不能开下一笔，同一天不能买卖两次',
                 '示例：`prices=[1,7,6,2], k=2` → `10`'],
        quote='注意到题中有不持仓、持有多单、持有空单这三种状态，于是可以令long_hold[i][j]表示前i天完成j笔交易，目前持有多单股票时的最大收益。',
        quote_src='—— yiduobo 题解',
        idea=['`long_hold` 从 `unhold` 买入转移，`short_hold` 从 `unhold` 卖出转移',
              '`unhold[j]` 由 `long_hold[j-1]` 卖出、或 `short_hold[j-1]` 买回得到，说明第 `j` 笔交易完成',
              '转移只依赖前一天，所以 `index`（交易笔数）从大到小更新，省去天数一维',
              '代码用 `None` 表示「状态还不可能」，每次转移前都判断；动画只演示条件成立、真正更新的那些步'],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '易错：`index` 倒序；先更新 `long/short_hold`，再更新 `unhold`',
                 '易错：每天末尾还要更新 `long_hold[0]`、`short_hold[0]`（第 0 笔的开仓）',
                 '原文最后的 `max(unhold)` 在 Python 3 里要求没有 `None` 才不会报错，示例已保证',
                 '同类：188 买卖股票 IV'],
    ),
)
