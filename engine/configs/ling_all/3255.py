CONFIG = dict(
    num=3255, title='长度为 K 的子数组的能量值 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='统计连续上升段长度',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1595'],
    code='''
class Solution:
    def resultsArray(self, nums: List[int], k: int) -> List[int]:
        ans = [-1] * (len(nums) - k + 1)
        cnt = 0
        for i, x in enumerate(nums):
            cnt = cnt + 1 if i == 0 or x == nums[i - 1] + 1 else 1
            if cnt >= k:
                ans[i - k + 1] = x
        return ans
''',
    call='Solution().resultsArray([1,2,3,4,3,2,5], 3)',
    expect=[3, 4, -1, -1, -1],
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, window=('i - cnt + 1', 'i'), h=240,
             label='nums（框 = 以 i 结尾的连续 +1 段）',
             color=lambda S, i, v: 'green' if 'cnt' in S and 'i' in S and S['cnt'] >= S['k'] and i == S['i'] else None),
        dict(type='array', var='ans', h=240, label='ans（-1 表示这个窗口不合格）',
             color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink'), ('cnt', 'cnt', 'cyan'), 'k'],
    captions={
        'ans = [-1]': '长度为 `k` 的窗口一共 `n - k + 1 = {len(ans)}` 个，默认都是 `-1`',
        'cnt = 0': '`cnt`：以当前元素结尾的「连续 +1」段长度',
        'cnt = cnt + 1 if': lambda S, B, r: ('第一个数，`cnt` = 1' if S.i == 0 else
                                           f'`{S.x}` 等于 `{S.nums[S.i-1]} + 1` → 连续，`cnt` = {S.cnt}'
                                           if S.x == S.nums[S.i-1] + 1 else
                                           f'`{S.x}` 不等于 `{S.nums[S.i-1]} + 1` → 连续性断了，`cnt` 重置为 ==1=='),
        'if cnt >= k': lambda S, B, r: (f'`cnt = {S.cnt} ≥ k = {S.k}` → 以 `{S.x}` 结尾的长为 k 的窗口合格'
                                       if S.cnt >= S.k else f'`cnt = {S.cnt} < k = {S.k}` → 凑不够 k 个，窗口不合格'),
        'ans[i - k + 1] = x': '窗口 `[{i-k+1}, {i}]` 合格，最大值就是末尾 `{x}`：`ans[{i-k+1}] = {x}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='找连续 +1 的段，段内长度够 k 的窗口，能量值就是窗口末尾',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['能量值：窗口内元素依次连续且上升 → 最大元素，否则 `-1`',
                 '求所有长为 `k` 的子数组的能量值，返回长 `n-k+1` 的数组',
                 '示例：`[1,2,3,4,3,2,5], k=3` → `[3,4,-1,-1,-1]`'],
        quote='找连续上升的段。如果段长至少是 k，那么这段中的所有长为 k 的子数组都是符合要求的，子数组的最后一个元素是最大的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用计数器 `cnt` 记录以 `nums[i]` 结尾的连续 +1 段长度',
              '`cnt >= k`：窗口 `[i-k+1, i]` 合格，能量值 `nums[i]`',
              '连续性断开就把 `cnt` 置为 1（元素自己算一个）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：要「连续 +1」，不是只要递增；`[2,2,2]` 里相等也要重置',
                 '答案下标是窗口左端点 `i - k + 1`，不是 `i`',
                 '这是分组循环题单里的题，灵神这里用计数器写法'],
    ),
)
