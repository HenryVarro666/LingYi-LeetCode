GRID = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
GETS_LINES = (43, 44, 45, 46, 72)


def _seg(S):
    """get_s 正在求和的斜边：('left'/'right', s_pos, start, end, 格子列表)"""
    if S.get('_line') not in GETS_LINES:
        return None
    if not all(k in S for k in ('s', 's_pos', 'start', 'end')):
        return None
    n = len(S['grid'][0])
    kind = 'left' if S['s'] == S.get('left_s') else 'right'
    p, a, b = S['s_pos'], S['start'], S['end']
    if kind == 'left':
        cells = [(r, p - r) for r in range(a, b + 1)]
    else:
        cells = [(r, r - p + n - 1) for r in range(a, b + 1)]
    return kind, p, a, b, cells


def _table(cv, T, X, Y, tab, cell, title, plus=None, minus=None, row_hi=None, color=None):
    cv.text((X, Y), title, 20, color or T['muted'], bold=True)
    Y += 28
    for r, row in enumerate(tab):
        if row_hi == r:
            cv.rect((X - 4, Y + r * cell, X + len(row) * cell + 4, Y + (r + 1) * cell), outline=T['cyan'], width=2, r=6)
        cv.text((X - 8, Y + r * cell + cell / 2), r, 16, T['dim'], anchor='rm', mono=True)
        for c, v in enumerate(row):
            fill, tc = T['panel2'], T['text']
            if plus == (r, c):
                fill, tc = T['green'], T['bg']
            elif minus == (r, c):
                fill, tc = T['red'], T['bg']
            cv.rect((X + c * cell + 2, Y + r * cell + 2, X + (c + 1) * cell - 2, Y + (r + 1) * cell - 2), fill=fill,
                    r=5, outline=T['border'])
            cv.text((X + c * cell + cell / 2, Y + r * cell + cell / 2), v, 18, tc, anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('grid')
    if g is None:
        return
    m, n = len(g), len(g[0])
    line = S.get('_line')
    seg = _seg(S)
    cv.text((x0 + 18, y0 + 4), 'grid（黄框 = 中心，紫 = 顶点 angle_pos，绿 = 正在求和的斜边）', 21, T['muted'], bold=True)
    cell = 76
    gx, gy = x0 + 36, y0 + 40
    ap = S.get('angle_pos') if line in (40,) + GETS_LINES + (48,) else None
    verts = {tuple(p): k for k, p in enumerate(ap or [])}
    segc = set(seg[4]) if seg else set()
    for r in range(m):
        for c in range(n):
            X, Y = gx + c * cell, gy + r * cell
            fill, tc = T['panel2'], T['text']
            if (r, c) in segc:
                fill, tc = T['green'], T['bg']
            elif (r, c) in verts:
                fill, tc = T['purple'], T['bg']
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=8, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), g[r][c], 28, tc, anchor='mm', bold=True)
            if (r, c) in verts:
                cv.text((X + 8, Y + 6), verts[(r, c)], 16, T['bg'], bold=True)
    ci, cj = S.get('i'), S.get('j')
    if isinstance(ci, int) and isinstance(cj, int) and line not in (21, 51, 52, 6, 7, 3, 4) and 'first' in S:
        X, Y = gx + cj * cell, gy + ci * cell
        cv.rect((X, Y, X + cell, Y + cell), outline=T['yellow'], width=4, r=10)
    # 前三名
    tx = gx + n * cell + 40
    cv.text((tx, gy), '前三名', 22, T['muted'], bold=True)
    if 'first' in S:
        for k, nm in enumerate(('first', 'second', 'third')):
            Y = gy + 34 + k * 54
            cv.rect((tx, Y, tx + 220, Y + 46), fill=T['panel2'], r=10, outline=T['border'])
            cv.text((tx + 14, Y + 23), nm, 20, T['muted'], anchor='lm', mono=True)
            cv.text((tx + 206, Y + 23), S[nm], 26, T['green'], anchor='rm', bold=True)
    # 两张斜边前缀和
    if 'left_s' not in S:
        return
    ty = gy + m * cell + 14
    tc_ = 44
    lp = lm = rp = rm = lrow = rrow = None
    if seg:
        kind, p, a, b, _ = seg
        plus, minus = (p, b), ((p, a - 1) if a > 0 else None)
        if kind == 'left':
            lp, lm, lrow = plus, minus, p
        else:
            rp, rm, rrow = plus, minus, p
    _table(cv, T, x0 + 50, ty, S['left_s'], tc_, 'left_s ↙（i+j 相同）', lp, lm, lrow,
           T['cyan'] if lrow is not None else None)
    if 'right_s' in S:
        _table(cv, T, x0 + 50 + len(S['right_s'][0]) * tc_ + 110, ty, S['right_s'], tc_, 'right_s ↘（i−j 相同）',
               rp, rm, rrow, T['cyan'] if rrow is not None else None)


def _cap_gets(name):
    def f(S, B, ret):
        return f'{name}：第 `{S.s_pos}` 条斜边上，第 `{S.start}` 行到第 `{S.end}` 行这一段（含两端顶点）'
    return f


def _cap_ret_res(S, B, ret):
    kind = '左' if S.s == S.left_s else '右'
    if S.start > 0:
        return (f'{kind}斜边前缀和之差：`s[{S.s_pos}][{S.end}] − s[{S.s_pos}][{S.start - 1}]` = '
                f'`{S.s[S.s_pos][S.end]} − {S.s[S.s_pos][S.start - 1]}` = =={ret}==')
    return f'{kind}斜边从第 0 行开始：直接取 `s[{S.s_pos}][{S.end}]` = =={ret}=='


def _cap_check_ret(S, B, ret):
    v = S.now
    a, b, c = ret
    return f'用 `{v}` 更新（相同的和不重复计）→ 前三名 `{a}, {b}, {c}`'


def _cap_len(S, B, ret):
    ap = S.angle_pos
    if len(ap) < 4:
        dirs = '上右下左'
        return f'`l = {S.l}`：往{dirs[len(ap)]}走 {S.l} 格就==出界==了（只放进 {len(ap)} 个顶点）→ 这个中心没有更大的菱形'
    return f'`l = {S.l}`：四个顶点 `{ap}` 都在界内；顶点之后会被算两次，`now` 先减去它们 = `{S.now}`'


CONFIG = dict(
    num=1878, title='矩阵中最大的三个菱形和', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='每条斜边的前缀和 · 枚举中心向四周扩张',
    tags=['字节30天'],
    code='''
class Solution(object):
    def getBiggestThree(self, grid):
        m = len(grid)
        n = len(grid[0])

        left_s = [[0] * max(m, n) for _ in range(m + n - 1)]
        right_s = [[0] * max(m, n) for _ in range(m + n - 1)]

        for i in range(m):
            for j in range(n):
                left_pos = i + j
                left_s[left_pos][i] = grid[i][j]
                if i > 0:
                    left_s[left_pos][i] += left_s[left_pos][i - 1]

                right_pos = i - j + n - 1
                right_s[right_pos][i] = grid[i][j]
                if i > 0:
                    right_s[right_pos][i] += right_s[right_pos][i - 1]

        first = second = third = 0
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                first, second, third = self.check(first, second, third, grid[i][j])
                l = 1
                while True:
                    angle_pos = []
                    now = 0
                    for index in range(4):
                        x = i + dx[index] * l
                        y = j + dy[index] * l
                        if x >= 0 and x < m and y >= 0 and y < n:
                            angle_pos.append([x, y])
                            now -= grid[x][y]
                        else:
                            break

                    if len(angle_pos) < 4:
                        break

                    now += self.get_s(left_s, angle_pos[0][0] + angle_pos[0][1], angle_pos[0][0], angle_pos[3][0])
                    now += self.get_s(left_s, angle_pos[1][0] + angle_pos[1][1], angle_pos[1][0], angle_pos[2][0])
                    now += self.get_s(right_s, angle_pos[0][0] - angle_pos[0][1] + n - 1, angle_pos[0][0], angle_pos[1][0])
                    now += self.get_s(right_s, angle_pos[3][0] - angle_pos[3][1] + n - 1, angle_pos[3][0], angle_pos[2][0])

                    first, second, third = self.check(first, second, third, now)
                    l += 1

        if third > 0:
            return [first, second, third]
        elif second > 0:
            return [first, second]
        else:
            return [first]

    def check(self, first, second, third, now):
        if now > first:
            first, second, third = now, first, second
        elif now > second and now != first:
            second, third = now, second
        elif now > third and now != first and now != second:
            third = now

        return first, second, third

    def get_s(self, s, s_pos, start, end):
        res = s[s_pos][end]
        if start > 0:
            res -= s[s_pos][start - 1]
        return res
''',
    call=f'Solution().getBiggestThree({GRID})',
    expect=[20, 9, 8],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('l', 'l'), ('now', 'now', 'green')],
    captions={
        'left_s = [[0]': '左斜边上的格子 `i + j` 相同：`left_s[i+j][i]` 存这条斜边==从上到第 i 行==的前缀和',
        'right_s = [[0]': '右斜边上的格子 `i − j` 相同：`right_s[i−j+n−1][i]` 同理（`+n−1` 防止下标为负）',
        'first = second = third = 0': '两张斜边前缀和建好了；`first, second, third` 维护前三名',
        'dx = [-1, 0, 1, 0]': '`dx, dy`：从中心往==上、右、下、左==四个方向扩张，找菱形的四个顶点',
        'first, second, third = self.check(first, second, third, grid[i][j])':
            lambda S, B, ret: f'中心 `({B.i},{B.j})`：单个格子 `{S.now}` 也算菱形 → `check`',
        'return first, second, third': _cap_check_ret,
        'if len(angle_pos) < 4': _cap_len,
        'now += self.get_s(left_s, angle_pos[0][0] + angle_pos[0][1]': _cap_gets('左斜边：上顶点 → 左顶点'),
        'now += self.get_s(left_s, angle_pos[1][0] + angle_pos[1][1]': _cap_gets('左斜边：右顶点 → 下顶点'),
        'now += self.get_s(right_s, angle_pos[0][0]': _cap_gets('右斜边：上顶点 → 右顶点'),
        'now += self.get_s(right_s, angle_pos[3][0]': _cap_gets('右斜边：左顶点 → 下顶点'),
        'return res': _cap_ret_res,
        'first, second, third = self.check(first, second, third, now)':
            lambda S, B, ret: f'`now` 一开始先减去了四个顶点各一次，再加上四段斜边 → 菱形和 =={B.now}== → `check`',
        'if third > 0': '`third = {third} > 0`：凑齐了三个不同的和',
        'return [first, second, third]': '返回 `{ret}`',
    },
    skip=[3, 4, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 41, 49,
          59, 60, 61, 62, 63, 64, 69, 70, 71],
    max_steps=60,
    cards=dict(
        one_liner='每条斜边做前缀和，枚举中心向四周扩张，四段斜边和减去重复的顶点',
        complexity='时间 `O(mn·min(m,n))`，空间 `O(mn)`',
        problem=['菱形和：正方形旋转 45° 后，==边界==上格子的元素和（面积为 0 的单个格子也算）',
                 '按降序返回 grid 中==最大的三个互不相同==的菱形和，不足三个就全部返回',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]` → `[20,9,8]`'],
        quote='同一条左斜边经过的格子满足==横纵坐标之和相等==，而同一条右斜边经过的格子满足==横纵坐标之差相等==……需要注意的是，==菱形的四个顶点都被计算了两次==，因此需要分别减去对应格子上的数值各一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每条左斜边、右斜边按行做前缀和，斜边上一段的和 = 两个前缀和之差',
              '枚举中心，`l = 1, 2, …` 向上右下左扩张得到四个顶点；有顶点出界就停',
              '四条边各是一段斜边（含两端顶点）→ 顶点被算两次，先在 `now` 里各减一次'],
        result='最大的三个菱形和：`[20, 9, 8]` ✓',
        summary=['时间 `O(mn·min(m,n))`：中心 `mn` 个，每个最多扩张 `min(m,n)/2` 次',
                 '易错：四条边都包含两端顶点，所以 `now` 先减去四个顶点的值',
                 '`check` 里用 `now != first` 等条件去掉重复的和',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神让四条边分段不重叠，不用减顶点；前缀和多开一维免特判'],
    ),
)
