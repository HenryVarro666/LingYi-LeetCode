import math


def _txt(S):
    if 'k' not in S:
        return '每个查询：把 `k` 分解质因数，每个质因子 `p^e` 独立算一次放球'
    n, k, res = S['n'], S['k'], S['res']
    i = S.get('i')
    line = f'`n = {n}`，剩余的 `k = {k}`，当前 `res = {res}`'
    if 'e' in S and S.get('_line') in (10, 11, 12, 13):
        line += f'，质因子 `{i}` 已数到 `e = {S["e"]}`'
    return line


CONFIG = dict(
    num=1735, title='生成乘积数组的方案数', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='质因数分解 + 组合数（放球）',
    tags=['数论', '组合数学', '难度分 2500'],
    setup='''
MOD = 1_000_000_007

# 预处理组合数
c = [[0] * 14 for _ in range(10013)]
c[0][0] = 1
for i in range(1, 10013):
    c[i][0] = 1
    for j in range(1, 14):
        c[i][j] = (c[i - 1][j] + c[i - 1][j - 1]) % MOD
''',
    code='''
class Solution:
    def waysToFillArray(self, queries: List[List[int]]) -> List[int]:
        ans = []
        for n, k in queries:
            res = 1
            i = 2
            while i * i <= k:
                if k % i == 0:  # i 是 k 的质因子
                    e = 0
                    while k % i == 0:
                        e += 1  # 统计有多少个质因子 i
                        k //= i
                    res = res * c[e + n - 1][e] % MOD
                i += 1
            if k > 1:  # 还剩下一个质因子
                res = res * n % MOD
            ans.append(res)
        return ans
''',
    call='Solution().waysToFillArray([[2, 6], [5, 1], [4, 12]])',
    expect=[4, 1, 40],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='queries', label='queries（每项 [n, k]）', cell=140, h=140,
             fmt=lambda v: f'{v[0]},{v[1]}' if isinstance(v, list) else str(v)),
        dict(type='array', var='ans', label='ans（每个查询的方案数）', cell=110,
             color=lambda S, i, v: 'green', h=150),
    ],
    watch=['n', 'k', ('i', 'i', 'blue'), 'e', ('res', 'res', 'green')],
    skip=['i = 2'],
    captions={
        'ans = []': '`ans` 收集每个查询的答案；每个查询独立',
        'for n, k in queries': lambda S, B, r: ('所有查询都处理完了，循环结束' if 'k' in B and B.k == S.k and B.n == S.n else f'取出查询 `n = {S.n}`，`k = {S.k}`：长为 n、乘积为 k 的数组有几种'),
        'res = 1': '`res` 是各质因子方案数的乘积（乘法原理），初始 1',
        'while i * i <= k': lambda S, B, r: (f'`{S.i}² = {S.i * S.i} ≤ {S.k}`，继续试除' if S.i * S.i <= S.k else f'`{S.i}² = {S.i * S.i} > {S.k}`：剩下的 `k` 不会再有更小的因子 → 停止枚举'),
        'if k % i == 0': '`{k} % {i} = {k % i}` → {"==i 是质因子=="if k % i == 0 else "不整除，跳过"}',
        'e = 0': '准备数质因子 `{i}` 的个数 `e`',
        'while k % i == 0': lambda S, B, r: (f'`{S.k} % {S.i} = 0`，还能除' if S.k % S.i == 0 else f'`{S.k} % {S.i} ≠ 0`：质因子 `{S.i}` 除干净了，`e = {S.e}`'),
        'e += 1': '`e = {e}`',
        'k //= i': '`k` 除掉一个 `{i}` → {k}',
        'res = res * c': lambda S, B, r: f'`e = {S.e}` 个 `{S.i}` 放进 `n = {S.n}` 个位置：隔板法 `C(e+n-1, e) = C({S.e + S.n - 1}, {S.e}) = {math.comb(S.e + S.n - 1, S.e)}` → `res = {S.res}`',
        'i += 1': '`i` → {i}',
        'if k > 1': lambda S, B, r: (f'`k = {S.k} > 1`：还剩一个质因子 `{S.k}`（指数 1）' if S.k > 1 else '`k = 1`：质因子都处理完了'),
        'res = res * n': '指数 1：`C(1+n-1, 1) = n = {n}` → `res = {res}`',
        'ans.append': '这个查询的答案 `{res}` 加入 `ans`',
        'return ans': '全部查询处理完：`{ret}`',
    },
    cards=dict(
        one_liner='乘积 k 拆成质因子，每个质因子 p^e 独立「放球」，方案数相乘',
        complexity='单查询时间 `O(√k)`，预处理组合数 `O((N+log K)·log K)`',
        problem=['每个查询 `[n, k]`：构造长为 `n`、元素为正整数、乘积为 `k` 的数组',
                 '求方案数，对 `10^9+7` 取余，返回每个查询的答案',
                 '示例：`[2,6]` → 4（`[1,6] [2,3] [3,2] [6,1]`）',
                 '本视频：`[[2,6],[5,1],[4,12]]` → `[4,1,40]`'],
        quote='把 e 个无区别的小球放到 n 个有区别的盒子中，允许盒子为空。从 i=2 开始枚举，如果 k 能被 i 整除就不断除 i，统计除 i 的次数 e。',
        quote_src='—— 灵茶山艾府题解（节选）',
        idea=['质因子互不影响：每个质因子 `p^e` 的 `e` 个 `p` 分给 `n` 个位置',
              '放球问题：方案数 `C(e + n − 1, e)`；各质因子相乘',
              '`2^13 < 10^4 < 2^14`，所以 `e ≤ 13`，只预处理 `C(·, 0..13)`',
              '枚举到 `i² > k` 就停；剩下的 `k > 1` 是一个指数为 1 的质因子，贡献 `n`'],
        summary=['时间：单个查询 `O(√k)`；空间 `O((N+log K)·log K)`',
                 '组合数表在类外预处理（视频中放在 setup 里，不逐行演示），用 `C(n,m)=C(n-1,m)+C(n-1,m-1)` 递推',
                 '易错：循环里 `k` 被不断除小，答案要在最后用剩余的 `k > 1` 补一个质因子',
                 '写法二：预处理阶乘/逆元 + 最小质因子 LPF，单查询 `O(log k)`',
                 '同类：2338. 统计理想数组的数目（同样的放球模型）'],
    ),
)
