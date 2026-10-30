CONFIG = dict(
    num=4069, title='买卖股票的最佳时机含冷冻期II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP · 枚举买入日',
    code='''
class Solution(object):
    def maxProfit(self, prices, cooldown, costs):
        
        f = [0]
        for index in range(1, len(prices) + 1):
            f.append(f[-1])
            for buy_day in range(index - 1, 0, -1):
                pre_day = buy_day - cooldown - 1
                if pre_day <= 0:
                    pre = 0
                else:
                    pre = f[pre_day]
                
                f[-1] = max(f[-1], pre + prices[index - 1] - prices[buy_day - 1] - costs[index - buy_day])
        
        return f[-1]
''',
    call='Solution().maxProfit([1,5,2,8], 1, [0,1,1,2])',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"买第 {S['buy_day']} 天（价 {S['prices'][S['buy_day']-1]}），卖第 {S['index']} 天（价 {S['prices'][S['index']-1]}），持有 {S['index']-S['buy_day']} 天，费用 {S['costs'][S['index']-S['buy_day']]}" if 'buy_day' in S and 'index' in S and 'costs' in S and 1 <= S['buy_day'] < S['index'] else '')),
        dict(type='array', var='prices', label='prices（第 d 天对应下标 d-1）',
             pointers={'buy_day - 1': 'blue', 'index - 1': 'pink'}, h=200),
        dict(type='array', var='costs', label='costs[k]：持有 k 天的费用', h=170),
        dict(type='array', var='f', label='f[i]：前 i 天、第 i 天不持股的最大收益', pointers={'pre_day': 'cyan'},
             color=lambda S, i, v: 'green' if i == len(S['f']) - 1 else None, h=200),
    ],
    watch=['index', 'buy_day', 'pre_day', 'pre', ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f = [0]': '`f[0] = 0`：还没有任何一天，收益为 0',
        'f.append(f[-1])': '先继承前一天：`f[{index}] = f[{index-1}] = {f[-1]}`（第 {index} 天什么都不做）',
        'for buy_day in': '第 {index} 天卖出，从 `index-1` 往前枚举买入日 `buy_day`',
        'pre_day = ': '买入日是 `buy_day={buy_day}`，卖出冷却 `{cooldown}` 天 → 上次清仓最晚在 `pre_day = {pre_day}`',
        'if pre_day <= 0': lambda S, B, r: (f'`pre_day = {S.pre_day} <= 0`：买入前没有可做的交易 → 前置收益 0' if S.pre_day <= 0
                                            else f'`pre_day = {S.pre_day} > 0`：之前可以交易，取 `f[{S.pre_day}]`'),
        'pre = 0': '没有之前的交易，`pre = 0`',
        'pre = f[pre_day]': '`pre = f[{pre_day}] = {pre}`：冷却结束前能拿到的最大收益',
        'f[-1] = max': '最后一笔：`{pre} + {prices[index-1]} − {prices[buy_day-1]} − {costs[index-buy_day]}` = {pre + prices[index-1] - prices[buy_day-1] - costs[index-buy_day]}；`f[{index}] = max({B.f[-1]}, 它)` = =={f[-1]}==',
        'return f[-1]': '最后一天不持股的最大收益 `{f[-1]}`，就是答案',
    },
    cards=dict(
        one_liner='f[i] 记前 i 天不持股的最大收益，枚举最后一笔买入日',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['给 `prices`、冷却天数 `cooldown`、持有费 `costs`；持有 `k` 天要付 `costs[k]`',
                 '第 `d` 天卖出后，最早第 `d + cooldown + 1` 天才能再买',
                 '利润 = 卖价 − 买价 − `costs[持有天数]`，求最大总利润，没有赚头就返回 0',
                 '本视频：`[1,5,2,8]`，`cooldown=1`，`costs=[0,1,1,2]`'],
        quote='可以考虑使用f[index]表示在第index天没有持有股票时可能得到的最大收益',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]` 先继承 `f[index-1]`：这一天什么也不做',
              '或者在 `index` 卖出：往前枚举买入日 `buy_day`',
              '买入前最晚清仓日 `pre_day = buy_day - cooldown - 1`，`pre_day <= 0` 就记 0，否则 `f[pre_day]`'],
        summary=['时间 `O(n²)`（n ≤ 1500 可过），空间 `O(n)`',
                 '易错点：下标错位，第 d 天的价格是 `prices[d-1]`，`f` 比 `prices` 多一格',
                 '`pre_day <= 0` 表示之前无法交易，要取 0，不能去读 `f[负数]`',
                 '原文为 Python 2 风格（`class Solution(object)`），代码本身无需修改'],
    ),
)
