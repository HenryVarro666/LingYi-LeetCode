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
    cv.text((x0 + 18, y0 + 4), '网格（蓝 = 起点，绿 = 终点，虚线 = 先斜着走再直走）', 22, T['muted'], bold=True)
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
    if (sx, sy) != (fx, fy) and S.get('_line', 0) >= 5:
        d = min(abs(sx - fx), abs(sy - fy))
        dx = (fx > sx) - (fx < sx)
        dy = (fy > sy) - (fy < sy)
        mx, my = sx + dx * d, sy + dy * d
        cv.dashed(ctr(sx, sy), ctr(mx, my), T['yellow'], 4)
        cv.dashed(ctr(mx, my), ctr(fx, fy), T['yellow'], 4)
    if 'fx' in S:
        cv.text((x0 + 20, y1 - 60),
                f"|sx−fx| = {abs(sx - fx)}，|sy−fy| = {abs(sy - fy)}，t = {S['t']}", 26, T['text'], bold=True)


CONFIG = dict(
    num=2849, title='判断能否在给定时间到达单元格', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='切比雪夫距离 + 绕圈消耗',
    code='''
class Solution:
    def isReachableAtTime(self, sx: int, sy: int, fx: int, fy: int, t: int) -> bool:
        if sx == fx and sy == fy:
            return t != 1
        return max(abs(sx - fx), abs(sy - fy)) <= t
''',
    call='[Solution().isReachableAtTime(2, 4, 7, 7, 6), Solution().isReachableAtTime(3, 1, 7, 3, 3), Solution().isReachableAtTime(2, 2, 2, 2, 1)]',
    expect=[True, False, False],
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', fn=lambda S: (f"最快 `max({abs(S['sx']-S['fx'])}, {abs(S['sy']-S['fy'])})` = =={max(abs(S['sx']-S['fx']), abs(S['sy']-S['fy']))}== 秒，对比 `t = {S['t']}`" if 'sx' in S else ''), h=70),
    ],
    watch=['sx', 'sy', 'fx', 'fy', 't'],
    captions={
        'if sx == fx': '起点终点重合吗？`({sx}, {sy})` vs `({fx}, {fy})` → {"重合，要原地绕圈" if sx == fx and sy == fy else "不重合，走最短路"}',
        'return t != 1': '重合时一步必然离开起点，回不来：`t = {t}` → ==t != 1 即可==，返回 =={ret}==',
        'return max': '8 方向走，最快 `max(|dx|, |dy|)` = =={max(abs(sx - fx), abs(sy - fy))}== 秒；`<= t = {t}` 就能在终点附近绕圈耗时间 → =={ret}==',
    },
    cards=dict(
        one_liner='八方向走：最快 max(|dx|, |dy|) 步，多的时间绕圈耗掉',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['无限网格，每秒必须走到相邻 8 格之一，问能否恰好 `t` 秒到 `(fx, fy)`',
                 '示例：`(2,4)→(7,7), t=6` → `true`；`(3,1)→(7,3), t=3` → `false`',
                 '本视频另加一组：起点终点重合且 `t=1` → `false`'],
        quote='最快可以在 max{|sx-fx|, |sy-fy|} 秒后到达终点（先斜着走再直走）。上式只要小于等于 t 就能恰好到达终点。因为我们可以在终点周围不断「绕圈」消耗时间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['斜着走一步同时改变 x 和 y，所以最短时间是较大的那个差',
              '时间有富余就在终点附近绕圈，能拖到最后一秒才到',
              '特殊：起点终点重合时 `t = 1` 无法回到原地，其余 `t` 都能绕圈回来'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：重合且 `t = 1` 要单独判断，`t = 0` 在原地是成立的',
                 '数据到 10^9，不能模拟，必须用公式',
                 '思考题：只能走 4 个方向时，要用曼哈顿距离并看奇偶性'],
    ),
)
