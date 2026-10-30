
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
    author='灵茶山艾府', technique='分类讨论：0 / 1 / 2 步',
    tags=[],
    code='''
class Solution:
    def minQueenMoves(self, source: list[int], target: list[int]) -> int:
        sr, sc = source
        tr, tc = target
        if sr == tr and sc == tc:
            return 0
        if sr == tr or sc == tc or sr + sc == tr + tc or sr - sc == tr - tc:
            return 1
        return 2
''',
    setup='CASES = [([8, 1], [1, 8]), ([4, 2], [1, 3]), ([1, 1], [1, 1]), ([2, 3], [5, 7])]',
    call='[Solution().minQueenMoves(a, b) for a, b in CASES]',
    expect=[1, 2, 0, 2],
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('sr', 'sr', 'blue'), ('sc', 'sc', 'blue'), ('tr', 'tr', 'pink'), ('tc', 'tc', 'pink')],
    captions={
        'sr, sc = source': '皇后在第 `{sr}` 行第 `{sc}` 列',
        'tr, tc = target': '目标在第 `{tr}` 行第 `{tc}` 列',
        'if sr == tr and sc == tc': lambda S, B, r: ('起点终点是同一格' if (S.sr, S.sc) == (S.tr, S.tc) else '起点终点不同格 → 至少要走一步'),
        'return 0': '已经在目标上，==不需要移动==：返回 0',
        'if sr == tr or': lambda S, B, r: (
            '同一行（`sr == tr`）→ 一步直达' if S.sr == S.tr else
            '同一列（`sc == tc`）→ 一步直达' if S.sc == S.tc else
            f'同一条斜率 -1 的对角线：`sr + sc = {S.sr + S.sc}` == `tr + tc = {S.tr + S.tc}` → 一步直达' if S.sr + S.sc == S.tr + S.tc else
            f'同一条斜率 1 的对角线：`sr - sc = {S.sr - S.sc}` == `tr - tc = {S.tr - S.tc}` → 一步直达' if S.sr - S.sc == S.tr - S.tc else
            f'四个条件都不满足：行 {S.sr}≠{S.tr}，列 {S.sc}≠{S.tc}，和 {S.sr + S.sc}≠{S.tr + S.tc}，差 {S.sr - S.sc}≠{S.tr - S.tc}'),
        'return 1': '在同一条直线上，皇后==一步==就能到',
        'return 2': '不在同一直线：先走到目标所在的行，再沿列走过去，==两步==足够',
    },
    cards=dict(
        one_liner='0 步、1 步、2 步，三种情况分类讨论',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`8×8` 棋盘，皇后可沿行、列、对角线走任意格',
                 '求从 `source` 到 `target` 的最少移动次数',
                 '示例：`[4,2] → [1,3]` 答案 `2`'],
        quote='如果起点终点相同，无需移动，返回 0。如果起点终点在同一条直线上，返回 1。否则要走两步，返回 2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一直线四种：横坐标相同、纵坐标相同、斜率为 -1、斜率为 1',
              '斜率 -1 对应 `sr + sc` 相等，斜率 1 对应 `sr - sc` 相等',
              '其余情况一定是 2：棋盘空，先横后竖'],
        summary=['时间、空间都是 `O(1)`',
                 '易错：必须==先判断相同==再判断共线，否则 `(1,1)→(1,1)` 会返回 1',
                 '类似题：4034 象到达目标格子的最少移动步数',
                 '演示用 4 组输入连续调用，看三种答案各自怎么来的'],
    ),
)
