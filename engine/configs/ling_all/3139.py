def _col(S, i, v):
    nums = S['nums']
    if v == max(nums):
        return 'pink'
    if v == min(nums):
        return 'blue'
    return None


def _info(S):
    if 'base' in S:
        return (f"最小 `m = {S['m']}`，最大 `M = {S['M']}`；全变成 M 要 `base = n×M − sum = {S['base']}` 次操作一")
    if 'M' in S:
        return f"最小 `m = {S['m']}`，最大 `M = {S['M']}`"
    return '先看全部变成最大值 `M` 的情况，再看能不能「变成更大的 x」更便宜'


def _fx(S):
    I = S.get('_inner', {})
    if 'x' not in I:
        return ''
    x = I['x']
    t = f"目标 `x = {x}`"
    if 's' in I:
        t += f"：盒子里共 `s = {I['s']}` 个球"
    if 'd' in I:
        t += f"，最多的盒子 `d = x − m = {I['d']}` 个"
    return t


CONFIG = dict(
    num=3139, title='使数组中所有元素相等的最小开销', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 枚举目标 x 附近的几个值',
    tags=['灵神题单', '难度分 2666'],
    code='''
class Solution:
    def minCostToEqualizeArray(self, nums: List[int], c1: int, c2: int) -> int:
        MOD = 1_000_000_007
        n = len(nums)
        m = min(nums)
        M = max(nums)
        base = n * M - sum(nums)
        if n <= 2 or c1 * 2 <= c2:
            return base * c1 % MOD

        def f(x: int) -> int:
            s = base + (x - M) * n
            d = x - m
            return max(s // 2 * c2 + s % 2 * c1, (s - d) * c2 + (d * 2 - s) * c1)

        i = (n * M - m * 2 - base + n - 3) // (n - 2)
        return min(f(M), f(M + 1)) % MOD if i <= M else \\
               min(f(M), f(i - 1), f(i), f(i + 1)) % MOD
''',
    call='Solution().minCostToEqualizeArray([1,3,4,4], 9, 5)',
    expect=20,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='bars', var='nums', color=_col, h=330, label='nums（蓝 = 最小 m，粉 = 最大 M）'),
        dict(type='text', fn=_fx, h=80),
    ],
    watch=[('c1', 'c1', 'blue'), ('c2', 'c2', 'pink'), 'base', 'i', 'x', 's', 'd'],
    captions={
        'MOD =': '答案要对 `10^9 + 7` 取余',
        'n = len': '`n = {n}`',
        'm = min': '`m = {m}`：最小值，它需要补得最多',
        'M = max': '`M = {M}`：最大值，目标至少是它',
        'base = n * M': '都变成 `M` 总共要加 `base = {n}×{M} − sum = {base}` 次 1',
        'if n <= 2 or': lambda S, B, r: ('`n ≤ 2` 或 `c1×2 ≤ c2`（两次操作一不比一次操作二贵）→ 只用操作一，答案 `base × c1`' if (S.n <= 2 or S.c1 * 2 <= S.c2)
                                          else f'`n = {S.n} > 2` 且 `c1×2 = {S.c1 * 2} > c2 = {S.c2}`：操作二更划算 → 尽量多用操作二，继续'),
        'return base * c1': '只用操作一：`base × c1 % MOD`',
        's = base + (x - M) * n': '目标 `x = {x}`：每个数在 M 的基础上再多加 `x − M`，总共要加 `s = {s}` 次（盒子里的球数）',
        'd = x - m': '最小的数要加 `d = x − m = {d}` 次，它是球最多的盒子',
        'return max(s // 2': '操作二最多 `min(s//2, s−d) = min({s // 2}, {s - d})` = {min(s // 2, s - d)} 次，其余 {s - 2 * min(s // 2, s - d)} 次用操作一 → `f({x})` = =={ret}==（公式取两式较大者）',
        'i = (n * M': '解 `2d ≤ s` 的临界点：`i = {i}`；`x` 到了 `i` 附近，只和 `s` 有关，再往后只会更贵',
        'return min(f(M), f(M + 1))': lambda S, B, r: (f'候选里最小的取余：=={r}==，这就是答案' if r is not None else
                                                       (f'`i = {S.i} ≤ M = {S.M}`：临界点不超过 M → 只需比较 `f(M)` 和 `f(M+1)`' if S.i <= S.M
                                                        else f'`i = {S.i} > M = {S.M}`：临界点在 M 右边 → 要比较 4 个候选，走 else 分支')),
        'min(f(M), f(i - 1)': '依次算 `f(M)`、`f(i−1)`、`f(i)`、`f(i+1)`，取最小再取余',
    },
    cards=dict(
        one_liner='都变成最大值不一定最省，目标 x 可以更大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['操作一：一个数 `+1`，花 `cost1`；操作二：两个不同的数各 `+1`，花 `cost2`',
                 '求让所有数相等的最小总开销，结果对 `10^9+7` 取余',
                 '示例：`[4,1], 5, 2` → `15`；本视频：`[1,3,4,4], 9, 5` → `20`'],
        quote='想象有 n 个盒子，第 i 个盒子装有 x−nums[i] 个小球。操作一相当于从一个非空盒子中取出一个球，操作二相当于从两个不同的非空盒子中各取一个小球。我们需要计算最多能执行多少次操作二。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n ≤ 2` 或 `2c1 ≤ c2`：操作二没有优势，都变成 `M`，`base × c1`',
              '否则目标 `x ≥ M`，盒子共 `s` 个球、最多的盒子 `d` 个，操作二至多 `min(s//2, s−d)` 次',
              '`f(x)` 只在临界点 `i` 附近、以及 `M` 处可能取到最小，所以只算 4 个值'],
        summary=['时间 `O(n)`（求 m、M、sum），之后 `O(1)`',
                 '`i = ceil((nM − 2m − base) / (n − 2))`，写成 `// ` 时要加 `n − 3`',
                 '`f(x)` 取两种情形的较大者：总数的一半，或被最大盒子卡住的情形',
                 '同一思路也能用循环枚举 `x` 到 `2M`，这里用公式把枚举缩到 4 个值'],
    ),
)
