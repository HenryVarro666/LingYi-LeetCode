def _top(S):
    if 'j' not in S or 'i' not in S:
        return ''
    n = len(S['nums2'])
    i, j = S['i'], S['j']
    return f"nums1[{i}] = {S['nums1'][i]}，j 指向第一个放不下的位置 `{j}`，最远可配对的下标是 `j − 1 = {j - 1}`，距离 `j − i − 1 = {j - i - 1}`，res ==`{S['res']}`=="


CONFIG = dict(
    num=1855, title='下标对中的最大距离', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='双序列双指针 · 求每个 nums1[i] 对应的最远 j',
    tags=['滑动窗口与双指针', '双序列双指针', '难度分 1515'],
    code='''
class Solution(object):
    def maxDistance(self, nums1, nums2):

        j = 0
        res = 0
        for i in range(len(nums1)):
            while j < len(nums2) and nums1[i] <= nums2[j]:
                j += 1
            res = max(res, j - i - 1)
            if j == len(nums2):
                break
        
        return res
''',
    call='Solution().maxDistance([30,29,19,5], [25,25,25,25,25])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: _top(S) if 'i' in S and 'j' in S else '', size=24),
        dict(type='array', var='nums1', label='nums1', pointers={'i': 'blue'}, h=230,
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None),
        dict(type='array', var='nums2', label='nums2（j 只会往后走）', pointers={'j': 'pink'}, h=230,
             color=lambda S, i, v: 'green' if 'i' in S and 'j' in S and i < S['j'] and S['nums1'][S['i']] <= v else None,
             dim=lambda S, i, v: 'j' in S and 'i' in S and i < S['i']),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'j = 0': '`j` 是对 nums1[i] 向后扩展的指针：==满足 nums2[j] >= nums1[i] 的最大下标 + 1==',
        'res = 0': '`res` 记录最大距离，没有有效对时为 `0`',
        'for i in': '处理 `nums1[{i}] = {nums1[i]}`：由于 nums1 非递增，上一个 i 能到的位置它也一定能到，==j 不用回头==',
        'while j <': lambda S, B, r: (f'`j = {S.j} == len(nums2)`：已经走到头，停止' if S.j >= len(S.nums2)
                                      else (f'`nums1[{S.i}] = {S.nums1[S.i]} <= nums2[{S.j}] = {S.nums2[S.j]}`：能配对 → j 继续后移' if S.nums1[S.i] <= S.nums2[S.j]
                                            else f'`nums1[{S.i}] = {S.nums1[S.i]} > nums2[{S.j}] = {S.nums2[S.j]}`：配不上了，j 停下')),
        'j += 1': '`nums2[{j-1}]` 可以配对，`j` → {j}',
        'res = max': '最远可配对下标是 `j − 1 = {j-1}`，距离 `j − i − 1 = {j - i - 1}`；`res = max({B.res}, {j - i - 1}) = {res}`',
        'if j == len': lambda S, B, r: ('`j == len(nums2)`：nums2 已全部扫完，后面的 i 不会更远 → break' if S.j == len(S.nums2)
                                        else '`j` 还没到头，继续下一个 i'),
        'return res': '最大距离是 `{res}`',
    },
    cards=dict(
        one_liner='对每个 nums1[i]，找最远的 j；j 只前进不后退',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个非递增数组，`i <= j` 且 `nums1[i] <= nums2[j]` 的下标对 `(i, j)` 有效',
                 '求有效下标对中 `j − i` 的最大值，没有则为 `0`',
                 '本视频：`[30,29,19,5]`、`[25,25,25,25,25]` → `2`'],
        quote='对于nums1[index + 1]而言，首先可以确定的是由于nums1[index] >= nums1[index + 1]，因此必然有nums2[p[index]] >= nums1[index] >= nums1[index + 1]，此时求解p[index + 1]就只需在p[index]的基础上继续向后遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['设 `p[i]` 为满足 `nums2[p] >= nums1[i]` 的最大下标',
              'nums1 递减，`p[i+1]` 一定不小于 `p[i]`，==接着上次的位置往后找==',
              '均摊 `O(1)` 求出所有 p，边求边用 `p − i` 更新答案'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '循环结束时 `j` 指向第一个不满足的位置，所以最远下标是 `j − 1`，距离为 `j − i − 1`',
                 '若 `nums1[i] > nums2[i]`，则 `j − i − 1` 为负，被 `res = 0` 兜住',
                 '`j == len(nums2)` 时提前 break，之后的 i 不会得到更大距离',
                 '对比灵神：灵神枚举 nums2 的 j、移动 nums1 的 i；yiduobo 枚举 nums1 的 i、移动 j'],
    ),
)
