M = [[2, -1, 3], [4, 5, -2], [3, 6, 1]]


def _mcol(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') not in range(14, 21):
        return None
    if r == i - 1 and abs(c - j) <= 1:
        return 'blue'
    return None


def _fcol(S, r, c, v):
    flag, j = S.get('flag'), S.get('j')
    if flag is None or j is None or S.get('_line') not in range(14, 21):
        return None
    if r == flag and c == j:
        return 'yellow'
    if r == 1 - flag and abs(c - j) <= 1:
        return 'blue'
    return None


def _text(S):
    if S.get('flag') is None or S.get('i') is None or S.get('_line') not in range(12, 21):
        return '`f[i][j]`：以第 i 层第 j 个数==结尾==的下降路径最小和；只留两行滚动'
    fl = S['flag']
    return f"上一层在 `f[{1 - fl}]`，当前第 `{S['i']}` 层写进 `f[{fl}]`"


def _left(S, B, ret):
    if S.j > 0:
        return f'`j = {S.j} > 0`：还能从上一层的 ==j − 1==（左上）过来'
    return '`j = 0`：最左边，没有左上方'


def _right(S, B, ret):
    n = S.n
    if S.j < n - 1:
        return f'`j = {S.j} < n − 1`：还能从上一层的 ==j + 1==（右上）过来'
    return f'`j = {S.j} = n − 1`：最右边，没有右上方'


CONFIG = dict(
    num=931, title='下降路径最小和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP · 两行滚动数组',
    tags=['labuladong', '灵神核心路线', '难度分 1573'],
    code='''
class Solution(object):
    def minFallingPathSum(self, matrix):

        n = len(matrix)
        f = [[0] * n for _ in range(2)]

        for i in range(n):
            f[0][i] = matrix[0][i]

        flag = 0
        for i in range(1, n):
            flag = 1 - flag
            for j in range(n):
                tmp = f[1 - flag][j]
                if j > 0:
                    tmp = min(tmp, f[1 - flag][j - 1])
                if j < n - 1:
                    tmp = min(tmp, f[1 - flag][j + 1])
                f[flag][j] = tmp + matrix[i][j]

        return min(f[flag])
''',
    call=f'Solution().minFallingPathSum({M!r})',
    expect=-2,
    skip=['for j in range(n)', 'for i in range(n)'],
    views=[
        dict(type='grid', var='matrix', label='matrix（黄框 = 第 i 层第 j 个，蓝 = 能走过来的上一层位置）', h=330, cell=90,
             cursors=[(lambda S: S.get('i') if S.get('_line') in range(14, 21) else None, 'j', 'yellow')], color=_mcol),
        dict(type='text', fn=_text, size=26, h=60),
        dict(type='table', var='f', label='f（两行滚动：黄 = 正在写，蓝 = 上一层的候选）', h=250, cell=90,
             rows=['0', '1'], color=_fcol),
    ],
    watch=['i', 'j', ('flag', 'flag', 'purple'), ('tmp', 'tmp', 'cyan')],
    captions={
        'n = len(matrix)': '`n = {n}`',
        'f = [[0] * n': '只开 ==2 行==：每一层的状态只和上一层有关',
        'f[0][i] = matrix[0][i]': '第 0 层：路径只有自己，`f[0][{i}] = {f[0][i]}`',
        'flag = 0': '`flag` 指向当前层所在的行，`1 − flag` 是上一层',
        'for i in range(1, n)': lambda S, B, r: (f'开始第 `{S.i}` 层' if B.get('i') != S.i else '所有层算完'),
        'flag = 1 - flag': '`flag = {flag}`：当前层写到 `f[{flag}]`，上一层在 `f[{1 - flag}]`',
        'tmp = f[1 - flag][j]': '任何情况下都能从上一层的 ==j==（正上）过来：`tmp = {tmp}`',
        'if j > 0': _left,
        'tmp = min(tmp, f[1 - flag][j - 1])': '`tmp = min({B.tmp}, {f[1-flag][j-1]}) = {tmp}`',
        'if j < n - 1': _right,
        'tmp = min(tmp, f[1 - flag][j + 1])': '`tmp = min({B.tmp}, {f[1-flag][j+1]}) = {tmp}`',
        'f[flag][j] = tmp + matrix': '`f[{flag}][{j}] = {tmp} + {matrix[i][j]}` = =={f[flag][j]}==',
        'return min(f[flag])': '最后一层 `f[{flag}]` 的最小值就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='每个位置先从正上方来，再看左上、右上能不能更小',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n × n` 矩阵，从第一行任一格出发，每次走到下一行的==左下、正下、右下==',
                 '求下降路径上元素和的最小值',
                 '示例：`[[2,1,3],[6,5,4],[7,8,9]]` → `13`',
                 f'本视频：`{M}` → `-2`（`-1 → -2 → 1`）'],
        quote='在任何情况下，当前层的位置j都可以从上一层的j过来……若此时的j > 0，那么当前位置j可以从上一层的j - 1过来……',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 先取 `f[i-1][j] + matrix[i][j]`',
              '`j > 0` 再和左上比，`j < n − 1` 再和右上比，用边界判断代替哨兵',
              '只与上一层有关 → 两行滚动数组，`flag` 来回切换'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：滚动数组要分清 `f[flag]`（当前层）和 `f[1 − flag]`（上一层）',
                 '答案是==最后一层==的最小值，不是 `f[flag][n-1]`',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神从下往上思考、两端放 ∞ 哨兵，一维数组 + `pre`'],
    ),
)
