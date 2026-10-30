SQ = [[0, 0, 2], [1, 1, 1], [3, 3, 1]]
TOT = sum(l * l for _, _, l in SQ)


def _plane(box):
    x0, y0, x1, y1 = box
    s = min((x1 - x0 - 140) / 4.6, (y1 - y0 - 120) / 4.4)
    ox, oy = x0 + 70, y1 - 50
    return s, ox, oy


def _draw(cv, S, B, box, T):
    s, ox, oy = _plane(box)
    line = S.get('_line')
    live = 'below' in S and 'pre_y' in S
    pre = S.get('pre_y') if live else None
    nxt = S.get('y') if live and 'now' in S and line in (16, 17, 18) else None
    cv.text((box[0] + 18, box[1] + 4), '正方形（绿 = 已扫过的面积 below，黄带 = 这一步扫过的 now，橙线 = 扫描线 pre_y）', 22, T['muted'], bold=True)
    cv.line([(ox - 10, oy), (ox + 4.4 * s, oy)], T['border'], 2)
    for t in range(5):
        cv.text((ox - 18, oy - t * s), t, 20, T['dim'], anchor='rm', mono=True)
    for (x, y, l) in SQ:
        X0, X1 = ox + x * s, ox + (x + l) * s
        cv.rect((X0, oy - (y + l) * s, X1, oy - y * s), fill=T['panel2'], outline=T['border'], width=3)
        if pre is not None and pre > y:
            top = min(pre, y + l)
            cv.rect((X0 + 2, oy - top * s, X1 - 2, oy - y * s - 2), fill=T['green'], alpha=120)
        if nxt is not None and S['tot_l'] > 0:
            lo, hi = max(pre, y), min(nxt, y + l)
            if hi > lo:
                cv.rect((X0 + 2, oy - hi * s, X1 - 2, oy - lo * s), fill=T['yellow'], alpha=140)
        cv.text((X0 + 6, oy - (y + l) * s + 4), f'l={l}', 20, T['text'], anchor='la', bold=True)
    if pre is not None:
        cv.line([(ox - 10, oy - pre * s), (ox + 4.4 * s, oy - pre * s)], T['orange'], 4)
        cv.text((ox + 4.4 * s + 8, oy - pre * s), f'pre_y={pre}', 22, T['orange'], anchor='lm', bold=True)
    if nxt is not None:
        cv.line([(ox - 10, oy - nxt * s), (ox + 4.4 * s, oy - nxt * s)], T['yellow'], 3)
        cv.text((ox + 4.4 * s + 8, oy - nxt * s - 4), f'y={nxt}', 22, T['yellow'], anchor='lm', bold=True)
    if line == 18 and 'now' in S and (S['below'] + S['now']) * 2 >= S['s']:
        ay = S['pre_y'] + (S['s'] / 2.0 - S['below']) / S['tot_l']
        cv.line([(ox - 10, oy - ay * s), (ox + 4.4 * s, oy - ay * s)], T['pink'], 5)
        cv.text((ox + 4.4 * s + 150, oy - ay * s - 14), f'答案 {ay:.4f}', 22, T['pink'], anchor='lm', bold=True)


def _top(S):
    if 'below' not in S:
        return '想象一条水平扫描线从下往上走，线下面积到总面积 `s` 的一半时，就是答案'
    if 'now' in S and S.get('_line') in (16, 17, 18):
        return f'扫描线 `{S["pre_y"]}` → `{S["y"]}`：生效边长 `tot_l = {S["tot_l"]}`，扫过 `now = {S["now"]}`；已有 `below = {S["below"]}`，一半是 `{S["s"] / 2}`'
    return f'扫描线在 `{S["pre_y"]}`，生效边长 `tot_l = {S["tot_l"]}`，线下面积 `below = {S["below"]}`'


def _half(S, B, ret):
    t = S.below + S.now
    ok = t * 2 >= S.s
    return (f'`below + now = {t}`，×2 = `{t * 2}` {">=" if ok else "<"} `s = {S.s}`：' +
            ('这一段扫过去就越过一半 → 答案在 `pre_y` 与 `y` 之间' if ok else '还没过一半，继续往上'))


CONFIG = dict(
    num=3453, title='分割正方形 I', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='扫描线 · 事件排序 + 线性插值',
    tags=['灵神题单·二分算法', '灵神题单·常用数据结构', '难度分 1735'],
    code='''
class Solution(object):
    def separateSquares(self, squares):
        
        s = 0
        points = []
        for x, y, l in squares:
            points.append((y, l))
            points.append((y + l, -l))
            s += l * l
        
        points.sort()
        below = 0
        pre_y = points[0][0]
        tot_l = points[0][1]
        for y, l in points[1:]:
            now = (y - pre_y) * tot_l
            if (below + now) * 2 >= s:
                return pre_y + (s / 2.0 - below) / tot_l
            
            tot_l += l
            pre_y = y
            below += now
''',
    call=f'Solution().separateSquares({SQ})',
    expect=1 + (TOT / 2.0 - 2) / 3,
    views=[
        dict(type='text', fn=_top, size=24, h=100),
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: f"事件点 `points = {S['points']}`" if 'points' in S and S.get('_line', 0) >= 11 else '', size=22, h=70),
    ],
    watch=[('s', 's', 'cyan'), ('pre_y', 'pre_y', 'orange'), ('y', 'y', 'yellow'), ('tot_l', 'tot_l', 'pink'), ('now', 'now', 'green'), ('below', 'below', 'blue')],
    captions={
        's = 0': '`s` 累计所有正方形的面积（重叠算多次）',
        'points = []': '`points` 存扫描线会停下的事件：(高度, 边长变化)',
        'for x, y, l in squares': lambda S, B, r: (f'`s = {S.s}`，事件收集完毕' if B.get('y') == S.y and B.get('l') == S.l and 'l' in B
                                                   else f'正方形 `y = {S.y}`，边长 `l = {S.l}`'),
        'points.append((y, l))': '下边在 `y = {y}`：扫描线越过它，生效边长 `+{l}`',
        'points.append((y + l, -l))': '上边在 `y + l = {y + l}`：越过它，生效边长 `-{l}`',
        's += l * l': '面积累加：`s = {s}`',
        'points.sort()': '事件按高度排序：`points = {points}`，扫描线就在这些高度之间停靠',
        'below = 0': '`below` 记扫描线下方已累计的面积',
        'pre_y = points[0][0]': '扫描线从最低的事件 `pre_y = {pre_y}` 出发',
        'tot_l = points[0][1]': '`tot_l` = 当前生效的正方形边长之和，初始是第一个事件的 `{tot_l}`',
        'for y, l in points[1:]': lambda S, B, r: (f'下一个事件：`y = {S.y}`，边长变化 `l = {S.l}`' if not (B.get('y') == S.y and B.get('l') == S.l and 'now' in B) else '事件都处理完了'),
        'now = (y - pre_y) * tot_l': '扫描线从 `{pre_y}` 抬到 `{y}`，扫过的面积 `now = ({y} − {pre_y}) × {tot_l} = {now}`',
        'if (below + now) * 2 >= s': _half,
        'return pre_y +': lambda S, B, r: f'还差 `s/2 − below = {S.s / 2.0 - S.below}`，除以生效边长 `{S.tot_l}`，从 `pre_y = {S.pre_y}` 往上走这么多 → 答案 ==`{r:.5f}`==',
        'tot_l += l': '越过 `y = {y}`：生效边长变化 `{l:+d}` → `tot_l = {tot_l}`',
        'pre_y = y': '扫描线停到 `pre_y = {pre_y}`',
        'below += now': '把这一段面积记入线下：`below = {below}`',
    },
    cards=dict(
        one_liner='水平扫描线从下往上扫，线下面积一过一半就按比例回推',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`squares[i] = [x, y, l]` 是与坐标轴平行的正方形，重叠部分面积重复计算',
                 '求最小的水平线 `y`，使它上方与下方正方形总面积相等；误差 `1e-5` 内算对',
                 f'本视频：`squares = {SQ}` → `1.33333`'],
        quote='不妨想象有一条水平的扫码线从下往上移动，那么随着这条线的移动，线下方的面积会越来越大。当某一时刻这条线下方的面积等于总面积的一半时，这条线对应的y就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据太大不能连续扫，只在每个正方形的 `y` 和 `y + l` 处停：收集 `(y, +l)`、`(y+l, -l)` 两种事件并排序',
              '两个事件之间生效边长 `tot_l` 不变，扫过面积 = 高度差 × `tot_l`，类似差分数组',
              '一旦 `below + now` 过半，答案在这一段里：`pre_y + (s/2 − below) / tot_l`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '答案不一定在某个事件高度上，要在最后一段里线性插值',
                 '同一高度可能既有上边又有下边：排序时 `(y, l)` 一起比较，边长为负的先处理',
                 '原文已是 Python 3 也能运行的写法（`s / 2.0` 本来就是浮点除法），无需改动',
                 '对比灵神：灵神用 `defaultdict` 差分后 `pairwise` 扫描；这里直接排事件点'],
    ),
)
