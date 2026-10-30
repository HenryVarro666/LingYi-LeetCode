

def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = 8
    cell = min((x1 - x0 - 80) / n, (y1 - y0 - 50) / n, 64)
    ox = x0 + ((x1 - x0) - cell * n) / 2
    oy = y0 + 10
    marks = {}
    for nm, col, xk, yk in (('1', 'blue', 'x1', 'y1'), ('2', 'pink', 'x2', 'y2')):
        if xk in S and yk in S:
            marks[(S[xk] - 1, S[yk] - 1)] = (nm, col)
    for r in range(n):
        for c in range(n):
            black = (c + 1 + r + 1) % 2 == 0   # 行列坐标之和为偶 = 黑格
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


def _txt(S):
    if 'x1' not in S:
        return ''
    if 'y2' not in S:
        return f"第一个格子：列 `{S['x1']}`，行 `{S['y1']}`，和 = `{S['x1'] + S['y1']}`"
    tot = S['x1'] + S['y1'] + S['x2'] + S['y2']
    return f"四个坐标之和 `{S['x1']} + {S['y1']} + {S['x2']} + {S['y2']}` = =={tot}==，{'偶数 → 同色' if tot % 2 == 0 else '奇数 → 异色'}"


CONFIG = dict(
    num=3274, title='检查棋盘方格颜色是否相同', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='行列坐标和的奇偶性',
    tags=[],
    code='''
class Solution(object):
    def checkTwoChessboards(self, coordinate1, coordinate2):

        x1 = ord(coordinate1[0]) - 96
        y1 = int(coordinate1[1])

        x2 = ord(coordinate2[0]) - 96
        y2 = int(coordinate2[1])

        return (x1 + y1 + x2 + y2) % 2 == 0
''',
    call='Solution().checkTwoChessboards("a1", "h3")',
    expect=False,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: '棋盘：深色 = 行列坐标和为偶的格子（a1 = 1+1，黑格），浅色 = 和为奇', size=24),
    ],
    watch=[('x1', 'x1', 'blue'), ('y1', 'y1', 'blue'), ('x2', 'x2', 'pink'), ('y2', 'y2', 'pink')],
    captions={
        'x1 =': '列字母转数字：`ord(\'{coordinate1[0]}\') - 96` = `{x1}`（a=1, b=2, ...）',
        'y1 =': '行数字直接 `int` 转换：`y1 = {y1}`',
        'x2 =': '第二个格子的列：`x2 = {x2}`',
        'y2 =': '第二个格子的行：`y2 = {y2}`',
        'return': '两格和的奇偶相同 ⇔ 四个数相加是偶数：`{x1 + y1 + x2 + y2} % 2` = `{(x1 + y1 + x2 + y2) % 2}` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='行列坐标之和的奇偶，决定棋盘格的颜色',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['8×8 国际象棋棋盘，左下角是黑色，相邻格颜色互不相同',
                 '给两个坐标，判断两个格子是否同色',
                 '示例：`"a1"`、`"h3"` → `false`'],
        quote='棋盘是奇偶性问题常见的背景板，棋盘中行列坐标之和为偶数的单元格都是同一种颜色，而和为奇数的单元格则是另一种颜色。',
        quote_src='—— yiduobo 题解',
        idea=['先把列字母转成 1~8：`ord(c) - 96`，行数字直接 `int`',
              '两格和的奇偶相同 → 同色；而这等价于==四个数之和为偶数==',
              '所以只需累加四个坐标，看是不是偶数'],
        after=[dict(heading='推导：为什么只看四数之和', lines=[
            '设两格坐标和为 `a`、`b`，同色 ⇔ `a` 与 `b` 奇偶相同',
            '奇偶相同 ⇔ `a + b` 为偶数（奇+奇、偶+偶都是偶）',
            '所以直接判断 `x1 + y1 + x2 + y2` 是否为偶数'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错：`ord` 减 96 才让 `a` 变成 1，和 `a1` 的行号对齐',
                 '奇偶性相同 ⇔ 两个和相加为偶，不用分别求奇偶'],
    ),
)
