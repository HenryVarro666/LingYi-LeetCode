CONFIG = dict(
    num=3916, title='锯齿形数组的总数 III', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='DP + 拉格朗日插值',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        MOD = 1_000_000_007

        # 3699. 锯齿形数组的总数 I
        def dp(k: int) -> int:
            f = [1] * k

            for i in range(1, n):
                if i % 2:  # 增
                    pre = 0
                    for j, v in enumerate(f):
                        f[j] = pre % MOD
                        pre += v
                else:  # 减
                    suf = 0
                    for j in range(k - 1, -1, -1):
                        v = f[j]
                        f[j] = suf % MOD
                        suf += v

            return sum(f) * 2 % MOD

        k = r - l + 1
        if k <= n + 1:
            return dp(k)

        xs = list(range(1, n + 2))
        ys = [dp(x) for x in xs]
        return self.lagrange(xs, ys, k)

    # 传入 n 次多项式 f(x) 上的 n+1 个点 (xs[i], ys[i])，返回 f(k)
    def lagrange(self, xs: list[int], ys: list[int], k: int) -> int:
        MOD = 1_000_000_007
        n = len(xs)
        fk = 0
        for i in range(n):
            a, b = ys[i], 1
            for j in range(n):
                if i != j:
                    a = a * (k - xs[j]) % MOD  # 分子
                    b = b * (xs[i] - xs[j]) % MOD  # 分母
            fk += a * pow(b, -1, MOD)
        return fk % MOD
''',
    call='Solution().zigZagArrays(3, 1, 10)',
    expect=570,
    views=[
        dict(type='text', fn=lambda S: ('拉格朗日：`f(k) = Σ ys[i] · Π (k − xs[j]) / (xs[i] − xs[j])`' if 'fk' in S else
                                        'dp(k)：`f[j]` = 以第 j 小的数结尾的方案数' if 'f' in S else
                                        '先用 DP 算出前 n+1 个点，再插值'), size=24, h=56),
        dict(type='array', var='f', label='f（dp 数组，蓝 = j）', pointers={'j': 'blue'}, cell=70, h=130),
        dict(type='array', var='xs', label='xs（插值点的 x）', cell=70, h=120,
             color=lambda S, i, v: 'blue' if 'fk' in S and i == S.get('i') else None),
        dict(type='array', var='ys', label='ys（S(x) = dp(x) 的值）', cell=70, h=120,
             color=lambda S, i, v: 'blue' if 'fk' in S and i == S.get('i') else None),
        dict(type='text', fn=lambda S: (f"当前点：`x = {S['xs'][S['i']]}`，`a`（分子）= {S['a']}，`b`（分母）= {S['b']}　`fk = {S['fk']}`"
                                        if 'fk' in S and 'a' in S and 'b' in S else ''), size=22, h=56),
    ],
    watch=[('k', lambda S: S['_inner'].get('k'), 'cyan'), ('i', lambda S: S['_inner'].get('i'), 'blue'),
           ('j', lambda S: S['_inner'].get('j'), 'blue'), ('fk', lambda S: S.get('fk'), 'green')],
    captions={
        'f = [1] * k': '`dp({k})`：值域只有 `{k}` 个数；长度为 1 的数组，以每个数结尾各 1 种 → `f = {f}`',
        'for i in range(1, n)': '开始填第 `{i + 1}` 个数（`i = {i}`）',
        'if i % 2': lambda S, B, r: (f'第 {S.i + 1} 个数要比前一个==大==（增）→ 现有 `f = {S.f}` 变成前缀和：`f[j]` = 所有更小位置的 `f` 之和' if S.i % 2 else
                                     f'第 {S.i + 1} 个数要比前一个==小==（减）→ 现有 `f = {S.f}` 变成后缀和：`f[j]` = 所有更大位置的 `f` 之和'),
        'return sum(f) * 2': '转移完 `f = {f}`，`sum(f) = {sum(f)}` 是「先增后减」的个数；「先减后增」与之对称 → 再 ×2 = =={ret}==',
        'k = r - l + 1': '值域 `[{l}, {r}]` 共 `k = {k}` 个数，方案数只和 `k` 有关；真实数据 k 可达 10^9，DP 跑不动 → 改用插值',
        'if k <= n + 1': 'k = {k} > n + 1 = {n + 1}：真实数据里 k 可达 10^9，DP 跑不动 → 改用插值',
        'xs = list': 'S_n(k) 是 ==n 次多项式==：S_1 = k，每做一次前缀和次数 +1。取 `n + 1 = {n + 1}` 个点：`xs = {xs}`',
        'ys = [dp': 'S_n(k) 是 ==n 次多项式==，取 `{n + 1}` 个点 `xs = {xs}`，用 3699 的 `dp` 算出各点的值',
        'return self.lagrange': '`ys = {ys}`：{n + 1} 个点已够确定 {n} 次多项式 → 拉格朗日插值求 `k = {k}` 处的值',
        'fk = 0': '`n = {n}` 个点；`fk` 累加每个点的贡献：点 i 的贡献 = ys[i] × 分子 / 分母',
        'b = b * (xs[i] - xs[j])': '`x = {xs[i]}` 对 `x = {xs[j]}`：分子 × `{k - xs[j]}`，分母 × `{xs[i] - xs[j]}` → `a = {a}`，`b = {b}`',
        'fk += a * pow': '点 {i} 的贡献 = `a / b`；除法用逆元 `pow(b, -1, MOD)` 变成乘法 → `fk = {fk}`（最后再统一取模）',
        'return fk % MOD': '`f({k})` = =={ret}==',
    },
    skip=['for j, v in enumerate(f)', 'for j in range(k - 1', 'v = f[j]', 'pre += v', 'suf += v', 'if i != j', 'for j in range(n)', 'for i in range(n)', 'pre = 0', 'suf = 0', 'for i in range(1, n)', 'f[j] = pre % MOD', 'f[j] = suf % MOD', 'a = a * (k - xs[j])', 'a, b = ys[i], 1', 'MOD = 1_000_000_007', 'n = len(xs)', 'if k <= n + 1', 'xs = list'],
    max_steps=110,
    cards=dict(
        one_liner='方案数是 n 次多项式：算出 n+1 个点，插值求 k 处的值',
        complexity='时间 `O(n^3)`，空间 `O(n)`',
        problem=['构造长度为 `n` 的锯齿形数组，元素在 `[l, r]` 内，相邻不等，且任意连续三个数不单调',
                 '即相邻差正负交替；求方案数模 `10^9+7`，`r - l` 最大 10^9',
                 '本视频：`n = 3, l = 1, r = 10` → `570`'],
        quote='从 S_{i-1}(x) 到 S_i(x)，我们在计算前缀和，这会导致多项式的次数加一。所以 S_n(x) 是 n 次多项式。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`S_1(x) = x`，每做一次前缀和次数加 1 → 答案是 k 的 ==n 次多项式==',
              'k 太大：先用 3699 的 DP 算 `k = 1 ~ n+1` 的 `n+1` 个点，再拉格朗日插值求 `S_n(k)`'],
        summary=['dp 是 `O(nk)`，要算 `n+1` 个点：`O(n^3)`；插值本身 `O(n^2)`（逆元另有 log）',
                 '`f` 初始全 1；最后 `×2` 因为先增后减与先减后增一一对应',
                 '`k <= n + 1` 时直接 DP，不用插值',
                 '分母用 `pow(b, -1, MOD)` 求逆元（Python 3.8+），分子分母每步都要取模',
                 '前置：3699 锯齿形数组的总数 I'],
    ),
)
