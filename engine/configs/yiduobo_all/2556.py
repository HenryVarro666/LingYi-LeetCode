G0 = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]

CONFIG = dict(
    num=2556, title='二进制矩阵中翻转最多一次使路径不连通', difficulty='Medium', category='网格图',
    author='yiduobo', technique='路径计数 f×g：所有路径都过的格子',
    tags=['灵神题单·网格图', '灵神题单·贪心与思维', '难度分 2369'],
    code='''
class Solution(object):
    def isPossibleToCutPath(self, grid):

        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        f[0][0] = 1
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    if i == 0:
                        if j == 0:
                            f[i][j] = 1
                        else:
                            f[i][j] = f[i][j - 1]
                    elif j == 0:
                        f[i][j] = f[i - 1][j]
                    else:
                        f[i][j] = f[i - 1][j] + f[i][j - 1]
        
        g = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 1:
                    if i == m - 1:
                        if j == n - 1:
                            g[i][j] =  1
                        else:
                            g[i][j] = g[i][j + 1]
                    elif j == n - 1:
                        g[i][j] = g[i + 1][j]
                    else:
                        g[i][j] = g[i + 1][j] + g[i][j + 1]
        
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                if i == m - 1 and j == n - 1:
                    continue
                if f[i][j] * g[i][j] == f[m - 1][n - 1]:
                    return True
        
        return False
''',
    call=f'Solution().isPossibleToCutPath({G0})',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"总路径数 `f[2][2]` = =={S['f'][-1][-1]}==；格子 `({S['i']},{S['j']})`：`f × g` = `{S['f'][S['i']][S['j']]} × {S['g'][S['i']][S['j']]}` = =={S['f'][S['i']][S['j']] * S['g'][S['i']][S['j']]}==" if 'g' in S and S['g'][0][0] and 'i' in S and 'j' in S and S['_line'] >= 39 else ''), h=50),
        dict(type='grid', var='grid', label='grid（0 = 墙）', cursors=[('i', 'j', 'yellow')], h=190, cell=60,
             color=lambda S, i, j, v: None),
        dict(type='table', var='f', label='f[i][j]：从起点走到 (i,j) 的路径数', cursors=[('i', 'j', 'yellow')], h=190, cell=60,
             color=lambda S, i, j, v: 'blue' if v else None),
        dict(type='table', var='g', label='g[i][j]：从 (i,j) 走到终点的路径数', cursors=[('i', 'j', 'yellow')], h=190, cell=60,
             color=lambda S, i, j, v: 'pink' if v else None),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow')],
    skip=['m = len', 'n = len', 'if i == 0:', 'if j == 0:', 'elif j == 0:', 'if i == m - 1:', 'if j == n - 1:', 'elif j == n - 1:',
          'if i == 0 and j == 0', 'continue', 'if i == m - 1 and j == n - 1'],
    max_steps=90,
    captions={
        'f = [[0]': '`f[i][j]`：从 `(0,0)` 走到 `(i,j)` 的==方案数==（只能向下、向右）',
        'f[0][0] = 1': '起点只有 1 种走法',
        'if grid[i][j] == 1': lambda S, B, ret: (f'`({S.i},{S.j})` 是 `1`，可走 → 按来源累加路径数' if S.grid[S.i][S.j] == 1 else f'`({S.i},{S.j})` 是 `0`（墙），路径数保持 0'),
        'f[i][j] = 1': '起点：`f[0][0] = 1`',
        'f[i][j] = f[i][j - 1]': '第一行只能从左边来：`f[{i}][{j}] = f[{i}][{j - 1}]` = =={f[i][j]}==',
        18: '第一列只能从上面来：`f[{i}][{j}] = f[{i - 1}][{j}]` = =={f[i][j]}==',
        'f[i][j] = f[i - 1][j] + f[i][j - 1]': '上面 + 左边：`{f[i - 1][j]} + {f[i][j - 1]}` = =={f[i][j]}==',
        'g = [[0]': '`g[i][j]`：从 `(i,j)` 反着走到终点 `(m-1,n-1)` 的方案数，同样从后往前填',
        'g[i][j] =  1': '终点：`g[m-1][n-1] = 1`',
        'g[i][j] = g[i][j + 1]': '最后一行只能向右：`g[{i}][{j}] = g[{i}][{j + 1}]` = =={g[i][j]}==',
        32: '最后一列只能向下：`g[{i}][{j}] = g[{i + 1}][{j}]` = =={g[i][j]}==',
        'g[i][j] = g[i + 1][j] + g[i][j + 1]': '下面 + 右边：`{g[i + 1][j]} + {g[i][j + 1]}` = =={g[i][j]}==',
        'if f[i][j] * g[i][j] == f[m - 1][n - 1]': lambda S, B, ret: (
            f'`f×g` = `{S.f[S.i][S.j]}×{S.g[S.i][S.j]}` = {S.f[S.i][S.j] * S.g[S.i][S.j]}；总路径 `{S.f[S.m - 1][S.n - 1]}`：'
            + ('==相等 → 所有路径都经过它=='  if S.f[S.i][S.j] * S.g[S.i][S.j] == S.f[S.m - 1][S.n - 1] else '不相等 → 有路径绕开它')),
        'return True': '翻转 `({i},{j})`（1 变 0），所有路径都被切断 → 返回 `True`',
        'return False': '没有这样的必经点 → 返回 `False`',
    },
    cards=dict(
        one_liner='路径数：f×g 等于总路径数，说明所有路径都经过这个格子',
        complexity='时间 `O(mn)`，空间 `O(mn)`（f、g 的值会很大，Python 大整数无忧）',
        problem=['`m×n` 的 0/1 矩阵，只能向下或向右走到值为 `1` 的格子',
                 '最多翻转一个格子（起点终点除外），能否让起点到不了终点？',
                 '本视频示例：`[[1,1,0],[1,1,1],[0,1,1]]` → `true`'],
        quote='若存在某个非起点和终点的位置(i, j)，满足f[i][j] * g[i][j] = f[m - 1][n - 1]，那么就说明每一条从(0, 0)到(m - 1, n - 1)的路径都会经过(i, j)',
        quote_src='—— yiduobo 题解原文',
        idea=['翻 0 变 1 没意义，只需考虑把某个 1 变 0，问题就是「有向图里有没有割点」',
              '`f[i][j]` 从起点到 `(i,j)` 的路径数，`g[i][j]` 从 `(i,j)` 到终点的路径数',
              '`f×g` 是经过 `(i,j)` 的路径数；等于总路径数 ⇒ 每条路径都经过它 ⇒ 翻掉它就断了'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错点：路径数可能极大，C++/Java 要大数，Python 原生支持',
                 '易错点：必须排除起点和终点（它们的 `f×g` 一定等于总路径数）',
                 '原文本身已是 Python 3 可运行的写法，代码未做修改',
                 '对比灵神：灵神用「贪心走一遍抹掉下轮廓」，思路更巧、空间更省；这里是计数法'],
    ),
)
