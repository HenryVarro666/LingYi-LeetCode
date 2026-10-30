def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mat, vv = S.get('self.mat'), S.get('self.v')
    cv.text((x0 + 18, y0 + 4), '表格（上 = 单元格内容：数字 / 公式；下 = 本轮已算出的值；黄框 = 正在 calc 的格子）', 21, T['muted'], bold=True)
    if mat is None or vv is None:
        return
    m, n = S['self.m'], S['self.n']
    cw = min(220, (x1 - x0 - 100) / n)
    ch = min(110, (y1 - y0 - 120) / m)
    sx, sy = x0 + 70, y0 + 100
    cur = (S['x'], S['y']) if 'x' in S and 'y' in S and S.get('_line') in calc_lines else None
    for j in range(1, n + 1):
        cv.text((sx + (j - 0.5) * cw, sy - 8), chr(64 + j), 26, T['dim'], anchor='mb', bold=True)
    for i in range(1, m + 1):
        cv.text((sx - 14, sy + (i - 0.5) * ch), i, 26, T['dim'], anchor='rm', bold=True)
        for j in range(1, n + 1):
            X, Y = sx + (j - 1) * cw, sy + (i - 1) * ch
            c = mat[i][j]
            val = vv[i][j]
            isf = not (c[0][0] == '-' or '0' <= c[0][0] <= '9')
            out = T['yellow'] if cur == (i, j) else T['border']
            cv.rect((X + 4, Y + 4, X + cw - 4, Y + ch - 4), fill=(52, 46, 70) if isf else T['panel2'], r=10, outline=out, width=4 if cur == (i, j) else 2)
            txt = ('=' + '+'.join(c)) if isf else c[0]
            cv.text((X + cw / 2, Y + ch * 0.33), txt, 22 if isf else 28, T['purple'] if isf else T['text'], anchor='mm', mono=True, bold=True)
            cv.text((X + cw / 2, Y + ch * 0.72), '—' if val is None else val, 30, T['dim'] if val is None else T['green'], anchor='mm', bold=True, mono=True)


calc_lines = tuple(range(15, 38))

CONFIG = dict(
    num=631, title='设计Excel求和公式', difficulty='Hard', category='设计',
    author='yiduobo', technique='记忆化搜索 · 每次重算',
    tags=[],
    code='''
class Excel(object):

    def __init__(self, height, width):
        self.m = height
        self.n = ord(width) - 64
        self.mat = [[["0"] for j in range(self.n + 1)] for i in range(self.m + 1)]
        self.v = [[None] * (self.n + 1) for _ in range(self.m + 1)]

    def set(self, row, column, val):
        x = row
        y = ord(column) - 64
        self.mat[x][y] = [str(val)]

    def calc(self, x, y):
        if self.v[x][y] is None:
            if self.mat[x][y][0][0] == '-' or '0' <= self.mat[x][y][0][0] <= '9':
                self.v[x][y] = int(self.mat[x][y][0])
            else:
                s = 0
                for part in self.mat[x][y]:
                    p = part.find(':')
                    if p == -1:
                        next_y = ord(part[0]) - 64
                        next_x = int(part[1:])
                        s += self.calc(next_x, next_y)
                    else:
                        
                        y1 = ord(part[0]) - 64
                        x1 = int(part[1: p])
                        y2 = ord(part[p + 1]) - 64
                        x2 = int(part[p + 2:])
                        for i in range(x1, x2 + 1):
                            for j in range(y1, y2 + 1):
                                s += self.calc(i, j)
                self.v[x][y] = s
        
        return self.v[x][y]

    def get(self, row, column):
        x = row
        y = ord(column) - 64
        self.v = [[None] * (self.n + 1) for _ in range(self.m + 1)]
        return self.calc(x, y)

    def sum(self, row, column, numbers):
        x = row
        y = ord(column) - 64
        self.mat[x][y] = numbers[:]
        self.v = [[None] * (self.n + 1) for _ in range(self.m + 1)]
        return self.calc(x, y)
''',
    call='''e = Excel(3, 'B')
out = []
e.set(1, 'A', 2)
out.append(e.sum(2, 'B', ['A1', 'A1:B1']))
e.set(1, 'B', 3)
out.append(e.get(2, 'B'))
out''',
    expect=[4, 7],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='calls', label='正在执行（递归 calc 展开依赖）', h=170),
    ],
    watch=['x', 'y', 's', ('part', 'part', 'purple')],
    skip=['x = row', 'y = ord(column) - 64', 'self.m = height', 'self.n = ord(width)', 'next_y =', 'next_x =', 'y1 =', 'x1 =', 'y2 =', 'x2 =', 'self.v = [[None]', 's = 0', 'self.mat = [[['],
    max_steps=140,
    captions={
        12: '`set`：格子改成纯数字 `{val}`，之前的公式被覆盖',
        48: '`sum`：格子 `({x}, {y})` 改成公式，记下要加的项 `{numbers}`',
        15: lambda S, B, r: ('`calc({}, {})`：本轮还没算过，往下算'.format(S.x, S.y) if S.self.v[S.x][S.y] is None
                             else '`calc({}, {})`：本轮已算过 = =={}==，直接用缓存'.format(S.x, S.y, S.self.v[S.x][S.y])),
        16: lambda S, B, r: ('格子 `({}, {})` 内容是数字 `{}`'.format(S.x, S.y, S.self.mat[S.x][S.y][0]) if S.self.mat[S.x][S.y][0][0] == '-' or '0' <= S.self.mat[S.x][S.y][0][0] <= '9'
                             else '格子 `({}, {})` 是公式 `{}`：要把每一项算出来再相加'.format(S.x, S.y, S.self.mat[S.x][S.y])),
        17: '数字格子：直接记下 `v[{x}][{y}] = {self.v[x][y]}`',
        20: lambda S, B, r: ('公式的各项都读完了' if B.get('part') == S.part and S.get('p') is not None else '读公式里的下一项 `{}`'.format(S.part)),
        21: '`find` 冒号：`-1` 说明是单个格子，否则是区间',
        22: lambda S, B, r: ('`{}` 是单个格子 → 递归 `calc`'.format(S.part) if S.p == -1 else '`{}` 含 `:`，是矩形区间 → 枚举里面每个格子'.format(S.part)),
        25: '单个格子：递归算 `({next_x}, {next_y})` 的值再加进 `s`',
        32: lambda S, B, r: ('所有行枚举完' if B.get('i') == S.i and S.j == S.y2 else '区间：逐行枚举，行 `{}`（范围 `{}` 到 `{}`）'.format(S.i, S.x1, S.x2)),
        33: lambda S, B, r: ('这一行的列枚举完' if B.get('j') == S.j and S.j == S.y2 else '区间：逐列枚举，列 `{}`（范围 `{}` 到 `{}`）'.format(S.j, S.y1, S.y2)),
        34: '区间里的格子 `({i}, {j})`：递归 `calc` 后累加到 `s`',
        35: '公式各项加完：格子 `({x}, {y})` 的值记为 =={s}==，本轮之后直接用缓存',
        37: '`calc` 返回 `{ret}`',
        42: '`get`：先把缓存 `v` ==整体清空==，保证用到的是最新数据',
        49: '`sum`：同样先清空缓存 `v`',
        43: '从目标格子出发 `calc({x}, {y})`',
        50: '设好公式后，从该格子出发 `calc({x}, {y})`',
    },
    cards=dict(
        one_liner='不维护依赖图：每次求值前清空缓存，递归算出来',
        complexity='`calc` 最坏 `O((mn)^2)`，总计 `O(K·(mn)^2)`',
        problem=['`Excel(height, width)`：表格全是 0；`set` 设置数字；`get` 取值',
                 '`sum(r, c, numbers)`：把格子设为公式，`numbers` 里是 `A1` 或 `A1:B2` 区间，返回和',
                 '公式格子的值要随被引用格子的变化而变化'],
        quote='直接对于每次求值操作，都枚举所有单元格并执行记忆化搜索就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['公式 = 若干项之和；每项是单个格子或矩形区间',
              '`calc(x, y)` 递归：数字直接返回，公式就把每个被引用格子再 `calc`',
              '`get` / `sum` 前先把缓存 `v` 清空：改过的格子立刻反映到所有公式上'],
        summary=['最坏复杂度 `O(K·(mn)^2)`，但题目限制总操作只有 100 次，够用',
                 '易错：区间 `A1:B2` 要枚举矩形里每个格子；缓存 `v` 每次操作前要重置',
                 '易错：`set` 要把格子改回数字，公式格子被覆盖后不再依赖别的格子',
                 '进阶做法是二维树状数组 + 拓扑序，但最坏复杂度并不更好'],
    ),
)
