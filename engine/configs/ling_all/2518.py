def _col(S, i, v):
    if S.get('_line') == 9 and 'j' in S and 'x' in S:
        if i == S['j']:
            return 'yellow'
        if i == S['j'] - S['x']:
            return 'blue'
    return None


def _txt(S):
    if S.get('_line') == 9 and 'j' in S and 'x' in S:
        j, x = S['j'], S['x']
        return f'`f[{j}] += f[{j - x}]`：和为 `{j}` 的方案 = 不选 `{x}` + 选 `{x}`（凑 `{j - x}`）'
    if 'x' in S:
        return f'当前数 `x = {S["x"]}`：倒序更新，每个数只用一次'
    return '`f[j]` = 选若干数、和恰好为 `j` 的方案数（只算 `j < k`）'


CONFIG = dict(
    num=2518, title='好分区的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='正难则反 · 01 背包计数',
    tags=['数学算法', '难度分 2415'],
    code='''
class Solution:
    def countPartitions(self, nums: List[int], k: int) -> int:
        if sum(nums) < k * 2: return 0
        MOD = 10 ** 9 + 7
        f = [0] * k
        f[0] = 1
        for x in nums:
            for j in range(k - 1, x - 1, -1):
                f[j] = (f[j] + f[j - x]) % MOD
        return (pow(2, len(nums), MOD) - sum(f) * 2) % MOD
''',
    call='Solution().countPartitions([1, 2, 3, 4], 4)',
    expect=6,
    skip=['for j in range', 'MOD = 10'],
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=80,
             color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] and S.get('_line') in (7, 9) else None),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='f', label='f[j]：和为 j 的方案数（j < k）', h=210, cell=110, color=_col),
        dict(type='text', fn=lambda S: (f'坏分区 = `sum(f) × 2` = `{sum(S["f"])} × 2` = =={sum(S["f"]) * 2}==，总数 `2^{len(S["nums"])}` = {2 ** len(S["nums"])}'
                                         if S.get('_line') == 10 else ''), size=24, h=60),
    ],
    watch=[('x', 'x', 'blue'), ('j', 'j', 'yellow'), ('k', 'k', 'pink'), ('sum(nums)', 'sum(nums)', 'cyan')],
    captions={
        'if sum(nums) < k * 2': '`sum = {sum(nums)}`，`2k = {k * 2}`：总和够 `2k` 才可能有好分区（不特判会重复统计坏分区）',
        'f = [0] * k': '只统计和 `< k` 的方案，数组长度 `k = {k}`，背包容量小',
        'f[0] = 1': '不选任何数，和为 0，有 1 种方案',
        'for x in nums': lambda S, B, r: (f'枚举 `x = {S.x}`' + ('，`x ≥ k`：选了和就 ≥ k，内层循环为空' if S.x >= S.k else '，选或不选') if S.get('x') != B.get('x') or S.get('x') is None else '所有数都处理完'),
        'f[j] = (f[j]': '`f[{j}] = {B.f[j]} + f[{j - x}]({f[j - x]})` = =={f[j]}==：不选 {x} + 选 {x}；`j` 倒序，保证每个数只选一次',
        'return': '坏分区 `sum(f)×2 = {sum(f) * 2}`，总数 `2^{len(nums)} = {2 ** len(nums)}`，答案 `{2 ** len(nums)} − {sum(f) * 2}` = =={ret}==',
    },
    cards=dict(
        one_liner='正难则反：数坏分区，再用 2^n 减掉',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['把 `nums` 分成有序的两组，==每组元素和都 ≥ k== 才是好分区',
                 '返回不同好分区的个数，对 `10^9+7` 取余',
                 '示例：`nums=[1,2,3,4], k=4` → `6`'],
        quote='如果直接计算好分区的数目，我们可以用 01 背包来做，但是背包容量太大，会超时。正难则反，我们可以反过来，计算坏分区的数目。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数组和可达 `10^12`，背包容量太大；但 `k ≤ 1000`',
              '坏分区：某组和 `< k`。对称性：只算第一组和 `< k`，再 ×2',
              '`bad = (f[0]+…+f[k-1]) × 2`，答案 `2^n − bad`'],
        summary=['时间 `O(nk)`，空间 `O(k)`（倒序循环滚动数组）',
                 '易错：`sum(nums) < 2k` 必须先特判返回 0，否则两组都 < k 会被重复统计',
                 '易错：`pow(2, n, MOD)` 减去后可能为负，最后要再 `% MOD`',
                 '相似题：494. 目标和（01 背包计数）'],
    ),
)
