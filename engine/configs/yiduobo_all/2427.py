CONFIG = dict(
    num=2427, title='公因子的数目', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='暴力枚举 1..min(a,b)',
    tags=['数论', '难度分 1172'],
    code='''
class Solution(object):
    def commonFactors(self, a, b):

        res = 0
        for x in range(1, min(a, b) + 1):
            if a % x == 0 and b % x == 0:
                res += 1
        
        return res
''',
    call='Solution().commonFactors(12, 18)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f'`{S["x"]}`：`{S["a"]} % {S["x"]} = {S["a"] % S["x"]}`，`{S["b"]} % {S["x"]} = {S["b"] % S["x"]}`' if 'x' in S else '数据只到 1000：每个 `x` 都试一遍'), h=60),
        dict(type='array', var=lambda S: list(range(1, min(S['a'], S['b']) + 1)) if 'a' in S else [],
             label='x 从 1 到 min(a, b)（绿 = 公因子）', 
             color=lambda S, k, v: 'green' if S['a'] % v == 0 and S['b'] % v == 0 and ('x' in S and (v < S['x'] or (v == S['x'] and S.get('_line') != 5))) else ('blue' if 'x' in S and v == S['x'] else None),
             cell=64, h=260),
    ],
    watch=['a', 'b', ('x', 'x', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计公因子个数',
        'for x in range': lambda S, B, r: ('`x` 已经枚举到 min(a, b)，循环结束' if 'x' in B and B.x == S.x else f'试 `x = {S.x}`' if 'x' in S else f'`x` 从 1 枚举到 `min(a, b) = {min(S.a, S.b)}`，规模很小可以直接暴力'),
        'if a % x == 0 and b % x == 0': lambda S, B, r: (f'`{S.a} % {S.x} = {S.a % S.x}`，`{S.b} % {S.x} = {S.b % S.x}` → ' + ('==两个都整除，是公因子==' if S.a % S.x == 0 and S.b % S.x == 0 else '至少一个不整除，跳过')),
        'res += 1': '`x = {x}` 是公因子 → `res = {res}`',
        'return res': '共 `{ret}` 个公因子',
    },
    cards=dict(
        one_liner='数据规模很小：从 1 到 min(a,b) 逐个试除',
        complexity='时间 `O(min(a,b))`，空间 `O(1)`',
        problem=['给两个正整数 `a`、`b`，求能同时整除它们的 `x` 的个数',
                 '示例：`a = 12, b = 6` → `4`（1、2、3、6）',
                 '本视频：`a = 12, b = 18` → `4`（1、2、3、6）'],
        quote='由于题目的数据规模非常小，那么完全可以从1开始到min(a, b)枚举所有的数x，并统计其中是a和b公因子的x的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a, b ≤ 1000`，最多枚举 1000 个数',
              '公因子不会超过 `min(a, b)`，所以枚举上界取 `min`',
              '`a % x == 0 and b % x == 0` 就计一个'],
        summary=['时间 `O(min(a,b))`，空间 `O(1)`',
                 '`range(1, min(a, b) + 1)` 右端要 `+ 1`，否则漏掉 `x = min(a, b)`',
                 '原文本身是 Python 3 可运行的写法，只是类写成 `Solution(object)`',
                 '对比灵神：先求 gcd，只枚举到 sqrt(g)，更快'],
    ),
)
