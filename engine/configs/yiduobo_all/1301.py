B0 = ["E12", "1X1", "21S"]


def _fmt(S, B, r):
    return ''


def _src(S, B, r):
    return (f'三个方向的最大和 `v1 = {S.v1}`（上）、`v2 = {S.v2}`（左）、`v3 = {S.v3}`（左上）；'
            f'`-1` 表示那个方向走不过来')


CONFIG = dict(
    num=1301, title='最大得分的路径数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='网格 DP：每格记 [最大和, 方案数]',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1853'],
    code='''
class Solution(object):
    def pathsWithMaxScore(self, board):

        mod = 10 ** 9 + 7
        m = len(board)
        n = len(board[0])
        f = []
        g = []
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'X':
                    f.append([0, 0])
                elif board[i][j] == 'E':
                    f.append([0, 1])
                else:
                    v1 = v2 = v3 = -1
                    if i > 0 and g[j][1] > 0:
                        v1 = g[j][0]
                        s1 = g[j][1]
                    if j > 0 and f[-1][1] > 0:
                        v2 = f[-1][0]
                        s2 = f[-1][1]
                    if i > 0 and j > 0 and g[j - 1][1] > 0:
                        v3 = g[j - 1][0]
                        s3 = g[j - 1][1]

                    max_v = max(v1, v2, v3)
                    if max_v < 0:
                        f.append([0, 0])
                    else:
                        s = 0
                        if v1 == max_v:
                            s += s1
                        if v2 == max_v:
                            s += s2
                            s %= mod
                        if v3 == max_v:
                            s += s3
                            s %= mod
                        if board[i][j] != 'S':
                            max_v += int(board[i][j])
                        f.append([max_v, s])

            g = f[:]
            f = []

        return g[-1]
''',
    call=f'Solution().pathsWithMaxScore({B0!r})',
    expect=[4, 2],
    skip=['mod = ', 'm = len', 'n = len', 'f = []', 'g = []', 'f = []', 's1 = ', 's2 = ', 's3 = ', 'v1 = g[j][0]',
          'v2 = f[-1][0]', 'v3 = g[j - 1][0]', 's += s', 's %= mod', 'if i > 0 and g[j][1]', 'if j > 0 and f[-1][1]',
          'if i > 0 and j > 0'],
    views=[
        dict(type='grid', var='board', label='board（黄 = 当前格，红 = 障碍）', h=230, cell=70,
             cursors=[('i', 'j', 'yellow')], color=lambda S, i, j, v: 'red' if v == 'X' else None),
        dict(type='array', var='g', label='g：上一行每格的 [最大和, 方案数]', h=150, cell=110,
             fmt=lambda v: f'{v[0]},{v[1]}', pointers={'j': 'blue'}),
        dict(type='array', var='f', label='f：当前行已算出的格子', h=150, cell=110,
             fmt=lambda v: f'{v[0]},{v[1]}'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('v1 上', 'v1', 'cyan'), ('v2 左', 'v2', 'pink'), ('v3 左上', 'v3', 'purple'),
           ('max_v', 'max_v', 'orange'), ('s', 's', 'green')],
    max_steps=66,
    captions={
        "== 'X'": lambda S, B, r: (f'`board[{S.i}][{S.j}]` 是障碍 `X` → 记 `[0, 0]`：和 0、方案 0（到不了）'
                                   if S.board[S.i][S.j] == 'X' else f'`board[{S.i}][{S.j}] = {S.board[S.i][S.j]}` 不是障碍，继续判断'),
        "== 'E'": lambda S, B, r: ('`E` 是出发点（从左上往右下推）→ 初始化 `[0, 1]`：得分 0，方案 1' if S.board[S.i][S.j] == 'E'
                                   else f'`{S.board[S.i][S.j]}` 不是 `E`，是普通格或 `S` → 要看三个方向'),
        's = 0': '方案数累加器 `s` 从 0 开始，只累加和等于 `max_v` 的方向',
        'v1 = v2 = v3': '三个方向先都记 `-1`（不可达），能走再覆盖',
        'v1 = g[j][0]': '上方 `g[{j}]` 可达 → `v1 = {v1}`',
        'max_v = max': _src,
        'if max_v < 0': lambda S, B, r: ('三个方向都是 `-1` → 走不到这格 → 记 `[0, 0]`' if S.max_v < 0
                                         else f'`max_v = {S.max_v} >= 0`，至少一个方向走得通'),
        'if v1 == max_v': lambda S, B, r: (f'上方和 `{S.v1}` == 最大 `{S.max_v}` → 它的方案数 `{S.s1}` 计入' if S.v1 == S.max_v
                                           else f'上方和 `{S.v1}` ≠ 最大 `{S.max_v}` → 不计'),
        'if v2 == max_v': lambda S, B, r: (f'左方和 `{S.v2}` == 最大 `{S.max_v}` → 方案数 `{S.s2}` 也计入' if S.v2 == S.max_v
                                           else f'左方和 `{S.v2}` ≠ 最大 `{S.max_v}` → 不计'),
        'if v3 == max_v': lambda S, B, r: (f'左上和 `{S.v3}` == 最大 `{S.max_v}` → 方案数 `{S.s3}` 也计入' if S.v3 == S.max_v
                                           else f'左上和 `{S.v3}` ≠ 最大 `{S.max_v}` → 不计'),
        "!= 'S'": lambda S, B, r: (f'这格是数字 `{S.board[S.i][S.j]}` → 路径和再加上它' if S.board[S.i][S.j] != 'S' else '`S` 不加分'),
        'max_v += int': '`max_v` → {max_v}',
        'f.append([max_v, s])': '这格结果 `[最大和 {max_v}, 方案数 {s}]`',
        'g = f[:]': '这一行算完：`f` 成为下一行的「上一行」`g`，`f` 清空',
        'return g[-1]': lambda S, B, r: f'`g[-1]` 就是终点：最大得分 `{r[0]}`，方案数 `{r[1]}`',
    },
    cards=dict(
        one_liner='每格记 [最大和, 方案数]，三个方向里和最大的方案数相加',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['从右下 `S` 走到左上 `E`，可以向上、向左、向左上，不能进 `X`',
                 '得分 = 经过的数字之和；返回 `[最大得分, 方案数 % (1e9+7)]`',
                 '示例：`["E12","1X1","21S"]` → `[4,2]`；到不了返回 `[0,0]`'],
        quote='题目要求从右下角走到左上角，但是过程中并没有什么额外限制，因此我们可以认为问题是从左上角开始走到右下角。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j][0]` 最大得分，`f[i][j][1]` 对应方案数；障碍记 `[0, 0]`',
              '分别看上、左、左上：能走过来记 `v`、`s`，否则 `v = -1`',
              '取 `max(v1, v2, v3)`，只把等于最大值的那些方案数累加，再加上本格数字',
              '每行只依赖上一行，用 `g` 保存上一行、`f` 记当前行'],
        summary=['时间 `O(mn)`，空间 `O(n)`（只留两行）',
                 '易错：`S` 不加分；`v` 用 `-1` 标不可达，所以「和为 0」的合法格要靠方案数 `> 0` 判断',
                 '易错：累加方案数后要对 `mod` 取模',
                 '对比灵神：灵神用 `-inf` 表示不可达，yiduobo 用方案数是否为 0'],
    ),
)
