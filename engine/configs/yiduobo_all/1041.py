INS = 'GLGLGL'
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
    if 'x' not in S or 'now_d' not in S:
        return None
    cur = (S['x'], S['y'], S['now_d'])
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
        d = S['now_d'] % 4
        cv.rect((cx - 14, cy - 14, cx + 14, cy + 14), fill=T['orange'], r=14)
        dx, dy = DIRS_[d]
        cv.arrow((cx, cy), (cx + dx * 44, cy - dy * 44), T['pink'], 5, 14)
        cv.text((x1 - 24, y1 - 30), f'朝{NAMES[d]}  位置 ({S["x"]}, {S["y"]})', 26, T['text'], anchor='rm', bold=True)


CONFIG = dict(
    num=1041, title='困于环中的机器人', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='跑一轮 · 分类讨论方向',
    tags=['灵神题单', '贪心与思维', '难度分 1521'],
    code='''
class Solution(object):
    def isRobotBounded(self, instructions):

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        now_d = 0
        x = 0
        y = 0
        for order in instructions:
            if order == 'L':
                now_d -= 1
                if now_d < 0:
                    now_d = 3
            elif order == 'R':
                now_d += 1
                if now_d > 3:
                    now_d = 0
            else:
                x += dx[now_d]
                y += dy[now_d]
        
        if x == 0 and y == 0:
            return True

        return now_d != 0
''',
    call='Solution().isRobotBounded("GLGLGL")',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('now_d', 'now_d', 'orange'), ('order', 'order', 'cyan')],
    skip=['dx = [', 'dy = ['],
    captions={
        'now_d = 0': '`now_d` 是方向下标：0 北、1 东、2 南、3 西，一开始朝北',
        'y = 0': '从原点 `(0, 0)` 出发：`x = y = 0`',
        'for order in instructions': lambda S, B, r: ('一轮指令全部执行完，退出循环' if _locate(S) == len(INS) else f'下一条指令 `{S.order}`'),
        "if order == 'L'": lambda S, B, r: ('`L`：左转' if S.order == 'L' else f'`{S.order}` 不是 `L`，继续判断'),
        'now_d -= 1': '左转一次，方向下标减 1：`now_d = {now_d}`',
        'if now_d < 0': lambda S, B, r: ('`now_d = -1` 越界 → 绕回 3（朝西）' if S.now_d < 0 else f'`now_d = {S.now_d}` 没越界'),
        'now_d = 3': '从北左转到西：`now_d = 3`',
        "elif order == 'R'": lambda S, B, r: ('`R`：右转' if S.order == 'R' else '不是 `L` 也不是 `R`，只剩 `G`：直走'),
        'x += dx': lambda S, B, r: f'朝{NAMES[S.now_d]}走一步，`x += dx[{S.now_d}]` → `x = {S.x}`',
        'y += dy': '`y += dy[{now_d}]` → `y = {y}`',
        'if x == 0 and y == 0': lambda S, B, r: (
            f'一轮结束，位置 `({S.x}, {S.y})`：回到原点 → 必在环里' if S.x == 0 and S.y == 0
            else f'一轮结束，位置 `({S.x}, {S.y})` ≠ 原点，还要看方向'),
        'return True': '回到原点，机器人一直在原地兜圈 → 返回 `True`',
        'return now_d != 0': lambda S, B, r: (
            f'`now_d = {S.now_d}`：' + ('一轮后不再朝北，四轮内必回原点' if S.now_d != 0 else '一轮后还朝北却没回原点，会越走越远') + f' → ==返回 {r}=='),
    },
    cards=dict(
        one_liner='跑一轮：回到原点，或者方向不再朝北，就一定在环里',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['机器人在原点朝北，按 `G`（前进）`L`（左转）`R`（右转）循环执行指令',
                 '是否存在一个环，使机器人永远离不开？',
                 '示例：`"GGLLGG"` → `true`；本视频用 `"GLGLGL"`'],
        quote='若一轮下来方向变成了朝向东方或者西方，那么第二轮之后将朝向南方，接下来的第三轮将抵消掉第一轮同时将方向变为西方或者东方，而第四轮则会抵消掉第二轮，即四轮过后将走回原点。',
        quote_src='—— yiduobo 题解原文',
        idea=['一轮后回到原点：显然在环里',
              '一轮后还朝北：每轮位移相同，只会越走越远',
              '朝南：两轮抵消；朝东/西：四轮抵消 → 方向不是北就一定成环'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先判 `x == 0 and y == 0`，再返回 `now_d != 0`',
                 '左转 `now_d -= 1` 要处理小于 0 绕回 3，右转要处理大于 3 绕回 0',
                 '对比灵神：灵神用 `(k + 3) % 4` 取模，yiduobo 用 if 手动绕回，原文无需改动'],
    ),
)
