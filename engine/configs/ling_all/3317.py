_ST = [[0] * 5 for _ in range(5)]  # 与代码里预处理相同的递推，只画前 5×5
_ST[0][0] = 1
for _i in range(1, 5):
    for _j in range(1, _i + 1):
        _ST[_i][_j] = _ST[_i - 1][_j - 1] + _j * _ST[_i - 1][_j]


def _top(S):
    if 'perm' not in S or 'i' not in S or S.get('_line', 0) < 17:
        return '答案 = 枚举有表演者的节目数 `i`：`A(x,i) × S(n,i) × y^i`'
    i = S['i']
    return (f"`i = {i}`：排列 `{S['perm']}` × 斯特林数 `S({S['n']},{i}) = {_ST[S['n']][i]}` × 打分 `{S['pow_y']}`"
            f" → 本项 =={S['perm'] * _ST[S['n']][i] * S['pow_y']}==")


def _tbl(S):
    return _ST


def _cur(S):
    n = S.get('n')
    return n if n is not None and n <= 4 else None


CONFIG = dict(
    num=3317, title='安排活动的方案数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='枚举非空节目数 + 第二类斯特林数',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2414'],
    code='''
MOD = 1_000_000_007
MX = 1001

s = [[0] * MX for _ in range(MX)]
s[0][0] = 1
for i in range(1, MX):
    for j in range(1, i + 1):
        s[i][j] = (s[i - 1][j - 1] + j * s[i - 1][j]) % MOD

class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        ans = 0
        perm = pow_y = 1
        for i in range(1, min(n, x) + 1):
            perm = perm * (x + 1 - i) % MOD
            pow_y = pow_y * y % MOD
            ans += perm * s[n][i] * pow_y
        return ans % MOD
''',
    call='Solution().numberOfWays(3, 3, 4)',
    expect=684,
    views=[
        dict(type='text', fn=_top, size=27, h=70),
        dict(type='table', var=_tbl, label='斯特林数表 s[n][i]（只画前 5×5，预处理已填好）', h=330, cell=80,
             rows=['n=0', 'n=1', 'n=2', 'n=3', 'n=4'], cols=['i=0', 'i=1', 'i=2', 'i=3', 'i=4'],
             color=lambda S, r, c, v: ('yellow' if (r == S.get('n') and c == S.get('i') and S.get('_line', 0) > 14) else None)),
        dict(type='text', fn=lambda S: '`S(i,j) = S(i-1,j-1) + j·S(i-1,j)`：第 i 人 ==单独成组== 或 ==放进前面 j 组之一==', size=26, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('perm', 'perm', 'cyan'), ('pow_y', 'pow_y', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累加每个 `i` 的方案数；`s[n][i]` 在类外预处理好了（画面右侧表格）',
        'perm = pow_y = 1': '`perm` 滚动算排列数 `A(x,i)`，`pow_y` 滚动算 `y^i`，都从 1 开始',
        'for i in range': lambda S, B, r: (f'枚举有表演者的节目数 `i = {S.i}`（最多 `min(n, x)` 个）' if S.get('i') != B.get('i') or 'i' not in B else '枚举完毕'),
        'perm = perm': '`A(x,i) = A(x,i-1) × (x+1-i)`：从 x 个节目里==有序==选 i 个 → `perm = {perm}`',
        'pow_y = pow_y': '每个非空节目有 y 种打分 → `y^i` = `{pow_y}`',
        'ans += ': lambda S, B, r: f'`{S.perm}` × `S({S.n},{S.i}) = {_ST[S.n][S.i]}` × `{S.pow_y}` = =={S.perm * _ST[S.n][S.i] * S.pow_y}==，累加得 `ans = {S.ans}`',
        'return ans': '三个子问题相乘再求和，最后取模：=={ret}==',
    },
    cards=dict(
        one_liner='枚举非空节目数 i：选节目 × 分人 × 打分',
        complexity='预处理 `O(N^2)`，查询时间 `O(min(n,x))`',
        problem=['`n` 位表演者各被安排到 `x` 个节目之一，节目可以没人',
                 '评委给每个==有表演者==的节目打 `[1, y]` 分，求总方案数（模 `10^9+7`）',
                 '示例：`n=3, x=3, y=4` → `684`（本视频同）'],
        quote='枚举有 i 个非空（有表演者）的节目，原问题可以拆分成三个问题：排列数、第二类斯特林数、打分方案数。三者相乘得 A(x,i)·S(n,i)·y^i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选节目要==有顺序==：因为斯特林数 `S(n,i)` 只管“分成 i 个无序非空组”',
              '`S(i,j)`：第 i 人单独一组 `S(i-1,j-1)`，或放进 j 组之一 `j·S(i-1,j)`',
              '三个问题独立，乘法原理；`i` 从 1 枚举到 `min(n,x)`'],
        before=[dict(heading='预处理：斯特林数表', lines=['代码开头先把 `s[0..1000][0..1000]` 全算好', '`S(0,0)=1`，其余按递推式填表', '这一段有 50 万次循环，视频里直接跳过，只展示表的左上角'])],
        summary=['预处理 `O(N^2)`，`N = 1000`；每次查询 `O(min(n,x))`',
                 '易错：节目有区别，要用排列数 `A(x,i)` 而不是组合数',
                 '`ans` 不在循环里取模，最后统一 `% MOD`（Python 大整数不会溢出）',
                 '`i` 从 1 开始：`n ≥ 1` 时至少有一个节目有人',
                 '同类题：3343、3539（多重集排列 + 计数 DP）'],
    ),
)
