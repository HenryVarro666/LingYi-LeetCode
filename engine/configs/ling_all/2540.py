CONFIG = dict(
    num=2540, title='最小公共值', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='双序列双指针 · 谁小移谁',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        i, n = 0, len(nums1)
        j, m = 0, len(nums2)
        while i < n and j < m:
            if nums1[i] == nums2[j]:
                return nums1[i]
            if nums1[i] < nums2[j]:
                i += 1
            else:
                j += 1
        return -1
''',
    call='Solution().getCommon([1,2,6,8,9], [3,4,6,10])',
    expect=6,
    views=[
        dict(type='array', var='nums1', pointers={'i': 'blue'}, label='nums1', h=200),
        dict(type='array', var='nums2', pointers={'j': 'pink'}, label='nums2', h=200),
        dict(type='text', fn=lambda S: f"比较 `nums1[{S['i']}] = {S['nums1'][S['i']]}` 与 `nums2[{S['j']}] = {S['nums2'][S['j']]}`" if 'i' in S and 'j' in S and S['i'] < S['n'] and S['j'] < S['m'] else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'i, n = 0': '`i` 指向 `nums1` 的当前最小值，`n = {n}`',
        'j, m = 0': '`j` 指向 `nums2` 的当前最小值，`m = {m}`',
        'while i < n': lambda S, B, r: ('两个数组都还有元素，继续比较' if S.i < S.n and S.j < S.m else '有一个数组用完了：没有公共值'),
        'nums1[i] == nums2[j]': lambda S, B, r: (f'`{S.nums1[S.i]}` == `{S.nums2[S.j]}`：两个数组都递增，==最先相等的就是最小公共值=='
                                                  if S.nums1[S.i] == S.nums2[S.j] else
                                                  f'`{S.nums1[S.i]}` != `{S.nums2[S.j]}`，还没找到公共值'),
        'nums1[i] < nums2[j]': lambda S, B, r: (f'`{S.nums1[S.i]} < {S.nums2[S.j]}`：较小的 `nums1[i]` 比 nums2 剩下的数都小，不可能是公共值' if S.nums1[S.i] < S.nums2[S.j] else
                                                  f'`{S.nums1[S.i]} > {S.nums2[S.j]}`：`nums2[j]` 比 nums1 剩下的数都小，不可能是公共值'),
        'i += 1': '排除 `nums1[i]`，`i` → {i}',
        'j += 1': '排除 `nums2[j]`，`j` → {j}',
        'return nums1[i]': '找到最小公共值 =={ret}==',
        'return -1': '某个数组走完仍无公共值 → `-1`',
    },
    cards=dict(
        one_liner='比较两个数组的最小值，较小的那个一定不是公共值，直接排除',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个非降序数组 `nums1`、`nums2`，返回最小的公共整数，没有则返回 `-1`',
                 '示例：`[1,2,3]` 和 `[2,4]` → `2`',
                 '本视频：`[1,2,6,8,9]` 和 `[3,4,6,10]` → `6`'],
        quote='找最小公共值，首先关注两个数组的最小值，也就是比较 x = nums1[0] 和 y = nums2[0] 的大小',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x < y`：x 也小于 `nums2` 其余元素，x 排除，问题变成后缀子问题',
              '`x > y`：同理排除 y；`x = y`：就是答案',
              '用下标 `i`、`j` 表示当前比较的两个数，不用真的删元素'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '两个数组都必须有序，才能用「最小值比较」排除',
                 '另一种写法：`min(set(nums1) & set(nums2), default=-1)`，更短但要 `O(n)` 额外空间',
                 '同类题：350 两个数组的交集 II、88 合并两个有序数组'],
    ),
)
