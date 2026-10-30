GR = [[0, 1, 0, 0], [2, 0, 2, 0], [0, 0, 0, 0], [0, 0, 2, 1]]
DN = ['右下', '左下', '左上', '右上']


def _gcol(S, i, j, v):
    if v == 1:
        return 'green'
    if v == 0:
        return None
    return None


def _txt(S):
    if S.get('_line', 0) < 8 or 'target' not in S.get('_inner', {}) and S['_line'] > 19:
        return '合法线段：从 `1` 出发，依次 `2, 0, 2, 0, ...`，最多右转 90° 一次'
    inn = S.get('_inner', {})
    if 'target' in inn:
        return f"沿 ==DIRS[{inn['k']}]（{DN[inn['k']]}）== 走，下一格必须是 `{inn['target']}`；{'还可以右转一次' if inn['can_turn'] else '已经转过弯，只能直行'}"
    return '合法线段：从 `1` 出发，依次 `2, 0, 2, 0, ...`，最多右转 90° 一次'


CONFIG = dict(
    num=3459, title='最长 V 形对角线段的长度', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索 · 方向 + 能否右转 + 最优性剪枝',
    tags=['灵神题单', '网格图 DP', '难度分 2337'],
    code='''
class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        DIRS = (1, 1), (1, -1), (-1, -1), (-1, 1)
        m, n = len(grid), len(grid[0])

        @cache
        def dfs(i: int, j: int, k: int, can_turn: bool, target: int) -> int:
            i += DIRS[k][0]
            j += DIRS[k][1]
            if not (0 <= i < m and 0 <= j < n) or grid[i][j] != target:
                return 0
            res = dfs(i, j, k, can_turn, 2 - target) + 1
            if can_turn:
                maxs = (m - i, j + 1, i + 1, n - j)  # 理论最大值（走到底）
                k = (k + 1) % 4
                # 优化二：如果理论最大值没有超过 res，那么不递归
                if min(maxs[k], maxs[k - 1]) > res:
                    res = max(res, dfs(i, j, k, False, 2 - target) + 1)
            return res

        ans = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x != 1:
                    continue
                maxs = (m - i, j + 1, i + 1, n - j)  # 理论最大值（走到底）
                for k, mx in enumerate(maxs):  # 枚举起始方向
                    # 优化一：如果理论最大值没有超过 ans，那么不递归
                    if mx > ans:
                        ans = max(ans, dfs(i, j, k, True, 2) + 1)
        return ans
''',
    call=f'Solution().lenOfVDiagonal({GR})',
    expect=4,
    skip=['for i, row', 'for j, x', 'if x != 1', 'continue', 'i += DIRS', 'DIRS = ', 'm, n = len', 26, 'for k, mx'],
    max_steps=110,
    views=[
        dict(type='text', fn=_txt, size=22, h=60),
        dict(type='grid', var='grid', label='grid（绿 = 1；黄 = 当前所在格子（dfs 里是刚走到的格））', cell=64, h=330,
             color=_gcol, cursors=[('i if 0 <= i < m and 0 <= j < n else None', 'j', 'yellow', '')]),
        dict(type='calls', h=220),
    ],
    watch=[('ans', 'ans', 'green'), ('res', 'res', 'blue'), ('k', 'k')],
    captions={
        'ans = 0': '`ans = 0`：枚举每个 `1` 当起点，向 4 个对角方向试，记最长线段',
        'j += DIRS': lambda S, B, r: f'向 `DIRS[{S.k}]`（{DN[S.k]}）走一步 → 现在看格子 `({S.i},{S.j})`，目标值 `{S.target}`',
        'if not (0 <= i < m': lambda S, B, r: (f'`({S.i},{S.j})` 出界 → 走不下去' if not (0 <= S.i < S.m and 0 <= S.j < S.n)
                                               else (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` ≠ 目标 `{S.target}` → 走不下去' if S.grid[S.i][S.j] != S.target
                                                     else f'`grid[{S.i}][{S.j}] = {S.target}` 符合 → 能走')),
        'return 0': '这一步走不通：这条线段到此为止，返回 `0`',
        'res = dfs(i, j, k, can_turn, 2 - target) + 1': '==直行==：沿同一方向继续，下一格目标是 `2 - {target} = {2 - target}`（2 和 0 交替）；返回后加这一步 `+ 1`',
        'if can_turn': lambda S, B, r: ('还没转过弯 → 可以在这里右转' if S.can_turn else '已经转过弯 → 不能再转'),
        'maxs = (m - i': lambda S, B, r: f'理论最大值 `maxs` = {tuple(S.maxs)}：沿四个对角方向“走到底”最多能访问的格子数（下/左/上/右边缘）',
        'k = (k + 1) % 4': '==右转==：方向换成下一个（顺时针 90°），`k = {k}`（{DN[k]}）',
        'if min(maxs[k]': lambda S, B, r: (f'优化二：右转后最多还能走 `min({S.maxs[S.k]}, {S.maxs[S.k-1]}) = {min(S.maxs[S.k], S.maxs[S.k-1])}`，'
                                           + (f'大于当前 `res = {S.res}` → 值得递归' if min(S.maxs[S.k], S.maxs[S.k-1]) > S.res else f'不超过 `res = {S.res}` → 剪枝，不递归')),
        'res = max(res, dfs(i, j, k, False, 2 - target) + 1)': '右转后继续走（`can_turn = False`，不能再转）：`res = max(直行, 右转)`',
        'return res': '这一段从这里往后最多还能走 `res = {res}` 步（含这一步）',
                'if mx > ans': lambda S, B, r: (f'起点 `({S.i},{S.j})`，方向 `{S.k}`（{DN[S.k]}）：走到底最多 `{S.mx}` 格，'
                                        + (f'大于 `ans = {S.ans}` → 值得试' if S.mx > S.ans else f'不超过 `ans = {S.ans}` → 剪枝，不用搜')),
        'ans = max(ans, dfs': lambda S, B, r: f'从起点 `({S.i},{S.j})` 往 {DN[S.k]} 搜：`dfs` 返回的是起点之后的步数，`+ 1` 把起点算上，再和 `ans` 取最大',
        'return ans': '所有起点、方向都试完：最长 V 形线段 `{ans}`',
    },
    cards=dict(
        one_liner='模拟人在网格上走：记「方向 + 能否右转」，目标值 2、0 交替',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里是 `0/1/2`；线段从 `1` 开始，后面依次 `2,0,2,0...`',
                 '沿一个对角方向走，最多顺时针转 90° 一次，求最长长度',
                 '题目示例 1 答案是 `5`（`(0,2)→(1,3)→(2,4)` 转弯 `→(3,3)→(4,2)`）',
                 '本视频用 4×4：`[[0,1,0,0],[2,0,2,0],[0,0,0,0],[0,0,2,1]]` → `4`'],
        quote='想象有一个人在网格图上移动，按照题目要求，移动经过的值必须为 1,2,0,2,0,…。由于至多转弯一次，所以移动路径不会形成环，可以写一个记忆化搜索，模拟人在网格图上的移动。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j,k,can_turn,target)`：上一步在 `(i,j)`，朝 `DIRS[k]` 走，下一格必须是 `target`',
              '直行继续；`can_turn` 时右转：`(k+1)%4`，且之后不能再转',
              '`target` 用 `2 - target` 在 2、0 之间切换，且由 `(i,j,k)` 唯一确定，不用记忆化',
              '再加两个最优性剪枝：理论最大值不超过当前答案就不递归'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（状态数 = 格子 × 4 方向 × 是否转弯）',
                 '易错：`dfs` 里“上一步位置”要先 `+= DIRS[k]`，出界或值不等于 `target` 就返回 `0`',
                 '起点自己要 `+ 1`；方向用环形数组，`(k+1)%4` 就是顺时针右转',
                 '灵神还给了不带剪枝的写法（优化前），本视频演示带两个剪枝的版本'],
    ),
)
