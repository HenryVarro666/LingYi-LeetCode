IMG = [[1, 2, 0, 3], [0, 3, 0, 4], [6, 0, 3, 0]]
KK = 3
M, N = 3, 4


def _islands():
    seen, out = set(), []
    for i in range(M):
        for j in range(N):
            if IMG[i][j] and (i, j) not in seen:
                st, cells = [(i, j)], []
                seen.add((i, j))
                while st:
                    x, y = st.pop()
                    cells.append((x, y))
                    for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= a < M and 0 <= b < N and IMG[a][b] and (a, b) not in seen:
                            seen.add((a, b))
                            st.append((a, b))
                out.append(cells)
    return out


ISL = _islands()
ISL_OF = {c: k for k, cells in enumerate(ISL) for c in cells}
ISL_SUM = [sum(IMG[x][y] for x, y in cells) for cells in ISL]


def _cur(S):
    """正在 BFS 的岛编号（岛内扫描中为编号，否则 None）"""
    I = S['_inner']
    if 13 <= S['_line'] <= 28 and 'i' in I:
        return ISL_OF.get((I['i'], I['j']))
    return None


def _color(S, i, j, v):
    if IMG[i][j] == 0:
        return None
    if v != 0:
        return 'blue'
    k = ISL_OF[(i, j)]
    if k == _cur(S):
        return 'yellow'
    return 'green' if ISL_SUM[k] % KK == 0 else 'red'


def _info(S):
    k = _cur(S)
    if k is None:
        return f'绿 = 总价值是 `{KK}` 的倍数的岛　红 = 不是　蓝 = 未访问陆地　　已数到 ==`{S.get("res", 0)}`== 个'
    got = sum(IMG[x][y] for x, y in ISL[k] if S['grid'][x][y] == 0)
    return f'黄 = 当前岛，已并入的格子之和 ==`{got}`==　　已数到 ==`{S.get("res", 0)}`== 个'


CONFIG = dict(
    num=3619, title='总价值可以被 K 整除的岛屿数目', difficulty='Medium', category='网格图',
    author='yiduobo', technique='floodfill（BFS）· 顺便累加岛屿价值',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1461'],
    code='''
class Solution(object):
    def countIslands(self, grid, k):
        
        res = 0
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j]:
                    s = grid[i][j]
                    grid[i][j] = 0
                    q = [(i, j)]
                    head, tail = 0, 1
                    while head < tail:
                        for x, y in q[head : tail]:
                            for d in range(4):
                                xx = x + dx[d]
                                yy = y + dy[d]
                                if 0 <= xx < m and 0 <= yy < n and grid[xx][yy] > 0:
                                    s += grid[xx][yy]
                                    grid[xx][yy] = 0
                                    q.append((xx, yy))
                        
                        head, tail = tail, len(q)
                    
                    if s % k == 0:
                        res += 1
        
        return res
''',
    call=f'Solution().countIslands({IMG}, {KK})',
    expect=3,
    skip=['res = 0', 'dx = [', 'dy = [', 'm = len', 'n = len', 'for i in range', 'for j in range', 'if grid[i][j]:',
          'for d in range', 'xx = x', 'yy = y', 'if 0 <= xx', 'head, tail = 0, 1'],
    views=[
        dict(type='text', fn=_info, size=22),
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '起点'), ('x if 18 <= _line <= 28 else None', 'y', 'pink', '出队')], cell=92, h=300,
             color=_color),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S and S['_line'] >= 15 else None,
             label='q（暗 = 已处理，head 指向本层开头）', cell=70, pointers={'head': 'blue', 'tail': 'pink'},
             dim=lambda S, i, v: i < S.get('head', 0), h=170),
    ],
    watch=[('res', 'res', 'green'), ('s', 's', 'yellow'), ('k', 'k'), ('head', 'head', 'blue'), ('tail', 'tail', 'pink')],
    captions={
        's = grid[i][j]': '`({i},{j})` 是没访问的陆地 → ==发现新岛==！`s` 记它的价值 `{s}`',
        'grid[i][j] = 0': '起点置 `0`：入队前就标记，==防止被重复入队==',
        'q = [(i, j)]': '起点入队，开始 floodfill（BFS 一层一层向外扩）',
        'while head < tail': lambda S, B, r: (f'`head = {S.head} < tail = {S.tail}`：这一层还有格子，继续扩'
                                              if S.head < S.tail else '这一层没有新格子了 → 整座岛找完了'),
        'for x, y in q': lambda S, B, r: (f'`({S.x},{S.y})` 的四个邻居看完了：新的陆地都已并入、入队'
                                          if B.get('x') == S.x and B.get('y') == S.y and B.get('head') == S.head else
                                          f'处理 `q[{S.head}:{S.tail}]` 这一层：出队 `({S.x},{S.y})`，看右、下、左、上四个邻居'),
        's += grid[xx][yy]': '邻居 `({xx},{yy})` 在界内且是陆地 → 价值 `{grid[xx][yy]}` 并入：`s = {s}`',
        'grid[xx][yy] = 0': '邻居置 `0` 标记访问过，随后入队',
        'q.append': '`({xx},{yy})` 入队，等下一层再向外扩',
        'head, tail = tail': lambda S, B, r: f'进入下一层：`head, tail = {S.head}, {S.tail}`',
        'if s % k': lambda S, B, r: (f'整座岛价值 `s = {S.s}`，`{S.s} % {S.k} = {S.s % S.k}` → ==整除==，岛屿数加一'
                                     if S.s % S.k == 0 else f'整座岛价值 `s = {S.s}`，`{S.s} % {S.k} = {S.s % S.k}` ≠ 0 → ==不整除==，不计'),
        'res += 1': '`res = {res}`：这座岛合格',
        'return res': '扫描结束，总价值能被 `k` 整除的岛有 ==`{ret}`== 座',
    },
    max_steps=110,
    cards=dict(
        one_liner='套 200 题的 floodfill，找岛的同时累加价值',
        complexity='时间 `O(mn)`，空间 `O(mn)`（队列）',
        problem=['`m×n` 矩阵，正整数是陆地，上下左右相连的陆地组成岛屿',
                 '岛屿总价值 = 所有格子值之和，求能被 `k` 整除的岛屿数',
                 '本视频示例：3×4 网格，`k = 3` → ==3=='],
        quote='找岛屿相关的问题，可以直接照搬之前200题的处理方法，利用floodfill来寻找矩阵中的岛屿。……在这个过程中顺便计算岛屿的总价值，然后判断其是否可以被k整除即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层逐格扫描，碰到值大于 0 的格子就是新岛的起点',
              '用数组 `q` 做队列 BFS：每层 `q[head:tail]`，四个方向扩展',
              '格子进队时就置 `0`，同时 `s += 它的值`',
              'BFS 结束后判断 `s % k == 0`，是就 `res += 1`'],
        result='运行结束，返回 `3`：总价值 6、6、3 的岛能被 3 整除，总价值 7 的不能',
        summary=['时间 `O(mn)`：每格入队一次；空间 `O(mn)`',
                 '易错：入队时就要置 `0`，出队再置会重复入队、重复累加',
                 '`head, tail = tail, len(q)` 用双下标一层层推进，没有用 deque',
                 '会修改输入 `grid`；原文代码未改动（本来就是 Python 3 可运行）'],
    ),
)
