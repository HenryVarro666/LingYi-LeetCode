G = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]


def _nb(S, B, r):
    x, y = B.x, B.y
    m, n = B.m, B.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` 越界，不计数'
    if B.grid[x][y] != B.origin:
        return f'邻居 `({x},{y})` 颜色 `{B.grid[x][y]}` ≠ 原色 `{B.origin}`，不在连通分量里'
    if (x, y) == (B.r0, B.c0):
        return f'邻居 `({x},{y})` 是起点（同色）→ `used` 变成 =={B.used[x][y] + 1}==，其中 1 是开头预记的，最后减掉'
    return f'邻居 `({x},{y})` 同色 → 它被看到一次：`used[{x}][{y}]` = =={B.used[x][y] + 1}=='


def _used(S, i, j, v):
    if 'used' not in S:
        return None
    return 'green' if v >= 4 else ('yellow' if v > 0 else None)


CONFIG = dict(
    num=1034, title='边框着色', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS 数被访问次数',
    tags=['灵神核心路线', '灵神题单·网格图'],
    code='''
class Solution(object):
    def colorBorder(self, grid, r0, c0, color):

        origin = grid[r0][c0]
        q = [[r0, c0]]
        l = 0
        r = 1
        m = len(grid)
        n = len(grid[0])
        used = [[0] * n for _ in range(m)]
        used[r0][c0] = 1
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == origin:
                    used[x][y] += 1
                    if used[x][y] == 1:
                        q.append([x, y])
                        r += 1
        
        used[r0][c0] -= 1

        for x, y in q:
            if used[x][y] < 4:
                grid[x][y] = color
        
        return grid
''',
    call=f'Solution().colorBorder({G}, 1, 1, 2)',
    expect=[[0, 2, 0], [2, 1, 2], [0, 2, 0]],
    skip=['l = 0', 'r = 1', 'm = len', 'n = len', 'dx = [', 'dy = [', 'l += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'q.append', 'r += 1'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（粉色 = 已染成新颜色；蓝框 = 出队格，黄框 = 正在数的邻居）', cell=84, h=250,
             color=lambda S, i, j, v: 'pink' if 'color' in S and v == S['color'] and S.get('l', 0) and S.get('_line', 0) >= 30 else None,
             cursors=[('nowx', 'nowy', 'blue'), ('x if _line in (20, 21, 22) else None', 'y', 'yellow')]),
        dict(type='grid', var='used', label='used（被看到的次数；满 4 次 = 内部格，变绿）', cell=84, h=250, color=_used),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队，l 指向下一个）', cell=70, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=120),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('origin', 'origin')],
    captions={
        'origin = grid': '记下起点 `({r0},{c0})` 的原色 `origin = {origin}`，连通分量就是与它同色且相连的格子',
        'q = [[r0, c0]]': '起点入队，用数组 + `l`、`r` 做队列',
        'used = [[0]': '`used` 记录每个格子在 BFS 中被“看到”几次',
        'used[r0][c0] = 1': '起点先记 1 次：它是第一个入队的，没有谁“看到”它，后面要补偿',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续' if B.l < B.r else f'`l == r = {B.r}`：整个连通分量遍历完'),
        'nowx, nowy = q[l]': '出队 `({nowx},{nowy})`，看它的四个邻居：内部格四周必然全是同色',
        'if x >= 0 and x < m': _nb,
        'used[x][y] += 1': '`used[{x}][{y}]` 加 1：每个同色邻居都会“看到”它一次，内部格会被看满 ==4 次==',
        'if used[x][y] == 1': lambda S, B, r: (f'第一次被看到 → 入队，`({S.x},{S.y})` 进入连通分量' if S.used[S.x][S.y] == 1
                                              else f'已经是第 {S.used[S.x][S.y]} 次看到，已在队里，不重复入队'),
        'used[r0][c0] -= 1': '起点开头多记了 1 次，这里减回去，保证所有格子“被看次数”口径一致',
        'for x, y in q': '遍历连通分量的每个格子',
        'if used[x][y] < 4': lambda S, B, r: (f'`({S.x},{S.y})` 被看到 `{S.used[S.x][S.y]}` < 4 次：有邻居不同色或出界 → ==边框=='
                                              if S.used[S.x][S.y] < 4 else f'`({S.x},{S.y})` 被看到 4 次：四周全同色 → 内部格，不染'),
        'grid[x][y] = color': '边框格染成 `color = {color}`',
        'return grid': '返回染色后的 `grid`',
    },
    cards=dict(
        one_liner='内部格四周全同色：BFS 里被看到 4 次，不足 4 次就是边框',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给 `grid` 和起点 `(r0, c0)`，起点所在的==连通分量==（同色、四方向相连）',
                 '把该连通分量的==边框==染成 `color`，内部不变',
                 '边框格：在网格边缘，或上下左右有不同色的格子',
                 '示例：十字形 `[[0,1,0],[1,1,1],[0,1,0]]`，从 `(1,1)` 染成 `2`'],
        quote='对于连通分量的任意内部区域(x, y)而言，其四周必然与(x, y)同色。那么按照普通bfs计算连通分量，内部区域将被访问到4次，而非内部区域则不足4次。',
        quote_src='—— yiduobo 题解原文',
        idea=['直接判断边框麻烦，换成判断“内部”：四周全同色',
              'BFS 时每个同色邻居都给该格计数 +1，记在 `used`',
              '内部格恰好被看 4 次，边框格不足 4 次',
              'BFS 完，对计数 < 4 的格子染色即可'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：起点没有“发现者”，初始记 1 后最后要 `-= 1` 补偿',
                 '必须先统计完再染色，染色会改变 `grid` 的颜色而影响判断',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
