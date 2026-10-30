FR = [[1, 2, 3, 4], [5, 6, 8, 7], [9, 10, 11, 12], [13, 14, 15, 16]]
PH2 = 30  # phase 2 begins at this line


def _ph2(S):
    return S.get('_line', 0) >= PH2


def _pre(S, d):
    if S['_line'] < PH2:
        a = S.i + d
        return f'来自上一列第 `{a}` 行：`g[{a}] = {S.g[a]}` → `pre = {S.pre}`'
    a = S.j + d
    return f'来自上一行第 `{a}` 列：`g[{a}] = {S.g[a]}` → `pre = {S.pre}`'


def _fset(S, x):
    if S.i == S.j:
        return f'`({S.i},{S.j})` 在对角线上：水果归小朋友 1，只传递 `pre` → `f[{x}] = {S.f[x]}`'
    return f'`f[{x}] = {S.pre} + {S.fruits[S.i][S.j]}` = =={S.f[x]}==（`pre` 加本格水果）'


def _ix(S):
    return S['i'] if S['_line'] < PH2 else S['j']


def _cell(S, r, c, v):
    if 'g' not in S:
        return 'green' if r == c else None
    if 'i' not in S:
        return 'green' if r == c else None
    i = S['i']
    j = S['j']
    if S['_line'] < PH2:
        if (r, c) == (i, j):
            return 'yellow'
        if c == j - 1 and abs(r - i) <= 1:
            return 'blue'
    else:
        if (r, c) == (i, j):
            return 'yellow'
        if r == i - 1 and abs(c - j) <= 1:
            return 'blue'
    return 'green' if r == c else None


CONFIG = dict(
    num=3363, title='最多可收集的水果数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='对角线置零 + 两遍滚动数组 DP',
    tags=['灵神题单', '网格图 DP', '难度分 2200'],
    code='''
class Solution(object):
    def maxCollectedFruits(self, fruits):

        n = len(fruits)
        
        f = [-1] * n
        f[n - 1] = fruits[n - 1][0]
        for j in range(1, n):
            g = f[:]
            f = [-1] * n
            for i in range(max(n - 1 - j, j), n):
                pre = -1
                if i - 1 >= 0 and g[i - 1] != -1:
                    pre = max(pre, g[i - 1])
                if g[i] != -1:
                    pre = max(pre, g[i])
                if i + 1 < n and g[i + 1] != -1:
                    pre = max(pre, g[i + 1])
                
                if pre == -1:
                    continue
                
                if i == j:
                    f[i] = pre
                else:
                    f[i] = pre + fruits[i][j]
        
        res = f[-1]

        f = [-1] * n
        f[n - 1] = fruits[0][n - 1]
        for i in range(1, n):
            g = f[:]
            f = [-1] * n
            for j in range(max(n - 1 - i, i), n):
                pre = -1
                if j - 1 >= 0 and g[j - 1] != -1:
                    pre = max(pre, g[j - 1])
                if g[j] != -1:
                    pre = max(pre, g[j])
                if j + 1 < n and g[j + 1] != -1:
                    pre = max(pre, g[j + 1])
                
                if pre == -1:
                    continue
                
                if i == j:
                    f[j] = pre
                else:
                    f[j] = pre + fruits[i][j]

        res += f[-1]

        
        for i in range(n):
            res += fruits[i][i]
        
        return res
''',
    call=f'Solution().maxCollectedFruits({FR})',
    expect=100,
    skip=['for i in range(max', 'for j in range(max', 'pre = -1', 'continue', 'if pre == -1', 'f = [-1] * n',
          'if i - 1 >= 0', 'if g[i] != -1', 'if i + 1 < n', 'if j - 1 >= 0', 'if g[j] != -1', 'if j + 1 < n',
          'if i == j', 'for i in range(n)'],
    views=[
        dict(type='grid', var='fruits', label='fruits（绿 = 对角线；黄 = 正在算的格；蓝 = 它可能来自的格）', cell=84, h=340, color=_cell),
        dict(type='array', var=lambda S: S.get('g'), label='g：上一轮的 f（-1 = 到不了）', cell=70, h=150,
             color=lambda S, k, v: 'blue' if 'i' in S and abs(k - _ix(S)) <= 1 and S['_line'] not in (28, 52) and S['_line'] not in (8, 32) else None),
        dict(type='array', var=lambda S: S.get('f'), label='f：本轮结果', cell=70, h=150,
             color=lambda S, k, v: 'yellow' if 'i' in S and k == _ix(S) and S['_line'] not in (28, 52) and S['_line'] not in (8, 32) else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('pre', 'pre'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'f[n - 1] = fruits[n - 1][0]': '小朋友 3 的起点 `(n-1, 0)`：`f[{n-1}] = {f[n-1]}`，`f[i]` = 走到当前列第 `i` 行的最大水果，`-1` 表示到不了',
        'for j in range(1, n)': lambda S, B, r: (f'`j = {S.j}`：按列往右推，每一列只依赖前一列' if S.j != B.get('j') else '所有列都推完了'),
        'g = f[:]': '`g` 存上一轮的结果，`f` 重新开始算这一轮（滚动数组）',
        'pre = max(pre, g[i - 1])': lambda S, B, r: _pre(S, -1),
        'pre = max(pre, g[i])': lambda S, B, r: _pre(S, 0),
        'pre = max(pre, g[i + 1])': lambda S, B, r: _pre(S, 1),
        'pre = max(pre, g[j - 1])': lambda S, B, r: _pre(S, -1),
        'pre = max(pre, g[j])': lambda S, B, r: _pre(S, 0),
        'pre = max(pre, g[j + 1])': lambda S, B, r: _pre(S, 1),
        'f[i] = pre': lambda S, B, r: _fset(S, S.i),
        'f[j] = pre': lambda S, B, r: _fset(S, S.j),
        'res = f[-1]': '小朋友 3 走到 `(n-1,n-1)`：`res = {res}`',
        'f[n - 1] = fruits[0][n - 1]': '小朋友 2 的起点 `(0, n-1)`：`f[{n-1}] = {f[n-1]}`，这次按行推进',
        'for i in range(1, n)': lambda S, B, r: (f'`i = {S.i}`：按行往下推，每一行只依赖上一行' if S.i != B.get('i') else '所有行都推完了'),
        'res += f[-1]': '小朋友 2 走到终点：`res = {res}`',
        'res += fruits[i][i]': '把对角线 `({i},{i})` 的 `{fruits[i][i]}` 加给小朋友 1：`res = {res}`',
        'return res': '三个小朋友一共收集 `{res}`',
    },
    cards=dict(
        one_liner='对角线先让左上小朋友拿走，另两位只做滚动数组 DP',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n × n` 房间，三个小朋友从 `(0,0)`、`(0,n-1)`、`(n-1,0)` 出发',
                 '都走 `n-1` 步到 `(n-1,n-1)`，同一房间水果只能收一次',
                 '示例：`[[1,2,3,4],[5,6,8,7],[9,10,11,12],[13,14,15,16]]` → `100`'],
        quote='对于从左上角出发的小朋友而言，其只能沿着对角线从左上角一路走到右下角。',
        quote_src='—— yiduobo 题解原文',
        idea=['另外两位走不过对角线，只会和走对角线的人重叠',
              '所以对角线直接让第一位收走，DP 时==对角线格子不再加水果==',
              '`f[i]` 表示走到当前这一列的第 `i` 行的最大水果，从上一轮的三个格子转移'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`-1` 表示这个状态到不了；`pre == -1` 就跳过',
                 '`i == j` 的对角线格子只传递 `pre`，不加水果',
                 '原文本身就是 Python 3 可运行的写法，代码未改'],
    ),
)
