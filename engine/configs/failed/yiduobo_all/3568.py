ROOM = ['LS', 'RL']


def _fmt(t):
    return f"({t[0]},{t[1]}) e{t[2]} {t[3]:02b}"


CONFIG = dict(
    num=3568, title='清理教室的最少移动', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS 状态压缩 · f[x][y][e][s] + best_energy',
    tags=['动态规划', '难度分 2143'],
    code='''
class Solution(object):
    def minMoves(self, classroom, energy):

        m = len(classroom)
        n = len(classroom[0])

        sx, sy = None, None
        garbadge_id = {}

        for i in range(m):
            for j in range(n):
                if classroom[i][j] == 'L':
                    garbadge_id[(i, j)] = len(garbadge_id)
                elif classroom[i][j] == 'S':
                    sx = i
                    sy = j

        if not garbadge_id:
            return 0

        max_state = (1 << len(garbadge_id)) - 1

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        f = [[[[None] * (max_state + 1) for _ in range(energy + 1)] for _ in range(n)] for _ in range(m)]
        best_energy = [[[None] * (max_state + 1) for _ in range(n)] for _ in range(m)]
        q = deque()
        q.append((sx, sy, energy, 0))
        f[sx][sy][energy][0] = 0
        best_energy[sx][sy][0] = energy

        while q:
            now_x, now_y, now_e, now_s = q.popleft()
            for d in range(4):
                nxt_x = now_x + dx[d]
                nxt_y = now_y + dy[d]
                if 0 <= nxt_x < m and 0 <= nxt_y < n and classroom[nxt_x][nxt_y] != 'X':
                    if classroom[nxt_x][nxt_y] == 'R':
                        nxt_e = energy
                        nxt_s = now_s
                    else:
                        nxt_e = now_e - 1
                        if classroom[nxt_x][nxt_y] == 'L':
                            delta_s = 1 << garbadge_id[(nxt_x, nxt_y)]
                            nxt_s = now_s | delta_s
                        else:
                            nxt_s = now_s
                    
                    if f[nxt_x][nxt_y][nxt_e][nxt_s] is None and (best_energy[nxt_x][nxt_y][nxt_s] is None or best_energy[nxt_x][nxt_y][nxt_s] < nxt_e):
                        best_energy[nxt_x][nxt_y][nxt_s] = nxt_e
                        if nxt_e > 0:
                            q.append((nxt_x, nxt_y, nxt_e, nxt_s))
                        f[nxt_x][nxt_y][nxt_e][nxt_s] = f[now_x][now_y][now_e][now_s] + 1
                        if nxt_s == max_state:
                            return f[nxt_x][nxt_y][nxt_e][nxt_s]
    
        return -1
''',
    call=f'Solution().minMoves({ROOM}, 4)',
    expect=3,
    skip=['m = len', 'n = len', 'sx, sy = None', 'garbadge_id = {}', 'for i in range(m)', 'for j in range(n)',
          "elif classroom[i][j] == 'S'", 'sx = i', 'sy = j', 'dx = [', 'dy = [', 'f = [[[[', 'best_energy = [[[',
          'q = deque()', 'for d in range(4)', 'nxt_x = now_x', 'nxt_y = now_y', 'max_state = ('],
    max_steps=60,
    views=[
        dict(type='text', size=24, fn=lambda S: (
            f"当前 `({S['now_x']},{S['now_y']})` 能量 ==`{S['now_e']}`==，已收垃圾 `{S['now_s']:0{len(S['garbadge_id'])}b}`，已走 `{S['f'][S['now_x']][S['now_y']][S['now_e']][S['now_s']]}` 步"
            if 'now_s' in S and 'f' in S else '')),
        dict(type='grid', var='classroom', cell=110, h=300, label='classroom（蓝 = 当前出队的格子，粉 = 正在看的邻居）',
             cursors=[('now_x', 'now_y', 'blue'), ('nxt_x if _line >= 38 else None', 'nxt_y', 'pink')]),
        dict(type='queue', var='q', fmt=_fmt, font=24, label='q（队首 → 队尾：(行,列) 能量 垃圾集合）', h=130),
    ],
    watch=[('now_e', 'now_e', 'cyan'), ('now_s', 'now_s', 'blue'), ('nxt_e', 'nxt_e', 'pink'), ('nxt_s', 'nxt_s', 'pink')],
    captions={
        'garbadge_id[(i, j)] = len': '遇到垃圾 `({i},{j})`，编号 `{len(garbadge_id) - 1}`（第 k 个垃圾对应第 k 位）',
        'if not garbadge_id': lambda S, B, r: ('有垃圾，需要 BFS' if S.garbadge_id else '没有垃圾，直接返回 0'),
        'q.append((sx, sy, energy, 0))': '起点入队：位置 `({sx},{sy})`，满能量 `{energy}`，垃圾集合空',
        'f[sx][sy][energy][0] = 0': '`f[x][y][e][s]` = 到这个状态的最少移动次数，起点是 0',
        'best_energy[sx][sy][0] = energy': '`best_energy[x][y][s]` = 位置、垃圾集合相同时==剩下过的最大体力==，用来剪掉“反复横跳”',
        'while q': lambda S, B, r: ('队列不空，继续 BFS' if B.q else '队列空了，没收完所有垃圾 → 返回 -1'),
        'q.popleft()': '出队 `({now_x},{now_y})`，能量 `{now_e}`，垃圾集合 `{now_s:0{len(garbadge_id)}b}`，已走 `{f[now_x][now_y][now_e][now_s]}` 步',
        'if 0 <= nxt_x < m': lambda S, B, r: (f'邻居 `({B.nxt_x},{B.nxt_y})` 在界内且不是障碍 → 可以走'
                                              if (0 <= B.nxt_x < B.m and 0 <= B.nxt_y < B.n and B.classroom[B.nxt_x][B.nxt_y] != 'X')
                                              else f'邻居 `({B.nxt_x},{B.nxt_y})` 越界或是障碍 X → 跳过'),
        "if classroom[nxt_x][nxt_y] == 'R'": lambda S, B, r: ('休息区：走进去就能把能量补满，垃圾集合不变' if B.classroom[B.nxt_x][B.nxt_y] == 'R'
                                                              else '不是休息区，要消耗 1 点能量'),
        'nxt_e = energy': '进入休息区 → 能量回满 `nxt_e = {nxt_e}`，垃圾集合 `nxt_s` 不变',
        'nxt_e = now_e - 1': '移动消耗 1 点能量：`nxt_e = {now_e} - 1 = {nxt_e}`',
        "if classroom[nxt_x][nxt_y] == 'L'": lambda S, B, r: ('邻居是垃圾 → 要把它并入集合' if B.classroom[B.nxt_x][B.nxt_y] == 'L'
                                                              else '邻居没有垃圾 → 垃圾集合不变'),
        'nxt_s = now_s | delta_s': '收垃圾：`{now_s:0{len(garbadge_id)}b} | {delta_s:0{len(garbadge_id)}b} = {nxt_s:0{len(garbadge_id)}b}`',
        'nxt_s = now_s': lambda S, B, r: f'垃圾集合不变：`nxt_s = {S.nxt_s:0{len(S.garbadge_id)}b}`',
        'if f[nxt_x][nxt_y][nxt_e][nxt_s] is None and': lambda S, B, r: (
            f'状态 `({B.nxt_x},{B.nxt_y}, e={B.nxt_e}, s={B.nxt_s:0{len(B.garbadge_id)}b})` 没到过，且体力 `{B.nxt_e}` > 之前同位置同集合的最大体力 `{B.best_energy[B.nxt_x][B.nxt_y][B.nxt_s] if B.best_energy[B.nxt_x][B.nxt_y][B.nxt_s] is not None else '（还没记录）'}` → ==值得更新=='
            if (B.f[B.nxt_x][B.nxt_y][B.nxt_e][B.nxt_s] is None and (B.best_energy[B.nxt_x][B.nxt_y][B.nxt_s] is None or B.best_energy[B.nxt_x][B.nxt_y][B.nxt_s] < B.nxt_e))
            else f'这个状态到过了，或体力 `{B.nxt_e}` ≤ 之前同位置同集合的最大体力 `{B.best_energy[B.nxt_x][B.nxt_y][B.nxt_s]}` → ==往返横跳只会浪费能量，剪掉=='),
        'best_energy[nxt_x][nxt_y][nxt_s] = nxt_e': '更新最优体力：`best_energy[{nxt_x}][{nxt_y}][{nxt_s}] = {nxt_e}`',
        'if nxt_e > 0': lambda S, B, r: (f'体力 `{B.nxt_e}` > 0，还能继续走 → 入队' if B.nxt_e > 0 else '体力是 0，在非休息区走不动了 → 不入队（但步数仍要记录）'),
        'q.append((nxt_x': '入队 `({nxt_x},{nxt_y})`，体力 `{nxt_e}`，集合 `{nxt_s:0{len(garbadge_id)}b}`',
        'f[nxt_x][nxt_y][nxt_e][nxt_s] = f[now_x]': '`f` 记下步数：当前步数 + 1 = =={f[nxt_x][nxt_y][nxt_e][nxt_s]}==',
        'if nxt_s == max_state': lambda S, B, r: (f'`nxt_s == max_state`：垃圾全收完 → ==BFS 先到的就是最少移动次数 {S.f[S.nxt_x][S.nxt_y][S.nxt_e][S.nxt_s]}=='
                                                  if S.nxt_s == S.max_state else f'`nxt_s = {S.nxt_s:0{len(S.garbadge_id)}b}` ≠ `{S.max_state:0{len(S.garbadge_id)}b}`，还没收完'),
        'return f[nxt_x][nxt_y][nxt_e][nxt_s]': '返回最少移动次数 `{ret}`',
        'return -1': '队列空了仍未收完所有垃圾 → 返回 -1',
    },
    cards=dict(
        one_liner='f[x][y][e][s] 做 BFS，best_energy 剪掉反复横跳',
        complexity='时间 `O(mn·energy·2^L)`，空间同上',
        problem=['网格里 `S` 起点、`L` 垃圾、`R` 休息区、`X` 障碍',
                 '每步耗 1 点能量，能量为 0 只能靠休息区补满',
                 '收完所有垃圾最少要走几步？不可能就 `-1`',
                 '本视频：`["LS", "RL"]`，`energy = 4` → `3`'],
        quote='可以使用一个最优化数组best_energy[x][y][s]表示处于(x, y)且已经收集了状态表示为s的垃圾时可以剩下的最大体力。',
        quote_src='—— yiduobo 题解原文',
        idea=['垃圾顺序没有明显贪心 + 最多 10 个 → ==状态压缩==记录收集情况',
              '状态 `f[x][y][e][s]`：在 `(x,y)`、剩余能量 `e`、已收集集合 `s` 的最少步数',
              '用 BFS 做转移：休息区回满能量，垃圾格并入集合，其他格 `e-1`',
              '`best_energy` 剪枝：同位置同集合下，体力不比之前多就是无用功'],
        summary=['时间 `O(mn·energy·2^L)`，`L ≤ 10`；极限状态约 2000 万，要靠剪枝',
                 '`best_energy` 比 `f` 判重更强：体力少的同类状态直接丢掉',
                 '易错：体力变 0 时不入队，但仍要先记步数、检查是否收完',
                 '易错：休息区回满能量，且不会改变垃圾集合',
                 '对比灵神：灵神按层展开用 `ans` 计步，这里把步数存在 `f` 里',
                 '原文已是 Python 3 可运行的写法，代码未改'],
    ),
)
