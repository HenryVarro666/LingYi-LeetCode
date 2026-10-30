def _info(S):
    nums = S['nums']
    n = len(nums)
    line = S.get('_line', 0)
    if line >= 8 and 'xor_sum' in S:
        z = S['xor_sum'] == 0
        return (f"`xor_sum = {S['xor_sum']}`：" + ('==为 0，不能全选== → 去掉一个非零元素，`n - 1`' if z else '==非 0，全选== → `n`'))
    if line >= 5:
        return '有非零元素，有解；再看异或和是否为 0'
    return ''


CONFIG = dict(
    num=3702, title='按位异或非零的最长子序列', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='分类讨论 · 全选或去掉一个', tags=['灵神题单', '难度分 1489'],
    code='''
class Solution:
    def longestSubsequence(self, nums: List[int]) -> int:
        if all(x == 0 for x in nums):
            return 0  # nums 全为 0，无解

        xor_sum = reduce(xor, nums)
        # 如果 xor_sum 为 0，那么去掉 nums 的一个非零元素，就可以使 xor_sum 不为 0
        return len(nums) - (xor_sum == 0)
''',
    call='Solution().longestSubsequence([2, 3, 1])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=190, label='nums',
             color=lambda S, i, v: ('yellow' if v != 0 else None) if 'xor_sum' in S and S['xor_sum'] == 0 and v != 0 and i == [j for j, x in enumerate(S['nums']) if x][0] else None),
        dict(type='text', size=28, fn=_info),
        dict(type='text', size=28, fn=lambda S: (f"`{' ^ '.join(map(str, S['nums']))}` = =={S['xor_sum']}==" if 'xor_sum' in S else '')),
    ],
    watch=[('n', 'len(nums)', 'blue'), ('xor_sum', 'xor_sum', 'yellow')],
    captions={
        'if all': lambda S, B, r: '检查 `nums` 是否全为 0：有非零元素，继续',
        'xor_sum = reduce': '所有元素的异或和 `xor_sum = {xor_sum}`',
        'return len(nums)': lambda S, B, r: (f'`xor_sum = {S.xor_sum}` 非 0：全选就满足条件，返回 `n = {r}`' if S.xor_sum else
                                             f'`xor_sum = 0`：不能全选，去掉一个非零元素（相当于异或上它）就非 0，返回 `n - 1 = {r}`'),
    },
    cards=dict(
        one_liner='异或和非零就全选，为零就去掉一个非零元素',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，选一个子序列，使其按位异或结果 ==非零==',
                 '求这样的最长子序列长度，不存在返回 0',
                 '示例：`[1,2,3]` → `2`，`[2,3,4]` → `3`；本视频：`[2,3,1]`'],
        quote='分类讨论：如果所有 nums[i] 都是 0，无法异或得到非零值，返回 0。如果 xorSum≠0，那么全选即可满足条件，返回 n。否则 xorSum=0，不能全选，去掉一个非零元素 x 后，就可以使异或和不为零，返回 n−1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三种情况：全 0 → 无解 `0`；异或和非 0 → 全选 `n`；异或和为 0 → `n-1`',
              '异或和为 0 时去掉非零 `x`，剩下的异或和就是 `0 ^ x = x`，非零',
              '最后一行用 `len(nums) - (xor_sum == 0)` 一句合并后两种情况'],
        after=[dict(heading='变形题', lines=['最长异或和不为 `0` 的连续子数组？', '最长异或和等于 `0` 的连续子数组？', '最长异或和等于 `0` 的子序列？', '灵神留给评论区的思考题'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：全 0 要先判，否则会错返回 `n - 1`',
                 '`xor` 来自 `operator`，`reduce(xor, nums)` 即所有元素异或',
                 '变形：最长异或和不为 0 / 等于 0 的连续子数组、异或和等于 0 的子序列'],
    ),
)
