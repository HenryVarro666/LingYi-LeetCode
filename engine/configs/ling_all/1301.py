B0 = ["E12", "1X1", "21S"]


def _gcolor(S, i, j, v):
    if 'j' not in S or S.get('_line', 0) < 8:
        return None
    ri = S['board'].index(S['row']) if 'row' in S else None
    if v == 'X':
        return 'red'
    if ri is not None and i == ri and j == S['j']:
        return 'yellow'
    return None


def _cmp(S, B, ret):
    ps, ms, ms0 = S.pre_s, S.max_sum[S.j + 1], S.max_sum[S.j]
    return f'三个来源的路径和：左上 `{ps}`、正上 `{ms}`、正左 `{ms0}` → 最大 `s = {S.s}`'


def _w(S, B, ret):
    return f'方案数累加到 `w = {S.w}`'


CONFIG = dict(
    num=1301, title='最大得分的路径数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='网格 DP：最大和 + 加法原理（空间优化）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1853'],
    code='''
class Solution:
    def pathsWithMaxScore(self, board: List[str]) -> List[int]:
        MOD = 1_000_000_007
        n = len(board[0])
        max_sum = [0] + [-inf] * n  # 定义同 64 题（改成最大路径和）
        ways = [1] + [0] * n  # 定义同 63 题

        for row in board:
            # 计算 max_sum[i+1][j+1] 时，pre_s 表示 max_sum[i][j]，pre_w 表示 ways[i][j]
            pre_s, pre_w = max_sum[0], ways[0]
            max_sum[0], ways[0] = -inf, 0
            for j, ch in enumerate(row):
                if ch == 'X':
                    pre_s, pre_w = max_sum[j + 1], ways[j + 1]
                    max_sum[j + 1], ways[j + 1] = -inf, 0
                    continue
                tmp_s, tmp_w = max_sum[j + 1], ways[j + 1]
                # 左上、正上、正左
                s = max(pre_s, max_sum[j + 1], max_sum[j])
                # 如果路径和相同，则累加方案数（加法原理）
                w = 0
                if pre_s == s:
                    w += pre_w
                if max_sum[j + 1] == s:
                    w += ways[j + 1]
                if max_sum[j] == s:
                    w += ways[j]
                ways[j + 1] = w % MOD
                max_sum[j + 1] = s
                if ch.isdigit():
                    max_sum[j + 1] += int(ch)  # 加上当前格子的值
                pre_s, pre_w = tmp_s, tmp_w

        return [max_sum[n], ways[n]] if max_sum[n] != -inf else [0, 0]
''',
    call=f'Solution().pathsWithMaxScore({B0!r})',
    expect=[4, 2],
    skip=['w += ', 'w = 0', 'max_sum[j + 1] = s', 'for row in board', 'pre_s, pre_w = max_sum[0]', 'MOD = ', 'n = len', 'tmp_s, tmp_w', 'pre_s, pre_w = tmp_s', 'max_sum[0], ways[0] = -inf'],
    views=[
        dict(type='grid', var='board', label='board（黄 = 当前格，红 = 障碍）', h=230, cell=70,
             cursors=[(lambda S: S['board'].index(S['row']) if 'row' in S else -1, 'j', 'yellow')],
             color=lambda S, i, j, v: 'red' if v == 'X' else None),
        dict(type='array', var='max_sum', label='max_sum（滚动一行；-inf = 到不了）', h=150,
             pointers={'j + 1': 'blue'}, cell=90,
             color=lambda S, i, v: 'cyan' if i == S.get('j', -9) + 1 and S.get('_line', 0) > 14 else None),
        dict(type='array', var='ways', label='ways（得到最大和的方案数）', h=150, pointers={'j + 1': 'blue'}, cell=90,
             color=lambda S, i, v: 'green' if i == S.get('j', -9) + 1 and S.get('_line', 0) > 14 else None),
    ],
    max_steps=66,
    watch=[('j', 'j', 'blue'), 'ch', 'pre_s', 'pre_w', 's', 'w'],
    captions={
        'max_sum = [0]': '`max_sum[j]`：走到当前行第 `j-1` 列的最大路径和；起点外面设为 `0`，其余 `-inf`（还没走到）',
        'ways = [1]': '`ways[j]`：对应的方案数；起点 1 种，其余 0 种',
        'for row in board': '逐行处理，`max_sum`/`ways` 保存的是上一行的结果，边算边覆盖成当前行',
        'pre_s, pre_w = max_sum[0]': '`pre_s`/`pre_w` 暂存「左上角」那一格的旧值，因为它马上要被覆盖',
        'if ch ==': lambda S, B, r: (f'`ch = {S.ch!r}` 是障碍 → 这一格到不了：路径和 `-inf`，方案数 0；旧值留给右边格子当「左上」'
                                      if S.ch == 'X' else f'`ch = {S.ch!r}` 不是障碍，继续算'),
        's = max': _cmp,
        'w = 0': '方案数从 0 开始，只累加「路径和等于最大值」的来源',
        'if pre_s == s': lambda S, B, r: (f'左上 `{S.pre_s}` == 最大 `{S.s}` → 加上它的方案数 `{S.pre_w}`' if S.pre_s == S.s
                                          else f'左上 `{S.pre_s}` ≠ 最大 `{S.s}` → 这条路不是最优，不加'),
        'if max_sum[j + 1] == s': lambda S, B, r: (f'正上 `{S.max_sum[S.j+1]}` == 最大 `{S.s}` → 加上方案数 `{S.ways[S.j+1]}`' if S.max_sum[S.j+1] == S.s
                                                   else f'正上 `{S.max_sum[S.j+1]}` ≠ 最大 `{S.s}` → 不加'),
        'if max_sum[j] == s': lambda S, B, r: (f'正左 `{S.max_sum[S.j]}` == 最大 `{S.s}` → 加上方案数 `{S.ways[S.j]}`' if S.max_sum[S.j] == S.s
                                               else f'正左 `{S.max_sum[S.j]}` ≠ 最大 `{S.s}` → 不加'),
        'ways[j + 1] = w': '`ways[{j+1}] = {w} % MOD` = =={ways[j+1]}==（加法原理：几条最优路径就加几份）',
        'max_sum[j + 1] = s': '先写入来源里的最大路径和 `{s}`',
        'if ch.isdigit': lambda S, B, r: (f'`{S.ch}` 是数字 → 路径和再加上它' if S.ch.isdigit() else '`E` / `S` 不是数字，不加分'),
        'max_sum[j + 1] += int': '`max_sum[{j+1}] += {ch}` → =={max_sum[j+1]}==',
        'return': lambda S, B, r: f'终点：最大得分 `{r[0]}`，方案数 `{r[1]}`',
    },
    cards=dict(
        one_liner='64 题求最大和 + 63 题数方案，路径和相同就相加',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['从右下 `S` 出发，向上/向左/向左上走，到左上 `E`，不能进 `X`',
                 '得分 = 路径上数字之和；返回 `[最大得分, 最大得分的方案数 % (1e9+7)]`',
                 '示例：`["E12","1X1","21S"]` → `[4,2]`；到不了则 `[0,0]`'],
        quote='如果往左走的路径和，严格大于往上走的路径和，那么计算方案数时，只需考虑往左走的方案数。……如果二者一样大，那么根据==加法原理==，要把两种方案数相加。',
        quote_src='—— 灵茶山艾府题解',
        idea=['本题是前置题 64（最小路径和）和 63（不同路径）的综合',
              '三个来源取最大路径和 `s`，再把「路径和恰为 s」的来源方案数累加',
              '方向反过来看：从 `E` 往右下走也一样，所以从左上往右下递推'],
        summary=['时间 `O(mn)`；滚动数组把空间从 `O(mn)` 降到 `O(n)`',
                 '易错：障碍格要把 `max_sum`/`ways` 置成 `-inf`/`0`，并先保存旧值给右边格子当「左上」',
                 '易错：`ways` 累加时只加路径和等于最大值的来源，最后取模',
                 '原文还有未空间优化的二维写法，思路相同；可中途取模，因为只有加法'],
    ),
)
