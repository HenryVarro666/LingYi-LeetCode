N1, N2 = [1, 1, 1, 1, 1, 2], [2, 2, 2, 2, 2, 1]


def _txt(S):
    if 'diff' not in S:
        return '同数组内交换免费 → 数组当==无序集合==；只关心每个数在两边的次数差'
    pos = sum(d for d in S['diff'].values() if d > 0)
    if 'ans' not in S:
        return '`diff[x]` = x 在 nums1 的次数 − 在 nums2 的次数；要让它全变成 0'
    return f'正的 diff 之和 = `{pos}`；每交换一次，正的 diff 之和减 2'


CONFIG = dict(
    num=3868, title='通过交换使数组相等的最小花费', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='等价转化 · 出现次数之差',
    tags=['灵神题单', '难度分 1579'],
    code='''
class Solution:
    def minCost(self, nums1: List[int], nums2: List[int]) -> int:
        diff = Counter(nums1)
        diff.subtract(nums2)

        ans = 0
        for d in diff.values():
            if d % 2:
                return -1
            if d > 0:
                ans += d
        return ans // 2
''',
    call=f'Solution().minCost({N1}, {N2})',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='nums1', label='nums1', cell=80),
        dict(type='array', var='nums2', label='nums2', cell=80),
        dict(type='map', var='diff', label='diff[x] = nums1 中 x 的次数 − nums2 中 x 的次数', fmt=lambda k, v: f'{k}: {v:+d}'),
    ],
    watch=[('d', 'd', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'diff = Counter': '先统计 nums1 中每个数的次数：`{dict(diff)}`',
        'diff.subtract': '再减去 nums2 的次数 → `diff = {dict(diff)}`；正数 = nums1 多出来的，负数 = nums2 多出来的',
        'ans = 0': '`ans` 累加所有==正==的 diff',
        'for d in diff.values()': lambda S, B, r: (f'取一个数的次数差 `d = {S.d}`' if S.get('d') != B.get('d') or 'd' not in B
                                                  else '所有数都看完了'),
        'if d % 2': lambda S, B, r: (f'`d = {S.d}` 是奇数：这个数总个数是奇数，无法均分 → 返回 `-1`' if S.d % 2
                                     else f'`d = {S.d}` 是偶数，总个数为偶数，可以均分'),
        'if d > 0': lambda S, B, r: (f'`d = {S.d} > 0`：nums1 多出 `{S.d}` 个，要换走' if S.d > 0
                                     else f'`d = {S.d} ≤ 0`：这是 nums2 多出来的部分，已被正的部分抵消，不用再数'),
        'ans += d': '`ans += {d}` → `{ans}`：正的 diff 之和',
        'return ans // 2': '每次交换让正的 diff 之和减 2，所以交换次数 = `{ans} // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='组内交换免费，数组就是无序集合；数一数每个数要换几个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['同一数组内任意交换免费，跨数组交换同一下标花费 1',
                 '求让 `nums1` 和 `nums2` 相同的最小花费，做不到返回 `-1`',
                 '本视频：`nums1 = [1,1,1,1,1,2]`，`nums2 = [2,2,2,2,2,1]` → `2`'],
        quote='由于在同一个数组内交换是免费的，我们可以把数组视作无序集合，里面的元素是什么顺序都可以。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每种数的总次数必须是偶数，否则无法均分',
              '`diff[x]` = x 在 A 中的次数减在 B 中的次数，要让它全变成 0',
              '`diff` 总和为 0，正数之和 = 负数绝对值之和；一次交换让正数之和减 2',
              '所以答案 = 正的 diff 之和 ÷ 2'],
        result='`diff = {1: 4, 2: -4}`，正数之和 4，交换 `4 // 2 = 2` 次 ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`diff` 奇数就返回 `-1`，不是看 nums1 或 nums2 单边的次数',
                 '只累加正的 diff，再除以 2；负的部分是同一批交换的另一半',
                 '同类思路：把“可任意重排”的对象当成集合/计数来比较'],
    ),
)
