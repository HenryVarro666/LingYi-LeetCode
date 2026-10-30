TX = [[2, 1], [5, 0], [4, 2], [3, 3]]


def _tx_color(S, i, j, v):
    if 'cost' not in S:
        return None
    t = S['transactions'][i]
    if t == [S['cost'], S['cashback']]:
        return 'blue'
    return 'pink' if t[0] > t[1] else 'green'


def _tx_txt(S):
    if 'cost' not in S:
        return '粉 = 亏钱（cost > cashback），绿 = 赚钱（cost ≤ cashback）'
    c, b = S['cost'], S['cashback']
    return f"当前 `({c}, {b})`：累计亏损 `total_lose = {S['total_lose']}`，最大 `min(cost, cashback) = {S['mx']}`"


CONFIG = dict(
    num=2412, title='完成所有交易的初始最少钱数', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='最坏顺序 · 一次遍历',
    tags=['灵神题单', '难度分 2092'],
    code='''
class Solution:
    def minimumMoney(self, transactions: List[List[int]]) -> int:
        total_lose = mx = 0
        for cost, cashback in transactions:
            total_lose += max(cost - cashback, 0)
            mx = max(mx, min(cost, cashback))
        return total_lose + mx
''',
    call=f'Solution().minimumMoney({TX})',
    expect=11,
    views=[
        dict(type='grid', var='transactions', label='transactions（每行 [cost, cashback]）', color=_tx_color,
             cols=['cost', 'cashback'], cell=110, h=330),
        dict(type='text', fn=_tx_txt, size=28, h=90),
    ],
    watch=['cost', 'cashback', ('total_lose', 'total_lose', 'pink'), ('mx', 'mx', 'orange')],
    captions={
        'total_lose = mx = 0': '`total_lose` 记所有亏钱交易的总亏损，`mx` 记 `min(cost, cashback)` 的最大值',
        'total_lose +=': '亏损 `max({cost} − {cashback}, 0)` = `{max(cost - cashback, 0)}`：赚钱的交易不亏，==只有亏钱交易累加==。`total_lose` = =={total_lose}==',
        'mx = max': '最坏情况下要么==卡在第一笔赚钱交易==（要 cost），要么==卡在最后一笔亏钱交易==（要 cashback），两者取小：`min({cost}, {cashback})` = `{min(cost, cashback)}`，`mx` 取最大 → =={mx}==',
        'return': '最坏情况需要 `total_lose + mx` = `{total_lose} + {mx}` = =={total_lose + mx}==',
    },
    cards=dict(
        one_liner='先亏后赚是最坏顺序：总亏损 + 最难的那一笔门槛',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每笔交易 `[cost, cashback]`：钱 `>= cost` 才能做，做完钱 `-cost+cashback`',
                 '求在==任意顺序==下都能做完的最少初始钱数',
                 '示例：`[[2,1],[5,0],[4,2]]` → `10`；本视频多加了 `[3,3]`'],
        quote='什么时候最穷？完成所有亏钱交易后最穷。……初始钱数 initMoney 等于 totalLose 加上 min(cost, cashback) 的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最坏情况：先把亏钱交易全做完，人最穷',
              '第一笔赚钱交易要 `totalLose + cost`；最后一笔亏钱交易要 `totalLose + cashback`',
              '赚钱时 `total_lose` 加的是 cost 的较小者，亏钱时是 cashback，统一成 `min(cost, cashback)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：亏损只算 `max(cost - cashback, 0)`，赚钱交易不能抵消亏损',
                 '`mx` 初始为 0 即可，全是亏钱/赚钱的情况也成立',
                 '思考题：改成「至少一种顺序」要按 cashback/cost 排序，属于交换论证'],
    ),
)
