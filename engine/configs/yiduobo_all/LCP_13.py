MAZE = ['S.MO', '#M.T']


def _arrs(S):
    if 'mech_to_stone' not in S:
        return ''
    l1 = f"start_to_stone = {S['start_to_stone']}   mech_to_stone = {S['mech_to_stone']}"
    l2 = []
    if S.get('start_to_mech') is not None:
        l2.append(f"start_to_mech = {S['start_to_mech']}")
    if S.get('mech_to_mech') is not None:
        l2.append(f"mech_to_mech = {S['mech_to_mech']}")
    if S.get('mech_to_target') is not None:
        l2.append(f"mech_to_target = {S['mech_to_target']}")
    return l1 + '\n' + '   '.join(l2)


def _maze(S):
    return [list(r) for r in S['maze']] if 'maze' in S else None


def _mcol(S, i, j, v):
    ch = S['maze'][i][j]
    return {'S': 'green', 'T': 'orange', 'M': 'purple', 'O': 'cyan', '#': 'red'}.get(ch)


def _dcol(S, i, j, v):
    I = S['_inner']
    if 'nowx' in I and (i, j) == (I['nowx'], I['nowy']):
        return 'blue'
    return None


def _fv(S):
    f = S.get('f')
    if f is None or 'max_state' not in S:
        return None
    return [['-' if c is None else c for c in r] for r in f]


def _fcol(S, i, j, v):
    I = S['_inner']
    if 'state' in I and (i, j) == (I['state'], I['last']):
        return 'yellow'
    return 'green' if v not in ('-', -1) else None

CODE = "class Solution(object):\n    def minimalSteps(self, maze):\n\n        mechs = []\n        stones = []\n        m = len(maze)\n        n = len(maze[0])\n\n        for i in range(m):\n            for j in range(n):\n                if maze[i][j] == 'S':\n                    sx = i\n                    sy = j\n                elif maze[i][j] == 'T':\n                    tx = i\n                    ty = j\n                elif maze[i][j] == 'M':\n                    mechs.append([i, j])\n                elif maze[i][j] == 'O':\n                    stones.append([i, j])\n        \n        def bfs(x, y, dis):\n            dis[x][y] = 0\n            q = [[x, y]]\n            dx = [0, 1, 0, -1]\n            dy = [1, 0, -1, 0]\n            head, tail = 0, 1\n            while head < tail:\n                nowx, nowy = q[head]\n                head += 1\n                for index in range(4):\n                    x = nowx + dx[index]\n                    y = nowy + dy[index]\n                    if x >= 0 and x < m and y >= 0 and y < n and maze[x][y] != '#' and dis[x][y] == -1:\n                        dis[x][y] = dis[nowx][nowy] + 1\n                        q.append([x, y])\n                        tail += 1\n\n        mech_cnt = len(mechs)\n        stone_cnt = len(stones)\n\n        start_to_stone = [-1] * stone_cnt\n        mech_to_stone = [[-1] * stone_cnt for _ in range(mech_cnt)]\n\n        for i, stone_pos in enumerate(stones):\n            stone_x, stone_y = stone_pos\n            dis = [[-1] * n for _ in range(m)]\n            bfs(stone_x, stone_y, dis)\n            start_to_stone[i] = dis[sx][sy]\n            for j, mech_pos in enumerate(mechs):\n                mech_x, mech_y = mech_pos\n                mech_to_stone[j][i] = dis[mech_x][mech_y]\n        \n        start_to_mech = [-1] * mech_cnt\n        for i in range(mech_cnt):\n            for j in range(stone_cnt):\n                if start_to_stone[j] == -1 or mech_to_stone[i][j] == -1:\n                    continue\n                if start_to_mech[i] == -1 or start_to_mech[i] > start_to_stone[j] + mech_to_stone[i][j]:\n                    start_to_mech[i] = start_to_stone[j] + mech_to_stone[i][j]\n        \n        mech_to_mech = [[-1] * mech_cnt for _ in range(mech_cnt)]\n        for i in range(mech_cnt - 1):\n            for j in range(i + 1, mech_cnt):\n                for k in range(stone_cnt):\n                    if mech_to_stone[i][k] == -1 or mech_to_stone[j][k] == -1:\n                        continue\n                    if mech_to_mech[i][j] == -1 or mech_to_mech[i][j] > mech_to_stone[i][k] + mech_to_stone[j][k]:\n                        mech_to_mech[i][j] = mech_to_stone[i][k] + mech_to_stone[j][k]\n                \n                mech_to_mech[j][i] = mech_to_mech[i][j]\n\n        dis = [[-1] * n for _ in range(m)]\n        bfs(tx, ty, dis)\n        start_to_target = dis[sx][sy]\n        mech_to_target = [-1] * mech_cnt\n        for i, mech_pos in enumerate(mechs):\n            mech_x, mech_y = mech_pos\n            mech_to_target[i] = dis[mech_x][mech_y]\n\n        if mech_cnt == 0:\n            return start_to_target\n        \n        res = -1\n        max_state = (1 << mech_cnt) - 1\n        f = [[None] * mech_cnt for _ in range(max_state + 1)]\n\n        def dfs(state,last, f):\n            if f[state][last] is not None:\n                return f[state][last]\n\n            prev_state = (state ^ (1 << last))\n            if prev_state == 0:\n                f[state][last] = start_to_mech[last]\n                return f[state][last]\n            else:\n                f[state][last] = -1\n                for i in range(mech_cnt):\n                    if mech_to_mech[last][i] == -1:\n                        continue\n                    if (prev_state & (1 << i)) == (1 << i):\n                        dfs(prev_state, i, f)\n                        if f[prev_state][i] != -1:\n                            if f[state][last] == -1 or f[state][last] > f[prev_state][i] + mech_to_mech[last][i]:\n                                f[state][last] = f[prev_state][i] + mech_to_mech[last][i]\n                return f[state][last]\n\n        for i in range(mech_cnt):\n            if mech_to_target[i] != -1:\n                dfs(max_state, i, f)\n                if f[max_state][i] is not None and f[max_state][i] != -1 and (res == -1 or res > f[max_state][i] + mech_to_target[i]):\n                    res = f[max_state][i] + mech_to_target[i]\n            \n        return res"

CONFIG = dict(
    num='LCP 13', title='寻宝', difficulty='Hard', category='网格图',
    author='yiduobo', technique='BFS 预处理 + 状压 DP（记忆化）',
    tags=['网格图'],
    code=CODE,
    call=f'Solution().minimalSteps({MAZE})',
    expect=10,
    skip=['mechs = []', 'stones = []', 'm = len', 'n = len', 'for i in range(m)', 'for j in range(n)', 'if maze[i][j]',
          'elif maze[i][j]', 'sx = i', 'sy = j', 'tx = i', 'ty = j', 'mechs.append', 'stones.append',
          'dx = [', 'dy = [', 'head, tail', 'head += 1', 'for index in range(4)', 'x = nowx', 'y = nowy',
          'if x >= 0 and x < m and y >= 0', 'q.append', 'tail += 1', 'while head < tail', 'q = [[x, y]]',
          'mech_x, mech_y', 'stone_x, stone_y', 'dis = [[-1]', 'mech_cnt = len', 'stone_cnt = len',
          'start_to_stone = [-1]', 'mech_to_stone = [[-1]', 'start_to_mech = [-1]', 'mech_to_mech = [[-1]',
          'mech_to_target = [-1]', 'for i in range(mech_cnt', 'for j in range(stone_cnt)', 'for j in range(i + 1',
          'for k in range(stone_cnt)', 'for index in range(4)', 'for i, stone_pos', 'for j, mech_pos',
          'for i, mech_pos', 'continue', 'res = -1', 'max_state = ', 'f = [[None]', 'prev_state = ', 'f[state][last] = -1',
          'for i in range(mech_cnt)', 'if (prev_state & ', 'dfs(prev_state, i, f)', 'return f[state][last]', 'nowx, nowy = q[head]', 'if mech_to_mech[last][i] == -1', 'if f[state][last] is not None'],
    max_steps=110,
    views=[
        dict(type='grid', var=_maze, label='maze（S 起点 T 终点 M 机关 O 石头）', cell=84, h=220, color=_mcol),
        dict(type='grid', var='dis', label='dis：BFS 距离（-1 = 没到过，蓝 = 出队格）', cell=84, h=220, color=_dcol),
        dict(type='table', var=_fv, label='f[state][last]（行 state，列 last）', cell=84, h=210,
             color=_fcol),
        dict(type='text', fn=_arrs, size=19, h=140),
    ],
    watch=[('mech_cnt', 'mech_cnt', 'purple'), ('res', 'res', 'green')],
    captions={
        'dis[x][y] = 0': 'BFS 从 `({x},{y})` 出发：`dis[x][y] = 0`，其余格子是 -1（没到过）',
        'dis[x][y] = dis[nowx][nowy] + 1': '`({nowx},{nowy})` 走一步到 `({x},{y})`：距离 {dis[nowx][nowy]} + 1 = =={dis[x][y]}==',
        'start_to_stone[i] = dis': '以石头为起点 BFS（无向，距离对称）：起点 S 到这块石头 `{start_to_stone[i]}` 步',
        'mech_to_stone[j][i] = dis': '机关 {j} 到石头 {i} 的最短路 `{mech_to_stone[j][i]}`',
        'if start_to_stone[j] == -1 or': lambda S, B, r: ('起点或机关到不了这块石头 → 跳过' if (S.start_to_stone[S.j] == -1 or S.mech_to_stone[S.i][S.j] == -1)
                                                          else f'石头 {S.j} 两头都连得通：起点 → 石头 → 机关 {S.i} 可行'),
        'if start_to_mech[i] == -1 or': '比较：起点经石头 {j} 到机关 {i} = `{start_to_stone[j]} + {mech_to_stone[i][j]}`，比已有的短就更新',
        'start_to_mech[i] = start_to_stone[j]': '`start_to_mech[{i}] = {start_to_mech[i]}`：起点先到石头、再到机关 {i}（机关只能被石头弹过去）',
        'if mech_to_stone[i][k] == -1 or': '机关 {i} → 石头 {k} → 机关 {j}：两段都要通',
        'if mech_to_mech[i][j] == -1 or': '`{mech_to_stone[i][k]} + {mech_to_stone[j][k]}` 和已有的 `mech_to_mech[i][j]` 比，更短就更新',
        'mech_to_mech[i][j] = mech_to_stone': '`mech_to_mech[{i}][{j}] = {mech_to_mech[i][j]}`：从机关 {i} 借石头弹到机关 {j} 的最短步数',
        'mech_to_mech[j][i] = mech_to_mech[i][j]': '对称：`mech_to_mech[{j}][{i}]` 同值',
        'bfs(tx, ty, dis)': '再以终点 T 为起点 BFS，得到起点和每个机关到终点的距离',
        'start_to_target = dis': '`start_to_target = {start_to_target}`（没机关时直接答案）',
        'mech_to_target[i] = dis': '机关 {i} 到终点 `{mech_to_target[i]}` 步',
        'if mech_cnt == 0': lambda S, B, r: ('没有机关：答案就是起点到终点' if S.mech_cnt == 0 else f'有 `{S.mech_cnt}` 个机关，预处理完毕，开始状压 DP：`f[state][last]`'),
        'if mech_to_target[i] != -1': '枚举最后停在机关 {i}：它能走到终点才有意义',
        'dfs(max_state, i, f)': '求 `f[全部打开][{i}]`：已打开全部机关、最后停在机关 {i}',
        'if prev_state == 0': lambda S, B, r: ('去掉 last 后没有机关了：边界，从起点出发' if S.prev_state == 0
                                               else f'`prev_state = {S.prev_state}`：还有别的机关，枚举上一个打开的机关 i，先递归求 `f[prev_state][i]`'),
        'f[state][last] = start_to_mech[last]': '边界：`f[{state}][{last}] = start_to_mech[{last}] = {f[state][last]}`',
        'if f[prev_state][i] != -1': '上一个状态 `f[{prev_state}][{i}] = {f[prev_state][i]}`',
        'if f[state][last] == -1 or': '转移：`f[prev][i] + mech_to_mech[last][i]` = `{f[prev_state][i]} + {mech_to_mech[last][i]}`，取最小',
        'f[state][last] = f[prev_state][i]': '`f[{state}][{last}]` 更新为 =={f[state][last]}==',
        'if f[max_state][i] is not None': '全打开、停在机关 {i}：`f = {f[max_state][i]}`，再加上到终点 `{mech_to_target[i]}`，和 `res` 比',
        'res = f[max_state][i] + mech_to_target[i]': '`res = {f[max_state][i]} + {mech_to_target[i]}` = =={res}==',
        'return res': '最少 `{res}` 步',
    },
    cards=dict(
        one_liner='机关只能靠石头弹：把「机关→石头→机关」压成一条边，再做状压 DP',
        complexity='预处理 BFS `O(石头数·mn)`，DP `O(2^k·k^2)`（k 为机关数）',
        problem=['迷宫里 `S` 起点、`T` 终点、`M` 机关、`O` 石头、`#` 墙，每步走一格',
                 '要先把==所有机关==都触发，才能到终点；触发机关要把石头推到机关上（石头可无限次使用）',
                 '求最少步数，到不了返回 `-1`',
                 '本视频：`["S.MO","#M.T"]` → `10`'],
        quote='行动顺序必然是 起点->石头->机关->石头->机关->...->石头->机关->终点……可以将到达机关作为里程碑来构造更好的状态表示，即==f[state][last]==。',
        quote_src='—— yiduobo 题解原文',
        idea=['从每块石头做 BFS，预处理 `mech_to_stone`，再合成 `start_to_mech`、`mech_to_mech`（机关经某块石头到另一个机关）',
              '`f[state][last]`：打开了 state 里的机关、最后停在机关 last 的最少步数',
              '转移：`f[state][last] = min(f[prev][i] + mech_to_mech[last][i])`，prev 是 state 去掉 last',
              '最后加上 `mech_to_target[last]`，对所有 last 取最小'],
        summary=['预处理 BFS `O(石头数·mn)`，DP `O(2^k·k^2)`；没机关要特判，到不了的距离 -1 要跳过',
                 '`mech_to_mech` 只填 i<j 再对称复制；起点→机关、机关→终点单独处理',
                 '原文为 Python 2 风格，代码未改动（Python 3 可直接运行）；演示用 1 块石头、2 个机关的小图'],
    ),
)
