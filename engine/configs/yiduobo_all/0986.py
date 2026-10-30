def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    A, Bl = S['firstList'], S['secondList']
    res = S.get('res', [])
    live = 'i' in S and 'j' in S
    i, j = S.get('i', -1), S.get('j', -1)
    hi = max(max(p[1] for p in A), max(p[1] for p in Bl)) + 1
    L, R = x0 + 130, x1 - 40
    unit = (R - L) / hi

    def X(v):
        return L + v * unit

    cv.text((x0 + 18, y0 + 4), '两个有序区间列表（蓝 = A[i]，粉 = B[j]，黄 = 相交部分，绿 = 已收集）', 22, T['muted'], bold=True)
    rows = [('A', A, i, T['blue']), ('B', Bl, j, T['pink']), ('res', res, -1, T['green'])]
    top = y0 + 60
    rowh = 100
    axis_y = top + rowh * 3 + 8
    for v in range(0, hi + 1):
        cv.line([(X(v), top - 6), (X(v), axis_y)], (36, 42, 52), 1)
        if v % 2 == 0 or hi < 14:
            cv.text((X(v), axis_y + 6), v, 20, T['dim'], anchor='mt', mono=True)
    for r, (name, lst, cur, col) in enumerate(rows):
        y = top + r * rowh
        cv.text((x0 + 70, y + rowh / 2), name, 26, col, anchor='rm', bold=True)
        for k, (a, b) in enumerate(lst):
            done = live and ((name == 'A' and k < i) or (name == 'B' and k < j))
            c = col if (k == cur or name == 'res') else ((60, 66, 76) if done else (92, 100, 112))
            cv.rect((X(a), y + 22, max(X(b), X(a) + 8), y + rowh - 22), fill=c, r=8)
            wide = (X(b) - X(a)) > 90
            if wide:
                cv.text(((X(a) + X(b)) / 2, y + rowh / 2), f'[{a},{b}]', 18, T['bg'] if c == col else T['text'],
                        anchor='mm', bold=True, mono=True)
            else:
                cv.text(((X(a) + max(X(b), X(a) + 8)) / 2, y + rowh - 20), f'[{a},{b}]', 16, col if c == col else T['text'],
                        anchor='mt', bold=True, mono=True)
    if live and i < len(A) and j < len(Bl):
        a1, b1 = A[i]
        a2, b2 = Bl[j]
        lo, up = max(a1, a2), min(b1, b2)
        cv.text((x0 + 18, axis_y + 44), f'max_x = max({a1}, {a2}) = {lo}，min_y = min({b1}, {b2}) = {up}', 24, T['text'], anchor='lm', bold=True)
        if lo <= up:
            cv.rect((X(lo) - 2, top, max(X(up), X(lo) + 4) + 2, top + rowh * 2), fill=T['yellow'], alpha=70)
            cv.text((x0 + 18, axis_y + 80), f'{lo} <= {up} → 相交，区间 [{lo}, {up}]', 24, T['yellow'], anchor='lm', bold=True)
        else:
            cv.text((x0 + 18, axis_y + 80), f'{lo} > {up} → 不相交', 24, T['red'], anchor='lm', bold=True)


CONFIG = dict(
    num=986, title='区间列表的交集', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='双指针 · 类似二路归并',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def intervalIntersection(self, firstList, secondList):

        i = j = 0
        m = len(firstList)
        n = len(secondList)

        res = []
        while i < m and j < n:
            x1, y1 = firstList[i]
            x2, y2 = secondList[j]
            if max(x1, x2) <= min(y1, y2):
                res.append([max(x1, x2), min(y1, y2)])
            
            if y1 < y2:
                i += 1
            elif y1 > y2:
                j += 1
            else:
                i += 1
                j += 1
        
        return res
''',
    call='Solution().intervalIntersection([[0,2],[5,10],[13,23]], [[1,5],[8,12],[15,24]])',
    expect=[[1, 2], [5, 5], [8, 10], [15, 23]],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: f"res = `{S['res']}`" if 'res' in S else '', size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('y1', 'y1', 'blue'), ('y2', 'y2', 'pink')],
    skip=['m = len', 'n = len'],
    captions={
        'i = j = 0': '`i` 指向 A 的当前区间，`j` 指向 B 的当前区间，像二路归并',
        'res = []': '`res` 收集所有相交区间',
        'while i < m': lambda S, B, r: (f"`i = {S.i} < {S.m}` 且 `j = {S.j} < {S.n}` → 两边都还有区间，继续" if S.i < S.m and S.j < S.n else f"有一边用完了（`i = {S.i}`，`j = {S.j}`）→ 后面不可能再相交，结束"),
        'x1, y1 = ': '取 A 的第 `{i}` 个区间 `[{x1}, {y1}]`',
        'x2, y2 = ': '取 B 的第 `{j}` 个区间 `[{x2}, {y2}]`',
        'if max(x1, x2)': lambda S, B, r: (f"`max_x = {max(S.x1, S.x2)}`，`min_y = {min(S.y1, S.y2)}`：{max(S.x1, S.x2)} <= {min(S.y1, S.y2)} → ==相交=="
                                         if max(S.x1, S.x2) <= min(S.y1, S.y2) else f"`max_x = {max(S.x1, S.x2)}` > `min_y = {min(S.y1, S.y2)}` → 不相交"),
        'res.append': '相交部分就是 `[max_x, min_y]` = `{res[-1]}`，加入 `res`',
        'if y1 < y2': lambda S, B, r: (f"`y1 = {S.y1} < y2 = {S.y2}`：A 的这个区间先结束，B 后面的区间都在 {S.y2} 之后 → ==i 右移==" if S.y1 < S.y2 else f"`y1 = {S.y1}` 不比 `y2 = {S.y2}` 小，再看是否更大"),
        'elif y1 > y2': lambda S, B, r: (f"`y1 = {S.y1} > y2 = {S.y2}`：B 的这个区间先结束，A 后面的区间都在 {S.y1} 之后 → ==j 右移==" if S.y1 > S.y2 else f"`y1 = y2 = {S.y1}`：两个区间同时结束"),
        'i += 1': '`i` → {i}：A 这个区间用完了',
        'j += 1': '`j` → {j}：B 这个区间用完了',
        'return res': '所有相交区间都找到了：`{res}`',
    },
    cards=dict(
        one_liner='区间的交 = [max(左端点), min(右端点)]，右端点小的先出局',
        complexity='时间 `O(m+n)`，空间 `O(1)`（不计结果）',
        problem=['两个各自有序、互不相交的区间列表 `firstList`、`secondList`',
                 '返回它们所有的交集区间（闭区间）',
                 '本视频：`[[0,2],[5,10],[13,23]]` 与 `[[1,5],[8,12],[15,24]]`'],
        quote='设max_x = max(x1, y2)，那么只有当max_x <= min_y时会产生相交，区间恰好就是[max_x， min_y]',
        quote_src='—— yiduobo 题解原文（原文笔误 y2，应为 x2）',
        idea=['先分情况讨论，归纳出：相交 ⇔ `max_x <= min_y`',
              '区间已排序：右端点小的那个，后面再也碰不到对方的后续区间',
              '所以像二路归并：每轮先求交，再让右端点小的指针前进'],
        summary=['时间 `O(m+n)`，空间 `O(1)`（结果除外）',
                 '右端点相等时 `i`、`j` 要一起前进',
                 '闭区间：`max_x == min_y` 也算相交（单点）',
                 '原文为 Python 2 风格（`class Solution(object)`），无需修改即可运行'],
    ),
)
