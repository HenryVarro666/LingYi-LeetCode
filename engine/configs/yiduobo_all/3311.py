R, C = 2, 3   # 示例走的是“最大度数 ≤ 3”的两行情形


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('g')
    n = len(g) if g else 0
    rows = S.get('res') or []
    deg = S.get('degree')
    cv.text((x0 + 18, y0 + 4), '矩阵（绿 = 已填入，黄 = 正在处理的邻居 y）', 22, T['muted'], bold=True)
    cell = min(120, (y1 - y0 - 90) / R, (x1 - x0) * 0.62 / C)
    gx = x0 + 30
    gy = y0 + 70
    y = S.get('y') if S.get('_line', 0) >= 20 else None
    for r in range(R):
        for c in range(C):
            X, Y = gx + c * cell, gy + r * cell
            v = rows[r][c] if r < len(rows) and c < len(rows[r]) else None
            fill = T['green'] if v is not None else T['panel2']
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), v if v is not None else '?', 38, T['bg'] if v is not None else T['dim'],
                    anchor='mm', bold=True, mono=True)
    ax = gx + C * cell + 40
    cv.text((ax, gy - 8), '邻居集合 g[x]（度数）', 22, T['muted'], bold=True)
    placed = {v for r in rows for v in r}
    for k in range(n):
        Y = gy + 28 + k * 46
        col = T['yellow'] if k == y else (T['green'] if k in placed else T['text'])
        cv.text((ax, Y), f"{k}: {sorted(g[k])}  （{len(g[k])}）", 26, col, bold=(k == y), mono=True)


CONFIG = dict(
    num=3311, title='构造符合图结构的二维矩阵', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='按度数 2/3/4 识别角和边',
    tags=['贪心算法', '思维题', '难度分 2664'],
    code='''
class Solution(object):
    def constructGridLayout(self, n, edges):

        g = [set() for _ in range(n)]
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        degree = [len(g[x]) for x in range(n)]
        res = []

        if min(degree) == 1:
            for x in range(n):
                if degree[x] == 1:
                    break

            res.append([x])
            while len(res[-1]) < n:
                for y in g[res[-1][-1]]:
                    if len(res[-1]) == 1 or y != res[-1][-2]:
                        res[-1].append(y)
                        break
        
        elif max(degree) <= 3:
            res.append([])
            res.append([])

            for x in range(n):
                if degree[x] == 2:
                    break
            res[0].append(x)
            for y in g[x]:
                if degree[y] == 2 and len(res[1]) < len(res[0]):
                    res[1].append(y)
                else:
                    res[0].append(y)

            for col in range(1, n // 2 - 1):
                for y in g[res[0][col]]:
                    if y == res[0][col - 1]:
                        continue
                    if y in g[res[1][col - 1]]:
                        res[1].append(y)
                    else:
                        res[0].append(y)
            
            for y in g[res[0][-1]]:
                if degree[y] == 2 and y != res[0][-2]:
                    res[1].append(y)
                    break

        else:
            res.append([])
            for x in range(n):
                if degree[x] == 2:
                    break
            
            res[0].append(x)
            while len(res[0]) == 1 or degree[res[0][-1]] != 2:
                for y in g[res[0][-1]]:
                    if degree[y] != 4 and (len(res[0]) == 1 or res[0][-2] != y):
                        res[0].append(y)
                        break
            
            m = n // len(res[0])
            for row in range(1, m):
                res.append([])
                for y in g[res[row - 1][0]]:
                    if y != res[row - 1][1] and (row == 1 or y != res[row - 2][0]):
                        res[row].append(y)
                        break
                
                for col in range(1, len(res[0])):
                    for y in g[res[row][col - 1]]:
                        if y != res[row - 1][col - 1] and y in g[res[row - 1][col]]:
                            res[row].append(y)
                            break

        return res
''',
    call='Solution().constructGridLayout(6, [[3,0],[0,4],[1,5],[5,2],[3,1],[0,5],[4,2]])',
    expect=[[1, 5, 2], [3, 0, 4]],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='degree', h=190, label='degree（每个点的度数）',
             color=lambda S, i, v: 'orange' if v == 2 else ('blue' if v == 3 else None)),
    ],
    watch=['x', 'y', 'col', ('min(degree)', 'min(degree)', 'cyan'), ('max(degree)', 'max(degree)', 'cyan')],
    skip=['g[x].add', 'g[y].add', 'for x, y in edges', 'res.append([])'],
    captions={
        'g = [set()': '建图：`g[x]` 是 `x` 的邻居集合',
        'degree = [': '`degree[x]` = 邻居个数。矩阵里：角 ==2==、边 ==3==、内部 ==4==（单行时端点是 1）',
        'if min(degree) == 1': lambda S, B, r: (f"`min(degree) = {min(S.degree)}`" + (' == 1：只有一行（一列）' if min(S.degree) == 1 else ' ≠ 1：不是单行')),
        'elif max(degree) <= 3': lambda S, B, r: (f"`max(degree) = {max(S.degree)}`" + (' ≤ 3：没有内部点 → ==只有两行==' if max(S.degree) <= 3 else ' > 3：有内部点，行数 ≥ 3')),
        'for x in range(n)': lambda S, B, r: (f"找一个度数为 2 的点（角）：`x = {S.x}`，`degree[{S.x}] = {S.degree[S.x]}`" if 'x' in S else ''),
        'if degree[x] == 2': lambda S, B, r: (f"`degree[{S.x}] = {S.degree[S.x]}`" + (' == 2：找到一个角，放在左上角' if S.degree[S.x] == 2 else ' ≠ 2，继续找')),
        'res[0].append(x)': '左上角 `res[0] = {res[0]}`',
        'res = []': '`res` 存矩阵的各行',
        'for y in g[x]': lambda S, B, r: ('角 `x = %d` 的邻居看完了' % S.x if getattr(B, 'y', None) == S.y and S.y == list(S.g[S.x])[-1] else f"看角 `x = {S.x}` 的邻居 `y = {S.y}`"),
        'if degree[y] == 2 and len(res[1]) < len(res[0])': lambda S, B, r: (f"`degree[{S.y}] = {S.degree[S.y]}`" + (' == 2 且下一行还空着' if S.degree[S.y] == 2 and len(S.res[1]) < len(S.res[0]) else '：不满足') + ' → ' + ('==这个邻居放左下角==（两行的角）' if S.degree[S.y] == 2 and len(S.res[1]) < len(S.res[0]) else '放在上一行右侧')),
        'for col in range(1, n // 2 - 1)': lambda S, B, r: ('中间的列都处理完了' if getattr(B, 'col', None) == S.col else f"处理第 `col = {S.col}` 列：上方 `res[0][{S.col}] = {S.res[0][S.col]}`"),
        'for y in g[res[0][col]]': lambda S, B, r: ('上方点 `%d` 的邻居看完了' % S.res[0][S.col] if getattr(B, 'y', None) == S.y and S.y == list(S.g[S.res[0][S.col]])[-1] else f"看上方点 `{S.res[0][S.col]}` 的邻居 `y = {S.y}`"),
        'if y == res[0][col - 1]': lambda S, B, r: (f"`y = {S.y}`：" + ('是左边那个点，跳过' if S.y == S.res[0][S.col - 1] else '不是左边的点，继续判断')),
        'continue': '跳过左边的点',
        'if y in g[res[1][col - 1]]': lambda S, B, r: (f"`y = {S.y}` 是否也是下一行左边点 `{S.res[1][S.col - 1]}` 的邻居？" + (' ==是 → 放在这一列的下面==' if S.y in S.g[S.res[1][S.col - 1]] else ' 否 → 放在上一行右侧')),
        'res[1].append(y)': '放到下面一行：`res[1] = {res[1]}`',
        'res[0].append(y)': '放到上面一行：`res[0] = {res[0]}`',
        'for y in g[res[0][-1]]': lambda S, B, r: (f"最后补右下角：看右上角 `{S.res[0][-1]}` 的邻居 `y = {S.y}`" if 'y' in S else ''),
        'if degree[y] == 2 and y != res[0][-2]': lambda S, B, r: (f"`degree[{S.y}] = {S.degree[S.y]}`，" + ('是度数 2 的另一个邻居 → ==右下角==' if S.degree[S.y] == 2 and S.y != S.res[0][-2] else '不是 → 看下一个')),
        'return res': '矩阵完成：`{res}`',
    },
    cards=dict(
        one_liner='用度数认出角和边：角 2、边 3、内部 4，再逐步摆放',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`edges` 描述一张 `n` 个点的无向图；把 `0 ~ n-1` 填进矩阵',
                 '矩阵中上下左右相邻 ==当且仅当== 图中有边；返回任意一种合法答案',
                 '本视频：`n=6` 的图，走“最大度数 ≤ 3”的两行分支'],
        quote='对于一个矩阵而言，其四个角上的单元格只与两个单元格相邻，在四条边上且不在四个角上的单元格，则与三个单元格相邻，其他所有单元格均与四个单元格相邻。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看度数最小值 / 最大值，判断矩阵是 1 行、2 行，还是 ≥ 3 行',
              '2 行：从度 2 的角出发，逐列摆上下两行（谁和左下角相邻谁放下面）',
              '≥ 3 行：先走边摆第一行，再逐行用“左边的邻居 ∩ 上边的邻居”确定每格'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '三个分支：`min(degree) == 1` 单行；`max(degree) <= 3` 两行；其余 ≥ 3 行',
                 '本视频只演示了两行分支；≥ 3 行时靠“同时是左邻居和上邻居的邻居”确定每格',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动',
                 '对比灵神：灵神每步选度数最小的邻居统一成一段；yiduobo 分三种情形各写一套'],
    ),
)
