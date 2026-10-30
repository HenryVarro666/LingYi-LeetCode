NUMS = [4, 3, 6, 5]

SETUP = '''
# 预处理每个数的质因子
MX = 1_000_001
prime_divisors = [[] for _ in range(MX)]
for i in range(2, MX):
    if not prime_divisors[i]:  # i 是质数
        for j in range(i, MX, i):  # 枚举 i 的倍数 j
            prime_divisors[j].append(i)  # i 是 j 的质因子
'''


def _text(S):
    if 'max_diff' not in S:
        return '对每个质因子 `p` 当 `k`：`p` 的倍数记 `+x`，其余记 `−x` → 最大子数组和'
    md = '-∞' if S['max_diff'] == float('-inf') else S['max_diff']
    return f'目前最优：分数差 `max_diff` = =={md}==，`best_k` = =={S["best_k"]}=='


def _cap_f(S, B, ret):
    p, x = S.p, S.x
    old = B.f.get(p, 0)
    la = B.last.get(p, 0)
    gap = S.s[S.i] - S.s[la]
    if p not in B.last:
        return f'第一次遇到质因子 `{p}`：前面没有它的倍数，`f[{p}]` 从 0 起步 → `max(0, 0) + {x}` = =={S.f[p]}=='
    if gap == 0:
        return f'质因子 `{p}` 刚出现过（紧挨着），中间没有非倍数：`f[{p}] = max({old}, 0) + {x}` = =={S.f[p]}=='
    keep = old - gap
    way = f'中间 {S.i - la} 个非倍数合成 `−{gap}`，`{old} − {gap} = {keep}` ' + ('仍为正 → 接着拼' if keep > 0 else '不为正 → 重新开始')
    return f'`{p}` 的倍数 `{x}`：{way} → `f[{p}] = {S.f[p]}`'


def _cap_best(S, B, ret):
    d = S.f[S.p]
    mx = S.max_diff
    if d > mx:
        return f'`diff = {d}` 超过当前最优 `{"-∞" if mx == float("-inf") else mx}` → 更新 `max_diff`、`best_k = {S.p}`'
    if d == mx and S.p < S.best_k:
        return f'`diff = {d}` 与最优相同，`k = {S.p}` 更小 → 更新 `best_k`'
    return f'`diff = {d}` 没有超过最优 `{mx}`，不更新'


CONFIG = dict(
    num=3984, title='可整除游戏', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='质因子 + 前缀和合并负数段的最大子数组和',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1944'],
    setup=SETUP,
    code='''
class Solution:
    def divisibleGame(self, nums: list[int]) -> int:
        MOD = 1_000_000_007

        n = len(nums)
        s = list(accumulate(nums, initial=0))

        if s[n] == n:
            # 每个数都是 1
            # 最优是只选一个 1（分数差为 -1），最小 k 为 2
            return MOD - 2

        f = defaultdict(int)
        last = defaultdict(int)
        max_diff = -inf
        best_k = 0

        for i, x in enumerate(nums):
            for p in prime_divisors[x]:
                diff = f[p] = max(f[p] - s[i] + s[last[p]], 0) + x
                if diff > max_diff or diff == max_diff and p < best_k:
                    max_diff = diff
                    best_k = p
                last[p] = i + 1

        return max_diff * best_k % MOD
''',
    call=f'Solution().divisibleGame({NUMS})',
    expect=27,
    skip=['MOD = 1_000_000_007', 'n = len(nums)'],
    views=[
        dict(type='text', fn=_text, size=24, h=70),
        dict(type='array', var='nums', label='nums（蓝 = 当前 x；p 的倍数才是 Alice 的分）', cell=96, h=210,
             pointers={'i': 'blue'}, color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='map', var='f', label='f[p]：以质因子 p 为 k、结尾在 p 的最近倍数的最大子数组和', fmt=lambda k, v: f'{k} → {v}', h=150),
        dict(type='map', var='last', label='last[p]：p 上次出现的下标 + 1', fmt=lambda k, v: f'{k} → {v}', h=150),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'yellow'), ('p', 'p', 'pink'), ('max_diff', 'max_diff', 'green'), ('best_k', 'best_k', 'orange')],
    captions={
        's = list(accumulate': '前缀和 `s = {s}`：用来快速求两个倍数之间那一段非倍数的和',
        'if s[n] == n': '`s[n] = {s[n]}`，`n = {n}`：不是全 1，继续',
        'f = defaultdict': '`f[p]`：以质因子 `p` 为 k 时，DP 的最近一个值',
        'last = defaultdict': '`last[p]`：`p` 上一次作为质因子出现的下标 + 1',
        'max_diff = -inf': '`max_diff` 记最大分数差，`best_k` 记对应最小的 `k`',
        'for i, x in enumerate': '枚举 `nums[{i}] = {x}`，它的质因子有 `{prime_divisors[x]}`',
        'for p in prime_divisors': '质因子 `p = {p}`：只有 `{p}` 的倍数才给 Alice 加分',
        'diff = f[p]': _cap_f,
        'if diff > max_diff': _cap_best,
        'best_k = 0': '`best_k` 初值 0，找到第一个候选后就会被覆盖',
        'max_diff = diff': '`max_diff` → =={max_diff}==',
        'best_k = p': '`best_k` → =={best_k}==',
        'last[p] = i + 1': '记下 `last[{p}] = {i} + 1 = {i+1}`：下一次从这里之后算中间的非倍数',
        'return max_diff': '`max_diff × best_k % MOD` = `{max_diff} × {best_k}` = =={ret}==',
    },
    cards=dict(
        one_liner='只枚举质因子当 k，非倍数合成一个大负数',
        complexity='时间 `O(n log U / log log U)`，空间 `O(n log log U)`',
        problem=['Alice 选 `k>1` 和区间 `[l,r]`：`k` 的倍数加给 Alice，其余加给 Bob',
                 '最大化 Alice − Bob，并列取最小 `k`，返回分数差 × k 取模 `10^9+7`',
                 '本视频：`nums=[4,3,6,5]` → `27`（`k=3`，区间 `[3,6]`，差 9）'],
        quote='夹在 nums 中的两个 k 的倍数之间的数，都是负数。我们可以把这些负数合在一起，当作一个大负数。……在遍历 nums 的同时，计算与 nums[i] 的质因子有关的最大子数组和。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['固定 `k`，倍数记 `+x`、非倍数记 `−x` → 最大子数组和（53 题）',
              '`k` 只需取质因子：倍数更多，同样的差时 `k` 还更小',
              '方法三：遍历 `nums` 时只更新 `x` 的质因子，中间一段非倍数用前缀和合成一个大负数'],
        summary=['时间 `O(n log U / log log U)`，忽略预处理',
                 '预处理 `prime_divisors` 用质数筛，演示里放在 `setup` 中，不单独追踪',
                 '全是 1 的特判：分数差 `-1`、`k = 2` → `MOD - 2`',
                 '`diff == max_diff and p < best_k` 处理并列时取最小 `k`',
                 '另有「枚举质因子 + 53 题」与线段树维护动态最大子数组和两种写法'],
    ),
)
