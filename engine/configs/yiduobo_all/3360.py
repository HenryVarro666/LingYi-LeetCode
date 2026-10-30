WIN = [(10, 18), (27, 33), (40, 44), (49, 50)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'n 从 1 到 50：绿 = Alice 必胜，灰 = Alice 必输', 24, T['muted'], bold=True)
    cell = (x1 - x0 - 40) / 25
    live = 'n' in S
    for i in range(1, 51):
        r, c = divmod(i - 1, 25)
        X, Y = x0 + 20 + c * cell, y0 + 60 + r * 150
        win = any(a <= i <= b for a, b in WIN)
        fill = T['green'] if win else (70, 76, 86)
        if live and i == S['n']:
            fill = T['yellow']
        cv.rect((X + 1, Y, X + cell - 1, Y + 70), fill=fill, r=4, alpha=255 if win or (live and i == S['n']) else 200)
        cv.text((X + cell / 2, Y + 35), i, 16, T['bg'] if win else T['dim'], anchor='mm', bold=True)


def _txt(S):
    if 'n' not in S:
        return ''
    n = S['n']
    for a, b in WIN:
        if a <= n <= b:
            return f'`n = {n}` 落在 `[{a}, {b}]` → Alice ==必胜=='
    return f'`n = {n}` 不在任何必胜区间 → Alice 输'


CONFIG = dict(
    num=3360, title='移除石头游戏', difficulty='Easy', category='模拟',
    author='yiduobo', technique='手推得到必胜区间', tags=[],
    code='''
class Solution(object):
    def canAliceWin(self, n):
        
        return 10 <= n < 19 or 27 <= n < 34 or 40 <= n < 45 or 49 <= n
''',
    call='Solution().canAliceWin(30)',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_txt, h=80, size=30),
    ],
    watch=['n'],
    captions={
        'return': lambda S, B, r: f'`n = {S.n}`：依次判断四个区间 `[10,19)` `[27,34)` `[40,45)` `[49,50]`，只要落进一个就是 Alice 赢 → `{r}`',
    },
    cards=dict(
        one_liner='n 最大才 50：把 Alice 必胜的区间手推出来',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['Alice 先手拿 10 个，之后每人拿对方上一次 − 1 个，拿不了的人输',
                 '给定石头数 `n`（`1 <= n <= 50`），Alice 能赢吗',
                 '示例：`n=12` → `true`；本视频用 `n=30`'],
        quote='题目给出了明确的移除方案，另外石头的总数n不超过50，那么可以直接暴力计算alice获胜的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['Alice 拿 10 后剩余不足 9 → `n` 在 `[10, 19)`，Alice 赢',
              '再往下：10、9、8 拿完后剩余不足 7 → `n` 在 `[27, 34)`',
              '10、9、8、7、6 拿完剩余不足 5 → `[40, 45)`',
              '10 到 4 拿完剩余不足 3 → `[49, 50]`',
              '四个区间一次判断就是答案'],
        after=[dict(heading='区间怎么来的', lines=[
            'Alice 拿完一手后累计拿走：`10`、`27`、`40`、`49`',
            '轮到 Bob 时下一手要拿：`9`、`7`、`5`、`3`',
            'Bob 拿不了 ⟺ 剩余 < 下一手 ⟺ `n` < 累计 + 下一手',
            '即 `n < 19`、`n < 34`、`n < 45`、`n < 52`（上限 50）',
        ])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：区间左闭右开：`10 <= n < 19`，`n = 19` 时 Bob 还能拿 9 个',
                 '最后一个区间只写 `49 <= n`，因为 n 最大 50',
                 '原文为 Python 2 风格，代码未改，只删去了类型说明文档字符串',
                 '对比灵神：灵神循环模拟，yiduobo 把模拟结果压成常数判断'],
    ),
)
