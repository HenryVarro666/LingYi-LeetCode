def _tri(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    c = S.get('c')
    cv.text((x0 + 18, y0 + 4), 'c：左对齐的杨辉三角（黄 = 正在算，蓝 = 左上 + 正上）', 24, T['muted'], bold=True)
    if not c:
        return
    rows = min(len(c), 7)
    cur_i, cur_j = S.get('i'), S.get('j')
    line = S.get('_line', 0)
    calc = cur_i is not None and cur_j is not None and line in (6,)
    top = 0 if not calc else max(0, min(cur_i - 6, len(c) - rows))
    if not calc:
        top = 0
    cell = 70
    sx = x0 + 90
    sy = y0 + 60
    for r in range(top, min(len(c), top + rows)):
        cv.text((sx - 10, sy + (r - top) * 62 + 28), f'c[{r}]', 20, T['dim'], anchor='rm', mono=True)
        for k, v in enumerate(c[r]):
            if k > 9:
                cv.text((sx + k * cell + 10, sy + (r - top) * 62 + 28), '…', 24, T['muted'], anchor='lm')
                break
            col = None
            if calc and r == cur_i and k == cur_j:
                col = T['yellow']
            elif calc and r == cur_i - 1 and k in (cur_j - 1, cur_j):
                col = T['blue']
            fill = col if col else (60, 66, 76)
            cv.rect((sx + k * cell, sy + (r - top) * 62, sx + k * cell + cell - 6, sy + (r - top) * 62 + 54), fill=fill, r=6)
            cv.text((sx + k * cell + cell / 2 - 3, sy + (r - top) * 62 + 27), v if v < 1e7 else '…', 22,
                    T['bg'] if col else T['text'], anchor='mm', bold=True)


def _f(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') not in (6,):
        return '`c[i][0] = c[i][i] = 1`，中间 `c[i][j] = c[i-1][j-1] + c[i-1][j]`'
    c = S['c']
    return f'`c[{i}][{j}] = c[{i-1}][{j-1}] + c[{i-1}][{j}] = {c[i-1][j-1]} + {c[i-1][j]}` = =={c[i][j]}=='


CODE = '''
MX = 6
c = [[1] * (i + 1) for i in range(MX)]
for i in range(2, MX):
    for j in range(1, i):
        # 左上方的数 + 正上方的数
        c[i][j] = c[i - 1][j - 1] + c[i - 1][j]

class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        return c[rowIndex]
'''.strip('\n')


CONFIG = dict(
    num=119, title='杨辉三角 II', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='预处理杨辉三角',
    code=CODE,
    setup=f'CODE = {CODE!r}\ndel MX, c, i, j',
    call="exec(compile(CODE, '<solution>', 'exec'), globals())\nSolution().getRow(4)",
    expect=[1, 4, 6, 4, 1],
    skip=['for j in range'],
    max_steps=80,
    views=[
        dict(type='text', fn=_f, size=26, h=60),
        dict(type='custom', draw=_tri, h=500),
    ],
    watch=['i', 'j', ('rowIndex', 'rowIndex', 'green')],
    captions={
        'MX = 6': '原文 `MX = 34`（题目 `rowIndex <= 33`）；演示取 `MX = {MX}`，预处理 `c[0]` 到 `c[{MX-1}]`',
        'c = [[1]': '先把每一排都填满 `1`：每排首尾本来就是 `1`，只剩中间要算',
        'for i in range(2': lambda S, B, ret: ('第 0、1 排只有 1，从 `i = 2` 开始算中间的数' if B.get('i') is None else (f'第 `{S.i}` 排算完，继续下一排' if S.i < S.MX - 1 else f'第 `{S.i}` 排算完，所有排都算完了，预处理结束')),
        'c[i][j] =': '`c[{i}][{j}] = {c[i-1][j-1]} + {c[i-1][j]}` = =={c[i][j]}==：左上 + 正上',
        'return c[rowIndex]': '预处理好了，查询直接取 `c[{rowIndex}]` = =={ret}==，==O(1)==',
    },
    cards=dict(
        one_liner='预处理整个杨辉三角，每次查询直接取一排',
        complexity='查询时间 `O(1)`，空间 `O(1)`（预处理不计）',
        problem=['给定 `rowIndex`，返回杨辉三角的第 `rowIndex` 行（从 0 开始）',
                 '每个数是它左上方和正上方两数之和',
                 '示例：`rowIndex = 3` → `[1,3,3,1]`；`0 <= rowIndex <= 33`'],
        quote='每一排的第一个数和最后一个数都是 1；其余数字，等于左上方的数，加上正上方的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把每一排左对齐，`c[i][j]` 就在 `c[i-1][j-1]` 和 `c[i-1][j]` 的下方',
              '数据范围只到 33，==一次性预处理==全部排，调用只是取下标',
              '本视频把常数 `MX` 由 34 改成 6，其余代码逐字照搬；演示 `rowIndex = 4`'],
        summary=['查询 `O(1)`，预处理的时间空间不计入',
                 '递推式本质是组合数恒等式：某个物品选或不选，`C(i,j) = C(i-1,j-1) + C(i-1,j)`',
                 '易错点：首尾要是 1，内层 `j` 只循环 `1` 到 `i-1`',
                 '直接返回 `c[rowIndex]` 是同一个列表对象，调用方不要修改'],
    ),
)
