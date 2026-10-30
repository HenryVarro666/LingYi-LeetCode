CONFIG = dict(
    num=2706, title='购买两块巧克力', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='维护最小与次小值', tags=[],
    code='''
class Solution:
    def buyChoco(self, prices: List[int], money: int) -> int:
        mn1 = mn2 = inf
        for p in prices:
            if p < mn1:
                mn2 = mn1
                mn1 = p
            elif p < mn2:
                mn2 = p
        return money if mn1 + mn2 > money else money - mn1 - mn2
''',
    call='Solution().buyChoco([3,1,4,5,2,6], 4)',
    expect=1,
    views=[
        dict(type='array', var='prices', h=200,
             color=lambda S, i, v: 'green' if 'mn1' in S and v == S['mn1'] else 'yellow' if 'mn2' in S and v == S['mn2'] else 'blue' if S.get('p') == v else None),
        dict(type='text', h=90, fn=lambda S: f"最小 `mn1 = {S['mn1']}`，次小 `mn2 = {S['mn2']}`，两块合计 =={S['mn1'] + S['mn2'] if S['mn2'] != float('inf') else '?'}== / money = {S['money']}" if 'mn1' in S else ''),
    ],
    watch=[('p', 'p', 'blue'), ('mn1', 'mn1', 'green'), ('mn2', 'mn2', 'yellow'), 'money'],
    captions={
        'if p < mn1': '`{p}` 比最小值 `{mn1 if False else B.mn1}` 还小吗？{"是，成为新的最小" if p < B.mn1 else "否，再看能不能当次小"}',
        'mn2 = mn1': '老的最小值退位成次小：`mn2 = {mn2}`',
        'mn1 = p': '新的最小值：`mn1 = {mn1}`',
        'elif p < mn2': '`{p}` 比次小值 `{B.mn2}` 小吗？{"是" if p < B.mn2 else "否，丢掉"}',
        'mn2 = p': '`{p}` 介于两者之间，成为新的次小值：`mn2 = {mn2}`',
        'return': '最便宜两块合计 `{mn1} + {mn2} = {mn1 + mn2}`，{"超过 money，买不起，原样返回 money" if mn1 + mn2 > money else "买得起，剩下 money - 合计"} → =={ret}==',
    },
    cards=dict(
        one_liner='只要最便宜的两块：边扫边维护最小和次小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['买恰好两块巧克力，剩余的钱不能为负，想剩得最多',
                 '买不起任何两块就返回原来的 `money`',
                 '示例：`prices=[1,2,2], money=3` → `0`'],
        quote='遍历 prices，维护最小值 mn1 和次小值 mn2。如果 mn1+mn2>money，那么剩余的钱会变成负数，返回 money，否则返回 money-mn1-mn2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['花得最少 = 买最便宜的两块，不用排序',
              '新数比 `mn1` 小：老最小退位给 `mn2`',
              '否则比 `mn2` 小：只更新 `mn2`'],
        summary=['时间 `O(n)`，只扫一遍，空间 `O(1)`',
                 '==先退位 `mn2 = mn1`，再写 `mn1 = p`==，顺序反了会丢数据',
                 '最后别忘了判断买不起的情况：返回 `money` 而不是负数'],
    ),
)
