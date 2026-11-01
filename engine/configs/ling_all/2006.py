CONFIG = dict(
    num=2006, title='差的绝对值为 K 的数对数目', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 先统计再枚举 v-k（Go 原文转写）',
    code='''
class Solution:
    def countKDifference(self, nums: List[int], k: int) -> int:
        ans = 0
        cnt = Counter()
        for v in nums:
            cnt[v] += 1
        for v in nums:
            ans += cnt[v - k]
        return ans
''',
    call='Solution().countKDifference([1,2,2,1], 1)',
    expect=4,
    views=[
        dict(type='array', var='nums', h=190, cell=100, label='nums（v 是当前枚举的数）',
             color=lambda S, i, v: 'blue' if S.get('_line') == 8 and 'v' in S and v == S['v'] else None),
        dict(type='map', var='cnt', h=200, label='cnt：每个数出现的次数'),
        dict(type='text', size=28, h=100, fn=lambda S: (f"`v = {S['v']}`：和它差 `k` 的更小的数是 `v - k = {S['v'] - S['k']}`，出现 ==`{S['cnt'].get(S['v'] - S['k'], 0)}`== 次" if S.get('_line') == 8 and 'v' in S else '')),
    ],
    watch=[('k', 'k', 'blue'), ('v', 'v', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计满足条件的数对个数',
        'cnt = Counter()': '`cnt` 记录每个数出现的次数',
        'cnt[v] += 1': '数 `{v}` 的次数 → `{cnt[v]}`',
        5: lambda S, B, r: ('第一轮：取下一个数去统计次数（取完则结束第一轮）'),
        7: lambda S, B, r: ('第二轮：取下一个 `v` 当作较大的数（取完则结束）'),
        'ans += cnt[v - k]': '`v = {v}`：另一个数必须是 `v - k = {v - k}`，它在数组里共 `{cnt[v - k]}` 个 → `ans` = =={ans}==',
        'return ans': '每个数对恰好在较大数 `v` 处被数一次，答案 `{ans}`',
    },
    cards=dict(
        one_liner='枚举较大的数 v，去哈希表里数有多少个 v-k',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求数对 `(i, j)` 的个数，满足 `i < j` 且 `|nums[i] - nums[j]| == k`',
                 '示例：`[1,2,2,1], k=1` → `4`'],
        quote='for _, v := range nums { ans += cnt[v-k] }',
        quote_src='—— 灵茶山艾府题解代码（Go）',
        idea=['先遍历一遍，用哈希表统计每个数出现的次数',
              '再遍历每个 `v`：让它当较大的数，配对的较小数是 `v-k`',
              '数对不分先后，每对只会在较大数这一侧数到一次，不会重复'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`map[int]int{}` 用 `Counter()`，读不存在的键得 0 且不插入；Go 的具名返回值 `ans` 显式写成 `ans = 0`）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：`k >= 1`，所以 `v` 和 `v-k` 不是同一个数，不会自己配自己',
                 '对比暴力 `O(n^2)` 双重循环'],
    ),
)
