def _idx(S):
    return S['prices'].index(S['price']) if 'price' in S and S.get('price') in S['prices'] else -1


def _txt(S):
    if 'res' not in S:
        return '`hold` = 第 i 天持仓的最大收益；`res` = 第 i 天未持仓的最大收益'
    return f"持仓 `hold` = =={S['hold']}==　　未持仓 `res` = =={S['res']}=="


CONFIG = dict(
    num=714, title='买卖股票的最佳时机含手续费', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='持仓 / 未持仓两个状态',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def maxProfit(self, prices, fee):

        hold = -prices[0]
        res = 0
        for price in prices[1:]:
            tmp = hold
            hold = max(hold, res - price)
            res = max(res, tmp + price - fee)
        
        return res
''',
    call='Solution().maxProfit([1, 3, 2, 8, 4, 9], 2)',
    expect=8,
    skip=['tmp = hold'],
    views=[
        dict(type='array', var='prices', label='prices（蓝 = 今天的价格）', h=200, cell=90,
             color=lambda S, i, v: 'blue' if i == _idx(S) else ('green' if i == 0 and 'price' not in S else None),
             dim=lambda S, i, v: _idx(S) >= 0 and i < _idx(S)),
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='text', fn=lambda S: (f"今天 `price = {S['price']}`：买入要 `res - price`，卖出要 `hold + price - fee`" if 'price' in S else '边界：`hold = -prices[0]`（第 0 天买入），`res = 0`'), size=24, h=60),
    ],
    watch=[('hold', 'hold', 'pink'), ('res', 'res', 'green'), 'price', 'fee'],
    captions={
        'hold = -prices[0]': '边界 `f[0] = -prices[0]`：第 0 天就买入，持仓收益是 ==`{hold}`==',
        'res = 0': '边界 `g[0] = 0`：第 0 天不持仓，收益 ==0==',
        'for price in prices': lambda S, B, r: ('所有天都处理完了' if B.get('price') == S.get('price') and 'price' in B else f"看下一天的价格 `price = {S['price']}`"),
        'hold = max': '持仓：继续拿着 `{B.hold}`，或不持仓时今天买入 `{B.res} - {price}` → ==hold = {hold}==',
        'res = max': '未持仓：保持 `{B.res}`，或昨天持仓今天卖出 `{tmp} + {price} - {fee}` → ==res = {res}==（手续费在卖出时扣）',
        'return res': '最后一定不持仓，答案取 `res` = =={ret}==',
    },
    cards=dict(
        one_liner='f 记持仓，g 记未持仓，用两个变量滚动',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`prices[i]` 是第 `i` 天的股价，每笔交易（买入到卖出）要付一次手续费 `fee`',
                 '可以交易多次，但卖出之前不能再买入',
                 '示例：`prices = [1,3,2,8,4,9], fee = 2` → `8`'],
        quote='令f[i]表示在第i天时持仓最大的收益，g[i]则表示第i天未持仓最大的收益。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i] = max(f[i-1], g[i-1] - prices[i])`：继续拿着，或今天买进',
              '`g[i] = max(g[i-1], f[i-1] + prices[i] - fee)`：继续空仓，或今天卖出并付手续费',
              '只依赖前一天，所以用 `hold`、`res` 两个变量滚动；用 `tmp` 保存旧的 `hold`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：更新 `res` 要用更新前的 `hold`，所以先存到 `tmp`',
                 '手续费只在卖出时扣一次；答案取不持仓的 `res`',
                 '同类：122 买卖股票 II、309 含冷冻期'],
    ),
)
