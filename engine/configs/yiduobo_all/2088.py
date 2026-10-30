G = [[0, 1, 1, 0], [1, 1, 1, 1], [0, 1, 1, 0]]


def _jj(S):
    # 当前正在算的列：f 里已有 len(f) 个，刚算完的是 len(f)-1
    return S.get('j')


def _gcolor(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if ci is None or cj is None or 'g' not in S:
        return None
    if (i, j) == (ci, cj):
        return 'yellow'
    if i == (ci - 1 if S.get('_pass') == 1 else ci + 1) and abs(j - cj) <= 1:
        return 'blue'
    return None


def _pass(S):
    return 1 if S.get('_line') is not None and S['_line'] <= 22 else 2


def _fml(S):
    if 'g' not in S or 'j' not in S:
        return '`f[j]` = 以当前行第 j 格为顶的金字塔最大高度（单格 = 1）'
    i, j, n = S['i'], S['j'], len(S['grid'][0])
    g = S['g']
    p = '向上金字塔：看上一行（上方）' if _pass(S) == 1 else '倒金字塔：看下一行（下方）'
    if j == 0 or j == n - 1:
        return f'{p}｜`j = {j}` 在边界：最多只有单格，`f = grid[{i}][{j}]`'
    if S['grid'][i][j] == 0:
        return f'{p}｜`grid[{i}][{j}] = 0`：贫瘠，`f = 0`'
    return f'{p}｜`min(g[{j-1}], g[{j}], g[{j+1}]) + 1 = min({g[j-1]}, {g[j]}, {g[j+1]}) + 1 = {min(g[j-1], g[j], g[j+1]) + 1}`'


CONFIG = dict(
    num=2088, title='统计农场中肥沃金字塔的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='滚动数组 DP · 金字塔最大高度',
    tags=['难度分 2105'],
    code='''
class Solution(object):
    def countPyramids(self, grid):

        m = len(grid)
        n = len(grid[0])
        res = 0
        
        f = grid[0][:]
        for i in range(1, m):
            g = f[:]
            f = []
            for j in range(n):
                if j == 0 or j == n - 1:
                    f.append(grid[i][j])
                elif grid[i][j] == 0:
                    f.append(0)
                else:
                    f.append(min(g[j - 1], g[j], g[j + 1]) + 1)

                if f[-1] > 0:
                    res += f[-1] - 1
        
        f = grid[m - 1][:]
        for i in range(m - 2, -1, -1):
            g = f[:]
            f = []
            for j in range(n):
                if j == 0 or j == n - 1:
                    f.append(grid[i][j])
                elif grid[i][j] == 0:
                    f.append(0)
                else:
                    f.append(min(g[j - 1], g[j], g[j + 1]) + 1)

                if f[-1] > 0:
                    res += f[-1] - 1
        
        return res
''',
    call=f'Solution().countPyramids({G})',
    expect=4,
    skip=['if j == 0 or j == n - 1', 'if f[-1] > 0', 'm = len', 'n = len', 'g = f[:]', 'f = []', 'for j in range(n)', 'elif grid[i][j] == 0', 'else:'],
    views=[
        dict(type='text', fn=_fml, size=24, h=60),
        dict(type='grid', var='grid', label='grid（黄 = 当前格，蓝 = 它依赖的上/下一行三格）', cell=84, h=290,
             color=lambda S, i, j, v: _gcolor(dict(S, _pass=_pass(S)), i, j, v)),
        dict(type='array', var='g', label='g：上一行（已算好）', cell=84, h=150, pointers={'j': 'blue'}),
        dict(type='array', var='f', label='f：当前行（一格一格 append）', cell=84, h=150),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = grid[0][:]': '第一遍统计==向上的金字塔==：第 0 行每格自己就是高度 1 的「金字塔」',
        'f = grid[m - 1][:]': '第二遍统计==倒金字塔==：把行的顺序反过来，从最后一行往上算，公式完全一样',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：用上一行的 `g` 算这一行的 `f`' if S.get('i') != B.get('i') else '这一遍的所有行都算完了'),
        'if j == 0 or j == n - 1': lambda S, B, r: (f'`j = {S.j}` 在最左/最右：两侧没有格子，==撑不起 3 宽的塔==，高度只能是自己' if (S.j == 0 or S.j == len(S.grid[0]) - 1) else f'`j = {S.j}` 不在边界，往下判断'),
        'f.append(grid[i][j])': '`j = {j}` 在最左/最右列：两侧没有格子，==撑不起 3 宽的塔==，高度只能是自己 → `f` 加入 `{grid[i][j]}`',
        'f.append(0)': '`grid[{i}][{j}] = 0` 是贫瘠格：以它为顶不成塔，`f` 加入 `0`，不计数',
        'f.append(min(': '塔高 = 下一层三个格子能撑起的塔高的最小值 + 1：`min({g[j-1]}, {g[j]}, {g[j+1]}) + 1` = =={f[-1]}==',
        'if f[-1] > 0': lambda S, B, r: (f'`f[-1] = {S.f[-1]} > 0`：是个塔' if S.f[-1] > 0 else '`f[-1] = 0`：不成塔，不计数'),
        'res += f[-1] - 1': '高度 `{f[-1]}` 的塔 → 真金字塔 `{f[-1]} − 1` 个（单格不算）：`res` = =={res}==',
        'return res': '正、倒金字塔共 =={ret}== 个',
    },
    cards=dict(
        one_liner='正、倒金字塔等价：算一遍，翻转行序再算一遍',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['0/1 农场 `grid`，统计==金字塔==与==倒金字塔==的总数（格子数 > 1，全是 1）',
                 '金字塔：顶在最上，往下每行向两边各扩 1 格',
                 '本视频：`[[0,1,1,0],[1,1,1,1],[0,1,1,0]]` → `4`（上 2 + 倒 2）'],
        quote='令f[i][j]表示顶部为(i, j)的向上的金字塔的最大高度……f[i][j] = min(f[i + 1][j - 1], f[i + 1][j], f[i + 1][j + 1]) + 1',
        quote_src='—— yiduobo 题解原文',
        idea=['顶部 `(i,j)` 必须肥沃，下一行只需看三个格子的塔高，取最小再 + 1',
              '高度 `h` 的塔能截出高度 `1..h`，去掉高度 1 的单格 → 贡献 `h − 1`',
              '倒金字塔：把枚举行的顺序反过来，公式不变；每行只依赖相邻一行 → 滚动数组'],
        summary=['时间 `O(mn)`，滚动数组空间 `O(n)`',
                 '易错：边界列（`j = 0` / `n−1`）塔高最多为 1，直接取 `grid`',
                 '易错：单个格子不算金字塔，所以累加的是 `f − 1`',
                 '易错：两遍的区别只是行序，别忘了第二遍用 `grid[m−1]` 初始化',
                 '同类：221 最大正方形（`min(三邻居) + 1`）'],
    ),
)
