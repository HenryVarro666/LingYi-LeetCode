INS = 'GGLLGG'
DIRS_ = ((0, 1), (1, 0), (0, -1), (-1, 0))
NAMES = ['北', '东', '南', '西']


def _states():
    x = y = d = 0
    out = [(0, 0, 0)]
    for c in INS:
        if c == 'G':
            x += DIRS_[d][0]
            y += DIRS_[d][1]
        elif c == 'R':
            d = (d + 1) % 4
        else:
            d = (d + 3) % 4
        out.append((x, y, d))
    return out


STATES = _states()
assert len(set(STATES)) == len(STATES)


def _locate(S):
    if 'x' not in S or 'k' not in S:
        return None
    cur = (S['x'], S['y'], S['k'])
    if cur in STATES:
        return STATES.index(cur)
    x, y, d = cur
    for j, c in enumerate(INS):
        px, py, pd = STATES[j]
        if c == 'G' and (x, y, d) == (px + DIRS_[pd][0], py, pd):
            return j
        if c in 'LR' and (x, y) == (px, py) and d in (-1, 4) and pd == (0 if d == -1 else 3):
            return j
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(INS)
    j = _locate(S)
    cv.text((x0 + 18, y0 + 4), f'instructions = "{INS}"（蓝框 = 正在执行的指令）', 24, T['muted'], bold=True)
    cell = min(70, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    ty = y0 + 46
    for i, c in enumerate(INS):
        X = sx + i * cell
        done = j is not None and i < j
        if j is not None and i == j and S.get('_line') != 'ret':
            cv.rect((X + 2, ty, X + cell - 2, ty + cell - 6), fill=T['blue'], alpha=200, r=8)
        cv.text((X + cell / 2, ty + (cell - 6) / 2), c, 34, T['dim'] if done else T['text'], anchor='mm', bold=True, mono=True)
    # plane
    py0 = ty + cell + 24
    pts = STATES
    xs = [p[0] for p in pts] + [0]
    ys = [p[1] for p in pts] + [0]
    gx0, gx1, gy0, gy1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    gw, gh = gx1 - gx0, gy1 - gy0
    sc = min((x1 - x0 - 120) / gw, (y1 - py0 - 30) / gh, 90)
    ox = (x0 + x1) / 2 - (gx0 + gx1) / 2 * sc
    oy = (py0 + y1) / 2 + (gy0 + gy1) / 2 * sc
    P = lambda a, b: (ox + a * sc, oy - b * sc)
    for a in range(gx0, gx1 + 1):
        for b in range(gy0, gy1 + 1):
            px, py = P(a, b)
            cv.rect((px - 3, py - 3, px + 3, py + 3), fill=T['border'], r=3)
    ox_, oy_ = P(0, 0)
    cv.rect((ox_ - 11, oy_ - 11, ox_ + 11, oy_ + 11), outline=T['green'], width=3, r=11)
    cv.text((ox_ + 16, oy_ + 14), '原点', 20, T['green'], anchor='la', bold=True)
    upto = len(INS) if j is None else j
    upto = min(upto, len(INS))
    trail = [P(a, b) for a, b, _ in STATES[:upto + 1]]
    if j is not None and len(trail) >= 1:
        if len(trail) > 1:
            cv.line(trail, T['cyan'], 4)
        if S.get('x', None) is not None:
            pass
    if j is not None:
        cx, cy = P(S['x'], S['y'])
        d = S['k'] % 4
        cv.rect((cx - 14, cy - 14, cx + 14, cy + 14), fill=T['orange'], r=14)
        dx, dy = DIRS_[d]
        cv.arrow((cx, cy), (cx + dx * 44, cy - dy * 44), T['pink'], 5, 14)
        cv.text((x1 - 24, y1 - 30), f'朝{NAMES[d]}  位置 ({S["x"]}, {S["y"]})', 26, T['text'], anchor='rm', bold=True)


CONFIG = dict(
    num=1041, title='困于环中的机器人', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='跑一轮 · 看方向是否回到北',
    tags=['灵神题单', '贪心与思维', '难度分 1521'],
    code='''
DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)  # 上右下左（顺时针）

class Solution:
    def isRobotBounded(self, instructions: str) -> bool:
        x = y = k = 0
        for c in instructions:
            if c == 'G':
                x += DIRS[k][0]
                y += DIRS[k][1]
            else:
                k = (k + ord(c) + 3) % 4
        return k != 0 or x == y == 0
''',
    call='Solution().isRobotBounded("GGLLGG")',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('k', 'k', 'orange'), ('c', 'c', 'cyan')],
    captions={
        'x = y = k = 0': '从原点出发：`x = y = 0`，`k = 0` 表示朝 `DIRS[0] = (0, 1)`，即==北==',
        'for c in instructions': lambda S, B, r: ('一轮指令全部执行完，退出循环' if _locate(S) == len(INS) else f'下一条指令 `{S.c}`'),
        "if c == 'G'": lambda S, B, r: (f'`c = G`：直走' if S.c == 'G' else f'`c = {S.c}`：不是直走，是转向'),
        'x += DIRS': lambda S, B, r: f'横坐标加上 `DIRS[{S.k}][0] = {DIRS_[S.k][0]}` → `x = {S.x}`',
        'y += DIRS': lambda S, B, r: f'纵坐标加上 `DIRS[{S.k}][1] = {DIRS_[S.k][1]}` → `y = {S.y}`',
        'k = (k + ord': lambda S, B, r: (
            f'`ord("{S.c}") = {ord(S.c)}`，`(k + ord + 3) % 4`：'
            + ('==右转==，`k` 加 1' if S.c == 'R' else '==左转==，`k` 加 3（等于减 1）') + f' → `k = {S.k}`，朝{NAMES[S.k]}'),
        'return k != 0': lambda S, B, r: (
            f'一轮后 `k = {S.k}`、位置 `({S.x}, {S.y})`：'
            + ('方向不是北' if S.k != 0 else '方向还是北') + '，'
            + ('回到了原点' if S.x == S.y == 0 else '没回原点') + f' → ==返回 {r}=='),
    },
    cards=dict(
        one_liner='只跑一轮：方向变了，或者回到原点，就一定困在环里',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['机器人在原点朝北，按 `G`（前进）`L`（左转）`R`（右转）循环执行指令',
                 '是否存在一个环，使机器人永远离不开？',
                 '示例：`"GGLLGG"` → `true`，`"GG"` → `false`'],
        quote='如果 w ≠ 1，那么机器人执行完四轮指令后，一定位于原点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一轮后方向变成 `w·d`，第二轮的位移是第一轮的位移旋转 `w`：`z2 = w·z1`',
              '`w ≠ 1` 时四轮位移之和 `(1+w+w²+w³)·z1 = 0`，必回原点',
              '`w = 1`（还朝北）时，只有 `z1 = 0` 才不会越跑越远'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '判断条件：`k != 0 or x == y == 0`',
                 '`ord("R") % 4 + 3 = 1`、`ord("L") % 4 + 3 = 3`，左右转合成一个式子',
                 '另一种写法用复数：`z += d`，`d *= 1j` / `-1j`',
                 '易错：方向 `k` 必须取模 4，否则下标越界'],
    ),
)
