def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g, tg = S['ghosts'], S['target']
    X0, X1, Y0, Y1 = -4, 5, -3, 4
    nx, ny = X1 - X0 + 1, Y1 - Y0 + 1
    cell = min((x1 - x0 - 40) / nx, (y1 - y0 - 60) / ny)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * nx) / 2
    sy = y0 + 40

    def P(x, y):
        return sx + (x - X0 + 0.5) * cell, sy + (Y1 - y + 0.5) * cell
    cv.text((x0 + 18, y0 + 2), '坐标平面（你 = 原点，绿星 = 终点，红点 = 阻碍者）', 22, T['muted'], bold=True)
    for i in range(nx):
        cv.line([(sx + (i + 0.5) * cell, sy + 0.5 * cell), (sx + (i + 0.5) * cell, sy + (ny - 0.5) * cell)], T['border'], 1)
        cv.text((sx + (i + 0.5) * cell, sy + ny * cell), X0 + i, 16, T['dim'], anchor='mt', mono=True)
    for j in range(ny):
        cv.line([(sx + 0.5 * cell, sy + (j + 0.5) * cell), (sx + (nx - 0.5) * cell, sy + (j + 0.5) * cell)], T['border'], 1)
        cv.text((sx + 4, sy + (j + 0.5) * cell), Y1 - j, 16, T['dim'], anchor='lm', mono=True)
    ox, oy = P(0, 0)
    cv.rect((ox - 11, oy - 11, ox + 11, oy + 11), fill=T['blue'], r=4)
    cv.text((ox, oy - 16), '你', 18, T['blue'], anchor='mb', bold=True)
    tx, ty = P(*tg)
    cv.text((tx, ty), '★', int(cell * 0.6), T['green'], anchor='mm', bold=True)
    cur = (S['x'], S['y']) if 'x' in S else None
    for k, (a, b) in enumerate(g):
        px, py = P(a, b)
        hot = cur == (a, b)
        c = T['yellow'] if hot else T['pink']
        if hot:
            cv.line([(px, py), (tx, ty)], T['yellow'], 3)
        cv.rect((px - 11, py - 11, px + 11, py + 11), fill=c, r=11)
        cv.text((px, py - 16), f'#{k}', 18, c, anchor='mb', bold=True)
    if 'dis' in S:
        a, b = P(0, 0)[0], P(0, 0)[1]
        cv.line([(ox, oy), (tx, oy), (tx, ty)], T['blue'], 3)


def _fn(S):
    if 'dis' not in S:
        return '先算你到终点的最短时间'
    s = f"你到终点：`|{S['target'][0]}| + |{S['target'][1]}|` = =={S['dis']}=="
    if 'x' in S:
        d = abs(S['x'] - S['target'][0]) + abs(S['y'] - S['target'][1])
        s += f"　阻碍者 `({S['x']},{S['y']})` 到终点：=={d}=="
    return s


CONFIG = dict(
    num=789, title='逃脱阻碍者', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='曼哈顿距离比较',
    tags=[],
    code='''
class Solution(object):
    def escapeGhosts(self, ghosts, target):

        dis = abs(target[0]) + abs(target[1])
        for x, y in ghosts:
            if abs(x - target[0]) + abs(y - target[1]) <= dis:
                return False

        return True
''',
    call='Solution().escapeGhosts([[4,3],[-3,2],[1,4],[3,0]], [2,-1])',
    expect=False,
    views=[
        dict(type='text', fn=_fn, size=26, h=60),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('dis', 'dis', 'blue'), 'x', 'y'],
    captions={
        'dis = abs': '你从原点走到终点至少 `|{target[0]}| + |{target[1]}|` = =={dis}== 步（没有障碍，就是横纵坐标绝对值之和）',
        'for x, y in ghosts': '取下一个阻碍者 `({x}, {y})`',
        'if abs(x': lambda S, B, r: (
            f"阻碍者到终点 `{abs(S.x - S.target[0]) + abs(S.y - S.target[1])}`，你要 `{S.dis}`："
            + ('它不比你慢 → ==能先到终点守株待兔=='
               if abs(S.x - S.target[0]) + abs(S.y - S.target[1]) <= S.dis else '比你慢 → 拦不住，看下一个')),
        'return False': '有阻碍者不晚于你到终点（相遇也算失败）→ ==逃脱失败== `False`',
        'return True': '所有阻碍者都比你慢 → ==逃脱成功==',
    },
    cards=dict(
        one_liner='阻碍者最优策略：直奔终点守株待兔',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['你从 `(0,0)` 出发去 `target`，每回合你和所有阻碍者各走一步（上下左右或不动）',
                 '任何阻碍者能在你之前或同时与你相遇，你就失败',
                 '示例：`ghosts=[[1,0],[0,3]], target=[0,1]` → `True`；本视频用另一组数据'],
        quote='对于所有阻碍者来说，只需要尽可能早的到达终点，然后守株待兔即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['若中途能拦截你，则从拦截点到终点它和你步数一样 → 终点同样能拦到',
              '无障碍物，最短时间 = 横纵坐标绝对值之和',
              '只要有阻碍者到终点的时间 `<=` 你的时间，就失败'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：==相遇也算失败==，所以用 `<=` 而不是 `<`',
                 '思路转化最关键：把「拦截」转成「谁先到终点」',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
