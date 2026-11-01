CODE = r"""
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
"""
_LN = CODE.strip('\n').split('\n')


def _find(s):
    for k, l in enumerate(_LN):
        if s in l:
            return k + 1
    return 10 ** 6


_LNEED = _find('need_fill = set()')
_LCAND = _find('for x, y in candidate')
_LCAND0 = _find('candidate = set()')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    col = S.get('piece_dict')
    cv.text((x0 + 18, y0 + 2), '棋盘（红框 = 白的缺口，绿框 = 当前点的缺口，黄环 = 试下的黑子）', 20, T['muted'], bold=True)
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
        if v == 0:
            cv.rect((X - r, Y - r, X + r, Y + r), fill=(20, 22, 26), outline=T['blue'], width=2, r=r)
        else:
            cv.rect((X - r, Y - r, X + r, Y + r), fill=(235, 235, 235), r=r)
    for w in (S.get('need_fill') or ()):
        X, Y = pos(w)
        cv.rect((X - r - 3, Y - r - 3, X + r + 3, Y + r + 3), outline=T['red'], width=3, r=6)
    for w in (S.get('_inner', {}).get('fill_set') or ()):
        X, Y = pos(w)
        cv.rect((X - r - 3, Y - r - 3, X + r + 3, Y + r + 3), outline=T['green'], width=3, r=6)
    ln = S.get('_line', 0)
    if ln >= _LCAND and 'x' in S and 'y' in S and (S['x'], S['y']) in col:
        X, Y = pos((S['x'], S['y']))
        cv.rect((X - r - 6, Y - r - 6, X + r + 6, Y + r + 6), outline=T['yellow'], width=4, r=r + 6)


def _fml(S):
    ln = S.get('_line', 0)
    if 'need_fill' not in S:
        return '「5 缺 1」：同一方向 5 格里恰好 4 子同色、1 格空，补上那一子就成五'
    if ln >= _LCAND:
        return '情况 3/4：试下一颗黑子，看它能不能同时造出 ≥ 2 处「5 缺 1」'
    return f"白的「5 缺 1」位置：`{sorted(S['need_fill'])}`" if S['need_fill'] else '白暂时没有「5 缺 1」，黑可以放心发展'


def _cap_cp(S, B, r):
    x, y, c = S.x, S.y, S.c
    who = '黑' if c == 0 else '白'
    fs = sorted(S.fill_set)
    return f'以 `({x}, {y})` 为中心扫 4 个方向 × 5 种起点：{who}的「5 缺 1」缺口有 `{len(fs)}` 处' + (f' `{fs}`' if fs else '')


CONFIG = dict(
    num='LCP 48', title='无限棋局', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='「5 缺 1」检测 + 枚举黑子发展位置',
    tags=['常用数据结构', '数学算法'],
    code=CODE,
    call='Solution().gobang([[1, 1, 0], [0, 2, 0], [2, 0, 0], [5, 5, 1]])',
    expect='Black',
    max_steps=90, max_events=60000,
    skip=['def ', 'fill_x, fill_y = None, None', 'for length in range', 'x = sx + length', 'y = sy + length', 'c = piece_dict.get((x, y))',
          'if c == check_c', 'continue', 'if (c == 1 - check_c)', 'return None, None', 'fill_x, fill_y = x, y', 'return fill_x, fill_y',
          'fill_set = set()', 'for index in range(4)', 'fill_x, fill_y = check_line', 'if fill_x is not None', 'fill_set.add', 'dx = [', 'dy = [', 'if c == 0:', _find('for x, y, c in pieces'),
          'piece_dict[(x, y)] = c', 'if piece_dict.get(', 'candidate.add', 'else:'],
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('need_fill', lambda S: len(S['need_fill']) if 'need_fill' in S else None, 'red'),
           ('candidate', lambda S: len(S['candidate']) if 'candidate' in S else None, 'yellow')],
    captions={
        'return fill_set': _cap_cp,
        'if len(check_point(x, y, c)):': lambda S, B, r: ('黑子 `({}, {})`：它的 5 连窗口里有「5 缺 1」吗？有就一手补成五，黑直接胜'.format(S.x, S.y)),
        'need_fill.update(check_point(x, y, c))': '白子 `({x}, {y})` 的「5 缺 1」缺口，收进 `need_fill`',
        'need_fill = set()': '`need_fill` 收集白子所有的「5 缺 1」缺口',
        'return \'Black\'': lambda S, B, r: ('黑一子补成五连 → =="Black"==' if S.get('_line', 0) < _LCAND else '试下的这颗黑子造出 ≥ 2 处「5 缺 1」，白堵不住 → =="Black"=='),
        'if len(need_fill) >= 2': lambda S, B, r: (f'白有 `{len(S.need_fill)}` 处缺口 ≥ 2：黑堵不过来 → =="White"==' if len(S.need_fill) >= 2 else f'白的缺口 `{len(S.need_fill)}` 处，不到 2 处：白没有双杀'),
        'if len(need_fill) == 1': lambda S, B, r: ('白恰好 1 处缺口：黑必须下在这里防守，候选点就只有它' if len(S.need_fill) == 1 else '白没有缺口：黑可以自由发展一子'),
        'candidate = need_fill': '候选点 = 白的缺口（黑被迫防守）',
        'candidate = set()': '候选点：黑子周围距离 ≤ 2 的空位（再远就是孤子，一步连不成五）',
        'for x, y, c in pieces': lambda S, B, r: ('棋子都检查完了' if B.get('x') == S.get('x') and B.get('y') == S.get('y') and 'x' in B
                                                  else (f'黑子 `({S.x}, {S.y})`：沿 4 个方向，把距离 1、2 的空位都加进候选' if S.c == 0 else f'白子 `({S.x}, {S.y})`，不用发展，跳过')
                                                  if S.get('_line', 0) >= _LCAND0 else f'检查棋子 `({S.x}, {S.y})`（{"黑" if S.c == 0 else "白"}）'),
        'for x, y in candidate': '逐个试下候选点（黑第一手）',
        'piece_dict[(x, y)] = 0': '黑第一手试下 `({x}, {y})`',
        'if len(check_point(x, y, 0)) >= 2': '以这颗新子为中心，「5 缺 1」缺口是否 ≥ 2？有则白只能堵一处',
        'piece_dict.pop((x, y))': '不够 2 处：撤回这手，试下一个',
        'return \'None\'': '所有候选都试过，黑造不出双缺口 → =="None"==',
    },
    cards=dict(
        one_liner='找「5 缺 1」：缺口一处就防，两处就输，黑再试着造两处',
        complexity='时间 `O(n·C)`（C 为常数：4 方向 × 5 起点），空间 `O(n)`',
        problem=['无边界五子棋，黑先、黑白黑三步内，先连成同行/列/对角线连续 5 子者胜',
                 '`pieces[i]=[x,y,color]`，`0` 黑 `1` 白；当前无胜者，双方最优',
                 '返回 `"Black"` / `"White"` / `"None"`'],
        quote='如果当前盘面上有5缺1的黑子，那么将其填充成5连，黑就能取胜。……如果存在两个位置可以使得白子形成5连，说明黑防守不过来，此时白能取胜。',
        quote_src='—— yiduobo 题解原文',
        idea=['「5 缺 1」：某个方向的 5 格里 4 子同色、1 格空（XXXX_、XX_XX 都算）',
              '黑有缺口直接赢；白缺口 ≥ 2 → 白赢；恰好 1 处 → 黑被迫防守',
              '否则黑在距离 ≤ 2 处发展一子，若新子造出 ≥ 2 处缺口 → 黑赢，否则和棋'],
        summary=['原文为 Python 2 风格但无需改动，已直接在 Python 3 运行',
                 '检测「5 缺 1」：每个子要看 4 个方向 × 5 种窗口起点，缺口可以在窗口任意位置',
                 '发展黑子只需考虑距离 ≤ 2 的位置，且只检测包含这颗新子的缺口（旧子已检查过）',
                 '视频隐去了窗口内逐格扫描，只展示每个点算出的缺口'],
    ),
)
