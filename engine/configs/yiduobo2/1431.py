CANDIES, EXTRA = [4, 2, 1, 1, 2], 1


def _draw(cv, S, B, box, T):
    """柱子 = 原有糖果，上面叠一段 extraCandies（黄）；能顶到 now_max 虚线就是 true"""
    x0, y0, x1, y1 = box
    c = CANDIES
    mx = S.get('now_max')
    done = S.get('_line') == 4
    cv.text((x0 + 18, y0 + 4), '每个孩子：原有糖果（蓝）+ 全部额外糖果（黄）', 24, T['muted'], bold=True)
    n = len(c)
    slot = (x1 - x0 - 240) / n
    base = y1 - 120
    top = y0 + 70
    unit = (base - top) / (max(c) + EXTRA + 1)
    sx = x0 + 190
    if mx is not None:
        ym = base - mx * unit
        cv.dashed((sx - 20, ym), (x1 - 30, ym), T['orange'], 3)
        cv.text((sx - 28, ym), f'now_max = {mx}', 22, T['orange'], anchor='rm', bold=True)
    for i, v in enumerate(c):
        X = sx + i * slot + slot * 0.2
        W = slot * 0.6
        cv.rect((X, base - v * unit, X + W, base), fill=T['blue'], r=6)
        cv.text((X + W / 2, base - v * unit / 2), v, 24, T['bg'], anchor='mm', bold=True)
        if mx is not None:
            cv.rect((X, base - (v + EXTRA) * unit, X + W, base - v * unit), fill=T['yellow'], alpha=210, r=6)
            cv.text((X + W / 2, base - (v + EXTRA) * unit - 6), f'{v}+{EXTRA}={v + EXTRA}', 22,
                    T['green'] if done and v + EXTRA >= mx else T['text'], anchor='mb', bold=True)
        cv.text((X + W / 2, base + 8), f'孩子 {i}', 20, T['dim'], anchor='mt')
        if done:
            ok = v + EXTRA >= mx
            cv.text((X + W / 2, base + 40), 'true' if ok else 'false', 24, T['green'] if ok else T['red'], anchor='mt', bold=True)
    cv.line([(sx - 20, base), (x1 - 30, base)], T['border'], 2)


CONFIG = dict(
    num=1431, title='拥有最多糖果的孩子', difficulty='Easy', category='普通数组',
    author='yiduobo', technique='两趟遍历：先找最大值，再逐个比较',
    tags=['字节30天'],
    code='''
class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        now_max = max(candies)
        return [candy + extraCandies >= now_max for candy in candies]
''',
    call=f'Solution().kidsWithCandies({CANDIES}, {EXTRA})',
    expect=[True, False, False, False, False],
    views=[
        dict(type='custom', h=520, draw=_draw),
        dict(type='text', h=60, size=26,
             fn=lambda S: ('第二趟：`candy + extraCandies >= now_max`' if S.get('_line') == 4
                           else (f"第一趟：`now_max = max(candies) = {S['now_max']}`" if 'now_max' in S else ''))),
    ],
    watch=[('extraCandies', 'extraCandies', 'yellow'), ('now_max', 'now_max', 'orange')],
    captions={
        'now_max = max(candies)': '第一趟遍历：初始状态下最多的孩子有 `now_max = {now_max}` 个糖果',
        'return [candy + extraCandies': lambda S, B, ret: (f'第二趟遍历：每个孩子加上 `{EXTRA}` 个额外糖果，'
                                                           f'和 `now_max` 比较 → `{ret}`'),
    },
    cards=dict(
        one_liner='先找出原来最多的糖果数，再看谁加上额外糖果能追上它',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['`candies[i]` 是第 `i` 个孩子的糖果数，另有 `extraCandies` 个额外糖果',
                 '把额外糖果==全部==给第 `i` 个孩子后，他是不是拥有最多糖果的（可以并列）？',
                 '示例：`candies = [4,2,1,1,2], extraCandies = 1` → `[true,false,false,false,false]`'],
        quote='比较基础的题目。首先==一趟遍历找出初始状态下糖果数最多的孩子拥有的糖果数==，记为now_max。接下来再一趟遍历，考察当前孩子加上额外糖果之后拥有的糖果数目与now_max的大小即可。',
        quote_src='—— yiduobo 题解',
        idea=['第一趟：`now_max = max(candies)`',
              '第二趟：`candy + extraCandies >= now_max` 就是 true',
              '只有 1 个额外糖果时，只有原本最多的孩子能保持最多'],
        result='只有孩子 0 加完能达到 `now_max = 4`：`[true,false,false,false,false]` ✓',
        before=[dict(heading='题意拆解', lines=[
            '额外糖果只给一个孩子，其余孩子的糖果数不变',
            '「拥有最多」= 不少于所有其他孩子，==并列也算==',
            '所以只要和初始的最大值比较就够了'])],
        summary=['时间 `O(n)`：两趟遍历',
                 '比较要用 `>=`：追平最大值也算最多',
                 '对比灵神：灵神把不等式移项成 `candies[i] >= mx - extraCandies`，思路相同',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
