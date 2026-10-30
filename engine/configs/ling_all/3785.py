def _bad(S, i, j, v):
    return i < 2 and S['nums'][j] == S['forbidden'][j]

CONFIG = dict(
    num=3785, title='避免禁用值的最小交换次数', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='坏列计数 · 相邻不同',
    tags=['灵神题单', '难度分 2052'],
    code='''
class Solution:
    def minSwaps(self, nums: List[int], forbidden: List[int]) -> int:
        n = len(nums)
        total = Counter(nums) + Counter(forbidden)
        if any(c > n for c in total.values()):
            return -1

        same = Counter(x for x, y in zip(nums, forbidden) if x == y)
        k = same.total()
        mx = max(same.values(), default=0)
        return max((k + 1) // 2, mx)
''',
    call='Solution().minSwaps([4,6,6,5], [4,6,5,5])',
    expect=2,
    views=[
        dict(type='grid', var=lambda S: [S['nums'], S['forbidden']], label='两行数组排成 2×n 矩阵（红 = 坏列）', h=210,
             rows=['nums', 'forb'], cols=lambda S: list(range(len(S['nums']))),
             color=lambda S, i, j, v: 'red' if S['nums'][j] == S['forbidden'][j] else None),
        dict(type='map', var='total', label='total：nums 与 forbidden 里每个数的总次数（不能超过 n）', h=170),
        dict(type='map', var='same', label='same：坏列上每个数出现几次', h=170),
        dict(type='text', size=30, fn=lambda S: (
            f"坏列数 `k = {S['k']}`，最多的数出现 `mx = {S['mx']}` 次" if 'mx' in S else (f"坏列数 `k = {S['k']}`" if 'k' in S else ''))),
    ],
    watch=['n', ('k', 'k', 'blue'), ('mx', 'mx', 'orange')],
    captions={
        'n = len': '列数 `n = {n}`',
        'total = Counter': '统计每个数在两个数组里的总次数：`{total}`',
        'if any': lambda S, B, r: ('`total` 里有数的次数 > n：鸽巢原理，必有一整列都是它 → 无解' if any(c > S.n for c in S.total.values())
                                  else '没有数的总次数超过 `n = %d`：一定有解，继续' % S.n),
        'same = Counter': '只统计「坏列」（`nums[i] == forbidden[i]`）上的数：`{dict(same)}`',
        'k = same.total': '坏列一共 `k = {k}` 个',
        'mx = max': '坏列里最多的那个数出现 `mx = {mx}` 次：它们必须各用一次操作',
        'return max': '最少操作 `max(ceil(k/2), mx)` = `max({(k + 1) // 2}, {mx})` = =={ret}==：两个下界取较大者（成对换 vs 最多的值）',
    },
    cards=dict(
        one_liner='把「坏列」数清楚：两两不同的互换，最多的数决定下限',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['两个等长数组 `nums`、`forbidden`，每次交换 `nums` 里两个下标的值',
                 '要让每个 `nums[i]` 都不等于 `forbidden[i]`，求最少交换次数，无解返回 -1',
                 '示例：`[4,6,6,5]`, `[4,6,5,5]` → `2`'],
        quote='把坏列第一行的元素记在数组 a 中，问题变成：每次操作，删除 a 中的至多两个不同元素。删除所有元素，最少要操作多少次？',
        quote_src='—— 灵茶山艾府题解',
        idea=['某个数在两数组中总共超过 `n` 次，必有一整列相同 → 无解',
              '否则优先交换两个不同值的坏列，一次消两个',
              '剩下的坏列去找「两个数都不等于它」的好列互换',
              '答案 `max(ceil(k/2), mx)`：`k` 为坏列数，`mx` 为最多的值的坏列数'],
        after=[dict(heading='为什么取 max', lines=['每次操作最多消掉两个不同值的坏列：至少 `ceil(k/2)` 次', '同一个值的坏列不能互相抵消，至少 `mx` 次', '例：`1,1,1,2,2,3` → `max(3, 3) = 3`，先换同值再换会多一次'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：先判无解，`total` 要把两个数组的计数加起来',
                 '`same.total()` 是 Counter 的总和（Python 3.10+），无坏列时 `max(..., default=0)` 防空',
                 '同类题：相邻不同类贪心（题单 §1.8），如 1953、2856'],
    ),
)
