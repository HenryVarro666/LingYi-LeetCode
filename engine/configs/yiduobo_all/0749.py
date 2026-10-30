GRID = [[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]
DX = [1, 0, -1, 0]
DY = [0, 1, 0, -1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S['grid']
    m, n = len(g), len(g[0])
    walls = S.get('walls')
    cv.text((x0 + 18, y0 + 4), 'grid（红 = 已感染；橙线 = 防火墙；黄 = 将被感染；粉 = 威胁最大的那块）', 22, T['muted'], bold=True)
    cell = min(110, (x1 - x0 - 60) / n, (y1 - y0 - 80) / m)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    sy = y0 + 54
    targets = S.get('target') or []
    mp = S.get('max_target_pos')
    tcol = {}
    for k, t in enumerate(targets):
        for c in t:
            tcol[c] = 'pink' if k == mp else 'yellow'
    cur = None
    if 'virius' in S and S['virius'] and S.get('_line', 0) <= 53:
        cur = set(map(tuple, S['virius'][-1]))
    for i in range(m):
        for j in range(n):
            X, Y = sx + j * cell, sy + i * cell
            infected = g[i][j] == 1
            fill = T['red'] if infected else T['panel2']
            if (i, j) in tcol and not infected:
                fill = T[tcol[(i, j)]]
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=8, outline=T['pink'] if (cur and (i, j) in cur) else T['border'],
                    width=4 if (cur and (i, j) in cur) else 1)
            cv.text((X + cell / 2, Y + cell / 2), g[i][j], 34, T['bg'] if (infected or (i, j) in tcol) else T['muted'], anchor='mm', bold=True, mono=True)
    if walls:
        for i in range(m):
            for j in range(n):
                for d in range(4):
                    if walls[i][j] & (1 << d):
                        # 墙在 (i,j) 靠近病毒（反方向）的那条边
                        X, Y = sx + j * cell, sy + i * cell
                        if d == 0:
                            seg = [(X, Y), (X + cell, Y)]
                        elif d == 1:
                            seg = [(X, Y), (X, Y + cell)]
                        elif d == 2:
                            seg = [(X, Y + cell), (X + cell, Y + cell)]
                        else:
                            seg = [(X + cell, Y), (X + cell, Y + cell)]
                        cv.line(seg, T['orange'], 8)


def _txt(S):
    if 'rnd' not in S:
        return ''
    return f"第 `{S['rnd']}` 轮；已筑墙 ==`{S['res']}`== 面"


def _blk(S, B, r):
    k = len(S.target) - 1
    return f'第 `{k + 1}` 块病毒：{len(S.virius[-1])} 个格子，威胁区域 `{len(S.target[-1])}` 个空格；最大威胁 `{S.max_target}`'


CONFIG = dict(
    num=749, title='隔离病毒', difficulty='Hard', category='网格图',
    author='yiduobo', technique='模拟 · BFS 找病毒块 + 位掩码记墙',
    tags=[],
    code='''
class Solution(object):
    def containVirus(self, grid):

        m = len(grid)
        n = len(grid[0])
        walls = [[0] * n for _ in range(m)]
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        res = 0
        rnd = 0
        used = [[0] * n for _ in range(m)]

        while True:
            virius = []
            target = []
            prepare_wall = []
            
            max_target = 0
            max_target_pos = None
            rnd += 1

            for i in range(m):
                for j in range(n):
                    #used[i][j]不等于rnd表示在第rnd轮(i,j)这个位置还未被访问过
                    if used[i][j] != rnd and grid[i][j] == 1:
                        virius.append([])
                        target.append(set())
                        prepare_wall.append([])
                        used[i][j] = rnd
                        q = [[i, j]]
                        l = 0
                        r = 1
                        while l < r:
                            nowx, nowy = q[l]
                            l += 1
                            virius[-1].append([nowx, nowy])
                            for index in range(4):
                                x = nowx + dx[index]
                                y = nowy + dy[index]
                                #walls[x][y]表示位置(x,y)的筑墙情况。
                                if x >= 0 and x < m and y >= 0 and y < n and (walls[x][y] & (1 << index)) == 0:
                                    #若(x,y)未被感染，则将其加入接下来被感染的target中，同时将如果需要筑的墙加入prepare_wall中
                                    if grid[x][y] == 0:
                                        target[-1].add((x, y))
                                        prepare_wall[-1].append([x, y, 1 << index])
                                    #否则若(x,y)已被感染，且在这一轮没有被访问过，那么将其加入bfs队列中
                                    else:
                                        if used[x][y] != rnd:
                                            q.append([x, y])
                                            r += 1
                                            used[x][y] = rnd

                        #max_target_pos表示这一轮target中面积最大的下标
                        if max_target < len(target[-1]):
                            max_target = len(target[-1])
                            max_target_pos = len(target) - 1
            
            if max_target == 0:
                return res

            #筑墙并累加至答案
            for nowx, nowy, direct in prepare_wall[max_target_pos]:
                walls[nowx][nowy] |= direct
            res += len(prepare_wall[max_target_pos])

            #感染
            for index in range(len(target)):
                if index != max_target_pos:
                    for (nowx, nowy) in target[index]:
                        grid[nowx][nowy] = 1
''',
    call=f'Solution().containVirus({GRID})',
    expect=7,
    skip=['prepare_wall[-1].append', 'max_target_pos = len(target) - 1', 'if used[i][j] != rnd and grid[i][j] == 1', 'for nowx, nowy, direct in prepare_wall', 'm = len', 'n = len', 'walls = [[', 'dx = [', 'dy = [', 'res = 0', 'rnd = 0', 'used = [[', 'virius = []', 'target = []',
          'prepare_wall = []', 'max_target = 0', 'max_target_pos = None', 'for i in range(m)', 'for j in range(n)',
          'target.append(set())', 'prepare_wall.append([])', 'q = [[i, j]]', 'l = 0', 'r = 1', 'l += 1',
          'for index in range(4)', 'x = nowx', 'y = nowy', 'q.append', 'r += 1', 'used[x][y] = rnd', 'used[i][j] = rnd',
          'virius[-1].append', 'for index in range(len(target))', 'for (nowx, nowy) in target', 'while True', 'nowx, nowy = q[l]'],
    max_steps=54,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_txt, size=28),
    ],
    watch=[('res', '已筑墙数 res', 'orange'), ('rnd', '轮 rnd', 'blue'), ('max_target', 'max_target', 'pink'), ('max_target_pos', 'max_target_pos', 'pink')],
    captions={
        'rnd += 1': '新的一轮：`rnd` = {rnd}。每轮 ==先找病毒块，再筑墙，最后其余病毒扩散==',
        'virius.append([])': '`({i},{j})` 是还没访问的病毒 → ==新的一块病毒==，用 BFS 找出整块，`rnd` 轮号当 visited',
        'if x >= 0 and x < m': lambda S, B, r: (
            f'邻居 `({S.x},{S.y})` 出界或这个方向已筑墙 → 跳过' if not (0 <= S.x < S.m and 0 <= S.y < S.n and (S.walls[S.x][S.y] & (1 << S.index)) == 0) else
            f'邻居 `({S.x},{S.y})` 在界内且没墙'),
        'if grid[x][y] == 0': lambda S, B, r: (
            f'`({S.x},{S.y})` 是空格 → 它会被这块病毒感染，记入 `target`，==预备在这条边上筑墙==' if S.grid[S.x][S.y] == 0 else
            f'`({S.x},{S.y})` 已感染 → 同一块病毒，没访问过就入队'),
        'target[-1].add': '空格 `({x},{y})` 记入集合 `target`（==去重算面积==，共 `{len(target[-1])}` 个），同时按边记下一面墙',
        'prepare_wall[-1].append': '`prepare_wall` 按==边==记：空格两边都挨着病毒要筑两面墙；现在 `{len(prepare_wall[-1])}` 面',
        'if max_target < len(target[-1])': lambda S, B, r: (
            f'这块威胁 `{len(S.target[-1])}` > 当前最大 `{B.max_target}` → ==更新最大==' if len(S.target[-1]) > B.max_target else
            f'这块威胁 `{len(S.target[-1])}` ≤ 当前最大 `{B.max_target}` → 不更新'),
        'max_target = len(target[-1])': '最大威胁 `max_target = {max_target}`',
        'max_target_pos = len(target) - 1': '记下这一块的下标 `max_target_pos = {max_target_pos}`',
        'if max_target == 0': lambda S, B, r: ('没有任何病毒还能扩散 → 结束' if S.max_target == 0 else f'最大威胁 `{S.max_target}` > 0 → 要隔离第 `{S.max_target_pos}` 块'),
        'walls[nowx][nowy] |= direct': '==隔离威胁最大的那块==：筑墙 `walls[{nowx}][{nowy}] |= {direct}` → `{walls[nowx][nowy]}`（4 位二进制记四个方向）',
        'res += len(prepare_wall': '这一轮筑了 `{len(prepare_wall[max_target_pos])}` 面墙，累计 `res` = =={res}==',
        'if index != max_target_pos': lambda S, B, r: (f'第 `{S.index}` 块不是最大威胁 → ==它会扩散==' if S.index != S.max_target_pos else f'第 `{S.index}` 块已被隔离 → 不扩散'),
        'grid[nowx][nowy] = 1': '`({nowx},{nowy})` 被感染，`grid` 置 1',
        'return res': '没有病毒能再扩散，一共筑墙 ==`{res}`== 面',
    },
    cards=dict(
        one_liner='每轮：找出病毒块，隔离威胁最大的，其余的扩散',
        complexity='每轮 `O(mn)`，至多 `O(mn)` 轮',
        problem=['`m × n` 的网格：`1` 是病毒，`0` 是空地',
                 '每晚==只能隔离威胁最大的那一块==（会感染最多空格的），在它与空格之间筑墙',
                 '其余病毒块向相邻空格扩散一格；求总共用了多少面墙',
                 '本视频：`[[0,1,0,0],[0,0,0,0],[0,0,0,1]]` → `7`'],
        quote='对于墙，每个位置最多有4个方向，那么可以使用4位的二进制来表示当前方向上是否有墙。另外需要注意的是，被墙隔开的病毒要算作两块病毒。',
        quote_src='—— yiduobo 题解原文',
        idea=['每轮先 BFS 找所有病毒块：记下块内格子、将被感染的空格集合 `target`、要筑的墙 `prepare_wall`',
              '`target` 最大的块被隔离：把它的墙写进 `walls`（4 位掩码），累加墙数',
              '其余块的 `target` 全部置 1。没有块能扩散就结束'],
        summary=['时间：每轮 `O(mn)`，最多 `O(mn)` 轮',
                 '易错：空格用集合去重算「面积」，墙数却按边计，两者别混',
                 '被墙隔开的病毒算两块：BFS 扩展时要先查 `walls`',
                 '`used[i][j] = rnd` 用轮号当 visited，免去每轮清零',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改，仅删去空行里的空格'],
    ),
)
