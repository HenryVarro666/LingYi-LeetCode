N1, N2 = [3, 3, 3, 3, 5, 5], [5, 5, 7, 7, 3, 3]

CONFIG = dict(
    num=3868, title='通过交换使数组相等的最小花费', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='哈希表记次数差 · 剩余的一半',
    tags=['灵神题单', '贪心与思维', '难度分 1579'],
    code='''
class Solution(object):
    def minCost(self, nums1, nums2):
        
        cnt = {}
        for v in nums1:
            cnt[v] = cnt.get(v, 0) + 1
        for v in nums2:
            cnt[v] = cnt.get(v, 0) - 1
        
        res = 0
        for v in cnt:
            if cnt[v] % 2 == 1:
                return -1
            if cnt[v] > 0:
                res += cnt[v] // 2

        return res
''',
    call=f'Solution().minCost({N1}, {N2})',
    expect=1,
    views=[
        dict(type='array', var='nums1', label='nums1', cell=80),
        dict(type='array', var='nums2', label='nums2', cell=80),
        dict(type='map', var='cnt', label='cnt[v]：nums1 中的次数 − nums2 中的次数', fmt=lambda k, v: f'{k}: {v:+d}'),
    ],
    watch=[('v', 'v', 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt = {}': '同组交换免费 → 不管顺序，只用哈希表 `cnt` 记==次数差==',
        'for v in nums1': '遍历 nums1：取下一个元素，次数 +1',
        'for v in nums2': '遍历 nums2：取下一个元素，次数 -1',
        'cnt[v] = cnt.get(v, 0) + 1': '`cnt[{v}] += 1` → `{cnt[v]}`（nums1 多了一个 {v}）',
        'cnt[v] = cnt.get(v, 0) - 1': '`cnt[{v}] -= 1` → `{cnt[v]}`（nums2 的 {v} 抵消一个）',
        'res = 0': '`res` 累计要从 nums1 换到 nums2 的个数',
        'for v in cnt': lambda S, B, r: ('所有元素都检查完了' if S.v == B.get('v') and S.v == list(S.cnt)[-1] else f'检查元素 `v = {S.v}`，次数差 `{S.cnt[S.v]}`'),
        'if cnt[v] % 2 == 1': lambda S, B, r: (f'`cnt[{S.v}] = {S.cnt[S.v]}` 是奇数：两边总次数为奇，无法分一半 → 返回 `-1`' if S.cnt[S.v] % 2 == 1
                                             else f'`cnt[{S.v}] = {S.cnt[S.v]}` 是偶数，抵消后剩下的成对，可以分一半'),
        'if cnt[v] > 0': lambda S, B, r: (f'`cnt[{S.v}] = {S.cnt[S.v]} > 0`：nums1 多出这么多个 `{S.v}`' if S.cnt[S.v] > 0
                                          else f'`cnt[{S.v}] = {S.cnt[S.v]} ≤ 0`：多出来的在 nums2 一侧，会被换过来，不另算'),
        'res += cnt[v] // 2': '把 nums1 多余的 `{v}` 的一半换过去：`res += {cnt[v]} // 2` → `{res}`',
        'return res': '最少需要 `{res}` 次跨数组交换',
    },
    cards=dict(
        one_liner='同组交换免费，只看次数差：多出来的一半要换过去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['同数组内交换免费，`nums1[i]` 与 `nums2[i]` 交换花费 1',
                 '求让两个数组变得相同的最小花费，做不到返回 `-1`',
                 '本视频：`nums1 = [3,3,3,3,5,5]`，`nums2 = [5,5,7,7,3,3]` → `1`'],
        quote='若某个元素在两个数组中出现次数之和为奇数，那么答案必然为-1，因为不可能使得两个数组中该元素出现的次数相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['同组交换免费 → 只关心每种元素在两数组中的次数',
              '某元素总次数为奇数 → 无法平分，返回 `-1`',
              'nums1 遍历 +1、nums2 遍历 -1，得到每种元素的次数差 `cnt[v]`',
              '`cnt[v] > 0`：nums1 多余的 `v` 要换走一半，累加 `cnt[v] // 2`'],
        result='`3` 多 2 个，换走一半，共 `1` 次；`7` 在 nums2 一侧，由同一次交换补齐 ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：用 `% 2 == 1` 判奇数；负数在 Python 里 `-3 % 2 == 1`，也能判到',
                 '只累加正的 `cnt[v] // 2`，因为两数组长度相同，负的一半恰好与之配对',
                 '对比灵神：灵神用 `Counter.subtract` 并给出 diff 的数学含义，这里手写两次遍历'],
    ),
)
