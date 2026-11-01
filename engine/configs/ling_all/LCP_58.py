CODE = '''
# 每条边压缩成二进制
def encode(a):
    res = [[0, 0] for _ in range(4)]
    n = len(a)
    for i, b in enumerate(a[0]):
        res[0][0] |= (b & 1) << i  # 正向
        res[0][1] |= (b & 1) << (n - 1 - i)  # 反向
        res[2][0] |= (a[n - 1][i] & 1) << i
        res[2][1] |= (a[n - 1][i] & 1) << (n - 1 - i)
    for i, r in enumerate(a):
        res[1][0] |= (r[n - 1] & 1) << i
        res[1][1] |= (r[n - 1] & 1) << (n - 1 - i)
        res[3][0] |= (r[0] & 1) << i
        res[3][1] |= (r[0] & 1) << (n - 1 - i)
    return res

# 顺时针旋转矩阵 90°
def rotate(a):
    n, m = len(a), len(a[0])
    b = [None] * m
    for i in range(len(b)):
        b[i] = [0] * n
    for i, r in enumerate(a):
        for j, v in enumerate(r):
            b[j][n - 1 - i] = v
    return b

class Solution:
    def composeCube(self, shapes: List[List[str]]) -> bool:
        n = len(shapes[0])
        a = [[[None] * 4 for _ in range(8)] for _ in range(6)]  # [积木][旋转+翻转][边][0-正向/1-反向]
        for i, shape in enumerate(shapes):
            t = [None] * n
            for j, s in enumerate(shape):
                t[j] = list(s.encode())
            for j in range(4):
                a[i][j] = encode(t)
                t = rotate(t)
            for r in t:
                for j in range(n // 2):
                    r[j], r[n - 1 - j] = r[n - 1 - j], r[j]
            for j in range(4, 8):
                a[i][j] = encode(t)
                t = rotate(t)

        # 判断两条边是否恰好重叠（除了顶角）
        MASK = (1 << (n - 1)) - 2
        def ok(v, w):
            return v & w == 0 and (v | w) & MASK == MASK

        fill = [(0, 0)] * 6  # 枚举每个积木以什么旋转/翻转姿势放在哪个面（0-顶面，1234-侧面，5-底面）
        vis = 0
        def dfs(p):  # 当前考虑的面
            nonlocal vis
            if p == 6:
                return True
            for cur in range(1, 6):  # 枚举 6 个积木（固定第一个积木放在顶面）
                if vis >> cur & 1 > 0:
                    continue
                vis ^= 1 << cur
                for rot in range(8):  # 枚举 8 种旋转+翻转的情况
                    if p == 1:
                        # 1 和 0 是否有冲突
                        if not ok(a[cur][rot][0][0], a[0][0][2][0]):
                            continue
                    elif p == 2:
                        # 2 和 0 1 是否有冲突
                        w, r = fill[p - 1]
                        if (not ok(a[cur][rot][0][0], a[0][0][1][1]) or  # 边是否冲突
                                not ok(a[cur][rot][3][0], a[w][r][1][0]) or
                                a[0][0][2][1] & 1 == 0 and a[cur][rot][0][0] & 1 == 0 and a[w][r][0][1] & 1 == 0):  # 角是否冲突
                            continue
                    elif p == 3:
                        # 3 和 0 2 是否有冲突
                        w, r = fill[p - 1]
                        if (not ok(a[cur][rot][0][0], a[0][0][0][1]) or
                                not ok(a[cur][rot][3][0], a[w][r][1][0]) or
                                a[0][0][1][0] & 1 == 0 and a[cur][rot][0][0] & 1 == 0 and a[w][r][0][1] & 1 == 0):
                            continue
                    elif p == 4:
                        # 4 和 0 1 3 是否有冲突
                        w, r = fill[p - 1]
                        w1, r1 = fill[1]
                        if (not ok(a[cur][rot][0][0], a[0][0][3][0]) or
                                not ok(a[cur][rot][3][0], a[w][r][1][0]) or
                                not ok(a[cur][rot][1][0], a[w1][r1][3][0]) or
                                a[0][0][3][0] & 1 == 0 and a[cur][rot][0][0] & 1 == 0 and a[w][r][0][1] & 1 == 0 or
                                a[0][0][2][0] & 1 == 0 and a[cur][rot][0][1] & 1 == 0 and a[w1][r1][0][0] & 1 == 0):
                            continue
                    else:
                        # 5 和 1 2 3 4 是否有冲突
                        w1, r1 = fill[1]
                        w2, r2 = fill[2]
                        w3, r3 = fill[3]
                        w4, r4 = fill[4]
                        if (not ok(a[cur][rot][0][0], a[w1][r1][2][0]) or
                                not ok(a[cur][rot][1][0], a[w2][r2][2][0]) or
                                not ok(a[cur][rot][2][1], a[w3][r3][2][0]) or
                                not ok(a[cur][rot][3][1], a[w4][r4][2][0]) or
                                a[cur][rot][0][1] & 1 == 0 and a[w1][r1][2][1] & 1 == 0 and a[w2][r2][2][0] & 1 == 0 or
                                a[cur][rot][1][1] & 1 == 0 and a[w2][r2][2][1] & 1 == 0 and a[w3][r3][2][0] & 1 == 0 or
                                a[cur][rot][2][0] & 1 == 0 and a[w3][r3][2][1] & 1 == 0 and a[w4][r4][2][0] & 1 == 0 or
                                a[cur][rot][0][0] & 1 == 0 and a[w4][r4][2][1] & 1 == 0 and a[w1][r1][2][0] & 1 == 0):
                            continue
                    fill[p] = (cur, rot)
                    if dfs(p + 1):
                        return True
                vis ^= 1 << cur
            return False
        return dfs(1)
'''


def _ln(sub, k=0):
    ls = [i for i, l in enumerate(CODE.strip('\n').split('\n'), 1) if sub in l]
    return ls[k]


SHAPES = [["110","011","000"],["000","010","111"],["000","110","000"],["011","010","000"],["110","011","110"],["011","111","011"]]

def _rot(g):
    n = len(g)
    return [[g[n - 1 - j][i] for j in range(n)] for i in range(n)]


def _orient(shape, rot):
    g = [list(s) for s in shape]
    if rot >= 4:
        g = [row[::-1] for row in g]
    for _ in range(rot % 4):
        g = _rot(g)
    return g


def _ok(v, w, MASK):
    return v & w == 0 and (v | w) & MASK == MASK


def _conds(S):
    """复刻代码里每一层的判断：返回 (边检查列表, 角检查列表)"""
    a, cur, rot, p, fill, MASK = S['a'], S['cur'], S['rot'], S['p'], S['fill'], S['MASK']
    A = a[cur][rot]
    a0 = a[0][0]
    if p == 1:
        e = [('1 上边 ↔ 0 下边', A[0][0], a0[2][0])]
        c = []
    elif p == 2:
        w, r = fill[1]
        e = [('2 上边 ↔ 0 右边', A[0][0], a0[1][1]), ('2 左边 ↔ 1 右边', A[3][0], a[w][r][1][0])]
        c = [a0[2][1] & 1 == 0 and A[0][0] & 1 == 0 and a[w][r][0][1] & 1 == 0]
    elif p == 3:
        w, r = fill[2]
        e = [('3 上边 ↔ 0 上边', A[0][0], a0[0][1]), ('3 左边 ↔ 2 右边', A[3][0], a[w][r][1][0])]
        c = [a0[1][0] & 1 == 0 and A[0][0] & 1 == 0 and a[w][r][0][1] & 1 == 0]
    elif p == 4:
        w, r = fill[3]
        w1, r1 = fill[1]
        e = [('4 上边 ↔ 0 左边', A[0][0], a0[3][0]), ('4 左边 ↔ 3 右边', A[3][0], a[w][r][1][0]),
             ('4 右边 ↔ 1 左边', A[1][0], a[w1][r1][3][0])]
        c = [a0[3][0] & 1 == 0 and A[0][0] & 1 == 0 and a[w][r][0][1] & 1 == 0,
             a0[2][0] & 1 == 0 and A[0][1] & 1 == 0 and a[w1][r1][0][0] & 1 == 0]
    else:
        (w1, r1), (w2, r2), (w3, r3), (w4, r4) = fill[1], fill[2], fill[3], fill[4]
        e = [('5 上边 ↔ 1 下边', A[0][0], a[w1][r1][2][0]), ('5 右边 ↔ 2 下边', A[1][0], a[w2][r2][2][0]),
             ('5 下边 ↔ 3 下边', A[2][1], a[w3][r3][2][0]), ('5 左边 ↔ 4 下边', A[3][1], a[w4][r4][2][0])]
        c = [A[0][1] & 1 == 0 and a[w1][r1][2][1] & 1 == 0 and a[w2][r2][2][0] & 1 == 0,
             A[1][1] & 1 == 0 and a[w2][r2][2][1] & 1 == 0 and a[w3][r3][2][0] & 1 == 0,
             A[2][0] & 1 == 0 and a[w3][r3][2][1] & 1 == 0 and a[w4][r4][2][0] & 1 == 0,
             A[0][0] & 1 == 0 and a[w4][r4][2][1] & 1 == 0 and a[w1][r1][2][0] & 1 == 0]
    return [(nm, v, w, _ok(v, w, MASK)) for nm, v, w in e], c


def _verdict(S):
    e, c = _conds(S)
    bad = [x[0] for x in e if not x[3]]
    if bad:
        return False, f'冲突：{bad[0]}'
    if any(c):
        return False, '边都吻合，但有个角没人盖'
    return True, '边和角都没问题 → 可以放'


NET = {0: (1, 1, 0), 1: (1, 2, 0), 2: (2, 1, 3), 3: (1, 0, 2), 4: (0, 1, 1), 5: (1, 3, 0)}
FOR_ROT = _ln('for rot in range(8)')
FILL_L = _ln('fill[p] = (cur, rot)')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    shapes = S.get('shapes') or SHAPES
    n = len(shapes[0])
    line = S.get('_line') or 0
    in_dfs = 'p' in S and 'fill' in S
    p = S['p'] if in_dfs else 0
    cand = in_dfs and 1 <= p <= 5 and 'cur' in S and 'rot' in S and FOR_ROT <= line <= FILL_L
    placed = {}
    if in_dfs:
        placed[0] = (0, 0)
        for f in range(1, p):
            placed[f] = tuple(S['fill'][f])
    # ---- 积木一排
    cv.text((x0 + 14, y0 + 2), '6 片积木（黄 = 正在试，蓝 = 已放好）', 21, T['muted'], bold=True)
    pc = min(18, (x1 - x0 - 40) / (6 * (n + 1.4)))
    px0 = x0 + 20
    for k, sh in enumerate(shapes):
        X = px0 + k * (n + 1.4) * pc
        face = [f for f, (wh, _) in placed.items() if wh == k]
        iscand = cand and S['cur'] == k
        g = [list(s) for s in sh]
        col = T['yellow'] if iscand else (T['blue'] if face else T['text'])
        for i in range(n):
            for j in range(n):
                cv.rect((X + j * pc + 1, y0 + 40 + i * pc + 1, X + (j + 1) * pc - 1, y0 + 40 + (i + 1) * pc - 1),
                        fill=col if g[i][j] == '1' else T['panel2'], alpha=255 if g[i][j] == '1' else 120, r=3)
        cv.text((X + n * pc / 2, y0 + 44 + n * pc), f'积木 {k}', 18, col, anchor='mt', bold=True)
    # ---- 展开图
    ty = y0 + 40 + n * pc + 70
    avail = y1 - ty - 70
    c = min(30, avail / (4 * n) - 2)
    fs = n * c
    nx0 = x0 + 28
    cv.text((nx0, ty - 26), '展开图（0 在中间）', 20, T['muted'], bold=True)
    for f, (fx, fy, q) in NET.items():
        X, Y = nx0 + fx * (fs + 6), ty + fy * (fs + 6)
        item = placed.get(f)
        trial = False
        if item is None and cand and f == p:
            item, trial = (S['cur'], S['rot']), True
        if item is None:
            cv.rect((X, Y, X + fs, Y + fs), outline=T['border'], width=2, r=6)
            cv.text((X + fs / 2, Y + fs / 2), f, 26, T['dim'], anchor='mm', bold=True)
            continue
        g = _orient(shapes[item[0]], item[1])
        for _ in range(q):
            g = _rot(g)
        col = T['yellow'] if trial else T['blue']
        for i in range(n):
            for j in range(n):
                cv.rect((X + j * c + 1, Y + i * c + 1, X + (j + 1) * c - 1, Y + (i + 1) * c - 1),
                        fill=col if g[i][j] == '1' else T['panel2'], alpha=255 if g[i][j] == '1' else 110, r=3)
        cv.rect((X, Y, X + fs, Y + fs), outline=col, width=3, r=4)
        cv.text((X + 4, Y + 2), f'面{f}', 15, T['bg'] if g[0][0] == '1' else col, anchor='la', bold=True)
    # ---- 检查表
    rx = nx0 + 3 * (fs + 6) + 20
    cv.text((rx, ty - 26), '边的检查（二进制）', 20, T['muted'], bold=True)
    if cand:
        e, cs = _conds(S)
        cv.text((rx, ty + 4), f'面 {p} ← 积木 {S["cur"]}，姿势 {S["rot"]}', 21, T['yellow'], bold=True)
        cv.text((rx, ty + 32), '青 = 新放的边，粉 = 已放的边', 16, T['dim'])
        yy = ty + 66
        for nm, v, w, good in e:
            cv.text((rx, yy), nm, 18, T['text'], bold=True)
            cv.text((rx + 170, yy), f'{v:0{n}b}', 18, T['cyan'], mono=True, bold=True)
            cv.text((rx + 232, yy), f'{w:0{n}b}', 18, T['pink'], mono=True, bold=True)
            cv.text((rx + 292, yy), '吻合' if good else '冲突', 18, T['green'] if good else T['red'], bold=True)
            yy += 30
        if cs:
            yy += 6
            cv.text((rx, yy), '角：' + ' '.join('空缺' if x else '已盖' for x in cs), 18, T['text'], bold=True)
            yy += 36
        good, msg = _verdict(S)
        cv.text((rx, yy + 4), msg, 18, T['green'] if good else T['red'], bold=True)
    elif in_dfs:
        cv.text((rx, ty + 4), '6 个面全部放好，拼成立方体' if p >= 6 else f'正在为面 {p} 挑积木', 22, T['green'] if p >= 6 else T['text'], bold=True)
        used = [k for k in range(6) if S['vis'] >> k & 1] if 'vis' in S else []
        cv.text((rx, ty + 44), f'已用积木：{used}（0 固定在面 0）', 18, T['muted'])


def _pos(rot):
    return f'翻面后转 {(rot - 4) * 90}°' if rot >= 4 else f'转 {rot * 90}°'


def _end(S, B, name):
    return name in B['_inner'] and B['_inner'][name] == S['_inner'].get(name)


def _chk(S, B, ret):
    good, msg = _verdict(S)
    return f'面 `{S.p}` ← 积木 `{S.cur}`（{_pos(S.rot)}）：{msg}' + ('' if good else ' → ==换下一种姿势==')


_LAST = _ln('MASK = ')

CONFIG = dict(
    num='LCP 58', title='积木拼接', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='搜索 + 位运算检查边角（Go 原文转写）',
    tags=['链表树与回溯'],
    code=CODE,
    call='Solution().composeCube(SHAPES)',
    setup='SHAPES = ' + repr(SHAPES),
    expect=True,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('p', 'p', 'yellow'), ('cur', 'cur', 'blue'), ('rot', 'rot', 'cyan'), ('vis', 'bin(vis)', 'pink')],
    skip=[i for i in range(1, _LAST) if i not in (_ln('n = len(shapes[0])'), _ln('a = [[[None]'))] + [_i for _i, _l in enumerate(CODE.strip('\n').split('\n'), 1) if _l.strip().startswith(('not ok(', 'a['))] + [_ln('for cur in range'), _ln('if p == 6'), _ln('if vis >> cur'), _ln('continue'), _ln('return True', 1), _ln('return dfs(1)')] + ['v & w == 0', 'if p == 1', 'elif p ==', 'w, r = fill', 'w1, r1 = fill', 'w2, r2 = fill', 'w3, r3 = fill', 'w4, r4 = fill'],
    max_steps=80,
    captions={
        'n = len(shapes[0])': '每片积木是 `{n} × {n}` 的方阵',
        'a = [[[None]': '`a[积木][姿势][边][方向]`：6 片积木 × 8 种姿势（4 次旋转 × 翻面）× 4 条边 × 正反两个方向',
        'MASK = ': '前面已经把每片积木 8 种姿势的 4 条边都压成二进制；`MASK = {MASK:0{n}b}` 去掉两端的顶角，只看边的中间',
        'fill = [': '`fill[面]` 记录每个面放的（积木, 姿势）；面 0 固定放积木 0 的原样',
        'vis = 0': '`vis` 用位记录哪些积木用过',
        'return dfs(1)': '从面 1 开始搜索，面 0 固定放积木 0',
        'if p == 6': lambda S, B, r: ('6 个面都放好了 → ==拼成立方体== ，返回 True' if S.p == 6 else f'`p = {S.p}`：还有面没放，继续'),
        'if vis >> cur': lambda S, B, r: (f'积木 `{S.cur}` 已经用过，跳过' if S.vis >> S.cur & 1 else f'积木 `{S.cur}` 还没用，可以试'),
        'vis ^= 1 << cur': lambda S, B, r: (f'给面 `{S.p}` 选一片还没用的积木 `{S.cur}`：`vis` → `{S.vis:06b}`' if not (B.vis >> S.cur & 1) else f'积木 `{S.cur}` 的 8 种姿势都放不下，释放它：`vis` → `{S.vis:06b}`（回溯）'),
        'for rot in range(8)': lambda S, B, r: (f'积木 `{S.cur}` 的 8 种姿势都试过了，面 `{S.p}` 放不下它' if _end(S, B, 'rot') else f'试姿势 `{S.rot}`（{_pos(S.rot)}）'),
        'not ok(': _chk,
        'continue': lambda S, B, r: '边或角冲突 → 这个姿势不行，试下一个',
        'for cur in range(1, 6)': lambda S, B, r: (f'面 `{S.p}` 的积木都试完了，放不下 → 回溯' if _end(S, B, 'cur') else (f'积木 `{S.cur}` 已经放过了，跳过' if S.vis >> S.cur & 1 else f'给面 `{S.p}` 挑还没用的积木：`cur = {S.cur}`')),
        'fill[p] = (cur, rot)': '没有冲突：把积木 `{cur}` 按姿势 `{rot}` 放在面 `{p}`',
        'if dfs(p + 1)': '递归：去放面 `{B.p + 1}`',
        'return True': '6 个面都放好了 → ==拼成立方体==，一路返回 True',
        'return False': '面 `{p}` 无论放哪片积木都不行 → 返回 False，上一层换个放法',
    },
    cards=dict(
        one_liner='搜索每个面放哪片积木：枚举旋转翻转，边要严丝合缝、角不能重叠',
        complexity='时间 `O(6! × 8^5 × 1)`（有剪枝，实际很小），空间 `O(1)`',
        problem=['6 片积木，每片是 `n × n` 的 0/1 方阵（厚度 1），中间一定是实心',
                 '积木可旋转、翻面，要拼成一个正方体，每片正好是一个面',
                 '本视频：6 片 `3 × 3` 积木（示例 1 的顺序做了调整，答案 `true`）'],
        quote='基本思路是搜索每个面放哪块积木，枚举积木的旋转+翻转状态。放之前先检查下当前放的积木和相邻的积木：边是否严丝合缝；角是否有重叠。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每条边压成一个二进制数：`encode` 出 8 种姿势下 4 条边的正向/反向值',
              '两条棱重叠检查：`v & w == 0` 不重叠，`(v | w) & MASK == MASK` 中间不留空',
              '第一块积木固定放顶面，从第二块开始 `dfs`，面 1–5 各检查与已放面的边和角'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`pair` 结构体写成元组 `(who, rot)`，`switch` 写成 `if/elif`）',
                 '精髓是把边压成二进制：重叠、缝隙、拼合都变成位运算',
                 '角的检查：相邻三片在同一个顶点处至少要有一片是 1',
                 '易错点：面的顺序和旋转方向要与 `encode` 的边号约定一致',
                 '视频里为了步数少，把示例 1 的 6 片积木换了顺序（搜索更快找到解）'],
    ),
)
