def _top(S):
    if 'j' not in S or 'i' not in S:
        return ''
    n = len(S['nums1'])
    i, j, y = S['i'], S['j'], S['y']
    if i >= n:
        return f'`i = {i} == len(nums1)`：nums1 没有 `<= {y}` 的数了，后面的 j 更小，更不可能'
    return f"当前：`nums1[{i}] = {S['nums1'][i]}`，`nums2[{j}] = {y}`，距离 `j − i = {j - i}`，答案 ==`{S['ans']}`=="


CONFIG = dict(
    num=1855, title='下标对中的最大距离', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='双序列双指针 · 枚举 j、i 只增不减',
    tags=['滑动窗口与双指针', '双序列双指针', '难度分 1515'],
    code='''
class Solution:
    def maxDistance(self, nums1: List[int], nums2: List[int]) -> int:
        ans = i = 0
        for j, y in enumerate(nums2):
            while i < len(nums1) and nums1[i] > y:
                i += 1
            if i == len(nums1):
                break
            ans = max(ans, j - i)
        return ans
''',
    call='Solution().maxDistance([55,30,5,4,2], [100,20,10,10,5])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='nums1', label='nums1（非递增）', pointers={'i': 'blue'}, h=230,
             color=lambda S, i, v: 'blue' if 'j' in S and i == S['i'] else None,
             dim=lambda S, i, v: 'j' in S and i < S['i']),
        dict(type='array', var='nums2', label='nums2（非递增）', pointers={'j': 'pink'}, h=230,
             color=lambda S, i, v: 'pink' if 'j' in S and i == S['j'] else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'y', ('ans', 'ans', 'green')],
    captions={
        'ans = i = 0': '答案初始为 `0`（没有有效下标对就返回 0），`i = 0`',
        'for j, y': '枚举 `j`：`nums2[{j}] = {y}`。j 变大，y 只会变小，所以要求的最小 i 只会变大',
        'while i < len': lambda S, B, r: (f'`i = {S.i} == len(nums1)`，没有可用的 i 了，退出循环' if S.i >= len(S.nums1)
                                      else (f'`nums1[{S.i}] = {S.nums1[S.i]} > y = {S.y}`：==nums1[i] 太大==，不满足 `nums1[i] <= nums2[j]` → 增大 i'
                                            if S.nums1[S.i] > S.y else f'`nums1[{S.i}] = {S.nums1[S.i]} <= y = {S.y}`：满足条件，i 停在这里（最小的合法 i）')),
        'i += 1': '`i` 右移到 `{i}`：之前的 nums1 值都比 y 大，以后 y 更小，==永远不会再用到==',
        'if i == len': lambda S, B, r: ('`i == len(nums1)`：nums1 里已经没有数 `<= y` → ==break==，后面的 j 更不可能' if S.i == len(S.nums1)
                                         else '`i < len(nums1)`：找到了合法的 i，继续'),
        'ans = max': '距离 `j − i = {j} − {i} = {j - i}`；`ans = max({B.ans}, {j - i}) = {ans}`（j − i 为负也不影响，因为 ans 从 0 起）',
        'return ans': '最大距离是 `{ans}`',
    },
    cards=dict(
        one_liner='枚举 j，满足条件的最小 i 只会随 j 变大而变大',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个非递增数组，下标对 `(i, j)` 满足 `i <= j` 且 `nums1[i] <= nums2[j]` 时有效',
                 '距离是 `j − i`，求最大距离，没有有效对就返回 `0`',
                 '示例：`[55,30,5,4,2]`、`[100,20,10,10,5]` → `2`'],
        quote='枚举 j，随着 j 的变大，nums2[j] 变小，满足要求的最小的 i 随之变大。所以可以用双指针做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['固定 j，想让距离最大，就要 ==i 尽量小==，即最小的、满足 `nums1[i] <= nums2[j]` 的 i',
              'j 变大后 `nums2[j]` 变小，之前不合格的 i 仍不合格，所以 i 不用回头',
              '每个 j 都用 `j − i` 更新答案'],
        summary=['时间 `O(n+m)`：虽是二重循环，但 i 最多自增 n 次',
                 '`if i == len(nums1): break` 不能漏，否则 `nums1[i]` 会越界',
                 '不用担心 `j − i < 0`：答案从 0 开始取最大，不影响结果',
                 '本题 nums1、nums2 都非递增，才能让双指针单调'],
    ),
)
