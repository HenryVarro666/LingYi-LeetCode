R, C = 3, 2   # 示例的答案是 3 行 2 列


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('g')
    n = len(g) if g else 0
    rows = S.get('ans')
    if rows is None:
        rows = [S['row']] if S.get('row') else []
    cv.text((x0 + 18, y0 + 4), '矩阵（绿 = 已填入，粉 = 当前 x，黄 = 当前 y）', 22, T['muted'], bold=True)
    cell = min(110, (y1 - y0 - 90) / R, (x1 - x0) * 0.5 / C)
    gx = x0 + 40
    gy = y0 + 60
    line = S.get('_line', 0)
    x = S.get('x') if line >= 17 else None
    y = S.get('y') if line >= 17 else None
    for r in range(R):
        for c in range(C):
            X, Y = gx + c * cell, gy + r * cell
            v = rows[r][c] if r < len(rows) and c < len(rows[r]) else None
            fill = T['panel2']
            if v is not None:
                fill = T['green']
            if v is not None and v == x:
                fill = T['pink']
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), v if v is not None else '?', 38, T['bg'] if v is not None else T['dim'],
                    anchor='mm', bold=True, mono=True)
    # 邻接表
    ax = gx + C * cell + 60
    cv.text((ax, gy - 4), '邻接表 g[x]（度数）', 22, T['muted'], bold=True)
    placed = {v for r in rows for v in r}
    for k in range(n):
        Y = gy + 30 + k * 46
        col = T['pink'] if k == x else T['yellow'] if k == y else (T['green'] if k in placed else T['text'])
        cv.text((ax, Y), f"{k}: {g[k]}  （{len(g[k])}）", 26, col, bold=(k == x or k == y), mono=True)


CONFIG = dict(
    num=3311, title='构造符合图结构的二维矩阵', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='拼图：先拼第一行，再逐行往下',
    tags=['贪心算法', '思维题', '难度分 2664'],
    code='''
class Solution:
    def constructGridLayout(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        # 找一个度数最小的点
        x = 0
        for i, to in enumerate(g):
            if len(to) < len(g[x]):
                x = i

        row = [x]
        vis = [False] * n
        vis[x] = True
        deg_st = len(g[x])  # 起点的度数
        while True:  # 注意题目保证 n >= 2，可以至少循环一次
            nxt = -1
            for y in g[x]:
                if not vis[y] and (nxt < 0 or len(g[y]) < len(g[nxt])):
                    nxt = y
            x = nxt
            row.append(x)
            vis[x] = True
            if len(g[x]) == deg_st:
                break

        ans = [[] for _ in range(n // len(row))]
        ans[0] = row
        for i in range(1, len(ans)):
            for x in ans[i - 1]:
                for y in g[x]:
                    # x 上左右的邻居都访问过了，没访问过的邻居只会在 x 下面
                    if not vis[y]:
                        vis[y] = True
                        ans[i].append(y)
                        break
        return ans
''',
    call='Solution().constructGridLayout(6, [[3,0],[0,4],[1,5],[5,2],[3,1],[0,5],[4,2]])',
    expect=[[1, 3], [5, 0], [2, 4]],
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='array', var='vis', h=170, label='vis（True = 已填入矩阵）',
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=['x', 'y', 'nxt', 'deg_st', 'i'],
    skip=['g[x].append', 'g[y].append', 'for x, y in edges', 'for i, to in enumerate', 'x = i'],
    captions={
        'g = [[]': '建图：`g[x]` 存 `x` 的邻居，邻居个数就是度数',
        'if len(to) < len(g[x])': '`len(g[{i}]) = {len(to)}` < `len(g[{x}]) = {len(g[x])}`？→ {"更小，更新起点" if len(to) < len(g[x]) else "不更小"}',
        'row = [x]': '拼图先找==角==：度数最小的点 `x = {x}`（度数 {len(g[x])}），作为第一行的起点',
        'vis = [False]': '`vis` 标记已经填入矩阵的点',
        'deg_st = len': '`deg_st = {deg_st}`：起点的度数。第一行的另一个角度数也会是它',
        'while True': '沿着第一行往右走，直到遇到度数和起点相同的点（另一个角）',
        'nxt = -1': '`nxt` 记录 `x` 的未访问邻居中度数最小的',
        19: '`nxt` 记录 `x` 的未访问邻居中度数最小的',
        20: lambda S, B, r: ('`x = %d` 的邻居都看完了' % S.x if getattr(B, 'y', None) == S.y and S.y == S.g[S.x][-1] else f"看 `x = {S.x}` 的邻居 `y = {S.y}`（度数 {len(S.g[S.y])}）"),
        33: lambda S, B, r: ('`x = %d` 的邻居看完了' % S.x if getattr(B, 'y', None) == S.y and S.y == S.g[S.x][-1] else f"看 `x = {S.x}` 的邻居 `y = {S.y}`（度数 {len(S.g[S.y])}）"),
        27: '第一行完成，跳出循环',
        38: '`x` 的下方找到了，换下一个 `x`',
        'if not vis[y] and': lambda S, B, r: (f"`y = {S.y}`：" + ('已访问，跳过' if S.vis[S.y] else (f"未访问，度数 `{len(S.g[S.y])}`" + ('，==暂时最小，记为 nxt==' if (S.nxt < 0 or len(S.g[S.y]) < len(S.g[S.nxt])) else f'，不比 `nxt = {S.nxt}` 小')))),
        'nxt = y': '`nxt = {nxt}`：目前度数最小的邻居（优先走度数小的，即外圈）',
        'x = nxt': '`x` 走到 `{x}`',
        'row.append(x)': '第一行 `row = {row}`',
        'vis[x] = True': '`{x}` 标记已填入',
        'if len(g[x]) == deg_st': lambda S, B, r: (f"`len(g[{S.x}]) = {len(S.g[S.x])}` " + ('==' if len(S.g[S.x]) == S.deg_st else '≠') + f" `deg_st = {S.deg_st}` → " + ('==到达另一个角，第一行完成==' if len(S.g[S.x]) == S.deg_st else '继续往右')),
        'ans = [[]': '第一行长度 `{len(row)}`，所以一共 `n // len(row) = {n // len(row)}` 行',
        'ans[0] = row': '第一行填好：`ans[0] = {row}`',
        'for i in range(1, len(ans))': lambda S, B, r: ('所有行都构造完了' if getattr(B, 'i', None) == S.i else f"构造第 `{S.i}` 行"),
        'for x in ans[i - 1]': lambda S, B, r: ('上一行的格子都处理完了' if getattr(B, 'x', None) == S.x else f"上一行的 `x = {S.x}`：它正下方是谁？"),
        'if not vis[y]': lambda S, B, r: (f"`y = {S.y}`：" + ('已填过（在 x 的上、左、右）→ 跳过' if S.vis[S.y] else '==没填过 → 只会在 x 正下方==')),
        'vis[y] = True': '`{y}` 填在 `{B.x}` 正下方',
        'ans[i].append(y)': '第 `{i}` 行：`{ans[i]}`',
        'return ans': '矩阵完成：`{ans}`',
    },
    cards=dict(
        one_liner='像拼拼图：先拼好第一行，再靠已填的格子逐行推出下一行',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`edges` 描述一张 `n` 个点的无向图；要把 `0 ~ n-1` 填进矩阵',
                 '矩阵里上下左右相邻的格子 ==当且仅当== 在图中有边',
                 '本视频：`n=6` → `[[1,3],[5,0],[2,4]]`（任意一种合法答案）'],
        quote='回想一下怎么玩拼图。拼图的最外圈是比较容易完成的：先找角：找有两条直边的拼图块。再找边：找有一条直边的拼图块。',
        quote_src='—— 灵茶山艾府题解',
        idea=['度数 = 邻居数：角 2、边 3、内部 4（只有一行时端点 1）',
              '写法二：从度数最小的点出发，每步选度数最小的未访问邻居，直到再遇到同样度数的点 → 第一行',
              '下一行：`x` 的上左右都已访问，没访问的邻居只会在正下方'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '起点度数 `deg_st` 区分 1 列 / 2 列 / 多列，三种情况统一成一段代码',
                 '填下一行时只用 `vis`，不需要再判断方向',
                 '灵神还给了写法一：按度数 1/2/4 分类讨论，再用同样的逐行填法'],
    ),
)
