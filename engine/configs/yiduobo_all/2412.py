TX = [[2, 1], [5, 0], [4, 2], [3, 3]]


def _tx_color(S, i, j, v):
    if 'cost' not in S:
        return None
    t = S['transactions'][i]
    if t == [S['cost'], S['callback']]:
        return 'blue'
    return 'pink' if t[0] > t[1] else 'green'


CONFIG = dict(
    num=2412, title='完成所有交易的初始最少钱数', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='分类讨论 · 赔钱 / 赚钱两种卡点',
    tags=['灵神题单', '贪心与思维', '难度分 2092'],
    code='''
class Solution(object):
    def minimumMoney(self, transactions):

        neg_sum = 0
        max_pos = 0
        max_callback = 0
        for cost, callback in transactions:
            if cost > callback:
                neg_sum += cost - callback
                max_callback = max(max_callback, callback)
            else:
                max_pos = max(max_pos, cost)
        
        return neg_sum + max(max_callback, max_pos)
''',
    call=f'Solution().minimumMoney({TX})',
    expect=11,
    views=[
        dict(type='grid', var='transactions', label='transactions（粉 = 赔钱，绿 = 赚钱，蓝 = 当前）', color=_tx_color,
             cols=['cost', 'callback'], cell=110, h=330),
        dict(type='text', h=90, size=28,
             fn=lambda S: f"`neg_sum = {S['neg_sum']}`，`max_callback = {S['max_callback']}`，`max_pos = {S['max_pos']}`" if 'neg_sum' in S else ''),
    ],
    watch=['cost', 'callback', ('neg_sum', 'neg_sum', 'pink'), ('max_callback', 'max_callback', 'orange'), ('max_pos', 'max_pos', 'green')],
    captions={
        'neg_sum = 0': '`neg_sum`：所有赔钱买卖一共赔掉的钱',
        'max_pos = 0': '`max_pos`：赚钱买卖里最大的 cost',
        'max_callback = 0': '`max_callback`：赔钱买卖里最大的 callback',
        'if cost > callback': lambda S, B, r: f'`{S.cost} > {S.callback}` → ' + ('==赔钱买卖==' if S.cost > S.callback else '==赚钱买卖=='),
        'neg_sum +=': '赔掉 `{cost} − {callback}`，`neg_sum` = =={neg_sum}==',
        'max_callback = max': '它放最后做最糟：要 `neg_sum + callback`。`max_callback` = =={max_callback}==',
        'max_pos = max': '赔钱做完后紧接着做它要 `neg_sum + cost`。`max_pos` = =={max_pos}==',
        'return': '答案 `neg_sum + max(max_callback, max_pos)` = `{neg_sum} + max({max_callback}, {max_pos})` = =={neg_sum + max(max_callback, max_pos)}==',
    },
    cards=dict(
        one_liner='赔钱的全做完，再看会被哪一笔卡住',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每笔交易 `[cost, cashback]`：钱 `>= cost` 才能做，做完钱 `-cost+cashback`',
                 '求在==任意顺序==下都能做完的最少初始钱数',
                 '示例：`[[2,1],[5,0],[4,2]]` → `10`；本视频多加了 `[3,3]`'],
        quote='对于某个赔钱买卖(cost, callback)，在进行这个买卖之前赔掉的钱就是neg_sum - (cost - callback)，因此能进行这个买卖的最少初始钱数就是neg_sum + callback。',
        quote_src='—— yiduobo 题解原文',
        idea=['最坏情况是先干完所有赔钱买卖',
              '卡点一：紧接着干赚钱买卖里 cost 最大的 → `neg_sum + max_pos`',
              '卡点二：卡在最后一个赔钱买卖 → 取 callback 最大者 → `neg_sum + max_callback`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：可能没有赚钱买卖（样例一），`max_pos` 取 0 即可',
                 '最后一个赔钱买卖不能选 cost 最大的，要选 callback 最大的',
                 '对比灵神：灵神用 `min(cost, cashback)` 把两类合并，yiduobo 分开讨论'],
    ),
)
