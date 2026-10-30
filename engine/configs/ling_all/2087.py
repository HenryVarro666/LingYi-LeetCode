CONFIG = dict(
    num=2087, title='网格图中机器人回家的最小代价', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='径直走 + 前缀和式累加',
    tags=['脑筋急转弯', '难度分 1744'],
    code='''
class Solution:
    def minCost(self, startPos: List[int], homePos: List[int], rowCosts: List[int], colCosts: List[int]) -> int:
        x0, y0 = startPos
        x1, y1 = homePos

        # 起点的代价不计入，先减去
        ans = -rowCosts[x0] - colCosts[y0]

        # 累加代价（包含起点）
        ans += sum(rowCosts[min(x0, x1): max(x0, x1) + 1])
        ans += sum(colCosts[min(y0, y1): max(y0, y1) + 1])

        return ans
''',
    call='Solution().minCost([1, 0], [2, 3], [5, 4, 3], [8, 2, 6, 7])',
    expect=18,
    views=[
        dict(type='array', var='rowCosts', label='rowCosts（走到第 r 行付 rowCosts[r]）', h=200,
             pointers={'x0': 'blue', 'x1': 'pink'}, window=('min(x0, x1)', 'max(x0, x1)')),
        dict(type='array', var='colCosts', label='colCosts（走到第 c 列付 colCosts[c]）', h=200,
             pointers={'y0': 'blue', 'y1': 'pink'}, window=('min(y0, y1)', 'max(y0, y1)')),
        dict(type='text', fn=lambda S: f"当前 ans = ==`{S['ans']}`==" if 'ans' in S else '起点 (x0,y0) 蓝色，终点 (x1,y1) 粉色'),
    ],
    watch=[('x0,y0', '(x0, y0)', 'blue'), ('x1,y1', '(x1, y1)', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'x0, y0 = startPos': '起点：第 `{x0}` 行、第 `{y0}` 列',
        'x1, y1 = homePos': '终点：第 `{x1}` 行、第 `{y1}` 列',
        'ans = -rowCosts': '后面会把起点所在行、列的代价也加进去，但起点是出发处不用付 → 先减掉 `{rowCosts[x0]} + {colCosts[y0]}`，`ans = {ans}`',
        'rowCosts[min': '径直走：上下方向把 `[{min(x0,x1)}, {max(x0,x1)}]` 行都经过一遍，行代价之和 `{sum(rowCosts[min(x0, x1): max(x0, x1) + 1])}`，`ans` → =={ans}==',
        'colCosts[min': '左右方向同理，把 `[{min(y0,y1)}, {max(y0,y1)}]` 列经过一遍，列代价之和 `{sum(colCosts[min(y0, y1): max(y0, y1) + 1])}`，`ans` → =={ans}==',
        'return ans': '行、列互不影响，直走就是最优：最小代价 =={ret}==',
    },
    cards=dict(
        one_liner='代价都非负，绕路只会更贵：径直走，行列分开算',
        complexity='时间 `O(|Δrow| + |Δcol|)`，空间 `O(1)`（Python 切片除外）',
        problem=['网格里机器人从 `startPos` 走回 `homePos`，上下左右各走一步',
                 '走到第 `r` 行付 `rowCosts[r]`，走到第 `c` 列付 `colCosts[c]`',
                 '示例：起点 `(1,0)`，终点 `(2,3)` → 最小代价 `18`'],
        quote='脑筋急转弯：由于题目保证代价均为非负数，所以==除了径直走以外，其它弯弯绕绕的策略都不可能更优==，那么直接统计径直走的代价即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从起点行走到终点行，中间每一行都必须经过；绕路只会多付非负的钱',
              '行和列各算各的：累加 `rowCosts` 与 `colCosts` 的一段子数组',
              '子数组包含起点，所以先减去起点自己的代价，不用分 `x0 < x1` 和 `x0 > x1` 两种情况'],
        summary=['时间 `O(|Δrow| + |Δcol|)`；Python 切片会拷贝，换成循环可做到 `O(1)` 空间',
                 '易错点：起点的代价不计，别忘了先减去 `rowCosts[x0] + colCosts[y0]`',
                 '`min/max` 取闭区间，起点在终点上方或下方都适用',
                 '思考题：若代价可为负，就变成最短路，要用 Bellman-Ford，有负环则是 `-inf`'],
    ),
)
