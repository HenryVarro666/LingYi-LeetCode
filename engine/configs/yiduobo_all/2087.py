CONFIG = dict(
    num=2087, title='网格图中机器人回家的最小代价', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='行列分开 · 直走累加',
    tags=['脑筋急转弯', '难度分 1744'],
    code='''
class Solution(object):
    def minCost(self, startPos, homePos, rowCosts, colCosts):

        row_delta = col_delta = 1
        if startPos[0] > homePos[0]:
            row_delta = -1
        if startPos[1] > homePos[1]:
            col_delta = -1
        
        res = 0
        for index in range(startPos[0] + row_delta, homePos[0] + row_delta, row_delta):
            res += rowCosts[index]
        for index in range(startPos[1] + col_delta, homePos[1] + col_delta, col_delta):
            res += colCosts[index]
        
        return res
''',
    call='Solution().minCost([3, 3], [1, 0], [5, 4, 3, 6], [8, 2, 6, 7])',
    expect=23,
    views=[
        dict(type='array', var='rowCosts', label='rowCosts（蓝 = 起点行，粉 = 目标行，黄 = 正在累加）', h=200,
             pointers={'startPos[0]': 'blue', 'homePos[0]': 'pink'},
             color=lambda S, i, v: 'yellow' if S.get('_inner', {}).get('index') == i and 'index' in S and S['_line'] in (11, 12) else None),
        dict(type='array', var='colCosts', label='colCosts（蓝 = 起点列，粉 = 目标列，黄 = 正在累加）', h=200,
             pointers={'startPos[1]': 'blue', 'homePos[1]': 'pink'},
             color=lambda S, i, v: 'yellow' if S.get('_inner', {}).get('index') == i and 'index' in S and S['_line'] in (13, 14) else None),
        dict(type='text', fn=lambda S: f"累计代价 res = ==`{S['res']}`==" if 'res' in S else ''),
    ],
    watch=['row_delta', 'col_delta', ('index', 'index', 'yellow'), ('res', 'res', 'green')],
    captions={
        'row_delta = col_delta': '先假设行、列都是往编号增大的方向走（步长 `+1`）',
        'startPos[0] > homePos[0]': lambda S, B, r: f'起点行 `{S.startPos[0]}` {"大于" if S.startPos[0] > S.homePos[0] else "不大于"}目标行 `{S.homePos[0]}` → ' + ('行要往回走，`row_delta = -1`' if S.startPos[0] > S.homePos[0] else '保持 `+1`'),
        'startPos[1] > homePos[1]': lambda S, B, r: f'起点列 `{S.startPos[1]}` {"大于" if S.startPos[1] > S.homePos[1] else "不大于"}目标列 `{S.homePos[1]}` → ' + ('列要往回走，`col_delta = -1`' if S.startPos[1] > S.homePos[1] else '保持 `+1`'),
        'for index in range(startPos[0]': '行：从起点的==下一行==走到目标行（含），中间每行都必须经过，不用再算起点',
        'res += rowCosts': '经过第 `{index}` 行，付 `rowCosts[{index}] = {rowCosts[index]}`，`res` → =={res}==',
        'for index in range(startPos[1]': '列：同样从起点的下一列走到目标列，行列互不影响',
        'res += colCosts': '经过第 `{index}` 列，付 `colCosts[{index}] = {colCosts[index]}`，`res` → =={res}==',
        'return res': '直走就是最优，最小代价 =={ret}==',
    },
    cards=dict(
        one_liner='行列互不影响：分开考虑，每行每列至少经过一次，直走最省',
        complexity='时间 `O(|Δrow| + |Δcol|)`，空间 `O(1)`',
        problem=['机器人从 `startPos` 走回 `homePos`，四个方向都能走',
                 '走到第 `r` 行付 `rowCosts[r]`，走到第 `c` 列付 `colCosts[c]`',
                 '本视频：起点 `(3,3)` 到终点 `(1,0)`，要往上、往左走'],
        quote='题目中行列互不影响，那么可以分开来考虑。要从起始行走到目标行，这中间的所有行都必须经过至少一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次经过的代价都非负，经过次数当然越少越好 → 从起始行直接往目标行走',
              '列同理，直接往目标列走',
              '用 `row_delta / col_delta` 记录方向，遍历途中的行、列累加代价'],
        summary=['时间 `O(|Δrow| + |Δcol|)`，空间 `O(1)`',
                 '`range` 的终点要写 `homePos + delta`，才能把目标行、列包含进来',
                 '遍历从 `startPos + delta` 开始，起点自己的代价不计入',
                 '对比灵神：灵神用 `min/max` 切片求和再减去起点；yiduobo 直接确定方向后逐个累加'],
    ),
)
