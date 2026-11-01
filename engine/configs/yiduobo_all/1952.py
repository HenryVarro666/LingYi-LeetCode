CONFIG = dict(
    num=1952, title='三除数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='质数平方 查表',
    tags=['难度分 1204'],
    code='''
class Solution(object):
    def isThree(self, n):

        p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        for num in p:
            if num * num == n:
                return True

        return False
''',
    call='Solution().isThree(121)',
    expect=True,
    views=[
        dict(type='array', var='p', label='质数表 p（蓝 = 当前 num）', h=240,
             color=lambda S, i, v: (('green' if v * v == S['n'] else 'blue') if 'num' in S and v == S['num'] else None),
             dim=lambda S, i, v: 'num' in S and v < S['num']),
        dict(type='text', fn=lambda S: f"`num = {S['num']}`：`{S['num']} × {S['num']} = {S['num']*S['num']}`，目标 `n = {S['n']}`" if 'num' in S else f"目标 `n = {S['n']}`：只可能是质数的平方"),
    ],
    watch=['n', ('num', 'num', 'blue')],
    captions={
        'p = [': 'n 不超过 10000，所以质数只需列到 100 以内：`p` 共 {len(p)} 个',
        'for num in p': '取下一个质数 `num = {num}`',
        'if num * num == n': lambda S, B, r: f'`{S.num} × {S.num} = {S.num*S.num}`' + (f' == {S.n}：==n 是质数的平方==' if S.num * S.num == S.n else f' != {S.n}，不是它'),
        'return True': '`n = {n}` 恰好是 `{num}` 的平方 → 约数只有 1、{num}、{n}，返回 ==True==',
        'return False': '所有质数的平方都不等于 `n` → 返回 ==False==',
    },
    cards=dict(
        one_liner='三个约数的数，一定是质数的平方',
        complexity='时间 `O(1)`（质数表固定 25 个），空间 `O(1)`',
        problem=['判断 `n` 是否恰好有三个正约数',
                 '`n` 不超过 `10^4`',
                 '本视频：`n = 121` → 约数 1、11、121 → `true`'],
        quote='有且仅有三个约数的数必然是质数的完全平方数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 分解质因数，约数个数 = `(k0+1)(k1+1)...`',
              '乘积等于 3 → 只有一个质因子，且指数 `k0 = 2`',
              '所以 `n = p^2`，把 100 以内的质数列出来逐个比较'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`n = 1` 只有一个约数，不会命中任何质数的平方',
                 '质数表范围由 `sqrt(10^4) = 100` 决定，换范围要重列',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（原代码本身无需改动）'],
    ),
)
