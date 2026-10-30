def _fmt(S):
    A, B = S.get('A'), S.get('B')
    if A is None or B is None:
        return '`f[A][B]` = A 有 A 份、B 有 B 份（1 份 25 毫升）时的概率'
    return f'当前状态 `dfs({A}, {B})`：A 剩 {A} 份，B 剩 {B} 份'


def _color(S, i, j, v):
    A, B = S.get('A'), S.get('B')
    if A is None or B is None or A < 0 or B < 0 or A >= len(S['f']) or B >= len(S['f']):
        return None
    if (i, j) == (A, B):
        return 'yellow'
    if v is not None:
        return 'green'
    return None


CONFIG = dict(
    num=808, title='分汤', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='除以 25 化为份数 · 记忆化 dfs',
    tags=['概率 DP、期望 DP', '难度分 2397'],
    code='''
class Solution(object):
    def soupServings(self, N):

        if N >= 5000:
            return 1.0
        
        if N % 25 == 0:
            N = N // 25
        else:
            N = N // 25 + 1
        f = [[None] * (N + 1) for _ in range(N + 1)]
        return self.dfs(N, N, f)

    def dfs(self, A, B, f):
        if A <= 0:
            if B <= 0:
                return 0.5
            else:
                return 1.0
        elif B <= 0:
            return 0.0
        
        if f[A][B] is None:
            f[A][B] = 0.25 * (self.dfs(A - 4, B, f) + self.dfs(A - 3, B - 1, f) + self.dfs(A - 2, B - 2, f) + self.dfs(A - 1, B - 3, f))
            
        return f[A][B]
''',
    call='Solution().soupServings(100)',
    expect=0.71875,
    max_steps=90,
    skip=['f = [[None]'],
    views=[
        dict(type='text', fn=_fmt, size=26, h=60),
        dict(type='table', var='f', label='f[A][B]（黄 = 当前状态，绿 = 已记忆的结果，空 = 还没算）', h=300, cell=96,
             rows=lambda S: [f'A{k}' for k in range(len(S['f']))] if 'f' in S else [],
             cols=lambda S: [f'B{k}' for k in range(len(S['f']))] if 'f' in S else [], color=_color),
        dict(type='calls', h=260),
    ],
    watch=[('N', 'N', 'blue'), ('A', 'A', 'blue'), ('B', 'B', 'pink')],
    captions={
        'if N >= 5000': '`N = {N}`：N 够大时 A 先分完的概率就是 1（5000 是试出来的边界），这里 N 小，继续',
        'N = N // 25': '`{B.N}` 刚好是 25 的倍数 → 每次操作变成份数，`N = {N}` 份',
        'N = N // 25 + 1': '不是 25 的倍数 → 向上取整，`N = {N}` 份',
        'return self.dfs(N, N, f)': '从 `dfs({N}, {N})` 开始，`f` 是记忆表；算好的 `f[A][B]` 之后直接用',
        'return 0.5': '`A = {A}, B = {B.B}` 都不大于 0：同时分完 → 按题意只算一半 ==0.5==',
        'return 1.0': '`A = {A} <= 0` 而 `B = {B.B} > 0`：A 先分完 → ==概率 1==',
        'return 0.0': '`A = {A} > 0` 而 `B = {B.B} <= 0`：B 先分完 → ==概率 0==',
        'f[A][B] = 0.25': '`f[{B.A}][{B.B}]` 还没算过：四种分法等概率 → 先算四个子状态，再 ×0.25 求和',
        'return f[A][B]': '`f[{A}][{B.B}]` = =={ret}==（以后再遇到这个状态直接用）',
    },
    cards=dict(
        one_liner='操作都是 25 的倍数，除以 25 后只剩 4 种分法，二维记忆化',
        complexity='时间 `O((N/25)^2)`，空间 `O((N/25)^2)`',
        problem=['汤 A、B 各 `N` 毫升，每轮等概率 (A,B) 取 (100,0)、(75,25)、(50,50)、(25,75)',
                 '求 ==A 先取完的概率 + 同时取完概率的一半==',
                 '示例：`N = 100` → `0.71875`'],
        quote='注意到每次操作都是25ml的倍数，那么可以将N除上25向上取整，同时将四种操作分别变为A4、A3B1、A2B2以及A1B3。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：A 有 i 份、B 有 j 份开始分汤的概率',
              '四种分法等概率 → `0.25 × (f[i-4][j] + f[i-3][j-1] + f[i-2][j-2] + f[i-1][j-3])`',
              '写完测 `N=5000` 发现答案就是 1：A 的期望消耗更快，`N ≥ 5000` 直接返回 1'],
        summary=['时间 `O((5000/25)^2)`，空间同阶',
                 '边界：`A≤0,B≤0` 为 0.5；`A≤0,B>0` 为 1；`A>0,B≤0` 为 0',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：边界 4451 由程序算出，这里用试出来的 5000，正确性相同'],
    ),
)
