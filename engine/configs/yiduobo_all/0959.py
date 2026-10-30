GRID = [' /', '/ ']
COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange', 'red']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = GRID
    n = len(g)
    fa = S.get('fa')
    cv.text((x0 + 18, y0 + 4), '每格切成 4 块（1 上 2 右 3 下 4 左）；同色 = 已合并到一起', 22, T['muted'], bold=True)
    cell = min(250, (x1 - x0 - 60) / n, (y1 - y0 - 110) / n)
    sx = x0 + ((x1 - x0) - cell * n) / 2
    sy = y0 + 56
    roots = {}
    if fa is not None:
        for p in range(1, len(fa)):
            r = _root(fa, p)
            roots.setdefault(r, []).append(p)
    big = {r: k for k, r in enumerate(sorted(r for r, m in roots.items() if len(m) > 1))}
    cur = S.get('square')
    for i in range(n):
        for j in range(n):
            X, Y = sx + j * cell, sy + i * cell
            tl, tr, br, bl, c = (X, Y), (X + cell, Y), (X + cell, Y + cell), (X, Y + cell), (X + cell / 2, Y + cell / 2)
            base = (i * n + j) * 4
            tris = {1: (tl, tr, c), 2: (tr, br, c), 3: (br, bl, c), 4: (bl, tl, c)}
            for k, pts in tris.items():
                p = base + k
                col = T['panel2']
                if fa is not None:
                    r = _root(fa, p)
                    if r in big:
                        col = T[COLS[big[r] % len(COLS)]]
                cv.poly(list(pts), col)
                mx = sum(q[0] for q in pts) / 3
                my = sum(q[1] for q in pts) / 3
                cv.text((mx, my), p, 22, T['bg'] if col != T['panel2'] else T['dim'], anchor='mm', bold=True, mono=True)
            cv.rect((X, Y, X + cell, Y + cell), outline=T['border'], width=2)
            ch = g[i][j]
            if ch == '/':
                cv.line([bl, tr], T['text'], 8)
            elif ch == '\\':
                cv.line([tl, br], T['text'], 8)
            if cur is not None and base + 1 == cur:
                cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), outline=T['yellow'], width=6)


def _info(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    roots = {_root(fa, p) for p in range(1, len(fa))}
    return f'目前不同的祖先（= 区域数）：`{len(roots)}`'


CONFIG = dict(
    num=959, title='由斜杠划分区域', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='每格拆 4 块 + 并查集',
    tags=[],
    code='''
class Solution(object):
    def regionsBySlashes(self, grid):

        n = len(grid)
        fa = list(range(n * n * 4 + 1))

        for i in range(n):
            for j in range(n - 1):
                left_pos = (i * n + j) * 4 + 2
                right_pos = (i * n + j + 1) * 4 + 4
                fa[right_pos] = left_pos
        
        for i in range(n - 1):
            for j in range(n):
                up_pos = (i * n + j) * 4 + 3
                donw_pos = ((i + 1) * n + j) * 4 + 1
                fa[donw_pos] = up_pos
        
        for i in range(n):
            for j in range(n):
                square = (i * n + j) * 4 + 1
                if grid[i][j] == ' ':
                    self.union(square, square + 1, fa)
                    self.union(square, square + 2, fa)
                    self.union(square, square + 3, fa)
                elif grid[i][j] == '/':
                    self.union(square, square + 3, fa)
                    self.union(square + 1, square + 2, fa)
                else:
                    self.union(square, square + 1, fa)
                    self.union(square + 2, square + 3, fa)
        
        res = 0
        for i in range(1, n * n * 4 + 1):
            if self.find(i, fa) == i:
                res += 1
        
        return res
    
    def find(self, now, fa):
        if fa[now] != now:
            fa[now] = self.find(fa[now], fa)
        
        return fa[now]
    
    def union(self, x, y, fa):
        fa_x = self.find(x, fa)
        fa_y = self.find(y, fa)
        if fa_x < fa_y:
            fa[fa_y] = fa_x
        else:
            fa[fa_x] = fa_y
''',
    call=f'Solution().regionsBySlashes({GRID})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_info, size=26, h=50),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('square', 'square', 'yellow'), ('res', 'res', 'green')],
    skip=['if fa_x < fa_y', 'if fa[now] != now', 'return fa[now]', 'fa[now] = self.find', 'n = len', 'fa = list', 'left_pos =', 'up_pos =', 'res = 0', 'fa_x = self', 'fa_y = self'],
    max_steps=110,
    captions={
        'right_pos =': '右边格子的 4 号块：`{right_pos}`',
        'fa[right_pos] = left_pos': '左右相邻：左格的 2（右块）和右格的 4（左块）==无论如何都连通==：`fa[{right_pos}] = {left_pos}`',
        'fa[donw_pos] = up_pos': '上下相邻：上格的 3（下块）和下格的 1（上块）==无论如何都连通==：`fa[{donw_pos}] = {up_pos}`',
        'square = ': '这一格的 1 号块编号 `square = {square}`',
        22: lambda S, B, r: f"格子 `({S.i},{S.j})` = `{S.grid[S.i][S.j]!r}`：" + ('空白 → 4 块全合并' if S.grid[S.i][S.j] == ' ' else '不是空白，往下看'),
        23: '空白：1 和 2 合并',
        24: '空白：1 和 3 合并',
        25: '空白：1 和 4 合并 → 整格是一个区域',
        26: '格子 `({i},{j})` 不是空白，看是不是 `/`',
        27: '`/`：1 和 4 合并（左上角的块）',
        28: '`/`：2 和 3 合并（右下角的块）',
        29: '格子 `({i},{j})` 是 `\\`',
        30: '`\\`：1 和 2 合并（右上角）',
        31: '`\\`：3 和 4 合并（左下角）',
        'fa[fa_y] = fa_x': '`fa[{fa_y}] = {fa_x}`：把较大的祖先挂到较小的下面',
        'fa[fa_x] = fa_y': '`fa[{fa_x}] = {fa_y}`：把祖先并到一起（已同祖先则不变）',
        'if self.find(i, fa) == i': lambda S, B, r: f'块 `{S.i}` 的祖先是{"自己 → 它是一个区域的代表" if S.fa[S.i] == S.i else "别人 → 已并入其他区域"}',
        'res += 1': '又数到一个区域：`res` = =={res}==',
        'return res': '不同的祖先个数就是区域数 → =={res}==',
    },
    cards=dict(
        one_liner='不用算几何：每格切成 4 块，斜杠只是在合并这些块',
        complexity='时间 `O(n² α)`，空间 `O(n²)`',
        problem=['`n × n` 的格子，每格是 `/`、`\\` 或空格，斜杠把正方形分开',
                 '求这些斜杠把整个方块划分成几个区域',
                 '本视频：`[" /", "/ "]` → `2`'],
        quote='直接按照几何做法是比较复杂的，不妨试着逆向思维，根据斜杠的情况对格子进行合并。',
        quote_src='—— yiduobo 题解原文',
        idea=['每格按两条对角线顺时针分成 4 块：1 上、2 右、3 下、4 左',
              '`/` 合并 1&4、2&3；`\\` 合并 1&2、3&4；空白 1–4 全合并',
              '相邻格：左格的 2 与右格的 4、上格的 3 与下格的 1 永远相连；最后数祖先个数'],
        summary=['时间 `O(n² α)`，空间 `O(n²)`，总共 `4n²` 个块',
                 '块编号从 1 开始，所以 `fa` 开 `4n² + 1` 个位置',
                 '相邻格的连接先直接赋 `fa`，之后再用 `union` 合并格内的块',
                 '原文为 Python 2 写法，`fa = range(...)` 已改为 `fa = list(range(...))`'],
    ),
)
