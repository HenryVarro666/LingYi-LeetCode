M0 = [[1, 3, 2], [4, 2, 1]]


def _color(S, i, j, v):
    f = S.get('f')
    if f is None:
        return None
    if (i, j) == (S['_inner'].get('nowx'), S['_inner'].get('nowy')):
        return 'yellow'
    return {1: 'blue', 2: 'orange', 3: 'green'}.get(f[i][j])


def _chk(S, B, r):
    nx, ny, x, y = S.nowx, S.nowy, S.x, S.y
    mat = S.matrix
    p = f'`({nx},{ny})` 的邻居 '
    if not (0 <= x < len(mat) and 0 <= y < len(mat[0])):
        return p + f'`({x},{y})` 出界 → 跳过'
    if S.used[x][y]:
        return p + f'`({x},{y})` 本轮已经访问过（`used`）→ 跳过，防止重复搜索'
    a, b = mat[x][y], mat[nx][ny]
    if a >= b:
        return p + f'`({x},{y})` 高度 `{a} >= {b}`：水能从它流向 `({nx},{ny})` → ==染上这个大洋的标记=='
    return p + f'`({x},{y})` 高度 `{a} < {b}`：水流不到当前点 → 跳过'


def _val(S):
    v = S['_inner'].get('val')
    return v


CONFIG = dict(
    num=417, title='太平洋大西洋水流问题', difficulty='Medium', category='网格图',
    author='yiduobo', technique='两次 DFS 种子染色 · 位标记 1 / 2 / 3',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1900'],
    code='''
class Solution(object):
    def pacificAtlantic(self, matrix):

        if not matrix:
            return []

        m = len(matrix)
        n = len(matrix[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        f = [[0] * n for _ in range(m)]

        used = [[False] * n for _ in range(m)]
        for index in range(m):
            f[index][0] |= 1
            used[index][0] = True
        for index in range(n):
            f[0][index] |= 1
            used[0][index] = True

        for index in range(1, m):
            self.dfs(index, 0, used, matrix, 1, f, dx, dy)
        for index in range(1, n):
            self.dfs(0, index, used, matrix, 1, f, dx, dy)

        used = [[False] * n for _ in range(m)]
        for index in range(m):
            f[index][n - 1] |= 2
            used[index][n - 1] = True
        for index in range(n):
            f[m - 1][index] |= 2
            used[m - 1][index] = True
        
        for index in range(m - 1):
            self.dfs(index, n - 1, used, matrix, 2, f, dx, dy)
        for index in range(n - 1):
            self.dfs(m - 1, index, used, matrix, 2, f, dx, dy)

        res = []
        for i in range(m):
            for j in range(n):
                if f[i][j] == 3:
                    res.append([i, j])
        return res

    def dfs(self, nowx, nowy, used, matrix, val, f, dx, dy):
        for index in range(4):
            x = nowx + dx[index]
            y = nowy + dy[index]
            if x >= 0 and x < len(matrix) and y >= 0 and y < len(matrix[0]) and not used[x][y] and matrix[x][y] >= matrix[nowx][nowy]:
                f[x][y] |= val
                used[x][y] = True
                self.dfs(x, y, used, matrix, val, f, dx, dy)
''',
    call=f'Solution().pacificAtlantic({M0})',
    expect=[[0, 1], [0, 2], [1, 0]],
    views=[
        dict(type='text', fn=lambda S: '`f` 的位标记：`1` 通太平洋（蓝），`2` 通大西洋（橙），`3` 两个都通（绿）', size=24, h=60),
        dict(type='grid', var='matrix', label='matrix（颜色 = f 的值，黄 = 当前 DFS 所在点）', cell=110, h=270, color=_color),
        dict(type='grid', var='f', label='f（0 = 哪个都不通）', cell=80, h=230),
        dict(type='calls', h=170, hide=('pacificAtlantic',)),
    ],
    watch=[('val', _val, 'cyan')],
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'for index in range(m)', 'for index in range(n)',
          'for index in range(1', 'for index in range(m - 1)', 'for index in range(n - 1)', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'used[index][0] = True', 'used[0][index] = True',
          'used[index][n - 1] = True', 'used[m - 1][index] = True', 'f[x][y] |= val', 'used[x][y] = True',
          'for i in range(m)', 'for j in range(n)', 'if not matrix', 'return []'],
    captions={
        'f = [[0] * n': '`f[i][j]` 用二进制位记录：能到太平洋或上 `1`，能到大西洋或上 `2`',
        'used = [[False]': lambda S, B, r: ('`used` 记录这一轮 DFS 有没有走过' if 'used' not in B else '==`used` 重新清空==：大西洋这一轮要重新走，不能沿用太平洋的标记'),
        'f[index][0] |= 1': '左边界 `({index},0)` 紧贴太平洋：`f` 或上 `1`',
        'f[0][index] |= 1': '上边界 `(0,{index})` 紧贴太平洋：`f` 或上 `1`',
        'self.dfs(index, 0, used, matrix, 1': '从左边界 `({index},0)` 出发，往高处染 `1`',
        'self.dfs(0, index, used, matrix, 1': '从上边界 `(0,{index})` 出发，往高处染 `1`',
        'f[index][n - 1] |= 2': '右边界 `({index},{n - 1})` 紧贴大西洋：`f` 或上 `2`',
        'f[m - 1][index] |= 2': '下边界 `({m - 1},{index})` 紧贴大西洋：`f` 或上 `2`',
        'self.dfs(index, n - 1, used, matrix, 2': '从右边界 `({index},{n - 1})` 出发，往高处染 `2`',
        'self.dfs(m - 1, index, used, matrix, 2': '从下边界 `({m - 1},{index})` 出发，往高处染 `2`',
        'res = []': '两次染色完成，下面找 `f == 3` 的点',
        'if f[i][j] == 3': lambda S, B, r: (f'`f[{S.i}][{S.j}] = {S.f[S.i][S.j]}` = 3：两个大洋都能到 → ==加入答案==' if S.f[S.i][S.j] == 3
                                           else f'`f[{S.i}][{S.j}] = {S.f[S.i][S.j]}` ≠ 3 → 不是答案'),
        'if x >= 0 and x < len': _chk,
        'self.dfs(x, y': '递归染色：从 `({x},{y})` 继续往高处走',
        'return res': '`f == 3` 的点就是答案：`{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='做两次 DFS 染色：通太平洋 |= 1，通大西洋 |= 2，值为 3 就是答案',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['矩阵 `matrix` 表示高度，水可以流向高度 ==不高于== 当前格的相邻格',
                 '左、上是太平洋，右、下是大西洋',
                 '求既能流到太平洋、又能流到大西洋的所有格子',
                 '本视频：`[[1,3,2],[4,2,1]]`'],
        quote='为了方便起见，对地图上能到太平洋的点或上1，能到大西洋的点或上2，那么最后值为3的点就能同时到两个大洋了。',
        quote_src='—— yiduobo 题解原文',
        idea=['分别从太平洋、大西洋的边界出发，做“种子染色法”的 DFS',
              '倒着走，只往 ==高度不低于当前点== 的邻居扩散',
              '用位运算合并两次结果：`f` 里是 3 的点两个洋都能到'],
        summary=['时间空间 `O(mn)`：每个格子每轮最多染一次',
                 '第二轮前要把 `used` 重新清空，否则第二个大洋无法搜索',
                 '倒着走，条件是 `matrix[x][y] >= matrix[nowx][nowy]`',
                 '原文是 Python 2 风格，在 Python 3 下无需改动即可运行',
                 '对比灵神：他每个洋用一个 `vis` 集合再取交集；这里一个 `f` 数组用位标记'],
    ),
)
