CONFIG = dict(
    num=2918, title='数组的最小相等和', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='下界分析 + 分类讨论', tags=['灵神题单', '难度分 1526'],
    code='''
class Solution:
    def minSum(self, nums1: List[int], nums2: List[int]) -> int:
        s1 = sum(max(x, 1) for x in nums1)
        s2 = sum(max(x, 1) for x in nums2)
        if s1 < s2 and 0 not in nums1 or \\
           s2 < s1 and 0 not in nums2:
            return -1
        return max(s1, s2)
''',
    call='Solution().minSum([3, 2, 0, 1, 0], [6, 5, 0])',
    expect=12,
    views=[
        dict(type='array', var='nums1', label='nums1', h=210, color=lambda S, i, v: 'orange' if v == 0 else None),
        dict(type='array', var='nums2', label='nums2', h=210, color=lambda S, i, v: 'orange' if v == 0 else None),
        dict(type='text', fn=lambda S: f"0 全换成 1 后：`s1 = {S['s1']}`" + (f"，`s2 = {S['s2']}`" if 's2' in S else '')),
    ],
    skip=['s2 < s1 and 0 not in nums2'],
    watch=[('s1', 's1', 'blue'), ('s2', 's2', 'pink')],
    captions={
        's1 = sum': '把 0 当成 1 求和：`s1 = {s1}`，这是 nums1 和的下界，只能增大',
        's2 = sum': '同理 `s2 = {s2}`',
        'if s1 < s2': '较小的和要补到较大的和，需要有 0 可调：`s1={s1}, s2={s2}`，nums1 有 0：{0 in nums1}，nums2 有 0：{0 in nums2} → {"无法补齐" if (s1 < s2 and 0 not in nums1) or (s2 < s1 and 0 not in nums2) else "可以补齐"}',
        'return -1': '较小的一边没有 0，和增大不了 → 返回 -1',
        'return max': '较小的一边把 0 调大即可补到较大的和 → 答案 `max({s1}, {s2})` = =={ret}==',
    },
    cards=dict(
        one_liner='0 先全当 1，再把较小的和补到较大的和',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个数组里的 0 都要换成严格正整数，使两数组和相等且最小',
                 '做不到返回 `-1`',
                 '示例：`[3,2,0,1,0]` 与 `[6,5,0]` → `12`'],
        quote='先把数组中的 0 替换成最小的正整数 1，然后再看下一步要怎么走。替换后……这是元素和的最小值，只能增大，不能减小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['替换后的和 `s1`、`s2` 是下界，只能往上加',
              '所以只能把较小的和增大到较大的和',
              '较小的一边没有 0 就无法增大 → `-1`；否则答案 `max(s1, s2)`'],
        summary=['`sum(max(x, 1) for x in nums)` 一行完成「0 变 1」求和',
                 '`s1 == s2` 时不会返回 -1，直接 `max`',
                 '判断「有没有 0」要看较小的那一边',
                 '示例 2：`[2,0,2,0]` 与 `[1,4]`，s1=6 > s2=5 且 nums2 无 0 → `-1`'],
    ),
)
