LAND = [[0, 2, 1, 0], [0, 1, 0, 1], [1, 1, 0, 1]]


def _col(S, i, j, v):
    if v == 1 and LAND[i][j] == 0:
        return 'green'
    return None


def _nb(S, B, r):
    i, j = S['_inner']['i'], S['_inner']['j']
    x, y = S['_inner']['x'], S['_inner']['y']
    m, n = S.m, S.n
    if (i, j) == (x, y):
        return f'`({i},{j})` 就是自己，已经标成访问过了 → 跳过'
    if not (0 <= i < m and 0 <= j < n):
        return f'`({i},{j})` 出界 → 跳过'
    if S.land[i][j] == 0:
        return f'`({i},{j})` 是没访问过的 0 → ==递归进去=='
    return f'`({i},{j})` 不是水域或已访问过 → 跳过'


CONFIG = dict(
    num='面试题 16.19', title='水域大小', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='八方向 DFS 求连通块大小',
    tags=['灵神核心路线', '灵神题单·网格图'],
    code='''
class Solution:
    def pondSizes(self, land: List[List[int]]) -> List[int]:
        m, n = len(land), len(land[0])

        def dfs(x: int, y: int) -> int:
            land[x][y] = 1  # 标记 (x,y) 被访问，避免重复访问
            cnt0 = 1
            # 访问八方向的 0
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if 0 <= i < m and 0 <= j < n and land[i][j] == 0:
                        cnt0 += dfs(i, j)
            return cnt0

        ans = []
        for i, row in enumerate(land):
            for j, x in enumerate(row):
                if x == 0:  # 从没有访问过的 0 出发
                    ans.append(dfs(i, j))
        ans.sort()
        return ans
''',
    call=f'Solution().pondSizes({LAND})',
    expect=[2, 3],
    skip=['m, n = len', 'cnt0 = 1', 'for i in range(x', 'for j in range(y', 'ans = []', 'for i, row', 'for j, x in'],
    max_steps=84,
    views=[
        dict(type='grid', var='land', label='land（绿 = 已访问的水域；蓝框 = 起点；黄框 = 当前 dfs；粉框 = 正在看的邻居）', cell=84, h=290,
             color=_col, cursors=[("i if 'y' not in _inner else None", 'j', 'blue'),
                                  ("x if 'y' in _inner else None", "y if 'y' in _inner else None", 'yellow'),
                                  ("i if 'y' in _inner and _line == 11 else None", 'j', 'pink')]),
        dict(type='calls', h=200),
        dict(type='array', var='ans', label='ans（每个池塘的大小）', cell=64, h=110),
    ],
    watch=[('ans', 'ans', 'green')],
    captions={
        'land[x][y] = 1': '到达水域 `({x},{y})`，先改成 `1` 标记访问过，避免来回无限递归',
        'if 0 <= i < m': _nb,
        'cnt0 += dfs': '递归进入邻居，它返回的池塘格数会累加到 `cnt0`',
        'return cnt0': '八个方向都看完，这一片池塘有 `cnt0` = =={cnt0}== 格',
        'if x == 0': lambda S, B, r: (f'`({S.i},{S.j})` 是没访问过的 0 → 新池塘，==从这里 DFS=='
                                      if S.x == 0 else f'`({S.i},{S.j})` 不是水域或已访问过，跳过'),
        'ans.append': '这个池塘大小 `{ans[-1]}` 记入答案：`ans = {ans}`',
        'ans.sort()': '题目要求从小到大返回，最后排序',
        'return ans': '返回所有池塘的大小 =={ans}==',
    },
    cards=dict(
        one_liner='八方向 DFS，每找到一片水域就数它有多大',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['矩阵 `land` 中 `0` 是水域，其余是海拔',
                 '垂直、水平或==对角==相连的水域是一个池塘',
                 '返回所有池塘的大小，从小到大排序',
                 '示例：`[[0,2,1,0],[0,1,0,1],[1,1,0,1]]` → `[2,3]`'],
        quote='从一个值为 0 格子出发，尝试移动到它的邻居，即周围八个方向相邻的格子。如果邻居是 0，就移动到邻居，然后按同样的方法移动到邻居的邻居。',
        quote_src='—— 灵茶山艾府题解',
        idea=['网格图 DFS 会重复访问，必须标记；这里直接把 `0` 改成 `1`',
              '`dfs` 返回从该格出发能连到的 0 的个数，累加得池塘大小',
              '每次从新的 0 出发就是一个新池塘，最后把答案排序'],
        summary=['时间瓶颈在排序：`O(mn log(mn))`',
                 '空间 `O(mn)`：蛇形池塘时递归栈最深',
                 '易错：八方向，枚举 `x-1..x+1`、`y-1..y+1` 时要判界',
                 '会修改输入 `land`；DFS 可换成 BFS，但要手写队列'],
    ),
)
