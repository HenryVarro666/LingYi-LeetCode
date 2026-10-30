ROOM = ['LS', 'RL']


def _same(S, B, names):
    try:
        return all(S[k] == B[k] for k in names)
    except Exception:
        return False


def _txt(S):
    I = S['_inner']
    if 'e' not in I or 'full_mask' not in I:
        return ''
    k = bin(I['full_mask']).count('1')
    return (f"位置 `({I['x']},{I['y']})`，能量 ==`{I['e']}`==/{I['energy']}，已收垃圾 `{I['mask']:0{k}b}`"
            f"（目标 `{I['full_mask']:0{k}b}`），已走 `{I['ans']}` 步")


CONFIG = dict(
    num=3568, title='清理教室的最少移动', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='BFS 状态 (x,y,e,mask) + max_energy 去重',
    tags=['动态规划', '难度分 2143'],
    code='''
class Solution:
    def minMoves(self, classroom: List[str], energy: int) -> int:
        m, n = len(classroom), len(classroom[0])
        idx = [[0] * n for _ in range(m)]
        cnt_l = sx = sy = 0
        for i, row in enumerate(classroom):
            for j, b in enumerate(row):
                if b == 'L':
                    idx[i][j] = 1 << cnt_l
                    cnt_l += 1
                elif b == 'S':
                    sx, sy = i, j
        if cnt_l == 0:
            return 0

        DIRS = (-1, 0), (1, 0), (0, -1), (0, 1)
        max_energy = [[[-1] * (1 << cnt_l) for _ in range(n)] for _ in range(m)]
        max_energy[sx][sy][0] = energy
        q = [(sx, sy, energy, 0)]

        full_mask = (1 << cnt_l) - 1
        ans = 0
        while q:
            tmp = q
            q = []
            for x, y, e, mask in tmp:
                if mask == full_mask:
                    return ans
                if e == 0:
                    continue
                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and classroom[nx][ny] != 'X':
                        new_e = energy if classroom[nx][ny] == 'R' else e - 1
                        new_mask = mask | idx[nx][ny]
                        if new_e > max_energy[nx][ny][new_mask]:
                            max_energy[nx][ny][new_mask] = new_e
                            q.append((nx, ny, new_e, new_mask))
            ans += 1
        return -1
''',
    call=f'Solution().minMoves({ROOM}, 4)',
    expect=3,
    skip=['m, n = len', 'idx = [[0]', 'cnt_l = sx', 'DIRS =', 'for i, row', 'for j, b', 'elif b ==', 'tmp = q', 'q = []'],
    max_steps=64,
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='grid', var='classroom', cell=110, h=300, label='classroom（蓝 = 当前状态的位置，粉 = 下一步要去的格子）',
             cursors=[('x', 'y', 'blue'), ('nx if _line >= 32 else None', 'ny', 'pink')]),
        dict(type='queue', var='tmp', fmt=lambda t: f"({t[0]},{t[1]}) e{t[2]} {t[3]:02b}", font=24,
             label='tmp（本层状态：(行,列) 能量 垃圾集合）', h=120),
        dict(type='queue', var='q', fmt=lambda t: f"({t[0]},{t[1]}) e{t[2]} {t[3]:02b}", font=24,
             label='q（下一层状态）', h=120),
    ],
    watch=[('ans', 'ans', 'green'), ('e', lambda S: S['_inner'].get('e'), 'cyan'),
           ('mask', lambda S: S['_inner'].get('mask'), 'blue'), ('new_e', 'new_e', 'pink')],
    captions={
        'idx[i][j] = 1 << cnt_l': '给第 `{cnt_l}` 个垃圾分配编号，用一位二进制表示：`1 << {cnt_l}`',
        'if cnt_l == 0': lambda S, B, r: (f'有 `{S.cnt_l}` 个垃圾，需要搜索' if S.cnt_l else '没有垃圾就不用动：返回 0'),
        'max_energy = [[[': '`max_energy[x][y][mask]` = 到 `(x,y)`、已收垃圾集合为 `mask` 时见过的==最大能量==（-1 表示没到过）',
        'max_energy[sx][sy][0] = energy': '起点：位置 `(sx,sy)`，垃圾集合空，满能量 `{energy}`',
        'q = [(sx, sy, energy, 0)]': '起点状态入队：`(x, y, e, mask)`',
        'full_mask = ': '`full_mask` 是全部垃圾的集合（所有位都是 1）：`{full_mask:0{cnt_l}b}`',
        'while q': lambda S, B, r: (f'第 `{B.ans}` 层还有 `{len(B.q)}` 个状态要处理' if B.q else '队列空了，还没收完 → 返回 -1'),
        'for x, y, e, mask in tmp': lambda S, B, r: (
            '本层所有状态都处理完了' if _same(S, B, ('x', 'y', 'e', 'mask'))
            else f'取出状态 `({S.x},{S.y})`，能量 `{S.e}`，垃圾集合 `{S.mask:0{S.cnt_l}b}`'),
        'if mask == full_mask': lambda S, B, r: (f'`mask == full_mask`：垃圾全收完 → ==BFS 按层扩展，当前层数 {B.ans} 就是最少移动次数=='
                                                   if S.mask == S.full_mask else f'垃圾还没收完（`{S.mask:0{S.cnt_l}b}` ≠ `{S.full_mask:0{S.cnt_l}b}`），继续'),
        'if e == 0': lambda S, B, r: ('能量为 0 且不在 R 上，无法再走 → 丢弃这个状态' if S.e == 0 else f'能量 `{S.e}` > 0，可以继续走'),
        'for dx, dy in DIRS': lambda S, B, r: ('四个方向都试完了' if _same(S, B, ('dx', 'dy')) else f'尝试方向 `({S.dx},{S.dy})`'),
        'nx, ny = x + dx': '新位置 `({nx},{ny})`',
        'if 0 <= nx < m': lambda S, B, r: (f'`({B.nx},{B.ny})` 在界内且不是障碍 → 可以走' if (0 <= B.nx < B.m and 0 <= B.ny < B.n and B.classroom[B.nx][B.ny] != 'X')
                                           else f'`({B.nx},{B.ny})` 越界或是障碍 X → 不能走'),
        'new_e = energy if': lambda S, B, r: (f'`({S.nx},{S.ny})` 是 R → 能量重置回 `{S.energy}`' if S.classroom[S.nx][S.ny] == 'R'
                                              else f'普通移动消耗 1 点能量：`new_e = {S.e} - 1 = {S.new_e}`'),
        'new_mask = mask |': lambda S, B, r: (f'`({S.nx},{S.ny})` 是垃圾 → 集合并入：`{S.mask:0{S.cnt_l}b} | {S.idx[S.nx][S.ny]:0{S.cnt_l}b} = {S.new_mask:0{S.cnt_l}b}`'
                                              if S.idx[S.nx][S.ny] else f'没有垃圾 → 集合不变 `{S.new_mask:0{S.cnt_l}b}`'),
        'if new_e > max_energy[nx][ny][new_mask]': lambda S, B, r: (
            f'`new_e = {S.new_e}` > 之前见过的最大能量 `{B.max_energy[S.nx][S.ny][S.new_mask]}` → ==值得入队=='
            if S.new_e > B.max_energy[S.nx][S.ny][S.new_mask]
            else f'`new_e = {S.new_e}` ≤ 之前见过的 `{B.max_energy[S.nx][S.ny][S.new_mask]}`：同位置同集合下能量更少，==不会更优，剪掉（避免来回横跳）=='),
        'max_energy[nx][ny][new_mask] = new_e': '更新 `max_energy[{nx}][{ny}][{new_mask}] = {new_e}`',
        'q.append': '入队下一层：`({nx},{ny}, e={new_e}, mask={new_mask:0{cnt_l}b})`',
        'ans += 1': '这一层处理完，没有收完 → 层数 `ans` 加 1，处理下一层 → =={ans}==',
        'return -1': '队列空了仍没收完 → 返回 -1',
    },
    cards=dict(
        one_liner='把 (位置, 能量, 垃圾集合) 当状态做 BFS，同状态只留能量最大的',
        complexity='时间 `O(mn·energy·2^L)`，空间同上',
        problem=['网格里 `S` 起点、`L` 垃圾、`R` 重置能量、`X` 障碍；每步耗 1 能量',
                 '收集完所有垃圾，最少要走几步？不可能返回 `-1`',
                 '垃圾最多 10 个，所以用二进制集合表示已收垃圾',
                 '本视频：`["LS", "RL"]`，`energy = 4` → `3`'],
        quote='只有当状态 (x,y,e,mask) 中的 e > maxEnergy[x][y][mask]，才入队，并更新 maxEnergy[x][y][mask]=e。这样做的好处是，不会让相同 (x,y,mask) 下的更小的能量入队。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 = 位置 `(x,y)` + 能量 `e` + 垃圾集合 `mask`，每走一步层数 +1',
              '起点 `(sx,sy,energy,0)`，终点是 `mask` 等于全集',
              '优化：把 `vis[..][e][..]` 改成 `max_energy[x][y][mask]`，能量更小的同类状态直接剪掉',
              '双列表 `tmp` / `q` 一层一层往外扩，`ans` 就是层数'],
        summary=['时间 `O(mn·energy·2^L)`，`L ≤ 10` 是垃圾个数',
                 '优化前用 `vis` 记录能量这一维；优化后只记最大能量，避免无意义地来回横跳',
                 '易错：走到 R 时能量重置为 `energy`，不是 `e - 1`',
                 '易错：`e == 0` 的状态不能再走（R 格上除外，因为进 R 时已经重置了）',
                 '同类题：864 获取所有钥匙的最短路径，LCP 13 寻宝'],
    ),
)
