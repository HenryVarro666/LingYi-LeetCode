G0 = ['..', '#.']


def _txt(S):
    if 'dd' not in S:
        return '`f` = 跨层走到该格的路径数，`g` = 同层平移走到该格；`sf`、`sg` 是前缀和'
    i, j = S.get('i'), S.get('j')
    d, dd = S['d'], S['dd']
    if i is None or j is None:
        return f'`d = {d}`：跨层横向差 `≤ dd = {dd}`（`d^2 − 1` 开方取整），同层横向差 `≤ d = {d}`'
    return f'当前格 `({i},{j})`：跨层看上一层 `[{max(0, j - dd)}, {min(S["m"] - 1, j + dd)}]` 列，同层看本层 `[{max(0, j - d)}, {min(S["m"] - 1, j + d)}]` 列'


CONFIG = dict(
    num=3797, title='统计在矩形格子里移动的路径数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按层 DP · f/g + 前缀和，省掉层数维度',
    tags=['灵神题单·动态规划', '难度分 2376'],
    code='''
class Solution(object):
    def numberOfRoutes(self, grid, d):
        
        n = len(grid)
        m = len(grid[0])
        mod = 10 ** 9 + 7

        f = []
        sf = []
        for j in range(m):
            if grid[-1][j] == '#':
                f.append(0)
            else:
                f.append(1)
            
            if j == 0:
                sf.append(f[0])
            else:
                sf.append(sf[-1] + f[-1])
        
        g = []
        sg = []
        for j in range(m):
            if grid[-1][j] == '#':
                g.append(0)
            else:
                left = max(0, j - d)
                right = min(m - 1, j + d)
                g.append(sf[right] - f[j])
                if left > 0:
                    g[-1] -= sf[left - 1]
            
            if j == 0:
                sg.append(g[0])
            else:
                sg.append(sg[-1] + g[-1])

        dd = int((d * d - 1) ** 0.5)

        for i in range(n - 2, -1, -1):
            for j in range(m):
                if grid[i][j] == '#':
                    f[j] = 0
                else:
                    left = max(0, j - dd)
                    right = min(m - 1, j + dd)
                    f[j] = (sf[right] + sg[right]) % mod
                    if left > 0:
                        f[j] = (f[j] - (sf[left - 1] + sg[left - 1]) % mod + mod) % mod

            sf[0] = f[0]
            for j in range(1, m):
                sf[j] = (sf[j - 1] + f[j]) % mod
            
            for j in range(m):
                if grid[i][j] == '#':
                    g[j] = 0
                else:
                    left = max(0, j - d)
                    right = min(m - 1, j + d)
                    g[j] = (sf[right] - f[j] + mod) % mod
                    if left > 0:
                        g[j] = (g[j] - sf[left - 1] + mod) % mod
            
            sg[0] = g[0]
            for j in range(1, m):
                sg[j] = (sg[j - 1] + g[j]) % mod
        
        return (sf[-1] + sg[-1]) % mod
''',
    call=f'Solution().numberOfRoutes({G0!r}, 2)',
    expect=4,
    skip=['left = max', 'right = min', 'mod = 10', 'n = len', 'if j == 0', 'else:', 'if left > 0', 'g[-1] -= sf', 'f.append', 'sg.append', 'sf.append'],
    views=[
        dict(type='grid', var=lambda S: [list(r) for r in S['grid']], label='grid（红 = #；黄 = 当前格；从最后一行往上走）', h=170, cell=80,
             cursors=[('i', 'j', 'yellow', '')],
             color=lambda S, r, c, v: 'red' if v == '#' else None),
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='array', var='f', label='f[j]：跨层走到 (i,j)', h=130, cell=64, pointers={'j': 'yellow'}),
        dict(type='array', var='sf', label='sf[j]：f 的前缀和', h=130, cell=64),
        dict(type='array', var='g', label='g[j]：同层平移走到 (i,j)', h=130, cell=64, pointers={'j': 'yellow'}),
        dict(type='array', var='sg', label='sg[j]：g 的前缀和', h=130, cell=64),
    ],
    watch=[('d', 'd', 'cyan'), ('dd', 'dd', 'orange'), ('i', 'i', 'blue'), ('j', 'j', 'yellow')],
    captions={
        8: '`f[j]`：==跨层==移动到本层第 `j` 列的路径数',
        21: '`g[j]`：==同层==移动到本层第 `j` 列的路径数',
        9: '`sf[j]`：f 的前缀和，先空着',
        22: '`sg[j]`：g 的前缀和，先空着',
        11: lambda S, B, r: f'最后一行 `({len(S.grid) - 1},{S.j})` 是 `{S.grid[-1][S.j]}`' + ('：不能当起点，`f = 0`' if S.grid[-1][S.j] == '#' else '：可作起点，`f = 1`'),
        24: lambda S, B, r: f'`({len(S.grid) - 1},{S.j})` 是 `{S.grid[-1][S.j]}`' + ('：被堵，`g = 0`' if S.grid[-1][S.j] == '#' else '：可用，算 g'),
        'g.append(sf[right] - f[j])': '起点行也能先平移一步：`g[{j}]` = 同层 `[{left}, {right}]` 列的 f 之和 − 自己（不能原地不动）= =={g[j]}==',
        'sg.append(g[0])': '`sg[0] = g[0]` = {g[0]}',
        'dd = int': '跨层移动水平距离 `p` 满足 `p^2 + 1 ≤ d^2`，所以 `|p| ≤ ` `dd = int(sqrt({d}^2 − 1))` = =={dd}==',
        'for i in range(n - 2': lambda S, B, r: ('所有层都算完了，答案在第 0 层' if B.get('i') == S.i
                                                  else f'往上算第 `{S.i}` 层。每层顺序：==上一层 sf/sg → f → sf → g → sg=='),
        'for j in range(1, m)': '继续往后累加前缀和',
        'if grid[i][j]': lambda S, B, r: f'`({S.i},{S.j})` 是 `{S.grid[S.i][S.j]}`' + ('：被堵，值为 0' if S.grid[S.i][S.j] == '#' else '：可用，要算'),
        'f[j] = 0': '被堵 → `f[{j}] = 0`',
        'g[j] = 0': '被堵 → `g[{j}] = 0`',
        'f[j] = (sf[right] + sg[right]) % mod': '`f[{j}]` = 上一层 `[{left}, {right}]` 列的 f+g 之和（先 `0..{right}` 全加）= {f[j]}',
        'f[j] = (f[j] - (sf': '区间和 = 前缀和之差：减去 `0..{left-1}` 列 → `f[{j}]` = =={f[j]}==',
        'sf[0] = f[0]': '重算本层 `sf`：`sf[0] = f[0]` = {sf[0]}',
        'sf[j] = (sf[j - 1] + f[j])': '`sf[{j}] = sf[{j-1}] + f[{j}]` = =={sf[j]}==',
        'g[j] = (sf[right] - f[j] + mod)': '`g[{j}]` = 本层 `[{left}, {right}]` 列的 f 之和 − `f[{j}]`（不能原地不动）= =={g[j]}==',
        'g[j] = (g[j] - sf': '去掉 `0..{left-1}` 列 → `g[{j}]` = =={g[j]}==',
        'sg[0] = g[0]': '`sg[0] = g[0]` = {sg[0]}',
        'sg[j] = (sg[j - 1] + g[j])': '`sg[{j}] = sg[{j-1}] + g[{j}]` = =={sg[j]}==',
        'return (sf[-1] + sg[-1])': '第 0 层终点：`sf[-1] + sg[-1]` = {sf[-1]} + {sg[-1]} = =={ret}==',
    },
    cards=dict(
        one_liner='按层 DP：f 跨层来、g 同层来，区间和用前缀和',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['格子是 `.`（可用）或 `#`（堵），从最后一行任意可用格出发，走到第 0 行',
                 '每步欧氏距离 ≤ `d`，只能同层或上一层，==不能连续两次同层==',
                 '示例：`["..","#."], d=2` → `4`（本视频用它）'],
        quote='若grid[i][j]为\'#\'，那么f[i][j]必然为0。反之，若当前处于第n - 1层，那么就有f[i][j] = 1，因为可以选择任意为\'.\'的单元格作为路径的起点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f` 是跨层来的、`g` 是同层来的：这样「不能连续同层」自然成立',
              '跨层：`(p−j)^2 + 1 ≤ d^2`，即 `|p−j| ≤ dd = int(sqrt(d^2 − 1))`',
              '同层：`|j−p| ≤ d`，但不能原地不动 → 区间和再减去 `f[j]`',
              '依赖顺序：上一层 `sf/sg` → `f` → `sf` → `g` → `sg`，所以层数维度可以省掉'],
        summary=['时间 `O(nm)`，空间 `O(m)`',
                 '易错：跨层用 `dd`，同层用 `d`；`g` 要减去 `f[j]`',
                 '区间和 = `sf[right] − sf[left−1]`，`left = 0` 时不用减',
                 '原文为 Python 2 风格，但语法在 Python 3 下可直接运行，代码未改动',
                 '对比灵神：灵神从第 0 行往下走（路径反过来）并把 `+f` 与 `−f` 抵消；yiduobo 从最后一行往上，显式保存 f、g'],
    ),
)
