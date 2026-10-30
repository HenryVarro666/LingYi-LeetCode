CONFIG = dict(
    num=507, title='完美数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='枚举约数到 sqrt(n)',
    tags=['灵神题单', '数学算法'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def checkPerfectNumber(self, num):

        if num <= 1:
            return False

        tmp = 1
        for i in range(2, int(sqrt(num) + 1)):
            if i * i > num:
                break
            elif i * i == num:
                tmp += i
            elif num % i == 0:
                tmp += i + num // i
        return tmp == num
''',
    call='Solution().checkPerfectNumber(28)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"约数和 `tmp = {S['tmp']}`，目标 `num = {S['num']}`" if 'tmp' in S else ''), size=28),
        dict(type='text', fn=lambda S: (f"当前 `i = {S['i']}`：`{S['num']} % {S['i']} = {S['num'] % S['i']}`" + ('，==整除==：两个约数 ' + f"`{S['i']}` 和 `{S['num']//S['i']}`" if S['num'] % S['i'] == 0 else '，不整除') if 'i' in S and S['i'] > 0 and S['num'] > 1 else ''), size=26),
    ],
    watch=['num', ('tmp（约数和）', 'tmp', 'green'), ('i', 'i', 'blue')],
    captions={
        'if num <= 1': '1 和更小的数没有「除自身外的正约数」之和等于自己的可能 → 直接 `False`',
        'tmp = 1': '`tmp` 累加约数，先放进 `1`（1 一定是约数，且不是 num 本身）',
        'for i in range': '`i` 只需要枚举 `2` 到 sqrt(num)，因为约数总是成对出现',
        'if i * i > num': lambda S, B, r: (f'`{S.i}² = {S.i*S.i} > {S.num}`：超过 sqrt(num) 了，停' if S.i*S.i > S.num else f'`{S.i}² = {S.i*S.i} <= {S.num}`：还在范围内'),
        'elif i * i == num': lambda S, B, r: (f'`{S.i}² == {S.num}`：完全平方数，`i` 和 `num/i` 是同一个数，只加一次' if S.i*S.i == S.num else f'`{S.i}² != {S.num}`，不是完全平方'),
        'elif num % i == 0': lambda S, B, r: (f'`{S.num} % {S.i} == 0` → `{S.i}` 是约数，`{S.num // S.i}` 也是' if S.num % S.i == 0 else f'`{S.num} % {S.i} != 0`，不是约数'),
        'tmp += i + num': '一次加上一对约数：`{i} + {num // i}`，`tmp` → =={tmp}==',
        'return tmp == num': lambda S, B, r: f'`tmp = {S.tmp}`，`num = {S.num}`，{"相等 → 完美数" if S.tmp == S.num else "不相等 → 不是"}',
    },
    cards=dict(
        one_liner='约数成对出现：枚举到 sqrt(num)，一次加两个',
        complexity='时间 `O(sqrt(num))`，空间 `O(1)`',
        problem=['完美数：等于它除自身外所有正约数之和的正整数',
                 '给定 `num`，判断它是不是完美数',
                 '示例：`28` → `True`（1+2+4+7+14 = 28）'],
        quote='采用的是朴素的O(sqrt(n))的做法，具体就是从1到sqrt(n)循环，若当前数x能被num整数，那么x和num/x都是num的约数，将这两个数累加至sum，最后判断sum是否等于num。',
        quote_src='—— yiduobo 题解原文',
        idea=['`i` 能整除 `num`，则 `num // i` 也是约数，成对加入',
              '`1` 的配对是 `num` 自己，不能算，所以 `tmp` 从 `1` 起、`i` 从 `2` 起',
              '完全平方数的 sqrt 只能加一次'],
        summary=['时间 `O(sqrt(num))`，空间 `O(1)`',
                 '易错：`i * i == num` 时只加 `i`；`num <= 1` 要先返回 `False`',
                 '原文为 Python 2 写法，`/` 整除已改为 `//`；`sqrt` 来自 `math`'],
    ),
)
