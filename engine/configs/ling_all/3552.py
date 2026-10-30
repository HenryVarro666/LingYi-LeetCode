M = ["A..", ".A."]


def _mcol(S, i, j, v):
    if v == '#':
        return 'red'
    if v.isalpha():
        return 'purple'
    return None


CONFIG = dict(
    num=3552, title='网格传送门旅游', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='0-1 BFS（传送边权 0）',
    tags=['灵神题单', '网格图', '难度分 2036'],
    code='''
class Solution:
    def minMoves(self, matrix: List[str]) -> int:
        if matrix[-1][-1] == '#':
            return -1

        m, n = len(matrix), len(matrix[0])
        pos = defaultdict(list)
        for i, row in enumerate(matrix):
            for j, c in enumerate(row):
                if c.isupper():
                    pos[c].append((i, j))

        DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        dis = [[inf] * n for _ in range(m)]
        dis[0][0] = 0
        q = deque([(0, 0)])

        while q:
            x, y = q.popleft()
            d = dis[x][y]

            if x == m - 1 and y == n - 1:  # 到达终点
                return d

            c = matrix[x][y]
            if c in pos:
                # 使用所有传送门
                for px, py in pos[c]:
                    if d < dis[px][py]:
                        dis[px][py] = d
                        q.appendleft((px, py))
                del pos[c]  # 避免重复使用传送门

            # 下面代码和普通 BFS 是一样的
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] != '#' and d + 1 < dis[nx][ny]:
                    dis[nx][ny] = d + 1
                    q.append((nx, ny))

        return -1
''',
    call=f'Solution().minMoves({M})',
    expect=1,
    skip=['m, n = len', 'DIRS = ', 'for i, row in', 'for j, c in', 'if c.isupper', 'pos[c].append', 'q = deque', 'for dx, dy in DIRS', 'dis = [[inf]', 'if matrix[-1][-1]', 'nx, ny = x', 'd = dis[x][y]', 'c = matrix[x][y]'],
    views=[
        dict(type='grid', var=lambda S: [list(r) for r in S['matrix']] if 'matrix' in S else None, label='matrix（紫 = 传送门字母，红 = 障碍；蓝框 = 当前格，粉框 = 邻居/传送目标）',
             cell=90, h=220, color=_mcol,
             cursors=[('x', 'y', 'blue'), ('nx', 'ny', 'pink'), ('px', 'py', 'pink')]),
        dict(type='grid', var='dis', label='dis（到该格的最少移动次数）', cell=90, h=220,
             color=lambda S, i, j, v: None if v == float('inf') else 'green'),
        dict(type='queue', var='q', fmt=lambda p: f'({p[0]},{p[1]})', label='q（传送 0 边权入队首，走一步 1 边权入队尾）', h=120),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'blue'), ('d', 'd', 'green'), ('pos', 'pos', 'purple')],
    captions={
        'if matrix[-1][-1]': '终点是障碍物 → 永远到不了，直接 `-1`',
        'pos = defaultdict': '`pos[c]`：记录每个字母传送门的所有位置',
        'dis[0][0] = 0': '起点 `dis[0][0] = 0`，其余格子是 ∞',
        'while q': lambda S, B, r: ('队列非空，继续' if B.q else '队列空了还没到终点 → `-1`'),
        'x, y = q.popleft()': '取队首 `({x},{y})`：==队首 dis 最小==，已确定最少移动 `{dis[x][y]}` 次，格子是 `{matrix[x][y]}`',
        'if x == m - 1': lambda S, B, r: ('到达终点 → 最少移动 `{}` 次'.format(S.d) if S.x == S.m - 1 and S.y == S.n - 1 else f'`({S.x},{S.y})` 还不是终点'),
        'if c in pos': lambda S, B, r: (f'`{S.c}` 是还没用过的传送门 → 可以==免费传送== 到同字母的所有格子' if S.c in B.pos else (f'`{S.c}` 的传送门之前已经用过 → 不再传送' if S.c.isupper() else f'`{S.c}` 不是传送门，只能走路')),
        'if d < dis[px][py]': lambda S, B, r: (f'传送到 `({S.px},{S.py})`：边权 0，`{S.d} < {S.dis[S.px][S.py]}` → 更新' if S.d < B.dis[S.px][S.py] else f'`({S.px},{S.py})` 已经有不更大的 dis → 跳过'),
        'dis[px][py] = d': '传送过去不花步数：`dis[{px}][{py}] = {d}`',
        'q.appendleft': '边权 0 → ==加入队首==，马上处理',
        'del pos[c]': '这个字母的传送门用掉了：==删掉，避免重复使用==',
        'if 0 <= nx < m': lambda S, B, r: (f'邻居 `({S.nx},{S.ny})` 在界内、不是障碍，且 `{S.d} + 1 < {S.dis[S.nx][S.ny]}` → 走一步更近' if (0 <= S.nx < S.m and 0 <= S.ny < S.n and S.matrix[S.nx][S.ny] != '#' and S.d + 1 < S.dis[S.nx][S.ny]) else f'邻居 `({S.nx},{S.ny})` 越界 / 障碍 / 不会更近 → 跳过'),
        'dis[nx][ny] = d + 1': '走一步，边权 1：`dis[{nx}][{ny}] = {d} + 1 = {dis[nx][ny]}`',
        'q.append((nx, ny))': '边权 1 → 加入队尾',
        'return -1': '队列空了都没到终点 → `-1`',
    },
    max_steps=110,
    cards=dict(
        one_liner='同字母之间连一条边权 0 的边，相邻格子之间边权 1：0-1 BFS',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里 `.` 是空格，`#` 是障碍，大写字母是传送门',
                 '从左上角走到右下角，上下左右走一步算 1 次移动',
                 '踏入字母格可以免费传送到同字母的另一格，每个字母最多用一次',
                 '示例：`["A..",".A.","..."]` → `2`；本视频：`["A..",".A."]` → `1`'],
        quote='所有相同字母之间都有一条边权为 0 的边。所有相邻格子之间都有一条边权为 1 的边。这可以用 Dijkstra 算法解决。不过，对于边权只有 0 和 1 的特殊图，可以用 0-1 BFS（双端队列）解决，做到线性时间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['传送是边权 0，走路是边权 1：求最短路',
              '遇到字母格就把该字母所有位置以 0 边权入队首',
              '`del pos[c]`：用过就清空，既不重复传送，也保证线性时间'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '终点是 `#` 要先判断，直接返回 `-1`',
                 '传送门入队首（`appendleft`），走路入队尾（`append`）',
                 '传送后 `del pos[c]`，不清空会被反复传送，时间退化',
                 '前置题：2290（0-1 BFS）'],
    ),
)
