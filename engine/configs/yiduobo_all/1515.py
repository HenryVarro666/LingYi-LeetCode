PTS = [[10, 10], [80, 20], [40, 80], [70, 70]]
RNG = 100.0   # 画布显示的坐标范围 0..100（与代码里的搜索范围一致）


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '服务中心候选位置（点 = 客户，蓝线 = 三分 x，粉线 = 三分 y）', 22, T['muted'], bold=True)
    pw = min(x1 - x0 - 120, y1 - y0 - 150)
    ox, oy = x0 + 60 + (x1 - x0 - 120 - pw) / 2, y0 + 60
    def px(v):
        return ox + max(-0.15, min(v / RNG, 1.15)) * pw * 0.85
    def py(v):
        return oy + pw * 0.85 - max(-0.15, min(v / RNG, 1.15)) * pw * 0.85
    cv.rect((px(0), py(RNG), px(RNG), py(0)), outline=T['border'], width=2)
    for g in (0, 25, 50, 75, 100):
        cv.text((px(g), py(0) + 8), g, 18, T['dim'], anchor='mt', mono=True)
        cv.text((px(0) - 8, py(g)), g, 18, T['dim'], anchor='rm', mono=True)
    # x 的搜索区间
    if 'lx' in S and 'rx' in S:
        a, b = max(S['lx'], 0), min(S['rx'], RNG)
        if S['rx'] - S['lx'] > 0:
            cv.rect((px(a), py(RNG), px(b), py(0)), fill=T['blue'], alpha=28)
    for nm, c in (('mx1', 'cyan'), ('mx2', 'cyan')):
        if nm in S and S.get('_inner', {}).get('xc') is None:
            X = px(S[nm])
            cv.dashed((X, py(RNG)), (X, py(0)), T[c], 3)
    xc = S.get('xc')
    if xc is not None:
        X = px(xc)
        cv.line([(X, py(RNG)), (X, py(0))], T['blue'], 4)
        cv.text((X, py(RNG) - 6), f'xc={xc:.1f}', 20, T['blue'], anchor='mb', bold=True)
        if 'ly' in S and 'ry' in S and S['ry'] - S['ly'] > 0:
            a, b = max(S['ly'], 0), min(S['ry'], RNG)
            cv.rect((px(0), py(b), px(RNG), py(a)), fill=T['pink'], alpha=26)
        for nm in ('my1', 'my2'):
            if nm in S:
                Y = py(S[nm])
                cv.dashed((px(0), Y), (px(RNG), Y), T['pink'], 3)
                cv.text((px(RNG) + 6, Y), nm, 18, T['pink'], anchor='lm', bold=True)
        # 当前试探点到各客户的连线
        if 'my1' in S:
            cx, cy = X, py(S['my1'] if S.get('_line') in (22, 23, 24, 25, 26) else S.get('ly', S['my1']))
            for (x, y) in PTS:
                cv.line([(cx, cy), (px(x), py(y))], T['yellow'], 2)
            cv.tri_up(cx, cy + 12, 10, T['yellow'])
    for (x, y) in PTS:
        cv.rect((px(x) - 9, py(y) - 9, px(x) + 9, py(y) + 9), fill=T['orange'], r=9)
        cv.text((px(x) + 14, py(y) - 14), f'({x},{y})', 18, T['text'], anchor='lb')
    yt = py(0) + 44
    if xc is None and 'lx' in S:
        cv.text((x0 + 18, yt), f"x 区间 [{S['lx']:.3f}, {S['rx']:.3f}]，宽 {S['rx']-S['lx']:.3f}", 22, T['blue'], bold=True)
    elif xc is not None and 'ly' in S:
        cv.text((x0 + 18, yt), f"固定 xc，y 区间 [{S['ly']:.3f}, {S['ry']:.3f}]，宽 {S['ry']-S['ly']:.3f}", 22, T['pink'], bold=True)


def _cap_cmp_x(S, B, ret):
    return (f"`dis1 = {S.dis1:.3f}`，`dis2 = {S.dis2:.3f}`：" +
            ('dis1 更小 → 最优在 mx2 左边，==rx = mx2==（砍掉右 1/3）' if S.dis1 < S.dis2 else 'dis2 不大于 dis1 → ==lx = mx1==（砍掉左 1/3）'))


def _cap_cmp_y(S, B, ret):
    return (f"`dis1 = {S.dis1:.3f}`，`dis2 = {S.dis2:.3f}`：" +
            ('my1 更优 → ==ry = my2==' if S.dis1 < S.dis2 else 'my2 不差于 my1 → ==ly = my1=='))


CONFIG = dict(
    num=1515, title='服务中心的最佳位置', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='凸函数 · 嵌套三分',
    tags=[],
    code='''
class Solution(object):
    def getMinDistSum(self, positions):

        lx, rx = 0.0, 100.0
        while rx - lx > 0.000001:
            mx1 = lx + (rx - lx) / 3
            mx2 = lx + (rx - lx) / 3 * 2
            dis1 = self.get_dis(mx1, positions)
            dis2 = self.get_dis(mx2, positions)
            if dis1 < dis2:
                rx = mx2
            else:
                lx = mx1
        
        return self.get_dis(lx, positions)
    
    def get_dis(self, xc, positions):
        ly, ry = 0.0, 100.0
        while ry - ly > 0.000001:
            my1 = ly + (ry - ly) / 3
            my2 = ly + (ry - ly) / 3 * 2
            dis1 = dis2 = 0.0
            for x, y in positions:
                dis1 += ((x - xc) ** 2 + (my1 - y) ** 2) ** 0.5
                dis2 += ((x - xc) ** 2 + (my2 - y) ** 2) ** 0.5
            
            if dis1 < dis2:
                ry = my2
            else:
                ly = my1
        
        res = 0.0
        for x, y in positions:
            res += ((x - xc) ** 2 + (ly - y) ** 2) ** 0.5

        return res
''',
    call='Solution().getMinDistSum([[10,10],[80,20],[40,80],[70,70]])',
    expect=156.9638,
    result_fn=lambda r: round(r, 4),
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('lx', 'lx'), ('rx', 'rx'), ('dis1', 'round(dis1, 3)', 'blue'), ('dis2', 'round(dis2, 3)', 'pink')],
    max_steps=52, max_events=600000,
    skip=[19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 32, 33, 34],   # 内层三分的循环体与外层完全同构，只保留入口和返回
    captions={
        'lx, rx = 0.0': '外层三分 x：搜索范围 `[0, 100]`（题目坐标 0..100）',
        'while rx - lx': lambda S, B, r: (f'`rx - lx = {S.rx - S.lx:.6f}` 还大于 1e-6 → 继续三分 x' if S.rx - S.lx > 0.000001 else '`rx - lx` 已小于 1e-6：x 收敛'),
        'mx1 = lx': '`mx1` = 区间左 1/3 点 = =={mx1:.3f}==',
        'mx2 = lx': '`mx2` = 区间右 1/3 点 = =={mx2:.3f}==',
        'dis1 = self.get_dis(mx1': '在 `x = mx1` 处，把 y 也三分到最优，得到最小总距离 `dis1`',
        'dis2 = self.get_dis(mx2': '在 `x = mx2` 处同样求最优 y，得到 `dis2`',
        'if dis1 < dis2': _cap_cmp_x,
        'rx = mx2': '`rx = mx2 = {rx:.3f}`：凸函数，最优不会在 mx2 右边',
        'lx = mx1': '`lx = mx1 = {lx:.3f}`：凸函数，最优不会在 mx1 左边',
        'return self.get_dis(lx': 'x 已收敛，再算一次该 x 下的最优 y 的总距离，即答案',
        'ly, ry = 0.0': '内层：固定 `xc = {xc:.3f}`，对 y 做同样的三分（约 45 轮，视频略过循环体）',
        'while ry - ly': lambda S, B, r: (f'`ry - ly = {S.ry - S.ly:.6f}` 还大于 1e-6 → 继续三分 y' if S.ry - S.ly > 0.000001 else '`ry - ly` 小于 1e-6：y 收敛'),
        'my1 = ly': '`my1` = y 区间左 1/3 点 = =={my1:.3f}==',
        'my2 = ly': '`my2` = y 区间右 1/3 点 = =={my2:.3f}==',
        'dis1 = dis2 = 0.0': '清零，准备累加两个候选点到所有客户的欧氏距离之和',
        'dis1 += ': '`dis1` 累加客户 `({x}, {y})` 到 `(xc, my1)` 的距离 → {dis1:.3f}',
        'dis2 += ': '`dis2` 累加客户 `({x}, {y})` 到 `(xc, my2)` 的距离 → {dis2:.3f}',
        'ry = my2': '`ry = my2 = {ry:.3f}`：my1 更近，最优在 my2 下方',
        'ly = my1': '`ly = my1 = {ly:.3f}`：my2 不差，最优在 my1 上方',
        'res = 0.0': 'y 已收敛到 `ly = {ly:.3f}`，计算此处的总距离',
        'res += ': '累加客户 `({x}, {y})` 到 `(xc, ly)` 的距离 → {res:.3f}',
        'return res': '`x = {xc:.3f}` 时，y 三分收敛到 `ly = {ly:.3f}`，最优总距离 =={res:.3f}==',
    },
    cards=dict(
        one_liner='总距离是凸函数：x 三分里套 y 三分，一路砍掉 1/3',
        complexity='时间 `O(n·log²(1/ε))`，空间 `O(1)`',
        problem=['平面上有若干客户 `positions`，选一个点建服务中心',
                 '使它到所有客户的==欧氏距离之和==最小，返回这个最小值',
                 '本视频：`[[10,10],[80,20],[40,80],[70,70]]` → `156.96`'],
        quote='知道f是一个凸函数之后，其局部极值就是全局最优值……我在这里采用的三分法来逼近。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f(x, y)` 是凸函数：局部最小 = 全局最小，可以用三分逼近',
              '先三分 x：取两个三分点 `mx1`、`mx2`，哪个函数值小，就砍掉另一侧的 1/3',
              '每个 x 的函数值，要先把 y 也三分到最优（`get_dis`）才能比较'],
        summary=['时间约 `O(n·log²)`：外层约 45 次 × 内层约 45 次 × n 个点',
                 '三分只对凸（单峰）函数成立；这里每个 `sqrt` 项都是凸函数，求和仍凸',
                 '搜索范围 `[0, 100]` 来自题目坐标范围；`1e-6` 是精度阈值',
                 '返回浮点数，题目允许 1e-5 误差；视频中取整只用于校验 `expect`',
                 '步数很多，视频只展示开头若干轮与最后的收敛，中间快进'],
    ),
)
