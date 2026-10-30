def _sq(S):
    return [x * x for x in range(isqrt(S['c']) + 1)] if 'c' in S else []


def _eq(S):
    if 's' not in S:
        return f"目标 `c = {S.get('c', '')}`：在有序数组 `[0, 1, 4, 9, ...]` 里找两数之和"
    a, b, c = S['a'], S['b'], S['c']
    if a > b:
        return f"`a > b`：指针错开，没有解"
    s = S['s']
    sym = '=' if s == c else ('<' if s < c else '>')
    return f"`{a}² + {b}²` = `{a*a} + {b*b}` = =={s}== {sym} `c = {c}`"


CONFIG = dict(
    num=633, title='平方数之和', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 有序平方数组',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·数学算法'],
    code='''
class Solution:
    def judgeSquareSum(self, c: int) -> bool:
        a, b = 0, isqrt(c)
        while a <= b:
            s = a * a + b * b
            if s == c:
                return True
            if s < c:
                a += 1
            else:
                b -= 1
        return False
''',
    call='Solution().judgeSquareSum(32)',
    expect=True,
    views=[
        dict(type='text', fn=_eq, h=60),
        dict(type='array', var=_sq, pointers={'a': 'blue', 'b': 'pink'}, h=300, label='有序数组 [0², 1², ..., k²]（下标 = 底数）',
             window=('a', 'b')),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), 'c', 's'],
    captions={
        'a, b = 0': '`a = 0`，`b = isqrt({c}) = {b}`：两个指针分别指向最小、最大的平方数',
        'while a <= b': lambda S, B, ret: (('`a == b`：==等号必须有==，`a` 和 `b` 可以相等（如 `c = 2`）' if S.a == S.b
                                            else f'`a = {S.a} <= b = {S.b}`：指针还没错开，继续') if S.a <= S.b
                                           else '`a > b`：两个指针错开，还没找到'),
        's = a * a': '`s = {a}² + {b}² = {s}`，目标 `c = {c}`',
        'if s == c': lambda S, B, ret: (f'`{S.s} == {S.c}`：找到了 `{S.a}² + {S.b}² = {S.c}`' if S.s == S.c
                                        else f'`{S.s} != {S.c}`：继续比较大小'),
        'if s < c': lambda S, B, ret: (f'`{S.s} < {S.c}`：和太小' if S.s < S.c else f'`{S.s} > {S.c}`：和太大'),
        'a += 1': '和太小：`a` 与 `[a, b]` 里任何 `b\'` 的和都小于 `c`，`a²` 没希望 → `a` → {a}',
        'b -= 1': '和太大：`b` 与 `[a, b]` 里任何 `a\'` 的和都大于 `c`，`b²` 没希望 → `b` → {b}',
        'return True': '存在 `a² + b² = c`，返回 ==True==',
        'return False': '指针错开都没找到，返回 False',
    },
    cards=dict(
        one_liner='把平方数看成有序数组，转化为「两数之和」',
        complexity='时间 `O(√c)`，空间 `O(1)`',
        problem=['给定非负整数 `c`，判断是否存在整数 `a`、`b` 使得 `a² + b² = c`',
                 '示例：`c = 5` → `true`（`1² + 2²`）；`c = 3` → `false`',
                 '本视频演示 `c = 32`'],
        quote='设 k = ⌊√c⌋。本题相当于给你一个有序数组 [0,1,4,9,16,…,k²]，判断是否存在两数之和等于 c。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['数组 `[0², 1², ..., k²]` 有序，两端各放一个指针',
              '和太小：左指针 `a` 加一；和太大：右指针 `b` 减一',
              '`a` 和 `b` 可以相等，所以循环条件是 `a <= b`'],
        summary=['时间 `O(√c)`，空间 `O(1)`',
                 '易错：循环条件必须 `a <= b`，否则 `c = 2`（`1² + 1²`）会漏掉',
                 '其他语言要防溢出：改用 `a * a == c - b * b` 比较',
                 '方法一是枚举 `a`，用 `isqrt(c - a * a)` 求 `b`，枚举到 `2a² > c` 为止'],
    ),
)
