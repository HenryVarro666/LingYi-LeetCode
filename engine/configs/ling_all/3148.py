G = [[9, 5, 7, 3], [8, 9, 6, 1], [6, 7, 14, 3]]




def _ri(S):
    return next((k for k, r in enumerate(S['grid']) if r is S['row']), None) if 'row' in S else None


CONFIG = dict(
    num=3148, title='矩阵中的最大得分', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='列最小值 + 行前缀最小值',
    tags=['动态规划', '常用数据结构', '难度分 1820'],
    code='''
class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        ans = -inf
        col_min = [inf] * len(grid[0])
        for row in grid:
            pre_min = inf  # col_min[0..j] 的最小值
            for j, x in enumerate(row):
                ans = max(ans, x - min(pre_min, col_min[j]))
                col_min[j] = min(col_min[j], x)
                pre_min = min(pre_min, col_min[j])
        return ans
''',
    call=f'Solution().maxScore({G})',
    expect=9,
    skip=['ans = -inf', 'col_min = [inf]', 'pre_min = inf', 'for j, x in enumerate'],
    views=[
        dict(type='text', size=26, h=60, fn=lambda S: (
            f"终点 `x = {S['x']}`，起点最小值 `min({S['pre_min']}, {S['col_min'][S['j']]})`"
            if 'x' in S and S.get('_line') == 8 else '得分 = ==终点海拔 − 起点海拔==，中间点全被消掉')
             if 'row' in S else '得分 = ==终点海拔 − 起点海拔==，中间点全被消掉'),
        dict(type='grid', var='grid', label='grid（黄框 = 当前终点 x）', cell=96, h=330,
             cursors=[(_ri, 'j', 'yellow')]),
        dict(type='array', var='col_min', label='col_min[j]：第 j 列到当前行为止的最小值', cell=96, h=200,
             pointers={'j': 'blue'}),
    ],
    watch=[('j', 'j', 'blue'), ('x', 'x', 'yellow'), ('pre_min', 'pre_min', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = max': '终点 `{x}` − 起点最小值 `min({pre_min}, {col_min[j]})` = `{x - min(pre_min, col_min[j])}`，答案 `max({B.ans}, …)` = =={ans}==',
        'col_min[j] = min': '把这一格并入第 j 列：`col_min[{j}] = {col_min[j]}`（先算答案、后更新，保证起点 ≠ 终点）',
        'pre_min = min': '`pre_min` = 本行 0..j 列的列最小值的最小值 = =={pre_min}==，下一格的起点候选',
        'for row in grid': lambda S, B, r: ('换到下一行；`col_min` 保留了上面所有行的信息' if S.get('row') != B.get('row') else '所有行都处理完了'),
        'return ans': '最大得分 = =={ret}==',
    },
    cards=dict(
        one_liner='得分之和 = 终点海拔 − 起点海拔，枚举终点找左上最小值',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['矩阵 `grid`，可以向下或向右走到任意远的格子，得分 `c2 - c1`',
                 '起点任选，==至少移动一次==，求最大总得分',
                 '示例：`[[9,5,7,3],[8,9,6,1],[6,7,14,3]]` → `9`（从 5 到 14）'],
        quote='把 grid[i][j] 视作海拔高度，把得分视作重力势能的变化量……题目相当于计算重力势能的变化量之和，也就是终点与起点的海拔高度之差。',
        quote_src='—— 灵茶山艾府题解',
        idea=['中间的格子一加一减全消掉，只剩 ==终点 − 起点==',
              '枚举终点，起点取左上方最小值：左边用 `pre_min`，上边用 `col_min[j]`',
              '先算答案再更新最小值，所以起点一定不是终点自己'],
        summary=['时间 `O(mn)`，用 `col_min` 压缩后空间 `O(n)`',
                 '易错：初始 `ans = -inf`，答案可能是负数（如 `[[4,3,2],[3,2,1]]` → -1）',
                 '易错：必须先用 `x` 更新答案，再更新 `col_min`/`pre_min`，否则会出现起点 = 终点',
                 '题解的另一种写法：二维数组 `f[i+1][j+1]` 记左上角子矩阵最小值，空间 `O(mn)`'],
    ),
)
