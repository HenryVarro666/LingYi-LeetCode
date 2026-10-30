def _cell(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if ci is None or cj is None or S['_line'] < 6:
        return None
    if i == ci and j == cj:
        return 'yellow'
    if i == ci:
        return 'blue'
    if j == cj:
        return 'pink'
    return None


def _formula(S):
    if 'ans' not in S or 'x' not in S:
        return ''
    i, j, x = S['i'], S['j'], S['x']
    r, c = S['row_max'][i], S['col_max'][j]
    return f"`min(rowMax[{i}]={r}, colMax[{j}]={c}) − {x}` = =={min(r, c) - x}=="


CONFIG = dict(
    num=807, title='保持城市天际线', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='行最大 / 列最大 · 取较小者',
    code='''
class Solution:
    def maxIncreaseKeepingSkyline(self, grid: List[List[int]]) -> int:
        row_max = list(map(max, grid))
        col_max = list(map(max, zip(*grid)))
        ans = 0
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                ans += min(row_max[i], col_max[j]) - x
        return ans
''',
    call='Solution().maxIncreaseKeepingSkyline([[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]])',
    expect=35,
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 第 i 行，粉 = 第 j 列，黄 = 当前楼；左侧=行最大，上方=列最大）', cell=84, h=330,
             cursors=[], color=_cell,
             rows=lambda S: [f"{m}" for m in S['row_max']] if 'row_max' in S else None,
             cols=lambda S: [f"{m}" for m in S['col_max']] if 'col_max' in S else None),
        dict(type='text', h=70, size=30, fn=_formula),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('x', 'x', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'row_max = ': '每行的最大值（从东、西看到的天际线）：`row_max = {row_max}`',
        'col_max = ': '`zip(*grid)` 把列转成行，再取每列最大值（从南、北看）：`col_max = {col_max}`',
        'ans = 0': '`ans` 累计所有楼能增加的高度',
        'for i, row': lambda S, B, r: (f"看第 `{S.i}` 行，这一行的上限是 `row_max[{S.i}] = {S.row_max[S.i]}`" if 'i' not in B or S.i != B.i else '所有行都看完了'),
        'for j, x': lambda S, B, r: (f"看 `({S.i}, {S.j})` 这栋楼，高度 `x = {S.x}`；这一列的上限是 `col_max[{S.j}] = {S.col_max[S.j]}`" if 'j' not in B or S.j != B.j or S.i != B.i else '这一行的楼都看完了'),
        'ans += ': '至多加到 `min({row_max[i]}, {col_max[j]}) = {min(row_max[i], col_max[j])}`，能增加 `{min(row_max[i], col_max[j])} − {x}` = =={min(row_max[i], col_max[j]) - x}==，累计 `ans = {ans}`',
        'return ans': '所有楼增加的高度之和 `{ans}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='每栋楼最多加到所在行、所在列最大值中的较小者',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['`grid[r][c]` 是街区 `(r, c)` 上楼的高度，可以随意加高',
                 '但从东南西北四个方向看到的==天际线不能变==，求高度增量总和最大是多少',
                 '示例：`[[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]]` → `35`'],
        quote='第一行的最大值是 8，只要第一行的数，增大到不超过 8，就不会改变从西边看和从东边看的天际线。对于其他行也同理。',
        quote_src='—— 灵茶山艾府题解',
        idea=['行最大值决定东西方向的天际线，列最大值决定南北方向',
              '`grid[i][j]` 同时受两者约束：至多增加到 `min(rowMax[i], colMax[j])`',
              '每栋楼的增量 `min(rowMax[i], colMax[j]) − grid[i][j]` 加起来就是答案'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`',
                 '`zip(*grid)` 是转置，用来按列取最大值',
                 '易错：别忘了减掉原高度 `grid[i][j]`',
                 '题解还给了写法二：`sum(map(min, product(row_max, col_max))) - sum(map(sum, grid))`，一行完成，思路相同'],
    ),
)
