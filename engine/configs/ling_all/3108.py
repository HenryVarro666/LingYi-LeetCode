N0 = 5
E0 = [[0, 1, 7], [1, 2, 1], [3, 4, 6]]
Q0 = [[0, 2], [2, 3]]
POS = {0: (0.08, 0.25), 1: (0.32, 0.55), 2: (0.12, 0.88), 3: (0.68, 0.25), 4: (0.92, 0.75)}
COLS = ['blue', 'orange', 'green', 'purple']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ids = S.get('ids')
    line = S.get('_line', 0)
    indfs = 'and_' in S and 'y' in S and 'w' in S and line in (11, 12, 13, 14) and ids is not None
    cur = S.get('x') if indfs or (ids is not None and line in (10, 11, 15) and 'and_' in S) else None
    W, H = x1 - x0 - 80, y1 - y0 - 110
    P = {k: (x0 + 40 + v[0] * W, y0 + 60 + v[1] * H) for k, v in POS.items()}
    cv.text((x0 + 18, y0 + 4), '带权无向图（颜色 = 连通块编号，黄边 = 正在走的边，黄圈 = 当前 dfs 的点）', 22, T['muted'], bold=True)
    for u, v, w in E0:
        hot = indfs and {S['x'], S['y']} == {u, v}
        c = T['yellow'] if hot else T['border']
        cv.line([P[u], P[v]], c, 6 if hot else 3)
        mx, my = (P[u][0] + P[v][0]) / 2, (P[u][1] + P[v][1]) / 2
        cv.rect((mx - 20, my - 16, mx + 20, my + 16), fill=T['panel2'], r=8)
        cv.text((mx, my), w, 24, T['yellow'] if hot else T['text'], anchor='mm', bold=True, mono=True)
    for k, (px, py) in P.items():
        cid = ids[k] if ids is not None else -1
        fill = T[COLS[cid % 4]] if cid >= 0 else T['panel2']
        if k == cur:
            cv.rect((px - 40, py - 40, px + 40, py + 40), outline=T['yellow'], width=5, r=40)
        cv.rect((px - 32, py - 32, px + 32, py + 32), fill=fill, outline=T['border'], r=32)
        cv.text((px, py), k, 32, T['bg'] if cid >= 0 else T['muted'], anchor='mm', bold=True, mono=True)


def _and(S):
    if 'and_' not in S or S.get('_line') in (19, 20, 21, 23, 24):
        cc = S.get('cc_and')
        return ('各连通块边权 AND：' + '，'.join(f'块 {i} = {v}' for i, v in enumerate(cc))) if cc else ''
    return f"本块当前 AND = ==`{S['and_']}`==（初值 -1 = 全 1，不改变任何数）"


CONFIG = dict(
    num=3108, title='带权图里旅途的最小代价', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='DFS 求连通块 + 块内边权 AND',
    tags=['灵神题单·位运算', '灵神题单·图论算法', '难度分 2109'],
    code='''
class Solution:
    def minimumCost(self, n: int, edges: List[List[int]], query: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))

        def dfs(x: int) -> int:
            and_ = -1
            ids[x] = len(cc_and)  # 记录每个点所在连通块的编号
            for y, w in g[x]:
                and_ &= w
                if ids[y] < 0:  # 没有访问过
                    and_ &= dfs(y)
            return and_

        ids = [-1] * n  # 记录每个点所在连通块的编号
        cc_and = []  # 记录每个连通块的边权的 AND
        for i in range(n):
            if ids[i] < 0:
                cc_and.append(dfs(i))

        return [-1 if ids[s] != ids[t] else cc_and[ids[s]]
                for s, t in query]
''',
    call=f'Solution().minimumCost({N0}, {E0}, {Q0})',
    expect=[1, -1],
    skip=['g[x].append', 'g[y].append', 'for x, y, w in edges', 'g = [[]', 'for i in range(n)'],
    max_steps=90,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='ids', label='ids（每个点所在连通块，-1 = 没访问）', h=150, cell=70),
        dict(type='text', fn=_and, size=26, h=60),
        dict(type='calls', h=150),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink'), ('and_', 'and_', 'orange'), ('cc_and', 'cc_and', 'green')],
    captions={
        'and_ = -1': '`and_` 初值 `-1`：二进制全是 1，和任何数 AND 都等于那个数',
        'ids[x] =': '点 `{x}` 归入连通块 `{ids[x]}`',
        'for y, w in g[x]': lambda S, B, r: f'走点 `{S.x}` 的邻边：到 `{S.y}`，边权 `{S.w}`',
        'and_ &= w': '这条边必须走（AND 的数越多结果越小）：`and_` = {B.and_} & {w} = =={and_}==',
        'if ids[y] < 0': lambda S, B, r: (f'`ids[{S.y}] = -1`：没访问过 → 递归进去' if S.ids[S.y] < 0
                                         else f'`ids[{S.y}] = {S.ids[S.y]}`：访问过 → 不递归'),
        'and_ &= dfs(y)': '把下游子树里所有边权的 AND 并进来：`and_` → =={and_}==',
        'return and_': '这棵子树的边权 AND = =={and_}==',
        'ids = [-1]': '`ids[i] = -1` 表示没访问',
        'if ids[i] < 0': lambda S, B, r: (f'点 `{S.i}` 没访问过 → 新的连通块，从它 dfs' if S.ids[S.i] < 0
                                         else f'点 `{S.i}` 已经属于块 `{S.ids[S.i]}` → 跳过'),
        'cc_and.append': '块 `{len(cc_and)-1}` 的边权 AND = =={cc_and[-1]}==',
        'for s, t in query': lambda S, B, r: (f'查询 `({S.s}, {S.t})`：' + (f'点 `{S.s}` 在块 {S.ids[S.s]}，点 `{S.t}` 在块 {S.ids[S.t]} → 不连通，答案 -1' if S.ids[S.s] != S.ids[S.t]
                                                else f'同在块 {S.ids[S.s]} → 答案 = 块内 AND = ==`{S.cc_and[S.ids[S.s]]}`==')),
        'return [-1': lambda S, B, r: (f'全部查询的答案：`{r}`' if r is not None else '用推导式逐个回答查询'),
    },
    cards=dict(
        one_liner='边可以重复走：走遍整个连通块的边，AND 最小',
        complexity='时间 `O(n+m+q)`，空间 `O(n+m)`',
        problem=['带权无向图，一趟旅途的代价 = 经过的边权按位与',
                 '边和点可以重复经过，每次查询求 `s` 到 `t` 的最小代价，不连通为 `-1`',
                 '示例：`n=5, edges=[[0,1,7],[1,3,7],[1,2,1]]` → `[1,-1]`',
                 '本视频：5 个点、两个连通块，查询 `[[0,2],[2,3]]` → `[1,-1]`'],
        quote='AND 的性质是 AND 的数字越多，结果越小。在可以重复经过边的前提下，最优方案是把 s 所在连通块内的边都走一遍。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s`、`t` 不连通 → `-1`',
              '连通：能走遍块内所有边（走过去再走回来不影响 AND）',
              '所以答案 = 块内所有边权的 AND，DFS 一次求出每块的 AND',
              'AND 的初值取 `-1`（全 1）'],
        summary=['时间 `O(n+m+q)`，空间 `O(n+m)`',
                 '`and_` 初值必须是 `-1`，不能是 0',
                 '无向边每条会被两端各看一次，AND 重复无妨',
                 '孤立点 `s=t` 时块内无边，AND 仍是初值 `-1`，需留意',
                 '题解还给了并查集写法，同样是维护每个集合的边权 AND'],
    ),
)
