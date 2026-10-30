INPUT = [[2, 6], [8, 10], [1, 3], [9, 9], [15, 18]]
LO, HI = 0, 19


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L, R = x0 + 200, x1 - 50

    def X(v):
        return L + (v - LO) / (HI - LO) * (R - L)
    y = y0 + 14
    ivs = S.get('intervals') or []
    idx = S.get('index')
    cv.text((x0 + 18, y), 'intervals' + ('（已按左边界排序）' if 'left' in S else ''), 22, T['muted'], bold=True)
    y += 34
    for k, (a, b) in enumerate(ivs):
        c = T['yellow'] if k == idx and 'interval' in S else T['blue']
        cv.text((x0 + 30, y + 10), f'[{a},{b}]', 20, c, anchor='lm', mono=True)
        cv.rect((X(a), y, max(X(b), X(a) + 8), y + 20), fill=c, r=10)
        y += 30
    y += 14
    cv.text((x0 + 18, y), '基准区间 [left, right]', 22, T['orange'], bold=True)
    y += 34
    if 'right' in S and 'left' in S:
        a, b = S['left'], S['right']
        cv.rect((X(a), y, max(X(b), X(a) + 8), y + 24), fill=T['orange'], r=12)
        cv.text((X(a) - 8, y + 12), str(a), 20, T['orange'], anchor='rm', bold=True)
        cv.text((max(X(b), X(a) + 8) + 8, y + 12), str(b), 20, T['orange'], anchor='lm', bold=True)
        if B.get('right') is not None and B['right'] != b and B.get('left') == a:
            cv.dashed((X(B['right']), y - 6), (X(B['right']), y + 30), T['text'], 2, 6, 5)
    y += 50
    cv.text((x0 + 18, y), 'res', 22, T['green'], bold=True)
    y += 34
    for a, b in S.get('res') or []:
        cv.text((x0 + 30, y + 10), f'[{a},{b}]', 20, T['green'], anchor='lm', mono=True)
        cv.rect((X(a), y, max(X(b), X(a) + 8), y + 20), fill=T['green'], r=10)
        y += 30
    for v in range(LO, HI + 1):
        if v % 2 == 0:
            cv.text((X(v), y1 - 30), str(v), 18, T['dim'], anchor='mt')
            cv.line([(X(v), y1 - 40), (X(v), y1 - 34)], T['dim'], 2)
    cv.line([(L, y1 - 40), (R, y1 - 40)], T['border'], 2)


def _if_cap(S, B, ret):
    a, b = B.interval
    if B.index == 0:
        return '第 0 个区间就是基准区间自己：一定「重叠」，下一行 `max` 后不变'
    if a <= B.right:
        if b <= B.right:
            return f'`{a} ≤ right = {B.right}` 重叠，且右边界 `{b} ≤ {B.right}`：情况 1，==被基准区间包含=='
        return f'`{a} ≤ right = {B.right}` 重叠，右边界 `{b}` 更大：情况 2，==合并=='
    return f'左边界 `{a}` > `right = {B.right}`：不重叠'


CONFIG = dict(
    num=56, title='合并区间', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='排序 + 基准区间',
    code='''
class Solution(object):
    def merge(self, intervals):
        if not intervals:
            return []

        intervals = sorted(intervals, key=lambda d:d[0])

        left = intervals[0][0]
        right = intervals[0][1]
        res = []

        for index, interval in enumerate(intervals):
            if interval[0] <= right:
                right = max(right, interval[1])
            else:
                res.append([left, right])
                left = interval[0]
                right = interval[1]

        res.append([left, right])
        return res
''',
    call=f'Solution().merge({INPUT})',
    expect=[[1, 6], [8, 10], [15, 18]],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('index', 'index', 'yellow'), ('interval', 'interval', 'yellow'), ('left', 'left', 'orange'),
           ('right', 'right', 'orange'), ('res', 'res', 'green')],
    captions={
        'if not intervals': '`intervals` 非空，继续',
        'intervals = sorted': '先把所有区间==按左边界排序==：`{intervals}`',
        'left = intervals[0][0]': '以最左侧的区间为==基准区间==：`left = {left}`',
        'right = intervals[0][1]': '基准区间 `[{left}, {right}]`',
        'res = []': '`res` 存放已经确定的区间',
        'for index, interval': lambda S, B, ret: (f'看第 {S.index} 个区间 `{S.interval}`'
                                                  if 'index' not in B or S.index != B.index else '所有区间都看完了'),
        'if interval[0] <= right': _if_cap,
        'right = max(right, interval[1])': lambda S, B, ret: (
            f'`right = max({B.right}, {S.interval[1]}) = {S.right}` → 基准区间扩成 `[{S.left}, {S.right}]`' if S.right != B.right
            else f'`right = max({B.right}, {S.interval[1]}) = {S.right}`：基准区间不变，相当于==什么都不用做=='),
        '                res.append([left, right])': '基准区间 `[{left}, {right}]` 不会再和后面的区间重叠 → ==加入答案==',
        'left = interval[0]': '当前区间成为新的基准：`left = {left}`',
        'right = interval[1]': '新的基准区间 `[{left}, {right}]`',
        '        res.append([left, right])': '==最后要记得把基准区间也加入答案==：`res` 加入 `[{left}, {right}]`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='排序后拿最左的区间当基准：重叠就合并，不重叠就把基准存进答案、换新基准',
        complexity='时间 `O(n log n)`，空间 `O(n)`（`sorted` 生成新列表）',
        problem=['合并所有==重叠的区间==，返回一个不重叠的区间数组',
                 '示例：`[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`',
                 '演示用 `[[2,6],[8,10],[1,3],[9,9],[15,18]]`'],
        quote='两个区间重叠的条件是，靠右的那个区间的左边界小于等于靠左的那个区间的右边界。于是可以先把所有区间按左边界排序，接下以最左侧的区间为基准区间，往后遍历每个区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['当前区间左边界 ≤ 基准右边界 → 重叠：右边界也 ≤ 就==被包含==，否则==合并==（扩右边界）',
              '左边界 > 基准右边界 → 不重叠：基准区间存进答案，当前区间==成为新基准==',
              '==最后要记得将基准区间也加入到答案中=='],
        summary=['排序 `O(n log n)` + 合并 `O(n)` → 总时间 `O(n log n)`',
                 '循环结束后基准区间还没存，`res.append` 不能漏',
                 '「被包含」和「合并」都用 `right = max(right, interval[1])` 一行处理',
                 '用 `sorted` 生成新列表，不改动输入；循环从第 0 个开始（和基准自己比较一次，无害）',
                 '原文代码可直接在 Python 3 运行，只删去了 docstring'],
    ),
)
