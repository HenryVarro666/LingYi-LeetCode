def _top(S):
    if 'energy' not in S:
        return '先排序，再把所有两两差值收集成集合 `energy_set`，逐个当候选能量'
    if S['_line'] <= 38:
        return f"候选能量 `energy = {S['energy']}`：数「相邻差都 ≥ energy」减「都 > energy」"
    return f"`energy = {S['energy']}`：累加 `f - g` = 恰好有一对相邻差 == energy 的方案数"


def _cur(S):
    if 'index' not in S or 'nums' not in S or S['_line'] < 25 or S['_line'] > 42:
        return None
    return S['index']


def _txt(S):
    if 'f' not in S or 'energy' not in S or 'pre_f' not in S:
        return ''
    return f"`pre_f = {S['pre_f']}`   `pre_g = {S['pre_g']}`"


CONFIG = dict(
    num=3098, title='求出所有子序列的能量和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='枚举能量 · 排序 DP · 双指针前缀和',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def sumOfPowers(self, nums, k):

        nums.sort()
        energy_set = set()
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                energy_set.add(abs(nums[i] - nums[j]))
        
        res = 0
        mod = 10 ** 9 + 7
        n = len(nums)
        for energy in energy_set:
            f = [1] * n
            g = [1] * n
            for _ in range(2, k + 1):
                pre_f = f[:]
                pre_g = g[:]
                f = [0] * n
                g = [0] * n
                sf = 0
                sg = 0
                p = 0
                q = 0
                for index, v in enumerate(nums):
                    while p < index and v - nums[p] >= energy:
                        sf += pre_f[p]
                        if sf >= mod:
                            sf -= mod
                        p += 1
                    while q < index and v - nums[q] > energy:
                        sg += pre_g[q]
                        if sg >= mod:
                            sg -= mod
                        q += 1

                    f[index] = sf
                    g[index] = sg
        
            tot = 0
            for index in range(n):
                tot += (f[index] - g[index] + mod)
                if tot >= mod:
                    tot -= mod
            
            res = (res + tot * energy) % mod
        
        return res
''',
    call='Solution().sumOfPowers([1, 2, 3], 2)',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var='nums', label='nums（已排序，蓝 = 当前 index）', cell=100, h=160,
             color=lambda S, i, v: 'blue' if _cur(S) == i else None),
        dict(type='array', var='f', label='f[i]：以 nums[i] 结尾，相邻差 >= energy 的方案数', cell=90, h=150, color=lambda S, i, v: 'green' if _cur(S) == i else None),
        dict(type='array', var='g', label='g[i]：同上，但相邻差 > energy', cell=90, h=150, color=lambda S, i, v: 'green' if _cur(S) == i else None),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=[('energy', 'energy', 'pink'), ('index', 'index', 'blue'), ('p', 'p', 'cyan'), ('q', 'q', 'orange'), ('sf', 'sf', 'green'), ('sg', 'sg', 'yellow'), ('res', 'res', 'green')],
    skip=[6, 7, 8, 16, 'energy_set = set()', 'res = 0', 'mod = 10', 'n = len(nums)', 'f = [1] * n', 'g = [1] * n', 'pre_f = f', 'pre_g = g',
          'f = [0] * n', 'g = [0] * n', 'if sf >= mod', 'if sg >= mod', 'if tot >= mod', 'tot -= mod', 'sf -= mod', 'sg -= mod', 'tot = 0', 'sf = 0', 'sg = 0', 'p = 0', 'q = 0'],
    captions={
        4: '先排序：最小差只会出现在==相邻==元素之间；再收集所有两两差当候选能量',
        8: '收集两两差：`|{nums[i]} - {nums[j]}| = {abs(nums[i] - nums[j])}`；能量只可能是其中之一 → `energy_set = {sorted(energy_set)}`',
        13: lambda S, B, r: ('候选能量都试完了' if B.get('energy') == S.energy else f'候选能量只可能是某两数之差 `{sorted(S.energy_set)}`；试 `energy = {S.energy}`：数「最小差恰好等于它」的子序列'),
        16: lambda S, B, r: ('`k = 2`：只需要做 `k - 1 = 1` 轮，把长度 1 的方案扩展到长度 2；`f`、`g` 初值全 1（单个元素）' if 'pre_f' not in S else '`k - 1` 轮做完，`f`、`g` 就是长度为 `k` 的方案数'),
        25: lambda S, B, r: (f'`nums[{S.index}] = {S.v}`：算以它结尾的方案数' if S.index != B.get('index') else '这一轮算完了'),
        26: lambda S, B, r: (f'`nums[{S.p}] = {S.nums[S.p]}`：`{S.v} - {S.nums[S.p]} = {S.v - S.nums[S.p]} >= {S.energy}`，可以做前驱，`p` 右移' if S.p < S.index and S.v - S.nums[S.p] >= S.energy else f'`p` 停在 {S.p}：`sf = {S.sf}` 是 `nums[0..p-1]` 的 `f` 之和（差 >= energy 的前驱）'),
        27: '`sf` += `pre_f[{p}]` → `{sf}`：前驱方案数并入',
        30: '`p` → `{p}`，只右移不回退',
        31: lambda S, B, r: (f'`nums[{S.q}] = {S.nums[S.q]}`：`{S.v} - {S.nums[S.q]} = {S.v - S.nums[S.q]} > {S.energy}`（严格大于），`q` 右移' if S.q < S.index and S.v - S.nums[S.q] > S.energy else f'`q` 停在 {S.q}：`sg = {S.sg}` 是差 > energy 的前驱方案数'),
        32: '`sg` += `pre_g[q]` → `sg = {sg}`',
        35: '`q` → `{q}`，也只右移',
        37: '`f[{index}] = {sf}`：以 `{v}` 结尾，相邻差都 >= energy 的方案数',
        38: '`g[{index}] = {sg}`：差都 > energy。`f − g = {f[index] - g[index]}` 个==恰好==等于',
        42: '`tot` += `f - g = {f[index] - g[index]}`（以 `nums[{index}]` 结尾）',
        46: '`res += tot × energy = {tot} × {energy}`：这些子序列的能量都恰好是 energy → `res = {res}`',
        48: '所有长度为 `k` 的子序列的能量和：`{ret}`',
    },
    cards=dict(
        one_liner='枚举能量值，用 f − g 数出「恰好等于」它的方案',
        complexity='时间 `O(n²·k·n)`，空间 `O(n)`',
        problem=['长度为 `k` 的子序列，能量 = 两两元素差的绝对值的==最小值==',
                 '求 `nums` 所有长度为 `k` 的子序列的能量之和，对 `10^9+7` 取模',
                 '本视频：`nums = [1,2,3]`，`k = 2` → `4`'],
        quote='令f[i][j]表示选出以nums[i]为结尾的长度为j的子序列，且子序列中相邻元素之间的差值大于等于energy的方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组较短：先枚举所有两两差，当候选能量 `energy`',
              '排序后只看相邻：`f` 数「差 ≥ energy」，`g` 数「差 > energy」，`f − g` 就是恰好等于',
              '`p` / `q` 随 `index` 单调右移，前缀和 `sf` / `sg` 均摊 `O(1)` 转移'],
        summary=['能量只可能是某两数之差，所以枚举 `energy_set`',
                 '`f − g` 保证至少有一对相邻差恰为 energy，最后乘 `energy`',
                 '`p`、`q` 单调不回退，前缀和 + 滚动数组把转移压到均摊 `O(1)`',
                 '原文已是 Python 3 可运行的写法，代码未改动'],
    ),
)
