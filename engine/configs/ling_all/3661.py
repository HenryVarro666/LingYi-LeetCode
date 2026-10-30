R0, D0, W0 = [5, 2, 9], [4, 3, 2], [1, 3, 4, 6, 7, 10]
A0 = [(0, 0)] + sorted(zip(R0, D0)) + [(float('inf'), 0)]
SW = sorted(W0)
XMAX = 11


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    px0, px1 = x0 + 50, x1 - 40
    unit = (px1 - px0) / XMAX
    base = y0 + 190

    def X(v):
        return px0 + v * unit
    cv.text((x0 + 18, y0 + 4), '数轴：方块 = 墙，三角 = 机器人（排序后），蓝带 = 往左射，橙带 = 往右射', 22, T['muted'], bold=True)
    i = S.get('i')
    live = i is not None and 'x' in S
    # 当前机器人的两个射程
    if live:
        x, d = S['x'], S['d']
        a = S['a']
        lx = max(x - d, a[i - 1][0] + 1)
        cv.rect((X(max(lx, 0)) - unit * 0.4, base - 62, X(x) + unit * 0.4, base - 8), fill=T['blue'], alpha=70, r=8)
        cv.text((X((max(lx, 0) + x) / 2), base - 84), f'往左 [{lx}, {x}]', 20, T['blue'], anchor='mb', bold=True)
        if 'right_x' in S and S.get('_line', 0) >= 27:
            rx = S['right_x']
            cv.rect((X(x) - unit * 0.4, base - 128, X(rx) + unit * 0.4, base - 74), fill=T['orange'], alpha=70, r=8)
            cv.text((X((x + rx) / 2), base - 150), f'往右 [{x}, {rx}]', 20, T['orange'], anchor='mb', bold=True)
    cv.line([(px0 - 20, base), (px1 + 10, base)], T['border'], 3)
    for v in range(0, XMAX + 1):
        cv.text((X(v), base + 56), v, 16, T['dim'], anchor='mt', mono=True)
    for w in SW:
        cv.rect((X(w) - unit * 0.3, base - 30, X(w) + unit * 0.3, base - 4), fill=(125, 133, 145), r=4)
    for k, (rx_, rd) in enumerate(A0[1:-1], start=1):
        cur = live and k == i
        c = T['yellow'] if cur else T['pink']
        cv.tri_up(X(rx_), base + 8, 12 if cur else 9, c)
        cv.text((X(rx_), base + 34), f'#{k} d={rd}', 17, c, anchor='mt', bold=True)


def _text(S):
    if 'f' not in S:
        return '`f[0]`：右边机器人往左射时的最优；`f[1]`：右边机器人往右射时的最优（只影响右射的射程）'
    return f'`f = [{S["f"][0]}, {S["f"][1]}]`　`f[0]` = 右边机器人往左射；`f[1]` = 右边机器人往右射'


CONFIG = dict(
    num=3661, title='可以被机器人摧毁的最大墙壁数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排序 + 二分 + 状态机 DP（空间优化）',
    tags=['灵神题单', '动态规划', '难度分 2525'],
    code='''
# 手写 min max 更快
min = lambda a, b: b if b < a else a
max = lambda a, b: b if b > a else a

class Solution:
    def maxWalls(self, robots: List[int], distance: List[int], walls: List[int]) -> int:
        n = len(robots)
        a = [(0, 0)] + sorted(zip(robots, distance), key=lambda p: p[0]) + [(inf, 0)]
        walls.sort()

        f = [0, 0]
        for i in range(1, n + 1):
            x, d = a[i]

            # 往左射，墙的坐标范围为 [left_x, x]
            left_x = max(x - d, a[i - 1][0] + 1)  # +1 表示不能射到左边那个机器人
            left = bisect_left(walls, left_x)
            cur = bisect_right(walls, x)
            left_res = f[0] + cur - left  # 下标在 [left, cur-1] 中的墙都能摧毁

            cur = bisect_left(walls, x)
            for j in range(2):
                # 往右射，墙的坐标范围为 [x, right_x]
                x2, d2 = a[i + 1]
                if j == 0:  # 右边那个机器人往左射
                    x2 -= d2
                right_x = min(x + d, x2 - 1)  # -1 表示不能射到右边那个机器人（或者它往左射到的墙）
                right = bisect_right(walls, right_x)
                f[j] = max(left_res, f[1] + right - cur)  # 下标在 [cur, right-1] 中的墙都能摧毁
        return f[1]
''',
    call=f'Solution().maxWalls({R0!r}, {D0!r}, {W0!r})',
    expect=5,
    max_steps=46,
    skip=['min = lambda', 'max = lambda', 'n = len(robots)', 'walls.sort()', 'f = [0, 0]', 'x, d = a[i]', 'left = bisect_left', 'cur = bisect_left(walls, x)', 'x2, d2 = a[i + 1]'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='f', label='f[j]（j=0：右边机器人往左射；j=1：往右射）', h=170, cell=110),
        dict(type='text', fn=_text, size=22, h=60),
    ],
    watch=['i', 'x', 'd', 'left_x', 'left_res', 'j', 'right_x', ('f', 'f', 'green')],
    captions={
        'a = [(0, 0)]': '机器人按位置排序，前后各加一个哨兵（位置 0 和 ∞）省边界判断',
        'for i in range(1, n + 1)': lambda S, B, r: (f'处理第 `{S.i}` 个机器人（从左到右）' if S.get('i') != B.get('i') else '所有机器人处理完了'),
        'left_x = max': '机器人 `x = {x}`，射程 `d = {d}`。往左最远 `x − d = {x - d}`，不能越过左邻居（`{a[i-1][0]} + 1`）→ `left_x = {left_x}`',
        'cur = bisect_right(walls, x)': '二分：`[left_x, x]` 里的墙，下标从 `left = {left}` 到 `cur − 1 = {cur - 1}`',
        'left_res =': '往左射：我们往左射时左边的最优 `f[0] = {f[0]}` + 墙数 `cur − left = {cur - left}` → `left_res = {left_res}`',
        'for j in range(2)': lambda S, B, r: (f'`j = {S.j}`：假设右邻居{"往左" if S.j == 0 else "往右"}射，算我们往右射的墙数' if S.get('j') != B.get('j') or S.get('i') != B.get('i')
                                              else '`j` 两种情况都算完'),
        'x2 -= d2': '右邻居往左射，会占住 `[x2 − d2, x2]`，我们不能进入',
        'right_x = min': lambda S, B, r: ('右边没有机器人（哨兵 ∞），只受射程限制：`right_x = ' + str(S.right_x) + '`' if S.x2 == float('inf')
                                          else f'往右最远 `min(x + d, x2 − 1) = {S.right_x}`（`x2 = {S.x2}`：不能射到右邻居，或它往左射到的墙）'),
        'right = bisect_right': lambda S, B, r: (f'二分：`[x, right_x]` 里的墙下标 `cur = {S.cur}` 到 `right − 1 = {S.right - 1}`，往右射到 `{S.right - S.cur}` 堵' if S.right >= S.cur
                                                 else f'`right = {S.right} < cur = {S.cur}`：右邻居挡住了，往右一堵也打不到（差为负，下面的 `max` 会选往左）'),
        'f[j] = max': '`f[{j}] = max(往左 {left_res}, 往右 f[1] = {B.f[1]} 加 {right - cur})` = =={f[j]}==',
        'return f[1]': '最后一个机器人右边没有机器人：答案 `f[1] = `=={f[1]}==',
    },
    cards=dict(
        one_liner='每个机器人只有「往左」「往右」两种选择，用状态机 DP 逐个决定',
        complexity='时间 `O(n log n + m log m + n log m)`，空间 `O(n)`',
        problem=['数轴上有机器人和墙，每个机器人一发子弹，向左或向右射出，最远 `distance[i]`',
                 '子弹打到别的机器人就停下，不会越过；求最多能摧毁多少堵墙',
                 '示例：`robots=[5,2,9]`、`distance=[4,3,2]`、`walls=[1,3,4,6,7,10]` → `5`'],
        quote='定义状态为 dfs(i,j)，表示对于（排序后）下标在 [0,i] 中的机器人，在机器人 i+1 往左/右射击的前提下，能摧毁的最大墙壁数量。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，每个机器人的射程只受左右邻居影响：往左不能越过左邻居，往右不能越过右邻居',
              '`f[j]`：右边邻居往左（`j=0`）或往右（`j=1`）射时的最优；只影响「往右射」的射程',
              '墙数用二分算：`[left, cur-1]` 或 `[cur, right-1]` 里的墙都能摧毁'],
        summary=['时间 `O(n log n + m log m + n log m)`，二分是 `log m`',
                 '易错：往左射用 `a[i-1][0] + 1`，往右射用右邻居位置或其左射到的位置再 `-1`',
                 '易错：`bisect_right(walls, x)` 与 `bisect_left(walls, x)` 区分「含 x 处的墙」与否',
                 '灵神还给了记忆化搜索 `dfs(i, j)`、二维递推和「双指针代替二分」的写法；本视频演示空间优化版'],
    ),
)
