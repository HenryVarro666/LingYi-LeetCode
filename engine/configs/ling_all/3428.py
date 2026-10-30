def _s_text(S):
    if 'i' not in S or 's' not in S:
        return '排序后：`nums[i]` 当最大值、`nums[-1-i]` 当最小值，两者的子序列个数相同'
    i, k, s = S['i'], S['k'], S['s']
    x = S['nums'][i]
    y = S['nums'][-1 - i]
    return f'`nums[{i}] = {x}` 当最大、`nums[-1-{i}] = {y}` 当最小：各有 `s = {s}` 个子序列 → 贡献 `({x} + {y}) × {s}` = =={(x + y) * s}=='


CONFIG = dict(
    num=3428, title='最多 K 个元素的子序列的最值之和', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 贡献法 + 递推',
    tags=['灵神题单'],
    code='''
class Solution:
    def minMaxSums(self, nums: List[int], k: int) -> int:
        MOD = 1_000_000_007
        nums.sort()
        ans = 0
        s = 1
        for i, x in enumerate(nums):
            ans += (x + nums[-1 - i]) * s
            s = (s * 2 - comb(i, k - 1)) % MOD
        return ans % MOD
''',
    setup='''
MOD = 1_000_000_007
MX = 100_000

fac = [0] * MX  # f[i] = i!
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i - 1] * i % MOD

inv_f = [0] * MX  # inv_f[i] = i!^-1
inv_f[-1] = pow(fac[-1], -1, MOD)
for i in range(MX - 1, 0, -1):
    inv_f[i - 1] = inv_f[i] * i % MOD

def comb(n: int, m: int) -> int:
    return fac[n] * inv_f[m] * inv_f[n - m] % MOD if m <= n else 0
''',
    call='Solution().minMaxSums([4,1,3,2,5], 3)',
    expect=150,
    views=[
        dict(type='text', fn=_s_text, size=24, h=110),
        dict(type='array', var='nums', pointers={'i': 'blue', 'len(nums)-1-i': 'pink'}, h=260, label='nums（排序后）',
             color=lambda S, i, v: ('blue' if i == S['i'] else 'pink' if i == len(S['nums']) - 1 - S['i'] else None) if 'i' in S and 'x' in S else None),
        dict(type='text', fn=lambda S: (f"`s` = 从前 `i` 个数里选至多 `k-1 = {S['k'] - 1}` 个的方案数" if 's' in S else ''), size=24, h=60),
    ],
    watch=['i', 'x', ('s', 's', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'MOD = 1_000_000_007': '答案要对 `10^9+7` 取模',
        'nums.sort()': '只关心最值，元素顺序不影响答案 → ==先排序==：`{nums}`',
        'ans = 0': '`ans` 累加所有贡献',
        's = 1': '`s` = 以 `nums[i]` 为最大值的子序列个数，`i = 0` 时只有 `[nums[0]]` 一个：`s = 1`',
        'for i, x in': lambda S, B, r: ('`nums` 枚举完毕，退出循环' if 'i' in B and B.i == S['i'] and B.x == S['x'] and S['i'] == len(S['nums']) - 1 else f"枚举 `nums[i] = {S['x']}` 作为最大值；对称地，`nums[-1-i] = {S['nums'][-1 - S['i']]}` 作为最小值"),
        'ans += (x + nums[-1 - i]) * s': '最大值 `{x}` 和最小值 `{nums[-1-i]}` 的子序列各有 `{s}` 个 → `ans` 加 `({x} + {nums[-1-i]}) × {s}`，得 =={ans}==',
        's = (s * 2': lambda S, B, r: (
            f"`i = {S['i']} < k-1 = {S['k']-1}`：多一个数，选或不选 → `s = 2 × {B.s} = {S['s']}`"
            if S['i'] < S['k'] - 1 else
            f"`i = {S['i']} ≥ k-1`：翻倍后要减去恰好选 `k-1` 个的 `C({S['i']}, {S['k']-1}) = {comb(S['i'], S['k']-1)}` → `s = {S['s']}`"),
        'return ans % MOD': '总和取模：`{ans} % MOD` = =={ret}==',
    },
    cards=dict(
        one_liner='排序后，每个数当最大值和当最小值的次数是对称的',
        complexity='时间 `O(n log n)`，空间 `O(1)`（忽略预处理）',
        problem=['给整数数组 `nums` 和正整数 `k`，对所有长度 ==至多 k== 的子序列，求「最大值 + 最小值」之和，结果对 `10^9+7` 取模',
                 '示例：`nums=[1,2,3], k=2` → `24`',
                 '本视频：`nums=[4,1,3,2,5], k=3` → `150`'],
        quote='由于我们只关心子序列中的最值，所以元素顺序不影响答案，可以先把数组排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后 `nums[i]` 当最大值：其余元素从下标 `[0, i-1]` 选至多 `k-1` 个，方案数 `s_i`',
              '根据对称性，`nums[n-1-i]` 当最小值的个数也是 `s_i`，一起算',
              '`s_i` 不用暴力求和：`s_{i+1} = 2·s_i`，当 `i ≥ k-1` 时再减去 `C(i, k-1)`'],
        summary=['时间 `O(n log n)`，瓶颈是排序；递推 `s` 让每步 `O(1)`',
                 '`s` 的递推：新数可选可不选；`i ≥ k-1` 时选上它会让原来恰好 `k-1` 个的变成 `k` 个，要减掉',
                 '组合数靠预处理阶乘和逆元，预处理放在 setup 里（未追踪），原文还有一种每步 `O(k)` 暴力求和的写法',
                 '`s` 取模后可能为负的情况由 Python 的 `%` 自动处理'],
    ),
)
