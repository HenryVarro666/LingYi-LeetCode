M = [[2, 1, 3], [6, 5, 4], [7, 8, 9]]


def _ri(S):
    row = S.get('row')
    if row is None:
        return None
    return next(k for k, rr in enumerate(M) if rr == row)


def _r(S):
    return _ri(S) if S.get('_line') in (7, 8) else None


def _fcol(S, i, v):
    line = S.get('_line')
    if 'c' not in S or line != 8:
        return None
    c = S['c']
    if i == c + 1:
        return 'yellow'
    if 1 <= i <= c:
        return 'green'
    return None


def PC(S):
    return S['c'] + 1 if S.get('_line') == 8 else None


def _text(S, B):
    if S.get('_line') == 8:
        c, x = S['c'], S['x']
        bf = B['f']
        a, b, d = B['pre'], bf[c + 1], bf[c + 2]
        fm = lambda v: '∞' if v == inf else str(v)
        return f"`f[{c + 1}] = min({fm(a)}, {fm(b)}, {fm(d)}) + {x}` = =={S['f'][c + 1]}==（左上、正上、右上）"
    return '`f[c+1]`：从 `matrix[r][c]` 往上走到第一行的最小路径和；两端 ∞ 是哨兵'


CONFIG = dict(
    num=931, title='下降路径最小和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='网格图 DP · 一维数组空间优化',
    tags=['labuladong', '灵神核心路线', '难度分 1573'],
    code='''
class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        n = len(matrix)
        f = [inf] + matrix[0] + [inf]
        for row in matrix[1:]:
            pre = f[0]  # 充当 f[c]
            for c, x in enumerate(row):
                pre, f[c + 1] = f[c + 1], min(pre, f[c + 1], f[c + 2]) + x
        return min(f)
''',
    call=f'Solution().minFallingPathSum({M!r})',
    expect=13,
    views=[
        dict(type='grid', var='matrix', label='matrix（黄框 = 正在计算的格子）', h=330, cell=90,
             cursors=[(_r, 'c', 'yellow')],
             color=lambda S, i, j, v: 'green' if _r(S) is not None and i == _r(S) - 1 and abs(j - S['c']) <= 1 else None),
        dict(type='text', fn=_text, size=26, h=60),
        dict(type='array', var='f', label='f（绿 = 已更新为当前行，其余仍是上一行）', h=200, cell=90,
             color=_fcol, pointers={PC: 'pink'}, pointer_labels={PC: 'c+1'}),
    ],
    watch=['n', ('pre', 'pre', 'cyan'), 'c', 'x'],
    captions={
        'n = len(matrix)': '`n = {n}`',
        'f = [inf]': '第一行：`f[c+1] = matrix[0][c]`；左右各加一个 ==∞ 哨兵==，代表出界',
        'for row in matrix[1:]': lambda S, B, r: (f'开始第 `{_ri(S)}` 行 `{S.row}`：只用到上一行的 f' if B.get('row') != S.get('row')
                                                 else '所有行算完，f 里存的是最后一行的结果'),
        'pre = f[0]': '`pre` 暂存上一行的 `f[c]`（左上方），防止被当前行覆盖',
        'for c, x in': lambda S, B, r: ('这一行算完，f 现在整体代表当前行' if B.get('c') == S.c and B.get('x') == S.x
                                        else f'`c = {S.c}`，`x = matrix[{_ri(S)}][{S.c}] = {S.x}`'),
        'pre, f[c + 1]': lambda S, B, r: (f'三个方向取最小 + `{S.x}` → `f[{S.c + 1}] = {S.f[S.c + 1]}`；'
                                          f'同时 `pre` 存下旧的 `f[{S.c + 1}] = {S.pre}`，留给下一列当左上方'),
        'return min(f)': '最后一行的 f 取最小（哨兵 ∞ 不影响）= =={ret}==',
    },
    cards=dict(
        one_liner='从下往上看：dfs(r,c) = 三个上方格子的最小值 + 自己',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n × n` 矩阵，从第一行任一格出发，每次走到下一行的==左下、正下、右下==',
                 '求下降路径上元素和的最小值',
                 f'示例 / 本视频：`{M}` → `13`（`1→5→7`）'],
        quote='dfs(r,c) = min(dfs(r−1,c−1), dfs(r−1,c), dfs(r−1,c+1)) + matrix[r][c]……==出界是不合法的，设置成无穷大==，这样取 min 的时候就会自动忽略不合法的情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举选哪个：从 `(r,c)` 往上走一步，有三个子问题',
              '1:1 翻译成递推，`f` 左右各加一列 ∞ 表示出界，下标整体 `+1`',
              '只依赖上一行 → 一维 `f`，用 `pre` 暂存被覆盖的左上方'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：原地更新会覆盖 `f[c]`，必须先用 `pre` 存下来',
                 '易错：`matrix` 有负数，记忆化的初始值不能用 0 或 -1',
                 '题解还给了递归、`@cache` 记忆化、二维 `f` 递推三种写法，本视频用最后的空间优化版'],
    ),
)
