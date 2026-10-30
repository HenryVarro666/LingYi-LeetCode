def _make_draw(rows, cmp_fn):
    """rows: [(label, var, ptr_var or None, color_name)]"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        rh = (y1 - y0 - 60) / len(rows)
        for r, (lab, var, ptr, cname) in enumerate(rows):
            data = S.get(var)
            top = y0 + 10 + r * rh
            cv.text((x0 + 18, top), lab, 24, T['muted'], bold=True)
            if data is None:
                continue
            cw = min(110, (x1 - x0 - 60) / max(1, len(data)))
            for k, (t, v) in enumerate(data):
                X = x0 + 30 + k * cw
                cur = ptr is not None and S.get(ptr) == k
                fill = (36, 43, 54)
                cv.rect((X + 3, top + 36, X + cw - 3, top + 36 + 56), fill=fill, outline=T[cname] if cur else None, width=4, r=8)
                cv.text((X + cw / 2, top + 36 + 14), str(t), 24, T[cname] if cur else T['text'], anchor='mm', bold=True)
                cv.text((X + cw / 2, top + 36 + 40), str(v), 22, T['muted'], anchor='mm')
            if ptr is not None and ptr in S and 0 <= S[ptr] < len(data):
                X = x0 + 30 + S[ptr] * cw + cw / 2
                cv.tri_up(X, top + 100, 9, T[cname])
                cv.text((X, top + 112), ptr, 20, T[cname], anchor='mt', bold=True)
            elif ptr is not None and ptr in S:
                cv.text((x0 + 30 + len(data) * cw + 6, top + 56), f'{ptr} = {S[ptr]}（已越界）', 20, T[cname], anchor='lm')
    return draw


def _cmp(S):
    if 't1' not in S or 't2' not in S:
        return ''
    return f"`t1 = {S['t1']}`，`t2 = {S['t2']}`，两边的值之和 `s = {S['s']}`"


CONFIG = dict(
    num=4001, title='聚合两个时间序列', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='归并 · 谁小移谁',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1506'],
    code='''
class Solution:
    def aggregateTimeSeries(self, series1: list[list[int]], series2: list[list[int]]) -> list[list[int]]:
        ans = []
        n, m = len(series1), len(series2)
        i = j = 0

        while i < n and j < m:
            t1, t2 = series1[i][0], series2[j][0]
            s = series1[i][1] + series2[j][1]
            if t1 < t2:
                ans.append([t1, s])
                i += 1
            elif t1 > t2:
                ans.append([t2, s])
                j += 1
            else:  # 相等
                ans.append([t1, s])
                i += 1
                j += 1

        ans += series1[i:]
        ans += series2[j:]
        return ans
''',
    call='Solution().aggregateTimeSeries([[1,3],[4,1],[6,2]], [[2,2],[4,5]])',
    expect=[[1, 5], [2, 3], [4, 6], [6, 2]],
    views=[
        dict(type='custom', draw=_make_draw([('series1  （上：时间戳，下：值）', 'series1', 'i', 'blue'), ('series2', 'series2', 'j', 'pink'), ('ans', 'ans', None, 'green')], None), h=420),
        dict(type='text', fn=_cmp),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s', 's', 'green')],
    captions={
        'ans = []': '聚合结果 `ans`（格子里写 `时间戳:值`）',
        'n, m = ': '`n = {n}`，`m = {m}`',
        'i = j = 0': '两个指针从头开始，像合并两个有序链表',
        'while i < n and j < m': lambda S, B, r: ('两边都还有时间戳，继续归并' if S.i < S.n and S.j < S.m else '有一边用完了：剩下的直接接上'),
        't1, t2 =': '当前两个时间戳：`t1 = {t1}`，`t2 = {t2}`',
        's = series1': '`s = {series1[i][1]} + {series2[j][1]}` = =={s}==：缺失的一边取「下一个更晚时间戳」的值，恰好就是当前指针指向的值',
        'if t1 < t2': lambda S, B, r: (f'`{S.t1} < {S.t2}`：`series2` 在时间 {S.t1} 缺失，取下一个更晚的 {S.t2} 的值 → 时间戳取较小的 {S.t1}'
                                      if S.t1 < S.t2 else f'`{S.t1}` 不小于 `{S.t2}`'),
        'ans.append([t1, s])': lambda S, B, r: f'加入 `[{S.t1}, {S.s}]` → `ans = {S.ans}`',
        'i += 1': '`i` → {i}',
        'elif t1 > t2': lambda S, B, r: (f'`{S.t1} > {S.t2}`：`series1` 在时间 {S.t2} 缺失，取下一个更晚的值 → 时间戳取较小的 {S.t2}'
                                        if S.t1 > S.t2 else f'`{S.t1} = {S.t2}`：时间戳相等'),
        'ans.append([t2, s])': '加入 `[{t2}, {s}]` → `ans = {ans}`',
        'j += 1': '`j` → {j}',
        'ans += series1[i:]': lambda S, B, r: (f'`series2` 已走完，`series1` 剩下的 `{S.series1[S.i:]}` 照搬（另一边按规则是 0）' if S.series1[S.i:] else '`series1` 没有剩余'),
        'ans += series2[j:]': lambda S, B, r: (f'`series1` 已走完，`series2` 剩下的 `{S.series2[S.j:]}` 照搬' if S.series2[S.j:] else '`series2` 没有剩余'),
        'return ans': '聚合序列 `{ret}`',
    },
    cards=dict(
        one_liner='读懂题意后就是归并：时间戳小的先出，两边的值直接相加',
        complexity='时间 `O(n+m)`，空间 `O(1)`（不计返回值）',
        problem=['两个按时间戳严格递增的序列，每项 `[timestamp, value]`',
                 '某序列缺失时间戳：取下一个更晚时间戳的值，没有更晚的就是 0',
                 '示例：`[[1,3],[4,1]]` 和 `[[2,2],[5,2]]` → `[[1,5],[2,3],[4,3],[5,2]]`'],
        quote='思路类似 21. 合并两个有序链表。双指针，谁小就移动谁。难度全在阅读理解',
        quote_src='—— 灵茶山艾府题解',
        idea=['缺失的那一边，「下一个更晚的值」正是它指针当前指向的值，所以 `s` 总是两个指针的值相加',
              '`t1 < t2`：记 `t1` 并移动 `i`；`t1 > t2`：记 `t2` 并移动 `j`；相等一起移动',
              '一边用完后，另一边剩下的值（对面按规则是 0）原样接到答案后面'],
        summary=['时间 `O(n+m)`，空间 `O(1)`（不计返回值）',
                 '难点在读题：缺失取「下一个更晚」的值，没有更晚的才取 0',
                 '循环结束后两个 `+=` 只会有一个非空',
                 '同类题：21 合并两个有序链表、2570 合并两个二维数组'],
    ),
)
