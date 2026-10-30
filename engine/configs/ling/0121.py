def _idx(S, name):
    return S['prices'].index(S[name]) if name in S else None


def _color(S, i, v):
    if 'p' in S and i == _idx(S, 'p'):
        return 'blue'
    if 'min_price' in S and i == _idx(S, 'min_price'):
        return 'green'
    return None


def _dim(S, i, v):
    return 'p' in S and i > _idx(S, 'p')


def _cap_ans(S, B, ret):
    p, mn = S['p'], S['min_price']
    head = f'今天卖出：`{p} - {mn} = {p - mn}`，`ans = max({B["ans"]}, {p - mn}) = {S["ans"]}`'
    if _idx(S, 'p') == 0:
        return head + '（第 0 天当天买卖，利润 0）'
    return head + ('　==更新答案==' if S['ans'] > B['ans'] else '')


def _cap_min(S, B, ret):
    if S['min_price'] < B['min_price']:
        return f'`{S["p"]}` 比之前都便宜 → `min_price = {S["min_price"]}`：==以后卖出时，最好在这天买=='
    if _idx(S, 'p') == 0:
        return f'`min_price = min({B["min_price"]}, {S["p"]}) = {S["min_price"]}`。==先算 ans 再更新 min==，保证买入在卖出之前'
    return f'`min_price = min({B["min_price"]}, {S["p"]})`，仍是 `{S["min_price"]}`'


CONFIG = dict(
    num=121, title='买卖股票的最佳时机', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='枚举卖出价格，维护买入最小值',
    code='''
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        ans = 0
        min_price = prices[0]
        for p in prices:
            ans = max(ans, p - min_price)
            min_price = min(min_price, p)
        return ans
''',
    call='Solution().maxProfit([7, 1, 5, 3, 6, 4])',
    expect=5,
    views=[
        dict(type='text', h=56, size=27, text='==蓝== = 今天卖出价 `p`，==绿== = 之前的最低价 `min_price`；灰色是还没看到的未来'),
        dict(type='bars', var='prices', h=520, cell=130, color=_color, dim=_dim,
             pointers={'prices.index(min_price)': 'green', 'prices.index(p)': 'blue'},
             pointer_labels={'prices.index(min_price)': '买', 'prices.index(p)': '卖'},
             window=('prices.index(min_price)', 'prices.index(p)')),
    ],
    watch=[('p', 'p', 'blue'), ('min_price', 'min_price', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'ans = 0': '`ans = 0`：不交易时利润为 0（题目允许返回 0）',
        'min_price = prices[0]': '`min_price` 记录==卖出日之前==的最低价，先设为 `prices[0] = {min_price}`',
        'for p in prices': lambda S, B, ret: ('遍历结束' if B.get('p') == S['p']
                                              else (f'枚举==卖出==价格 `p = {S["p"]}`（第 0 天）：哪天买最好？==之前最便宜的那天==' if _idx(S, 'p') == 0
                                                    else f'枚举卖出价格 `p = {S["p"]}`（第 {_idx(S, "p")} 天）')),
        'ans = max(ans, p - min_price)': _cap_ans,
        'min_price = min(min_price, p)': _cap_min,
        'return ans': '返回最大利润 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='枚举哪天卖出，买入一定选在它之前的最低价',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`prices[i]` 是股票第 `i` 天的价格，只能==买一次、卖一次==，且先买后卖',
                 '求最大利润；赚不到钱就返回 `0`',
                 '示例：`[7,1,5,3,6,4]` → `5`（价格 1 买入，价格 6 卖出）'],
        quote='从左到右枚举卖出价格 prices[i]。要想获得最大利润，哪天买入最好？在股票价格最低的那天买入。',
        quote_src='—— 灵茶山艾府题解',
        idea=['买入日必须在卖出日之前 → 要的是 `prices[0..i-1]` 的最小值',
              '用一个变量 `min_price` 边走边维护，==枚举右，维护左==',
              '只能买卖一次 → 答案是所有 `p - min_price` 的最大值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '==先更新 ans，再更新 min_price==：保证 `min_price` 来自 `p` 之前',
                 '本题允许不交易，交换两行顺序也对（同一天买卖利润 0）；若必须交易一次就不能换',
                 '“枚举右，维护左”是通用技巧；股票系列见 122/123/188/309/714'],
    ),
)
