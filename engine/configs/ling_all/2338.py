import math


def _exp(x):
    r, i = [], 2
    while i * i <= x:
        e = 0
        while x % i == 0:
            e += 1
            x //= i
        if e:
            r.append(e)
        i += 1
    if x > 1:
        r.append(1)
    return r


def _fac(x):
    out, i = [], 2
    while i * i <= x:
        e = 0
        while x % i == 0:
            e += 1
            x //= i
        if e:
            out.append(f'{i}^{e}' if e > 1 else str(i))
        i += 1
    if x > 1:
        out.append(str(x))
    return ' × '.join(out) or '1'


def _txt(S):
    if 'x' not in S:
        return '枚举最后一个数 `a[n-1] = x`；商分的乘积 = x，把 x 的质因子放进 n 个位置'
    x, n = S['x'], S['n']
    es = _exp(x)
    form = ' × '.join(f'C({n}+{e}-1, {e})' for e in es) or '1'
    return f'`x = {x} = {_fac(x)}`，指数 `{es}`：方案数 = `{form}`'


CONFIG = dict(
    num=2338, title='统计理想数组的数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='商分 + 质因数分解 + 放球',
    tags=['数论', '组合数学', '难度分 2615'],
    setup='''
MOD = 1_000_000_007
MAX_N = 10_000
MAX_E = 13

# EXP[x] 为 x 分解质因数后，每个质因数的指数
EXP = [[] for _ in range(MAX_N + 1)]
for x in range(2, len(EXP)):
    t = x
    i = 2
    while i * i <= t:
        e = 0
        while t % i == 0:
            e += 1
            t //= i
        if e:
            EXP[x].append(e)
        i += 1
    if t > 1:
        EXP[x].append(1)

# 预处理组合数
C = [[0] * (MAX_E + 1) for _ in range(MAX_N + MAX_E)]
for i in range(len(C)):
    C[i][0] = 1
    for j in range(1, min(i, MAX_E) + 1):
        C[i][j] = (C[i - 1][j] + C[i - 1][j - 1]) % MOD
''',
    code='''
class Solution:
    def idealArrays(self, n: int, maxValue: int) -> int:
        ans = 0
        for x in range(1, maxValue + 1):
            res = 1
            for e in EXP[x]:
                res = res * C[n + e - 1][e] % MOD
            ans += res
        return ans % MOD
''',
    call='Solution().idealArrays(3, 8)',
    expect=38,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var=lambda S: list(range(1, S['maxValue'] + 1)), label='结尾 x = 1 … maxValue（绿 = 已累加进 ans）', cell=90,
             h=170,
             color=lambda S, i, v: ('green' if 'x' in S and (v < S['x'] or (v == S['x'] and S.get('_line') == 8)) else ('blue' if 'x' in S and v == S['x'] else None))),
        dict(type='text', fn=lambda S: f'目前 `ans = {S["ans"]}`' if 'ans' in S else '', h=50),
    ],
    watch=['n', 'maxValue', ('x', 'x', 'blue'), 'e', 'res', ('ans', 'ans', 'green')],
    skip=['res = 1', 'for e in EXP[x]'],
    captions={
        'ans = 0': '`ans` 累计「以每个 x 结尾」的理想数组数',
        'for x in range': lambda S, B, r: ('`x` 枚举完了，所有结尾都累加过' if 'x' in B and B.x == S.x and S.x == S.maxValue else f'枚举最后一个数 `a[n-1] = x = {S.x}`（`res = 1`）：==商分 q 的乘积恰好等于 x=='),
        'res = res * C': lambda S, B, r: f'质因子指数 `e = {S.e}`，放进 `n = {S.n}` 个位置：`C(n+e-1, e) = C({S.n + S.e - 1}, {S.e}) = {math.comb(S.n + S.e - 1, S.e)}` → `res = {S.res}`',
        'ans += res': '以 `{x}` 结尾共 `{res}` 个，累加：`ans = {ans}`',
        'return ans': '`ans % MOD` = `{ret}`：把所有结尾的方案数加起来',
    },
    cards=dict(
        one_liner='相邻两数相除得「商分」，乘积 = 末尾数，质因子放球计数',
        complexity='时间 `O(m log log m)`（不含预处理），空间 `O(1)`',
        problem=['长为 `n` 的数组，每个数在 `1..maxValue`，==每个数被前一个数整除==',
                 '求不同理想数组的个数，对 `10^9+7` 取余',
                 '示例：`n = 2, maxValue = 5` → `10`',
                 '本视频：`n = 3, maxValue = 8` → `38`'],
        quote='定义 q0 = a0，qi = ai / a(i-1)。不同的 a，唯一对应着不同的 q。所有 q 的乘积等于 a(n-1)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['商分：`q` 全是整数，乘积等于最后一个数 `x`，`a` 与 `q` 一一对应',
              '`x` 的每个质因子 `p^e`：把 `e` 个 `p` 放进 `n` 个位置，`C(n+e-1, e)`',
              '枚举 `x = 1..maxValue`，各质因子方案数相乘，再把所有 `x` 加起来',
              '`e ≤ 13`（`2^13 < 10^4 < 2^14`），组合数表预处理一次'],
        summary=['时间 `O(m log log m)`（预处理不计），空间 `O(1)`',
                 'EXP 与组合数表放在类外预处理（视频中放在 setup，不逐行演示），组合数用递推，免去逆元',
                 '`x = 1` 没有质因子，`res = 1`：全是 1 的数组',
                 '易错：答案累加后最后再取模；`C[n+e-1][e]` 的行数要开到 `MAX_N + MAX_E`',
                 '同类：1735. 生成乘积数组的方案数（同样是放球）'],
    ),
)
