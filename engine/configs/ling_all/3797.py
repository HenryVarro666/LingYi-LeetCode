G0 = ['...', '#..']


def _txt(S):
    if 'sum_f' not in S:
        return '`f` = 上一步从上一行跳来；`g` = 上一步在本行平移。`sum_f`、`sum_fg` 是它们的前缀和'
    i, j, d = S.get('i'), S.get('j'), S['d']
    if i is None:
        return '所有行处理完，答案 = `sum_fg[m]`'
    line = S.get('_line')
    if j is None:
        return f'第 `{i}` 行（从第 0 行往下走）'
    if line is not None and line <= 18:
        return f'`f[{j}]`：上一行 `[{max(j - d + 1, 0)}, {min(j + d - 1, S["m"] - 1)}]` 列 f+g 之和（横向差 ≤ d−1）'
    return f'`g[{j}]`：本行 `[{max(j - d, 0)}, {min(j + d, S["m"] - 1)}]` 列 f 之和（横向差 ≤ d，f 与 −f 抵消）'


CONFIG = dict(
    num=3797, title='统计在矩形格子里移动的路径数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前缀和优化 DP · f/g 两种状态',
    tags=['灵神题单·动态规划', '难度分 2376'],
    code='''
# 手写 min max 更快
min = lambda a, b: b if b < a else a
max = lambda a, b: b if b > a else a
class Solution:
    def numberOfRoutes(self, grid: List[str], d: int) -> int:
        MOD = 1_000_000_007
        m = len(grid[0])
        sum_f = [0] * (m + 1)
        sum_fg = [0] * (m + 1)
        for i, row in enumerate(grid):
            # f 的前缀和
            for j, ch in enumerate(row):
                if ch == '#':
                    sum_f[j + 1] = sum_f[j]
                elif i == 0:  # 第一行（起点）
                    sum_f[j + 1] = sum_f[j] + 1  # DP 初始值
                else:
                    sum_f[j + 1] = (sum_f[j] + sum_fg[min(j + d, m)] - sum_fg[max(j - d + 1, 0)]) % MOD
            # f[j] + g[j] 的前缀和
            for j, ch in enumerate(row):
                if ch == '#':
                    sum_fg[j + 1] = sum_fg[j]
                else:
                    # -f[j] 和 +f[j] 抵消了
                    sum_fg[j + 1] = (sum_fg[j] + sum_f[min(j + d + 1, m)] - sum_f[max(j - d, 0)]) % MOD
        return sum_fg[m]
''',
    call=f'Solution().numberOfRoutes({G0!r}, 1)',
    expect=10,
    skip=['MOD = 1_000_000_007', 'min = lambda', 'max = lambda', '# 手写'],
    views=[
        dict(type='grid', var=lambda S: [list(r) for r in S['grid']], label='grid（黄 = 当前格；#=堵；第 0 行是起点行）', h=210, cell=84,
             cursors=[('i', 'j', 'yellow', '')],
             color=lambda S, r, c, v: 'red' if v == '#' else None),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='sum_f', label='sum_f[j+1]：本行 f[0..j] 的前缀和（f = 从上一行跳来）', h=190, cell=80, pointers={'j': 'yellow'}),
        dict(type='array', var='sum_fg', label='sum_fg[j+1]：本行 (f+g)[0..j] 的前缀和', h=190, cell=80, pointers={'j': 'yellow'}),
    ],
    watch=[('d', 'd', 'cyan'), ('i', 'i', 'blue'), ('j', 'j', 'yellow')],
    captions={
        'm = len(grid[0])': '`m = {m}` 列，前缀和数组开 `m+1` 格（`sum[0] = 0`）',
        'sum_f = [0]': '`sum_f`：==f 的前缀和==；`f[i][j]` 表示上一步在第 `i-1` 行时到 `(i,j)` 的方案数',
        'sum_fg = [0]': '`sum_fg`：==f+g 的前缀和==；`g[i][j]` 表示上一步也在第 `i` 行时的方案数',
        'for i, row in enumerate': lambda S, B, r: ('所有行都算完了' if B.get('i') == S.get('i') and S.get('i') == len(S.grid) - 1 and 'j' in B and B.get('j') == S.get('j') and S.get('_line') != 8
                                                    else f'第 `{S.i}` 行：先算整行 `f` 的前缀和，再算 `f+g` 的前缀和（从第 0 行往下走，和题目的方向反过来）'),
        'if ch == \'#\'': lambda S, B, r: (f'`({S.i},{S.j})` 是 `{S.ch}` → ' + ('==堵住了，方案数为 0，前缀和不增==' if S.ch == '#' else '可用，继续算')),
        14: '被堵：`sum_f[{j+1}] = sum_f[{j}]` = {sum_f[j+1]}',
        'sum_f[j + 1] = sum_f[j] + 1': '第 0 行任何可用格都是起点：`f[0][{j}] = 1`，前缀和 `sum_f[{j+1}]` = =={sum_f[j+1]}==',
        'sum_f[j + 1] = (sum_f[j] + sum_fg': '`f[{i}][{j}]` = 上一行列 `[{max(j-d+1,0)}, {min(j+d,m)-1}]` 的 f+g 之和（`|k−j| ≤ d−1`，因为要先走 1 行）→ `sum_f[{j+1}]` = =={sum_f[j+1]}==',
        22: '被堵：`sum_fg[{j+1}] = sum_fg[{j}]` = {sum_fg[j+1]}',
        'sum_fg[j + 1] = (sum_fg[j] + sum_f': '`f+g` 在本行：枚举本行列 `[{max(j-d,0)}, {min(j+d+1,m)-1}]` 的 f 之和（`|k−j| ≤ d`）；不能原地不动，`-f[j]` 与 `+f[j]` 抵消 → `sum_fg[{j+1}]` = =={sum_fg[j+1]}==',
        'return sum_fg[m]': '答案 = 最后一行所有格的 `f+g` 之和 = `sum_fg[{m}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f 记从上一行来的，g 记行内平移来的，两者都用前缀和',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['格子是 `.`（可用）或 `#`（堵），从最后一行任意格出发，走到第 0 行',
                 '每步欧氏距离 ≤ `d`，只能同行或上一行，==不能连续两次同行==',
                 '示例：`["..","#."], d=1` → `2`；本视频：`["...","#.."], d=1` → `10`'],
        quote='为方便计算，考虑从上往下移动。定义 f[i][j] 表示从 0 行移动到 (i,j)，且上一步在 i-1 行的方案数。定义 g[i][j] 表示……且上一步也在 i 行的方案数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把路线反过来，从第 0 行往下走，起点变成终点，方案数不变',
              '换行时水平差 `|k−j| ≤ d−1`（因为 `(k−j)^2 + 1 ≤ d^2`）；行内移动水平差 `≤ d`',
              '`f` 要累加上一行的 `f+g`；`g` 累加本行的 `f` 再减去自己（不能原地不动）',
              '两个求和都是区间和 → 前缀和 `O(1)`'],
        summary=['时间 `O(nm)`，空间 `O(m)`（只保留当前行的两个前缀和）',
                 '易错：换行的列范围是 `d−1`，行内是 `d`；`g` 不能从 `f[j]` 自己转移',
                 '被堵的格子 `f=g=0`，前缀和要原样往后抄一格',
                 '题解写法一是显式开 `f`、`g` 数组；这里选的是写法二：直接算前缀和，`+f[j]` 与 `−f[j]` 抵消',
                 '本视频演示用 `min`/`max` 手写 lambda 版（更快）'],
    ),
)
