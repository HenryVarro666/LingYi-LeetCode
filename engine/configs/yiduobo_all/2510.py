def _fs(S):
    if 'f' not in S:
        return None
    return [['{' + ','.join(f'{v:+d}' if v else '0' for v in sorted(s)) + '}' if s else '·' for s in row] for row in S['f']]


def _cur(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i - 1, j), (i, j - 1)):
        return 'blue'
    return None


CONFIG = dict(
    num=2510, title='检查是否有路径经过相同数量的0和1', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='网格 DP · 差值集合',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def isThereAPath(self, grid):

        m = len(grid)
        n = len(grid[0])

        f = [[set() for j in range(n)] for i in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    delta = -1
                else:
                    delta = 1

                if i == 0 and j == 0:
                    f[i][j].add(delta)
                else:
                    if i > 0:
                        for v in f[i - 1][j]:
                            f[i][j].add(v + delta)
                
                    if j > 0:
                        for v in f[i][j - 1]:
                            f[i][j].add(v + delta)
        
        return 0 in f[-1][-1]
''',
    call='Solution().isThereAPath([[0,1,1],[1,0,0]])',
    expect=True,
    skip=['m = len', 'n = len', 'for j in range(n)] for i'],
    max_steps=110,
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前格，蓝 = 能走过来的上方/左方格）', cell=96, h=240,
             color=_cur, cursors=[('i', 'j', 'yellow')]),
        dict(type='grid', var=_fs, label='f[i][j]：到达该格时「1 的个数 − 0 的个数」可能取到的值', cell=170, h=240,
             color=_cur),
    ],
    watch=['i', 'j', ('delta', 'delta', 'orange'), ('f[i][j]', "sorted(f[i][j])", 'green')],
    captions={
        'f = [[set()': '`f[i][j]` 是集合：走到 `(i,j)` 时「1 的个数 − 0 的个数」==可能取到的差值==',
        'if grid[i][j] == 0': '`grid[{i}][{j}] = {grid[i][j]}`：走进这格，差值要 ==变化 {"-1（多一个 0）" if grid[i][j] == 0 else "+1（多一个 1）"}==',
        'delta = -1': '这格是 0 → `delta = -1`',
        'delta = 1': '这格是 1 → `delta = 1`',
        'if i == 0 and j == 0': '起点没有前驱：`i == 0 and j == 0` → {i == 0 and j == 0}',
        'f[i][j].add(delta)': '起点：差值只能是 `{delta}` → `f[0][0] = {sorted(f[0][0])}`',
        'if i > 0': '`i > 0` → {i > 0}：{"有上方格，可以从上面走下来" if i > 0 else "第一行，没有上方格"}',
        'for v in f[i - 1][j]': '上方格 `f[{i-1}][{j}] = {sorted(f[i-1][j])}`，每个差值 `v` 都能走过来',
        'for v in f[i][j - 1]': '左边格 `f[{i}][{j-1}] = {sorted(f[i][j-1])}`，每个差值 `v` 都能走过来',
        'if j > 0': '`j > 0` → {j > 0}：{"有左边格，可以从左边走过来" if j > 0 else "第一列，没有左边格"}',
        '.add(v + delta)': '差值 `{v}` 走进这格 → `{v} + ({delta}) = {v + delta}` 加入 `f[{i}][{j}]` = {sorted(f[i][j])}',
        'return 0 in': '终点差值集合 `{sorted(f[-1][-1])}`：{"==包含 0==，1 和 0 一样多 → True" if 0 in f[-1][-1] else "不含 0 → False"}',
    },
    cards=dict(
        one_liner='每格记下「1 的个数 − 0 的个数」能取到的所有值',
        complexity='时间 `O(mn(m+n))`，空间 `O(mn(m+n))`',
        problem=['`m × n` 的 0/1 网格，只能向右或向下走，从左上走到右下',
                 '问：是否存在一条路径，经过的 ==0 和 1 数量相同==',
                 '本视频：`[[0,1,1],[1,0,0]]` → `True`'],
        quote='令f[i][j][k]表示来到位置(i, j)，经过的1的数量比0的数量之差是否可能为k。',
        quote_src='—— yiduobo 题解原文',
        idea=['“0 和 1 一样多”等价于 ==差值为 0==：0 记 −1，1 记 +1',
              '`f[i][j]` 只可能从上方、左方转移，把它们的每个差值 + 当前格的 `delta`',
              '差值范围稀疏，原文用 ==集合== 代替第三维 k，最后看终点集合里有没有 0'],
        summary=['时间/空间都是 `O(mn(m+n))`：每格差值最多 `m+n` 种',
                 '起点要单独处理：它没有前驱，直接放入 `delta`',
                 '终点差值集合含 0 即为 True；路径长度是 `m+n-1`，为偶数才可能相等',
                 '原文用集合代替数组下标 k，不必加偏移量'],
    ),
)
