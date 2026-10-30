def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = 8
    cell = min((x1 - x0 - 80) / n, (y1 - y0 - 50) / n, 64)
    ox = x0 + ((x1 - x0) - cell * n) / 2
    oy = y0 + 10
    marks = {}
    for nm, col in (('s', 'blue'), ('t', 'pink')):
        v = S.get(nm)
        if v:
            marks[(ord(v[0]) - 97, int(v[1]) - 1)] = (nm, col)
    for r in range(n):
        for c in range(n):
            black = ((c + 97) + (r + 49)) % 2 == 0   # ASCII 之和为偶 = 黑格
            fill = (70, 74, 90) if black else (205, 208, 216)
            X, Y = ox + c * cell, oy + (n - 1 - r) * cell
            cv.rect((X, Y, X + cell, Y + cell), fill=fill)
            if (c, r) in marks:
                nm, col = marks[(c, r)]
                cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), outline=T[col], width=5, r=8)
                cv.text((X + cell / 2, Y + cell / 2), nm, 30, T[col], anchor='mm', bold=True, mono=True)
    for c in range(n):
        cv.text((ox + c * cell + cell / 2, oy + n * cell + 6), chr(97 + c), 20, T['muted'], anchor='mt', mono=True)
    for r in range(n):
        cv.text((ox - 10, oy + (n - 1 - r) * cell + cell / 2), r + 1, 20, T['muted'], anchor='rm', mono=True)


CONFIG = dict(
    num=3274, title='检查棋盘方格颜色是否相同', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='ASCII 奇偶性',
    tags=[],
    code='''
class Solution:
    def checkTwoChessboards(self, s: str, t: str) -> bool:
        return (ord(s[0]) + ord(s[1])) % 2 == (ord(t[0]) + ord(t[1])) % 2
''',
    call='Solution().checkTwoChessboards("a1", "h3")',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: f"`s = {S['s']}`：`({ord(S['s'][0])} + {ord(S['s'][1])}) % 2 = {(ord(S['s'][0])+ord(S['s'][1]))%2}`；`t = {S['t']}`：`({ord(S['t'][0])} + {ord(S['t'][1])}) % 2 = {(ord(S['t'][0])+ord(S['t'][1]))%2}`" if 's' in S else '', size=26),
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: '棋盘：深色 = 黑格（ASCII 之和为偶），浅色 = 白格；a1 在左下角是黑格', size=24),
    ],
    watch=[('s', 's', 'blue'), ('t', 't', 'pink')],
    captions={
        'return': '`s` 的奇偶 `{(ord(s[0]) + ord(s[1])) % 2}`，`t` 的奇偶 `{(ord(t[0]) + ord(t[1])) % 2}` → 奇偶性{"相同，同色" if (ord(s[0]) + ord(s[1])) % 2 == (ord(t[0]) + ord(t[1])) % 2 else "不同，一黑一白"}，返回 ==`{ret}`==',
    },
    cards=dict(
        one_liner='坐标 ASCII 之和的奇偶性，决定格子颜色',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给两个国际象棋坐标，如 `"a1"`、`"h3"`',
                 '两个格子颜色相同返回 `true`，否则 `false`',
                 '示例：`a1`、`c3` 都是黑格 → `true`'],
        quote='如果 s[0] 和 s[1] 的 ASCII 值的奇偶性相同，那么格子是黑格，否则是白格。',
        quote_src='—— 灵茶山艾府题解',
        idea=['奇+奇=偶，偶+偶=偶，所以 `(s[0] + s[1]) % 2 == 0` 就是黑格',
              '奇+偶=奇，就是白格',
              '两格的 `(ord(x[0]) + ord(x[1])) % 2` 相等，颜色就相同'],
        after=[dict(heading='为什么奇偶性够用', lines=[
            '相邻格子颜色不同 → 横移或竖移一格，ASCII 之和的奇偶就翻转一次',
            'a1：`97 + 49 = 146`，偶数，黑格；b1：`98 + 49 = 147`，奇数，白格',
            '所以只比较两个和的奇偶，不用管具体是哪种颜色']),
               dict(heading='本题示例', lines=[
            '`s = "a1"`：`97 + 49 = 146`，偶数 → 黑格',
            '`t = "h3"`：`104 + 51 = 155`，奇数 → 白格',
            '奇偶不同 → 一黑一白，返回 `false`'])],
        summary=['时间、空间都是 `O(1)`',
                 '直接用 `ord` 的和，不必先把字母换成 1~8',
                 '也可以取异或的最低位，效果一样'],
    ),
)
