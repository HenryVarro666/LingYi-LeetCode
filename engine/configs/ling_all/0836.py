R1 = [0, 0, 3, 2]
R2 = [1, 2, 4, 4]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    r1, r2 = S.get('rec1', R1), S.get('rec2', R2)
    which = None
    if 'l1' in S:
        if (S['l1'], S['r1'], S['l2'], S['r2']) == (r1[0], r1[2], r2[0], r2[2]):
            which = 'x'
        elif (S['l1'], S['r1'], S['l2'], S['r2']) == (r1[1], r1[3], r2[1], r2[3]):
            which = 'y'
    ox, oy = x0 + 150, y1 - 120
    u = min((x1 - x0 - 260) / 5, (y1 - y0 - 200) / 5)
    P = lambda x, y: (ox + x * u, oy - y * u)
    cv.text((x0 + 18, y0 + 4), '两个矩形（蓝 = rec1，粉 = rec2），横轴/纵轴各压成线段比较', 22, T['muted'], bold=True)
    for k in range(6):
        cv.line([P(k, 0), P(k, 5)], T['border'], 1)
        cv.line([P(0, k), P(5, k)], T['border'], 1)
        cv.text((P(k, 0)[0], oy + 8), k, 18, T['dim'], anchor='mt', mono=True)
        cv.text((ox - 10, P(0, k)[1]), k, 18, T['dim'], anchor='rm', mono=True)
    for r, c in ((r1, T['blue']), (r2, T['pink'])):
        a, b = P(r[0], r[3]), P(r[2], r[1])
        cv.rect((a[0], a[1], b[0], b[1]), fill=c, alpha=70, outline=c, width=4)
    # x 方向线段
    for (r, c, dy) in ((r1, T['blue'], 40), (r2, T['pink'], 62)):
        hot = which == 'x'
        cv.line([(P(r[0], 0)[0], oy + dy), (P(r[2], 0)[0], oy + dy)], c, 9 if hot else 4)
    for (r, c, dx) in ((r1, T['blue'], 40), (r2, T['pink'], 62)):
        hot = which == 'y'
        cv.line([(ox - dx, P(0, r[1])[1]), (ox - dx, P(0, r[3])[1])], c, 9 if hot else 4)
    if which:
        i = 0 if which == 'x' else 1
        lo, hi = max(r1[i], r2[i]), min(r1[i + 2], r2[i + 2])
        col = T['green'] if lo < hi else T['red']
        if which == 'x':
            cv.line([(P(lo, 0)[0], oy + 84), (P(hi, 0)[0], oy + 84)], col, 9)
            cv.text((P(5, 0)[0] + 20, oy + 84), f'x 交集 [{lo}, {hi}]' + (' 长度>0' if lo < hi else ' 长度≤0'), 22, col, anchor='lm', bold=True)
        else:
            cv.line([(ox - 84, P(0, lo)[1]), (ox - 84, P(0, hi)[1])], col, 9)
            cv.text((ox + 5 * u + 20, P(0, hi)[1]), f'y 交集 [{lo}, {hi}]' + (' 长度>0' if lo < hi else ' 长度≤0'), 22, col, anchor='lm', bold=True)


CONFIG = dict(
    num=836, title='矩形重叠', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='压扁成区间 · 严格相交',
    tags=['灵神题单', '数学算法', '难度分 1443'],
    code='''
class Solution:
    # 判断闭区间 [l1, r1] 和 [l2, r2] 是否严格相交
    def isIntervalOverlap(self, l1: int, r1: int, l2: int, r2: int) -> bool:
        return r1 > l2 and r2 > l1

    def isRectangleOverlap(self, rec1: list[int], rec2: list[int]) -> bool:
        return self.isIntervalOverlap(rec1[0], rec1[2], rec2[0], rec2[2]) and \\
               self.isIntervalOverlap(rec1[1], rec1[3], rec2[1], rec2[3])
''',
    call='sol = Solution()\n[sol.isRectangleOverlap([0,0,3,2], [1,2,4,4]), sol.isRectangleOverlap([0,0,3,2], [1,1,4,4])]',
    expect=[False, True],
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', fn=lambda S: (f"区间 [{S['l1']}, {S['r1']}] 与 [{S['l2']}, {S['r2']}]：`{S['r1']} > {S['l2']}` 且 `{S['r2']} > {S['l1']}` → =={S['r1'] > S['l2'] and S['r2'] > S['l1']}==") if 'l1' in S else '', h=70),
    ],
    watch=['l1', 'r1', 'l2', 'r2'],
    captions={
        'return r1 > l2': '不相交只有两种：一个的右端点 `<=` 另一个的左端点。都不是就严格相交：`{r1} > {l2}` 且 `{r2} > {l1}` → =={ret}==',
        'return self.isIntervalOverlap(rec1[0]': lambda S, B, ret: ('先把两个矩形压到横轴，比较 x 方向的区间' if ret is None else f'两个方向的判断做完，矩形是否重叠：=={ret}=='),
        'self.isIntervalOverlap(rec1[1]': 'x 方向相交了，再把它们压到纵轴，比较 y 方向的区间',
    },
    cards=dict(
        one_liner='交集也是矩形：横、纵两个方向的区间都严格相交才算重叠',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['矩形 `[x1, y1, x2, y2]`：左下角和右上角，边与坐标轴平行',
                 '相交面积为 ==正== 才算重叠，只在角或边接触不算',
                 '示例：`[0,0,1,1]` 与 `[1,0,2,1]` → `false`'],
        quote='如果面积为正，意味着交集矩形的长大于 0，宽也大于 0。只看横坐标，问题变成一个一维问题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['交集矩形的长只和横坐标有关，宽只和纵坐标有关',
              '把矩形压扁成闭区间，判断两个区间是否严格相交',
              '一个区间的右端点 `<=` 另一个的左端点就不相交，否则相交'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：==边或角接触不算重叠==，所以比较用 `>` 而不是 `>=`',
                 '写法一：`max(l1, l2) < min(r1, r2)`，本视频用的是等价的写法二',
                 '同样的「压成一维」思路可用于求相交面积'],
    ),
)
