PIZZA = ['A.', 'AA']


def _has(S, x1, y1, x2, y2):
    p = S['pizza']
    return any(p[a][b] == 'A' for a in range(x1, x2 + 1) for b in range(y1, y2 + 1))


def _txt(S):
    if 'c' not in S:
        return '`prefix_s[x][y]` = 左上角 `(0,0)` 到 `(x,y)` 的苹果数；用它 `O(1)` 判断一块披萨有没有苹果'
    c = S['c']
    if 'i' not in S or 'j' not in S:
        return f'`f[c][i][j]`：左上角 `(i,j)`、右下角 `(m-1,n-1)` 的披萨切 `c = {c}` 刀的方案数'
    i, j = S['i'], S['j']
    if c == 0:
        return f'`c = 0`：不用再切，`(i,j)=({i},{j})` 这块有苹果就是 1 种'
    return f'`c = {c}`：`f[{i}][{j}]` = 横切各种切法 + 竖切各种切法，切掉的那块必须有苹果，剩下的看上一层 `g`'


def _chk(S, B, r):
    i, j, m, n = S.i, S.j, S.m, S.n
    ok = _has(S, i, j, m - 1, n - 1)
    return f'`(i,j)=({i},{j})` 这块披萨{"==有苹果==" if ok else "没有苹果"} → `f[{i}][{j}]` = =={1 if ok else 0}=='


def _h(S, B, r):
    i, j, h, n = S.i, S.j, S.h, S.n
    ok = _has(S, i, j, h, n - 1)
    return f'横切：切掉第 `{i}`~`{h}` 行（`h = {h}`），这块{"==有苹果==" if ok else "没有苹果 → 不算"}'


def _v(S, B, r):
    i, j, v, m = S.i, S.j, S.v, S.m
    ok = _has(S, i, j, m - 1, v)
    return f'竖切：切掉第 `{j}`~`{v}` 列（`v = {v}`），这块{"==有苹果==" if ok else "没有苹果 → 不算"}'


def _fc(S, i, j, v):
    if 'i' in S and 'j' in S and i == S['i'] and j == S['j']:
        return 'yellow'
    return None


CONFIG = dict(
    num=1444, title='切披萨的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='三维 DP + 二维前缀和 + 滚动数组',
    tags=['灵神题单', '难度分 2127'],
    code='''
class Solution(object):
    def ways(self, pizza, k):

        m = len(pizza)
        n = len(pizza[0])

        prefix_s = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if pizza[i][j] == 'A':
                    delta = 1
                else:
                    delta = 0

                if i == 0:
                    if j == 0:
                        prefix_s[i][j] = delta
                    else:
                        prefix_s[i][j] = prefix_s[i][j - 1] + delta
                elif j == 0:
                    prefix_s[i][j] = prefix_s[i - 1][j] + delta
                else:
                    prefix_s[i][j] = prefix_s[i - 1][j] + prefix_s[i][j - 1] - prefix_s[i - 1][j - 1] + delta
        
        mod = 10 ** 9 + 7
        for c in range(k):
            f = [[0] * n for _ in range(m)]
            for i in range(m - 1, -1, -1):
                for j in range(n - 1, -1, -1):
                    if c == 0:
                        if self.check(i, j, m - 1, n - 1, prefix_s):
                            f[i][j] = 1
                        else:
                            f[i][j] = 0
                    else:
                        for h in range(i, m - 1):
                            if self.check(i, j, h, n - 1, prefix_s):
                                f[i][j] += g[h + 1][j]
                                f[i][j] %= mod

                        for v in range(j, n - 1):
                            if self.check(i, j, m - 1, v, prefix_s):
                                f[i][j] += g[i][v + 1]
                                f[i][j] %= mod
                
            g = f[:]

        return f[0][0]

    def check(self, x1, y1, x2, y2, prefix_s):
        if x1 == 0:
            if y1 == 0:
                s = prefix_s[x2][y2] > 0
            else:
                s = prefix_s[x2][y2] - prefix_s[x2][y1 - 1]
        elif y1 == 0:
            s = prefix_s[x2][y2] - prefix_s[x1 - 1][y2]
        else:
            s = prefix_s[x2][y2] - prefix_s[x1 - 1][y2] - prefix_s[x2][y1 - 1] + prefix_s[x1 - 1][y1 - 1]
        
        return s > 0
''',
    call=f'Solution().ways({PIZZA!r}, 2)',
    expect=2,
    max_steps=80,
    skip=['m = len(pizza)', 'n = len(pizza[0])', 'delta = ', 'for j in range', 'mod = 10',
          'if x1 == 0', 'if y1 == 0', 'elif y1 == 0', 'else:', 's = prefix_s', 'return s > 0', 'f[i][j] %= mod', 'if c == 0',
          'g = f[:]'],
    views=[
        dict(type='text', fn=_txt, size=22, h=60),
        dict(type='table', var='pizza', label='pizza（绿 = 苹果）', h=170, cell=56,
             color=lambda S, i, j, v: 'green' if v == 'A' else None),
        dict(type='table', var='prefix_s', label='prefix_s（前缀苹果数）', h=170, cell=56),
        dict(type='table', var='f', label='f（本层，黄 = 正在算）', h=170, cell=56, color=_fc),
        dict(type='table', var='g', label='g（上一层 = 切 c−1 刀）', h=170, cell=56),
    ],
    watch=[('c', 'c', 'cyan'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('h', 'h', 'yellow'), ('v', 'v', 'yellow')],
    captions={
        'prefix_s = [[0]': '`prefix_s[x][y]`：以 `(0,0)` 为左上角、`(x,y)` 为右下角的苹果数，先全填 0',
        'for i in range(m):': lambda S, B, r: ('先预处理二维前缀和，之后判断任意一块有没有苹果只要 `O(1)`' if 'i' not in B else (f'下一行 `i = {S.i}`' if S.i != B.i else '前缀和算完了')),
        'if pizza[i][j]': lambda S, B, r: f'`pizza[{S.i}][{S.j}] = {S.pizza[S.i][S.j]!r}` → 这一格 `delta = {1 if S.pizza[S.i][S.j] == "A" else 0}`',
        'prefix_s[i][j] = delta': '左上角那格：`prefix_s[{i}][{j}] = {prefix_s[i][j]}`',
        'prefix_s[i][j] = prefix_s[i][j - 1] + delta': '第一行：只加左边 → `prefix_s[{i}][{j}] = {prefix_s[i][j]}`',
        'prefix_s[i][j] = prefix_s[i - 1][j] + delta': '第一列：只加上边 → `prefix_s[{i}][{j}] = {prefix_s[i][j]}`',
        'prefix_s[i - 1][j] + prefix_s[i][j - 1] - ': '容斥：上 + 左 − 左上 + 自己 → `prefix_s[{i}][{j}]` = =={prefix_s[i][j]}==',
        'for c in range(k)': lambda S, B, r: ('`k` 层都算完了' if S.get('c') == B.get('c') and 'f' in S and B.get('c') is not None
                                              else f'`c = {S.c}`：先算切 `{S.c}` 刀的方案数' ),
        'f = [[0] * n': '新开一层 `f`，上一层的结果留在 `g` 里',
        'for i in range(m - 1': lambda S, B, r: (f'`i = {S.i}`：从下往上、从右往左算，`f[c][i][j]` 要用到更靠右/下的上一层状态' if not any(any(r) for r in S.f) or S.i != B.get('i') else '这一层算完了'),
                'if self.check(i, j, m - 1, n - 1': _chk,
        'f[i][j] = 1': '剩下这块有苹果 → 切 0 刀的方案数 `f[{i}][{j}] = 1`',
        'f[i][j] = 0': '没有苹果 → 0 种',
        'for h in range': lambda S, B, r: (f'没有可横切的位置（`h` 的范围是空的），跳过横切' if S.i >= S.m - 1 else f'枚举横切：切掉第 `{S.i}` 行到第 `h` 行，`h` 从 `{S.i}` 到 `{S.m - 2}`'),
        'if self.check(i, j, h, n - 1': _h,
        'f[i][j] += g[h + 1][j]': '切掉的那块有苹果 → 剩下的从 `(h+1, j) = ({h+1}, {j})` 开始，再切 `c−1` 刀：加上 `g[{h+1}][{j}] = {g[h+1][j]}`，`f[{i}][{j}] = {f[i][j]}`',
        'for v in range': lambda S, B, r: (f'没有可竖切的位置，跳过竖切' if S.j >= S.n - 1 else f'枚举竖切：切掉第 `{S.j}` 列到第 `v` 列，`v` 从 `{S.j}` 到 `{S.n - 2}`'),
        'if self.check(i, j, m - 1, v': _v,
        'f[i][j] += g[i][v + 1]': '切掉的那块有苹果 → 剩下的从 `(i, v+1) = ({i}, {v+1})` 开始：加上 `g[{i}][{v+1}] = {g[i][v+1]}`，`f[{i}][{j}] = {f[i][j]}`',
        'return f[0][0]': '披萨整块切 `k−1` 刀的方案数 `f[0][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='剩下的披萨右下角不变，只看左上角 (i,j) 和还要切几刀',
        complexity='时间 `O(k·m·n·(m+n))`，空间 `O(mn)`（滚动数组）',
        problem=['`pizza` 里 `A` 是苹果，`.` 是空；切 `k−1` 刀分成 `k` 块',
                 '竖切给左边、横切给上边，每块都要 ==至少一个苹果==',
                 '求方案数；本视频：`["A.","AA"]`，`k = 2` → `2`'],
        quote='每次切割只能横切或者纵切，同时每次都会留下下面或者右边的部分，那么很自然想到使用动态规划，令f[c][i][j]表示对于以(i, j)为左上角，(m - 1, n - 1)为右下角的披萨切c刀的方案数',
        quote_src='—— yiduobo 题解原文',
        idea=['`c = 0`：这块有苹果就是 1，没有就是 0',
              '`c > 0`：枚举横切/竖切掉的那块，==有苹果才算==，再加上 `f[c−1]` 里剩下那块的方案数',
              '「有没有苹果」用二维前缀和 `O(1)` 判断；每层只依赖上一层，所以用 `g` 滚动'],
        summary=['时间 `O(k·m·n·(m+n))`：状态 `kmn` 个，每个枚举 `m+n` 个切点',
                 '易错：前缀和第一行/第一列要单独处理，否则下标 `-1` 会绕回末尾',
                 '易错：`f` 每层要重新开；`g = f[:]` 保存上一层再进入下一层',
                 '对比灵神：灵神用后缀和把每个状态降到 `O(1)`；yiduobo 保留了枚举切点',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行（原文未带 `:type` 注释）'],
    ),
)
