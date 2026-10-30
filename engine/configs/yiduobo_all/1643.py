def _tbl(S):
    c = S.get('c')
    return c if c else [[0]]


def _cell(S, r, col, v):
    if 'm' in S and 'index' in S and S['n'] >= 0 and (r, col) == (S['m'] + S['n'] - 1, S['n'] - 1) and S['n'] > 0 and S['_line'] in (17, 18, 21):
        return 'yellow'
    return 'green' if v else None


def _txt(S):
    if 'res' not in S:
        return '指令 = 从 m+n 个位置里选 m 个放 `V`，其余放 `H`'
    m, n, k = S['m'], S['n'], S['k']
    if m + n == 0:
        return '走到终点，指令拼完'
    return f'还剩 `V` × {m}，`H` × {n}，要找剩下指令里的第 `k = {k}` 条'


CONFIG = dict(
    num=1643, title='第K条最小指令', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='组合数计数 · 逐位确定',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def kthSmallestPath(self, destination, k):

        m, n = destination
        c = [[0] * (m + n + 1) for _ in range(m + n + 1)]

        for i in range(m + n + 1):
            for j in range(i + 1):
                if j == 0:
                    c[i][j] = 1
                else:
                    c[i][j] = c[i - 1][j] + c[i - 1][j - 1]
        
        res = []
        l = m + n
        for index in range(l):
            if n > 0 and k <= c[m + n - 1][n - 1]:
                res.append('H')
                n -= 1
            else:
                k -= c[m + n - 1][n - 1]
                res.append('V')
                m -= 1
        
        return ''.join(res)
''',
    call='Solution().kthSmallestPath([2, 3], 8)',
    expect='VHHVH',
    views=[
        dict(type='array', var='res', label='已确定的指令 res（H 蓝 / V 粉）', cell=96, h=150,
             color=lambda S, i, v: 'blue' if v == 'H' else 'pink'),
        dict(type='table', var=_tbl, label='组合数表 c[i][j]（黄 = 当前以 H 开头的指令数 C(m+n−1, n−1)）', color=_cell, h=330, cell=76),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('m (V)', 'm', 'pink'), ('n (H)', 'n', 'blue'), ('k', 'k', 'orange'), ('index', 'index')],
    skip=['for i in range(m + n + 1)', 'for j in range(i + 1)', 'if j == 0', 'c[i][j]'],
    captions={
        'm, n = destination': '`m = {m}` 次 `V`（向下），`n = {n}` 次 `H`（向右）；`H` 字典序比 `V` 小',
        'c = [[0]': '准备组合数表 `c[i][j]` = C(i, j)',
        'res = []': '组合数表已按 `c[i][j] = c[i-1][j] + c[i-1][j-1]` 填好。`res` 存逐位确定的指令',
        'l = m + n': '一共 `{l}` 步，逐位确定',
        'for index in range(l)': lambda S, B, r: ('每一位都确定了' if len(S.res) == S.l else f'确定第 `{S.index + 1}` 位：以 `H` 开头还是 `V` 开头？'),
        'if n > 0 and k <= c': lambda S, B, r: (f'以 `H` 开头的指令有 `C({S.m + S.n - 1}, {S.n - 1}) = {S.c[S.m + S.n - 1][S.n - 1]}` 条，排在最前；`k = {S.k}` 落在里面 → ==这一位是 H=='
                                                if S.n > 0 and S.k <= S.c[S.m + S.n - 1][S.n - 1]
                                                else (f'`n = 0`，没有 `H` 了，只能 `V`' if S.n == 0
                                                      else f'以 `H` 开头的指令只有 `C({S.m + S.n - 1}, {S.n - 1}) = {S.c[S.m + S.n - 1][S.n - 1]}` 条，`k = {S.k}` 排在它们后面 → ==这一位是 V==')),
        "res.append('H')": '确定这一位是 `H`',
        'n -= 1': '`H` 用掉一次 → 还剩 `n = {n}`',
        'k -= c': '跳过所有以 `H` 开头的指令：`k` 减去 `{B.k - k}` → `k = {k}`',
        "res.append('V')": '确定这一位是 `V`',
        'm -= 1': '`V` 用掉一次 → 还剩 `m = {m}`',
        'return': "拼成字符串 `{''.join(res)}` → 第 K 条最小指令",
    },
    max_steps=60,
    cards=dict(
        one_liner='以 H 开头的指令排在前面：数一数有多少条，就知道第 k 条该选 H 还是 V',
        complexity='时间 `O((m+n)^2)`，空间 `O((m+n)^2)`',
        problem=['从 `(0,0)` 走到终点 `destination = [m, n]`：`H` 向右，`V` 向下',
                 '每条路线对应一个由 `H`、`V` 组成的指令，把所有指令按字典序排序，返回第 `k` 条（`k` 从 1 开始）',
                 '示例：`destination = [2,3], k = 3` → `"HHVVH"`；本视频 `k = 8` → `"VHHVH"`'],
        quote='排在前面的 C(m + n - 1, n - 1) 条指令是以 H 开头的，而后面剩下的指令则是以 V 开头。',
        quote_src='—— yiduobo 题解原文',
        idea=['总共 `C(m+n, m)` 条指令：从 `m+n` 个位置里挑 `m` 个放 `V`',
              '以 `H` 开头的有 `C(m+n-1, n-1)` 条，字典序最前',
              '`k` 在其中 → 第一位是 `H`；否则是 `V`，并把 `k` 减去这些指令数',
              '剩下的是更小的同类问题，重复直到走完'],
        summary=['时间 `O((m+n)^2)`（建组合数表），空间 `O((m+n)^2)`',
                 '`n == 0` 时不能再放 `H`，所以条件里要先判断 `n > 0`',
                 '`k` 是 1 开始的序号，所以比较用 `k <= 条数`',
                 '视频里为了节省时间，杨辉三角预处理的循环没有逐行演示',
                 '题面：库里没有题面，题意据 yiduobo 文章与 LeetCode 原题整理'],
    ),
)
