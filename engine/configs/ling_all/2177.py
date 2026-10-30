CONFIG = dict(
    num=2177, title='找到和为给定整数的三个连续整数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='中间数 = num / 3', tags=[],
    code='''
class Solution:
    def sumOfThree(self, num: int) -> List[int]:
        x = num // 3
        return [] if num % 3 else [x - 1, x, x + 1]
''',
    call='[Solution().sumOfThree(33), Solution().sumOfThree(4)]',
    expect=[[10, 11, 12], []],
    views=[
        dict(type='text', size=34, h=120, fn=lambda S: (
            f"`{S['x']-1} + {S['x']} + {S['x']+1}` = {3*S['x']}，num = {S['num']}" if 'x' in S and 3 * S['x'] == S['num']
            else f"`3x = {3*S['x']}` ≠ num = {S['num']}：凑不出" if 'x' in S else f"num = {S['num']}")),
        dict(type='array', var=lambda S: [S['x'] - 1, S['x'], S['x'] + 1] if 'x' in S and 3 * S['x'] == S['num'] else [], label='三个连续整数（x−1, x, x+1）',
             cell=120, h=200, color=lambda S, i, v: 'green' if i == 1 else None),
    ],
    watch=[('num', 'num'), ('x', 'x', 'blue'), ('num % 3', lambda S: S['num'] % 3, 'orange')],
    captions={
        'x = num // 3': '设中间数为 `x`，三数之和就是 `3x`，所以 `x = {num} // 3 = =={x}==`',
        'return': '`num % 3 = {num % 3}`：' + '{"余数为 0，是 3 的倍数 → 返回 [x-1, x, x+1]" if num % 3 == 0 else "不是 3 的倍数 → 返回空数组"}',
    },
    cards=dict(
        one_liner='三个连续整数的和 = 3 倍的中间数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['返回三个连续整数，使它们的和等于 `num`；做不到返回空数组',
                 '示例：`33` → `[10,11,12]`；`4` → `[]`'],
        quote='x = num // 3；return [] if num % 3 else [x - 1, x, x + 1]',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['设三个数为 `x-1, x, x+1`，加起来恰好是 `3x`',
              '所以 `num` 必须是 ==3 的倍数==，中间数就是 `num // 3`',
              '余数不为 0 就直接返回空数组'],
        after=[dict(heading='为什么是 3 的倍数', lines=['`x-1 + x + x+1 = 3x`，两侧的偏移量正好抵消', '例：`33 = 3×11` → `[10,11,12]`', '例：`4` 除以 3 余 1，凑不出 → `[]`', '`num` 最大 `10^15`，Python 大整数直接算即可'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：先看 `num % 3`，不能直接用 `//` 的结果当中间数',
                 '同类思路：连续整数求和都先想「中间数 × 个数」'],
    ),
)
