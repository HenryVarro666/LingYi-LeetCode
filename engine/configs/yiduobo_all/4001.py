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
    if 'i' not in S or 'j' not in S or S['i'] >= len(S['series1']) or S['j'] >= len(S['series2']):
        return ''
    return f"当前两个时间戳：`{S['series1'][S['i']][0]}` 与 `{S['series2'][S['j']][0]}`"


CONFIG = dict(
    num=4001, title='聚合两个时间序列', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='二路归并 · 分三种情况推导',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1506'],
    code='''
class Solution(object):
    def aggregateTimeSeries(self, series1, series2):
        
        i, j = 0, 0
        res = []
        while i < len(series1) and j < len(series2):
            res.append([min(series1[i][0], series2[j][0]), series1[i][1] + series2[j][1]])
            if res[-1][0] == series1[i][0]:
                i += 1
            if res[-1][0] == series2[j][0]:
                j += 1
        
        res.extend(series1[i:])
        res.extend(series2[j:])
        return res
''',
    call='Solution().aggregateTimeSeries([[1,3],[4,1],[6,2]], [[2,2],[4,5]])',
    expect=[[1, 5], [2, 3], [4, 6], [6, 2]],
    views=[
        dict(type='custom', draw=_make_draw([('series1  （上：时间戳，下：值）', 'series1', 'i', 'blue'), ('series2', 'series2', 'j', 'pink'), ('res', 'res', None, 'green')], None), h=420),
        dict(type='text', fn=_cmp),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'i, j = 0, 0': '两个指针从头开始（格子里写 `时间戳:值`）',
        'res = []': '`res` 保存聚合结果',
        'while i <': lambda S, B, r: ('两方都存在，才需要归并' if S.i < len(S.series1) and S.j < len(S.series2) else '只剩一方（或都没了）：剩余部分直接拼接'),
        'res.append([min': '追加 `[较小时间戳, 两值之和]` → `{res[-1]}`：较大一方的「下一个更晚的值」正是它当前这项，所以直接两项相加',
        'if res[-1][0] == series1[i][0]': lambda S, B, r: (f'刚加入的时间戳 `{S.res[-1][0]}` 来自 `series1[{S.i}]` → `i` 后移' if S.res[-1][0] == S.series1[S.i][0] else f'`{S.res[-1][0]}` 不是 `series1` 当前时间戳 `{S.series1[S.i][0]}`，`i` 不动'),
        'if res[-1][0] == series2[j][0]': lambda S, B, r: (f'刚加入的时间戳 `{S.res[-1][0]}` 来自 `series2[{S.j}]` → `j` 后移' if S.res[-1][0] == S.series2[S.j][0] else f'`{S.res[-1][0]}` 不是 `series2` 当前时间戳 `{S.series2[S.j][0]}`，`j` 不动'),
        'i += 1': '`i` → {i}',
        'j += 1': '`j` → {j}',
        'res.extend(series1[i:])': lambda S, B, r: (f'一方已不存在：另一方剩下的 `{S.series1[S.i:]}` 在对面按规则值为 0，直接拼到末尾' if S.series1[S.i:] else '`series1` 没有剩余'),
        'res.extend(series2[j:])': lambda S, B, r: (f'`series2` 剩下的 `{S.series2[S.j:]}` 直接拼到末尾' if S.series2[S.j:] else '`series2` 没有剩余'),
        'return res': '聚合序列 `{ret}`',
    },
    cards=dict(
        one_liner='有序列表合并还是有序列表：二路归并，按三种情况推导',
        complexity='时间 `O(n+m)`，空间 `O(1)`（不计返回值）',
        problem=['两个按时间戳递增的序列，对每个出现过的时间戳把两边的值相加',
                 '某序列缺失该时间戳：取下一个更晚时间戳的值，没有则为 0',
                 '示例：`[[1,3],[4,1]]` 和 `[[2,2],[5,2]]` → `[[1,5],[2,3],[4,3],[5,2]]`'],
        quote='从题目描述上来看，有序列表的合并要求还是有序列表，很容易想到二路归并。',
        quote_src='—— yiduobo 题解原文',
        idea=['只有一方存在：另一方后面没有更大时间戳，值为 0，直接拼接剩余一方',
              '两方时间戳相同：加入时间戳和值之和，两个下标都后移',
              '两方都存在但不同：较大一方取的就是它当前的值，加入较小时间戳和两值之和，只移动较小一方'],
        summary=['时间 `O(n+m)`，空间 `O(1)`（不计返回值）',
                 '用 `min` 取时间戳，再各用一个 `if` 判断谁该移动，相同时两个 `if` 都成立',
                 '原文为 Python 2 风格，本题代码无需改动',
                 '对比灵神：灵神显式写 `<` `>` `=` 三个分支，yiduobo 合并成两个 `if`'],
    ),
)
