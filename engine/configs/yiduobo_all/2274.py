def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    lo, hi, sp = S['bottom'], S['top'], S['sorted_specail'] if 'sorted_specail' in S else S['special']
    n = hi - lo + 1
    cell = min(96, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    ys = y0 + 110
    ch = cell * 0.9
    cv.text((x0 + 18, y0 + 4), f'楼层 {lo}~{hi}（红 = 特殊楼层，绿 = 当前计算的连续楼层）', 22, T['muted'], bold=True)
    spset = set(sp)
    ranges = []
    ss = S.get('sorted_specail')
    if ss:
        if 'index' in S and S['_line'] >= 8:
            ranges = [(ss[S['index'] - 1] + 1, ss[S['index']] - 1)]
        elif 'res' in S and S['_line'] >= 6:
            ranges = [(lo, ss[0] - 1), (ss[-1] + 1, hi)]
    for f in range(lo, hi + 1):
        X = sx + (f - lo) * cell
        inr = any(a <= f <= b for a, b in ranges)
        fill = T['red'] if f in spset else (T['green'] if inr else T['panel2'])
        cv.rect((X + 3, ys, X + cell - 3, ys + ch), fill=fill, r=8, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), f, 30, T['bg'] if fill != T['panel2'] else T['muted'], anchor='mm', bold=True, mono=True)
    for a, b in ranges:
        if a <= b:
            xa, xb = sx + (a - lo) * cell, sx + (b - lo + 1) * cell
            cv.line([(xa + 4, ys + ch + 18), (xb - 4, ys + ch + 18)], T['green'], 4)
            cv.text(((xa + xb) / 2, ys + ch + 28), f'{b - a + 1} 层', 26, T['green'], anchor='mt', bold=True)
    if 'res' in S:
        cv.text((x0 + 18, y1 - 50), f"目前最大连续楼层数 res = {S['res']}", 28, T['yellow'], bold=True)


CONFIG = dict(
    num=2274, title='不含特殊楼层的最大连续楼层数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='排序 · 三种情况分类',
    tags=[],
    code='''
class Solution(object):
    def maxConsecutive(self, bottom, top, special):

        sorted_specail = sorted(special)
        res = max(sorted_specail[0] - bottom, top - sorted_specail[-1])
        for index in range(1, len(sorted_specail)):
            res = max(res, sorted_specail[index] - sorted_specail[index - 1] - 1)

        return res
''',
    call='Solution().maxConsecutive(2, 12, [9, 4, 6])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='sorted_specail', label='sorted_specail（排好序的特殊楼层）', cell=90, h=190,
             pointers={'index': 'blue', 'index - 1': 'pink'},
             color=lambda S, i, v: 'red' if 'index' in S and S['_line'] >= 8 and i in (S['index'], S['index'] - 1) else None),
        dict(type='text', h=70, size=28,
             fn=lambda S: ('三种情况：==底层到最低特殊层==、==最高特殊层到顶层==、==相邻特殊层之间=='
                           if 'index' not in S else f"相邻特殊楼层之间：`{S['sorted_specail'][S['index']]} − {S['sorted_specail'][S['index'] - 1]} − 1` = =={S['sorted_specail'][S['index']] - S['sorted_specail'][S['index'] - 1] - 1}==")),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'sorted_specail = sorted': '先从小到大排序：`{sorted_specail}`，这样首尾和相邻关系一目了然',
        'res = max(sorted_specail[0]': '情况 1、2：`{sorted_specail[0]} − {bottom}` = {sorted_specail[0] - bottom}，`{top} − {sorted_specail[-1]}` = {top - sorted_specail[-1]} → `res` = =={res}==（bottom、top 本身不是特殊楼层，可以算进去）',
        'for index in range': '`index` 从 1 开始，和前一个特殊楼层配对：`index = {index}`',
        'res = max(res, sorted': '情况 3：相邻两个特殊楼层自己都不能算，所以要减 1：`{sorted_specail[index]} − {sorted_specail[index - 1]} − 1 = {sorted_specail[index] - sorted_specail[index - 1] - 1}` → `res = max({B.res}, …)` = =={res}==',
        'return res': '最大连续楼层数 `{res}`',
    },
    cards=dict(
        one_liner='答案必是三种情况之一：底部段、顶部段、相邻特殊楼层之间',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['租下 `bottom` 到 `top` 的所有楼层，`special` 是特殊楼层',
                 '求不含特殊楼层的==最大连续楼层数==',
                 '示例：`bottom=2, top=9, special=[4,6]` → `3`',
                 '本视频：`bottom=2, top=12, special=[9,4,6]` → `3`'],
        quote='首先可以明确的是，最终答案必然属于以下三种情况之一：bottom与最低的特殊楼层之间、top与最高的特殊楼层之间、两个相邻的特殊楼层之间的连续楼层。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排序，再按三种情况各算一个数，取最大',
              '情况 1、2：bottom 和 top ==自身不是特殊楼层==，可以计入，不用减 1',
              '情况 3：相邻两个特殊楼层都不能计入，所以要 `- 1`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`（`sorted` 产生新列表）',
                 '易错：情况 3 比情况 1、2 多减 1 层',
                 '原文变量名 `sorted_specail` 拼写原样保留',
                 '对比灵神：他用 `special.sort()` 原地排序并 `pairwise` 遍历相邻对'],
    ),
)
