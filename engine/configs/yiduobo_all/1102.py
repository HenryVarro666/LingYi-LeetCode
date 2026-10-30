GRID = [[5, 4, 5], [1, 6, 6]]


def _vis_cell(S, i, j, v):
    if 'vis' not in S:
        return None
    n = len(GRID[0])
    if (S.get('nowx'), S.get('nowy')) == (i, j) and S.get('_line', 0) >= 17:
        return 'blue'
    if i * n + j in S['vis']:
        return 'green'
    if any(e[1] == i and e[2] == j for e in S.get('heap', [])):
        return 'yellow'
    return None


def _top(S):
    if 'res' not in S:
        return '路径得分 = 路径上的最小值；贪心：每次走==当前可达里分数最高==的格子'
    return f"已访问 `{len(S.get('vis', []))}` 个格子，路径最小值 `res = {S['res']}`（绿 = 已访问，黄 = 在堆里，蓝 = 刚取出）"


CONFIG = dict(
    num=1102, title='得分最高的路径', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='贪心 · 大根堆扩展最高分格子',
    tags=['二分算法', '网格图'],
    code='''
class Solution(object):
    def maximumMinimumPath(self, grid):

        m = len(grid)
        n = len(grid[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        heap = [[-grid[0][0], 0, 0]]
        res = grid[0][0]
        vis = set()
        while m * n - 1 not in vis:
            d, nowx, nowy = heapq.heappop(heap)
            if nowx * n + nowy not in vis:
                vis.add(nowx * n + nowy)
                res = min(res, -d)
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if 0 <= x < m and 0 <= y < n and x * n + y not in vis:
                        heapq.heappush(heap, [-grid[x][y], x, y])
        
        return res
''',
    call=f'Solution().maximumMinimumPath({GRID})',
    expect=4,
    max_steps=75,
    skip=['m = len(grid)', 'n = len(grid[0])', 'dx = [', 'dy = [', 'for index in range(4)', 'x = nowx + dx'],
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='grid', var='grid', cursors=[('nowx', 'nowy', 'blue', '')], color=_vis_cell, h=260, cell=110),
        dict(type='heap', var='heap', fmt=lambda e: f'{-e[0]}@({e[1]},{e[2]})', h=240),
    ],
    watch=['nowx', 'nowy', 'd', 'x', 'y', ('res', 'res', 'green')],
    captions={
        'heap = [[': '大根堆（存负数模拟）：起点分数 `{grid[0][0]}`',
        'res = grid[0][0]': '`res`：路径最小值，起点本身 = `{res}`',
        'vis = set()': '`vis`：已访问的格子，编号 `x*n + y`',
        'while m * n - 1 not in vis': lambda S, B, r: ('右下角还没访问，继续扩展' if S.m * S.n - 1 not in S.vis else '右下角已访问 → 结束'),
        'heapq.heappop': '取出堆里分数最高的格子 `({nowx}, {nowy})`，分数 `{-d}`',
        'if nowx * n + nowy not in vis': lambda S, B, r: ('这个格子没访问过 → 访问它' if S.nowx * S.n + S.nowy not in S.vis else '堆里的旧记录，已访问过 → 跳过'),
        'vis.add': '标记 `({nowx}, {nowy})` 已访问',
        'res = min(res, -d)': '路径经过它：`res = min({B.res}, {-d}) = {res}`（贪心：每次取最高分，最小值只会被迫降低）',
        'y = nowy + dy': '邻居 `({x}, {y})`',
        'if 0 <= x < m': lambda S, B, r: (f'邻居 `({S.x}, {S.y})` 越界 → 跳过' if not (0 <= S.x < S.m and 0 <= S.y < S.n) else (f'邻居 `({S.x}, {S.y})` 已访问 → 跳过' if S.x * S.n + S.y in S.vis else f'邻居 `({S.x}, {S.y})` 分数 `{S.grid[S.x][S.y]}`，未访问 → 入堆')),
        'heapq.heappush': '`({x}, {y})` 入堆，分数 `{grid[x][y]}`',
        'return res': '右下角已被访问，最大的最小值 = `{res}`',
    },
    cards=dict(
        one_liner='每步选当前可达的最高分格子，直到走到右下角',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['网格 `grid`，从左上走到右下，每步上下左右，路径得分 = ==路径上的最小值==',
                 '求所有路径里得分的最大值',
                 '示例：`[[5,4,5],[1,2,6],[7,4,6]]` → `4`；本视频：`[[5,4,5],[1,6,6]]` → `4`'],
        quote='就是每一轮都选择当前可以到达的未访问过，且分数最高的节点，使用该节点的分数更新答案。重复此过程直到某一时刻到达右下角的节点为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['堆里放「已到达邻居」的格子，每次取分数最高的',
              '若最终路径经过它，选它没问题；不经过，答案也不会超过它',
              '访问时用它的分数压低 `res`，到右下角就结束'],
        summary=['时间 `O(mn log(mn))`，空间 `O(mn)`',
                 '原文是 Python 2 风格但无需改动，直接可在 Python 3 运行',
                 '堆存负分模拟大根堆；同一格可能多次入堆，取出时要判 `vis`',
                 '结束条件是==右下角被访问==，不是被入堆',
                 '同类解法：二分最小值 + BFS/DFS，或并查集按分数从大到小合并'],
    ),
)
