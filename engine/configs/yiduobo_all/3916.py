CONFIG = dict(
    num=3916, title='锯齿形数组的总数 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前后缀和 DP + 拉格朗日插值',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def zigZagArrays(self, n, l, r):
        
        mod = 10 ** 9 + 7

        def calc(r):
            f = []
            s = []
            for v in range(r + 1):
                f.append(v)
                if not s:
                    s.append(f[-1])
                else:
                    s.append(s[-1] + f[-1])

            for length in range(3, n + 1):
                for v in range(r + 1):
                    if length % 2 == 0:
                        if v == 0:
                            f[v] = 0
                        else:
                            f[v] = s[v - 1]
                    else:
                        f[v] = s[-1] - s[v]
                        if f[v] < 0:
                            f[v] += mod
            
                s = []
                for v in range(r + 1):
                    if not s:
                        s.append(f[v])
                    else:
                        s.append(s[-1] + f[v])
                        if s[-1] >= mod:
                            s[-1] -= mod

            res = s[-1] + s[-1]
            if res >= mod:
                res -= mod
            return res

        def quick_pow(base, p):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = res * res % mod
            if p % 2 == 1:
                res = res * base % mod
            return res

        r -= l
        if r <= n:
            return calc(r)
        
        x = []
        y = []
        for v in range(n + 1):
            x.append(v)
            y.append(calc(v))

        res = 0
        for p in range(n + 1):
            a, b = 1, 1
            for index in range(n + 1):
                if p == index:
                    continue

                a = a * (r - x[index]) % mod
                b = b * (x[p] - x[index]) % mod
            
            a = a * y[p] % mod

            res = (res + a * quick_pow(b, mod - 2) % mod) % mod
        
        return res
''',
    call='Solution().zigZagArrays(3, 1, 10)',
    expect=570,
    views=[
        dict(type='text', fn=lambda S: ('calc(r)：值域 `0 ~ r`，`f[v]` = 以 v 结尾的个数，`s` = f 的前缀和' if 'f' in S and 's' in S else
                                        '用 `g(0) ~ g(n)` 这 n+1 个点，插值得到 `g(r)`'), size=24, h=56),
        dict(type='array', var='f', label='f（以 v 结尾的方案数）', cell=70, h=100),
        dict(type='array', var='s', label='s（f 的前缀和）', cell=70, h=100),
        dict(type='array', var='x', label='x（取点：0 ~ n）', cell=70, h=110,
             color=lambda S, i, v: 'blue' if 'p' in S and 'a' in S and i == S['p'] else None),
        dict(type='array', var='y', label='y（y[i] = calc(x[i])）', cell=70, h=140,
             color=lambda S, i, v: 'blue' if 'p' in S and 'a' in S and i == S['p'] else None),
        dict(type='text', fn=lambda S: (f"第 `{S['p']}` 项：`a`（分子）= {S['a']}，`b`（分母）= {S['b']}　`res = {S['res']}`"
                                        if 'p' in S and 'a' in S and 'b' in S and 'index' in S else ''), size=22, h=50),
    ],
    watch=[('r', 'r', 'cyan'), ('length', lambda S: S.get('length'), 'blue'), ('p', lambda S: S.get('p'), 'blue'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    skip=[7, 8, 9, 10, 11, 12, 14, 17, 18, 19, 20, 22, 24, 25, 26, 29, 30, 31, 33, 34, 38, 39, 43, 44, 45, 46, 48, 49, 50, 51, 52,
          55, 58, 59, 62, 69, 60, 61, 65, 66, 67, 68, 71],
    captions={
        54: '`r -= l`：把值域平移成 `0 ~ r`，只看大小关系；现在 `r = {r}`',
        4: '模数 `10^9 + 7`',
        16: lambda S, B, ret: (f'算点 `g({S.r})`：用 `0 ~ {S.r}` 构造 vvvv 型。长度为 2 时 `f[v] = v` → `f = {S.f}`，`s` 是前缀和 `{S.s}`' if 'length' not in B
                               else f'`length` 从 3 循环到 `n`，处理完了：`f = {S.f}`'),
        28: '`length = {length}` 是奇数：当前元素是==谷值==，`f[v] = s[-1] − s[v]`（比上一个小的数之和）→ `f = {f}`',
        37: '`s` 重新做前缀和 = {s}；`s[-1] = {s[-1]}` 是 vvvv 型的总数，^^^^ 型一一对应 → ==×2== = {res}',
        40: '`calc({r}) = {res}`',
        64: '已有点 `y = {y}`（对应 `x = {x}`）；`res` 累加每个点的拉格朗日项',
        72: '第 `{p}` 项，对点 `x = {x[index]}`：分子 × `r − {x[index]}` = `{r - x[index]}`，分母 × `{x[p] - x[index]}` → `a = {a}`，`b = {b}`',
        74: '分子再乘上 `y[{p}] = {y[p]}` → `a = {a}`',
        76: '这一项 = `a / b`：除法用 `quick_pow(b, mod − 2)` 求逆元（费马小定理）→ `res = {res}`',
        78: '`g({r}) = {res}`：就是 `n = 3`、值域 `1 ~ 10` 的锯齿数组总数 ==570==',
    },
    max_steps=100,
    cards=dict(
        one_liner='r 太大没法 DP：先算小的 g(0)~g(n)，拉格朗日插值求 g(r)',
        complexity='时间 `O(n^3)`，空间 `O(n)`',
        problem=['构造长度为 `n` 的数组，元素在 `[l, r]`，相邻不同，任意三个连续数不单调',
                 '即相邻差正负交替，求方案数模 `10^9+7`，`r` 可达 10^9',
                 '本视频：`n = 3, l = 1, r = 10` → `570`'],
        quote='每一轮都是前缀和或者后缀和，……必然是一个以r为参数n次的多项式g[r]……先计算出g[0]到g[n]，相当于使用n + 1个点来唯一确定一条n次的曲线。',
        quote_src='—— yiduobo 题解原文',
        idea=['值域平移成 `0 ~ r`（`r -= l`）；vvvv 型和 ^^^^ 型一一对应 → 只算一种再 ×2',
              '`f[v]` = 以 v 结尾的个数，奇数位取后缀和、偶数位取前缀和',
              '`r` 小直接 `calc(r)`；否则算 `g(0) ~ g(n)` 再拉格朗日插值'],
        summary=['时间 `O(n^3)`：`n+1` 次 `calc`，每次 `O(nr)`；插值 `O(n^2 log mod)`',
                 '`r -= l` 之后值域是 `0 ~ r`，共 `r + 1` 个数；`r <= n` 时直接 `calc`',
                 '`f[v]` 做减法后可能为负，要 `+ mod` 修正；前缀和每步都要取模',
                 '分母用 `quick_pow(b, mod - 2)` 求逆元；原文代码在 Python 3 下无需修改',
                 '对比灵神：灵神取点 `k = 1 ~ n+1`，用内置 `pow(b, -1, MOD)` 求逆元'],
    ),
)
