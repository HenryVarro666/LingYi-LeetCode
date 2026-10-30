from math import gcd

CONFIG = dict(
    num=3411, title='最长乘积等价子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='两两互质 + 滑动窗口',
    tags=['数学算法', '难度分 2300'],
    code='''
class Solution:
    def maxLength(self, nums: List[int]) -> int:
        ans = 2
        mul = 1
        left = 0
        for right, x in enumerate(nums):
            while gcd(mul, x) > 1:
                mul //= nums[left]
                left += 1
            mul *= x
            ans = max(ans, right - left + 1)
        return ans
''',
    call='Solution().maxLength([2,3,4,5,6])',
    expect=3,
    views=[
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=240,
             dim=lambda S, i, v: 'left' in S and 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', fn=lambda S: (f"窗口乘积 `mul = {S['mul']}`；新数 `x = {S['x']}`，`gcd(mul, x) = {gcd(S['mul'], S['x'])}`" if 'x' in S and 'mul' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'x', 'mul', ('ans', 'ans', 'green')],
    captions={
        'ans = 2': '任意两个数一定乘积等价，所以答案至少是 `2`',
        'for right': '新数 `x = {x}`：要想加入窗口，必须和窗口里所有数==两两互质==',
        'while gcd': lambda S, B, ret: f"`gcd({S['mul']}, {S['x']}) = {gcd(S['mul'], S['x'])}`：" + ("> 1，窗口里有数和 x 共因子，必须踢掉" if gcd(S['mul'], S['x']) > 1 else "= 1，互质，可以加入"),
        'mul //= nums[left]': '踢掉最左的 `{nums[left]}`：`mul` 变为 {mul}',
        'left += 1': '`left` → {left}',
        'mul *= x': 'x 加入窗口，乘积 `mul = {mul}`（互质数的乘积能代表整个窗口）',
        'ans = max': '窗口长 `right - left + 1 = {right-left+1}`，`ans = max({B.ans}, {right-left+1}) = {ans}`',
    },
    cards=dict(
        one_liner='k ≥ 3 时乘积等价 ⟺ 两两互质，用滑窗维护',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['数组满足 `prod == lcm * gcd` 叫乘积等价',
                 '求 `nums` 最长的乘积等价子数组长度',
                 '示例：`[2,3,4,5,6]` → `3`（`[3,4,5]`）'],
        quote='如果 k≥3，那么这 k 个数必须两两互质。如果两个数有大于 1 的公因子，那么不满足「至少 k-1 个 e_i=0」的要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['对每个质数的指数：乘积是 ==求和==，lcm 是 ==最大值==，gcd 是 ==最小值==',
              '`k ≥ 3` 时要求和 = 最大 + 最小，只能至少 k−1 个指数为 0，即两两互质',
              '窗口里只留互质的数，把它们的乘积记成 `mul`，用 `gcd(mul, x)` 一次判断'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '易错：`ans` 初值是 `2`，两个数总是合法',
                 '==先踢掉不互质的数，再把 x 乘进 mul==',
                 '另一种写法：暴力枚举子数组，乘积超过 `lcm(all) * max` 就停（方法一）'],
    ),
)
