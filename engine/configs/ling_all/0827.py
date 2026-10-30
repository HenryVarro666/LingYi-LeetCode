_PAL = ['green', 'pink', 'purple', 'cyan', 'orange']


def _col(S, i, j, v):
    if v >= 2:
        return _PAL[(v - 2) % len(_PAL)]
    return None


def _cur(S, k):
    return S['_inner'].get(k)


CONFIG = dict(
    num=827, title='最大人工岛', difficulty='Hard', category='网格图',
    author='灵茶山艾府', technique='DFS 给岛编号 + 集合去重',
    tags=['灵神题单', '网格图', '难度分 1934'],
    code='''
class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        def dfs(i: int, j: int) -> int:
            size = 1
            grid[i][j] = len(area) + 2  # 记录 (i,j) 属于哪个岛
            for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if 0 <= x < n and 0 <= y < n and grid[x][y] == 1:
                    size += dfs(x, y)
            return size

        # DFS 每个岛，统计各个岛的面积，记录到 area 列表中
        area = []
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x == 1:
                    area.append(dfs(i, j))

        # 加上这个特判，可以快很多
        if not area:  # 没有岛
            return 1

        ans = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x: continue
                s = set()
                for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    if 0 <= x < n and 0 <= y < n and grid[x][y]:
                        s.add(grid[x][y])  # 记录上下左右格子所属岛屿编号
                ans = max(ans, sum(area[idx - 2] for idx in s) + 1)  # 累加面积

        # 如果最后 ans 仍然为 0，说明所有格子都是 1，返回 n^2
        return ans if ans else n * n
''',
    call='Solution().largestIsland([[1,1,0],[1,0,1],[0,0,0]])',
    expect=5,
    skip=['n = len(grid)', 'def dfs', 'area = []', 'for i, row in enumerate', 'for j, x in enumerate', 'ans = 0', 7, 28, 16, 26],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（1 = 未编号的陆地；≥2 = 岛屿编号，同色同岛）', cell=92, h=300,
             color=_col, cursors=[('i', 'j', 'yellow', '')]),
        dict(type='array', var='area', label='area（下标 + 2 = 岛屿编号）', cell=70, h=130),
        dict(type='set', var=lambda S: S.get('s') if S['_line'] >= 21 else None, label='s（当前 0 格周围的岛编号，自动去重）', h=110),
        dict(type='calls', h=130),
    ],
    watch=[('ans', 'ans', 'green'), ('size', "_inner.get('size')", 'blue')],
    captions={
        'size = 1': '先算上自己这一格：`size = 1`',
        'grid[i][j] = len(area)': '给 `({i},{j})` 写上岛编号 `{len(area) + 2}`（`area` 长度 + 2）：既当访问标记，又记下属于哪个岛',
        'if 0 <= x < n and 0 <= y < n and grid[x][y] == 1': lambda S, B, r: (
            f'邻居 `({S.x},{S.y})` 出界' if not (0 <= S.x < S.n and 0 <= S.y < S.n)
            else f'邻居 `({S.x},{S.y})` 是 `{S.grid[S.x][S.y]}`：' + ('==未编号的陆地 → 递归 DFS==' if S.grid[S.x][S.y] == 1 else '不是未访问的 1 → 不走')),
        'size += dfs': '邻居那一片的面积加进来：`size = {size}`',
        'return size': '这一格往下的面积是 `{size}`，返回给上一层',
        'area.append': '`({i},{j})` 是 1：发现新岛，DFS 量面积；当前 `area = {area}`，新岛编号 `{len(area) + 2}`',
        'if not area': '`area` 不空，说明有岛，不用特判返回 1',
        'if x: continue': lambda S, B, r: (f'`({S.i},{S.j})` 是 `{S.x}`：已经是陆地，不用填' if S.x else f'`({S.i},{S.j})` 是水 → 假设把它填成陆地'),
        's = set()': '`({i},{j})` 是水 → 假设填成陆地；用集合收集周围岛的编号，==同一个岛只记一次==',
        'if 0 <= x < n and 0 <= y < n and grid[x][y]:': lambda S, B, r: (
            f'邻居 `({S.x},{S.y})` 出界' if not (0 <= S.x < S.n and 0 <= S.y < S.n)
            else f'邻居 `({S.x},{S.y})` 是 `{S.grid[S.x][S.y]}`：' + ('==有岛，记下编号==' if S.grid[S.x][S.y] else '是水 → 不管')),
        's.add': lambda S, B, r: (f'岛编号 `{S.grid[S.x][S.y]}` 已经在 `s` 里 → ==集合去重，不重复统计==，`s = {S.s}`' if S.grid[S.x][S.y] in B.s
                                  else f'岛编号 `{S.grid[S.x][S.y]}` 加入 `s`，现在 `s = {S.s}`'),
        'ans = max': lambda S, B, r: f'`s = {S.s or "空集"}`：面积 = ' + ''.join(f'`{S.area[k-2]}` + ' for k in sorted(S.s)) + f'1（自己） = =={sum(S.area[k-2] for k in S.s) + 1}==，`ans = {S.ans}`',
        'return ans if ans': '`ans = {ans}` 不为 0，直接返回',
    },
    cards=dict(
        one_liner='先给每个岛编号并量面积，再逐个把水变成陆地，编号去重后累加',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`n x n` 的 0/1 网格，最多把一个 0 变成 1',
                 '求操作后最大的岛屿面积',
                 '示例：`[[1,1,0],[1,0,1],[0,0,1]]` → `5`'],
        quote='把上下左右的岛（如果有）的编号去重后，累加去重后的这些岛的面积。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 数出每个岛的面积放进 `area`，同时把岛编号写回 `grid`',
              '遍历每个 0：上下左右的岛编号放进集合去重',
              '答案 = 去重后各岛面积之和 + 1（这格自己）'],
        summary=['时间 `O(n^2)`，每格最多看 4 个邻居',
                 '易错：不去重会把同一个岛算两次（示例里 `(1,1)` 的上、左是同一个岛）',
                 '编号从 2 开始，避免和原来的 0/1 混淆；全是 0 返回 1，全是 1 返回 `n*n`',
                 '同类：695 岛屿的最大面积'],
    ),
)
