def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, L, R = S['n'], list(S['left']), list(S['right'])
    cv.text((x0 + 18, y0 + 4), '木板 0 ~ n（蓝 = 向左走的蚂蚁，粉 = 向右走的蚂蚁；相遇掉头 = 穿过去）', 22, T['muted'], bold=True)
    cell = min(100, (x1 - x0 - 80) / (n + 1))
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    yb = y0 + 230
    cv.rect((sx - 14, yb - 8, sx + n * cell + 14, yb + 8), fill=T['panel'], outline=T['border'], width=2, r=8)
    for i in range(n + 1):
        X = sx + i * cell
        cv.line([(X, yb - 14), (X, yb + 14)], T['border'], 2)
        cv.text((X, yb + 24), i, 22, T['dim'], anchor='mt', mono=True)
    cv.text((sx, yb + 64), '0 端（向左的蚂蚁从这里掉）', 20, T['blue'], anchor='lt', bold=True)
    cv.text((sx + n * cell, yb + 64), f'n = {n} 端（向右的从这里掉）', 20, T['pink'], anchor='rt', bold=True)
    for p in L:
        X = sx + p * cell
        cv.arrow((X, yb - 44), (X - cell * 0.6, yb - 44), T['blue'], 5, 14)
        cv.rect((X - 6, yb - 40, X + 6, yb - 20), fill=T['blue'], r=5)
        cv.text((X, yb - 96), f'左·{p}', 22, T['blue'], anchor='mb', bold=True)
    for p in R:
        X = sx + p * cell
        cv.arrow((X, yb - 44), (X + cell * 0.6, yb - 44), T['pink'], 5, 14)
        cv.rect((X - 6, yb - 40, X + 6, yb - 20), fill=T['pink'], r=5)
        cv.text((X, yb - 96), f'右·{p}', 22, T['pink'], anchor='mb', bold=True)
    if 'l' in S and L:
        X = sx + S['l'] * cell
        cv.line([(sx, yb + 110), (X, yb + 110)], T['blue'], 6)
        cv.text(((sx + X) / 2, yb + 122), f"向左最远的蚂蚁走 l = {S['l']}", 22, T['blue'], anchor='mt', bold=True)
    if 'r' in S and R:
        X = sx + min(R) * cell
        cv.line([(X, yb + 170), (sx + n * cell, yb + 170)], T['pink'], 6)
        cv.text(((X + sx + n * cell) / 2, yb + 182), f"向右最远的蚂蚁走 r = n − {min(R)} = {S['r']}", 22, T['pink'], anchor='mt', bold=True)


CONFIG = dict(
    num=1503, title='所有蚂蚁掉下来前的最后一刻', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='相遇当作穿过 · 只看最远的蚂蚁',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def getLastMoment(self, n, left, right):

        if len(left) == 0:
            l = 0
        else:
            l = max(left)
        
        if len(right) == 0:
            r = 0
        else:
            r = n - min(right)
        
        return max(l, r)
''',
    call='Solution().getLastMoment(9, [2, 5], [6, 7])',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=lambda S: (f"最后一只掉下去的时刻 = max(`{S['l']}`, `{S['r']}`) = =={max(S['l'], S['r'])}==" if 'r' in S and 'l' in S else ''), size=28, h=60),
    ],
    watch=[('n', 'n'), ('l', lambda S: S.get('l'), 'blue'), ('r', lambda S: S.get('r'), 'pink')],
    captions={
        'if len(left) == 0': '`left` 里有 {len(left)} 只向左走的蚂蚁，非空 → 走 else，取最远的那只',
        'if len(right) == 0': '`right` 里有 {len(right)} 只向右走的蚂蚁，非空 → 走 else',
        'l = max(left)': '相遇掉头 ≈ 各走各的：向左的蚂蚁到 0 端要走 `位置` 步，最慢的是 `max(left)` = =={l}==',
        'r = n - min(right)': '向右的蚂蚁到 n 端要走 `n - 位置` 步，位置最小的最慢：`{n} - {min(right)}` = =={r}==',
        'return max': '所有蚂蚁都掉下去的时刻 = 最慢的那只：`max({l}, {r})` = =={ret}==',
    },
    cards=dict(
        one_liner='相遇掉头等于穿过彼此：只看最慢的那一只',
        complexity='时间 `O(n)`（扫一遍两个数组），空间 `O(1)`',
        problem=['长为 `n` 的木板，蚂蚁每秒走 1 个单位，`left` 里的向左走，`right` 里的向右走',
                 '两只蚂蚁相遇就各自反向，掉下木板的蚂蚁消失',
                 '返回最后一只蚂蚁掉下来的时刻',
                 '本视频：`n=9, left=[2,5], right=[6,7]` → `5`'],
        quote='两只蚂蚁相遇时……也可以认为是两只蚂蚁各走各的互不影响，那么这里就只需要统计向右走的蚂蚁距离n的最远距离，以及向左走的蚂蚁距离0的最远距离',
        quote_src='—— yiduobo 题解原文',
        idea=['相遇掉头：两只蚂蚁互换了方向，==整体看和穿过去一样==',
              '于是每只蚂蚁互不影响，各自直走到端点',
              '向左的看 `max(left)`，向右的看 `n - min(right)`，取较大者'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：某个方向没有蚂蚁时（空数组）不能直接 `max([])`，所以要单独判断并取 `0`',
                 '向右的蚂蚁离 n 端最远的是==位置最小==的那只，不是最大的',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
