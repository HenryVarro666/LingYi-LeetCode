GRID = ["S..", ".B#", "..T"]

CONFIG = dict(
    num=1263, title='推箱子', difficulty='Hard', category='网格图',
    author='yiduobo', technique='双层 BFS（推箱子 + 人寻路）',
    tags=['灵神题单·网格图'],
    code='''
class Solution(object):
    def minPushBox(self, grid):

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 'T':
                    tx = i
                    ty = j
                elif grid[i][j] == 'B':
                    bx = i
                    by = j
                elif grid[i][j] == 'S':
                    px = i
                    py = j

        if bx == tx and by == ty:
            return 0

        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]

        near_pos = self.check_path(grid, m, n, bx, by, px, py, dx, dy)
        if len(near_pos) == 0:
            return -1
        
        used = [[[False] * 4 for _ in range(n)] for _ in range(m)]
        q = []
        for p in near_pos:
            used[bx][by][p] = True
            q.append([bx, by, p])

        l = 0
        r = len(q)
        res = 0
        while l < r:
            res += 1
            for bx, by, p in q[l : r]:
                next_bx = bx + dx[p]
                next_by = by + dy[p]
                if next_bx == tx and next_by == ty:
                    return res
                if next_bx >= 0 and next_bx < m and next_by >= 0 and next_by < n and grid[next_bx][next_by] != '#':
                    near_pos = self.check_path(grid, m, n, next_bx, next_by, bx, by, dx, dy)
                    for next_p in near_pos:
                        if not used[next_bx][next_by][next_p]:
                            used[next_bx][next_by][next_p] = True
                            q.append([next_bx, next_by, next_p])
            
            l, r = r, len(q)
        
        return -1

    def check_path(self, grid, m, n, bx, by, px, py, dx, dy):
        used = [[False] * n for _ in range(m)]
        used[px][py] = True
        used[bx][by] = True
        q = [[px, py]]
        l = 0
        r = 1
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] != '#' and not used[x][y]:
                    used[x][y] = True
                    q.append([x, y])
                    r += 1

        res = []
        for index in range(4):
            px = bx - dx[index]
            py = by - dy[index]
            if px >= 0 and px < m and py >= 0 and py < n and used[bx - dx[index]][by - dy[index]]:
                res.append(index)
        
        return res
''',
    call=f'Solution().minPushBox({GRID})',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"箱子在 `({S['bx']},{S['by']})`，目标 `({S['tx']},{S['ty']})`；已推 ==`{S['res']}`== 次" if 'tx' in S and 'bx' in S and 'res' in S and isinstance(S.get('res'), int) else ('先找人能走到箱子哪几侧' if 'tx' in S else '')), h=60),
        dict(type='grid', var='grid', cursors=[('bx', 'by', 'orange', '箱'), ('px', 'py', 'blue', '人起点')],
             color=lambda S, i, j, v: 'green' if v == 'T' else 'orange' if v == 'B' else 'pink' if v == 'S' else ('blue' if S.get('used') and S['used'][i][j] is True and v != '#' else None), h=300),
        dict(type='queue', var='q', fmt=lambda e: '(' + ','.join(map(str, e)) + ')', label='q（推箱子队列：箱x,箱y,人所在方向）', h=110),
    ],
    watch=[('res', 'res', 'yellow'), ('l', 'l'), ('r', 'r'), ('near_pos', 'near_pos', 'blue')],
    skip=['for i in range(m)', 'for j in range(n)', "if grid[i][j] ==", "elif grid[i][j] ==", 'tx = i', 'ty = j', 'bx = i', 'by = j', 'px = i', 'py = j',
          'dx = [', 'dy = [', 'm = len', 'n = len', 'l = 0', 'r = 1', 'r = len(q)', 'next_bx = bx', 'next_by = by',
          'used = [[False]', 'used[px][py]', 'used[bx][by] = True', 'q = [[px', 'nowx, nowy = q[l]', 'l += 1', 'for index in range(4)',
          62, 68, 'if px >= 0 and px < m', 'res.append(index)', 'used[bx][by][p] = True', 'used[next_bx][next_by][next_p] = True', 'for p in near_pos', 'for next_p in near_pos', 'x = nowx', 'y = nowy', 'used[x][y] = True', 'q.append([x, y])', 'r += 1', 'while l < r:\n', 'px = bx - dx', 'py = by - dy'],
    max_steps=110,
    captions={
        'if bx == tx and by == ty': '箱子起点已经在目标上吗？`({bx},{by})` vs `({tx},{ty})` → ==不在，需要推==',
        'near_pos = self.check_path(grid, m, n, bx, by, px, py': '（蓝色 = 人能走到的格子）先让人 BFS 寻路：人从 `({px},{py})` 出发，能走到箱子的哪几侧？结果 `near_pos = {near_pos}`（方向编号 0..3）',
        'if len(near_pos) == 0': lambda S, B, r: ('人到不了箱子旁边 → 一步也推不了，返回 `-1`' if not S.near_pos else f'`near_pos = {S.near_pos}` 非空：人能走到箱子旁边，可以开始推'),
        'used = [[[False] * 4': '`used[bx][by][p]`：箱子在 `(bx,by)`、人在方向 `p` 的那一侧，==状态 = 箱子位置 + 人的方向==',
        'used[bx][by][p] = True': '初始状态：箱子在 `({bx},{by})`，人可以站在方向 `{p}` 侧 → 入队',
        'q.append([bx, by, p])': '`q` 加入 `[{bx},{by},{p}]`',
        'res += 1': '==每一轮 BFS = 多推一次箱子==：现在第 `{res}` 次推',
        'for bx, by, p in q[l : r]': '遍历本轮状态：箱子 `({bx},{by})`、人在方向 `{p}` 侧，人往箱子方向推一格（取完则本轮结束）',
        'if next_bx == tx': lambda S, B, r: (f"推一格后箱子到 `({S.next_bx},{S.next_by})` = 目标 `({S.tx},{S.ty})`" if (S.next_bx, S.next_by) == (S.tx, S.ty) else f"推一格后箱子到 `({S.next_bx},{S.next_by})`，不是目标 `({S.tx},{S.ty})`"),
        43: '箱子到达目标，推了 `{res}` 次',
        'if next_bx >= 0': lambda S, B, r: (f"新位置 `({S.next_bx},{S.next_by})` 在界内且不是墙 → 箱子能被推过去" if (0 <= S.next_bx < S.m and 0 <= S.next_by < S.n and S.grid[S.next_bx][S.next_by] != '#') else f"新位置 `({S.next_bx},{S.next_by})` 越界或是墙 → 这一推不成立"),
        'near_pos = self.check_path(grid, m, n, next_bx': '推完后人站在箱子原来的位置 `({bx},{by})`，重新 BFS：人能走到新箱子位置的哪几侧？',
        'if not used[next_bx]': lambda S, B, r: (f"状态 `({S.next_bx},{S.next_by},方向{S.next_p})` 没来过 → 入队" if not S.used[S.next_bx][S.next_by][S.next_p] else f"状态 `({S.next_bx},{S.next_by},方向{S.next_p})` 已访问过 → 不再入队"),
        'used[next_bx][next_by][next_p] = True': '标记 `({next_bx},{next_by})` + 方向 `{next_p}` 已访问',
        'q.append([next_bx': '`q` 加入 `[{next_bx},{next_by},{next_p}]`，下一轮再推',
        'l, r = r, len(q)': '这一轮推完，下一轮处理 `q[{l}:{r}]`',
        'while l < r:': lambda S, B, r: f'`l < r`（{S.l} < {S.r}）：队列里还有没处理的状态' if S.l < S.r else f'`l = r`：队列空了，没推到目标',
        'res = []': '寻路 BFS 结束：蓝色格子是人（把箱子当墙）能走到的地方，再看箱子四侧哪些在蓝色里',
        'if px >= 0 and px < m': lambda S, B, r: (f"箱子 `({S.bx},{S.by})` 的方向 `{S.index}` 侧 `({S.px},{S.py})`：" + ('==人能走到== → 记入结果' if (0 <= S.px < S.m and 0 <= S.py < S.n and S.used[S.px][S.py]) else '走不到或越界')),
        'res.append(index)': '`res = {res}`：这些方向都可以作为推箱子的起点',
        80: '返回人能站到的方向 `{res}`',
    },
    cards=dict(
        one_liner='箱子位置 + 人在哪一侧 = 状态；推一次 = BFS 一层，人怎么走过去另用一次 BFS',
        complexity='时间 `O(m·n·4·m·n)`，空间 `O(m·n)`',
        problem=['网格里 `S` 是人，`B` 是箱子，`T` 是目标，`#` 是墙',
                 '人可以走到相邻空格，也可以==向箱子推一格==（人站在箱子反面）',
                 '求把箱子推到 `T` 的最少推动次数，做不到返回 `-1`',
                 '本视频示例：`["S..",".B#","..T"]` → `2`'],
        quote='我在这里采用的是最朴素的bfs，令状态(x, y, 0)到(x, y, 3)分别表示箱子在位置(x, y)，人在箱子的上、下、左、右四个相邻位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案只统计「推」的次数，人走路不计数 → ==外层 BFS 一层 = 推一次==',
              '推箱子要求人站在箱子反面：先用 `check_path` BFS 判断人能否走到箱子某一侧（箱子本身当墙）',
              '推完后人站在箱子原来的位置，再 `check_path` 求出新状态，去重后入队'],
        summary=['外层状态 `m·n·4`，每个状态做一次 `O(mn)` 寻路，总体 `O((mn)^2)`',
                 '易错点：寻路时箱子视为障碍（`used[bx][by] = True`）',
                 '易错点：答案是推动次数，不是人走的总步数；推完后人在箱子的旧位置',
                 '原文本身已是 Python 3 可运行的写法，代码未做修改；作者提到可用启发式搜索 + 割点优化，这里只演示朴素 BFS'],
    ),
)
