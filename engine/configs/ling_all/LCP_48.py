CODE = r"""
black = "Black"
white = "White"
none = "None"

dir8 = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


class Solution:
    def gobang(self, pieces: List[List[int]]) -> str:
        color = {}
        for p in pieces:
            p[2] += 1  # 为方便利用零值，将黑改为 1，白改为 2
            color[(p[0], p[1])] = p[2]

        # 在 (i,j) 落子，颜色为 c，判断落子的一方是否获胜
        def checkWin(i, j, c):
            for k, d in enumerate(dir8[:4]):
                cnt = 1
                # 检查一个方向
                x, y = i + d[0], j + d[1]
                while color.get((x, y), 0) == c:
                    cnt += 1
                    x, y = x + d[0], y + d[1]
                # 检查相反的另一方向
                d = dir8[k ^ 4]
                x, y = i + d[0], j + d[1]
                while color.get((x, y), 0) == c:
                    cnt += 1
                    x, y = x + d[0], y + d[1]
                if cnt >= 5:
                    return True
            return False

        # 1. 黑第一手就可以获胜
        for p in pieces:
            if p[2] == 2:
                continue
            i, j = p[0], p[1]
            for d in dir8:  # 黑要想一步获胜只能下在黑子周围
                x, y = i + d[0], j + d[1]
                if color.get((x, y), 0) == 0 and checkWin(x, y, 1):
                    return black

        # 2. 黑第一手无法获胜
        whites = {}
        posW = (0, 0)
        for p in pieces:
            if p[2] == 1:
                continue
            i, j = p[0], p[1]
            for d in dir8:  # 白要想一步获胜只能下在白子周围
                x, y = i + d[0], j + d[1]
                q = (x, y)
                if color.get(q, 0) == 0 and checkWin(x, y, 2):
                    # 2.1 白可以一步胜，且获胜位置不止一处
                    whites[q] = True
                    if len(whites) > 1:
                        return white
                    posW = q

        # 2.2 白可以一步胜，但获胜位置只有一处
        if len(whites) == 1:
            color[posW] = 1  # 黑第一手下在该处，阻止白获胜
            blacks = {}

            # 检查第三步的黑能否获胜
            def checkBlackWin(i, j):
                for d in dir8:  # 黑要获胜只能下在黑子周围
                    x, y = i + d[0], j + d[1]
                    p = (x, y)
                    if color.get(p, 0) == 0 and checkWin(x, y, 1):
                        blacks[p] = True
                        if len(blacks) > 1:
                            return True
                return False

            checkBlackWin(posW[0], posW[1])
            for p in pieces:
                if p[2] == 1 and checkBlackWin(p[0], p[1]):
                    return black
            return none

        # 3. 白无法获胜，于是白的策略是防止黑获胜
        # 根据黑第一步的落子位置，在该位置周围枚举黑第三步的落子位置，检查黑能否获胜
        def checkBlackWin(i0, j0):
            blacks = {}
            for k, d in enumerate(dir8):
                i, j = i0, j0
                for l in range(5):  # 如果黑可以获胜，这两枚黑子的距离不会超过 5
                    i += d[0]
                    j += d[1]
                    p = (i, j)
                    if color.get(p, 0) > 0:
                        continue
                    cnt = 1
                    # 检查一个方向
                    x, y = i + d[0], j + d[1]
                    while color.get((x, y), 0) == 1:
                        cnt += 1
                        x, y = x + d[0], y + d[1]
                    # 检查相反的另一方向
                    d2 = dir8[k ^ 4]
                    x, y = i + d2[0], j + d2[1]
                    while color.get((x, y), 0) == 1:
                        cnt += 1
                        x, y = x + d2[0], y + d2[1]
                    if cnt >= 5:
                        blacks[p] = True
                        if len(blacks) > 1:
                            return True
            return False

        vis = {}  # 常数优化：避免重复枚举
        for p in pieces:
            if p[2] == 2:
                continue
            i, j = p[0], p[1]
            # 枚举黑第一步的落子。由于黑要下两手棋，需要枚举黑子周围两圈
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx == 0 and dy == 0:
                        continue
                    x, y = i + dx, j + dy
                    q = (x, y)
                    if vis.get(q) or color.get(q, 0) > 0:
                        continue
                    color[q] = 1  # 黑落子
                    vis[q] = True
                    if checkBlackWin(x, y):
                        return black
                    del color[q]
        return none
"""
_LN = CODE.strip('\n').split('\n')


def _find(s, start=0):
    for k in range(start, len(_LN)):
        if s in _LN[k]:
            return k + 1
    return 10 ** 6


_L1 = _find('# 1. 黑第一手就可以获胜')
_L2 = _find('# 2. 黑第一手无法获胜')
_L22 = _find('# 2.2 ')
_L3 = _find('# 3. 白无法获胜')
_LCB3 = _find('def checkBlackWin(i0, j0)')


def _sec(S):
    ln = S.get('_line', 0)
    if ln < _L2:
        return 1
    if ln < _L22:
        return 2
    if ln < _L3:
        return 22
    return 3


def _cells(S):
    c = S.get('color') or {}
    return c


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    col = S.get('color')
    cv.text((x0 + 18, y0 + 2), '棋盘（黑 = 实心黑，白 = 白，黄环 = 黑第一手，青环 = 正在试的格子，红框 = 白获胜点）', 20, T['muted'], bold=True)
    if not col:
        return
    xs = [k[0] for k in col]
    ys = [k[1] for k in col]
    mnx, mxx = min(xs) - 2, max(xs) + 2
    mny, mxy = min(ys) - 2, max(ys) + 2
    nx, ny = mxx - mnx + 1, mxy - mny + 1
    top = y0 + 40
    cs = min((x1 - x0 - 40) / nx, (y1 - top - 14) / ny, 64)
    ox = x0 + 20 + ((x1 - x0 - 40) - cs * nx) / 2
    oy = top

    def pos(p):
        return ox + (p[0] - mnx + 0.5) * cs, oy + (p[1] - mny + 0.5) * cs
    for a in range(nx):
        X = ox + (a + 0.5) * cs
        cv.line([(X, oy + 0.5 * cs), (X, oy + (ny - 0.5) * cs)], T['border'], 1)
        cv.text((X, oy + ny * cs + 1), mnx + a, 14, T['dim'], anchor='mt', mono=True)
    for b in range(ny):
        Y = oy + (b + 0.5) * cs
        cv.line([(ox + 0.5 * cs, Y), (ox + (nx - 0.5) * cs, Y)], T['border'], 1)
        cv.text((ox + 2, Y), mny + b, 14, T['dim'], anchor='lm', mono=True)
    r = cs * 0.36
    for k, v in col.items():
        X, Y = pos(k)
        if v == 1:
            cv.rect((X - r, Y - r, X + r, Y + r), fill=(20, 22, 26), outline=T['blue'], width=2, r=r)
        else:
            cv.rect((X - r, Y - r, X + r, Y + r), fill=(235, 235, 235), r=r)
    for w in (S.get('whites') or {}):
        X, Y = pos(w)
        cv.rect((X - r - 3, Y - r - 3, X + r + 3, Y + r + 3), outline=T['red'], width=3, r=6)
    for w in (S.get('blacks') or {}):
        X, Y = pos(w)
        cv.rect((X - r - 3, Y - r - 3, X + r + 3, Y + r + 3), outline=T['green'], width=3, r=6)
    cur = None
    inn = S.get('_inner', {})
    if 'c' in inn and 'i' in inn and 'j' in inn:
        cur = (inn['i'], inn['j'])
    elif S.get('_line', 0) >= _L3:
        cur = S['q'] if S.get('q') in col else None
    elif 'x' in S and 'y' in S and S.get('_line', 0) < _L3 and S.get('_line', 0) >= _L1:
        cur = (S['x'], S['y'])
    if cur is not None:
        X, Y = pos(cur)
        cv.rect((X - r - 6, Y - r - 6, X + r + 6, Y + r + 6), outline=T['yellow'] if S.get('_line', 0) >= _L3 else T['cyan'], width=4, r=r + 6)


_D8 = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def _run(col, x, y, d, c):
    n = 0
    x, y = x + d[0], y + d[1]
    while col.get((x, y), 0) == c:
        n += 1
        x, y = x + d[0], y + d[1]
    return n


def _best(col, x, y, c):
    """最长连子数（含落子本身）"""
    return max(1 + _run(col, x, y, d, c) + _run(col, x, y, _D8[k ^ 4], c) for k, d in enumerate(_D8[:4]))


def _spots(col, i0, j0):
    """黑第三手的获胜位置集合（与情况 3 里的 checkBlackWin 同逻辑，只用于字幕）"""
    out = set()
    for k, d in enumerate(_D8):
        i, j = i0, j0
        for _ in range(5):
            i += d[0]
            j += d[1]
            if col.get((i, j), 0) > 0:
                continue
            if 1 + _run(col, i, j, d, 1) + _run(col, i, j, _D8[k ^ 4], 1) >= 5:
                out.add((i, j))
    return out


def _cap_try(S, B, r):
    x, y = S.x, S.y
    c = 1 if _sec(S) == 1 else 2
    who = '黑' if c == 1 else '白'
    col = S.color
    if col.get((x, y), 0) != 0:
        return f'邻格 `({x}, {y})` 已经有子，跳过'
    m = _best(col, x, y, c)
    return f'邻格 `({x}, {y})` 是空的：{who}落这里，最长连子 `{m}`' + ('，==成五！==' if m >= 5 else '，不到 5')


def _cap_for(S, B, r):
    s = _sec(S)
    p = S.get('p')
    if s in (1, 2) and p is not None:
        mine = 1 if s == 1 else 2
        if B.get('p') == p and B.get('_line', 0) >= _L1:
            return '黑子都看完了：黑第一手无法直接成五 → 往下看白' if s == 1 else '白子都看完了，继续往下判断'
        if p[2] != mine:
            return f'`({p[0]}, {p[1]})` 是{"白" if p[2] == 2 else "黑"}子，不用看，跳过'
        return ('黑' if s == 1 else '白') + f'子 `({p[0]}, {p[1]})`：它的 8 个邻格才可能一步成五'
    return {1: '==第 1 种情况==：黑第一手能赢吗？黑要一步成五，只能下在黑子的邻格',
            2: '==第 2 种情况==：白一步能赢吗？白要成五也只能下在白子的邻格',
            22: '==2.2==：白只有一个获胜点，黑第一手必须堵在这里',
            3: '==第 3 种情况==：白赢不了，只会防黑。枚举黑第一手，再看第三手能否出现 ≥2 个获胜点'}[s]


def _ret_black(S, B, r):
    s = _sec(S)
    if s == 1:
        return '黑下在邻格就连成五 → 直接返回 =="Black"=='
    if s == 22:
        return '堵完之后黑第三手有两处以上获胜位置，白堵不住 → =="Black"=='
    return '黑第一手落下后，第三手有 ≥2 个获胜位置，白一手堵不住 → =="Black"=='


def _fml(S):
    s = _sec(S) if 'pieces' in S else 0
    return {0: '棋子编码：黑 = 1，白 = 2；无边界，坐标可以是任意整数', 1: '情况 1：黑一步成五？', 2: '情况 2：白一步成五？',
            22: '情况 2.2：白有唯一获胜点，黑被迫去堵', 3: '情况 3：枚举黑第一手 + 黑第三手的双获胜位置'}[s]


CONFIG = dict(
    num='LCP 48', title='无限棋局', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='分类讨论 + 枚举落子位置（Go 原文转写）',
    tags=['常用数据结构', '数学算法'],
    code=CODE,
    call='Solution().gobang([[1, 0, 0], [0, 0, 0], [2, 0, 0], [4, 2, 1]])',
    expect='Black',
    max_steps=90,
    skip=['p[2] += 1', 'color[(p[0], p[1])]', 'i, j = p[0], p[1]', 'for k, d in enumerate(dir8', 'cnt = 1', 'x, y = i + d[0], j + d[1]',
          'while color.get', 'cnt += 1', 'x, y = x + d[0], y + d[1]', 'd = dir8[k ^ 4]', 'q = (x, y)', 'p = (x, y)', 'p = (i, j)',
          'i, j = i0, j0', 'i += d[0]', 'j += d[1]', 'd2 = dir8', 'x, y = i + d2[0]', 'x, y = x + d2[0]', 'blacks = {}', 'for l in range(5)',
          'if color.get(p, 0) > 0', 'continue', 'vis[q] = True', 'if dx == 0 and dy == 0', 'def ', 'whites = {}', 'posW = (0, 0)',
          'for dy in range(-2, 3)', 'if p[2] == 2', 'if p[2] == 1:', 'if cnt >= 5', 'return True', 'return False', 'for d in dir8', _find('for p in pieces')],
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'pink'), ('whites', lambda S: len(S['whites']) if 'whites' in S else None, 'red'),
           ('blacks', lambda S: len(S['blacks']) if 'blacks' in S else None, 'green')],
    captions={
        'for p in pieces': _cap_for,
        'if color.get((x, y), 0) == 0 and checkWin': _cap_try,
        'if color.get(q, 0) == 0 and checkWin(x, y, 2)': _cap_try,
        'whites[q] = True': '白能一步成五：记下获胜位置 `{q}`',
        'if len(whites) > 1': lambda S, B, r: (f'白有 `{len(S.whites)}` 个获胜位置 > 1：黑一手堵不住 → ==白胜==' if len(S.whites) > 1 else '白目前只有 1 个获胜位置，继续找'),
        'posW = q': '先记住这个位置 `posW`',
        'if len(whites) == 1': lambda S, B, r: (f'白恰好 1 个获胜位置 `{S.posW}`：黑第一手必须堵这里' if len(S.whites) == 1 else '白没有一步获胜位置 → 进入情况 3'),
        'color[posW] = 1': '黑第一手下在 `{posW}`，阻止白获胜',
        'checkBlackWin(posW[0], posW[1])': '看这手新黑子周围：黑第三手能否有两处获胜位置',
        'for p in pieces': _cap_for,
        'blacks[p] = True': '黑在 `{p}` 能成五：记下这个获胜位置',
        'checkBlackWin(posW[0], posW[1])': '看这手新黑子周围：黑第三手能否有两处获胜位置',
        'if len(blacks) > 1': lambda S, B, r: (f'黑有 `{len(S.blacks)}` 个获胜位置 > 1：白一手堵不住 → ==黑胜==' if len(S.blacks) > 1 else '黑目前只有 1 个获胜位置'),
        'return black': _ret_black,
        'for p in pieces': _cap_for,
        'return white': '白有两个以上获胜位置，黑堵不住 → 返回 =="White"=="',
        'return none': '三步之内没有人能确保取胜 → 返回 =="None"=="',
        'vis = {}': '`vis` 记录枚举过的候选点，避免重复（常数优化）',
        'for dx in range(-2, 3)': '黑要下两手（第一手 + 第三手），第一手只可能在黑子周围两圈内',
        'x, y = i + dx, j + dy': '候选点 `({i + dx}, {j + dy})`（相对黑子 `({i}, {j})` 偏移 `({dx}, {dy})`）',
        'if vis.get(q) or color.get(q, 0) > 0': lambda S, B, r: (f'候选点 `{(S.i + S.dx, S.j + S.dy)}` 已经枚举过或有子 → 跳过' if (S.vis.get((S.i + S.dx, S.j + S.dy)) or S.color.get((S.i + S.dx, S.j + S.dy), 0) > 0) else '候选点是空位，可以落子'),
        'color[q] = 1': '==黑第一手==落在 `{q}`',
        'if checkBlackWin(x, y)': lambda S, B, r: (lambda sp: f'黑第一手落在 `({S.x}, {S.y})` 后，第三手的获胜位置有 `{len(sp)}` 个' + ('：' + str(sorted(sp)) + ' ≥ 2，白堵不住' if len(sp) > 1 else '，不到 2 个'))(_spots(S.color, S.x, S.y)),
        'del color[q]': '这手不行：撤回，换下一个候选点',
    },
    cards=dict(
        one_liner='三步内只有四种局面：先手赢、白双杀、白单杀被堵、黑做双杀',
        complexity='时间 `O(n·C)`（C 为常数，8 方向 × 两圈候选），空间 `O(n)`',
        problem=['无边界五子棋，黑先、黑白黑三步内，先连成同行/列/对角线连续 5 子者胜',
                 '`pieces[i]=[x,y,color]`，`0` 黑 `1` 白；当前无胜者，双方都按最优策略',
                 '返回 `"Black"` / `"White"` / `"None"`'],
        quote='白可以一步胜，且获胜位置不止一处，此时黑无法阻止白获胜，输出 "White"。白可以一步胜，但获胜位置只有一处，此时黑第一手下在该处，白无法获胜。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先手赢 → Black；白一步有 ≥2 个获胜点 → White；恰好 1 个 → 黑必须去堵，再看第三手',
              '白赢不了就枚举黑第一手（黑子周围两圈），第三手出现 ≥2 个获胜点 → Black，否则 None'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`map` 用 dict（读缺键用 `.get(k, 0)` 模拟零值），`pair` 用元组',
                 '「获胜位置 ≥ 2」是关键：对手一手只能堵一处；黑要下两手，所以第一手枚举两圈',
                 '视频隐去了方向计数等细碎循环，只展示每次落子的结论；示例是黑的「活三」'],
    ),
)
