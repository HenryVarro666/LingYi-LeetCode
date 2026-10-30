def _tab(S):
    return f"每个元素贡献 `x × mul` 或 `x`；当前 mul = =={S['mul']}==" + ('（`mul ≤ 1`，直接加 x）' if S['mul'] <= 1 else '（`mul > 1`，乘上去更赚）') if 'mul' in S else ''


CONFIG = dict(
    num=3974, title='K 个元素的最大总和', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序不等式：大数配大 mul',
    tags=['贪心与思维', '排序不等式', '难度分 1263'],
    code='''
class Solution:
    def maxSum(self, nums: list[int], k: int, mul: int) -> int:
        nums.sort(reverse=True)
        ans = 0
        for x in nums[:k]:
            ans += x * mul if mul > 1 else x
            mul -= 1
        return ans
''',
    call='Solution().maxSum([6, 1, 2, 9, 4], 4, 3)',
    expect=45,
    views=[
        dict(type='array', var='nums', h=240, label='nums（降序；绿 = 已处理，蓝 = 当前，灰 = 不选）',
             color=lambda S, i, v: ('blue' if 'mul' in S and i == 3 - S['mul'] else 'green' if 'mul' in S and i < 3 - S['mul'] else None),
             dim=lambda S, i, v: i >= 4),
        dict(type='text', fn=_tab, h=80),
    ],
    watch=[('x', 'x', 'yellow'), ('mul', 'mul', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort': '降序排序：`{nums}`，前 `k` 个就是最大的 `k` 个',
        'ans = 0': '`ans` 累计总和',
        'for x in nums[:k]': '按从大到小处理：`x = {x}`',
        'ans += x * mul': lambda S, B, r: (f'`mul = {S.mul}`' + (f' > 1 → 乘上：`ans += {S.x}×{S.mul}` = {S.ans}' if S.mul > 1 else f' ≤ 1，乘了不会更大 → 直接加 `{S.x}`：ans = {S.ans}')),
        'mul -= 1': '`mul` 减 1 → {mul}：后面的数乘的倍数更小，所以大数先处理',
        'return ans': '最大总和 `{ans}`',
    },
    cards=dict(
        one_liner='取最大的 k 个数，大数先用大的 mul',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['从 `nums` 恰好选 `k` 个数，逐个处理，每个数可直接加，或乘当前 `mul` 再加',
                 '每处理一个数，`mul` 减 1，可能变成 0 或负数',
                 '本视频：`nums=[6,1,2,9,4]`，`k=4`，`mul=3` → `45`'],
        quote='根据排序不等式，取 nums 最大的 k 个数，按照从大到小的顺序依次操作。如果 mul≤1，则不与 mul 相乘。',
        quote_src='—— 灵茶山艾府题解',
        idea=['处理顺序决定每个数拿到的 `mul`，是递减序列：大数配大倍数，和最大（排序不等式）',
              '选数当然选最大的 `k` 个，所以降序排序后取前 `k` 个',
              '`mul ≤ 1` 时乘法不赚（`mul=1` 一样，`≤0` 反而亏），直接加 `x`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '判断条件是 `mul > 1`；`mul` 为负或 0 时乘上去会变小',
                 '`mul` 每处理一个元素都要减 1，无论乘没乘',
                 '写法二：用 `nlargest(k, nums)` 取前 k 大，可做到 `O(n log k)`'],
    ),
)
