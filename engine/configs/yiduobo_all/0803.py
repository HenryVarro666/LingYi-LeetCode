GRID = [[1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 1, 0]]
HITS = [[1, 1], [0, 0], [2, 0]]
_PAL = ['cyan', 'orange', 'purple', 'pink', 'green']


def _cid(S):
    c = S.get('color')
    if c is None:
        return None
    return [['' if v is None else v for v in row] for row in c]


def _ccol(S, i, j, v):
    c = S.get('color')
    if c is None or c[i][j] is None:
        return None
    k = c[i][j]
    fa = S.get('fa')
    if fa is not None and 0 <= k < len(fa):
        while fa[k] != k:
            k = fa[k]
    if k == 0:
        return 'green'
    return _PAL[(k - 1) % 4]


def _gcol(S, i, j, v):
    if v == 1:
        return 'blue' if S.get('color') is None else None
    return None


def _info(S):
    if 'res' not in S or not isinstance(S.get('res'), list):
        return ''
    return f"从后往前加回，目前得到（倒序）`res = {S['res']}`"


CONFIG = dict(
    num=803, title='打砖块', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='逆序加回 · 染色分片 · 并查集',
    tags=['常用数据结构', '贪心与思维'],
    code='''
class Solution(object):
    def hitBricks(self, grid, hits):
        
        m = len(grid)
        n = len(grid[0])
        color = [[None] * n for _ in range(m)]
        for x, y in hits:
            grid[x][y] -= 1
        now = 0
        q = []
        cnt = []
        for j in range(n):
            if grid[0][j] == 1:
                color[0][j] = now
                q.append([0, j])
        self.bfs(q, m, n, grid, color, now, cnt)
        now += 1
        for i in range(1, m):
            for j in range(n):
                if grid[i][j] == 1 and color[i][j] is None:
                    color[i][j] = now
                    q = [[i, j]]
                    self.bfs(q, m, n, grid, color, now, cnt)
                    now += 1
        
        fa = [x for x in range(now)]
        res = []
        hits.reverse()
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        for nowx, nowy in hits:
            if grid[nowx][nowy] == 0:
                drop = set()
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:
                        drop.add(color[x][y])
                
                grid[nowx][nowy] = 1
                tmp = 0
                if nowx == 0:
                    min_fa = 0
                else:
                    min_fa = now
                drop_fa_set = set()
                for drop_color in drop:
                    drop_fa = self.find(drop_color, fa)
                    min_fa = min(min_fa, drop_fa)
                    if drop_fa != 0 and drop_fa not in drop_fa_set:
                        tmp += cnt[drop_fa]
                        drop_fa_set.add(drop_fa)
                
                if min_fa == 0:
                    res.append(tmp)
                    color[nowx][nowy] =0
                else:
                    res.append(0)
                    color[nowx][nowy] = min_fa
                    if min_fa == now:
                        fa.append(min_fa)
                        cnt.append(tmp + 1)
                        now += 1
                    else:
                        cnt[min_fa] = tmp + 1
                for drop_fa in drop_fa_set:
                    fa[drop_fa] = min_fa
                
            else:
                res.append(0)
        res.reverse()
        return res
    def find(self, drop_color, fa):
        if fa[drop_color] != drop_color:
            tmp = self.find(fa[drop_color], fa)
            fa[drop_color] = tmp
        return fa[drop_color]
    def bfs(self, q, m, n, grid, color, now, cnt):
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        l = 0
        r = len(q)
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x > 0 and x < m and y >=0 and y < n and grid[x][y] == 1 and color[x][y] is None:
                    color[x][y] = now
                    q.append([x, y])
                    r += 1
        
        cnt.append(len(q))
''',
    call=f'Solution().hitBricks({GRID}, {HITS})',
    expect=[2, 1, 0],
    views=[
        dict(type='grid', var='grid', label='grid（1 = 砖块；打掉的格子已经减 1：0 = 原来有砖，-1 = 原来就是空）', cell=76, h=250,
             color=_gcol, cursors=[('nowx', 'nowy', 'yellow')]),
        dict(type='grid', var=_cid, label='color：每个格子所属片区编号（0 = 仍连着第 0 行的片区；绿 = 片区 0）', cell=76, h=250,
             color=_ccol),
        dict(type='array', var='fa', label='fa：片区的并查集（fa[i] = i 的父亲）', cell=64, h=140),
        dict(type='text', fn=_info, size=26),
    ],
    watch=[('now', 'now', 'blue'), ('cnt', 'cnt', 'cyan'), ('min_fa', 'min_fa', 'orange'), ('res', 'res', 'green')],
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'l = 0', 'r = len(q)', 'l += 1', 'r += 1', 'for index in range(4)',
          'x = nowx + dx', 'y = nowy + dy', 'if x > 0 and x < m', 'if x >= 0 and x < m', 'q.append([0, j])', 'for j in range(n)',
          'if grid[0][j] == 1', 'q = []', 'cnt = []', 'hits.reverse()', 'res.reverse()', 'tmp = 0', 'drop = set()',
          'drop_fa_set = set()', 'for x, y in hits', 'now += 1', 'for i in range(1, m)', 'if grid[i][j] == 1 and', 'q = [[i, j]]',
          'color[0][j] = now', 'if fa[drop_color] != drop_color', 'if nowx == 0', 'min_fa = 0', 'min_fa = now\n',
          'drop_fa_set.add', 'if drop_fa != 0', 'tmp += cnt', 'else:', 'if min_fa == now', 'fa.append', 'now += 1', 'color[nowx][nowy] =0', 'while l < r', 'for drop_fa in drop_fa_set', 'min_fa = 0', 'tmp = self.find', 'fa[drop_color] = tmp', 'return fa[drop_color]'],
    captions={
        'color = [[None]': '`color` 记录每个格子属于哪个片区，先全空',
        'grid[x][y] -= 1': '把被打的格子 `({x}, {y})` 先全部减 1：有砖变 0，本来没砖变 -1 → ==先把要打的砖全打掉==',
        'nowx, nowy = q[l]': '出队 `({nowx}, {nowy})`，把相邻、值为 1、还没染色的格子染成同一片区',
        'color[x][y] = now': '`({x}, {y})` 染成片区 `{now}`，入队',
        'self.bfs(q, m, n, grid, color, now, cnt)': lambda S, B, r: ('第 0 行出发 BFS：到达的都是==最终状态下仍挂在顶上==的砖，片区 0'
                                                                      if S.now == 0 else f'从 `({S.i}, {S.j})` 出发 BFS，得到一个悬空的片区 `{S.now}`'),
        'cnt.append(len(q))': '这个片区一共 `{len(q)}` 块砖：`cnt` 记下 → `{cnt}`',
        'fa = [x for x': '并查集初始：每个片区自己是代表元；片区 0 是「挂在顶上」',
        'for nowx, nowy in hits': '==倒着==取下一块被打的砖（`hits` 已反转，从最后一次开始加回）',
        'color[i][j] = now': '`({i}, {j})` 是没染色的砖：新的悬空片区起点，编号 `{now}`',
        'for drop_color in drop': '逐个处理相邻的片区',
        'if min_fa == 0': lambda S, B, r: (f'`min_fa = {S.min_fa}`：这块砖连上了顶上（片区 0）→ 悬空片区会被拉回' if S.min_fa == 0
                                           else f'`min_fa = {S.min_fa}` ≠ 0：没连上顶上'),
        'if grid[nowx][nowy] == 0': lambda S, B, r: (f'`grid = 0`：这里原来有砖，现在加回来，看它连着哪些片区'
                                                    if S.grid[S.nowx][S.nowy] == 0 else
                                                    f'`grid = {S.grid[S.nowx][S.nowy]}` ≠ 0：这里原来就没有砖 → 打它不会掉砖'),
        'drop.add(color[x][y])': '邻居 `({x}, {y})` 有砖，属于片区 `{color[x][y]}`',
        'grid[nowx][nowy] = 1': '砖放回去：连着的片区有 `{sorted(drop)}`（片区 0 = 挂在顶上）',
        'min_fa = now': '`min_fa` 先设成大于所有片区编号的 `{now}`（表示还没连上顶）；若在第 0 行则直接为 0',
        'min_fa = min(min_fa, drop_fa)': lambda S, B, r: (f'相邻片区的代表元 `{S.drop_fa}` = 0：这块砖连上了顶上，`min_fa = 0`' if S.drop_fa == 0
                                                 else f'相邻片区的代表元 `{S.drop_fa}` ≠ 0：这是悬空片区' + ('；这块砖在第 0 行，本来就连着顶上' if S.nowx == 0 else f'，`min_fa = {S.min_fa}`')),
        'drop_fa_set.add': '片区 `{drop_fa}` 悬空，加回后会连上这块砖',
        'res.append(tmp)': '==连上了顶上==：这些悬空片区共 `{tmp}` 块，正着打这块砖时它们会掉下来 → `res` 记 `{tmp}`',
        'res.append(0)': lambda S, B, r: ('这块砖加回后仍没连上顶上：打它不会掉任何砖，记 `0`' if S.get('min_fa') is not None
                                           and S.grid[S.nowx][S.nowy] == 1 else '原来就没砖：记 `0`'),
        'fa[drop_fa] = min_fa': '把这些片区合并到 `{min_fa}` 里：`fa[{drop_fa}] = {min_fa}`',
        'return res': '`res` 是倒着算的，反转回来：`{res}`',
    },
    cards=dict(
        one_liner='正着打砖不好算，倒着把砖加回，连上顶部的片区就是掉落数',
        complexity='时间 `O(mn + h)`，空间 `O(mn)`',
        problem=['`grid` 中 1 是砖块；砖块「稳定」当且仅当它在第 0 行，或与稳定的砖块相邻',
                 '按顺序打掉 `hits` 里的砖，每次打完所有不稳定的砖会掉落',
                 '返回每次打砖后掉落的砖块数；打空位或不稳定处时是 `0`',
                 '本视频：`[[1,0,0,0],[1,1,1,0],[0,0,1,0]]`，`hits=[[1,1],[0,0],[2,0]]` → `[2,1,0]`'],
        quote='既然靠删节点的做法行不通，那么就索性将hits中的节点先全部删了，然后逆序遍历hits逐个再加回来。',
        quote_src='—— yiduobo 题解原文',
        idea=['图是动态变化的，tarjan 找关节点不行 → 改成「先全删，再倒着加」',
              '先把 hits 的格子都减 1，BFS 给最终状态染色：第 0 行连着的是片区 0，其余悬空片区各有编号和大小',
              '倒着加回 `(x, y)`：若连上片区 0，则它拉回的悬空片区就是正向打砖时掉下的',
              '分三种情况：孤立、只连悬空片区、连着片区 0；用并查集合并片区编号'],
        summary=['`grid[x][y] -= 1`：原来没砖的位置变成 `-1`，加回时 `grid != 0` 就记 `0`',
                 '加回第 0 行的砖，视作直接连上片区 0',
                 '连上片区 0 才记掉落数 `tmp`，否则只合并、记 `0`',
                 '答案是倒序的，最后 `res.reverse()`',
                 '代码原文即 Python 3 兼容，未做修改'],
    ),
)
