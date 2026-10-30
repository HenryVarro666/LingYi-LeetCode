PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def _names(mask):
    ps = [str(PR[j]) for j in range(10) if mask >> j & 1]
    return '×'.join(ps) if ps else '空集'


def _nz(S):
    f = S.get('f')
    if not f:
        return {}
    return {j: v for j, v in enumerate(f) if v}


def _top(S):
    if 'mask' not in S or 'x' not in S:
        return '`f[j]`：恰好用掉质数集合 `j` 的方案数（`j` 的第 i 位 = 第 i 个质数是否出现）'
    return f"当前数 `x = {S['x']}` 出现 `{S['c']}` 次，质因子集合 `mask = {S['mask']}`（{_names(S['mask'])}）"


def _mask_cap(S, B, r):
    if S.mask > 0:
        return f'`x = {S.x}` 的质因子集合 `mask = {S.mask}`（{_names(S.mask)}）→ 是 ==SF==，可以选'
    if S.mask == 0:
        return '`x = 1` 没有质因子，`mask = 0`：它们已经算在 `f[0]` 里了'
    return f'`x = {S.x}` 有平方因子，`mask = -1`：一个也不能选'


def _for_cap(S, B, r):
    if 'x' not in S or (B.get('x') == S.get('x') and 'x' in B):
        return '所有数字处理完：`f` 里全部方案数相加'
    pre = ''
    if B.get('mask', 0) > 0:
        pre = f'上一个数转移完，`sum(f)` = {sum(S.f)}。'
    return pre + f'处理数字 `{S.x}`（出现 `{S.c}` 次）'


CONFIG = dict(
    num=2572, title='无平方子集计数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='子集状压 DP · 枚举补集的子集',
    tags=['灵神题单', '难度分 2420'],
    code='''
PRIMES = 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
SF_TO_MASK = [0] * 31  # SF_TO_MASK[i] 为 i 的质因子集合（用二进制表示）
for i in range(2, 31):
    for j, p in enumerate(PRIMES):
        if i % p == 0:
            if i % (p * p) == 0:  # 有平方因子
                SF_TO_MASK[i] = -1
                break
            SF_TO_MASK[i] |= 1 << j  # 把 j 加到集合中

class Solution:
    def squareFreeSubsets(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        cnt = Counter(nums)
        M = 1 << len(PRIMES)
        f = [0] * M  # f[j] 表示恰好组成质数集合 j 的方案数
        f[0] = pow(2, cnt[1], MOD)  # 用 1 组成空质数集合的方案数
        for x, c in cnt.items():
            mask = SF_TO_MASK[x]
            if mask > 0:  # x 是 SF
                j = other = (M - 1) ^ mask  # mask 的补集
                while True:  # 枚举 other 的子集 j
                    f[j | mask] = (f[j | mask] + f[j] * c) % MOD  # 不选 mask + 选 mask
                    j = (j - 1) & other
                    if j == other: break
        return (sum(f) - 1) % MOD  # -1 表示去掉空集（nums 的空子集）
''',
    setup='',
    call='Solution().squareFreeSubsets([1,3,3,4,5])',
    expect=11,
    max_events=80000,
    skip=['for i in range(2, 31)', 'for j, p in enumerate', 'if i % p', 'if i % (p * p)', 'SF_TO_MASK[i] = -1', 'break',
          'SF_TO_MASK[i] |=', 'while True', 'f[j | mask] =', 'j = (j - 1)', 'if j == other', 'cnt = Counter', 'M = 1 <<', 'MOD ='],
    max_steps=60,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='array', var='nums', label='nums（4 含平方因子 2^2，永远不能选）', h=170, cell=70,
             color=lambda S, i, v: ('blue' if 'x' in S and S['x'] == v else None)),
        dict(type='map', var=_nz, label='f[j]：非零项（j = 质数集合位掩码 → 方案数）', h=330, font=26,
             fmt=lambda k, v: f'{k} ({_names(k)}) → {v}'),
        dict(type='map', var='cnt', label='cnt：每个数出现几次', h=210),
    ],
    watch=[('x', 'x', 'blue'), ('c', 'c', 'pink'), ('mask', 'mask', 'green'), ('sum(f)', 'sum(f)', 'yellow')],
    captions={
        'SF_TO_MASK = [0] * 31': '预处理：`SF_TO_MASK[i]` = `i` 的质因子集合；有平方因子记 -1（循环略过，只看结果）',
        'f = [0] * M': '`f[j]` 表示恰好组成质数集合 `j` 的方案数，共 `2^10 = 1024` 个集合',
        'f[0] = pow': '用 1 组成空质数集合：每个 1 选或不选 → `2^{cnt[1]}` = =={f[0]}== 种',
        'for x, c in cnt.items()': _for_cap,
        'mask = SF_TO_MASK[x]': _mask_cap,
        'if mask > 0': lambda S, B, r: ('`mask > 0` → 开始转移' if S.mask > 0 else '`mask ≤ 0` → 不转移，跳过'),
        'j = other': '`other` = `mask` 的补集；枚举它的子集 `j`（保证和 `mask` 不相交）：`f[j|mask] += f[j] * {c}`（`{c}` 个里选一个）',
        'return': lambda S, B, r: f'`sum(f)` = {sum(S.f)}，减去空集 → =={r}==',
    },
    cards=dict(
        one_liner='值域只有 30：相同数字一起处理，枚举补集的子集转移',
        complexity='时间 `O(n + q·2^m)`，空间 `O(2^m)`',
        problem=['无平方因子数：不能被 `1` 以外的任何平方数整除（如 `15` 是，`12` 不是）',
                 '数一数 `nums` 里乘积无平方因子的==非空子集==，对 `10^9 + 7` 取模',
                 '示例：`[3,4,4,5]` → `3`；本视频：`[1,3,3,4,5]` → `11`'],
        quote='毕竟 nums 的值域很小，把相同数字一并处理是更优的。……枚举 mask 的补集 other 的子集 j，这样可以保证 mask 和 j 是没有交集的。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['把每个 SF 变成质因子集合（二进制），选的数集合必须==两两不相交==',
              '`f[j]`：恰好组成质数集合 `j` 的方案数；用 1 组成空集有 `2^{cnt[1]}` 种',
              '对 `cnt[x]` 个相同的数：从中选 1 个，`f[j ∪ mask] += f[j] · cnt[x]`'],
        summary=['时间 `O(n + q·2^m)`，`m = 10`、`q ≤ 18`；方法一（0-1 背包，逐个 `nums[i]` 转移）是 `O(n·2^m)`',
                 '最后 `-1` 去掉空集；答案要对 `10^9 + 7` 取模',
                 '有平方因子的数（4、8、9……）`mask = -1`，直接跳过；`mask > 0` 才处理，1 已在 `f[0]` 里',
                 '本视频演示方法二（子集状压）；方法一是对每个 SF 做 0-1 背包方案数，倒序枚举 `j`',
                 '同类状压题：1494. 并行课程 II、1994. 好子集的数目'],
    ),
)
