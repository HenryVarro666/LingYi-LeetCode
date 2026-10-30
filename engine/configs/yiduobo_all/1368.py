G = [[2, 1, 1], [4, 4, 1]]
ARROW = {1: '→', 2: '←', 3: '↓', 4: '↑'}


def _arrows(S):
    return [[ARROW[v] for v in row] for row in S['grid']] if 'grid' in S else None


def _col(S, i, j, v):
    u = S.get('used')
    if not u:
        return None
    return 'green' if u[i][j] else None


def _new(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'`({x},{y})` 出界，不能走'
    if B.used[x][y]:
        return f'`({x},{y})` 已经可以到达，不重复加入'
    return f'`({x},{y})` 还没到过 → ==顺着箭头走到它，免费加入队列=='


def _new2(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.m and 0 <= y < S.n):
        return f'`({x},{y})` 出界，不能走'
    if B.used[x][y]:
        return f'`({x},{y})` 已经可以到达，跳过'
    return f'`({x},{y})` 没到过 → ==花 1 改箭头方向，就能走到它=='


CONFIG = dict(
    num=1368, title='使网格图至少有一条有效路径的最小代价', difficulty='Hard', category='网格图',
    author='yiduobo', technique='按修改次数分轮的 BFS',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def minCost(self, grid):

        m = len(grid)
        n = len(grid[0])
        used = [[False] * n for _ in range(m)]
        used[0][0] = True

        q = [[0, 0]]
        l = 0
        r = 1
        dx = [0, 0, 0, 1, -1]
        dy = [0, 1, -1, 0, 0]
        res = 0
        while not used[-1][-1]:
            last_l = l
            while l < r:
                nowx, nowy = q[l]
                l += 1
                d = grid[nowx][nowy]
                x = nowx + dx[d]
                y = nowy + dy[d]
                if x >= 0 and x < m and y >= 0 and y < n and not used[x][y]:
                    q.append([x, y])
                    used[x][y] = True
                    if used[-1][-1]:
                        return res
                    r += 1

            res += 1

            new_r = r
            for nowx, nowy in q[last_l : r]:
                for index in range(1, 5):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and not used[x][y]:
                        q.append([x, y])
                        used[x][y] = True
                        if used[-1][-1]:
                            return res
                        new_r += 1
            
            r = new_r

        return res
''',
    call=f'Solution().minCost({G})',
    expect=2,
    skip=['m = len', 'n = len', 'used = [[', 'used[0][0] = True', 'l = 0', 'r = 1', 'dx = [', 'dy = [', 'res = 0',
          'last_l = l', 'l += 1', 'r += 1', 'new_r = r', 'q.append', 'for index in range(1, 5)', 'x = nowx', 'y = nowy',
          'q = [[0, 0]]'],
    views=[
        dict(type='grid', var=_arrows, label='箭头 = 每格的方向（1→ 2← 3↓ 4↑）；绿 = 已能到达', cell=100, h=280,
             color=_col, cursors=[('nowx', 'nowy', 'blue'), ('x', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队；每轮结尾追加的是「改一次箭头」才能到的格子）', cell=80, h=170,
             dim=lambda S, i, v: i < S.get('l', 0), pointers={'l': 'blue', 'r': 'orange'}),
    ],
    watch=[('res（已改次数）', 'res', 'green'), ('l', 'l', 'blue'), ('r', 'r', 'orange'), ('d', 'd', 'yellow')],
    captions={
        'while not used[-1][-1]': lambda S, B, r: ('终点还没到过，继续' if not B.used[-1][-1] else '终点已经到过了，结束'),
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：这一轮还有格子要顺箭头走' if B.l < B.r
                                        else '这一轮顺箭头能走的都走完了，还没到终点 → ==需要多改一次箭头=='),
        'nowx, nowy = q[l]': '出队 `({nowx},{nowy})`：不修改，只顺着它的箭头走（免费）',
        'd = grid[nowx][nowy]': '这一格的方向 `d = {d}` → {["", "向右", "向左", "向下", "向上"][d]}',
        23: _new,
        'used[x][y] = True': '标记 `used[{x}][{y}]`',
        'if used[-1][-1]': lambda S, B, r: ('到达右下角 → 返回当前修改次数 `res`' if S.used[-1][-1] else '还没到终点'),
        'res += 1': '免费能走的走完了 → 再允许改一次箭头：`res = {res}`',
        'for nowx, nowy in q': '枚举这一轮新加入的格子 `q[last_l:r]`，改它的箭头，让它指向四个邻居之一（代价 1）',
        37: _new2,
        'r = new_r': '下一轮的起点 = 刚才花 1 到达的格子；`r` 扩到 `{r}`',
        'return res': '一共修改了 `{res}` 次箭头',
    },
    max_steps=120,
    cards=dict(
        one_liner='先免费顺箭头走，走不动再花 1 改一个箭头，分轮向外扩',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['每格有箭头：`1` 右、`2` 左、`3` 下、`4` 上，走到格子必须按它的箭头出发',
                 '每个格子的箭头只能改一次，每次修改代价 `1`，改成任意方向',
                 '求让左上角到右下角至少有一条有效路径的最小代价',
                 '本视频：`[[2,1,1],[4,4,1]]` → `2`（题面原文没有给出，这里按 LeetCode 原题补充）'],
        quote='若可以到达右下角，那么答案就是0。接下来，考虑修改一个网格的情况。此时显然应该修改上一步队列中格子相邻的位置，这样才能有效地扩展可以到达的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['修改 0 次：从起点顺着箭头 BFS，找出所有免费可达的格子',
              '修改 1 次：只需考察上一轮新加入格子的邻居（旧的早处理过了）',
              '每轮先顺箭头 BFS 扩展，没到终点就 `res += 1` 再来一轮'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '`dx`、`dy` 的 0 号位是占位，让 `d=1..4` 直接对应方向',
                 '易错：改箭头时只处理上一轮新加入的 `q[last_l:r]`，不要重复枚举',
                 '原文为 Python 2 风格，但在 Python 3 下无需修改，代码原样运行',
                 '最短路角度：顺箭头边权 0，改箭头边权 1，等价于 0-1 BFS'],
    ),
)
