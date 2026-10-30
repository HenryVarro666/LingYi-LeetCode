G0 = [[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0]]


def _side(name, cond, where):
    def f(S, B, r):
        i, j, g = S.i, S.j, S.grid
        m, n = len(g), len(g[0])
        if cond(i, j, g, m, n):
            return f'{name}：{where}是界外或水 → ==这是一条周长边==，下一步 `ans += 1`'
        return f'{name}：邻居是陆地 → 这条边在岛内部，不算'
    return f


def _col(S, i, j, v):
    return 'cyan' if v == 1 else None


CONFIG = dict(
    num=463, title='岛屿的周长', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='枚举陆地的四条边',
    tags=['灵神核心路线', '灵神题单·网格图', '灵神题单·贪心与思维'],
    code='''
class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        ans = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x == 0:
                    continue
                if i == 0 or grid[i - 1][j] == 0:  # 上：出界或者是水
                    ans += 1
                if i == m - 1 or grid[i + 1][j] == 0:  # 下：出界或者是水
                    ans += 1
                if j == 0 or row[j - 1] == 0:  # 左：出界或者是水
                    ans += 1
                if j == n - 1 or row[j + 1] == 0:  # 右：出界或者是水
                    ans += 1
        return ans
''',
    call=f'Solution().islandPerimeter({G0})',
    expect=12,
    skip=['m, n = len', 'ans = 0', 'for i, row', 'for j, x'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（青 = 陆地；黄框 = 当前格子）', cell=96, h=330,
             color=_col, cursors=[('i', 'j', 'yellow')]),
        dict(type='text', fn=lambda S: f"当前周长 ans = =={S['ans']}==" if 'ans' in S else '', size=34, h=60),
    ],
    watch=['i', 'j', 'x', ('ans', 'ans', 'green')],
    captions={
        'if x == 0': lambda S, B, r: (f'`({S.i},{S.j})` 是水 → 不是陆地，没有边，跳过' if S.x == 0
                                      else f'`({S.i},{S.j})` 是陆地 → 看它上下左右四个邻居'),
        'continue': '水不贡献周长，直接看下一格',
        '上：': _side('上', lambda i, j, g, m, n: i == 0 or g[i-1][j] == 0, '上面'),
        '下：': _side('下', lambda i, j, g, m, n: i == m-1 or g[i+1][j] == 0, '下面'),
        '左：': _side('左', lambda i, j, g, m, n: j == 0 or g[i][j-1] == 0, '左边'),
        '右：': _side('右', lambda i, j, g, m, n: j == n-1 or g[i][j+1] == 0, '右边'),
        'return ans': '所有陆地的边界边都数完了，周长 =={ans}==',
    },
    cards=dict(
        one_liner='周长 = 陆地和「水或界外」之间的边数',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`grid[i][j] = 1` 是陆地，`0` 是水；恰好有一个岛屿，没有内陆湖',
                 '格子是边长为 1 的正方形，求岛屿的周长',
                 '示例：`[[0,1,0,0],[1,1,1,0],[0,1,0,0]]` → `12`'],
        quote='边缘怎么判定？看图，黄色的边的两侧，一边是陆地，另一边出界或者是水。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不用 DFS 岛屿：直接枚举每个陆地格子的上下左右',
              '某一侧「出界」或者「是水」，就找到一条周长边，`ans += 1`',
              '题目保证没有内陆湖，所以数到的一定是岛屿外边缘'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：下和右要判断 `i == m - 1`、`j == n - 1`，否则越界',
                 '先判出界再取邻居：`or` 短路保证不会下标越界',
                 '对比岛屿数量：这题只需局部判断，不需要 DFS'],
    ),
)
