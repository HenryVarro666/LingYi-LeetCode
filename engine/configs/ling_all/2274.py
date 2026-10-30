def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    lo, hi, sp = S['bottom'], S['top'], S['special']
    n = hi - lo + 1
    cell = min(96, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    ys = y0 + 110
    ch = cell * 0.9
    cv.text((x0 + 18, y0 + 4), f'楼层 {lo}~{hi}（红 = 特殊楼层，绿 = 当前这段不含特殊楼层的连续楼层）', 22, T['muted'], bold=True)
    spset = set(sp)
    ranges = []
    if 'x' in S and 'y' in S and S['_line'] >= 5:
        ranges = [(S['x'] + 1, S['y'] - 1)]
    elif 'ans' in S and S['_line'] >= 4 and sorted(sp) == list(sp):
        ranges = [(lo, sp[0] - 1), (sp[-1] + 1, hi)]
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
    if 'ans' in S:
        cv.text((x0 + 18, y1 - 50), f"目前最大连续楼层数 ans = {S['ans']}", 28, T['yellow'], bold=True)


CONFIG = dict(
    num=2274, title='不含特殊楼层的最大连续楼层数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='排序 · 统计相邻间隔',
    tags=[],
    code='''
class Solution:
    def maxConsecutive(self, bottom: int, top: int, special: List[int]) -> int:
        special.sort()
        ans = max(special[0] - bottom, top - special[-1])
        for x, y in pairwise(special):
            ans = max(ans, y - x - 1)
        return ans
''',
    call='Solution().maxConsecutive(2, 12, [9, 4, 6])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='special', label='special（排序后从小到大）', cell=90, h=170,
             color=lambda S, i, v: 'red' if S['_line'] >= 5 and v in (S.get('x'), S.get('y')) else None),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"相邻两层特殊楼层 `{S['x']}` 和 `{S['y']}`：中间 `{S['y']} − {S['x']} − 1` = =={S['y'] - S['x'] - 1}== 层" if 'x' in S and S['_line'] == 6
                           else '答案 = 三类间隔的最大值：==最低特殊楼层以下、相邻特殊楼层之间、最高特殊楼层以上==')),
    ],
    watch=[('x', 'x', 'red'), ('y', 'y', 'red'), ('ans', 'ans', 'green')],
    captions={
        'special.sort()': '先排序：`special = {special}`，这样相邻两个就是==相邻的特殊楼层==',
        'ans = max(special[0]': '两端：`special[0] - bottom = {special[0] - bottom}`，`top - special[-1] = {top - special[-1]}` → `ans =` =={ans}==（两端的楼层都能用，不用减 1）',
        'for x, y in pairwise': '取相邻的特殊楼层 `x = {x}`，`y = {y}`',
        'ans = max(ans, y - x - 1)': '`x`、`y` 自己是特殊楼层不能算，中间有 `{y} − {x} − 1 = {y - x - 1}` 层 → `ans = max({B.ans}, {y - x - 1})` = =={ans}==',
        'return ans': '最大连续楼层数 `{ans}`',
    },
    cards=dict(
        one_liner='把特殊楼层排序，答案只可能出现在相邻两个特殊楼层之间或两端',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`bottom` 到 `top` 的楼层都被租下，`special` 里是特殊楼层',
                 '求==不含特殊楼层==的最大连续楼层数',
                 '示例：`bottom=2, top=9, special=[4,6]` → `3`（楼层 7~9）',
                 '本视频：`bottom=2, top=12, special=[9,4,6]` → `3`'],
        quote='核心思路：统计两个特殊楼层间的楼层数。把 special 从小到大排序后，计算如下数字的最大值，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，特殊楼层把大楼切成若干段，每段就是一个候选',
              '相邻两层 `x < y` 之间：`y - x - 1`；最低层以下：`special[0] - bottom`；最高层以上：`top - special[-1]`',
              '用 `pairwise` 遍历相邻对，取最大值'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`（不计排序栈）',
                 '易错：相邻之间要 `- 1`，两端不用减（`bottom`、`top` 本身可用）',
                 '题解另有一行写法：把 `bottom - 1`、`top + 1` 当作哨兵加进去，统一成 `y - x - 1`',
                 '`special` 保证非空且互不相同，所以 `special[0]` 不会越界'],
    ),
)
