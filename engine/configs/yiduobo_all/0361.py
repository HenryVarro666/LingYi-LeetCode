GRID = [['0', 'E', '0'], ['E', '0', 'W'], ['0', 'E', '0']]
NAMES = [('left', '左'), ('right', '右'), ('up', '上'), ('down', '下')]


def _gcolor(S, i, j, v):
    return {'E': 'red', 'W': 'purple'}.get(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '预处理表：在空地放炸弹时，该方向能炸到的敌人数（黄 = 这一步刚写入）', 22, T['muted'], bold=True)
    if 'left' not in S:
        return
    m, n = S['m'], S['n']
    gw = (x1 - x0 - 30) / 4
    cell = min(52, (gw - 16) / n)
    for k, (nm, zh) in enumerate(NAMES):
        tab, old = S[nm], B.get(nm)
        ox = x0 + 15 + k * gw + (gw - cell * n) / 2
        oy = y0 + 80
        cv.text((ox + cell * n / 2, oy - 12), f'{nm}（{zh}）', 22, T['text'], anchor='mb', bold=True, mono=True)
        for i in range(m):
            for j in range(n):
                v = tab[i][j]
                ch = old is not None and old[i][j] != v
                g = GRID[i][j]
                fill = T['yellow'] if ch else ((60, 40, 48) if g == 'E' else (52, 46, 70) if g == 'W' else T['panel2'])
                cv.rect((ox + j * cell + 1, oy + i * cell + 1, ox + (j + 1) * cell - 1, oy + (i + 1) * cell - 1), fill=fill, r=5)
                txt = '' if g in 'EW' else str(v)
                cv.text((ox + j * cell + cell / 2, oy + i * cell + cell / 2), txt, 26, T['bg'] if ch else T['text'], anchor='mm', bold=True)
        if 'i' in S and 'j' in S:
            i, j = S['i'], S['j']
            if i < m and j < n:
                cv.rect((ox + j * cell, oy + i * cell, ox + (j + 1) * cell, oy + (i + 1) * cell), outline=T['blue'], width=3, r=5)


CONFIG = dict(
    num=361, title='轰炸敌人', difficulty='Medium', category='网格图',
    author='yiduobo', technique='四方向预处理 · 类 DP 累计',
    code='''
class Solution(object):
    def maxKilledEnemies(self, grid):

        m = len(grid)
        n = len(grid[0])

        left = [[0] * n for _ in range(m)]
        right = [[0] * n for _ in range(m)]
        up = [[0] * n for _ in range(m)]
        down = [[0] * n for _ in range(m)]

        for i in range(m):
            cnt = 0
            for j in range(n):
                if grid[i][j] == 'W':
                    cnt = 0
                elif grid[i][j] == 'E':
                    cnt += 1
                else:
                    left[i][j] = cnt

            cnt = 0
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 'W':
                    cnt = 0
                elif grid[i][j] == 'E':
                    cnt += 1
                else:
                    right[i][j] = cnt

        for j in range(n):
            cnt = 0
            for i in range(m):
                if grid[i][j] == 'W':
                    cnt = 0
                elif grid[i][j] == 'E':
                    cnt += 1
                else:
                    up[i][j] = cnt

            cnt = 0
            for i in range(m - 1, -1, -1):
                if grid[i][j] == 'W':
                    cnt = 0
                elif grid[i][j] == 'E':
                    cnt += 1
                else:
                    down[i][j] = cnt

        res = 0
        for i in range(m):
            for j in range(n):
                res = max(res, left[i][j] + right[i][j] + up[i][j] + down[i][j])
        return res
''',
    call=f'Solution().maxKilledEnemies({GRID})',
    expect=3,
    views=[
        dict(type='grid', var='grid', label='grid（红 E = 敌人，紫 W = 墙，0 = 空地；蓝框 = 当前格）', cell=84, h=290,
             color=_gcolor, cursors=[('i', 'j', 'blue')]),
        dict(type='custom', draw=_draw, h=240),
        dict(type='text', size=26, h=70, fn=lambda S: (f"放在 `({S['i']},{S['j']})` 能炸到：`{S['left'][S['i']][S['j']]} + {S['right'][S['i']][S['j']]} + {S['up'][S['i']][S['j']]} + {S['down'][S['i']][S['j']]}` = =={S['left'][S['i']][S['j']] + S['right'][S['i']][S['j']] + S['up'][S['i']][S['j']] + S['down'][S['i']][S['j']]}==" if S.get('_line') == 53 and 'i' in S and 'j' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    skip=['m = len', 'n = len', 'up = [[0]', 'down = [[0]', 13, 22, 32, 41, "== 'W':", "== 'E':", 'for i in range', 'for j in range'],
    max_steps=130,
    captions={
        'left = [[0] * n': '`left[i][j]`：在 `(i,j)` 放炸弹，左侧能炸到几个敌人',
        'right = [[0] * n': '`right`、`up`、`down` 同理，各一张表，初值全 0',
        'cnt = 0': '`grid[{i}][{j}]` 是墙 → 前面的敌人被它挡住，==`cnt` 清零==',
        'cnt += 1': '`grid[{i}][{j}]` 是敌人 → `cnt` 加 1 = =={cnt}==，这格自己不能放炸弹',
        'left[i][j] = cnt': '`({i},{j})` 是空地：`left[{i}][{j}] = {cnt}`，左边没被挡住的敌人 {cnt} 个',
        'right[i][j] = cnt': '`({i},{j})` 是空地：`right[{i}][{j}] = {cnt}`，从右往左扫到的敌人 {cnt} 个',
        'up[i][j] = cnt': '`({i},{j})` 是空地：`up[{i}][{j}] = {cnt}`，上方敌人 {cnt} 个',
        'down[i][j] = cnt': '`({i},{j})` 是空地：`down[{i}][{j}] = {cnt}`，下方敌人 {cnt} 个',
        'res = max': '`res = max({B.res}, 四方向之和 {left[i][j] + right[i][j] + up[i][j] + down[i][j]}) = {res}`',
        'return res': '最多能炸 `{res}` 个敌人',
    },
    cards=dict(
        one_liner='四个方向各扫一遍，用累计的敌人数预处理出每个空地的杀伤',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里 `E` 敌人、`W` 墙、`0` 空地；炸弹放在空地上',
                 '炸弹向上下左右四个方向炸，直到碰到==墙==为止，求最多炸死几个敌人',
                 '本视频：`[["0","E","0"],["E","0","W"],["0","E","0"]]` → `3`'],
        quote='以杀伤左侧的敌人举例。cnt表示当前单元格左侧没有被墙壁阻隔的敌人数量。……若grid[i][j]是墙壁，那么之前左侧的敌人都被这堵墙壁阻隔开了，因此需要将cnt清零。',
        quote_src='—— yiduobo 题解原文',
        idea=['暴力枚举每个空地再向四方向走，会重复扫很多格子',
              '改成「每行从左、从右各扫一遍，每列从上、从下各扫一遍」，扫描时累计 `cnt`',
              '墙清零、敌人 +1、空地就把 `cnt` 写进对应表；最后四张表相加取最大值'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（四张表），可优化到 `O(n)`',
                 '易错：墙要清零 `cnt`；敌人和墙所在格不能放炸弹，表里保持 0 且最后也不会被选中',
                 '这里四张表之和只在空地有意义；敌人格、墙格的四项全为 0',
                 '同类思路：各方向预处理 + 枚举合并'],
    ),
)
