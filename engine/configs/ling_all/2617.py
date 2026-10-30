GRID = [[2, 2, 1], [1, 1, 0]]


def _stk(st, axis):
    if not st:
        return '空'
    return '  '.join(f'{v}格@{axis}{-k}' for v, k in st)


def _stacks(S):
    cs = S.get('col_stacks')
    if cs is None:
        return ''
    rs = S.get('row_st')
    top = '当前行单调栈（栈底→栈顶：f 递增，下标递减）：' + (_stk(rs, '列') if rs is not None else '—')
    cols = '每列单调栈：' + '   |   '.join(f'列{j}: ' + _stk(c, '行') for j, c in enumerate(cs))
    return top + '\n' + cols


def _cell(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if ci is None or cj is None:
        return None
    if (i, j) == (ci, cj):
        return 'yellow'
    g = S['grid'][ci][cj]
    if g and ((i == ci and cj < j <= cj + g) or (j == cj and ci < i <= ci + g)):
        return 'blue'
    if i > ci or (i == ci and j > cj):
        return 'green'
    return None


def _bis(S, B, ret):
    kind = '行' if 'row_st' in S['_line_src'] else '列'
    return ''


def _row_q(S, B, r):
    g, j = S.g, S.j
    k = S.k
    if k < len(S.row_st):
        return f'在行栈里二分：要下标 `<= {j + g}` 的最大者，找到 `{S.row_st[k][0]}` 格 @ 列 {-S.row_st[k][1]} '
    return f'行栈里没有下标落在 `[{j + 1}, {j + g}]` 的格子 → 这一行跳不出去'


def _col_q(S, B, r):
    g, i = S.g, S.i
    k = S.k
    if k < len(S.col_st):
        return f'在列栈里二分：要下标 `<= {i + g}` 的最大者，找到 `{S.col_st[k][0]}` 格 @ 行 {-S.col_st[k][1]} '
    return f'列栈里没有下标落在 `[{i + 1}, {i + g}]` 的格子 → 这一列跳不出去'


CONFIG = dict(
    num=2617, title='网格图中最少访问的格子数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='单调栈优化 DP + 二分',
    tags=['网格图', '动态规划', '难度分 2582'],
    code='''
class Solution:
    def minimumVisitedCells(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        col_stacks = [[] for _ in range(n)]  # 每列的单调栈
        for i in range(m - 1, -1, -1):
            row_st = []  # 当前行的单调栈
            for j in range(n - 1, -1, -1):
                g = grid[i][j]
                col_st = col_stacks[j]
                mn = inf if i < m - 1 or j < n - 1 else 1
                if g:  # 可以向右/向下跳
                    # 在单调栈上二分查找最优转移来源
                    k = bisect_left(row_st, -(j + g), key=lambda p: p[1])
                    if k < len(row_st):
                        mn = row_st[k][0] + 1
                    k = bisect_left(col_st, -(i + g), key=lambda p: p[1])
                    if k < len(col_st):
                        mn = min(mn, col_st[k][0] + 1)
                if mn < inf:
                    # 插入单调栈
                    while row_st and mn <= row_st[-1][0]:
                        row_st.pop()
                    row_st.append((mn, -j))  # 保证下标单调递增，方便调用 bisect_left
                    while col_st and mn <= col_st[-1][0]:
                        col_st.pop()
                    col_st.append((mn, -i))  # 保证下标单调递增，方便调用 bisect_left
        return mn if mn < inf else -1  # 最后一个算出的 mn 就是 f[0][0]
''',
    call=f'Solution().minimumVisitedCells({GRID})',
    expect=3,
    skip=['m, n = len', 'col_stacks = [', 'row_st = []', 'col_st = col_stacks', 'g = grid[i][j]', 'if k < len(', 'if mn < inf:', 'for j in range(n - 1', 'mn = inf if', 'col_st.append'],
    max_steps=100,
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前格 (i,j)，蓝 = 它能跳到的格子，绿 = 已算过 f 的格子）', cell=110, h=330,
             color=_cell, cursors=[('i', 'j', 'yellow')]),
        dict(type='text', fn=_stacks, size=22, h=150),
        dict(type='text', fn=lambda S: (f"`f[{S['i']}][{S['j']}]` = 从 `({S['i']},{S['j']})` 到终点的最少格子数 = =={S['mn']}==" if S.get('mn') not in (None,) and S['mn'] != float('inf') and S.get('_line', 0) >= 21 else '`f[i][j]` = 从 `(i,j)` 走到右下角经过的最少格子数；倒序枚举'), size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'g', ('mn', 'mn', 'green'), 'k'],
    captions={
        'mn = inf if': lambda S, B, r: ('终点 `(m-1,n-1)` 本身：`mn = 1`（只经过自己这 1 格）' if S.mn == 1
                                        else '先假设到不了终点：`mn = inf`'),
        'if g:': lambda S, B, r: ('终点 `(m-1,n-1)`：`mn = 1`，只经过自己这 1 格；' if S.mn == 1 else '') + (f'`g = {S.g}`：能向右、向下各跳 `1..{S.g}` 格，去栈里找最优来源' if S.g
                                  else '`g = 0` 哪也去不了，不用查栈'),
        'k = bisect_left(row_st': _row_q,
        'k = bisect_left(col_st': _col_q,
        'mn = row_st[k][0] + 1': '向右跳到那一格再 +1：`mn = {mn}`',
        'mn = min(mn, col_st': '向下跳的结果和向右比，取小：`mn = {mn}`',
        'while row_st and mn <=': lambda S, B, r: (f'行栈顶 `{S.row_st[-1][0]} >= mn = {S.mn}`：新格子更靠左又不更差 → ==旧的永远不会比它优==，弹出'
                                                   if S.row_st and S.mn <= S.row_st[-1][0] else '栈顶比新值小，保留，不再弹'),
        'row_st.append': '`({mn}, 列 {j})` 入行栈：栈里 f 严格递增，下标一路变小',
        'while col_st and mn <=': lambda S, B, r: (f'列栈顶 `{S.col_st[-1][0]} >= mn = {S.mn}`：新格子更靠上又不更差 → 弹出旧的'
                                                   if S.col_st and S.mn <= S.col_st[-1][0] else '列栈顶比新值小，保留'),
        'col_st.append': '`({mn}, 行 {i})` 入第 {j} 列的栈',
        'return mn if': lambda S, B, r: (f'最后算出的 `mn` 就是 `f[0][0] = {r}`' if r != -1 else '`mn` 是 inf → 到不了，返回 -1'),
    },
    cards=dict(
        one_liner='倒着算 f，用单调栈 + 二分找「跳得到的最小 f」',
        complexity='时间 `O(mn(log m + log n))`，空间 `O(mn)`',
        problem=['`grid[i][j]` 是在 `(i,j)` 最多能向右或向下跳的格数',
                 '从左上角出发，求到右下角==最少经过几个格子==，到不了返回 `-1`',
                 '示例：`[[3,4,2,1],[4,2,3,1],[2,1,0,0],[2,4,0,0]]` → `4`；本视频用 2×3 小例子'],
        quote='右边界没有单调性。联想到滑动窗口最小值的做法，我们用一个 f 值底小顶大的==单调栈==来维护 f[i][j] 及其下标 j……在单调栈上==二分查找==最大的不超过 j+g 的下标 k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]` = 从 `(i,j)` 到终点的最少格子数，转移是对一段区间取 min，+1',
              '倒着枚举 j，左边界天然单调，所以能用单调栈：新来的更靠左、f 不更大，就把旧的弹掉',
              '栈里下标单调，`bisect_left` 一次二分就找到区间内最优的来源；每行一个栈、每列一个栈'],
        summary=['时间 `O(mn(log m + log n))`：每个格子入栈出栈各一次，再做两次二分',
                 '栈里存 `(f, -下标)`：取负是为了让下标递增，才能直接用 `bisect_left(key=...)`（Python 3.10+）',
                 '终点要特判 `mn = 1`；`g = 0` 的格子不能转移，但它自己仍可能被别人跳到',
                 '另一种写法：灵神还给了「贪心 + 最小堆」，思路像 Dijkstra，复杂度相同'],
    ),
)
