def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if S.get('_line') not in (10, 11) or i is None or j is None or 'score' in S:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i - 1, j - 1), (i - 1, j)):
        return 'blue'
    return None


def _fin(S, r, c, v):
    if 'score' in S and 'a' in S and r == S['n'] and c == S.get('i') and S.get('i') is not None:
        return 'green'
    return _cell(S, r, c, v)


def _top(S):
    if 'score' not in S:
        i, j = S.get('i'), S.get('j')
        if i is None or j is None:
            return '`f[i][j]`：前 i 个人分到 j 个节目、==每个节目都有人==的方案数'
        return f"`f[{i}][{j}] = f[{i-1}][{j-1}] + f[{i-1}][{j}] × {j}` = {S['f'][i-1][j-1]} + {S['f'][i-1][j]} × {j}"
    if 'a' in S and S.get('_line', 0) >= 18 and 'res' in S:
        i = S['i']
        return f"`k = {i}`：排列 `A(x,{i}) = {S['a']}` × `f[n][{i}] = {S['f'][S['n']][i]}` × 打分 `y^{i} = {S['score']}`"
    return '再乘上：选节目的排列数 `A(x,k)` 和打分数 `y^k`'


CONFIG = dict(
    num=3317, title='安排活动的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='排列选节目 + 分配 DP',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2414'],
    code='''
class Solution(object):
    def numberOfWays(self, n, x, y):
        
        mod = 10 ** 9 + 7
        
        f = [[0] * (x + 1) for _ in range(n + 1)]
        f[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, x + 1):
                f[i][j] = (f[i - 1][j - 1] + f[i - 1][j] * j) % mod

        score = 1
        a = 1
        res = 0
        for i in range(1, x + 1):
            a = a * (x - i + 1) % mod
            score = score * y % mod
            res = (res + a * f[n][i] % mod * score % mod) % mod
        
        return res
''',
    call='Solution().numberOfWays(3, 3, 4)',
    expect=684,
    skip=['mod = 10', 'f[0][0] = 1', 'score = 1', 'a = 1', 'res = 0'],
    views=[
        dict(type='text', fn=_top, size=27, h=70),
        dict(type='table', var='f', label='f[i][j]：i 个人分到 j 个节目且节目都非空（黄 = 正在算，蓝 = 依赖）', h=360, cell=84,
             rows=['i=0', 'i=1', 'i=2', 'i=3'], cols=['j=0', 'j=1', 'j=2', 'j=3'], color=_fin),
        dict(type='text', fn=lambda S: '第 i 人：==独占一个新节目== `f[i-1][j-1]`，或 ==加入已有 j 个节目之一== `f[i-1][j]·j`', size=26, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('a', 'a', 'cyan'), ('score', 'score', 'orange'), ('res', 'res', 'green')],
    captions={
        'f = [[0]': '`f` 有 `n+1` 行 `x+1` 列，`f[i][j]` = 前 `i` 个人分到 `j` 个节目、每个节目都有人',
        'for i in range(1, n + 1)': lambda S, B, r: (f'考虑前 `i = {S.i}` 个人' if S.get('i') != B.get('i') or 'i' not in B else '前 n 个人都算完'),
        'for j in range(1, x + 1)': lambda S, B, r: f'分到 `j = {S.j}` 个节目' if 'j' in S and S.get('j') != B.get('j') else '这一行算完',
        'f[i][j] =': lambda S, B, r: (f'`f[{S.i}][{S.j}] = f[{S.i-1}][{S.j-1}] + f[{S.i-1}][{S.j}] × {S.j}` = {S.f[S.i-1][S.j-1]} + {S.f[S.i-1][S.j]} × {S.j} = =={S.f[S.i][S.j]}==：第 i 人独占新节目 或 加入已有的 j 个之一'),
        'for i in range(1, x + 1)': lambda S, B, r: (f'枚举恰有 `k = {S.i}` 个节目有人表演' if S.get('i') != B.get('i') else '枚举完毕'),
        'a = a *': '`a = A(x, k)`：节目有区别，==有序选 k 个==，`a` 乘以 `x-k+1` → `{a}`',
        'score = score': '每个有人的节目 y 种打分，`score = y^k` → `{score}`',
        'res = (res': lambda S, B, r: f'`{S.a}` × `f[n][{S.i}] = {S.f[S.n][S.i]}` × `{S.score}` = =={S.a * S.f[S.n][S.i] * S.score}==，累加得 `res = {S.res}`',
        'return res': '把 k 从 1 到 x 的方案数加起来：==`{ret}`==',
    },
    cards=dict(
        one_liner='先选节目（排列），再分人（DP），最后打分',
        complexity='时间 `O(n·x)`，空间 `O(n·x)`',
        problem=['`n` 位表演者各去 `x` 个节目之一，节目可以没人',
                 '有表演者的节目由评委打 `[1, y]` 分，求总方案数（模 `10^9+7`）',
                 '本视频：`n=3, x=3, y=4` → `684`'],
        quote='需要注意的是，由于节目有区分，因此选出前k个节目是排列而不是组合，对应的方案数是A(x, k)。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举恰好 `k` 个节目有人：选节目 `A(x,k)`，打分 `y^k`',
              '分人时 k 个节目已经选定，视为==相同的节目==，用 DP 计算',
              '`f[i][j] = f[i-1][j-1] + f[i-1][j] × j`：第 i 人独占新节目，或加入已有的 j 个之一'],
        summary=['时间 `O(n·x)`，空间 `O(n·x)`',
                 '易错：节目有区别，选节目用排列 `A(x,k)`；分人那步要当作无区别，否则重复计数',
                 '`f` 的列数只开到 `x`：多于 x 个节目没有意义',
                 '每步乘法都取模，防止大数；和灵神一样，`f` 其实就是第二类斯特林数',
                 '对比灵神：灵神预处理到 1000 的整张表，本文只算到 `n × x`'],
    ),
)
