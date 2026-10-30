G = [[2, 4, 3, 5], [5, 4, 9, 3], [3, 4, 2, 11]]


def _lst(S, k):
    if k not in S:
        return []
    try:
        return list(S[k])
    except Exception:
        return []


def _col(S, i, j, v):
    if 'j' not in S:
        return None
    jj = S['j']
    ln = S.get('_line', 0)
    if ln in (7, 8, 9):
        # 刚进入这一列：q 就是这一列的出发点
        if j == jj and i in _lst(S, 'q'):
            return 'blue'
        return None
    if j == jj and i in _lst(S, 'tmp'):
        return 'blue'
    if j == jj + 1 and i in _lst(S, 'q'):
        return 'green'
    return None


def _nb(S, B, r):
    i, k, j = B.i, B.k, B.j
    if not (0 <= k < B.m):
        return f'`k = {k}` 出界，跳过'
    a, b = B.grid[k][j + 1], B.grid[i][j]
    if a <= b:
        return f'右边 `grid[{k}][{j+1}] = {a}` 不大于 `grid[{i}][{j}] = {b}` → 不能走'
    if B.vis[k] == j:
        return f'`grid[{k}][{j+1}] = {a} > {b}` 能走，但这格本轮已入队过（`vis[{k}] == {j}`）→ ==不重复入队=='
    return f'`grid[{k}][{j+1}] = {a} > {b}` 能走，而且之前没入队 → ==入队=='


CONFIG = dict(
    num=2684, title='矩阵中移动的最大次数', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格图 BFS（双数组，一列一轮）',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1626'],
    code='''
class Solution:
    def maxMoves(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        vis = [-1] * m
        q = range(m)
        for j in range(n - 1):
            tmp = q
            q = []
            for i in tmp:
                for k in i - 1, i, i + 1:
                    if 0 <= k < m and vis[k] != j and grid[k][j + 1] > grid[i][j]:
                        vis[k] = j  # 第 k 行目前最右访问到了 j
                        q.append(k)
            if not q:  # 无法再往右走了
                return j
        return n - 1
''',
    call=f'Solution().maxMoves({G})',
    expect=3,
    skip=['m, n = len', 'q = []', 'for k in i - 1'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 本轮从这些格出发，绿 = 能走到的下一列格子）', cell=96, h=330,
             color=_col, cursors=[('i if _line in (10, 11, 12) else None', 'j', 'yellow'),
                                  ('k if _line in (11, 12, 13) else None', 'j + 1', 'pink')]),
        dict(type='array', var=lambda S: _lst(S, 'q') if S.get('_line', 0) not in (8, 9) else _lst(S, 'q'),
             label='q（当前这一列能到达的行号）', cell=70, h=130),
        dict(type='array', var='vis', label='vis[k]：第 k 行最近一次入队时的列号（-1 = 还没有）', cell=70, h=130),
    ],
    watch=[('j', 'j', 'blue'), ('i', 'i'), ('k', 'k', 'pink'), ('q', 'list(q)', 'green')],
    captions={
        'vis = [-1] * m': '`vis[k]` 记录第 `k` 行最近一次入队的列号，用来去重；初始 `-1`',
        'q = range(m)': '第 0 列的每一行都是出发点：`q = [0, 1, ..., m-1]`',
        'for j in range(n - 1)': lambda S, B, r: (f'一轮处理一列：从第 `{S.j}` 列的出发点，看第 `{S.j+1}` 列能走到哪些行' if S.j != B.get('j')
                                                  else '`j` 已枚举到 `n - 2`，每一列都走通了，循环结束'),
        'tmp = q': '`tmp` 是本列的出发行 `{list(tmp)}`，`q` 清空，准备装下一列能到的行',
        'for i in tmp': lambda S, B, r: (f'取出发行 `i = {S.i}`，当前值 `grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}`' if S.i != B.get('i') or S.get('j') != B.get('j') or S.tmp != B.get('tmp')
                                         else f'这一列的出发行 `{list(S.tmp)}` 都处理完了'),
        'if 0 <= k < m': _nb,
        'vis[k] = j': '标记第 `{k}` 行在这一轮已入队：多个出发点指向同一格时只算一次',
        'q.append(k)': '`q` 加入行 `{k}`：下一列的出发点 `{q}`',
        'if not q': lambda S, B, r: (f'`q` 空了：右边一列哪里都走不到 → 最多走到第 `{S.j}` 列，答案 ==`{S.j}`==' if not S.q
                                     else f'`q = {S.q}` 非空：还能继续往右走，进入下一列'),
        'return n - 1': '一直走到了最后一列：移动次数 = 列数 - 1 = =={n - 1}==',
    },
    cards=dict(
        one_liner='一列一列往右扩：每列只记“哪些行能到”，不用逐条路径',
        complexity='时间 `O(mn)`，空间 `O(m)`',
        problem=['`m × n` 正整数矩阵，可从第 0 列任意格出发',
                 '每步只能走到右上 / 右 / 右下，且==值严格更大==的格子',
                 '求最多能移动几次',
                 '示例：`[[2,4,3,5],[5,4,9,3],[3,4,2,11]]` → `3`'],
        quote='一开始把所有 (i,0) 都加入一个列表。每一轮循环，遍历列表中的坐标，把右边这一列的能到达的格子坐标加入一个新列表。注意只有之前没入队的格子才能入队，可以用一个 vis 数组。',
        quote_src='—— 灵茶山艾府题解（方法二：网格图 BFS）',
        idea=['每走一步列号 +1，所以 BFS 一轮正好推进一列',
              '`q` 只存行号：这一列里能到达的行',
              '多个出发点会走到同一格，用 `vis[k] = j` 去重',
              '某轮 `q` 为空 → 走不动了，答案就是当前列号 `j`'],
        summary=['时间 `O(mn)`：每格至多入队一次；空间 `O(m)`',
                 '易错：`vis` 要先于 `append` 标记，否则同一格重复入队',
                 '`q` 空时返回的是 `j`（已走到的最右列），走完整网格返回 `n - 1`',
                 '另有两种写法：DFS 把走过的格子置 0 当 vis；原地把入队格取反省掉 `vis`'],
    ),
)
