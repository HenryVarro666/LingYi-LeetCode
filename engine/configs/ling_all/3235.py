XC, YC = 4, 4
CIRCLES = [[2, 2, 1], [0, 2, 1], [4, 2, 1]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    X, Y, cs = S.get('X'), S.get('Y'), S.get('circles')
    if X is None:
        return
    cv.text((x0 + 18, y0 + 4), f'矩形 (0,0)–({X},{Y})：绿 = 已访问的圆，黄 = 当前 DFS 的圆，粉 = 正在比较的圆', 22, T['muted'], bold=True)
    lo_x = min([0] + [c[0] - c[2] for c in cs]) - 0.3
    hi_x = max([X] + [c[0] + c[2] for c in cs]) + 0.3
    lo_y = min([0] + [c[1] - c[2] for c in cs]) - 0.3
    hi_y = max([Y] + [c[1] + c[2] for c in cs]) + 0.3
    aw, ah = x1 - x0 - 60, y1 - y0 - 80
    sc = min(aw / (hi_x - lo_x), ah / (hi_y - lo_y))
    ox = x0 + 30 + (aw - sc * (hi_x - lo_x)) / 2
    oy = y0 + 56 + (ah - sc * (hi_y - lo_y)) / 2

    def P(x, y):
        return ox + (x - lo_x) * sc, oy + (hi_y - y) * sc

    vis = S.get('vis') or [False] * len(cs)
    cur = S.get('i') if isinstance(S.get('i'), int) and 0 <= S.get('i', -1) < len(cs) else None
    jj = S.get('j') if isinstance(S.get('j'), int) and 0 <= S.get('j', -1) < len(cs) else None
    ln = S.get('_line', 0)
    # 圆
    for k, (cx, cy, r) in enumerate(cs):
        px, py = P(cx, cy)
        R = r * sc
        if k == cur:
            col, a = T['yellow'], 120
        elif k == jj and cur is not None and k != cur and ln >= 11:
            col, a = T['pink'], 110
        elif vis[k]:
            col, a = T['green'], 90
        else:
            col, a = T['blue'], 70
        layer = cv.im
        from PIL import Image, ImageDraw
        lay = Image.new('RGBA', (int(2 * R) + 6, int(2 * R) + 6), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse((2, 2, 2 * R + 3, 2 * R + 3), fill=tuple(col) + (a,), outline=tuple(col) + (255,), width=4)
        cv.im.alpha_composite(lay, (int(px - R - 3), int(py - R - 3)))
        cv.text((px, py), f'{k}', 26, T['text'], anchor='mm', bold=True)
        cv.text((px, py + 28), f'({cx},{cy}) r={r}', 17, T['muted'], anchor='mm', mono=True)
    # 矩形（四条边着色：上/左 红，右/下 蓝）
    a = P(0, 0)
    b = P(X, 0)
    c = P(X, Y)
    d = P(0, Y)
    cv.line([d, c], T['orange'], 6)
    cv.line([a, d], T['orange'], 6)
    cv.line([b, c], T['cyan'], 6)
    cv.line([a, b], T['cyan'], 6)
    cv.text((P(X / 2, Y)[0], P(X / 2, Y)[1] - 6), '上边', 20, T['orange'], anchor='mb', bold=True)
    cv.text((P(0, Y * 0.9)[0] - 8, P(0, Y * 0.9)[1]), '左边', 20, T['orange'], anchor='rm', bold=True)
    cv.text((P(X, Y * 0.1)[0] + 8, P(X, Y * 0.1)[1]), '右边', 20, T['cyan'], anchor='lm', bold=True)
    cv.text((P(X / 2, 0)[0], P(X / 2, 0)[1] + 6), '下边', 20, T['cyan'], anchor='mt', bold=True)
    for p_, nm in ((a, '起点'), (c, '终点')):
        cv.d.ellipse((p_[0] - 8, p_[1] - 8, p_[0] + 8, p_[1] + 8), fill=T['red'])
    # 当前 i 与 j 的「桥」点 A
    if cur is not None and jj is not None and jj != cur and ln >= 11:
        x1_, y1_, r1_ = cs[cur]
        x2_, y2_, r2_ = cs[jj]
        if (x1_ - x2_) ** 2 + (y1_ - y2_) ** 2 <= (r1_ + r2_) ** 2:
            ax, ay = (x1_ * r2_ + x2_ * r1_) / (r1_ + r2_), (y1_ * r2_ + y2_ * r1_) / (r1_ + r2_)
            cv.line([P(x1_, y1_), P(x2_, y2_)], T['pink'], 3)
            pa = P(ax, ay)
            cv.d.ellipse((pa[0] - 9, pa[1] - 9, pa[0] + 9, pa[1] + 9), fill=T['yellow'], outline=T['bg'], width=2)
            cv.text((pa[0], pa[1] - 16), f'A({ax:g},{ay:g})', 22, T['yellow'], anchor='mb', bold=True)


CONFIG = dict(
    num=3235, title='判断矩形的两个角落是否可达', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='圆连成「墙」· DFS 判断是否堵死',
    tags=['七、并查集', '§7.2 进阶', '数学算法', '五、计算几何', '§5.2 圆'],
    code='''
class Solution:
    def canReachCorner(self, X: int, Y: int, circles: List[List[int]]) -> bool:
        vis = [False] * len(circles)
        def dfs(i: int) -> bool:
            x1, y1, r1 = circles[i]
            # 圆 i 是否与矩形右边界/下边界相交相切
            if y1 <= Y and abs(x1 - X) <= r1 or x1 <= X and y1 <= r1:
                return True
            vis[i] = True
            for j, (x2, y2, r2) in enumerate(circles):
                # 在两圆相交相切的前提下，点 A 是否严格在矩形内
                if not vis[j] and \\
                   (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) <= (r1 + r2) * (r1 + r2) and \\
                   x1 * r2 + x2 * r1 < (r1 + r2) * X and \\
                   y1 * r2 + y2 * r1 < (r1 + r2) * Y and \\
                   dfs(j):
                    return True
            return False
        for i, (x, y, r) in enumerate(circles):
            # 圆 i 包含矩形左下角 or
            # 圆 i 包含矩形右上角 or
            # 圆 i 与矩形上边界/左边界相交相切
            if x * x + y * y <= r * r or \\
               (x - X) * (x - X) + (y - Y) * (y - Y) <= r * r or \\
               not vis[i] and (x <= X and abs(y - Y) <= r or y <= Y and x <= r) and dfs(i):
                return False
        return True
''',
    call=f'Solution().canReachCorner({XC}, {YC}, {CIRCLES})',
    expect=False,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='array', var='vis', label='vis（圆是否已访问）', cell=80, h=130),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('x1,y1,r1', "(x1, y1, r1) if 'x1' in locals() else ''", 'cyan')],
    captions={
        3: '`vis[i]` 记录圆 i 是否已经走过',
        19: '依次取圆 `i = {i}`：圆心 `({x}, {y})`，半径 `{r}`',
        23: lambda S, B, r: (f'先判断圆 `{S.i}` 是否盖住起点 (0,0)：`{S.x}² + {S.y}² = {S.x * S.x + S.y * S.y}`，`r² = {S.r * S.r}` → '
                             + ('==盖住了，路径一定被挡 → 返回 False==' if S.x * S.x + S.y * S.y <= S.r * S.r else '没盖住起点')),
        24: lambda S, B, r: (f'再判断是否盖住终点 `({S.X}, {S.Y})`：距离² = `{(S.x - S.X) ** 2 + (S.y - S.Y) ** 2}`，`r² = {S.r * S.r}` → '
                             + ('==盖住了 → 返回 False==' if (S.x - S.X) ** 2 + (S.y - S.Y) ** 2 <= S.r ** 2 else '没盖住终点')),
        25: lambda S, B, r: (f'圆 `{S.i}` 是否碰到==上边界或左边界==？' + ('碰到了 → 从它开始 DFS，看能不能连到右 / 下边界' if (S.x <= S.X and abs(S.y - S.Y) <= S.r or S.y <= S.Y and S.x <= S.r) and not S.vis[S.i]
                                                                      else '没碰到 → 不是「墙」的起点，换下一个圆')),
        5: '进入 `dfs`：当前圆 `({x1}, {y1})`，半径 `{r1}`',
        7: lambda S, B, r: (f'圆 `({S.x1}, {S.y1})` 是否碰到==右边界或下边界==：' + ('碰到了 → 墙从 上 / 左 一路连到 右 / 下，路被堵死' if (S.y1 <= S.Y and abs(S.x1 - S.X) <= S.r1 or S.x1 <= S.X and S.y1 <= S.r1)
                                                                      else f'`|{S.x1} − {S.X}| = {abs(S.x1 - S.X)} > {S.r1}`，也不碰下边界 → 还没连到，继续找相邻的圆')),
        8: '连通了：返回 `True`，表示「有一堵墙」',
        9: '标记圆已访问，避免走回头路',
        10: '枚举每个圆 `j` 看它能不能接上当前圆',
        12: lambda S, B, r: (f'圆 `{S.j}` 已访问过 → 跳过' if S.vis[S.j] else f'圆 `{S.j}` 没访问过，继续看是否相交'),
        13: lambda S, B, r: (f'两圆心距离² = `{(S.x1 - S.x2) ** 2 + (S.y1 - S.y2) ** 2}`，半径和² = `{(S.r1 + S.r2) ** 2}` → '
                             + ('相交或相切，是一座「桥」' if (S.x1 - S.x2) ** 2 + (S.y1 - S.y2) ** 2 <= (S.r1 + S.r2) ** 2 else '不相交，不能接')),
        14: lambda S, B, r: (f'桥的点 A 横坐标 `({S.x1}×{S.r2} + {S.x2}×{S.r1}) / {S.r1 + S.r2} = {(S.x1 * S.r2 + S.x2 * S.r1) / (S.r1 + S.r2):g}`，要严格小于 `X = {S.X}`（交点要落在矩形内，不能只在外面）'),
        15: lambda S, B, r: (f'A 的纵坐标 `{(S.y1 * S.r2 + S.y2 * S.r1) / (S.r1 + S.r2):g}`，要严格小于 `Y = {S.Y}`：点 A 在矩形里，这座桥才真的挡路'),
        16: '桥有效 → 递归 `dfs(j)`，看新的圆能不能继续连到右 / 下边界',
        17: '递归返回 True：墙已经连通，一路返回 `True`',
        18: '这个圆的所有邻居都走不通 → 返回 `False`',
        26: '碰到右 / 下边界的墙存在 → 起点和终点被隔开，返回 ==False==',
        27: '没有任何一堵墙 → 能走到，返回 ==True==',
    },
    cards=dict(
        one_liner='把圆连成「墙」：从上 / 左边界连到右 / 下边界就走不通',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['矩形左下角在原点，右上角 `(X, Y)`；平面里有若干圆',
                 '求一条从 `(0,0)` 到 `(X,Y)` 的路径：只在起终点碰矩形边界，不碰 / 不进任何圆',
                 '本视频：`X = Y = 4`，`circles = [[2,2,1],[0,2,1],[4,2,1]]` → `False`',
                 '三个圆在 `y = 2` 排成一排，把矩形从左到右切断了'],
        quote='如果从矩形【上边界/左边界】到矩形【右边界/下边界】的路被圆堵死，则无法从矩形左下角移动到矩形右上角。',
        quote_src='—— 灵茶山艾府题解',
        idea=['直接找路径太难，反过来想：路是不是被「墙」切断了',
              '圆相交 / 相切 = 一座桥；圆碰到矩形边 = 墙连到边界；两圆交点必须在矩形内才算有效',
              '从碰到 上 / 左 边界的圆出发 DFS，碰到 右 / 下 边界就说明堵死',
              '特判：圆盖住起点或终点时，直接 `False`'],
        summary=['时间 `O(n^2)`：每个圆最多 DFS 一次，每次枚举其他圆',
                 '判断相交相切用整数：距离² `≤` 半径和²，不开方，避免浮点误差',
                 '点 A 用 `x1*r2 + x2*r1 < (r1+r2)*X` 判断，避免除法（交点可能在矩形外）',
                 '原文注：也可以用并查集，但 DFS 更快；圆心可以在矩形外'],
    ),
)
