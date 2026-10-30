G0 = [[1, 0, 0], [0, 0, 2]]


def _cell(S, i, j, v):
    if G0[i][j] == 1:
        return 'green'
    if G0[i][j] == 2:
        return 'pink'
    if v == -1 and G0[i][j] == 0:
        return 'orange'
    return None


def _cap_if(S, B, ret):
    x, y, left = S.x, S.y, S.left
    m, n, grid = S.m, S.n, S.grid
    if x < 0 or x >= m or y < 0 or y >= n:
        return f'`({x},{y})` ==出界== → 不合法，返回 0'
    if grid[x][y] < 0:
        return f'`({x},{y})` 是障碍或==已走过== → 不合法，返回 0'
    return f'`({x},{y})` 在界内且可走，继续（还需访问 `left = {left}` 个格子）'


CONFIG = dict(
    num=980, title='不同路径 III', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='网格回溯 + 恢复现场',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 1830'],
    code='''
class Solution:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def dfs(x: int, y: int, left: int) -> int:
            if x < 0 or x >= m or y < 0 or y >= n or grid[x][y] < 0:
                return 0  # 不合法
            if grid[x][y] == 2:  # 到达终点
                return left == 0  # 必须访问所有的无障碍方格
            grid[x][y] = -1  # 标记成访问过，因为题目要求「不能重复通过同一个方格」
            ans = dfs(x - 1, y, left - 1) + dfs(x, y - 1, left - 1) + \\
                  dfs(x + 1, y, left - 1) + dfs(x, y + 1, left - 1)
            grid[x][y] = 0  # 恢复现场
            return ans

        cnt0 = sum(row.count(0) for row in grid)
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                if v == 1:  # 起点
                    return dfs(i, j, cnt0 + 1)  # +1 把起点也算上
''',
    call=f'Solution().uniquePathsIII({G0})',
    expect=1,
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 起点，粉 = 终点，橙 = 已走过，蓝框 = 当前位置）', cell=110, h=300,
             color=_cell, cursors=[(lambda S: S['_inner'].get('x'), lambda S: S['_inner'].get('y'), 'blue')]),
        dict(type='text', size=28, h=60,
             fn=lambda S: (f"当前 `dfs({S['_inner']['x']}, {S['_inner']['y']}, left={S['_inner']['left']})`：还要走 `{S['_inner']['left']}` 格"
                           if 'x' in S['_inner'] and 'left' in S['_inner'] else '`left` = 还没访问的无障碍方格数（含起点、不含终点）')),
        dict(type='calls', h=230),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('y', lambda S: S['_inner'].get('y'), 'blue'),
           ('left', lambda S: S['_inner'].get('left'), 'yellow'), 'cnt0'],
    skip=['m, n = len(grid)', 'for i, row in enumerate', 'for j, v in enumerate', 'return 0  # 不合法'],
    captions={
        'cnt0 = sum': '数一数无障碍的空格：`cnt0 = {cnt0}`；路径要把它们和起点全走一遍',
        'if x < 0 or x >= m': _cap_if,
        'if grid[x][y] == 2': lambda S, B, ret: (f'`({S.x},{S.y})` 是终点：此时 `left = {S.left}`，'
                                                 + ('==恰好为 0== → 所有格子都走过了' if S.left == 0
                                                    else '==还没走完== → 这条路径不算')
                                                 if S.grid[S.x][S.y] == 2 else f'`({S.x},{S.y})` 不是终点，继续往下走'),
        'return left == 0': lambda S, B, ret: ('终点且 `left == 0` → 找到 ==1 条合法路径==，返回 1' if ret else '终点但 `left ≠ 0` → 没走完，返回 0'),
        'grid[x][y] = -1': '标记 `({x},{y})` 已走过（改成 -1），下面几层不能再踩它',
        'ans = dfs': '向上、左、下、右四个方向递归，累加合法路径数：`ans = {ans}`',
        'dfs(x + 1, y, left - 1) + dfs': '换下、右两个方向继续试，累加到 `ans`',
        'grid[x][y] = 0': '==恢复现场==：`({x},{y})` 改回 0，让别的路径还能走它',
        'return ans': '四个方向都试完，从 `({x},{y})` 出发共 `{ans}` 条路径 → 回到上一层',
        'return dfs(i, j': '找到起点 `({i},{j})`，从这里开始搜：`dfs({i}, {j}, {cnt0 + 1})`',
    },
    max_steps=50,
    cards=dict(
        one_liner='走过就标记成 -1，回来再恢复；终点处看 left 是否为 0',
        complexity='时间 `O(3^(mn))`，空间 `O(mn)`',
        problem=['网格里 `1` 是起点，`2` 是终点，`0` 可走，`-1` 是障碍',
                 '上下左右走，求起点到终点的路径数',
                 '要求==每个无障碍方格恰好走一次==（含起点和终点）',
                 '本视频：`[[1,0,0],[0,0,2]]` → `1`'],
        quote='把 grid[x][y] 改成 -1，表示这个格子访问过，在返回前改回 0（恢复现场）。',
        quote_src='—— 灵茶山艾府题解（方法一：回溯）',
        idea=['`dfs(x, y, left)`：从 `(x,y)` 出发，还剩 `left` 个格子要走',
              '每走一步 `left - 1`；到终点时 `left == 0` 才算走遍',
              '用 `-1` 标记走过的格子，退出时改回 `0`，避免重复经过'],
        result='只有 1 条路径能走遍所有格子 ✓',
        summary=['时间 `O(3^(mn))`（除了第一步，每步至多 3 个方向），实际远小于上界',
                 '`left` 初始是 `cnt0 + 1`：+1 是把起点也算上',
                 '易错：途中碰到终点必须 `left == 0` 才算，否则返回 0',
                 '题解还给了方法二：用 `vis` 位掩码代替改网格，配合 `@cache` 记忆化',
                 '同类题：79. 单词搜索'],
    ),
)
