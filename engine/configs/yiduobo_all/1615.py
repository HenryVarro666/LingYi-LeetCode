def _rank(S):
    if 'x' not in S or 'y' not in S:
        return '先记录每个点的度 `s` 和点对之间是否直接相连 `g`'
    x, y = S['x'], S['y']
    if S['_line'] >= 14 and 'g' in S:
        return f'点 `{x}` 与点 `{y}`：`{S["s"][x]} + {S["s"][y]} − {S["g"][x][y]}` = =={S["s"][x] + S["s"][y] - S["g"][x][y]}=='
    return f'点 `{x}` 与点 `{y}`'


def _color(S, i, j, v):
    if 'x' in S and 'y' in S and 'res' in S and i == S['x'] and j == S['y']:
        return 'yellow'
    return 'blue' if v else None


CONFIG = dict(
    num=1615, title='最大网络秩', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='度数 + 邻接矩阵 · 枚举点对',
    tags=[],
    code='''
class Solution(object):
    def maximalNetworkRank(self, n, roads):

        g = [[0] * n for _ in range(n)]
        s = [0] * n
        for x, y in roads:
            g[x][y] = 1
            g[y][x] = 1
            s[x] += 1
            s[y] += 1

        res = 0
        for x in range(n - 1):
            for y in range(x + 1, n):
                res = max(res, s[x] + s[y] - g[x][y])
        
        return res
''',
    call='Solution().maximalNetworkRank(4, [[0,1],[0,3],[1,2],[1,3]])',
    expect=4,
    views=[
        dict(type='grid', var='g', label='g（邻接矩阵：蓝 = 两点之间有路；黄 = 正在算的点对）', cell=84, h=330,
             color=_color, cursors=[('x', 'y', 'yellow')]),
        dict(type='array', var='s', label='s（每个点的度）', cell=90, h=170, pointers={'x': 'blue', 'y': 'pink'}),
        dict(type='text', h=90, size=30, fn=_rank),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('res', 'res', 'green')],
    captions={
        'g = [[0]': '`g[x][y] = 1` 表示 x、y 之间直接有路，先全置 0',
        's = [0]': '`s[x]` 记录点 x 的度（连了几条路）',
        'for x, y in roads': lambda S, B, r: ('所有道路处理完，度数与邻接矩阵都记好了' if B.get('x') == S.x and B.get('y') == S.y and B.get('s') == S.s else f'处理一条路 `({S.x}, {S.y})`'),
        'g[x][y] = 1': '`g[{x}][{y}] = 1`：记下 {x}、{y} 相连',
        'g[y][x] = 1': '无向图，反过来也记：`g[{y}][{x}] = 1`',
        's[x] += 1': '点 {x} 多了一条路：`s[{x}]` → {s[x]}',
        's[y] += 1': '点 {y} 多了一条路：`s[{y}]` → {s[y]}',
        'res = 0': '`res` 记录最大网络秩',
        'for x in range': '枚举第一个点：`x` 取 0 到 {n - 2}，当前 `x = {x}`',
        'for y in range': '`x = {x}` 的搭档：`y` 取 {x + 1} 到 {n - 1}，当前 `y = {y}`（每对只算一次）',
        'res = max': lambda S, B, r: (f'两点度之和 `{S.s[S.x]} + {S.s[S.y]}`，'
                                      + ('直接相连，那条路被算了两次，要 ==减 1==' if S.g[S.x][S.y] else '不相连，不用减')
                                      + f'：秩 `{S.s[S.x] + S.s[S.y] - S.g[S.x][S.y]}`，`res` = =={S.res}=='),
        'return res': '所有点对枚举完，最大网络秩 =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='点很少，直接两两枚举：度之和，相连就减 1',
        complexity='时间 `O(n² + m)`，空间 `O(n²)`',
        problem=['`n` 个城市和 `roads` 无向道路；两城市的网络秩 = 与它们相连的道路总数',
                 '同时连着两城市的那条路只算一次；求所有点对的最大网络秩',
                 '本视频：`n=4`，`roads=[[0,1],[0,3],[1,2],[1,3]]` → `4`'],
        quote='直接记录每个点的度以及点对之间相连的情况，然后两两枚举点对。若两个点相连，那么此时的秩就是这两个点度的和减1，若不相连那么就是这两个点度的和。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍 `roads`：`s` 统计度，`g` 记录是否直接相连',
              '点对 `(x, y)` 的秩 = `s[x] + s[y]`，若相连，公共那条路重复计数，减 `g[x][y]`',
              '`n` 很小，二重循环枚举所有点对取最大值'],
        summary=['时间 `O(n² + m)`，空间 `O(n²)`',
                 '易错：相连的两点要减 1，只减一次（`g` 是 0/1，重边题目不会出现）',
                 '`y` 从 `x + 1` 开始，每个点对只枚举一次',
                 '原文为 Python 2 风格，本题无需改动'],
    ),
)
