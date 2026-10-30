CONFIG = dict(
    num=3155, title='可升级服务器的最大数量', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='逐个数据中心 · 先全卖再赎回',
    code='''
class Solution(object):
    def maxUpgrades(self, count, upgrade, sell, money):

        res = []

        for c, u, s, m in zip(count, upgrade, sell, money):
            if m >= u * c:
                res.append(c)
            else:
                res.append((m + c * s) // (u + s))
        
        return res
''',
    call='Solution().maxUpgrades([4, 3, 2], [3, 5, 1], [4, 2, 5], [8, 9, 10])',
    expect=[3, 2, 2],
    views=[
        dict(type='array', var='count', label='count（服务器数量）', cell=80, h=105),
        dict(type='array', var='upgrade', label='upgrade（升级单价）', cell=80, h=105),
        dict(type='array', var='sell', label='sell（出售单价）', cell=80, h=105),
        dict(type='array', var='money', label='money（初始资金）', cell=80, h=105),
        dict(type='array', var='res', label='res（答案）', cell=80, h=105,
             color=lambda S, i, v: 'green'),
    ],
    watch=[('c', 'c'), ('u', 'u'), ('s', 's'), ('m', 'm'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 存每个数据中心的答案；资金不能跨数据中心混用，所以==逐个数据中心单独算==',
        'for c, u, s, m': lambda S, B, ret: ('遍历结束，所有数据中心都算过了' if len(S.res) == len(S.count) else f'这个数据中心：`c = {S.c}` 台，升级 `u = {S.u}`，卖出 `s = {S.s}`，资金 `m = {S.m}`'),
        'if m >= u * c': lambda S, B, ret: (f'`{S.m} ≥ {S.u} × {S.c} = {S.u * S.c}`：钱够，全部升级' if S.m >= S.u * S.c
                                            else f'`{S.m} < {S.u} × {S.c} = {S.u * S.c}`：钱不够，只能卖掉一部分再升级'),
        'res.append(c)': '全部 `{c}` 台都能升级 → `res = {res}`',
        'res.append((m': '设最后升级 `x` 台：`x×u ≤ (c−x)×s + m`，解得 `x ≤ (m + c×s) // (u + s)` = `({m} + {c}×{s}) // ({u} + {s})` = =={res[-1]}==',
        'return res': '全部数据中心算完，返回 `{ret}`',
    },
    cards=dict(
        one_liner='先把服务器全卖掉，再按“卖价 + 升级价”一台台赎回来',
        complexity='时间 `O(n)`，空间 `O(1)`（不含返回值）',
        problem=['有 `n` 个数据中心：`count` 台服务器、升级单价 `upgrade`、出售单价 `sell`、初始资金 `money`',
                 '可以卖掉部分服务器换钱，去升级剩下的；资金不能在数据中心之间混用',
                 '求每个数据中心最多能升级几台；官方示例 `[4,3] [3,5] [4,2] [8,9]` → `[3,2]`；本视频多加一个钱够的数据中心'],
        quote='x * (upgrade[i] + sell[i]) <= count[i] * sell[i] + money[i]……另一种理解为先把所有服务器都卖了，换来count[i] * sell[i]的资金，接下来可以认为赎回来一台服务器并升级的价格为upgrade[i] + sell[i]。',
        quote_src='—— yiduobo 题解原文',
        idea=['钱够（`m >= u * c`）：全部升级，答案就是 `c`',
              '钱不够：留 `x` 台升级、卖掉 `c−x` 台，要求 `x×u ≤ (c−x)×s + m`',
              '移项得 `x ≤ (m + c×s) // (u + s)`，向下取整即最大值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '题面库中没有，题意按 yiduobo 原文及官方示例整理',
                 '易错：钱够时不能套公式（公式可能超过 `c`），要先判断 `m >= u * c`',
                 '易错：用整除 `//` 向下取整，因为服务器只能整台',
                 '原文已是 Python 3 可运行写法（本来就用 `//`），无需修改'],
    ),
)
