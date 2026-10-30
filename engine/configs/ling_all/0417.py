H = [[1, 3, 2], [4, 2, 1]]


def _reach(starts):
    m, n = len(H), len(H[0])
    seen = set()
    st = list(starts)
    while st:
        i, j = st.pop()
        if (i, j) in seen:
            continue
        seen.add((i, j))
        for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):
            if 0 <= x < m and 0 <= y < n and H[x][y] >= H[i][j]:
                st.append((x, y))
    return seen


_m, _n = len(H), len(H[0])
_P = _reach([(0, j) for j in range(_n)] + [(i, 0) for i in range(1, _m)])
_A = _reach([(_m - 1, j) for j in range(_n)] + [(i, _n - 1) for i in range(_m - 1)])


def _isA(S):
    return S['cells'][0][0] != 0


def _cell(S, i, j, v):
    vis = S.get('vis')
    if vis is None:
        return None
    if (i, j) == (S.get('i'), S.get('j')) and 'x' not in S:
        return 'yellow'
    if (i, j) in vis:
        return 'orange' if _isA(S) else 'blue'
    return None


def _cur(S):
    if 'vis' not in S:
        return '先建出两个洋的边界起点，再各做一次“逆流而上”的 DFS'
    who = '大西洋（下边界 + 右边界）' if _isA(S) else '太平洋（上边界 + 左边界）'
    return f'正在从 =={who}== 出发倒着往高处走，已到达 `{len(S["vis"])}` 格'


def _chk(S, B, ret):
    i, j, x, y = S.i, S.j, S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'枚举 `({i},{j})` 的邻居 `({x},{y})`：出界 → 不走'
    a, b = S.heights[x][y], S.heights[i][j]
    if a >= b:
        return f'邻居 `({x},{y})` 高度 `{a} >= {b}`：水能从它流到 `({i},{j})` → ==往高处走，继续 dfs=='
    return f'邻居 `({x},{y})` 高度 `{a} < {b}`：水流不到当前格 → 不走'


CONFIG = dict(
    num=417, title='太平洋大西洋水流问题', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='从边界出发 · 逆流而上 DFS + 取交集',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1900'],
    code='''
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        m, n = len(heights), len(heights[0])

        def search(cells: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
            def dfs(i: int, j: int) -> None:
                if (i, j) in vis:  # 避免重复访问，避免反复横跳无限递归
                    return
                vis.add((i, j))  # 标记 (i,j) 已访问
                for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):  # 枚举相邻格子
                    if 0 <= x < m and 0 <= y < n and heights[x][y] >= heights[i][j]:  # 往高处走
                        dfs(x, y)

            vis = set()
            for i, j in cells:
                dfs(i, j)
            return vis

        pacific = [(0, j) for j in range(n)] + [(i, 0) for i in range(1, m)]
        atlantic = [(m - 1, j) for j in range(n)] + [(i, n - 1) for i in range(m - 1)]
        return list(search(pacific) & search(atlantic))  # 交集即为答案
''',
    call=f'sorted(Solution().pacificAtlantic({H}))',
    setup='from typing import Set, Tuple',
    expect=sorted(_P & _A),
    views=[
        dict(type='text', fn=_cur, size=24, h=60),
        dict(type='grid', var='heights', label='heights（蓝/橙 = 本轮 DFS 已到达，黄 = 当前格）', cell=110, h=360, color=_cell),
        dict(type='calls', h=200),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'yellow'), ('j', lambda S: S['_inner'].get('j'), 'yellow')],
    captions={
        'm, n = len': '`m = {m}`、`n = {n}`：网格 {m} 行 {n} 列',
        'if (i, j) in vis': lambda S, B, r: (f'`({S.i},{S.j})` 已访问过 → ==直接返回==，否则会反复横跳无限递归' if (S.i, S.j) in B.vis
                                             else f'`({S.i},{S.j})` 还没访问过，继续'),
        'vis.add': '标记 `({i},{j})` 已访问：它能流到当前这个洋',
        'if 0 <= x < m': _chk,
        'dfs(x, y)': '往高处走一步：`dfs({x}, {y})`',
        'vis = set()': '每个洋各用一个新的 `vis`：本轮从边界出发能到的格子',
        'for i, j in cells': '依次从每个边界起点 `({i},{j})` 开始 dfs',
        'return vis': '这个洋的搜索结束，共 `{len(vis)}` 个格子能流进去',
        'pacific = ': '太平洋边界：上边界一行 + 左边界一列（`i` 从 1 起，避免角落重复）',
        'atlantic = ': '大西洋边界：下边界一行 + 右边界一列',
        'return list': lambda S, B, r: f'两个集合取交集：既通太平洋又通大西洋的格子共 `{len(r)}` 个 → `{r}`',
    },
    skip=['m, n = len', 'return vis', 'for i, j in cells', 'for x, y in', '                return', 'dfs(x, y)'],
    max_steps=64,
    cards=dict(
        result=f'两个集合取交集：太平洋 `{len(_P)}` 格 ∩ 大西洋 `{len(_A)}` 格 = `{len(_P & _A)}` 格 → ==`{sorted(_P & _A)}`==',
        one_liner='起点不明确、终点（边界）明确 → 从边界倒着往高处走',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`heights[r][c]` 是格子高度，水可流向高度 ==小于等于== 当前格的相邻格',
                 '左、上边界是太平洋，右、下边界是大西洋',
                 '求既能流到太平洋、又能流到大西洋的所有格子',
                 '本视频：`[[1,3,2],[4,2,1]]`'],
        quote='本题起点（答案）不明确，但终点（边界）明确，所以==从边界出发==能方便地找到答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['正着做要对每个格子都搜一遍；反过来：水往低处流 = ==从海边往高处走==',
              '从上、左边界出发的 DFS 访问到的格子 = 能流向太平洋的格子',
              '从下、右边界出发同理得到大西洋，最后==取交集=='],
        summary=['时间空间都是 `O(mn)`：每个格子在每个洋的搜索里至多访问一次',
                 '倒着走，所以条件是 `heights[x][y] >= heights[i][j]`（往高处走）',
                 '`vis` 先判断再标记，防止在相等高度的格子间反复横跳',
                 '边界列表写成 `range(1, m)` / `range(m - 1)`，避免角落重复',
                 '网格图 DFS 原理见 200. 岛屿数量'],
    ),
)
