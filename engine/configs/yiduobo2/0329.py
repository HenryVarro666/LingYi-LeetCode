MAT = [[9, 8, 7], [4, 5, 6]]

CODE = '''
class Solution(object):
    def longestIncreasingPath(self, matrix):
        if not matrix:
            return 0

        m = len(matrix)
        n = len(matrix[0])

        f = [[None] * n for _ in range(m)]
        res = 0

        for i in range(m):
            for j in range(n):
                if f[i][j] is None:
                    res = max(res, self.dfs(i, j, matrix, f))

        return res

    def dfs(self, x, y, matrix, f):
        if f[x][y] is not None:
            return f[x][y]

        res = 1
        if x > 0 and matrix[x - 1][y] < matrix[x][y]:
            res = max(res, self.dfs(x - 1, y, matrix, f) + 1)
        if x < len(matrix) - 1 and matrix[x + 1][y] < matrix[x][y]:
            res = max(res, self.dfs(x + 1, y, matrix, f) + 1)
        if y > 0 and matrix[x][y - 1] < matrix[x][y]:
            res = max(res, self.dfs(x, y - 1, matrix, f) + 1)
        if y < len(matrix[0]) - 1 and matrix[x][y + 1] < matrix[x][y]:
            res = max(res, self.dfs(x, y + 1, matrix, f) + 1)
        f[x][y] = res
        return f[x][y]
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub, nth=0):
    return [i + 1 for i, s in enumerate(_LINES) if sub in s][nth]


DFS_DEF = _ln('def dfs')
DIRS = [('x > 0 and', -1, 0, '上'), ('x < len(matrix) - 1', 1, 0, '下'), ('y > 0 and', 0, -1, '左'),
        ('y < len(matrix[0]) - 1', 0, 1, '右')]
IF_LINES = {_ln(k): (dx, dy, nm) for k, dx, dy, nm in DIRS}


def _in_dfs(S):
    return S.get('_line', 0) > DFS_DEF


def _nbr(S):
    """当前这一步正在看的邻居"""
    ln = S.get('_line')
    if ln in IF_LINES and _in_dfs(S):
        dx, dy, _ = IF_LINES[ln]
        return S['x'] + dx, S['y'] + dy
    if ln - 1 in IF_LINES and _in_dfs(S):        # res = max(..., dfs(邻居)) 那一行
        dx, dy, _ = IF_LINES[ln - 1]
        return S['x'] + dx, S['y'] + dy
    return None, None


def _mat_color(S, i, j, v):
    f = S.get('f')
    if f is not None and f[i][j] is not None:
        return 'green'
    return None


def _if_cap(dx, dy, nm):
    def cap(S, B, ret):
        x, y = S.x, S.y
        nx, ny = x + dx, y + dy
        if not (0 <= nx < len(MAT) and 0 <= ny < len(MAT[0])):
            return f'{nm}边 `({nx},{ny})` ==出界==，跳过'
        a, b = MAT[nx][ny], MAT[x][y]
        if a < b:
            known = S.f[nx][ny]
            tail = f'，它的 f 已算出（`{known}`），直接用' if known is not None else '，递归去算它'
            return f'{nm}边 `{a} < {b}`：可以从 `({x},{y})` 走到 `({nx},{ny})`{tail}'
        return f'{nm}边 `{a} ≥ {b}`：不能往{nm}走'
    return cap


def _call_cap(S, B, ret):
    return f'`res = max(res, dfs({S.x},{S.y}) + 1)`：进入 `dfs({S.x},{S.y})`'


def _memo(S, B, ret):
    if S.f[S.x][S.y] is not None:
        return f'`f[{S.x}][{S.y}] = {S.f[S.x][S.y]}` ==已经算过==，记忆化直接返回'
    return f'`dfs({S.x},{S.y})`：`matrix = {MAT[S.x][S.y]}` 第一次搜到；`res = 1`（路径至少包含自己），看四个邻居'


CONFIG = dict(
    num=329, title='矩阵中的最长递增路径', difficulty='Hard', category='多维动态规划',
    author='yiduobo', technique='记忆化搜索：f[i][j] = 以 (i,j) 为起点的最长路径',
    tags=['字节30天', '热题173'],
    code=CODE,
    call=f'Solution().longestIncreasingPath({MAT})',
    expect=6,
    skip=['if not matrix', 'n = len(matrix[0])', 'for j in range(n)', 'f = [[None]', 'res = 1'],
    views=[
        dict(type='grid', var=lambda S: MAT, label='matrix（黄 = 当前 dfs 格，粉 = 正在看的邻居，绿 = f 已算出）', cell=100, h=230,
             cursors=[(lambda S: S['x'] if _in_dfs(S) else None, lambda S: S['y'] if _in_dfs(S) else None, 'yellow'),
                      (lambda S: _nbr(S)[0], lambda S: _nbr(S)[1], 'pink')],
             color=_mat_color),
        dict(type='grid', var='f', label='f（以该格为起点、往更小的数走，最多几个格子；· = 未算）', cell=84, h=194,
             cursors=[(lambda S: S['x'] if _in_dfs(S) else None, lambda S: S['y'] if _in_dfs(S) else None, 'yellow')],
             color=lambda S, i, j, v: 'green' if v is not None else None),
        dict(type='calls', label='递归调用栈', hide=('matrix', 'f'), h=210),
    ],
    watch=[('外层 (i,j)', lambda S: (S['i'], S['j'])), ('dfs (x,y)', lambda S: (S['x'], S['y']) if _in_dfs(S) else None, 'blue'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        'm = len(matrix)': '矩阵 `{m}` 行 `{len(matrix[0])}` 列',
        'res = 0': '`res`：全局答案',
        'for i in range(m)': lambda S, B, ret: (f'外层扫描第 `{S.i}` 行' if S.get('i') != B.get('i') else '所有格子都扫描过了'),
        'if f[i][j] is None': lambda S, B, ret: (f'`({S.i},{S.j})` 还没算过 → 以它为起点 dfs' if S.f[S.i][S.j] is None
                                                  else f'`f[{S.i}][{S.j}] = {S.f[S.i][S.j]}` 已在之前的搜索中算好，跳过'),
        'res = max(res, self.dfs(i, j, matrix, f))': lambda S, B, ret: f'调用 `dfs({S.x},{S.y})`，结果和 `res` 取最大',
        'if f[x][y] is not None': _memo,
        'return f[x][y]': lambda S, B, ret: (f'记忆化命中：直接返回 `{ret}`，==不再重复搜索==' if S._line == _ln('return f[x][y]')
                                             else f'返回 `f[{S.x}][{S.y}] = {ret}` 给上一层，上一层拿它 +1' if (S.x, S.y) != (S.i, S.j)
                                             else f'以 `({S.x},{S.y})` 为起点的搜索结束：返回 `{ret}`，外层和 `res` 取最大'),
        'f[x][y] = res': '四个方向都看完：`f[{x}][{y}] = {res}`（==记下来，以后直接用==）',
        'return res': '全部起点都试过，最长递增路径长度 =={ret}==',
    },
    max_steps=75,
    cards=dict(
        one_liner='f[i][j] = 以 (i,j) 为起点的最长路径，往更小的邻居走，记忆化搜索',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 整数矩阵，每步可以上下左右移动（不能斜走、不能出界）',
                 '求==严格递增==路径的最长长度',
                 '示例：`[[9,9,4],[6,6,8],[2,1,1]]` → `4`（`1→2→6→9`）',
                 '本视频：`[[9,8,7],[4,5,6]]` → `6`（`4→5→6→7→8→9`）'],
        quote='经典的记忆化搜索问题，设==f[i][j]表示以matrix[i][j]为起点的路径最长可以有多长==，那么对于其上、下、左、右这四个点，若满足在矩阵之内，且值小于matrix[i][j]，那么说明matrix[i][j]接下来可以往这里走。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j] = max(f[x][y]) + 1`，`(x,y)` 是四个方向上==更小==的邻居',
              '没有更小的邻居时 `f = 1`；从大往小走，倒过来就是递增路径',
              '每个格子只搜一次（`f` 不为 `None` 直接返回），所以是 `O(mn)`'],
        result='`f[0][0] = 6`：从 9 出发一路往小走 `9→8→7→6→5→4` ✓',
        summary=['时间 `O(mn)`：每格只算一次，每次看 4 个邻居；空间 `O(mn)`（含递归栈）',
                 '为什么不用 visited？路径严格单调，==不可能走回头路==，不会成环',
                 '也可以按值建有向图做拓扑排序，同样 `O(mn)`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)

for _ln_no, (_dx, _dy, _nm) in IF_LINES.items():
    CONFIG['captions'][_ln_no] = _if_cap(_dx, _dy, _nm)
    CONFIG['captions'][_ln_no + 1] = _call_cap
