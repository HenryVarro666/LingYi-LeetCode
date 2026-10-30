R0, D0, W0 = [5, 2, 9], [4, 3, 2], [1, 3, 4, 6, 7, 10]
RI = sorted(zip(R0, D0))
SW = sorted(W0)
XMAX = 11


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    px0, px1 = x0 + 50, x1 - 40
    unit = (px1 - px0) / XMAX
    base = y0 + 170

    def X(v):
        return px0 + v * unit
    cv.text((x0 + 18, y0 + 4), '数轴：方块 = 墙，三角 = 机器人，色带 = 正在数墙的区间', 22, T['muted'], bold=True)
    idx = S.get('index')
    if 'start' in S and 'end' in S:
        s_, e_ = max(S['start'], 0), min(S['end'], XMAX)
        if s_ <= e_:
            cv.rect((X(s_) - unit * 0.45, base - 66, X(e_) + unit * 0.45, base - 6), fill=T['cyan'], alpha=80, r=8)
            cv.text((X((s_ + e_) / 2), base - 88), f'区间 [{S["start"]}, {S["end"]}]', 20, T['cyan'], anchor='mb', bold=True)
        else:
            cv.text((X(XMAX / 2), base - 88), f'区间 [{S["start"]}, {S["end"]}] 为空', 20, T['muted'], anchor='mb', bold=True)
    cv.line([(px0 - 20, base), (px1 + 10, base)], T['border'], 3)
    for v in range(0, XMAX + 1):
        cv.text((X(v), base + 56), v, 16, T['dim'], anchor='mt', mono=True)
    for w in SW:
        cv.rect((X(w) - unit * 0.3, base - 30, X(w) + unit * 0.3, base - 4), fill=(125, 133, 145), r=4)
    for k, (rx_, rd) in enumerate(RI):
        cur = idx is not None and k == idx
        c = T['yellow'] if cur else T['pink']
        cv.tri_up(X(rx_), base + 8, 12 if cur else 9, c)
        cv.text((X(rx_), base + 34), f'#{k} d={rd}', 17, c, anchor='mt', bold=True)


def _text(S):
    if 'f' not in S or S.get('f') is None:
        return '`f[i]`：前 `i` 个机器人开完枪，第 `i` 个==向左==射的最多墙数；`g[i]`：第 `i` 个==向右==射的最多墙数'
    return f'`f = {S["f"]}`（最后一个向左射）　`g = {S["g"]}`（最后一个向右射）'


CONFIG = dict(
    num=3661, title='可以被机器人摧毁的最大墙壁数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='排序 + 二分计数 + 左/右两个状态',
    tags=['灵神题单', '动态规划', '难度分 2525'],
    code='''
class Solution(object):
    def maxWalls(self, robots, distance, walls):
        
        robot_info = sorted((r, d) for r, d in zip(robots, distance))
        walls.sort()
        robot_info.append((walls[-1] + 1, 0))

        def calc(start, end):
            if start > end:
                return 0
            
            if start > walls[-1] or end < walls[0]:
                return 0
            
            left = 0
            right = len(walls) - 1
            while left < right:
                mid = (left + right) // 2
                if walls[mid] >= start:
                    right = mid
                else:
                    left = mid + 1
            
            start_index = left

            left = 0
            right = len(walls) - 1
            while left < right:
                mid = (left + right + 1) // 2
                if walls[mid] <= end:
                    left = mid
                else:
                    right = mid - 1
            
            end_index = left

            return end_index - start_index + 1

        f, g = None, None
        for index in range(len(robot_info) - 1):
            r, d = robot_info[index]
            if index == 0:
                f = calc(max(0, r - d), r)
                g = calc(r, min(robot_info[index + 1][0] - 1, r + d))
            else:
                pre_f, pre_g = f, g
                f_from_f = calc(max(robot_info[index - 1][0] + 1, r - d), r)
                f_from_g = calc(max(robot_info[index - 1][0] + robot_info[index - 1][1] + 1, r - d), r)
                f = max(pre_f + f_from_f, pre_g + f_from_g)
                g = max(pre_f, pre_g) + calc(r, min(robot_info[index + 1][0] - 1, r + d))
        
        return max(f, g)
''',
    call=f'Solution().maxWalls({R0!r}, {D0!r}, {W0!r})',
    expect=5,
    max_steps=60,
    skip=['if start > end', 'if start > walls[-1]', 'left = 0', 'right = len(walls) - 1', 'while left < right',
          'mid = ', 'if walls[mid]', 'right = mid', 'left = mid', 'start_index = left', 'end_index = left',
          'walls.sort()', 'f, g = None, None', 'robot_info = sorted', 'def calc'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_text, size=22, h=70),
    ],
    watch=['index', 'r', 'd', ('f', 'f', 'blue'), ('g', 'g', 'pink'), 'f_from_f', 'f_from_g', 'start', 'end'],
    captions={
        'robot_info.append': '机器人按位置排好序，末尾补一个哨兵 `(最右墙+1, 0)`，方便算「下一个机器人」',
        'for index in range': lambda S, B, r: (f'处理第 `{S.index}` 个机器人' if S.get('index') != B.get('index') else '所有机器人都处理完了'),
        'r, d = robot_info': '位置 `r = {r}`，射程 `d = {d}`',
        'if index == 0': lambda S, B, r: ('第一个机器人：左边没有人挡，右边只受下一个机器人限制' if S.index == 0 else '后面的机器人：要看上一个机器人往哪边射'),
        'f = calc(max(0, r - d), r)': '往左射：覆盖 `[max(0, r−d), r]`（左边没人挡），调用 `calc` 数区间里的墙',
        'g = calc(r, min(robot_info[index + 1][0] - 1, r + d))': '往右射：最远 `min(下一个机器人−1, r+d)`，再调用 `calc` 数区间里的墙',
        'pre_f, pre_g = f, g': '先记下上一个机器人的 `f = {pre_f}`、`g = {pre_g}`',
        'f_from_f = calc': '上一个往左射，不挡我们：往左覆盖 `[max(上一个位置+1, r−d), r]`，调用 `calc` 数墙',
        'f_from_g = calc': '上一个往右射，已经打掉了它射程里的墙：我们往左要从它射程的右边起算，调用 `calc` 数墙',
        'f = max(pre_f + f_from_f': '`f = max(上一个往左 {pre_f} + {f_from_f}, 上一个往右 {pre_g} + {f_from_g})` = =={max(pre_f + f_from_f, pre_g + f_from_g)}==',
        'g = max(pre_f, pre_g)': '往右射不受上一个影响：先取 `max(pre_f, pre_g) = {max(pre_f, pre_g)}`，再加上往右区间里的墙数',
        'return 0': '区间 `[{start}, {end}]` 是空的（或不在墙的范围内）→ 0 堵墙',
        'return end_index': '二分找到区间两端的墙下标，相减加一：`[{start}, {end}]` 里有 =={ret}== 堵墙',
        'return max(f, g)': '最后一个机器人往左或往右都行：`max({f}, {g})` = =={max(f, g)}==',
    },
    cards=dict(
        one_liner='按位置排序，每个机器人只会被前一个机器人影响',
        complexity='时间 `O(n log m)`，空间 `O(1)`',
        problem=['数轴上有机器人和墙，每个机器人一发子弹，向左或向右，最远 `distance[i]`',
                 '子弹碰到别的机器人就停；墙和机器人同位置时，该机器人能打掉那堵墙',
                 '示例：`robots=[5,2,9]`、`distance=[4,3,2]`、`walls=[1,3,4,6,7,10]` → `5`'],
        quote='如果按坐标的顺序决定机器人开枪的方向，那么当前的机器人只可能受前一个机器人的影响，也最多只会影响到下一个机器人。基于这一点，就可以使用动态规划进行求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后用两个状态：`f` = 当前机器人往左射，`g` = 往右射',
              '`f` 要看上一个：上一个往左 → 我们的射程到上一个位置 +1；上一个往右 → 要躲开它的射程',
              '`g` 不受上一个影响，只受下一个机器人限制；区间里的墙数用两次二分算'],
        summary=['时间 `O(n log n + n log m)`，空间 `O(1)`（`f`、`g` 用变量滚动）',
                 '易错：往左要避开上一个往右射到的位置，往右只受下一个机器人限制',
                 '`calc(start, end)` 用两次二分数出区间里的墙数，区间为空要返回 0',
                 '对比灵神：灵神用 `bisect` 并给两端加哨兵，状态是「右邻居往左/往右射」；yiduobo 的状态是「当前往左/往右射」。原文已是 Python 3 可运行写法，未改动'],
    ),
)
