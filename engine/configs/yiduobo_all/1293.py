GRID = [[0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [1, 1, 0, 0]]


def _color(S, i, j, v):
    if 'f' not in S:
        return None
    if any(S['f'][i][j]):
        return 'green'
    return None


def _chk(S, B, r):
    x, y, m, n = B.x, B.y, B.m, B.n
    if not (0 <= x < m and 0 <= y < n):
        return f'`({x},{y})` 越界 → 不走'
    s = B.nows + B.grid[x][y]
    if B.grid[x][y]:
        tip = f'`({x},{y})` 是障碍，消除数变 `{s}`'
    else:
        tip = f'`({x},{y})` 是空地，消除数仍 `{s}`'
    if s > B.k:
        return tip + f' ==超过 k = {B.k}== → 不走'
    return tip + ' ≤ k，继续看是否访问过'


CONFIG = dict(
    num=1293, title='网格中的最短路径', difficulty='Hard', category='网格图',
    author='yiduobo', technique='BFS · 状态带上已消除障碍数',
    tags=[],
    code='''
class Solution(object):
    def shortestPath(self, grid, k):

        m = len(grid)
        n = len(grid[0])
        if m == 1 and n == 1:
            return 0
        f = [[[False] * (k + 1) for j in range(n)] for i in range(m)]
        q = [[0, 0, 0]]
        f[0][0][0] = True
        l = 0
        r = 1
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        res = 0
        while l < r:
            res += 1
            for nowx, nowy, nows in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        s = nows + grid[x][y]
                        if s <= k and not f[x][y][s]:
                            f[x][y][s] = True
                            q.append([x, y, s])
                            if x == m - 1 and y == n - 1:
                                return res

            l, r = r, len(q)

        return -1
''',
    call=f'Solution().shortestPath({GRID}, 1)',
    expect=6,
    skip=['m = len', 'n = len', 'l = 0', 'r = 1', 'dx = [', 'dy = [', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'if m == 1', 'f = [['],
    views=[
        dict(type='grid', var='grid', label='grid（1 = 障碍；绿 = 以某个消除数到达过；蓝 = 出队；粉 = 邻居）', cell=96, h=380,
             color=_color, cursors=[('nowx', 'nowy', 'blue'), ('x if _line >= 19 else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a}{b}{c}' for a, b, c in S['q']] if 'q' in S else None,
             label='q：x y s 连写（s = 已消除障碍数），暗 = 已处理', cell=84, h=190,
             dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('res（轮数=步数）', 'res', 'green'), ('l', 'l', 'blue'), ('r', 'r'), ('k', 'k', 'orange'), ('nows', 'nows')],
    captions={
        'q = [[0, 0, 0]]': '起点入队：状态 `(x, y, s)`，==s 是路上已经消除的障碍数==，起点 `(0,0,0)`',
        'f[0][0][0] = True': '`f[x][y][s]` 标记「带着 s 个消除数到过 (x,y)」，同一格不同 s 是不同状态',
        'while l < r': lambda S, B, r: (f'队列 `[l, r) = [{B.l}, {B.r})` 是==当前这一轮==的状态，继续' if B.l < B.r else '队列空了仍没到终点 → 返回 -1'),
        'res += 1': '新开一轮，所有状态再走一步：`res` = {res}',
        'for nowx, nowy, nows': '取出状态 `({nowx},{nowy})`，已消除 `{nows}` 个障碍',
        'if x >= 0 and x < m': lambda S, B, r: ('`(%d,%d)` 出界 → 跳过' % (S.x, S.y)) if not (0 <= S.x < S.m and 0 <= S.y < S.n) else '`(%d,%d)` 在地图内' % (S.x, S.y),
        's = nows + grid[x][y]': '走到 `({x},{y})`：消除数 = `{nows} + {grid[x][y]}` = =={s}==（障碍格 +1）',
        'if s <= k and not f': lambda S, B, r: (f'`s = {S.s}` 超过 `k = {S.k}` → 不能再消除，放弃' if S.s > S.k else
                                                (f'状态 `({S.x},{S.y},{S.s})` 已到过 → 放弃，BFS 先到的更短' if S.f[S.x][S.y][S.s] else f'`s = {S.s} ≤ k` 且没到过 → ==新状态==')),
        'f[x][y][s] = True': '入队前先标记，避免重复入队',
        'q.append': '`({x},{y},{s})` 入队，下一轮再扩展',
        'if x == m - 1': lambda S, B, r: ('==到达右下角=='
                                         if (S.x == S.m - 1 and S.y == S.n - 1) else f'`({S.x},{S.y})` 还不是右下角 `({S.m-1},{S.n-1})`'),
        'return res': '第一次走到右下角就是最短：==当前轮数 `{res}`==',
        'l, r = r, len(q)': '一轮结束：`[l, r)` 换成刚入队的新状态，`l = {l}`，`r = {r}`',
        'return -1': '没走到右下角 → `-1`',
    },
    cards=dict(
        one_liner='BFS 的状态多记一维：已经消除了几个障碍',
        complexity='时间 `O(mnk)`，空间 `O(mnk)`',
        problem=['`m × n` 的网格，0 是空地，1 是障碍，从左上角走到右下角',
                 '每步走上下左右一格，==最多可以消除 k 个障碍==（走进障碍格算消除一个）',
                 '求最短步数，走不到返回 `-1`',
                 '本视频：4×4 的网格，`k = 1` → `6`'],
        quote='令f[x][y][s]表示走到位置(x, y)，过程中消除了s个障碍的最短路径长度，那么我们可以从f[0][0][0]开始，每次尝试往四个方向走。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态 `(x, y, s)`：位置加已消除的障碍数，用 `f` 标记是否到过',
              '走到障碍格 `s + 1`，若 `s <= k` 且没到过才入队',
              '每一轮 BFS 就是多走一步，==第一次到右下角的轮数==就是答案'],
        summary=['时间、空间都是 `O(mnk)`：每个 `(x, y, s)` 最多入队一次',
                 '`q[l : r]` 是当前这一轮，轮末 `l, r = r, len(q)` 切到下一轮',
                 '易错：起点 `(0,0)` 若 `m == n == 1` 要直接返回 0',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改'],
    ),
)
