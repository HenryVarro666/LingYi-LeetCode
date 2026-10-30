CONFIG = dict(
    num=870, title='优势洗牌', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='田忌赛马 · 排序 + 下标数组双指针',
    tags=['贪心与思维', '双序列配对', '难度分 1648'],
    code='''
class Solution:
    def advantageCount(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1.sort()

        n = len(nums1)
        idx = sorted(range(n), key=lambda i: nums2[i])

        ans = [0] * n
        left, right = 0, n - 1
        for x in nums1:
            if x > nums2[idx[left]]:
                ans[idx[left]] = x  # 用下等马比下等马
                left += 1
            else:
                ans[idx[right]] = x  # 用下等马比上等马
                right -= 1
        return ans
''',
    call='Solution().advantageCount([12,24,8,32], [13,25,32,11])',
    expect=[24, 32, 8, 12],
    views=[
        dict(type='array', var='nums1', label='nums1（已排序，从小到大逐个出场）', h=170,
             color=lambda S, i, v: 'green' if 'left' in S and i < S['left'] + len(S['nums1']) - 1 - S['right'] else None),
        dict(type='array', var='nums2', label='nums2（不能排序；蓝=最弱，粉=最强）', h=170,
             color=lambda S, i, v: ('blue' if i == S['idx'][S['left']] else 'pink' if i == S['idx'][S['right']] else None) if 'right' in S and S['left'] <= S['right'] else None),
        dict(type='array', var='idx', label='idx：nums2 下标按值从小到大排', h=170,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right')),
        dict(type='array', var='ans', label='ans：每个位置安排的马', h=160,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=['x', ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'nums1.sort()': '先把田忌的马从弱到强排好：`nums1 = {nums1}`',
        'idx = sorted': '`nums2` 不能排序，改排下标：`idx = {idx}`，`idx[0]` 指向齐威王最弱的马',
        'left, right = 0, n - 1': '`left` 指向齐威王最弱的马，`right` 指向最强的马',
        'for x in nums1': '田忌派出当前最弱的马 `x = {x}`',
        'if x > nums2': '`x = {x}` 比 齐威王最弱的 `nums2[idx[left]] = {nums2[idx[left]]}`？{"能赢" if x > nums2[idx[left]] else "赢不了"}',
        'ans[idx[left]] = x': '能赢就赢：`ans[{idx[left]}] = {x}`，这一分直接拿下',
        'left += 1': '齐威王最弱的马已被击败，`left` → {left}',
        'ans[idx[right]] = x': '连最弱的都赢不了：这匹马注定输，拿去送给最强的马：`ans[{idx[right]}] = {x}`',
        'right -= 1': '齐威王最强的马已有对手，`right` → {right}',
        'return ans': '所有马都已配对：`ans = {ans}`',
    },
    cards=dict(
        one_liner='田忌赛马：赢得了就赢，赢不了就拿最弱的马去送最强的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums1[i] > nums2[i]` 的个数叫 nums1 的优势',
                 '重排 `nums1`，让优势最大，返回任意一种排列',
                 '示例：`[12,24,8,32]` 对 `[13,25,32,11]` → `[24,32,8,12]`'],
        quote='如果它能比过齐威王的下等马，那这一分田忌直接拿下；如果它比不过齐威王的下等马，则用田忌的下等马比齐威王的上等马。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 nums1 当田忌的马、nums2 当齐威王的马，每次讨论田忌==最弱==的马',
              '能赢对手最弱的，就赢下来；赢不了，它不可能赢任何马，==白送给对手最强的==',
              'nums2 不能排序，所以排下标 `idx`，双指针在 idx 上走'],
        summary=['时间 `O(n log n)`，瓶颈在两次排序；空间 `O(n)`',
                 '易错：`nums2` 要保持原位，用下标数组 `idx` 排序，而不是直接排序 nums2',
                 '`>` 是严格大于，相等也算赢不了，要送去对最强的马',
                 '同类题：双序列配对（田忌赛马）都是排序后用双指针贪心'],
    ),
)
