CONFIG = dict(
    num=1775, title='通过最少操作次数使数组的和相等', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='按最大变化量从大到小贪心', tags=['灵神题单', '难度分 1850'],
    code='''
class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        if 6 * len(nums1) < len(nums2) or 6 * len(nums2) < len(nums1):
            return -1  # 优化
        d = sum(nums2) - sum(nums1)  # 数组元素和的差，我们要让这个差变为 0
        if d < 0:
            d = -d
            nums1, nums2 = nums2, nums1  # 统一让 nums1 的数变大，nums2 的数变小
        ans = 0
        # 统计每个数的最大变化量（nums1 的变成 6，nums2 的变成 1）
        cnt = Counter(6 - x for x in nums1) + Counter(x - 1 for x in nums2)
        for i in range(5, 0, -1):  # 从大到小枚举最大变化量 5 4 3 2 1
            if i * cnt[i] >= d:  # 可以让 d 变为 0
                return ans + (d + i - 1) // i
            ans += cnt[i]  # 需要所有最大变化量为 i 的数
            d -= i * cnt[i]
''',
    call='Solution().minOperations([3,1], [4,4,5,3])',
    expect=3,
    views=[
        dict(type='array', var='nums1', label='nums1（要变大：变成 6）', h=150,
             color=lambda S, i, v: 'green' if 'cnt' in S else None),
        dict(type='array', var='nums2', label='nums2（要变小：变成 1）', h=150,
             color=lambda S, i, v: 'orange' if 'cnt' in S else None),
        dict(type='map', var=lambda S: {k: S['cnt'][k] for k in range(5, 0, -1)} if 'cnt' in S else {},
             fmt=lambda k, v: f'变化 {k}：{v} 个', label='cnt：最大变化量 → 个数', h=230),
        dict(type='text', fn=lambda S: (f"还差 `d` = =={S['d']}==，已用 `ans` = {S['ans']} 次操作" if 'ans' in S and 'd' in S else '')),
    ],
    watch=[('d', 'd if "d" in dir() else None', 'pink'), ('i', 'i if "i" in dir() else None', 'blue'), ('ans', 'ans if "ans" in dir() else None', 'green')],
    captions={
        '6 * len(nums1)': '长度 `{len(nums1)}` 和 `{len(nums2)}`：最大和 `6×长度` 都够不到另一边的最小和（=长度）才无解，这里 `{6*len(nums1)}`、`{6*len(nums2)}` 没问题',
        'd = sum(nums2)': '和的差 `d = {sum(nums2)} - {sum(nums1)} = {d}`，目标把它变成 0',
        'ans = 0': '`ans` 记录已经改了几个数',
        'if d < 0': '`d = {d}`：{"nums1 的和更小" if d >= 0 else "nums1 的和更大"}，需要保证 nums1 是和小的那个',
        'd = -d': '`nums1` 的和更大，取反并交换，统一让 `nums1` 变大、`nums2` 变小：`d = {d}`',
        'cnt = Counter': '每个数的最大变化量：`nums1` 变 6 得 `6-x`，`nums2` 变 1 得 `x-1`；统计得 `cnt = {dict(cnt)}`',
        'if i * cnt[i] >= d': '变化量 `{i}` 有 `{cnt[i]}` 个，最多能减 `{i}×{cnt[i]} = {i*cnt[i]}`，还差 `d = {d}`：{"够了" if i * cnt[i] >= d else "不够，全部用上"}',
        'return ans + (d + i - 1) // i': '剩余 `d={d}`，每次最多减 `{i}`，向上取整 `{(d + i - 1) // i}` 次，共 =={ret}== 次',
        'ans += cnt[i]': '这 `{cnt[i]}` 个数全改，`ans` = {ans}',
        'd -= i * cnt[i]': '差距减少 `{i}×{cnt[i]}`，`d` → =={d}==',
    },
    cards=dict(
        one_liner='先改变化量最大的数，一步减得最多',
        complexity='时间 `O(n+m)`，空间 `O(C)`，`C=6`',
        problem=['两个数组元素都在 `1~6`，每次操作可把任意一个数改成 `1~6` 的任意值',
                 '求使两数组和相等的最少操作次数，不可能返回 `-1`',
                 '示例：`[6,6]` 与 `[1]` → `3`'],
        quote='不妨设 nums1 的元素和小于 nums2 的元素和，那么 nums1 的元素需要变大，nums2 的元素需要变小。计算每个元素的最大变化量，从大到小枚举。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和小的数组把数改成 6，和大的数组把数改成 1：==每个数有个最大变化量 0~5==',
              '统计到 `cnt[0..5]`，从 5 往下枚举，变化量大的先用',
              '某档够填满差距时，只需 `ceil(d / i)` 个'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '易错：开头先判无解，`6n < m` 或 `6m < n`；有解就一定能拉平',
                 '易错：向上取整写成 `(d + i - 1) // i`',
                 '同类：2333、2611 这类「先选最大收益」的贪心'],
    ),
)
