G0 = [[1, 0, 0], [0, 0, 2]]
M, N = 2, 3


def _vis(S):
    f = S['_inner']
    return f.get('state')


def _cell(S, i, j, v):
    num = i * N + j
    st = S['_inner'].get('state')
    last = S['_inner'].get('last')
    if v == 1:
        return 'green'
    if st is not None and 'prev_state' in S['_inner'] or st is not None:
        if last == num:
            return 'blue'
        if S.get('end') == num:
            return 'pink'
        if st >> num & 1:
            return 'orange'
        return None
    return 'pink' if v == 2 else None


def _txt(S):
    I = S['_inner']
    if 'state' not in I:
        return '`state` 是二进制位集合：第 `i*n+j` 位为 1 表示格子 `(i,j)` 已经走过'
    st, last = I['state'], I['last']
    bits = format(st, f'0{M * N}b')
    return f'`state = {bits}`（已走过的格子集合），停在格子 `{last}` = `({last // N},{last % N})`'


def _cap_if(S, B, ret):
    I = S['_inner']
    st, last = I['state'], I['last']
    return f'`f[{st}][{last}]` 还没算过（None）→ 先置 0，然后往回找上一步'


CONFIG = dict(
    num=980, title='不同路径 III', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='状态压缩 DP（汉密尔顿路径）',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 1830'],
    code='''
class Solution(object):
    def uniquePathsIII(self, grid):

        g = {}
        start = end = None
        final_state = 0

        m = len(grid)
        n = len(grid[0])

        for i in range(m):
            for j in range(n):
                if grid[i][j] != -1:
                    num = i * n + j
                    if grid[i][j] == 1:
                        start = num
                    elif grid[i][j] == 2:
                        end = num
                    
                    final_state |= 1 << num

                    if num not in g:
                        g[num] = set()

                    if i + 1 < m and grid[i + 1][j] != -1:
                        tmp = (i + 1) * n + j
                        if tmp not in g:
                            g[tmp] = set()
                        
                        g[num].add(tmp)
                        g[tmp].add(num)
                    
                    if j + 1 < n and grid[i][j + 1] != -1:
                        tmp = i * n + j + 1
                        if tmp not in g:
                            g[tmp] = set()
                        
                        g[num].add(tmp)
                        g[tmp].add(num)

        f = [[None] * (m * n) for _ in range(final_state + 1)]
        f[1 << start][start] = 1

        return self.dfs(final_state, end, g, start, f)
    
    def dfs(self, state, last, g, start, f):
        if f[state][last] is None:
            f[state][last] = 0
            if last == start:
                return 0 

            prev_state = state ^ (1 << last)

            for prev in g[last]:
                if prev_state & (1 << prev):
                    f[state][last] += self.dfs(prev_state, prev, g, start, f)
        
        return f[state][last]
''',
    call=f'Solution().uniquePathsIII({G0})',
    expect=1,
    views=[
        dict(type='grid', var=lambda S: G0, label='grid（绿 = 起点，粉 = 终点，橙 = state 里已走过，蓝 = 当前停留的格子）', cell=110, h=300,
             color=_cell),
        dict(type='text', size=26, h=70, fn=_txt),
        dict(type='map', var='g', label='g：每个格子的邻居（编号 = i*n+j）', fmt=lambda k, v: f"{k}: {sorted(v)}", h=210, font=28),
        dict(type='calls', h=200, hide=('g', 'f')),
    ],
    watch=[('start', 'start', 'green'), ('end', 'end', 'pink'), ('final_state', 'final_state', 'yellow'),
           ('state', lambda S: S['_inner'].get('state'), 'orange'), ('last', lambda S: S['_inner'].get('last'), 'blue')],
    skip=['m = len(grid)', 'n = len(grid[0])', 'for i in range(m)', 'for j in range(n)', 'if grid[i][j] != -1',
          'num = i * n + j', 'if grid[i][j] == 1', 'elif grid[i][j] == 2', 'if num not in g', 'g[num] = set()',
          'if i + 1 < m', 'if j + 1 < n', 'if tmp not in g', 'g[tmp] = set()', 'tmp = ', 'g[num].add', 'g[tmp].add',
          'start = num', 'end = num', 'g = {}', 'start = end = None', 'final_state = 0', 'for prev in g[last]'],
    captions={
        'final_state |= 1 << num': '格子 `{num}` 可走 → 把第 `{num}` 位并入全集：`final_state = {final_state}`',
        'f = [[None]': '`f[state][x]`：走过 `state` 里的格子、最后停在 `x` 的路径数；`None` 表示还没算',
        'f[1 << start][start] = 1': '边界：只走过起点、停在起点，只有 ==1 种== → `f[{1 << start}][{start}] = 1`',
        'return self.dfs(final_state': '答案 = `f[final_state][end]`：==全部格子走完，停在终点==，从这里往回推',
        'if f[state][last] is None': lambda S, B, r: (f'`f[{S.state}][{S.last}]` 还没算过 → 开始计算' if S.f[S.state][S.last] is None
                                                        else f'`f[{S.state}][{S.last}] = {S.f[S.state][S.last]}` 已有值，直接用'),
        'f[state][last] = 0': '先置 0，再累加所有可能的上一步',
        'if last == start': lambda S, B, r: ('`last == start` 但 `state` 里还有别的格子：起点只能是第一格 → 返回 0' if S.last == S.start
                                              else '`last` 不是起点，继续找它的上一步'),
        'prev_state = state ^ (1 << last)': '去掉当前格子：`prev_state = {state} ^ (1 << {last}) = {prev_state}`，即上一步之前走过的集合',
        'if prev_state & (1 << prev)': lambda S, B, r: (f'邻居 `{S.prev}` 在 `prev_state` 里（已走过）→ 它可以是上一步'
                                                         if S.prev_state & (1 << S.prev) else f'邻居 `{S.prev}` 还没走过，不能是上一步 → 跳过'),
        'f[state][last] += self.dfs': '递归求上一步 `f[{prev_state}][{prev}]`，结果累加进 `f[{state}][{last}]`',
        'return f[state][last]': '`f[{state}][{last}] = ` =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='用二进制集合记走过的格子，从全集往回推上一步',
        complexity='时间 `O(K·2^K)`，空间 `O(K·2^K)`（K = 可走格子数）',
        problem=['网格：`1` 起点，`2` 终点，`0` 可走，`-1` 障碍',
                 '求起点到终点、==每个无障碍格恰走一次==的路径数',
                 '本质：在格子图里数汉密尔顿路径，格子数 ≤ 20',
                 '本视频：`[[1,0,0],[0,0,2]]` → `1`'],
        quote='使用状态f[state][x]表示当前已经经过了state中的网格，最后停留在x这个格子一共有多少种方案',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个可走格子编号 `i*n+j`，建邻接表 `g`',
              '`f[state][x]` 必来自 `f[state ^ (1<<x)][y]`，`y` 是 `x` 的邻居且在 `state` 里',
              '从 `f[全集][终点]` 开始记忆化递归，往回推到只剩起点'],
        result='`f[全集][终点] = 1`，只有 1 条路径 ✓',
        summary=['时间 `O(K·2^K)`，K 是可走格子数（≤ 20）',
                 '易错：起点 `last == start` 时必须返回 0，否则会走回头路',
                 '只数“恰好走遍”的路径，所以终点要从全集往回推',
                 '作者提到更优的做法是陈丹琦的“基于连通性的状态压缩 DP”，文中未展开',
                 '原文为 Python 2 风格，代码无需修改，直接运行'],
    ),
)
