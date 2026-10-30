def _eq(S):
    if 'a' not in S:
        return f"目标 `c = {S.get('c', '')}`：枚举 `a`，看 `c − a²` 是不是完全平方数"
    a, c = S['a'], S['c']
    if 'b' not in S:
        return f"枚举 `a = {a}`：`2a² = {2*a*a}`，`c = {c}`"
    b = S['b']
    return f"`a = {a}`，`b = int(sqrt({c} − {a*a})) = {b}`：`{a*a} + {b*b}` = =={a*a+b*b}== 对 `c = {c}`"


def _sq(S):
    return [x * x for x in range(isqrt(S['c']) + 1)] if 'c' in S else []


CONFIG = dict(
    num=633, title='平方数之和', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举 a，开方求 b',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·数学算法'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def judgeSquareSum(self, c):

        a = 0
        while (a * a + a * a <= c):
            b = int(sqrt(c - a * a))
            if a * a + b * b == c:
                return True
            a += 1

        return False
''',
    call='Solution().judgeSquareSum(14)',
    expect=False,
    views=[
        dict(type='text', fn=_eq, h=60),
        dict(type='array', var=_sq, pointers={'a': 'blue', 'b': 'pink'}, h=300, label='平方数 [0², 1², ..., k²]（下标 = 底数）'),
    ],
    watch=[('a', 'a', 'blue'), 'b', 'c'],
    captions={
        'a = 0': '从 `a = 0` 开始枚举',
        'while (a * a': lambda S, B, ret: (
            f'`2a² = {2*S.a*S.a} <= c = {S.c}`：`a` 还不超过 `b`，继续' if 2 * S.a * S.a <= S.c
            else f'`2a² = {2*S.a*S.a} > c = {S.c}`：`a` 已经比 `b` 大，再枚举只是重复，停'),
        'b = int(sqrt': '`b = int(sqrt({c} − {a}²))` = `int(sqrt({c - a*a}))` = =={b}==',
        'if a * a + b * b == c': lambda S, B, ret: (
            f'`{S.a}² + {S.b}² = {S.a*S.a + S.b*S.b}` == `{S.c}`：==找到了==' if S.a * S.a + S.b * S.b == S.c
            else f'`{S.a}² + {S.b}² = {S.a*S.a + S.b*S.b}` != `{S.c}`：`c − a²` 不是完全平方数'),
        'a += 1': '`a` → {a}',
        'return True': '凑出了 `c`，返回 True',
        'return False': '枚举完都凑不出，返回 ==False==',
    },
    cards=dict(
        one_liner='枚举 a，开方得 b，再验证平方和',
        complexity='时间 `O(√c)`，空间 `O(1)`',
        problem=['给定非负整数 `c`，判断是否存在整数 `a`、`b` 使得 `a² + b² = c`',
                 '示例：`c = 5` → `true`；`c = 3` → `false`',
                 '本视频演示 `c = 14`（无解）'],
        quote='直接枚举a，然后通过sqrt(c - a^2)得到b，再判断a^2 + b^2是否等于c。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a` 从 0 往上枚举，`b = int(sqrt(c − a²))` 取整',
              '`b` 取整后验证 `a² + b² == c`，成立才说明开方是整数',
              '`a² + a² > c` 时 `a` 已经大于 `b`，对称的情况前面见过'],
        summary=['时间 `O(√c)`，空间 `O(1)`',
                 '停止条件 `2a² > c`：再往后只是交换 `a`、`b`，不会有新答案',
                 '易错：`sqrt` 是浮点数，要 `int()` 取整后再验证平方和',
                 '原文用到 `sqrt`，已在 setup 里 `from math import sqrt`；原文无其它 Python 2 写法需要改',
                 '作者提到存在数学定理（费马平方和定理）可 `O(√c)` 以内解决，这里用枚举'],
    ),
)
