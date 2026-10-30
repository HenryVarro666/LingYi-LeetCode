def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'sx' not in S:
        return
    sx, sy, fx, fy = S['sx'], S['sy'], S['fx'], S['fy']
    lo_x, hi_x = min(sx, fx) - 1, max(sx, fx) + 1
    lo_y, hi_y = min(sy, fy) - 1, max(sy, fy) + 1
    nx, ny = hi_x - lo_x + 1, hi_y - lo_y + 1
    cell = min(80, (x1 - x0 - 40) / nx, (y1 - y0 - 120) / ny)
    gx = x0 + 20 + ((x1 - x0 - 40) - cell * nx) / 2
    gy = y0 + 50
    cv.text((x0 + 18, y0 + 4), '网格（蓝 = 起点，绿 = 终点，黄线 = 斜线 + 直线的最短路）', 22, T['muted'], bold=True)
    for i in range(nx):
        for j in range(ny):
            cv.rect((gx + i * cell + 2, gy + j * cell + 2, gx + (i + 1) * cell - 2, gy + (j + 1) * cell - 2),
                    fill=T['panel2'], r=6)

    def ctr(x, y):
        return gx + (x - lo_x) * cell + cell / 2, gy + (y - lo_y) * cell + cell / 2
    for (x, y, c, nm) in ((sx, sy, T['blue'], '起'), (fx, fy, T['green'], '终')):
        a, b = ctr(x, y)
        cv.rect((a - cell / 2 + 2, b - cell / 2 + 2, a + cell / 2 - 2, b + cell / 2 - 2), fill=c, r=6)
        cv.text((a, b), nm, 28, T['bg'], anchor='mm', bold=True)
    if (sx, sy) != (fx, fy) and 'xy' in S:
        d = S['xy']
        dx = (fx > sx) - (fx < sx)
        dy = (fy > sy) - (fy < sy)
        mx, my = sx + dx * d, sy + dy * d
        cv.dashed(ctr(sx, sy), ctr(mx, my), T['yellow'], 4)
        cv.dashed(ctr(mx, my), ctr(fx, fy), T['yellow'], 4)


def _info(S):
    if 'x' not in S:
        return ''
    s = f"x = {S['x']}，y = {S['y']}"
    if 'xy' in S:
        s += f"，斜线 `min(x, y)` = {S['xy']}"
    if 'min_cost' in S:
        s += f"，min_cost = =={S['min_cost']}==，t = {S['t']}"
    return s


CONFIG = dict(
    num=2849, title='判断能否在给定时间到达单元格', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='最短步数 + 多余步数分类讨论',
    code='''
class Solution(object):
    def isReachableAtTime(self, sx, sy, fx, fy, t):

        x = abs(sx - fx)
        y = abs(sy - fy)
        xy = min(x, y)
        
        min_cost = x + y - xy
        if min_cost > t:
            return False
        
        if x == 0 and y == 0 and t == 1:
            return False
        
        return True
''',
    call='[Solution().isReachableAtTime(2, 4, 7, 7, 6), Solution().isReachableAtTime(3, 1, 7, 3, 3), Solution().isReachableAtTime(2, 2, 2, 2, 1)]',
    expect=[True, False, False],
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', fn=_info, h=70),
    ],
    watch=['x', 'y', 'xy', 'min_cost', 't'],
    captions={
        'x = abs': '水平方向距离 `x = {x}`',
        'y = abs': '竖直方向距离 `y = {y}`',
        'xy = min': '一步斜线胜过一横加一竖，能走的斜线数 `min(x, y)` = =={xy}==',
        'min_cost = ': '最短步数 `x + y - min(x, y)` = `{x} + {y} - {xy}` = =={min_cost}==',
        'if min_cost > t': '最短都要 `{min_cost}` 步，`t = {t}`：{"走不到 → False" if min_cost > t else "时间够，再看多出来的步数"}',
        'if x == 0': '唯一的例外：起点终点重合（`x = y = 0`）且 `t = 1`，一步必然离开 → {"成立，返回 False" if x == 0 and y == 0 and t == 1 else "不是这种情况"}',
        'return False': '`min_cost > t` 或重合且 `t = 1` → 到不了：`False`',
        'return True': '`t - min_cost >= 2` 可左右横跳或绕三步浪费；差 1 也能用斜线替代直线浪费 → `True`',
    },
    cards=dict(
        one_liner='先算最短步数，多出来的步数几乎总能浪费掉',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['无限网格，每秒必须走到相邻 8 格之一，问能否恰好 `t` 秒到 `(fx, fy)`',
                 '示例：`(2,4)→(7,7), t=6` → `true`；`(3,1)→(7,3), t=3` → `false`',
                 '本视频另加一组：起点终点重合且 `t=1` → `false`'],
        quote='可以发现，一步斜线是比一步水平加一步竖直更优的，因此应该尽量走斜线。令x和y分别表示从起点与终点在水平方向和竖直方向的距离，那么可以走的斜线的数量就是min(x, y)。',
        quote_src='—— yiduobo 题解原文',
        idea=['`min_cost = x + y - min(x, y)`：先走斜线再走直线',
              '`min_cost > t` 必然 False；多 2 步以上：左右横跳 / 绕三步消耗',
              '刚好多 1 步：路径上只要动过，就能用斜线加回退替换一步，只有原地不动的 `t = 1` 例外'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：重合时 `t = 0` 成立，`t = 1` 不成立，`t >= 2` 成立',
                 '原文为 Python 2 风格，代码逐字保留，只删去了空行里的说明',
                 '对比灵神：灵神直接用 max(|dx|, |dy|)，这里把斜线数拆开推导，并逐类证明多余步数可浪费'],
    ),
)
