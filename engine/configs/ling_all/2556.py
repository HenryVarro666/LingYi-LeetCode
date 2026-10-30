G0 = [[1, 1, 1], [1, 0, 0], [1, 1, 1]]

CONFIG = dict(
    num=2556, title='二进制矩阵中翻转最多一次使路径不连通', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='贪心走下轮廓 + DFS 判断连通',
    tags=['灵神题单·网格图', '灵神题单·贪心与思维', '难度分 2369'],
    code='''
class Solution:
    def isPossibleToCutPath(self, g: List[List[int]]) -> bool:
        m, n = len(g), len(g[0])
        def dfs(x: int, y: int) -> bool:  # 返回能否到达终点
            if x == m - 1 and y == n - 1: return True
            g[x][y] = 0  # 直接修改
            return x < m - 1 and g[x + 1][y] and dfs(x + 1, y) or \\
                   y < n - 1 and g[x][y + 1] and dfs(x, y + 1)
        return not dfs(0, 0) or not dfs(0, 0)
''',
    call=f'Solution().isPossibleToCutPath({G0})',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: '橙色 = 原来是 1、已被「下轮廓」抹成 0 的格子；黄框 = 当前 dfs 所在格' if 'x' in S else '', h=50),
        dict(type='grid', var='g', cursors=[('x', 'y', 'yellow', '(x,y)')],
             color=lambda S, i, j, v: 'orange' if (v == 0 and G0[i][j] == 1) else None, h=300),
        dict(type='calls', h=200),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink')],
    skip=['m, n = len'],
    max_steps=70,
    captions={
        'if x == m - 1': lambda S, B, ret: (
            f'`({S.x},{S.y})` 就是终点 → 返回 `True`（终点不抹）' if (S.x == S.m - 1 and S.y == S.n - 1)
            else ('==第二次 dfs==：下轮廓已被抹成 0，再从起点走一遍，看还有没有通路' if (S.x == 0 and S.y == 0 and S.g[0][0] == 0)
                  else ('==第一次 dfs==：从 `(0,0)` 出发，优先向下走，得到下轮廓' if (S.x == 0 and S.y == 0) else f'`({S.x},{S.y})` 不是终点，继续走'))),
        'g[x][y] = 0': '把当前格子 `({x},{y})` ==直接改成 0==：走过的格子被抹掉（相当于标记「轮廓」）',
        'return x < m - 1 and g[x + 1][y]': lambda S, B, ret: (
            (f'第一优先：向下 `({B.x + 1},{B.y})` 值为 `{B.g[B.x + 1][B.y]}` → ==可走，先往下 dfs==' if (B.x < B.m - 1 and B.g[B.x + 1][B.y])
             else '向下走不通（越界或是 0）→ 看右边') if ret is None
            else f'这一层 dfs 返回 `{ret}`' + ('：已到达终点，一路返回 `True`' if ret else '：这条路走不通，往上回溯')),
        'y < n - 1 and g[x][y + 1]': lambda S, B, ret: (
            f'向右 `({B.x},{B.y + 1})`：' + ('值为 `1` → ==可走，往右 dfs==' if (B.y < B.n - 1 and B.g[B.x][B.y + 1]) else '越界或是 0 → 也走不通，返回 `False`')),
        'return not dfs(0, 0)': lambda S, B, ret: (
            '`not dfs() or not dfs()`：先走第一次，得到下轮廓' if ret is None else
            '第一次到得了终点 → `not True = False`；第二次到不了终点 → `not False = True`，==返回 True==：翻转轮廓上任一格即可断开' if ret else
            '返回 `False`：两次都走得通'),
    },
    cards=dict(
        one_liner='先贴着下边走一遍并抹掉，再看还能不能走通',
        complexity='时间 `O(mn)`，空间 `O(m+n)`（递归栈）',
        result='第二次 dfs 走不到终点 → `not False = True`：==可以断开==，返回 `True`',
        problem=['`m×n` 的 0/1 矩阵，只能向下或向右走到值为 `1` 的格子',
                 '最多翻转一个格子（起点终点除外），能否让 `(0,0)` 到不了 `(m-1,n-1)`？',
                 '示例：`[[1,1,1],[1,0,0],[1,1,1]]` → `true`'],
        quote='从 (0,0) 出发，优先向下走，其次向右走，得到下轮廓。如果两个轮廓有交集（除了起点终点），那么翻转交集中的任意一个格子，都可以使矩阵不连通。',
        quote_src='—— 灵茶山艾府题解',
        idea=['所有起终点路径的最上边是「上轮廓」，最下边是「下轮廓」',
              '能断开 ⇔ 两条轮廓相交于某个非端点格；翻掉它，上下轮廓都断了',
              '代码技巧：dfs 时把走过的格子改成 0，第一次得到下轮廓；第二次 dfs 还能走到终点，说明上轮廓不经过下轮廓 → 断不了'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`',
                 '`not dfs() or not dfs()`：第一次若已到不了终点，本来就不连通，直接 `true`',
                 '易错点：dfs 到终点时不要把终点改成 0，否则第二次永远走不到',
                 '「向下优先」只在只能向下/向右时成立；允许四个方向时需要别的做法（思考题）'],
    ),
)
