CONFIG = dict(
    num=2706, title='购买两块巧克力', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='一趟遍历找最小与次小', tags=[],
    code='''
class Solution(object):
    def buyChoco(self, prices, money):

        a = prices[0]
        b = prices[1]
        if a > b:
            a, b = b, a
        
        for p in prices[2:]:
            if p < a:
                a, b = p, a
            elif p < b:
                b = p
        
        if a + b <= money:
            return money - a - b
        else:
            return money
''',
    call='Solution().buyChoco([3,1,4,5,2,6], 4)',
    expect=1,
    views=[
        dict(type='array', var='prices', h=200,
             color=lambda S, i, v: 'green' if 'a' in S and v == S['a'] else 'yellow' if 'b' in S and v == S['b'] else 'blue' if S.get('p') == v else None),
        dict(type='text', h=90, fn=lambda S: f"最小 `a = {S['a']}`，次小 `b = {S['b']}`，合计 =={S['a'] + S['b']}== / money = {S['money']}" if 'b' in S else ''),
    ],
    watch=[('p', 'p', 'blue'), ('a', 'a', 'green'), ('b', 'b', 'yellow'), 'money'],
    captions={
        'a = prices[0]': '先拿前两个数当初值：`a = {a}`',
        'b = prices[1]': '`b = {b}`',
        'if a > b': '`a` 要放最小的：`{a} > {b}` → {"成立，交换" if a > b else "不成立，已有序"}',
        'a, b = b, a': '交换后 `a = {a}`，`b = {b}`',
        'if p < a': '`{p}` 比最小值 `{B.a}` 小吗？{"是，它成为最小" if p < B.a else "否，看能否当次小"}',
        'a, b = p, a': '`a` 换成新数 `{a}`，原来的最小值顺势成为次小 `b = {b}`',
        'elif p < b': '`{p}` 比次小值 `{B.b}` 小吗？{"是" if p < B.b else "否，丢掉"}',
        'b = p': '只更新次小：`b = {b}`',
        'if a + b <= money': '最便宜两块 `{a} + {b} = {a + b}`，`<= {money}` 吗？{"买得起" if a + b <= money else "买不起"}',
        'return money - a - b': '买得起，剩下 `{money} - {a} - {b}` = =={ret}==',
        'return money\n': '买不起，原样返回 =={ret}==',
    },
    cards=dict(
        one_liner='花费最小就买最便宜的两块，一趟遍历找最小和次小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['买恰好两块巧克力，剩余的钱不能为负，想剩得最多',
                 '买不起任何两块就返回原来的 `money`',
                 '示例：`prices=[3,2,3], money=3` → `3`'],
        quote='题目要求购买巧克力的花费最小，那么很明显应该买最便宜的两块。于是只需一趟遍历，找出prices中的最小值以及次小值即可。',
        quote_src='—— yiduobo 题解',
        idea=['先用前两个数初始化 `a`（小）、`b`（大）',
              '遍历后面的数：比 `a` 小就把 `a` 挤给 `b`',
              '否则比 `b` 小就只换 `b`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '初值取前两个数而不是无穷大，所以 `prices` 至少 2 个才安全',
                 '==`a, b = p, a` 一行同时完成新最小和老最小退位==',
                 '剩余钱数必须非负：买不起要返回 `money`'],
    ),
)
