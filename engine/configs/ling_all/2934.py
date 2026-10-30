def _hit(S, i):
    return 'x' in S and 'y' in S and S['x'] == S['nums1'][i] and S['y'] == S['nums2'][i]


def _txt(S, B):
    if 'last1' not in S:
        return '两种情况：不交换末位 / 交换末位，分别数必须交换的下标'
    return f"目标：nums1 末位 `{S['last1']}`，nums2 末位 `{S['last2']}`，已交换 ==`{S['res']}`== 次"


CONFIG = dict(
    num=2934, title='最大化数组末位元素的最少操作次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 末位交换与否', tags=['灵神题单', '难度分 1803'],
    code='''
class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        def f(last1: int, last2: int) -> int:
            res = 0
            for x, y in zip(nums1, nums2):
                if x > last1 or y > last2:
                    if y > last1 or x > last2:
                        return inf
                    res += 1
            return res
        ans = min(f(nums1[-1], nums2[-1]), f(nums2[-1], nums1[-1]))
        return ans if ans < inf else -1
''',
    call='Solution().minOperations([2,3,4,5,9], [8,8,4,4,4])',
    expect=2,
    skip=['for x, y in zip'],
    views=[
        dict(type='array', var='nums1', label='nums1', h=220, cell=100,
             color=lambda S, i, v: 'yellow' if _hit(S, i) else None),
        dict(type='array', var='nums2', label='nums2', h=220, cell=100,
             color=lambda S, i, v: 'yellow' if _hit(S, i) else None),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=[('last1', 'last1', 'blue'), ('last2', 'last2', 'pink'), ('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('res', 'res', 'green'), ('ans', 'ans', 'green')],
    captions={
        'res = 0': '情况：末位{"不交换" if last1 == nums1[-1] else "交换"}。`res` 统计必须交换的下标个数，末位目标 `{last1}`、`{last2}`',
        'if x > last1 or y > last2': lambda S, B, r: (f'`{S.x} > {S.last1}` 或 `{S.y} > {S.last2}`：不换就超过末位 → ==必须交换==' if (S.x > S.last1 or S.y > S.last2)
                                                       else f'`{S.x} ≤ {S.last1}` 且 `{S.y} ≤ {S.last2}`：不换也合法，不用动'),
        'if y > last1 or x > last2': lambda S, B, r: (f'换了以后 `{S.y} > {S.last1}` 或 `{S.x} > {S.last2}`：交换也不行 → ==这种情况无解，返回 inf=='
                                                       if (S.y > S.last1 or S.x > S.last2) else f'换了以后 `{S.y} ≤ {S.last1}` 且 `{S.x} ≤ {S.last2}`：合法'),
        'return inf': '无法满足 → 返回 `inf`',
        'res += 1': '这个下标必须交换，`res` = =={res}==',
        'return res': '这种情况共需交换 =={res}== 次',
        'return ans if': lambda S, B, r: ('`ans` 是 inf：两种情况都不行 → 返回 `-1`' if S.ans == inf else f'`ans = {S.ans}` 有限 → 直接返回'),
    },
    cards=dict(
        one_liner='末位交换与否只有两种，其余下标被强制决定',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可交换同一下标上的 `nums1[i]` 与 `nums2[i]`',
                 '要让两个数组的末位都成为各自的最大值，求最少交换次数，无解返回 `-1`',
                 '示例：`[2,3,4,5,9]`、`[8,8,4,4,4]` → `2`'],
        quote='对于每种情况，从 i=0 枚举到 i=n-2，一旦发现 nums1[i] > nums1[n-1] 或 nums2[i] > nums2[n-1]，就必须执行交换操作。',
        quote_src='—— 灵茶山艾府题解',
        idea=['总共就两种情况：末位 `(nums1[-1], nums2[-1])` 不交换，或者交换',
              '末位定了，其余每个下标超标就==必须换==，不超标就不用换（换了不会更优）',
              '换完还超标 → 这种情况无解；两种都无解返回 `-1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：不用交换时不要多换，换一次就多一次代价',
                 '易错：两种情况取最小，两种都是 `inf` 才返回 `-1`',
                 '代码把末位也放进循环里，对末位自己恒不超标，不影响结果'],
    ),
)
