def _b(v, n=4):
    return format(v & ((1 << n) - 1), f'0{n}b')


def _info(S):
    s = ''
    if 'x' in S and 'num' not in S:
        return f"异或累计 `x` = `{_b(S['x'])}`（成对的抵消）"
    if 'lowbit' in S:
        s = f"`x` = `{_b(S['x'])}`，`lowbit` = `{_b(S['lowbit'])}`（x 最低位的 1）"
    return s


def _grp(S, i, v):
    lb = S.get('lowbit')
    if not lb:
        return None
    return 'pink' if lb & v else 'blue'


def _fin(S):
    if 'y' not in S:
        return ''
    s = f"`y` = `{_b(S['y'])}` = {S['y']}"
    if 'lowbit' in S and S.get('_line') is not None:
        s += f"　另一个数 `x ^ y` = {S['x'] ^ S['y']}"
    return s


CONFIG = dict(
    num=260, title='只出现一次的数字 III', difficulty='Medium', category='位运算',
    author='yiduobo', technique='lowbit 分组异或',
    tags=['九、其他'],
    code='''
class Solution(object):
    def singleNumber(self, nums):

        x = 0
        for num in nums:
            x ^= num

        lowbit = x & -x

        y = 0
        for num in nums:
            if lowbit & num:
                y ^= num

        return [y, x ^ y]
''',
    call='Solution().singleNumber([1,2,1,3,2,5])',
    expect=[3, 5],
    views=[
        dict(type='text', fn=_info, size=28),
        dict(type='array', var='nums', color=_grp, h=220, label='nums（粉 = 在 lowbit 那一位为 1，会被异或进 y）'),
        dict(type='text', fn=_fin, size=28),
    ],
    watch=['x', 'lowbit', 'num', 'y'],
    captions={
        'x ^= num': '`x ^= {num}` → `x = {x}`（`{_b(x)}`）：成对的数会抵消',
        'lowbit = x & -x': '设两个数是 num1、num2，`x = num1 ^ num2` = {x}。`x & -x` 取最低位的 1：`lowbit = {lowbit}`，==这一位上 num1、num2 一个 0 一个 1==',
        'if lowbit & num': lambda S, B, r: (f'`{S.num}` 在 lowbit 那位是 1 → ==参与异或==' if S.lowbit & S.num
                                            else f'`{S.num}` 在 lowbit 那位是 0 → 跳过'),
        'y ^= num': '`y ^= {num}` → `y = {y}`：该位为 1 的数里，成对的抵消',
        'return [y, x ^ y]': '`y` 是其中一个数 = {y}；另一个是 `x ^ y` = {x ^ y}。返回 `{[y, x ^ y]}`',
        'y = 0': '`y` 专门异或「lowbit 那一位为 1」的数',
    },
    cards=dict(
        one_liner='全体异或得 num1^num2，取一位 1 把两数分开',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组里两个数只出现一次，其余都出现两次',
                 '找出这两个数（线性时间，常数空间）',
                 '示例：`[1,2,1,3,2,5]` → `[3,5]`'],
        quote='可以发现，6中低位的1来自10，而高位的1来自12。',
        quote_src='—— yiduobo 题解原文（举例 10^12=6）',
        idea=['全部异或，出现两次的抵消，剩 `x = num1 ^ num2`，且 `x != 0`',
              'x 的每个 1 都说明 num1、num2 在该位不同，取 `lowbit = x & -x`',
              '只异或该位为 1 的数，得到其中一个 `y`，另一个是 `x ^ y`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`x & -x` 取最低位的 1，也是树状数组的 lowbit',
                 '这位为 1 的数里包含成对的数，它们照样抵消',
                 '原文为 Python 2 风格写法，类名 `Solution(object)`，代码未改动'],
    ),
)
