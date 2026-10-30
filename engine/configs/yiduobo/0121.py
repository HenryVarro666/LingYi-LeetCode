def _buy_idx(S):
    k = S['index']
    seg = S['prices'][:k]
    return seg.index(min(seg))


def _color(S, i, v):
    if 'index' not in S:
        return 'green' if ('buy' in S and i == 0) else None
    if i == S['index']:
        return 'blue'
    if i == _buy_idx(S):
        return 'green'
    return None


def _dim(S, i, v):
    return 'index' in S and i > S['index']


def _formula(S):
    if 'index' not in S:
        return '第 `k` 天卖出的最大收益 = `prices[k] − min(prices[0], …, prices[k−1])`'
    k, P = S['index'], S['prices']
    m = min(P[:k])
    return f'第 `{k}` 天卖出：`prices[{k}] − min(prices[0..{k - 1}])` = `{P[k]} − {m}` = =={P[k] - m}=='


CONFIG = dict(
    num=121, title='买卖股票的最佳时机', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='一趟扫描维护前缀最小值',
    code='''
class Solution(object):
    def maxProfit(self, prices):
        if not prices:
            return 0

        ans = 0
        buy = prices[0]
        for index in range(1, len(prices)):
            ans = max(prices[index] - buy, ans)
            buy = min(buy, prices[index])

        return ans
''',
    call='Solution().maxProfit([3, 8, 2, 5, 9, 1])',
    expect=7,
    views=[
        dict(type='text', h=56, size=27, fn=_formula),
        dict(type='bars', var='prices', h=520, cell=130, color=_color, dim=_dim,
             pointers={'index': 'blue'}, pointer_labels={'index': 'k'}),
    ],
    watch=[('index', 'index', 'blue'), ('buy', 'buy', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'if not prices': '空数组没法交易，直接返回 0；这里不是空的',
        'ans = 0': '`ans = 0`：赚不到钱就是 0',
        'buy = prices[0]': '`buy` 就是公式里的 `min(prices[0..k-1])`，从 `prices[0] = {buy}` 开始',
        'for index in range': lambda S, B, ret: ('扫描结束' if B.get('index') == S['index']
                                                 else f'假设在第 `k = {S["index"]}` 天卖出（第 0 天之前没得买，所以从 1 开始）' if S['index'] == 1
                                                 else f'假设在第 `k = {S["index"]}` 天卖出'),
        'ans = max(prices[index] - buy, ans)': lambda S, B, ret: (
            f'==先==用 `prices[{S["index"]}] - buy = {S["prices"][S["index"]]} - {S["buy"]} = {S["prices"][S["index"]] - S["buy"]}` 更新答案：`ans = {S["ans"]}`'
            + ('　==变大了==' if S['ans'] > B['ans'] else '')),
        'buy = min(buy, prices[index])': lambda S, B, ret: (
            f'==再==用 `prices[{S["index"]}] = {S["prices"][S["index"]]}` 更新 min：`buy = {S["buy"]}`，'
            + ('留给后面的日子用' if S['index'] < len(S['prices']) - 1 else '可惜后面已经没有卖出日了')
            if S['buy'] < B['buy'] else f'==再==更新 min：`min({B["buy"]}, {S["prices"][S["index"]]}) = {S["buy"]}`，不变'),
        'return ans': '返回 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='第 k 天卖出的最佳收益 = 当天价格 − 之前的最低价',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`prices[i]` 是股票第 `i` 天的价格，只能==买一次、卖一次==，且先买后卖',
                 '求最大利润；赚不到钱就返回 `0`',
                 '例：`[3,8,2,5,9,1]` → `7`（价格 2 买入，价格 9 卖出）'],
        quote='假设我们在第k天卖出股票，那么我们所能得到的最大收益为 prices[k] - min(prices[0], ..., prices[k - 1])',
        quote_src='—— yiduobo 题解',
        idea=['从左往右一趟扫描，维护住后面这个 `min`（代码里叫 `buy`）',
              '每次==先==用 `prices[k] - min` 更新答案，==再==用 `prices[k]` 更新 `min`',
              '所有 `k` 里取最大，就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '顺序：先算收益再更新 `buy`，`buy` 才是“第 k 天之前”的最小值',
                 '本例 `buy` 从 3 变成 2 后才出现 `9 − 2 = 7`；最后的 1 已经没有卖出日可用',
                 '只删去了 `"""type ..."""` 文档字符串，其余照搬（兼容 Python 3）'],
    ),
)
