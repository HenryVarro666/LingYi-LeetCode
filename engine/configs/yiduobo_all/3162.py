CONFIG = dict(
    num=3162, title='优质数对的总数 I', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='频次统计 + 枚举倍数',
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
    call='Solution().numberOfPairs([1,2,4,12], [2,4], 3)',
    expect=2,
    views=[
        dict(type='array', var='nums1', label='nums1（绿色 = 当前枚举到的倍数 x）', h=150,
             color=lambda S, i, v: 'green' if 'x' in S and v == S['x'] else None),
        dict(type='map', var='freq1', label='freq1', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='map', var='freq2', label='freq2', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='text', h=80, size=30,
             fn=lambda S: f"枚举 `{S['v']}` 的倍数：当前 `x = {S['x']}`，累计 `res = {S['res']}`" if 'x' in S and 'v' in S else ''),
    ],
    watch=['ma', 'v', 'f', 'x', ('res', 'res', 'green')],
    captions={
        'ma = max': '`nums1` 的最大值 `ma = {ma}`：倍数超过它就不可能出现',
        'freq1 = ': '`freq1` 统计 `nums1` 每个数出现几次',
        'freq2 = ': '`freq2` 统计 `nums2` 每个数出现几次：相同的数能配成的对数一样，合并处理',
        'for v, f in freq2': lambda S, B, r: (f'`freq2` 全部处理完，累计 `res = {S.res}`' if ('v' in B and S.v == B.v and S.f == B.f) else f'取 `nums2` 里的数 `v = {S.v}`，它出现了 `f = {S.f}` 次'),
        'v *= k': '要整除 `v * k`，所以 `nums1` 里的数必须是 `v × k = {v}` 的倍数',
        'for x in range': '枚举 `{v}` 的倍数 x（`{v}`、2×`{v}`……，不超过 `ma = {ma}`）：这一步 x 取下一个倍数',
        'res += freq1': '`nums1` 里有 `{freq1[x]}` 个 `{x}` × `nums2` 里 `{f}` 个 → `res` 加 {freq1[x]*f}，累计 =={res}==',
        'return res': '优质数对一共 `{res}` 对',
    },
    cards=dict(
        one_liner='相同的数合并统计，只枚举 v×k 的倍数',
        complexity='时间 `O(ma log m)`，空间 `O(n+m)`',
        problem=['若 `nums1[i]` 能整除 `nums2[j] * k`，数对 `(i, j)` 就是优质数对',
                 '求优质数对总数',
                 '示例：`[1,2,4,12]`，`[2,4]`，`k=3` → `2`'],
        quote='对于数值相同的nums1[i]以及nums1[i\']，又或者nums2[j]以及nums2[j\']，其可以构成的优质数对的数目是一致的，因此在这里就可以先用哈希表freq1和freq2分别统计出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `Counter` 把两个数组按数值合并', '对 `freq2` 里的每个 `v`，让 `v *= k`',
              '`nums1` 里是 `v` 的倍数的数都能配：从 `v` 起每次加 `v` 枚举，累加 `freq1[x] * f`'],
        summary=['枚举倍数的总次数是调和级数，约 `ma log m`',
                 '易错点：先 `v *= k` 再枚举倍数，步长也是新的 `v`',
                 '`Counter` 取不存在的键返回 0，不用判断',
                 '这套做法对 3164 题（数据更大）同样适用',
                 '原文为 Python 2 风格，只删去了类型说明，逻辑未改'],
    ),
)
