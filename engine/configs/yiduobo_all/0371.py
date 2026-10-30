def _b(v):
    return format(v % (1 << 8), '08b')


def _row(S):
    if 'a' not in S:
        return ''
    return f"`a`（进位）= `{format(S['a'] % 256, '08b')}`　　`b`（不进位和）= `{format(S['b'] % 256, '08b')}`　　只显示低 8 位"


def _dim(S):
    if 'b' not in S:
        return ''
    return f"b = {S['b']}"


CONFIG = dict(
    num=371, title='两整数之和', difficulty='Medium', category='位运算',
    author='yiduobo', technique='异或加法 + 进位 · 模 2^32',
    tags=[],
    code='''
class Solution(object):
    def getSum(self, a, b):

        while a:
            tmp = a ^ b
            a &= b
            a <<= 1
            b = tmp
            a %= 4294967296
            b %= 4294967296

        if b > 2147483647:
            return ~((b % 2147483648) ^ 2147483647)
        else:
            return b
''',
    call='Solution().getSum(11, 5)',
    expect=16,
    views=[
        dict(type='text', fn=_row, size=28, h=120),
        dict(type='array', var=lambda S: [int(c) for c in format(S['a'] % 256, '08b')], h=170, label='a 的低 8 位（要继续加进去的进位）', index=False,
             color=lambda S, i, v: 'pink' if v else None),
        dict(type='array', var=lambda S: [int(c) for c in format(S['b'] % 256, '08b')], h=170, label='b 的低 8 位（当前的和）', index=False,
             color=lambda S, i, v: 'blue' if v else None),
    ],
    watch=['a', 'b', 'tmp'],
    captions={
        'while a': lambda S, B, r: (f'`a = {S.a}` 还有进位 → 继续把进位加进 b' if S.a else '`a = 0`：没有进位了，加法完成'),
        'tmp = a ^ b': '异或 = 不进位的加法：`tmp = a ^ b` = {tmp}',
        'a &= b': '两边都是 1 的位才会进位：`a & b` = {a}',
        'a <<= 1': '进位要加到高一位：左移一位，`a` = {a}',
        'b = tmp': '`b` 变成不进位的和 {b}；下一轮把进位 `a` 加进去',
        'a %= 4294967296': '`a % 2^32`：Python 整数无上界，把进位限制在 32 位内 → {a}',
        'b %= 4294967296': '`b % 2^32` → {b}（非负数不变；负数才会变成补码对应的大正数）',
        'if b > 2147483647': lambda S, B, r: (f'`b = {S.b}` 大于 `2^31 - 1`，说明符号位是 1，真实结果是负数' if S.b > 2147483647 else f'`b = {S.b}` 不超过 `2^31 - 1`，结果非负，直接返回'),
        'return ~(': '符号位为 1：低 31 位取反后再 `~`，还原成负数 `{ret}`',
        'return b': '直接返回 `{ret}`',
    },
    cards=dict(
        one_liner='异或做不进位加法，与再左移一位得进位，重复到没进位',
        complexity='时间 `O(1)`（最多约 32 轮），空间 `O(1)`',
        problem=['不用 `+` 和 `-`，计算两个整数 `a`、`b` 的和',
                 '整数范围是 32 位有符号整数',
                 '本视频示例：`getSum(11, 5)` → `16`'],
        quote='异或运算可以认为是不进位的加法运算，于是对于两个整数a和b，我们可以先通过异或得出没有进位的各位之后。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a ^ b` 是不进位的和；`(a & b) << 1` 是进位',
              '把「和」与「进位」再相加，重复到进位为 0',
              'Python 整数无上界，所以每轮 `% 2^32`，最后按 `2^31` 判断符号映射回负数'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '负数在 Python 里是无限长补码，必须模 `2^32` 限制位数，否则循环不会结束',
                 '`b > 2^31 - 1` 说明符号位为 1，要用 `~((b % 2^31) ^ (2^31 - 1))` 还原',
                 '原文为 Python 2 风格写法，类名 `Solution(object)`，代码未改动'],
    ),
)
