CONFIG = dict(
    num=3164, title='优质数对的总数 II', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='计数 · 枚举 v×k 的倍数',
    tags=['灵神题单', '数论', '难度分 1777'],
    code='''
class Solution(object):
    def numberOfPairs(self, nums1, nums2, k):

        ma = max(nums1)

        freq1 = Counter(nums1)
        freq2 = Counter(nums2)
        res = 0
        for v, f in freq2.items():
            v *= k
            for x in range(v, ma + 1, v):
                res += freq1[x] * f
        
        return res
''',
    call='Solution().numberOfPairs([6,12,12,3,5], [1,2,2], 3)',
    expect=10,
    views=[
        dict(type='map', var='freq1', label='freq1：nums1 里每个数出现几次', h=170),
        dict(type='map', var='freq2', label='freq2：nums2 里每个数出现几次', h=150),
        dict(type='text', h=100, fn=lambda S: (f"`nums2` 的 `{S['v'] // S['k']}` × k = ==`{S['v']}`==，它的倍数 `{S['v']}, {2*S['v']}, …` 都能配对，每个出现 `{S['f']}` 次的 v 都要算" if 'f' in S and 'x' not in S and S.get('v') else (f"倍数 `x = {S['x']}`：`freq1[{S['x']}]` = {S['freq1'].get(S['x'], 0)} 个 nums1，配 `{S['f']}` 个 nums2 → +`{S['freq1'].get(S['x'], 0) * S['f']}` 对" if 'x' in S and 'f' in S else ''))),
    ],
    watch=['ma', 'v', 'f', 'x', ('res', 'res', 'green')],
    captions={
        'ma = max': 'nums1 最大值 `ma = {ma}`：倍数只需要枚举到它',
        'freq1 = Counter': '数值相同的 `nums1[i]` 能配的对数一样，先合并计数：`freq1` = {dict(freq1)}',
        'freq2 = Counter': '`nums2` 也合并计数：`freq2` = {dict(freq2)}',
        'res = 0': '`res` 累计优质数对',
        'for v, f in': '取 `nums2` 里一种数 `v = {v}`，出现 `f = {f}` 次',
        'v *= k': '`nums1[i]` 要被 `v×k` 整除，所以先把 v 乘上 k：`v = {v}`',
        'for x in range': '以 `{v}` 为步长，枚举它的倍数 `x = {x}`',
        'res += freq1': '`freq1[{x}]` = {freq1[x]} 个，每个配 {f} 个 → `res` = =={res}==',
        'return res': '优质数对一共 `{res}` 对',
    },
    cards=dict(
        one_liner='先合并相同数值，再按 v×k 的倍数去找 nums1',
        complexity='时间 `O(n + m + M log m)`，空间 `O(n + m)`',
        problem=['`nums1[i]` 能被 `nums2[j] * k` 整除，则 `(i, j)` 是优质数对',
                 '求优质数对总数；n、m 达 10^5，数值达 10^6',
                 '示例：`[1,2,4,12]`，`[2,4]`，`k=3` → `2`'],
        quote='ma // 1 + ma // 2 + … + ma // m，这个式子的时间复杂度是 ma * log(m)，在本题的数据规模下是完全够用的。',
        quote_src='—— yiduobo 题解原文',
        idea=['数值相同的数可以合并：`freq1`、`freq2` 记次数',
              '对 `freq2` 里的 v，先 `v *= k`，nums1 里等于 v 的倍数的数都能配对',
              '每个倍数 x 贡献 `freq1[x] * f` 对；最坏情况下就是调和级数'],
        summary=['`freq1[x]` 是 `Counter`，没出现的键读出来是 0，不用 if',
                 '一定要先 `v *= k` 再枚举倍数，否则会漏掉 k 的约束',
                 '这题的第 I 题数据小，同样的代码也能过',
                 '对比灵神：灵神方法一枚举 nums1 的因子，yiduobo 直接用方法二的倍数枚举'],
    ),
)
