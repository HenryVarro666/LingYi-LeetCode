PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def _names(mask):
    ps = [str(PRIMES[j]) for j in range(10) if mask >> j & 1]
    return '×'.join(ps) if ps else '空'


def _nz(S):
    f = S.get('f')
    if not f:
        return {}
    return {k: v for k, v in f.items() if v}


def _top(S):
    if 'factor' not in S:
        return '`f[state]`：用掉的质数集合恰好是 `state` 时的合法子集数（`state` 的第 j 位 = 第 j 个质数）'
    fa = S['factor']
    return f"当前数 `{S['num']}` → 质数集合 `state = {fa}`（{_names(fa)}），出现 `{S['cnt']}` 次"


def _lf(S, B, ret):
    n = S.num
    return f'`{n}` 对应的 `factor = {S.factor}`（质因子 {_names(S.factor)}，互不重复）'


CONFIG = dict(
    num=1994, title='好子集的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='质数状压 DP · 背包计数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numberOfGoodSubsets(self, nums):

        mod = 10 ** 9 + 7
        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        pow2 = 1
        for index in range(cnt_dict.get(1, 0)):
            pow2 += pow2
            if pow2 >= mod:
                pow2 -= mod
        
        prime_mapping = {2:  1,
                         3:  2,
                         6:  3,
                         5:  4,
                         10: 5,
                         15: 6,
                         30: 7,
                         7:  8,
                         14: 9,
                         21: 10,
                         11: 16,
                         22: 17,
                         13: 32,
                         26: 33,
                         17: 64,
                         19:128,
                         23:256,
                         29:512}

        res = 0
        f = {x : 0 for x in range(1024)}
        
        for num, cnt in cnt_dict.items():
            if num in prime_mapping:
                factor = prime_mapping[num]
                for state in range(1023, factor, -1):
                    if (state & factor) == factor:
                        f[state] += f[state ^ factor] * cnt
                        f[state] %= mod
                f[factor] += cnt
                if f[factor] >= mod:
                    f[factor] -= mod

        return sum(f.values()) * pow2 % mod
''',
    call='Solution().numberOfGoodSubsets([1,1,2,3,4,6])',
    expect=16,
    skip=['for num in nums', 'cnt_dict[num] =', 'for index in range', 'pow2 += pow2', 'if pow2 >= mod', 'pow2 -= mod',
          'for state in range', 'if (state & factor)', 'f[state] +=', 'f[state] %=', 'if f[factor] >= mod', 'f[factor] -= mod',
          'cnt_dict = {}', 'res = 0'] + list(range(15, 34)),
    max_steps=60,
    max_events=60000,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='array', var='nums', label='nums（1 单独算，不影响是否合法）', h=170, cell=70,
             color=lambda S, i, v: ('blue' if 'num' in S and S['num'] == v and S['_line'] >= 36 else None)),
        dict(type='map', var=_nz, label='f[state]：非零项（键 = 质数集合的位掩码）', h=300, font=26,
             fmt=lambda k, v: f'{k} ({_names(k)}) → {v}'),
        dict(type='map', var='cnt_dict', label='cnt_dict：每个数出现几次', h=250),
    ],
    watch=[('pow2', 'pow2', 'yellow'), ('factor', 'factor', 'blue'), ('cnt', 'cnt', 'green')],
    captions={
        'mod =': '答案对 `10^9 + 7` 取模',
        'pow2 = 1': '`pow2` 先记 1：后面 1 有 k 个，就乘 `2^k`',
        'f = {x': '`prime_mapping`：18 个无平方因子的数 → 质因子位掩码（如 `6 = 2×3 → 1+2 = 3`）；`f[state]` 先全设 0',
        'for num, cnt in': lambda S, B, r: ('全部数字处理完' if B.get('num') == S.get('num') and 'num' in B else
                                            f'处理数字 `{S.num}`（出现 `{S.cnt}` 次）' + ('：==1 不影响合法性，最后乘 `2^k`==' if S.num == 1
                                            else '：含平方因子 → 不可用，跳过' if S.num not in S.prime_mapping else '')),
        'if num in prime_mapping': lambda S, B, r: (f'`{S.num}` 在表里（无平方因子）→ 可用' if S.num in S.prime_mapping
                                                    else '`1` 不在表里，不进 DP' if S.num == 1 else f'`{S.num}` 有平方因子 → 不可用，跳过'),
        'factor = prime_mapping[num]': _lf,
        'f[factor] += cnt': '从大到小枚举 `state`，把 `{num}` 并进不相交的集合，再单选：`f[{factor}] += {cnt}` → =={f[factor]}==',
        'return sum': lambda S, B, r: f'`f` 之和 `{sum(S.f.values())}` × `pow2 = {S.pow2}`（{S.cnt_dict.get(1, 0)} 个 1 → 每个可选可不选）= =={r}==',
    },
    cards=dict(
        one_liner='不能有相同质因子：10 个质数当 10 位二进制，背包计数',
        complexity='时间 `O(1024 × 18)`，空间 `O(1024)`',
        problem=['`nums` 的子集，若乘积能表示成==一个或多个互不相同的质数==相乘，就是好子集（乘积为 1 的不算）',
                 '求好子集的个数，对 `10^9 + 7` 取模；下标不同算不同子集',
                 '本视频：`nums = [1,1,2,3,4,6]` → `16`（4 含平方因子，永远不能选）'],
        quote='由于题目中不能出现相同的因子，而小于30的质因子总共只有2、3、5、7、11、13、17、19、23、29这10种，那么完全可以使用状态压缩动态规划',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[state]`：当前因子组合为 `state` 时有多少种合法子集',
              '对每个可用的数：从大到小枚举 `state`，`f[state] += f[state ^ factor] * cnt`（01 背包）',
              '`cnt` 个相同的数里只能选一个，所以乘 `cnt`',
              '1 不影响合法性：有 k 个 1 就乘 `2^k`'],
        summary=['时间 `O(18 × 1024)`，空间 `O(1024)`',
                 '`state` 必须从大到小枚举（01 背包），否则同一个数会被重复使用',
                 '1 要单独处理：最后乘 `2^k`；`f[0] = 0`，所以空集和只含 1 的子集都不会被算进去',
                 '含平方因子的数（4、8、9、12……）直接丢掉',
                 '原文已是 Python 3 可运行写法，无需改动'],
    ),
)
