CONFIG = dict(
    num=3927, title='可整除替换后的数组最小元素和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='预处理因子 · 换成最小因子',
    tags=['灵神题单', '数论', '难度分 1652'],
    setup='''
MX = 13  # 原文预处理到 100_001，演示缩小到 13，逻辑一致
divisors = [[] for _ in range(MX)]
for i in range(1, MX):
    for j in range(i, MX, i):
        divisors[j].append(i)
''',
    code='''
class Solution:
    def minArraySum(self, nums: list[int]) -> int:
        cnt = Counter(nums)
        ans = 0

        for x, c in cnt.items():  # 遍历 cnt 而不是 nums，这样重复元素只会计算一次
            for d in divisors[x]:  # 从小到大枚举 x 的因子 d
                if d in cnt:
                    ans += d * c  # 把 x 变成 d 是最优的
                    break

        return ans
''',
    call='Solution().minArraySum([4,2,8,3,12,12])',
    expect=13,
    views=[
        dict(type='map', var='cnt', label='cnt（nums 中每个数出现几次）', h=200),
        dict(type='array', var=lambda S: [i for i in range(1, S['x'] + 1) if S['x'] % i == 0] if 'x' in S else None, label='x 的因子（从小到大）', h=170,
             color=lambda S, i, v: ('green' if 'd' in S and v == S['d'] and v in S['cnt'] else 'yellow' if 'd' in S and v == S['d'] else None)),
        dict(type='text', h=90, fn=lambda S: (f"`x = {S['x']}` 出现 {S['c']} 次，最小的在 nums 里的因子是 ==d = {S['d']}== → 每个贡献 {S['d']}" if 'x' in S and 'd' in S and S['d'] in S['cnt'] else (f"`x = {S['x']}`：试因子 `d = {S['d']}`，不在 cnt 里" if 'x' in S and 'd' in S else ''))),
    ],
    watch=['x', 'c', 'd', ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '统计每个数出现的次数：同一个数的替换结果相同，只算一次',
        'ans = 0': '`ans` 累计替换后的元素和',
        'for x, c in': '取一个互不相同的数 `x = {x}`，它出现 `{c}` 次',
        'for d in': '从小到大试 `x = {x}` 的因子：`d = {d}`',
        'if d in cnt': lambda S, B, r: (f'`d = {S.d}` 在 cnt 里 → 可以把 {S.x} 换成 {S.d}' if S.d in S.cnt else f'`d = {S.d}` 不在 nums 里，没法换成它，试下一个'),
        'ans += d * c': '最小的可用因子最优：{x} 全换成 {d}，共 {c} 个 → `ans += {d}×{c}` = =={ans}==',
        'break': '更小的因子已找到；因子的因子也是 x 的因子，不可能再变小 → ==直接 break==',
        'return ans': '元素和最小为 `{ans}`',
    },
    cards=dict(
        one_liner='每个数换成它在 nums 里的最小因子',
        complexity='时间 `O(nA)`（A 为最大因子个数），空间 `O(n)`',
        problem=['选下标 a、b，满足 `nums[a] % nums[b] == 0`，把 `nums[a]` 换成 `nums[b]`',
                 '可操作任意次，求最后数组元素和的最小值',
                 '示例：`[4,2,8,3]` → `9`（变成 `[2,2,2,3]`）'],
        quote='为了让总和尽量小，把 x 替换成 x 的最小因子（因子必须在 nums 中）是最优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['替换 = 把 x 换成 nums 里 x 的某个因子 d',
              '==换成最小的 d 最优==：d 的因子也是 x 的因子，不会再往下换',
              '预处理 [1, 10^5] 每个数的因子，查询时从小到大找第一个在 cnt 里的'],
        summary=['遍历 cnt 而不是 nums：重复元素只算一次，用 `d * c` 一起加',
                 '因子表按 `i` 从小到大填，所以 `divisors[x]` 天然有序，第一个命中就 break',
                 '演示把预处理上限缩小到 13（原文 `MX = 100_001`），并放在 setup 中先执行',
                 '因子枚举题可在数学题单「§1.5 因子」中练'],
    ),
)
