G = [[1, 1, 1, 0], [1, 1, 1, 1], [0, 1, 1, 1]]


def _fml(S):
    if S.get('_line') in (18, 33) and 'j' in S and 0 < S['j'] < len(S['grid'][0]) - 1:
        j, g = S['j'], S['g']
        return f'`f[{j}] = min(g[{j-1}], g[{j}], g[{j+1}]) + 1` = `min({g[j-1]}, {g[j]}, {g[j+1]}) + 1` = =={min(g[j-1], g[j], g[j+1]) + 1}=='
    if S.get('_line', 0) >= 23:
        return f"第 2 遍：行顺序反过来（从下往上），当前 `res = {S.get('res', 0)}`"
    return f"第 1 遍：行顺序从上往下，当前 `res = {S.get('res', 0)}`"


CONFIG = dict(
    num=2088, title='统计农场中肥沃金字塔的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='滚动数组 DP + 行顺序反转',
    tags=['灵神题单·动态规划', '难度分 2105'],
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
    expect=6,
    skip=['m = len', 'n = len', 'for j in range', 'g = f[:]', 'f = []', 'if j == 0 or', 'f.append(grid', 'f.append(0)'],
    max_steps=100,
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前格 (i,j)）', cell=84, h=240, cursors=[('i', 'j', 'yellow')]),
        dict(type='array', var=lambda S: S.get('g'), label='g（上一行的 f）', cell=84, h=170, pointers={'j': 'pink'}),
        dict(type='array', var=lambda S: S.get('f'), label='f（正在算的这一行，高度 = 最大层数）', cell=84, h=170,
             color=lambda S, k, v: 'green' if v > 1 else None),
        dict(type='text', fn=_fml, size=24, h=80),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计答案',
        'f = grid[0][:]': '第一行每格最多 1 层：`f = grid[0]`；之后每行只依赖上一行 → 滚动数组',
        'for i in range(1, m)': lambda S, B, r: ('第 1 遍的所有行都算完了' if B.get('i') == S.get('i') else f'`i = {S.i}`：逐行向下，`g` 是上一行，`f` 是当前行'),
        'elif grid[i][j] == 0': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = 0`：贫瘠 → 层数 0' if S.grid[S.i][S.j] == 0
                                                 else f'`grid[{S.i}][{S.j}] = 1`：肥沃，用上一行三个格子判断'),
        'f.append(min(': '`min(g[{j-1}], g[{j}], g[{j+1}]) + 1` = =={f[-1]}==：三个格子的金字塔恰好覆盖整个梯形',
        'if f[-1] > 0': lambda S, B, r: ((f'`j = {S.j}` 是边界列：只能是单格，直接取 `grid` 的值；' if S.j in (0, len(S.grid[0]) - 1) else '') + (f'`f[-1] = {S.f[-1]} > 0`：层数里要去掉 1 个格子的情况' if S.f[-1] > 0 else '`f[-1] = 0`：不是金字塔，不累加')),
        'res += f[-1] - 1': '高度 {f[-1]} → 有 `{f[-1]} - 1` 个金字塔，`res` = =={res}==',
        'f = grid[m - 1][:]': '第 2 遍：==行顺序反过来==，从最后一行往上，统计倒金字塔',
        'for i in range(m - 2': lambda S, B, r: ('第 2 遍的所有行都算完了' if B.get('i') == S.get('i') else f'`i = {S.i}`：自下而上逐行'),
        'return res': '正金字塔 + 倒金字塔，共 =={ret}==',
    },
    cards=dict(
        one_liner='正反金字塔等价：同一个 DP，行顺序正着倒着各跑一遍',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['`m × n` 的 0/1 网格，1 为肥沃',
                 '统计全由肥沃格子组成、格子数大于 1 的金字塔和倒金字塔总数',
                 '示例：`[[1,1,1,0],[1,1,1,1],[0,1,1,1]]` → `6`'],
        quote='第i + 1行仅有三个格子需要判断，而通过这三个格子构造的金字塔恰好可以覆盖住整个梯形，即 f[i][j] = min(f[i + 1][j - 1], f[i + 1][j], f[i + 1][j + 1]) + 1',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` = 顶部为 `(i,j)` 的最大高度，贫瘠格为 0',
              '梯形不好直接判断，改看相邻行的三个格子',
              '正反金字塔构成一致，只需把枚举行的顺序反过来再算一遍',
              '每行只依赖上一行 → 滚动数组'],
        summary=['时间 `O(mn)`，空间 `O(n)`',
                 '易错：高度为 1（单个格子）不算金字塔，所以累加 `f - 1`',
                 '易错：最左、最右列只能是单格，直接取 `grid` 的值',
                 '原文本身就是 Python 3 可运行的写法，代码未改'],
    ),
)
