ORANGE = {1: 'orange', 2: 'red'}


def _scan(S, B, ret):
    v = S.grid[S.i][S.j]
    if v == 1:
        return f'`({S.i},{S.j})` 是好橘子 → 计数'
    if v == 2:
        return f'`({S.i},{S.j})` 不是好橘子，而是==已经腐烂的橘子=='
    return f'`({S.i},{S.j})` 是空格子'


def _bound(S, B, ret):
    x, y = S.x, S.y
    if 0 <= x < S.m and 0 <= y < S.n:
        return f'`({S.now_x},{S.now_y})` 的邻居 `({x},{y})` 在网格内，再看它是不是好橘子'
    return f'`({S.now_x},{S.now_y})` 的邻居 `({x},{y})` ==出界=='


def _good(S, B, ret):
    x, y = S.x, S.y
    v = S.grid[x][y]
    if v == 1:
        return f'`({x},{y})` 是==好橘子== → 被感染'
    if v == 2:
        return f'`({x},{y})` 已经烂了，跳过'
    return f'`({x},{y})` 是空格子，跳过'


CONFIG = dict(
    num=994, title='腐烂的橘子', difficulty='Medium', category='图论',
    author='yiduobo', technique='BFS 模拟扩散 · 按轮计数',
    code='''
class Solution(object):
    def orangesRotting(self, grid):
        q = []
        m = len(grid)
        n = len(grid[0])
        cnt = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    cnt += 1
                elif grid[i][j] == 2:
                    q.append([i, j])

        if cnt == 0:
            return 0

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        l, r = 0, len(q)
        step = 0
        while l < r:
            step += 1
            for now_x, now_y in q[l: r]:
                for index in range(4):
                    x = now_x + dx[index]
                    y = now_y + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        if grid[x][y] == 1:
                            q.append([x, y])
                            cnt -= 1
                            if cnt == 0:
                                return step
                            grid[x][y] = 2

            l, r = r, len(q)

        return -1
''',
    call='Solution().orangesRotting([[2, 1, 1], [1, 1, 0]])',
    expect=2,
    skip=['m = len(grid)', 'n = len(grid[0])', 'for j in range(n)', 'elif grid[i][j] == 2', 'dy = [1, 0',
          'for index in range(4)', 'x = now_x + dx', 'y = now_y + dy'],
    views=[
        dict(type='text', fn=lambda S: f"第 =={S['step']}== 轮　好橘子还剩 `cnt = {S['cnt']}`　橙 = 好橘子　红 = 烂橘子"
             if 'step' in S else '橙 = 好橘子 `1`　红 = 烂橘子 `2`', size=26),
        dict(type='grid', var='grid', cell=110, h=330,
             cursors=[('now_x', 'now_y', 'blue', '传染源'), ('x', 'y', 'yellow', '邻居')],
             color=lambda S, i, j, v: ORANGE.get(v)),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']],
             label='q（BFS 队列；[l, r) 是本轮要传染的橘子，灰 = 前几轮的）',
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', lambda S: S['r'] - 1),
             dim=lambda S, i, v: 'l' in S and i < S['l']),
    ],
    watch=[('step', 'step', 'green'), ('cnt', 'cnt', 'orange'), 'l', 'r'],
    captions={
        'q = []': '`q` 放烂橘子，`cnt` 数好橘子',
        'cnt = 0': '网格 `{m}` 行 `{n}` 列，`cnt = 0`',
        'for i in range(m)': lambda S, B, ret: f'扫描第 `{S.i}` 行' if B.get('i') != S.i or 'i' not in B else '扫描完毕',
        'if grid[i][j] == 1': _scan,
        'cnt += 1': '好橘子个数 `cnt` = {cnt}',
        'q.append([i, j])': '烂橘子 `({i},{j})` 作为 BFS 初始队列',
        14: lambda S, B, ret: '没有好橘子 → 直接返回 0' if S.cnt == 0 else f'有 `{S.cnt}` 个好橘子，需要 BFS 模拟（全是烂橘子或空格的话直接返回 0）',
        'dx = [': '`dx`、`dy` 表示右、下、左、上四个方向',
        'l, r = 0, len(q)': '`q[l:r]` 是==当前这一轮==要去传染别人的烂橘子：`[{l}, {r})`',
        'step = 0': '`step` 记录 BFS 进行到第几轮',
        'while l < r': lambda S, B, ret: (f'`l < r`（`{B.l} < {B.r}`）→ 还有烂橘子能传染，开始新的一轮' if B.l < B.r
                                          else '`l == r`：上一轮没有感染任何新橘子，BFS 结束'),
        'step += 1': '第 =={step}== 轮（第 {step} 分钟）',
        'for now_x, now_y in q[l: r]': lambda S, B, ret: (f'本轮的烂橘子 `({S.now_x},{S.now_y})` 去感染相邻的好橘子'
                                                          if (B.get('now_x'), B.get('now_y')) != (S.now_x, S.now_y)
                                                          or 'now_x' not in B else '本轮的烂橘子都传染完了'),
        'if x >= 0 and x < m': _bound,
        'if grid[x][y] == 1': _good,
        'q.append([x, y])': '`({x},{y})` 加入队尾，下一轮由它去传染',
        'cnt -= 1': '好橘子少一个：`cnt` = {cnt}',
        32: lambda S, B, ret: '`cnt == 0`：==最后一个好橘子也烂了==' if S.cnt == 0 else f'还剩 `{S.cnt}` 个好橘子，继续',
        'return step': '==好橘子数量变成 0==：当前轮次就是答案，立刻返回 `{ret}`',
        'grid[x][y] = 2': '`({x},{y})` 标记为烂橘子，以后不会再被重复感染',
        'l, r = r, len(q)': '这一轮结束：新入队的 `q[{l}:{r}]` 就是下一轮的烂橘子',
        'return -1': 'BFS 结束仍有好橘子 → 返回 -1',
    },
    max_steps=70,
    cards=dict(
        one_liner='BFS 一轮一轮地模拟腐烂扩散，好橘子数归零的那一轮就是答案',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`0` 空格子，`1` 新鲜橘子，`2` 烂橘子；每分钟烂橘子会传染上下左右的新鲜橘子',
                 '求所有橘子都烂掉的最少分钟数；不可能则返回 `-1`',
                 '本视频示例：`[[2,1,1],[1,1,0]]` → ==2=='],
        quote='初始化bfs队列为所有已经腐烂的橘子，接下来每一轮bfs都让这些腐烂的橘子感染相邻的好橘子。若某一轮好橘子的数量为0，那么当前bfs的轮次即为答案。',
        quote_src='—— yiduobo 题解',
        idea=['一开始就没有好橘子 → 直接返回 `0`',
              '`q[l:r]` 是==当前这一轮==的烂橘子，新感染的追加到队尾；一轮结束 `l, r = r, len(q)`',
              '感染时 `cnt -= 1`，==一旦归零就返回当前轮数==；BFS 跑完还有好橘子 → `-1`'],
        summary=['时间 `O(mn)`：每个橘子最多入队一次',
                 '`cnt == 0` 的提前判断不能省：否则全烂时会多进一轮或返回 `-1`',
                 '入队后立刻把格子改成 2，避免被重复感染、重复入队',
                 '用 `l, r` 两个下标在同一个列表上划分“轮”，不需要额外的 `tmp`',
                 '原文为 Python 2 风格，删去了 `"""type"""` 文档字符串'],
    ),
)
