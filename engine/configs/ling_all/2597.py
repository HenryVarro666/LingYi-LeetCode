def _txt(S):
    if 'f1' not in S:
        return '按“公差为 k 的等差数列”分组，每组做一次打家劫舍式 DP，最后相乘'
    x = S['x']
    return f"`f0 = {S['f0']}`（少看一个数的方案）　`f1 = {S['f1']}`（看到当前数的方案）　`ans = {S['ans']}`"


CONFIG = dict(
    num=2597, title='美丽子集的数目', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='分组 + 打家劫舍 DP（找等差数列首项）',
    tags=['其他线性 DP', '子集型回溯', '难度分 2023'],
    code='''
class Solution:
    def beautifulSubsets(self, nums: List[int], k: int) -> int:
        cnt = Counter(nums)
        ans = 1
        for x, c in cnt.items():
            if x - k in cnt:  # x 不是等差数列的首项
                continue
            # 计算这一组的方案数
            f0, f1 = 1, 1 << c
            x += k
            while x in cnt:
                f0, f1 = f1, f1 + f0 * ((1 << cnt[x]) - 1)
                x += k
            ans *= f1  # 每组方案数相乘
        return ans - 1  # 去掉空集
''',
    call='Solution().beautifulSubsets([2,4,6,4,5], 2)',
    expect=13,
    skip=['x += k', 'continue'],
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='map', var='cnt', label='cnt（数字 → 出现次数）', fmt=lambda k, v: f'{k}: ×{v}', h=230),
        dict(type='text', fn=lambda S: (f"当前这一组：公差 `{S['k']}` 的数列，正看到 `x = {S['x']}`" if 'f1' in S and S.get('_line', 0) >= 9 else ''), size=26, h=60),
    ],
    watch=[('x', 'x', 'blue'), ('c', 'c', 'cyan'), ('f0', 'f0', 'pink'), ('f1', 'f1', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '统计每个数出现的次数。相差恰好 `k` 的数不能同选，==相同的数可以一起选==',
        'ans = 1': '`ans` 是各组方案数的乘积，先取 1',
        'for x, c in cnt.items()': '看 `x = {x}`，出现 `c = {c}` 次',
        'if x - k in cnt': lambda S, B, r: (f'`x − k = {S.x - S.k}` 在 `cnt` 里：`x` 不是数列首项，跳过（会从首项走到它）' if S.x - S.k in S.cnt
                                             else f'`x − k = {S.x - S.k}` 不在 `cnt` 里：`x = {S.x}` 是==等差数列的首项==，从它开始算这一组'),
        'f0, f1 = 1, 1 <<': '首项 `x` 的 `{c}` 个数任选：`f0 = 1`（空），`f1 = 2^{c} = {f1}`（含不选）',
        'while x in cnt': lambda S, B, r: (f'`x = {S.x}` 在 `cnt` 里：数列还没结束，它和前一个数相差 `k`' if S.x in S.cnt
                                           else f'`x = {S.x}` 不在 `cnt` 里：这一组结束，方案数 `f1 = {S.f1}`'),
        'f0, f1 = f1': '`f1 = f1 + f0 × (2^{cnt[x]} − 1)`：不选 `x` 是旧 `f1`；选 `x` 就==不能选前一个==，用 `f0` 乘上 x 的非空选法 → `f1 = {f1}`',
        'ans *= f1': '这一组共 `{f1}` 种（含空）→ 乘到答案：`ans = {ans}`',
        'return ans - 1': '各组都可以什么都不选，总的空集要去掉：`{ans} − 1 = {ans - 1}`',
    },
    cards=dict(
        one_liner='相差 k 的数连成链，每条链做打家劫舍，各链方案数相乘',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['正整数数组 `nums` 和正整数 `k`，子集中任意两数之差都不等于 `k` 就是美丽子集',
                 '求非空美丽子集的个数（下标不同算不同子集）',
                 '本视频：`nums = [2,4,6,4,5]`，`k = 2` → `13`'],
        quote='这两个序列都是公差为 k 的等差数列。利用 128. 最长连续序列的技巧，找到等差数列的首项，就能通过不断 +k 找到等差数列中的其他元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['链与链之间互不影响（相差不是 k），方案数用==乘法原理==相乘',
              '链内类似打家劫舍：选 `x` 就不能选 `x−k`，选法数是 `2^c − 1`（至少一个）',
              '只从“`x − k` 不在 `cnt` 里”的首项出发，无需排序'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`f1 = 2^c` 含不选；转移里选 `x` 要用 `2^c − 1`（非空）',
                 '最后 `ans - 1` 去掉空集',
                 '题解还给了回溯（枚举选或不选，`O(2^n)`）和“按模 k 分组 + 排序”两种写法，这里选最优的 `O(n)` 写法'],
    ),
)
