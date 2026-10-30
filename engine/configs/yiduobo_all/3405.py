import itertools

N, M, K = 5, 3, 2
EXP = sum(1 for a in itertools.product(range(1, M + 1), repeat=N)
          if sum(a[i - 1] == a[i] for i in range(1, N)) == K)


def _text(S):
    I = S.get('_inner', {})
    if 'base' in I:
        return f'快速幂：`{I["base"]}^{I["p"]}`（对半拆：`p >> 1`，奇数再多乘一个 `base`）'
    if 'res' in S and 'v' in S and 'inv' in S:
        return f'`C(n-1, k)` 逐项乘：`res = res * (n - v) * inv[v]`，已乘到 `v = {S["v"]}`'
    if 'inv' in S:
        return '先用线性递推求 1..k 的逆元，再用它们做除法'
    return f'`n = {S["n"]}, m = {S["m"]}, k = {S["k"]}`：答案 = `C(n-1,k) * m * (m-1)^(n-k-1)`'


CONFIG = dict(
    num=3405, title='统计恰好有 K 个相等相邻元素的数组数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='组合数 + 线性求逆元 + 快速幂',
    tags=['灵神题单', '难度分 2310'],
    code='''
class Solution(object):
    def countGoodArrays(self, n, m, k):
        
        mod = 10 ** 9 + 7
        fact = [1]
        inv = [1]

        def quick_pow(base, p, mod):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p >> 1, mod)
            res *= res
            res %= mod
            if p & 1:
                res *= base
                res %= mod
            return res

        inv = [1, 1]
        for v in range(2, k + 1):
            inv.append(-(mod // v) * inv[mod % v] % mod)
        
        res = 1
        for v in range(1, k + 1):
            res *= n - v
            res %= mod
            res *= inv[v]
            res %= mod

        res *= m
        res %= mod
        res *= quick_pow(m - 1, n - k - 1, mod)
        return res % mod
''',
    call=f'Solution().countGoodArrays({N}, {M}, {K})',
    expect=EXP,
    views=[
        dict(type='text', fn=_text, size=26, h=90),
        dict(type='array', var=lambda S: S.get('inv', []), label='inv[v]：v 在模 mod 下的逆元', h=220, cell=140,
             pointers={'v': 'blue'}),
        dict(type='array', var=lambda S: [S['res']] if 'res' in S and 'quick_pow' not in S.get('_inner', {}) and 'base' not in S.get('_inner', {}) else [], label='res（当前结果）', h=170, cell=160),
        dict(type='calls', h=230, hide=('countGoodArrays',)),
    ],
    watch=[('v', 'v', 'blue'), ('res', 'res', 'green')],
    skip=['res %= mod', 'fact = ', 'inv = [1]', 'mod = 10'],
    captions={
        'inv = [1, 1]': '`inv[1] = inv[0] = 1`：逆元表从 1 开始。递推公式 `inv[v] = -(mod // v) * inv[mod % v]`',
        'inv.append': '`inv[{v}] = -({mod // v}) * inv[{mod % v}] % mod`：用更小的 `inv[mod % v]` 推出来，==不需要快速幂==',
        'res *= n - v': '`C(n-1, k)` 的分子：乘上 `n - v = {n - v}`',
        'res *= inv[v]': '分母 `v` 的除法，换成乘它的逆元 `inv[{v}]`；`res` 现在是 `C(n-1, {v})`',
        'res *= m': '再乘 `arr[0]` 的 `m = {m}` 种选择',
        'res *= quick_pow': '其余每个位置有 `m - 1` 种：乘 `(m-1)^(n-k-1)`，用快速幂',
        'if p == 0': lambda S, B, ret: f'`p = {S["p"]}`：{"指数为 0，结果是 1" if S["p"] == 0 else "指数不是 0，继续"}',
        'if p == 1': lambda S, B, ret: f'`p = {S["p"]}`：{"指数为 1，直接返回 base" if S["p"] == 1 else "指数大于 1，对半拆"}',
        'res = quick_pow': '先算 `base^(p // 2)`，再平方',
        'res *= res': '平方 → 得到 `base^(2 * (p >> 1))`',
        'if p & 1': lambda S, B, ret: ('`p` 是奇数，还差一个 `base`' if S['p'] & 1 else '`p` 是偶数，不用多乘'),
        'return base': '`p = 1`，直接返回 `{base}`',
        'return 1': '`p = 0` → 返回 `1`',
        'return res': lambda S, B, ret: f'返回 `{ret}`',
    },
    cards=dict(
        one_liner='先选相同的位置，再给其他位置填数',
        complexity='时间 `O(k + log(n-k))`，空间 `O(k)`',
        problem=['长为 `n`、取值 `[1, m]` 的数组，==恰好== `k` 个下标 `i` 满足 `arr[i-1] == arr[i]`',
                 '求这样的数组个数，对 `10^9 + 7` 取模',
                 '示例：`n=3, m=2, k=1` → `4`'],
        quote='根据题目的要求，首先需要从1到n - 1这些下标中选出k个下标，这些下标上的元素与前一个元素相同。这样一来，一共有C(n - 1, k)种选择的方案。',
        quote_src='—— yiduobo 题解',
        idea=['选 `k` 个位置与前一个相同：`C(n-1, k)`',
              '其余 `n-k` 个位置：`arr[0]` 有 `m` 种，后面 `n-k-1` 个各 `m-1` 种',
              '答案 `C(n-1,k) * m * (m-1)^(n-k-1)`',
              '算 `C` 要除法：用 `O(k)` 的线性递推求 1..k 的逆元，避开费马小定理'],
        after=[dict(heading='线性求逆元', lines=[
            '`p = x*v + y`，所以 `x*v + y ≡ 0`，两边同乘 `inv[v]*inv[y]`',
            '得 `inv[v] = -x * inv[y]`，其中 `x = p // v`，`y = p % v < v`',
            '`inv[y]` 已经算过，所以可以从小到大递推（要求 `p` 是质数）'])],
        summary=['时间 `O(k + log(n-k))`，空间 `O(k)`',
                 '易错点：「相同」的位置有 `k` 个，不同的有 `n-1-k` 个；指数是 `n-k-1`',
                 '`inv[v] = -(mod // v) * inv[mod % v] % mod`，Python 的 `%` 结果非负，直接可用',
                 '原文已是 Python 3 兼容写法，代码未改动；`fact` 在原文里没用到'],
    ),
)
