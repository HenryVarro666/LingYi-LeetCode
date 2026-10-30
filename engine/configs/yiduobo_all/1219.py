GRID = [[0, 6, 0], [5, 8, 0], [0, 9, 0]]
_IDX = {}
_POS = {}
for _i, _r in enumerate(GRID):
    for _j, _x in enumerate(_r):
        if _x > 0:
            _IDX[(_i, _j)] = len(_IDX)
            _POS[_IDX[(_i, _j)]] = (_i, _j)


def _cell(S, i, j, v):
    if v == 0:
        return None
    u = S.get('used')
    k = _IDX[(i, j)]
    now = S['_inner'].get('now')
    if u is not None and now == k:
        return 'yellow'
    if u is not None and k < len(u) and u[k]:
        return 'green'
    return None


def _cur(S):
    now = S['_inner'].get('now')
    if now is None:
        return '先建图：每块黄金编号，相邻的黄金连一条边'
    i, j = _POS[now]
    return f'当前在黄金 {now}（格子 ({i},{j})，金量 {S["v"][now]}），已选的路径涂成绿色'


CONFIG = dict(
    num=1219, title='黄金矿工', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='网格转稀疏图 + 枚举起点 DFS 回溯',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def getMaximumGold(self, grid):

        m = len(grid)
        n = len(grid[0])
        g = {}
        v = []
        cnt = 0
        num_dict = {}
        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    g[cnt] = set()
                    num_dict[(i, j)] = cnt
                    v.append(grid[i][j])
                    if i > 0 and grid[i - 1][j] > 0:
                        p = num_dict[(i - 1, j)]
                        g[p].add(cnt)
                        g[cnt].add(p)
                    if j > 0 and grid[i][j - 1] > 0:
                        p = num_dict[(i, j - 1)]
                        g[p].add(cnt)
                        g[cnt].add(p)
                    cnt += 1
        
        used = [False] * cnt
        res = 0
        for index in range(cnt):
            used[index] = True
            res = max(res, self.dfs(index, used, g, v))
            used[index] = False
        return res

    def dfs(self, now, used, g, v):
        max_next = 0
        for next in g[now]:
            if not used[next]:
                used[next] = True
                end_flag = False
                max_next = max(max_next, self.dfs(next, used, g, v))
                used[next] = False
        
        return max_next + v[now]
''',
    call='Solution().getMaximumGold([[0, 6, 0], [5, 8, 0], [0, 9, 0]])',
    expect=23,
    views=[
        dict(type='grid', var='grid', h=260, cell=84, color=_cell),
        dict(type='text', fn=_cur, size=28),
        dict(type='calls', h=170, hide=('grid',)),
        dict(type='text', fn=lambda S: f"`g` = {{{', '.join(f'{k}: {sorted(x)}' for k, x in S['g'].items())}}}" if 'g' in S and S['_line'] >= 25 else '', size=26),
    ],
    watch=[('index', lambda S: S.get('index'), 'blue'), ('now', lambda S: S['_inner'].get('now'), 'yellow'),
           ('max_next', lambda S: S['_inner'].get('max_next'), 'pink'), ('res', lambda S: S.get('res'), 'green')],
    max_steps=84,
    skip=['res = 0', 'num_dict[(i, j)] =', 'v.append', 'p = num_dict', 'g[p].add', 'if grid[i][j] > 0', 'for next in g[now]', 'm = len', 'n = len', 'g = {}', 'v = []', 'num_dict = {}', 'for j in range', 'end_flag = False'],
    captions={
        'cnt = 0': '`cnt` 给黄金编号',
        'g[cnt] = set()': '发现黄金 `({i},{j})` = `{grid[i][j]}`，编号 `{cnt}`，准备它的邻居集合',
        'if i > 0 and': lambda S, B, ret: (f'上方 `({S.i - 1},{S.j})` 有黄金 → 和它连边' if S.i > 0 and S.grid[S.i - 1][S.j] > 0 else '上方没有黄金，不连边'),
        'if j > 0 and': lambda S, B, ret: (f'左边 `({S.i},{S.j - 1})` 有黄金 → 和它连边' if S.j > 0 and S.grid[S.i][S.j - 1] > 0 else '左边没有黄金，不连边'),
        'g[cnt].add(p)': '无向边：`{p} — {cnt}`',
        'cnt += 1': '编号加一：`cnt` → {cnt}',
        'used = [False]': '建图完成，共 `{cnt}` 块黄金。`used` 标记路径上走过的块',
        'for index in range(cnt)': '枚举起点：黄金 `{index}`',
        'used[index] = True': '起点 `{index}` 入路径',
        'res = max(res': '调用 `dfs({index})`：求从起点 `{index}` 出发能拿到的最大金量，再用它更新 `res`（当前 {res}）',
        'used[index] = False': '起点处理完，撤销标记',
        'max_next = 0': '`max_next`：从 `{now}` 往下走能多拿的最大金量，先设为 0',
        'for next in g[now]': lambda S, B, ret: f'看 `{S.now}` 的邻居 `{S.next}`',
        'if not used[next]': lambda S, B, ret: (f'`{S.now}` 的邻居 `{S.next}` 还没走过 → 可以进' if not S.used[S.next] else f'`{S.now}` 的邻居 `{S.next}` 已在路径上 → 不能重复走'),
        'used[next] = True': '标记 `{next}` 在路径上，递归进入',
        'self.dfs(next': '递归进入 `{next}`：先求从它出发能拿到的最大金量，再和 `max_next = {max_next}` 比较取大',
        'used[next] = False': '回溯：撤销 `{next}` 的标记，换别的邻居试',
        'return max_next + v[now]': '`{now}` 能拿到的最大金量 = 往下走的最大值 `{max_next}` + 自己 `{v[now]}` = =={max_next + v[now]}==',
        'return res': '所有起点中最大的是 `{res}`',
    },
    cards=dict(
        one_liner='把有黄金的格子连成稀疏图，每个点当一次起点，DFS 回溯找最大路径',
        complexity='最坏 `O(n!)`，但网格图稀疏，实际远小于它',
        problem=['网格里的数字是黄金量，`0` 表示空格',
                 '可从任意有黄金的格子出发，上下左右走，==每格最多走一次==、不能走 0',
                 '本视频：`[[0,6,0],[5,8,7],[0,9,0]]` → `23`'],
        quote='首先扫描grid，对于每块黄金都进行编号，然后若两块黄金相连，那么就在图中给这两个点连上一条边。接下来枚举起点，然后从起点开始进行dfs即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫描网格：给黄金编号，相邻就连边 → 最多 25 个点的稀疏图',
              '`dfs(now)` 返回从 `now` 出发（不重复走）能拿到的最大金量',
              '`used` 标记路径，递归返回后撤销，才能换别的走法'],
        result='最大金量 23：6 → 8 → 9 ✓',
        summary=['最坏 `O(n!)`，但网格图稀疏，原文判断实际复杂度不高',
                 '易错：递归返回后要 `used[next] = False` 回溯',
                 '每个起点前后都要置 True / False',
                 '原文变量名 `next` 覆盖了内置函数，但在这里不影响运行',
                 '`end_flag` 是原文遗留的无用变量'],
    ),
)
