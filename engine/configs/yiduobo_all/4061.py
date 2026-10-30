
CASES = [([8, 1], [1, 8]), ([4, 2], [1, 3]), ([1, 1], [1, 1]), ([2, 3], [5, 7])]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '8×8 棋盘（行列从 1 开始）：皇后（蓝）走向目标（粉）', 22, T['muted'], bold=True)
    src = S.get('source')
    tgt = S.get('target')
    if not src or not tgt:
        return
    sr, sc = src
    tr, tc = tgt
    cell = min(76, (y1 - y0 - 150) / 8, (x1 - x0 - 120) / 8)
    bx = x0 + (x1 - x0 - cell * 8) / 2
    by = y0 + 56
    line = S.get('_line')
    show_rays = line is not None and line >= 7
    for r in range(1, 9):
        for c in range(1, 9):
            X, Y = bx + (c - 1) * cell, by + (r - 1) * cell
            dark = (r + c) % 2 == 0
            fill = (44, 52, 64) if dark else (30, 36, 46)
            if show_rays and (r == sr or c == sc or r + c == sr + sc or r - c == sr - sc):
                fill = (52, 82, 118) if dark else (44, 70, 104)
            cv.rect((X, Y, X + cell, Y + cell), fill=fill)
    for k in range(1, 9):
        cv.text((bx - 14, by + (k - 0.5) * cell), k, 18, T['dim'], anchor='rm', mono=True)
        cv.text((bx + (k - 0.5) * cell, by - 4), k, 18, T['dim'], anchor='mb', mono=True)
    tX, tY = bx + (tc - 0.5) * cell, by + (tr - 0.5) * cell
    sX, sY = bx + (sc - 0.5) * cell, by + (sr - 0.5) * cell
    if (sr, sc) != (tr, tc):
        cv.rect((tX - cell * 0.32, tY - cell * 0.32, tX + cell * 0.32, tY + cell * 0.32), fill=T['pink'], r=cell * 0.32)
        cv.text((tX, tY), 'T', 30, T['bg'], anchor='mm', bold=True)
    cv.rect((sX - cell * 0.32, sY - cell * 0.32, sX + cell * 0.32, sY + cell * 0.32), fill=T['blue'], r=cell * 0.32,
            outline=T['pink'] if (sr, sc) == (tr, tc) else None, width=5)
    cv.text((sX, sY), 'Q', 32, T['bg'], anchor='mm', bold=True)
    cv.text((x0 + 18, by + 8 * cell + 14), f'source = ({sr}, {sc})　target = ({tr}, {tc})', 26, T['text'], bold=True)
    hint = ''
    if show_rays:
        if (sr, sc) == (tr, tc):
            hint = '已经在目标上'
        elif sr == tr or sc == tc or sr + sc == tr + tc or sr - sc == tr - tc:
            hint = '目标在皇后的行/列/对角线上（亮色格）'
        else:
            hint = '目标不在任何一条亮色线上'
        cv.text((x0 + 18, by + 8 * cell + 50), hint, 24, T['yellow'], bold=True)


CONFIG = dict(
    num=4061, title='皇后到达目标格子的最少移动步数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='先判相同，再判共线，否则两步',
    tags=[],
    code='''
class Solution(object):
    def minQueenMoves(self, source, target):
        
        if source == target:
            return 0
        
        if source[0] == target[0] or source[1] == target[1] or source[0] + source[1] == target[0] + target[1] or source[0] - source[1] == target[0] - target[1]:
            return 1
        
        return 2
''',
    setup='CASES = [([8, 1], [1, 8]), ([4, 2], [1, 3]), ([1, 1], [1, 1]), ([2, 3], [5, 7])]',
    call='[Solution().minQueenMoves(a, b) for a, b in CASES]',
    expect=[1, 2, 0, 2],
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('source', 'source', 'blue'), ('target', 'target', 'pink')],
    captions={
        'if source == target': lambda S, B, r: ('`source == target`：一开始就在目标上' if S.source == S.target else '`source != target` → 至少要一步'),
        'return 0': '起点就是终点，答案显然是 ==0==',
        'if source[0] == target[0] or': lambda S, B, r: (
            '同一行：`source[0] == target[0]` → 1 步' if S.source[0] == S.target[0] else
            '同一列：`source[1] == target[1]` → 1 步' if S.source[1] == S.target[1] else
            f'右上到左下的对角线：横纵坐标之和相等 `{sum(S.source)}` = `{sum(S.target)}` → 1 步' if sum(S.source) == sum(S.target) else
            f'左上到右下的对角线：横纵坐标之差相等 `{S.source[0] - S.source[1]}` = `{S.target[0] - S.target[1]}` → 1 步' if S.source[0] - S.source[1] == S.target[0] - S.target[1] else
            f'行、列、和、差都不相等 → 不在一条直线上'),
        'return 1': '同行、同列或同对角线，==一步到位==',
        'return 2': '都不符合：先走到同一行，再走到同一列，==最多两步==',
    },
    cards=dict(
        one_liner='相同 0 步；共线 1 步；其余 2 步',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`8×8` 空棋盘，下标从 1 开始，皇后一次可沿行、列、对角线走多格',
                 '问从 `source` 走到 `target` 的最少次数',
                 '示例：`source=[8,1]`，`target=[1,8]` → `1`'],
        quote='同行同列是非常容易判断的，而对于对角线，若为左上到右下的对角线，同一条对角线上横纵坐标之差相等，若为右上到左下的对角线，同一条对角线上横纵坐标之和相等。',
        quote_src='—— yiduobo 题解',
        idea=['先看起点终点是否相同 → 0',
              '再看同行、同列、横纵坐标差相等、横纵坐标和相等 → 1',
              '否则先走一步到同一行，再走一步到同一列 → 2'],
        summary=['时间、空间都是 `O(1)`',
                 '判断顺序不能反：相同的点也满足共线，要先返回 0',
                 '差相等 = 左上到右下，和相等 = 右上到左下',
                 '原文代码已是 Python 3 可运行，未改动'],
    ),
)
