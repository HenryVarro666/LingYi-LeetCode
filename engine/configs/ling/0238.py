NUMS = [2, 3, 4, 5]
ANS = [60, 40, 30, 24]


def _nums_color(S, j, v):
    i = S.get('i')
    if i is None:
        return None
    if 'pre' in S:                      # 第二轮：左边进了 pre，右边在 suf[i] 里
        if j < i:
            return 'blue'
        if j > i:
            return 'pink'
        return None
    return 'pink' if j > i else None    # 第一轮：suf[i] 是右边这些数的乘积


def _info(S):
    i = S.get('i')
    if i is None or 'suf' not in S:
        return ''
    if 'pre' in S and 'x' in S:
        return f'粉 = 右边（已在 `suf[{i}]` 里），蓝 = 左边（`pre = {S["pre"]}`）'
    return f'粉 = `suf[{i}]` 覆盖的右边部分 `nums[{i + 1}..{len(S["nums"]) - 1}]`'


CONFIG = dict(
    num=238, title='除了自身以外数组的乘积', difficulty='Medium', category='普通数组',
    author='灵茶山艾府', technique='前后缀分解（空间优化）',
    code='''
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        suf = [1] * n
        for i in range(n - 2, -1, -1):
            suf[i] = suf[i + 1] * nums[i + 1]

        pre = 1
        for i, x in enumerate(nums):
            # 此时 pre 为 nums[0] 到 nums[i-1] 的乘积，直接乘到 suf[i] 中
            suf[i] *= pre
            pre *= x

        return suf
''',
    call=f'Solution().productExceptSelf({NUMS})',
    expect=[60, 40, 30, 24],
    views=[
        dict(type='text', fn=_info),
        dict(type='array', var='nums', pointers={'i': 'yellow'}, color=_nums_color, cell=110, h=200),
        dict(type='array', var='suf', label='suf（绿 = 已经是最终答案）', pointers={'i': 'yellow'}, cell=110, h=200,
             color=lambda S, j, v: 'green' if 'pre' in S and 'x' in S and j <= S['i'] and v == ANS[j] else None),
    ],
    watch=[('i', 'i', 'yellow'), 'x', ('pre', 'pre', 'blue'), ('suf', 'suf', 'pink')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'suf = [1] * n': '`suf[i]` = `nums[i+1]` 到 `nums[n-1]` 的乘积。`suf[n-1]` 是==空子数组的乘积，规定为 1==',
        'for i in range(n - 2': lambda S, B, ret: (f'倒着算后缀积：`i = {S.i}`' if 'i' not in B or S.i != B.i else '后缀积算好了'),
        'suf[i] = suf[i + 1] * nums[i + 1]': '`suf[{i}] = suf[{i + 1}] × nums[{i + 1}] = {suf[i + 1]} × {nums[i + 1]} = {suf[i]}`',
        'pre = 1': '`pre` = 左边所有数的乘积，从空乘积 `1` 开始（不再开 `pre` 数组）',
        'for i, x in enumerate': lambda S, B, ret: (f'正着走：`i = {S.i}`，`x = {S.x}`' if 'x' not in B or S.i != B.i else '遍历结束'),
        'suf[i] *= pre': '`suf[{i}]`（右边之积 `{B.suf[i]}`）× `pre`（左边之积 `{pre}`）= =={suf[i]}==，这就是 `answer[{i}]`',
        'pre *= x': '`pre = {B.pre} × {x} = {pre}`：把 `nums[{i}]` 乘进左边之积，留给下一个位置',
        'return suf': '`suf` 已经变成答案，直接返回 `{ret}`',
    },
    cards=dict(
        one_liner='answer[i] = i 左边所有数之积 × i 右边所有数之积',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['返回数组 `answer`：`answer[i]` = 除 `nums[i]` 外其余各元素的乘积',
                 '==不能用除法==，时间要求 `O(n)`',
                 '示例：`[1,2,3,4]` → `[24,12,8,6]`',
                 '演示用 `[2,3,4,5]` → `[60,40,30,24]`'],
        quote='如果知道了 i 左边所有数的乘积，以及 i 右边所有数的乘积，就可以算出 answer[i]。……先计算 suf，然后一边计算 pre，一边把 pre 直接乘到 suf[i] 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['递推：`pre[i] = pre[i-1] · nums[i-1]`，`suf[i] = suf[i+1] · nums[i+1]`',
              '初始值 `pre[0] = suf[n-1] = 1`：==空子数组的乘积规定为 1==，方便递推',
              '优化：`pre` 用一个变量，边算边乘进 `suf[i]` → 省一个数组、少遍历一次'],
        summary=['时间 `O(n)`，空间 `O(1)`：题目说输出数组不算额外空间',
                 '==先 suf[i] *= pre，再 pre *= x==：乘进去的 `pre` 不能含 `nums[i]` 自己',
                 '后缀积从 `n − 2` 倒着算，`suf[n-1] = 1`',
                 '优化前写法：分别建 `pre`、`suf` 两个数组再逐位相乘，空间 `O(n)`',
                 '这类套路叫「前后缀分解」'],
    ),
)
