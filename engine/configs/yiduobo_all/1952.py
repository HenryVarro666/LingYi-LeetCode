CONFIG = dict(
    num=1952, title='三除数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='质数平方判断',
    tags=['数论', '难度分 1204'],
    code='''
class Solution(object):
    def isThree(self, n):

        p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        for num in p:
            if num * num == n:
                return True

        return False
''',
    call='Solution().isThree(49)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f'`n = {S["n"]}`：恰好 3 个约数 ⇔ ==n 是质数的平方==' if 'num' not in S else f'`{S["num"]}² = {S["num"] * S["num"]}`，和 `n = {S["n"]}` 比较'), h=60),
        dict(type='array', var='p', label='100 以内的质数 p', cell=64,
             color=lambda S, k, v: 'blue' if 'num' in S and v == S['num'] else None,
             dim=lambda S, k, v: 'num' in S and v < S['num'], h=200),
    ],
    watch=['n', ('num', 'num', 'blue')],
    captions={
        'p = [2': '`n ≤ 10000`，所以质数 `p` 只需列到 100（`100² = 10000`）',
        'for num in p': '取下一个质数 `num = {num}`',
        'if num * num == n': lambda S, B, r: (f'`{S.num}² = {S.num * S.num}` == `n = {S.n}` → ==n 是质数 {S.num} 的平方==' if S.num * S.num == S.n else f'`{S.num}² = {S.num * S.num}` ≠ `{S.n}`，换下一个质数'),
        'return True': '`n` 恰好有三个约数 1、{num}、{n} → ==返回 True==',
        'return False': '没有任何质数的平方等于 n → 返回 False',
    },
    cards=dict(
        one_liner='恰好三个约数 ⇔ n 是某个质数的平方',
        complexity='时间 `O(1)`（质数表固定），空间 `O(1)`',
        problem=['给整数 `n`，若恰好有三个正除数返回 `true`，否则 `false`',
                 '示例：`n = 2` → `false`（只有 1、2）',
                 '示例：`n = 4` → `true`（1、2、4）；本视频：`n = 49`'],
        quote='有且仅有三个约数的数必然是质数的完全平方数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n = p0^k0 × … × pm^km`，约数个数 `(k0+1)(k1+1)…(km+1)`',
              '乘积要等于 3（质数）→ 只有一项且 `k0 = 2`，即 `n = p²`',
              '`n ≤ 10000`，把 100 以内的质数列出来，逐个看平方是否等于 `n`'],
        summary=['时间 `O(1)`，空间 `O(1)`：质数表只有 25 个',
                 '`n = 1` 只有 1 个约数，不会等于任何质数的平方，返回 False',
                 '原文本身是 Python 3 可运行的写法，未做修改',
                 '对比灵神：枚举 `i` 到 sqrt(n) 数约数个数，不依赖质数表'],
    ),
)
