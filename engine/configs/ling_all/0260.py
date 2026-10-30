def _b(v, n=4):
    return format(v & ((1 << n) - 1), f'0{n}b')


def _grp(S, i, v):
    sh = S.get('shift')
    if sh is None:
        return None
    return 'blue' if (v >> sh & 1) == 0 else 'pink'


def _info(S):
    if 'xor_all' not in S:
        return '两个只出现一次的数 a、b；其余成对出现，异或会抵消'
    s = f"`xor_all` = `{_b(S['xor_all'])}`（= a ^ b，一定不为 0）"
    if 'shift' in S:
        s += f"　取最高位的 1：第 ==`{S['shift']}`== 位，a、b 在这一位不同"
    return s


def _cur(S):
    if 'x' not in S or 'shift' not in S:
        return ''
    x, sh = S['x'], S['shift']
    g = x >> sh & 1
    return f"当前 `x = {x}`（`{_b(x)}`），第 {sh} 位是 =={g}==，异或进 `ans[{g}]`"


CONFIG = dict(
    num=260, title='只出现一次的数字 III', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='异或分组 · 尾零直接取位',
    tags=['九、其他'],
    code='''
class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        xor_all = reduce(xor, nums)
        shift = xor_all.bit_length() - 1 if xor_all > 0 else 31

        ans = [0, 0]
        for x in nums:
            ans[x >> shift & 1] ^= x
        return ans
''',
    call='Solution().singleNumber([1,2,1,3,2,5])',
    expect=[3, 5],
    views=[
        dict(type='text', fn=_info, size=28),
        dict(type='array', var='nums', color=_grp, h=200, label='nums（蓝 = 该位为 0 的一组，粉 = 该位为 1 的一组）'),
        dict(type='text', fn=_cur, size=28),
        dict(type='array', var='ans', h=170, label='ans（两组各自异或）', color=lambda S, i, v: 'blue' if i == 0 else 'pink'),
    ],
    watch=['xor_all', 'shift', 'x', ('ans', 'ans', 'green')],
    captions={
        'xor_all = reduce': '全部异或：成对的数互相抵消，只剩 `a ^ b` = =={xor_all}==（`{_b(xor_all)}`）',
        'shift =': '`a != b` 所以 `xor_all` 至少有一位是 1。取最高位的 1：`bit_length() - 1` = =={shift}==，a 和 b 在这一位上不同',
        'ans = [0, 0]': '准备两个异或累加器：==第 0 组、第 1 组==',
        'ans[x >> shift & 1] ^= x': '`x = {B.x}` 的第 `{shift}` 位是 `{x >> shift & 1}` → 异或进 `ans[{x >> shift & 1}]`，现在 `ans = {ans}`',
        'for x in nums': '依次取 `nums` 里的数，按第 `{shift}` 位分组',
        'return ans': '每组里成对的数都抵消了，只剩 a 和 b 各一个：`{ans}`',
    },
    cards=dict(
        one_liner='异或后找一位把两个数拆开，再各自异或',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组里恰好两个数只出现一次，其余都出现两次',
                 '找出这两个数，要求线性时间、常数额外空间',
                 '示例：`[1,2,1,3,2,5]` → `[3,5]`'],
        quote='计算异或和的尾零的个数，这样可以直接取到 nums[i] 在该比特位上的值，从而避免 if-else。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['全体异或得 `a ^ b`，某一位为 1 说明 a、b 在该位不同',
              '按这一位把数组分成两组：==a、b 各在一组==，成对的数不会被拆开',
              '写法二用 `ans[x >> shift & 1] ^= x`，省掉 if-else'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`xor_all` 不会为 0，因为 a != b；`shift` 取最高位的 1',
                 '负数在 Python 里 `bit_length` 按绝对值算，所以代码对 `xor_all <= 0` 取 31',
                 '写法一用 `lowbit = xor_all & -xor_all` 加 if-else 分组，思路一样'],
    ),
)
