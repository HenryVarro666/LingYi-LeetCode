def _bits(v, w=4):
    return format(v, '0%db' % w)


JL = (8, 9, 10, 11, 12)


def _info(S):
    if 'x' not in S:
        return ''
    i, x = S['i'], S['x']
    nums = S['nums']
    if 'j' in S and S['_line'] in JL and S['j'] < i:
        j = S['j']
        return f"`x = {_bits(x)}`　`nums[{j}] = {_bits(nums[j])}`　OR = `{_bits(nums[j] | x)}`　目标 `k = {S['k']}`"
    return f"`x = nums[{i}] = {_bits(x)}`　目标 `k = {S['k']}`"


CONFIG = dict(
    num=3097, title='或值至少为 K 的最短子数组 II', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='LogTrick · 或值只增不减',
    tags=['灵神题单', '难度分 1891'],
    code='''
class Solution:
    def minimumSubarrayLength(self, nums: List[int], k: int) -> int:
        ans = inf
        for i, x in enumerate(nums):
            if x >= k:
                return 1
            for j in range(i - 1, -1, -1):
                if nums[j] | x == nums[j]:
                    break
                nums[j] |= x
                if nums[j] >= k:
                    ans = min(ans, i - j + 1)
        return ans if ans < inf else -1
''',
    call='Solution().minimumSubarrayLength([2,1,8,1], 10)',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=30, h=60),
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, h=240, label='nums（原地改成「以 i 结尾的子数组或值」）',
             color=lambda S, idx, v: ('blue' if idx == S.get('i') else 'pink' if S['_line'] in JL and idx == S.get('j') else None)),
        dict(type='text', fn=lambda S: f"当前最短长度 ans = =={S['ans'] if S['ans'] != float('inf') else '∞（还没找到）'}==" if 'ans' in S else '', size=28, h=60),
    ],
    watch=['i', 'x', 'j', ('k', 'k', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '最短长度先设成无穷大',
        'for i, x in enumerate': lambda S, B, r: (f'`i = {S.i}`：看右端点为 `{S.i}` 的所有子数组' if S.get('i') != B.get('i') else '枚举结束'),
        'if x >= k': lambda S, B, r: (f'`x = {S.x} >= k = {S.k}`：单个元素就够了，长度 1 已是最短 → 直接返回' if S.x >= S.k
                                      else f'`x = {S.x} < k = {S.k}`：单个元素不够，要向左并入更多元素'),
        'return 1': '长度 1 不可能再短，返回 `1`',
        'if nums[j] | x == nums[j]': lambda S, B, r: (f'`nums[{S.j}] | x = {S.nums[S.j]}` 等于它自己 → ==x 已是子集==，再往左也不会变，退出内层循环' if S.nums[S.j] | S.x == S.nums[S.j]
                                                   else f'`{_bits(S.nums[S.j])} | {_bits(S.x)} = {_bits(S.nums[S.j] | S.x)}` ≠ 原值 → 或值会增大，继续并入'),
        'break': '退出内层循环：`nums[{j}]` 及更左的元素都不用再改了',
        'nums[j] |= x': '`nums[{j}]` 增大为 `{nums[j]}`：它现在表示 `[{j}..{i}]` 的或值',
        'if nums[j] >= k': lambda S, B, r: (f'`[{S.j}..{S.i}]` 的或值 `{S.nums[S.j]} >= k = {S.k}` → 是特别子数组' if S.nums[S.j] >= S.k
                                            else f'`[{S.j}..{S.i}]` 的或值 `{S.nums[S.j]} < k = {S.k}` → 还不够'),
        'ans = min(ans, i - j + 1)': '长度 `{i} − {j} + 1 = {i-j+1}`，`ans` = {ans}',
        'return ans if': lambda S, B, r: (f'找到了，最短长度 `{r}`' if r != -1 else '没有特别子数组，返回 `-1`'),
    },
    skip=['for j in range'],
    max_steps=90,
    cards=dict(
        one_liner='或值只增不减：x 已是子集就停，一旦 ≥ k 就记长度',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['找最短非空子数组，使所有元素按位或 `>= k`；不存在返回 `-1`',
                 '示例：`nums=[2,1,8], k=10` → `3`（或值 11）',
                 '本视频：`[2,1,8,1], k=10` → `3`'],
        quote='本题和 3171 思路是一样的，我的题解详细解释了两个方法的原理。本文只留代码。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums[j]` 被改写成 `[j..i]` 的或值，或值越并越大',
              '`nums[j] | x == nums[j]` 说明 x 是子集，左边也不变 → ==break==',
              '`nums[j] >= k` 时，当前长度 `i-j+1` 更新答案；单个元素 `x >= k` 直接返回 1'],
        after=[dict(heading='另一种写法：滑动窗口 + 栈', lines=[
            '或值随窗口变长而增大，满足 `>= k` 就收缩左端点',
            'OR 没有逆运算，用栈保存后缀或值',
            '本视频演示 LogTrick；思考题：OR 改 XOR 要用前缀异或和'])],
        summary=['时间 `O(n log U)`，空间 `O(1)`（原地改 nums）',
                 '易错：`k = 0` 时任何单个元素都满足，`x >= k` 先返回 1',
                 '易错：从右往左并入时，`break` 条件是 `nums[j] | x == nums[j]`',
                 '同类题：3171、1521、2411，见位运算题单 LogTrick'],
    ),
)
