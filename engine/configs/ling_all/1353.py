def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ev = S.get('events') or []
    if not ev:
        return
    mx = max(e[1] for e in ev)
    fa = S.get('fa')
    cur = (S['start_day'], S['end_day']) if 'start_day' in S and 'end_day' in S else None
    cv.text((x0 + 18, y0 + 4), '日历：绿色 = 这一天已被占用，黄条 = 当前这场会议的可选天数', 22, T['muted'], bold=True)
    cell = min(110, (x1 - x0 - 60) / (mx + 1))
    sx = x0 + 30
    top = y0 + 44
    for d in range(1, mx + 1):
        used = fa is not None and fa[d] != d
        X = sx + (d - 1) * cell
        in_cur = cur is not None and cur[0] <= d <= cur[1]
        fill = T['green'] if used else (70, 76, 86)
        cv.rect((X + 3, top, X + cell - 3, top + 62), fill=fill, r=8,
                outline=T['yellow'] if (in_cur and not used) else None, width=4)
        cv.text((X + cell / 2, top + 31), d, 28, T['bg'] if used else T['text'], anchor='mm', bold=True)
        if 'x' in S and S['x'] == d:
            cv.text((X + cell / 2, top + 70), '↑ x', 22, T['pink'], anchor='mt', bold=True)
    y = top + 112
    cv.text((x0 + 18, y - 34), '会议（已按结束时间排序）', 22, T['muted'], bold=True)
    for k, (a, b) in enumerate(ev):
        is_cur = cur == (a, b)
        c = T['yellow'] if is_cur else T['blue']
        cv.rect((sx + (a - 1) * cell + 6, y + k * 31, sx + b * cell - 6, y + k * 31 + 25), fill=c, r=10, alpha=255 if is_cur else 150)
        cv.text((sx + (a - 1) * cell + 14, y + k * 31 + 12), f'[{a},{b}]', 20, T['bg'], anchor='lm', bold=True)


CONFIG = dict(
    num=1353, title='最多可以参加的会议数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='按结束时间排序 + 并查集找空闲天',
    tags=['贪心与思维', '难度分 2016'],
    code='''
class Solution:
    def maxEvents(self, events: List[List[int]]) -> int:
        events.sort(key=lambda e: e[1])

        mx = events[-1][1]
        fa = list(range(mx + 2))

        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        ans = 0
        for start_day, end_day in events:
            x = find(start_day)  # 查找从 start_day 开始的第一个可用天
            if x <= end_day:
                ans += 1
                fa[x] = x + 1  # 标记 x 已占用
        return ans
''',
    call='Solution().maxEvents([[1,2],[2,2],[2,3],[1,1],[1,3]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='fa', pointers={'x': 'pink'}, label='fa（fa[i] 指向 ≥ i 的下一个空闲天；fa[i] = i 表示 i 空闲）', h=150),
        dict(type='calls', h=140),
    ],
    watch=[('start_day', 'start_day', 'blue'), ('end_day', 'end_day', 'blue'), ('x', 'x', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'events.sort': '把会议按==结束时间==从小到大排：临近截止的先安排（和「先复习临考课程」同一个贪心）',
        'mx = events[-1][1]': '最晚的结束日 `mx = {mx}`',
        'fa = list(range(mx + 2))': '`fa[i] = i`：每一天最初都空闲。多开一个位置 `mx + 1` 作为「没有空闲天」的哨兵',
        'def find': '`find(x)`：顺着 `fa` 走到第一个==空闲天==，并做路径压缩',
        'if fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] = {S.fa[S.x]}` ≠ {S.x} → 第 {S.x} 天被占用了，继续往后找' if S.fa[S.x] != S.x else f'`fa[{S.x}] = {S.x}` → 第 {S.x} 天空闲，就是它'),
        'fa[x] = find(fa[x])': '路径压缩：让 `fa[x]` 直接指向找到的空闲天 `{fa[x]}`，下次不用再绕',
        'return fa[x]': '找到空闲天 `{ret}`',
        'x = find(start_day)': '会议 `[{start_day}, {end_day}]` 能用的最早空闲天 `x = {x}`',
        'if x <= end_day': lambda S, B, r: (f'`x = {S.x} ≤ end_day = {S.end_day}` → 这一天还在会议期内，能参加' if S.x <= S.end_day
                                            else f'`x = {S.x} > end_day = {S.end_day}` → 区间内的天全被占满，这场只能放弃'),
        'ans += 1': '参加！`ans` → =={ans}==',
        'fa[x] = x + 1': '第 `{x}` 天被占用：并到 `{x + 1}`，之后 `find` 会跳过它',
        'return ans': '最多参加 `{ret}` 场',
    },
    cards=dict(
        one_liner='结束早的先选，每场会议占区间里最早的空闲天',
        complexity='时间 `O(U + n log n)`，空间 `O(U)`',
        problem=['`events[i] = [start, end]`：会议可以在 `start..end` 内任选一天参加',
                 '一天只能参加一场，求最多能参加几场',
                 '示例：`[[1,2],[2,3],[3,4],[1,2]]` → `4`',
                 '本视频：`[[1,2],[2,2],[2,3],[1,1],[1,3]]` → `3`'],
        quote='优先复习临考（endDay 小）的课程，即按照 endDay 从小到大排序。对于每门课，选择区间中最早的未被占用的那天复习。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['换成「复习课程」：按结束时间排序，每场占区间里==最早的空闲天==',
              '「最早的空闲天」用并查集：占用 `x` 就让 `fa[x] = x + 1`，`find` 顺着走到空闲天',
              '`find` 做路径压缩，每个会议近似 `O(1)`'],
        summary=['时间 `O(U + n log n)`，`U` 是最大结束日；空间 `O(U)`',
                 '`fa` 要开到 `mx + 2`：`x = mx + 1` 表示没有空闲天，必然 `> end_day`',
                 '`find` 是递归，路径压缩前先找到根再回填',
                 '方法一：按开始时间分组 + 最小堆，每天参加结束最早的会议；本视频用方法二']),
)
