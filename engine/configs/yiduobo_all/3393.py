G = [[1, 2], [3, 0]]


def _ftab(S):
    f = S.get('f')
    if f is None:
        return None
    return [[''.join(map(str, f[i][j][:4])) for j in range(len(f[0]))] for i in range(len(f))]


def _fcol(S, i, j, v):
    a, b = S.get('i'), S.get('j')
    if a is None or S.get('_line') not in (14, 17, 20, 23, 24):
        return None
    if (i, j) == (a, b):
        return 'yellow'
    if (i, j) in ((a, b - 1), (a - 1, b)):
        return 'blue'
    return None


def _vcap(S, B, ret):
    i, j, v, g = S.i, S.j, S.v, S.grid[S.i][S.j]
    src = []
    if j > 0:
        src.append(f'左 {S.f[i][j-1][v ^ g]}')
    if i > 0:
        src.append(f'上 {S.f[i-1][j][v ^ g]}')
    return f'`f[{i}][{j}][{v}]`：来源 `{v}^{g}={v ^ g}`，' + ' + '.join(src) + f' = =={S.f[i][j][v]}=='


CONFIG = dict(
    num=3393, title='统计异或值为给定值的路径数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='f[i][j][v] 三维 DP（上方 + 左侧）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1573'],
    code='''
class Solution(object):
    def countPathsWithXorValue(self, grid, k):
        
        m = len(grid)
        n = len(grid[0])
        mod = 10 ** 9 + 7

        f = [[[0] * 16 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    f[i][j][grid[i][j]] = 1
                elif i == 0:
                    for v in range(16):
                        f[i][j][v] += f[i][j - 1][v ^ grid[i][j]]
                elif j == 0:
                    for v in range(16):
                        f[i][j][v] += f[i - 1][j][v ^ grid[i][j]]
                else:
                    for v in range(16):
                        f[i][j][v] = (f[i][j - 1][v ^ grid[i][j]] + f[i - 1][j][v ^ grid[i][j]]) % mod
        
        return f[-1][-1][k]
''',
    call=f'Solution().countPathsWithXorValue({G}, 3)',
    expect=1,
    max_steps=60,
    skip=['mod = ', 'for _ in range', 'for i in range', 'for j in range', 'for v in range'],
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前格 (i,j)）', cell=84, h=210,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='table', var=_ftab, label='f（只画 v=0..3 四位；黄 = 正在算，蓝 = 来源）',
             cell=120, h=250, color=_fcol),
        dict(type='text', fn=lambda S: (f"`v = {S['v']}`，当前格 `grid = {S['grid'][S['i']][S['j']]}`，来源异或值 `{S['v']} ^ {S['grid'][S['i']][S['j']]} = {S['v'] ^ S['grid'][S['i']][S['j']]}`"
                                         if 'v' in S and 'i' in S and 'j' in S else '`f[i][j][v]` = 从 `(0,0)` 走到 `(i,j)`、路径异或值为 `v` 的路径数'), size=24, h=50),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'v', ('k', 'k', 'green')],
    captions={
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列',
        'f = [[[0]': '`f[i][j][v]`：多开一维 `v`，值域 0..15 共 16 个（视频只画前 4 个，示例值都小于 4）',
        'f[i][j][grid[i][j]] = 1': '起点：只有一条空路径，异或值就是自己 `{grid[0][0]}` → `f[0][0][{grid[0][0]}] = 1`',
        'f[i][j][v] += f[i][j - 1]': _vcap,
        'f[i][j][v] += f[i - 1][j]': _vcap,
        'f[i][j][v] = (': _vcap,
        'return f[-1][-1][k]': '右下角 `f[-1][-1][{k}]` = =={ret}==',
    },
    cards=dict(
        one_liner='先忽略异或做路径计数，再把异或值 v 当作状态多开一维',
        complexity='时间 `O(16mn)`，空间 `O(16mn)`',
        problem=['`m x n` 的 `grid`，只能向右或向下，从左上走到右下',
                 '要求路径上元素的==异或值恰好等于 `k`==，求路径数',
                 '元素与 `k` 都在 0 到 15 之间',
                 '本视频：`[[1,2],[3,0]]`，`k=3` → `1`'],
        quote='无论怎么走，路径上元素值的异或值也只会在0到15之间，于是可以在状态表示上再加上一维v',
        quote_src='—— yiduobo 题解原文',
        idea=['不考虑异或：`f[i][j] = f[i-1][j] + f[i][j-1]`',
              '再加一维 `v`：到 `(i,j)` 异或值为 `v`，则前一格的异或值是 `v ^ grid[i][j]`',
              '第 0 行、第 0 列只有一个来源，起点单独设为 1'],
        summary=['时间/空间 `O(16mn)`',
                 '易错：第 0 行只能从左来、第 0 列只能从上来，要分开写',
                 '易错：起点 `f[0][0][grid[0][0]] = 1`，不是 `v = 0`',
                 '原文第 0 行/第 0 列没有取模，只在一般格子取模；本题数据量小不影响结果',
                 '对比灵神：灵神多开一圈哨兵免去分支；yiduobo 把边界拆成三种情况'],
    ),
)
