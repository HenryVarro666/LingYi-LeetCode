PIECES = [[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 2, 1], [4, 2, 1]]
DX = [0, 1, 1, 1]
DY = [1, 1, 0, -1]
X0, X1, Y0, Y1 = -3, 6, -3, 5


def _line(st, sx, sy, c, dx, dy):
    fill = None
    for k in range(5):
        p = (sx + k * dx, sy + k * dy)
        v = st.get(p)
        if v == c:
            continue
        if v == 1 - c or fill is not None:
            return None
        fill = p
    return fill


def _fills(st, x, y, c):
    out = set()
    for ln in range(5):
        for d in range(4):
            f = _line(st, x - ln * DX[d], y - ln * DY[d], c, DX[d], DY[d])
            if f is not None:
                out.add(f)
    return out


def _fmt(s):
    return '、'.join(f'({a},{b})' for a, b in sorted(s)) if s else '无'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st = S.get('piece_dict') or {}
    nx, ny = X1 - X0 + 1, Y1 - Y0 + 1
    cell = min((x1 - x0 - 40) / nx, (y1 - y0 - 90) / ny, 64)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * nx) / 2
    sy = y0 + 56
    cv.text((x0 + 18, y0 + 4), '棋盘（黄环 = 试下的位置，绿环 = 黑成五处，红环 = 白成五处）', 20, T['muted'], bold=True)

    def ctr(p):
        return sx + (p[0] - X0) * cell + cell / 2, sy + (Y1 - p[1]) * cell + cell / 2

    for i in range(nx):
        for j in range(ny):
            X, Y = sx + i * cell, sy + j * cell
            cv.rect((X, Y, X + cell, Y + cell), fill=T['panel2'] if (i + j) % 2 == 0 else (30, 36, 46), outline=T['border'])
    for i in range(nx):
        cv.text((sx + i * cell + cell / 2, sy + ny * cell + 4), X0 + i, 16, T['dim'], anchor='mt', mono=True)
    for j in range(ny):
        cv.text((sx - 6, sy + j * cell + cell / 2), Y1 - j, 16, T['dim'], anchor='rm', mono=True)
    line = S.get('_line')
    cand = (S['x'], S['y']) if 'x' in S and 'y' in S and 'candidate' in S and line is not None and line >= 60 else None
    marks = []
    nf = S.get('need_fill') or set()
    for p in nf:
        marks.append((p, 'red'))
    if cand is not None and st.get(cand) == 0:
        for p in _fills(st, cand[0], cand[1], 0):
            marks.append((p, 'green'))
    for p, col in marks:
        if X0 <= p[0] <= X1 and Y0 <= p[1] <= Y1:
            X, Y = ctr(p)
            cv.rect((X - cell * 0.42, Y - cell * 0.42, X + cell * 0.42, Y + cell * 0.42), outline=T[col], width=5, r=cell * 0.4)
    if cand is not None and X0 <= cand[0] <= X1 and Y0 <= cand[1] <= Y1:
        X, Y = ctr(cand)
        cv.rect((X - cell * 0.46, Y - cell * 0.46, X + cell * 0.46, Y + cell * 0.46), outline=T['yellow'], width=4, r=cell * 0.4)
    for p, c in st.items():
        if X0 <= p[0] <= X1 and Y0 <= p[1] <= Y1:
            X, Y = ctr(p)
            r = cell * 0.32
            if c == 0:
                cv.rect((X - r, Y - r, X + r, Y + r), fill=(12, 14, 18), outline=(200, 205, 215), width=2, r=r)
            else:
                cv.rect((X - r, Y - r, X + r, Y + r), fill=(235, 238, 245), outline=(120, 126, 140), width=2, r=r)


def _cap_black(S, B, r):
    x, y = S.x, S.y
    f = _fills(S.piece_dict, x, y, 0)
    if f:
        return f'黑子 `({x},{y})`：枚举经过它的所有 5 连窗口，缺一格的位置 = `{_fmt(f)}` → ==一步成五，黑直接获胜=='
    return f'黑子 `({x},{y})`：经过它的 5 连窗口里没有「5 缺 1」，黑一步赢不了'


def _cap_white(S, B, r):
    x, y = S.x, S.y
    f = _fills(S.piece_dict, x, y, 1)
    return f'白子 `({x},{y})` 的「5 缺 1」位置：`{_fmt(f)}` → 记入 `need_fill`' if f else f'白子 `({x},{y})` 没有「5 缺 1」，不构成威胁'


def _cap_try(S, B, r):
    x, y = S.x, S.y
    f = _fills(S.piece_dict, x, y, 0)
    if len(f) >= 2:
        return f'黑子落在 `({x},{y})` 后，成五的位置有 `{_fmt(f)}` 共 =={len(f)}== 处：白==防不住两处== → 黑胜'
    return f'黑子落在 `({x},{y})` 后，成五的位置只有 `{len(f)}` 处（{_fmt(f)}）：白一步就能堵住，这个位置不够'


CONFIG = dict(
    num='LCP 48', title='无限棋局', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='分类讨论 + 枚举「5 缺 1」',
    tags=['灵神题单·常用数据结构', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def gobang(self, pieces):

        piece_dict = {}
        for x, y, c in pieces:
            piece_dict[(x, y)] = c

        dx = [0, 1, 1, 1]
        dy = [1, 1, 0, -1]

        def check_line(sx, sy, check_c, dx, dy):
            fill_x, fill_y = None, None
            for length in range(5):
                x = sx + length * dx
                y = sy + length * dy
                c = piece_dict.get((x, y))
                if c == check_c:
                    continue
                if (c == 1 - check_c) or (fill_x is not None):
                    return None, None
                fill_x, fill_y = x, y
            
            return fill_x, fill_y

        def check_point(x, y, c):
            fill_set = set()
            for length in range(0, 5):
                for index in range(4):
                    fill_x, fill_y = check_line(x - length * dx[index], y - length * dy[index], c, dx[index], dy[index])
                    if fill_x is not None:
                        fill_set.add((fill_x, fill_y))
        
            return fill_set

        need_fill = set()
        for x, y, c in pieces:
            if c == 0:
                if len(check_point(x, y, c)):
                    return 'Black'
                
            else:
                need_fill.update(check_point(x, y, c))
        
        if len(need_fill) >= 2:
            return 'White'

        if len(need_fill) == 1:
            candidate = need_fill
        else:
            candidate = set()
            for x, y, c in pieces:
                if c == 0:
                    for index in range(4):
                        if piece_dict.get((x + dx[index], y + dy[index]), None) is None:
                            candidate.add((x + dx[index], y + dy[index]))
                            if piece_dict.get((x + dx[index] * 2, y + dy[index] * 2), None) is None:
                                candidate.add((x + dx[index] * 2, y + dy[index] * 2))
                        if piece_dict.get((x - dx[index], y - dy[index]), None) is None:
                            candidate.add((x - dx[index], y - dy[index]))
                            if piece_dict.get((x - dx[index] * 2, y - dy[index] * 2), None) is None:
                                candidate.add((x - dx[index] * 2, y - dy[index] * 2))

        for x, y in candidate:
            piece_dict[(x, y)] = 0
            if len(check_point(x, y, 0)) >= 2:
                return 'Black'
            piece_dict.pop((x, y))

        return 'None'
''',
    call=f'Solution().gobang({PIECES!r})',
    expect='Black',
    max_events=600000,
    max_steps=44,
    skip=[5, 'piece_dict[(x, y)] = c', 'dx = [0', 'dy = [1', 'need_fill = set()', 'check_line', 'fill_x', 'fill_y', 'fill_set', 'for length', 'for index',
          'c = piece_dict.get', 'x = sx', 'y = sy', 'if c == check_c', 'continue', 'if (c == 1', 'return None, None',
          'if piece_dict.get', 'candidate.add', 'candidate = set()', 'else:'],
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('x', 'x'), ('y', 'y'), ('need_fill', 'sorted(need_fill) if "need_fill" in S else []', 'red')],
    captions={
        'piece_dict = {}': '把棋子放进字典：坐标 → 颜色（0 黑 / 1 白），无边界棋盘用字典最方便',
        36: lambda S, B, r: ('第一步：黑子有「5 缺 1」吗？白子有吗？逐个棋子检查' if 'c' not in B else f'下一枚棋子：`({S.x},{S.y})`，颜色 `{S.c}`'),
        37: lambda S, B, r: f'`({S.x},{S.y})` 是' + ('黑子' if S.c == 0 else '白子'),
        'if len(check_point(x, y, c))': _cap_black,
        'need_fill.update': _cap_white,
        'if len(need_fill) >= 2': lambda S, B, r: (f'白子要成五的位置有 `{len(S.need_fill)}` 处：黑只能堵一处 → ==白胜==' if len(S.need_fill) >= 2
                                                   else f'白子成五的位置只有 `{len(S.need_fill)}` 处，黑还防得住'),
        'if len(need_fill) == 1': lambda S, B, r: ('只有一处白子威胁：黑==必须下在那里防守==，候选位置只有它' if len(S.need_fill) == 1
                                                  else '白子没有威胁：黑可以自由「发展」一枚黑子'),
        'candidate = need_fill': '候选位置 = 白子要成五的那一格',
        51: '黑可以自由发展：只试离现有黑子距离 ≤ 2 的空位（太远的孤子一步成不了五）',
        52: lambda S, B, r: (f'黑子 `({S.x},{S.y})`：它四个方向上 ±1、±2 的空位都加入 `candidate`' if S.c == 0 else f'白子 `({S.x},{S.y})`，跳过'),
        'for x, y in candidate': lambda S, B, r: f'试把黑子下在 `({S.x},{S.y})`',
        'piece_dict[(x, y)] = 0': lambda S, B, r: f'临时把黑子放到 `({S.x},{S.y})`',
        'if len(check_point(x, y, 0)) >= 2': _cap_try,
        'piece_dict.pop': '不够 2 处，拿掉这枚试探的黑子，换下一个候选',
        "return 'Black'": '找到了「一手造出两处成五」的位置：白防不住 → 返回 ==Black==',
        "return 'None'": '所有位置都试完了：三步内无人能赢 → ==None==',
    },
    cards=dict(
        one_liner='先看一步成五，再看谁有两处威胁，最后枚举黑的发展',
        complexity='时间 `O(n·20·5)` + 候选 `O(n·8)` 个位置的检查，空间 `O(n)`',
        problem=['无边界五子棋，黑先，黑 / 白 / 黑 三步内谁先五连即胜',
                 '`pieces[i] = [x, y, color]`，`0` 黑 `1` 白，局面当前无胜者',
                 '返回 `"Black"` / `"White"` / `"None"`',
                 '本视频：黑已有三连，白两子在一旁 → `"Black"`'],
        quote='综合起来可以发现，一共只有四种情况：1、黑棋可以直接取胜 2、黑棋无法直接取胜，但是白子存在两处或以上的5缺1需要防守，此时白棋取胜 3、……白子存在一处5缺1的防守，此时黑子需要在此防守 4、黑棋无法直接取胜，且无需防守白子。此时黑子可以选择在任意位置发展一处黑子。',
        quote_src='—— yiduobo 题解原文',
        idea=['「5 缺 1」= 一个 5 连窗口里已有 4 个同色子、另 1 格是空的',
              '对每枚棋子，枚举横竖两斜 4 个方向 × 5 种起点，窗口里遇到异色或缺两格就作废',
              '黑有 5 缺 1 直接赢；白有两处白赢；白只有一处黑必须去堵',
              '否则黑「发展」一枚：只试距离现有黑子 ≤ 2 的空位，看能否一手造出两处 5 缺 1'],
        summary=['时间 `O(n)` 常数很大，空间 `O(n)`',
                 '易错：窗口要考虑 `XXXX_`、`_XXXX`、`XX_XX` 等所有缺口位置，所以 5 种起点',
                 '发展的黑子只需检查==包含它的==窗口，其他黑子一开始已检查过',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '视频中 `check_point` / `check_line` 内部没有逐行展示，结果直接画在棋盘上'],
    ),
)
