def _idx(S):
    return S['prices'].index(S['p']) if 'p' in S and S.get('p') in S['prices'] else -1


def _f(v):
    return '-∞' if v == float('-inf') else str(v)


def _txt(S):
    if 'f0' not in S:
        return '`f0` = 不持有股票的最大利润；`f1` = 持有股票的最大利润'
    return f"`f0` = =={_f(S['f0'])}==（手里没股票）　`f1` = =={_f(S['f1'])}==（手里有股票）"


CONFIG = dict(
    num=714, title='买卖股票的最佳时机含手续费', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP（空间优化）',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        f0, f1 = 0, -inf
        for p in prices:
            f0, f1 = max(f0, f1 + p - fee), max(f1, f0 - p)
        return f0
''',
    call='Solution().maxProfit([1, 3, 2, 8, 4, 9], 2)',
    expect=8,
    views=[
        dict(type='array', var='prices', label='prices（蓝 = 今天的价格 p）', h=200, cell=90,
             color=lambda S, i, v: 'blue' if i == _idx(S) else None,
             dim=lambda S, i, v: _idx(S) >= 0 and i < _idx(S)),
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='text', fn=lambda S: (f"今天价格 `p = {S['p']}`，手续费 `fee = {S['fee']}`" if 'p' in S else '手续费在卖出时扣一次'), size=26, h=60),
    ],
    watch=[('f0', 'f0', 'green'), ('f1', 'f1', 'pink'), 'p', 'fee'],
    captions={
        'f0, f1 = 0, -inf': '初始：还没买卖，==不持有 = 0==；==持有 = -∞==（不可能，还没买过）',
        'for p in prices': lambda S, B, r: ('所有天都看完了，退出循环' if B.get('p') == S.get('p') and 'p' in B else f"看第 `{S['prices'].index(S['p'])}` 天的价格 `p = {S['p']}`"),
        'f0, f1 =': '同时更新（右边都用旧值）：`f0 = max({B.f0}, {B.f1}+{p}-{fee})` = =={f0}==，`f1 = max({B.f1}, {B.f0}-{p})` = =={f1}==',
        'return f0': '最后手上不能有股票，答案是 `f0` = =={ret}==',
    },
    cards=dict(
        one_liner='每天只有两种状态：手里有股票，或者没有',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`prices[i]` 是第 `i` 天股票价格，`fee` 是每笔交易的手续费',
                 '可以买卖任意多次，但手里最多一只股票，每笔交易付一次手续费',
                 '示例：`prices = [1,3,2,8,4,9], fee = 2` → `8`'],
        quote='为什么在买入/卖出减去都可以呢？因为最终手上一定是没有股票的，那么==有买入就必定有卖出==，在买入/卖出其一减去手续费就行。',
        quote_src='—— 灵茶山艾府题解',
        idea=['思路同 122 题（买卖股票 II），只是卖出时多扣一份 `fee`',
              '`f0` 不持有：继续不持有，或今天卖出 `f1 + p - fee`',
              '`f1` 持有：继续持有，或今天买入 `f0 - p`；用元组赋值保证两个都用旧值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`f1` 初值是 `-inf`，答案可能出现负中间值，别用 -1 当哨兵',
                 '题解先讲记忆化搜索，再 1:1 翻译成递推，最后滚动成两个变量；这里演示最后一种',
                 '同类：122 买卖股票 II、309 含冷冻期'],
    ),
)
