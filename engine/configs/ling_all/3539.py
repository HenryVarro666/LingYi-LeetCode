def _top(S):
    if 'left_m' not in S:
        return '把 `m` 个下标分给 `nums` 的每个位置，`S = Σ c_i·2^i` 的二进制要恰有 `k` 个 1'
    return (f"还要选 ==`{S['left_m']}`== 个下标，`x = S >> i = {S['x']}`，还差 ==`{S['left_k']}`== 个 1")


CONFIG = dict(
    num=3539, title='魔法序列的数组乘积之和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多重集排列 + 数位 DP（右移 i 位）',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2694'],
    code='''
MOD = 1_000_000_007
MX = 31

fac = [0] * MX  # fac[i] = i!
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i - 1] * i % MOD

inv_f = [0] * MX  # inv_f[i] = i!^-1
inv_f[-1] = pow(fac[-1], -1, MOD)
for i in range(MX - 1, 0, -1):
    inv_f[i - 1] = inv_f[i] * i % MOD

class Solution:
    def magicalSum(self, m: int, k: int, nums: List[int]) -> int:
        n = len(nums)
        pow_v = [[1] * (m + 1) for _ in range(n)]
        for i, v in enumerate(nums):
            for j in range(1, m + 1):
                pow_v[i][j] = pow_v[i][j - 1] * v % MOD

        @cache
        def dfs(i: int, left_m: int, x: int, left_k: int) -> int:
            c1 = x.bit_count()
            if c1 + left_m < left_k:  # 可行性剪枝
                return 0
            if i == n or left_m == 0 or left_k == 0:  # 无法继续选数字
                return 1 if left_m == 0 and c1 == left_k else 0
            res = 0
            for j in range(left_m + 1):  # 枚举 I 中有 j 个下标 i
                # 这 j 个下标 i 对 S 的贡献是 j * pow(2, i)
                # 由于 x = S >> i，转化成对 x 的贡献是 j
                bit = (x + j) & 1  # 取最低位，提前从 left_k 中减去，其余进位到 x 中
                r = dfs(i + 1, left_m - j, (x + j) >> 1, left_k - bit)
                res += r * pow_v[i][j] * inv_f[j]
            return res % MOD

        return dfs(0, m, 0, k) * fac[m] % MOD
''',
    call='Solution().magicalSum(2, 2, [5, 4])',
    expect=40,
    skip=['c1 = x.bit_count()', 'if i == n or', 'for j in range(left_m + 1)', 'pow_v = ', 'for i, v in enumerate', 'for j in range(1, m + 1)', 'pow_v[i][j] = ', 'n = len(nums)', 'res = 0'],
    max_steps=60,
    views=[
        dict(type='text', fn=_top, size=25, h=100),
        dict(type='array', var='nums', label='nums（蓝 = 当前枚举的下标 i）', cell=90, h=190, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') and 'left_m' in S else None),
        dict(type='calls', h=250),
    ],
    watch=[('i', 'i', 'blue'), ('left_m', 'left_m', 'cyan'), ('x', 'x', 'orange'), ('left_k', 'left_k', 'pink'), ('j', 'j'), ('res', 'res', 'green')],
    captions={
        'return dfs(0, m, 0, k)': lambda S, B, r: (f'`dfs(0, m, 0, k) × m!` = =={r}==' if r is not None else '入口 `dfs(0, m, 0, k)`：从下标 0 开始，还要选 `m` 个，`x = 0`，还需 `k` 个 1'),
        'if c1 + left_m < left_k': lambda S, B, r: (f'`c1 + left_m = {S.c1 + S.left_m} < {S.left_k}`：再怎么选 1 也凑不够 → ==剪枝返回 0==' if S.c1 + S.left_m < S.left_k
                                                  else f'`c1 + left_m = {S.c1 + S.left_m} ≥ left_k = {S.left_k}`：还有可能凑够，继续'),
        'return 1 if left_m == 0': lambda S, B, r: (f'`left_m = {S.left_m}`，`x` 里有 `c1 = {S.c1}` 个 1，`left_k = {S.left_k}`：' + ('==恰好合法== → 返回 1' if S.left_m == 0 and S.c1 == S.left_k else '不合法 → 返回 0')),
        'bit = ': '选 `j = {j}` 个下标 `i`：`x` 变成 `{x} + {j} = {x + j}`，最低位 `bit = {bit}` 先从 `left_k` 扣掉，其余进位',
        'r = dfs': '`x` 右移一位，递归 `dfs({B.i + 1}, {B.left_m - B.j}, {(B.x + B.j) >> 1}, {B.left_k - B.bit})`',
        'res += r': '贡献 `r × nums[i]^j / j!` → `res = {res}`',
        'return res % MOD': '`dfs({i}, {left_m}, {x}, {left_k})` = =={ret}==',
    },
    cards=dict(
        one_liner='右移 i 位记状态：低位的 1 提前数掉',
        complexity='时间 `O(n m^3 k)`，空间 `O(n m^2 k)`',
        problem=['选 `m` 个下标 `I`（可重复），要求 `Σ 2^I[j]` 的二进制==恰有 `k` 个 1==',
                 '序列乘积 `∏ nums[I[j]]`，求所有合法序列的乘积之和（模 `10^9+7`）',
                 '本视频：`m=2, k=2, nums=[5,4]` → `40`'],
        quote='在递归过程中只需保存 S 右移 i 位的结果，而不是原始的 S，从而大幅减少状态个数！',
        quote_src='—— 灵茶山艾府题解',
        idea=['选 `c_i` 个下标 `i`：贡献 `nums[i]^c_i`，排列数 `m!/∏c_i!`，把 `m!` 提出来每项独立',
              '从小到大枚举 i：之后加的数 `≥ 2^i`，不会影响低位 → ==低位的 1 提前统计==',
              '状态 `(i, left_m, x, left_k)`：`x` = S 右移 i 位；加 `j` 个后 `bit = (x+j)&1` 扣掉，`(x+j)>>1` 带进位'],
        before=[dict(heading='预处理：阶乘与逆元', lines=['`fac[i] = i!`，`inv_f[i] = (i!)^-1 mod p`', '多重集排列数里要除以 `j!`，取模下用逆元', '这一段在类外，视频里跳过'])],
        summary=['时间 `O(n m^3 k)`，空间 `O(n m^2 k)`（滚动数组可更省）',
                 '可行性剪枝：`c1 + left_m < left_k` 直接返回 0，砍掉大量状态',
                 '易错：`bit` 要提前从 `left_k` 扣掉，进位 `(x+j)>>1` 带到下一个下标',
                 '最后要乘 `m!`（提出来的分子），累加时乘的是 `nums[i]^j / j!`',
                 '灵神另给了 1:1 翻译的递推写法，本视频演示记忆化搜索；同类题 3343'],
    ),
)
