G0 = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]


def _fc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or S.get('_line', 0) < 14:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i, j - 1), (i - 1, j)):
        return 'blue'
    return 'purple' if G0[r][c] == 1 and False else None


def _gc(S, r, c, v):
    return 'purple' if G0[r][c] == 1 else None


def _text(S):
    i, j = S.get('i'), S.get('j')
    if i is None or S.get('_line', 0) < 14:
        return '`f[i][j]`：==从左侧==进入 `(i,j)` 的方案数；`g[i][j]`：==从上方==进入的方案数；紫 = 镜子'
    gr = S['grid']
    L = '镜子' if j > 0 and gr[i][j - 1] else '空格'
    U = '镜子' if i > 0 and gr[i - 1][j] else '空格'
    return f'`({i},{j})`：左邻 {"—" if j == 0 else L}，上邻 {"—" if i == 0 else U}；左邻是空格 → `f + g`，是镜子 → 只取 `g`'


CONFIG = dict(
    num=3665, title='统计镜子反射路径数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='网格 DP · 两个数组记录进入方向',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1883'],
    code='''
class Solution(object):
    def uniquePaths(self, grid):
        
        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        g = [[0] * n for _ in range(m)]
        f[0][0] = 1
        g[0][0] = 1
        mod = 10 ** 9 + 7

        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        pass
                    else:
                        if grid[i][j - 1] == 0:
                            f[i][j] = f[i][j - 1]
                else:
                    if j == 0:
                        if grid[i - 1][j] == 0:
                            g[i][j] = g[i - 1][j]
                    else:
                        if grid[i][j - 1] == 0:
                            f[i][j] = f[i][j - 1] + g[i][j - 1]
                            if f[i][j] >= mod:
                                f[i][j] -= mod
                        else:
                            f[i][j] = g[i][j - 1]
                        
                        if grid[i - 1][j] == 0:
                            g[i][j] = f[i - 1][j] + g[i - 1][j]
                            if g[i][j] >= mod:
                                g[i][j] -= mod
                        else:
                            g[i][j] = f[i - 1][j]
        
        res = f[-1][-1] + g[-1][-1]
        if res >= mod:
            res -= mod
        return res
''',
    call=f'Solution().uniquePaths({G0})',
    expect=5,
    max_steps=90,
    skip=['m = len', 'n = len', 'mod = ', 'for j in range', 'if i == 0', 'if j == 0', 'else:', 'pass', '>= mod', '-= mod', 'g = [[0]', 'g[0][0] = 1'],
    views=[
        dict(type='grid', var='grid', label='grid（紫 = 镜子，黄框 = 当前格）', h=170, cell=56, color=_gc,
             cursors=[('i', 'j', 'yellow', '')]),
        dict(type='text', fn=_text, size=20, h=55),
        dict(type='table', var='f', label='f[i][j]：从左侧进入 (i,j) 的方案数', h=190, cell=52, color=_fc),
        dict(type='table', var='g', label='g[i][j]：从上方进入 (i,j) 的方案数（蓝 = 依赖的邻格）', h=190, cell=52, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i][j]', 'f[i][j]', 'green'), ('g[i][j]', 'g[i][j]', 'purple')],
    captions={
        'f = [[0]': '`f`：从==左侧==进入单元格的方案数；`g`（下一行）：从==上方==进入的方案数',
        'f[0][0] = 1': '起点：`f[0][0] = g[0][0] = 1`',
        19: lambda S, B, r: (f'第一行只能从左侧来：左邻 `({S.i},{S.j-1})` 是空格，可以直接向右' if S.grid[S.i][S.j-1] == 0 else f'左邻 `({S.i},{S.j-1})` 是镜子：第一行没有「从上方进入」，被反射会出界 → `f` 保持 0'),
        20: '第一行：`f[{i}][{j}] = f[{i}][{j-1}]` = =={f[i][j]}==，`g` 保持 0',
        23: lambda S, B, r: (f'第一列只能从上方来：上邻 `({S.i-1},{S.j})` 是空格，可以直接向下' if S.grid[S.i-1][S.j] == 0 else f'上邻 `({S.i-1},{S.j})` 是镜子：第一列没有「从左侧进入」，被反射会出界 → `g` 保持 0'),
        24: '第一列：`g[{i}][{j}] = g[{i-1}][{j}]` = =={g[i][j]}==，`f` 保持 0',
        26: lambda S, B, r: (f'左邻 `({S.i},{S.j-1})` 是空格：无论它从哪进入，都能向右到 `({S.i},{S.j})`' if S.grid[S.i][S.j-1] == 0 else f'左邻 `({S.i},{S.j-1})` 是镜子：只有==从上方==进入它才会被转向右，所以只取 `g`'),
        27: '`f[{i}][{j}] = f[{i}][{j-1}] + g[{i}][{j-1}]` = =={f[i][j]}==',
        31: '`f[{i}][{j}] = g[{i}][{j-1}]` = =={f[i][j]}==（`f[{i}][{j-1}]` 那一路被镜子转向下，进不来）',
        33: lambda S, B, r: (f'上邻 `({S.i-1},{S.j})` 是空格：无论它从哪进入，都能向下到 `({S.i},{S.j})`' if S.grid[S.i-1][S.j] == 0 else f'上邻 `({S.i-1},{S.j})` 是镜子：只有==从左侧==进入它才会被转向下，所以只取 `f`'),
        34: '`g[{i}][{j}] = f[{i-1}][{j}] + g[{i-1}][{j}]` = =={g[i][j]}==',
        38: '`g[{i}][{j}] = f[{i-1}][{j}]` = =={g[i][j]}==（`g[{i-1}][{j}]` 那一路被镜子转向右，进不来）',
        'res = f': '终点两个方向的方案数相加：`{f[-1][-1]} + {g[-1][-1]}`',
        'return res': '答案 `{ret}`',
    },
    cards=dict(
        one_liner='用 f、g 分别记录「从左侧进入」和「从上方进入」',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['机器人从左上走到右下，只能右/下；值为 1 的格子是镜子',
                 '向右进镜子会被转向下、向下进镜子会被转向右，出界则无效',
                 '示例：`[[0,1,0],[0,0,1],[1,0,0]]` → `5`'],
        quote='若 (i, j - 1) 为空白，那么无论从哪个方向进入到 (i, j - 1)，都可以顺利从左往右进入到 (i, j)，因此 f[i][j] = f[i][j - 1] + g[i][j - 1]；反之，若是镜子，那么只有从上方进入时才会被转向。',
        quote_src='—— yiduobo 题解',
        idea=['不考虑镜子就是 `f[i][j] = f[i-1][j] + f[i][j-1]`',
              '加入镜子要记方向：`f` = 从左侧进入，`g` = 从上方进入',
              '左邻是空格取 `f + g`，是镜子只取 `g`；上邻同理；第一行/第一列单独处理'],
        summary=['时间/空间 `O(mn)`',
                 '易错：第一行只能从左边来，第一列只能从上边来，不可混用',
                 '代码用减法取模：两数相加后 `>= mod` 就减一次 `mod`',
                 '答案是终点 `f + g`；终点题目保证不是镜子'],
    ),
)
