G = [[9, 5, 7, 3], [8, 9, 6, 1], [6, 7, 14, 3]]


def _fc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if S.get('_line') in range(12, 23):
        if (r, c) in ((i - 1, j), (i, j - 1)) and r >= 0 and c >= 0:
            return 'blue'
    return None


def _gc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    return 'yellow' if (r, c) == (i, j) else None


def _fml(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i][j]` = 以 (0,0) 为左上角、(i,j) 为右下角的矩阵最小值'
    if i == 0 and j == 0:
        return '左上角：只有自己，`f = grid`，没有合法路径'
    if i == 0:
        return f'首行：起点最小值 = `f[{i}][{j - 1}]` = {S["f"][i][j - 1]}'
    if j == 0:
        return f'首列：起点最小值 = `f[{i - 1}][{j}]` = {S["f"][i - 1][j]}'
    return f'起点最小值 = `min(f[{i - 1}][{j}], f[{i}][{j - 1}])` = {min(S["f"][i - 1][j], S["f"][i][j - 1])}'


CONFIG = dict(
    num=3148, title='矩阵中的最大得分', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二维 DP · 左上角最小值',
    tags=['动态规划', '常用数据结构', '难度分 1820'],
    code='''
class Solution(object):
    def maxScore(self, grid):

        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        res = -100000
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = grid[i][j]
                    else:
                        res = max(res, grid[i][j] - f[i][j - 1])
                        f[i][j] = min(f[i][j - 1], grid[i][j])
                elif j == 0:
                    res = max(res, grid[i][j] - f[i - 1][j])
                    f[i][j] = min(f[i - 1][j], grid[i][j])
                else:
                    res = max(res, grid[i][j] - min(f[i - 1][j], f[i][j - 1]))
                    f[i][j] = min(f[i - 1][j], f[i][j - 1], grid[i][j])

        return res
''',
    call=f'Solution().maxScore({G})',
    expect=9,
    skip=['m = len', 'n = len', 'for j in range(n)', 'if i == 0', 'elif j == 0', 'else:'],
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='grid', var='grid', label='grid（黄框 = 当前终点 (i,j)）', cell=84, h=290, color=_gc),
        dict(type='table', var='f', label='f[i][j]：左上角矩阵的最小值（黄 = 当前，蓝 = 起点候选）', cell=84, h=290, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('grid[i][j]', 'grid[i][j]', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = [[0]': '`f[i][j]`：以 (0,0) 为左上角、(i,j) 为右下角的矩阵里的最小值',
        'res = -100000': '`res` 记最大得分，初值设成很小的数（得分可能为负）',
        'if j == 0': lambda S, B, r: ('`j = 0`：左上角' if S.j == 0 else '`j > 0`：首行，左边还有格子'),
        'f[i][j] = grid[i][j]': '(0,0)：矩阵里只有自己，`f = {f[0][0]}`；==不存在以它为终点的路径==，不更新 res',
        'res = max(res, grid[i][j] - f[i][j - 1])': '首行：起点只能在左边矩阵里 → `{grid[i][j]} − {f[i][j-1]}`，`res` = =={res}==',
        'f[i][j] = min(f[i][j - 1], grid[i][j])': '首行：`f[{i}][{j}] = min({f[i][j-1]}, {grid[i][j]})` = =={f[i][j]}==',
        'res = max(res, grid[i][j] - f[i - 1][j])': '首列：起点只能在上边矩阵里 → `{grid[i][j]} − {f[i-1][j]}`，`res` = =={res}==',
        'f[i][j] = min(f[i - 1][j], grid[i][j])': '首列：`f[{i}][{j}] = min({f[i-1][j]}, {grid[i][j]})` = =={f[i][j]}==',
        'res = max(res, grid[i][j] - min(': '终点 `{grid[i][j]}`，起点取上、左两个矩阵最小值的较小者 `min({f[i-1][j]}, {f[i][j-1]})` = `{min(f[i-1][j], f[i][j-1])}`，`res` = =={res}==',
        'f[i][j] = min(f[i - 1][j], f[i][j - 1], grid[i][j])': '上、左矩阵会重叠，但求最小值==重复不影响==：`f[{i}][{j}]` = =={f[i][j]}==',
        'return res': '最大得分 = =={ret}==',
    },
    cards=dict(
        one_liner='路径得分中间项全消掉，只剩终点减起点',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['矩阵 `grid`，可向正右或正下移动到任意远的格子，得分 `c2 - c1`',
                 '起点任选，==至少移动一步==，求最大总得分',
                 '示例：`[[9,5,7,3],[8,9,6,1],[6,7,14,3]]` → `9`'],
        quote='除了c[1]和c[m]外，其他所有元素都将被消去，那么问题实际上就变成了从矩阵中某个单元格出发，走到其右下方的另一个单元格，要求终点的值减去起点的值最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['(c2−c1)+(c3−c2)+…：中间项成对抵消 → 只看首尾',
              '枚举终点 `(i,j)`，起点取左上矩阵（不含自己）的最小值',
              '分四种情况：左上角 / 首行 / 首列 / 一般位置，一般位置取 `min(上, 左)`'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：(0,0) 没有合法路径，不能用它更新答案',
                 '易错：`res` 初值要足够小，答案可能是负数',
                 '上、左两块矩阵重叠没关系：求最小值，重复计算不影响结果',
                 '对比灵神：灵神把四种情况合并，用 `inf` 哨兵 + 滚动数组压到 `O(n)`'],
    ),
)
