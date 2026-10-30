_COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    segs = S['segments']
    mx = max(e for _, e, _ in segs)
    mn = min(s for s, _, _ in segs)
    lo, hi = mn - 1, mx + 1
    W = x1 - x0 - 80
    unit = W / (hi - lo)
    X = lambda v: x0 + 40 + (v - lo) * unit
    cv.text((x0 + 18, y0 + 4), 'segments（半开区间 [start, end)，数字 = color）', 22, T['muted'], bold=True)
    y = y0 + 44
    for j, (s, e, c) in enumerate(segs):
        cv.rect((X(s), y, X(e), y + 36), fill=T[_COLS[j % len(_COLS)]], r=6, alpha=200)
        cv.text(((X(s) + X(e)) / 2, y + 18), c, 22, T['bg'], anchor='mm', bold=True)
        y += 44
    ya = y + 6
    cv.line([(X(lo), ya), (X(hi), ya)], T['border'], 2)
    for v in range(lo + 1, hi):
        cv.line([(X(v), ya - 5), (X(v), ya + 5)], T['border'], 2)
        cv.text((X(v), ya + 10), v, 18, T['dim'], anchor='mt', mono=True)
    # 游标
    pts = S.get('points')
    p = S.get('p')
    cur = None
    if pts is not None and p is not None and p < len(pts):
        cur = pts[p][0]
        cv.dashed((X(cur), y0 + 34), (X(cur), ya + 6), T['yellow'], 4)
        cv.text((X(cur), y0 + 30), f'p={p}', 20, T['yellow'], anchor='mb', bold=True)
    # 排序后的事件点
    yp = ya + 52
    cv.text((x0 + 18, yp - 2), 'points（排序后：位置，+color 开始 / −color 结束）', 22, T['muted'], bold=True)
    if pts is not None:
        n = len(pts)
        cw = min(150, W / n)
        sx = x0 + 40 + (W - cw * n) / 2
        for i, (pos, c) in enumerate(pts):
            on = (p is not None and i == p)
            cv.rect((sx + i * cw + 3, yp + 34, sx + (i + 1) * cw - 3, yp + 34 + 62), fill=T['panel2'],
                    outline=T['yellow'] if on else T['border'], width=4 if on else 1, r=8)
            cv.text((sx + i * cw + cw / 2, yp + 34 + 20), f'x={pos}', 20, T['text'], anchor='mm', bold=True, mono=True)
            cv.text((sx + i * cw + cw / 2, yp + 34 + 44), f'{c:+d}', 22, T['green'] if c > 0 else T['red'], anchor='mm', bold=True, mono=True)
    # 结果
    yr = yp + 120
    cv.text((x0 + 18, yr), 'res（已输出的段，数字 = 颜色和）', 22, T['muted'], bold=True)
    yr += 40
    cv.line([(X(lo), yr + 64), (X(hi), yr + 64)], T['border'], 2)
    for l, r, m in S.get('res', []):
        cv.rect((X(l) + 2, yr, X(r) - 2, yr + 56), fill=T['green'], r=8, alpha=220)
        cv.text(((X(l) + X(r)) / 2, yr + 28), m, 24, T['bg'], anchor='mm', bold=True)
    st, last = S.get('start'), S.get('last')
    if st is not None and last and cur is not None and cur > st:
        cv.rect((X(st) + 2, yr, X(cur) - 2, yr + 56), outline=T['yellow'], width=3, r=8)
        cv.text(((X(st) + X(cur)) / 2, yr + 28), f'? {last}', 22, T['yellow'], anchor='mm', bold=True)
    elif st is not None and last and cur is None and 'now' in S:
        pass
    if 'now' in S:
        cv.text((x1 - 24, yr + 100), f"now = {S['now']}（当前位置的颜色和）  last = {last}", 24, T['cyan'], anchor='ra', bold=True)


CONFIG = dict(
    num=1943, title='描述绘画结果', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分思想 · 只枚举端点并排序',
    tags=['难度分 1969'],
    code='''
class Solution(object):
    def splitPainting(self, segments):

        points = []
        for start, end, color in segments:
            points.append([start, color])
            points.append([end, -color])
        
        points = sorted(points, key=lambda d:d[0])

        now = 0
        last = 0
        start = None
        p = 0
        res = []
        while p < len(points):
            while p + 1 < len(points) and points[p][0] == points[p + 1][0]:
                now += points[p][1]
                p += 1
            
            now += points[p][1]
            if start is not None and last > 0:
                res.append([start, points[p][0], last])
            last = now
            start = points[p][0]
            
            p += 1
        
        if start < points[p - 1][0] and last > 0:
            res.append([start, points[p - 1][0], last])
        return res
''',
    call='Solution().splitPainting([[1,7,9],[6,8,15],[8,10,7]])',
    expect=[[1,6,9],[6,7,24],[7,8,15],[8,10,7]],
    views=[dict(type='custom', draw=_draw, h=700)],
    watch=['p', 'now', 'last', 'start'],
    captions={
        'points = []': '把每个线段拆成两个事件点：起点 `+color`，终点 `−color`（差分的思路）',
        'points.append([start, color])': '起点 `{start}`：此处颜色和 `+{color}`',
        'points.append([end, -color])': '终点 `{end}`：此处颜色和 `−{color}`（半开区间，`end` 处已不含该线段）',
        'points = sorted': '按位置从小到大排序：只需处理这些端点，颜色和只会在端点处变化',
        'now = 0': '`now`：扫到当前端点后，==当前位置的颜色和==',
        'last = 0': '`last`：上一个端点之后那一段的颜色和；`0` 表示那里没有颜色',
        'start = None': '`start`：上一段的起点',
        'while p < len': lambda S, B, r: (f'还有端点：`p = {S.p}`，位置 `{S.points[S.p][0]}`' if S.p < len(S.points) else '端点都处理完了'),
        'while p + 1 < len': lambda S, B, r: (f'`points[{S.p}]` 和 `points[{S.p + 1}]` 同在位置 `{S.points[S.p][0]}` → 先把同位置的合并' if S.p + 1 < len(S.points) and S.points[S.p][0] == S.points[S.p + 1][0] else f'`points[{S.p}]` 位置 `{S.points[S.p][0]}` 与下一个不同，合并结束'),
        'now += points[p][1]': lambda S, B, r: f'把 `points[{S.p}]` 的 `{S.points[S.p][1]:+d}` 加进 `now`：`{B.now}` → =={S.now}==',
        19: '同一位置还有事件，`p` → {p}，继续合并',
        27: '这个位置处理完，`p` → {p}，去看下一个端点',
        'p = 0': '`p`：当前处理的端点下标',
        'for start, end, color': lambda S, B, r: (f'取线段 `[{S.start}, {S.end})`，颜色 `{S.color}`' if (S.start, S.end, S.color) != (B.get('start'), B.get('end'), B.get('color')) else '线段都拆完了'),
        'if start is not None and last > 0': lambda S, B, r: (f'上一段 `[{S.start}, {S.points[S.p][0]})` 颜色和 `last = {S.last} > 0` → ==这一段要输出==' if S.start is not None and S.last > 0 else '还没有上一段，或上一段没有颜色 → 不输出'),
        'res.append([start, points[p][0], last])': '输出一段：`[{res[-1][0]}, {res[-1][1]})`，颜色和 `{res[-1][2]}`',
        'last = now': '新的一段开始，颜色和 `last = now = {last}`',
        'start = points[p][0]': '新一段从 `{start}` 开始',
        'if start < points[p - 1][0]': lambda S, B, r: (f'最后一个端点处没有后续段了，补上最后一段：`start = {S.start} < {S.points[S.p - 1][0]}` 且 `last = {S.last}`' if S.start < S.points[S.p - 1][0] else f'`start = {S.start}` 已经是最后一个端点：没有剩余的段要补，直接返回'),
        'return res': '得到 `{len(res)}` 段：`{res}`',
    },
    skip=['points = []', 'now = 0', 'last = 0', 'start = None', 'res = []'],
    cards=dict(
        one_liner='颜色和只在端点变化：拆成 ±color 事件点，排序后一趟扫',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`segments[i] = [start, end, color]`：半开区间 `[start, end)`，颜色互不相同',
                 '重叠处颜色混合，用颜色和表示；用最少数目的不重叠区间描述整幅画',
                 '示例：`[[1,7,9],[6,8,15],[8,10,7]]` → `[[1,6,9],[6,7,24],[7,8,15],[8,10,7]]`'],
        quote='对于起点start，在差分数组中start的位置加上color；对于终点end，则在end的位置减去color。……对于本题，则可以只枚举线段的起点和终点，因为是有线段的起点和终点会影响到最终的结果。',
        quote_src='—— yiduobo 题解原文',
        idea=['典型差分：起点 `+color`，终点 `−color`；不必存整条差分数组，只存端点',
              '端点按位置排序后一趟扫：先把==同一位置==的事件全部合并到 `now`',
              '遇到新端点时，若上一段颜色和 `last > 0`，就输出 `[start, 当前位置)`，再开始新的一段'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '同一位置的多个事件要先合并，否则会输出长度为 0 的段',
                 '颜色都大于 0，所以 `last > 0` 就表示那一段有颜色（没被涂的空隙不输出）',
                 '样例 3 说明：颜色和相同但来自不同线段也要分段；本解法碰到端点就切段，天然满足',
                 '原文是 Python 2 风格，代码无需改动（没有整数除法、print 等）'],
    ),
)
