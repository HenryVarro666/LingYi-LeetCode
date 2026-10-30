CONFIG = dict(
    num=3818, title='移除前缀使数组严格递增', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='倒序找最长严格递增后缀', tags=[],
    code='''
class Solution:
    def minimumPrefixLength(self, nums: List[int]) -> int:
        for i in range(len(nums) - 1, 0, -1):
            if nums[i - 1] >= nums[i]:
                return i  # 移除前缀 [0, i-1]，长度为 i
        return 0
''',
    call='Solution().minimumPrefixLength([3,1,5,6,2,7,8,9,10])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=260,
             window=('i', 'len(nums) - 1'),
             color=lambda S, k, v: ('pink' if 'i' in S and k == S['i'] - 1 else None)),
        dict(type='text', fn=lambda S: f"nums[{S['i']-1}] = {S['nums'][S['i']-1]}  vs  nums[{S['i']}] = {S['nums'][S['i']]}" if 'i' in S and S['i'] > 0 else '', h=100),
    ],
    watch=['i'],
    captions={
        'for i in range': '从最后一个下标往前扫，每次比较 `nums[i-1]` 和 `nums[i]`',
        'if nums[i - 1] >= nums[i]': lambda S, B, r: (f'`nums[{S.i-1}] = {S.nums[S.i-1]}` ≥ `nums[{S.i}] = {S.nums[S.i]}` → 断开了' if S.nums[S.i-1] >= S.nums[S.i] else f'`{S.nums[S.i-1]} < {S.nums[S.i]}` → 严格递增，继续往前'),
        'return i': '`[{i}, n-1]` 是最长严格递增后缀；它前面的 `[0, {i}-1]` 必须删 → 长度 =={i}==',
        'return 0': '一路没断开，整个数组已严格递增 → 不用删，返回 =={ret}==',
    },
    cards=dict(
        one_liner='保留尽量长的严格递增后缀，前面全删',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['必须恰好移除一个前缀（可为空），使剩下的数组严格递增', '求被移除前缀的最小长度', '示例：`[1,-1,2,3,3,4,5]` → `4`；本视频：`[3,1,5,6,2,7,8,9,10]`'],
        quote='倒序遍历 nums，如果发现 nums[i-1] >= nums[i]，那么前缀 [0, i-1] 必须删除，长度为 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删前缀 = 留后缀，前缀越短后缀越长', '从后往前找到第一个 `nums[i-1] >= nums[i]` 的位置 `i`', '`nums[i-1]` 无论如何都不能和 `nums[i]` 共存，所以前缀 `[0, i-1]` 都要删'],
        summary=['时间 `O(n)`，空间 `O(1)`', '易错点：是严格递增，相等也要断开（`>=`）', '循环到 `i = 1` 为止，`i = 0` 时没有前一个元素', '全程没断开就返回 0'],
    ),
)
