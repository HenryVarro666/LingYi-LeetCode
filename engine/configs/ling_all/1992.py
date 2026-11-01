def _col(S, i, j, v):
    if v == 0:
        return None
    if 'ii' in S and 'jj' in S and 'i' in S and 'j' in S and S['i'] <= i <= S['ii'] and S['j'] <= j <= S['jj']:
        return 'green'
    for r1, c1, r2, c2 in S.get('ans', []):
        if r1 <= i <= r2 and c1 <= j <= c2:
            return 'blue'
    return None


CONFIG = dict(
    num=1992, title='找到所有的农场组', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='找矩形左上角，再向右下延伸（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1539'],
    code='''
class Solution:
    def findFarmland(self, a: List[List[int]]) -> List[List[int]]:
        n, m = len(a), len(a[0])
        ans = []
        for i, row in enumerate(a):
            for j, v in enumerate(row):
                if v == 0 or j > 0 and row[j-1] == 1 or i > 0 and a[i-1][j] == 1:
                    continue
                ii = i
                while ii+1 < n and a[ii+1][j] == 1:
                    ii += 1
                jj = j
                while jj+1 < m and a[ii][jj+1] == 1:
                    jj += 1
                ans.append([i, j, ii, jj])
        return ans
''',
    call='Solution().findFarmland([[1,0,0],[0,1,1],[0,1,1]])',
    expect=[[0,0,0,0],[1,1,2,2]],
    views=[
        dict(type='grid', var='a', label='a（绿 = 正在延伸的农场组，蓝 = 已记录的农场组）', cell=96, h=420,
             color=_col, cursors=[('i', 'j', 'yellow')]),
        dict(type='text', fn=lambda S: f"已找到 `{len(S['ans'])}` 个农场组：`{S['ans']}`" if 'ans' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'ii', 'jj', ('ans', 'ans', 'green')],
    max_steps=90,
    captions={
        'if v == 0 or': lambda S, B, r: (f"`({S.i},{S.j})` 是森林 → 不是农场，跳过" if S.v == 0 else
                                          f"`({S.i},{S.j})` 左边是 1 → 在矩形内部或上边缘，跳过" if S.j > 0 and S.row[S.j-1] == 1 else
                                          f"`({S.i},{S.j})` 上边是 1 → 在矩形内部或左边缘，跳过" if S.i > 0 and S.a[S.i-1][S.j] == 1 else
                                          f"`({S.i},{S.j})` 是 1，左边和上边都不是 1 → ==矩形左上角=="),
        'ii = i': '是左上角，先让下边界 `ii = {ii}`',
        'ii += 1': '下面还是 1 → 下边界 `ii` 下移到 {ii}',
        'jj = j': '再让右边界 `jj = {jj}`，沿着最后一行 `a[ii]` 往右找',
        'jj += 1': '右边还是 1 → 右边界 `jj` 右移到 {jj}',
        'ans.append': '矩形 `[{i}, {j}, {ii}, {jj}]` 记入答案',
        'return ans': '所有农场组：`{ans}`',
    },
    cards=dict(
        one_liner='只在矩形左上角出手，然后向下、向右找边界',
        complexity='时间 `O(nm)`，空间 `O(1)`（不计答案）',
        problem=['`land` 里 1 是农场，农场组都是互不相邻的矩形',
                 '返回每个农场组的左上角与右下角 `[r1,c1,r2,c2]`',
                 '示例：`[[1,0,0],[0,1,1],[0,1,1]]` → `[[0,0,0,0],[1,1,2,2]]`'],
        quote='判断是否为矩形左上角，需要满足三个条件：元素值为 1；左边是边界或者是 0；上边是边界或者是 0。然后遍历找到矩形的右边界和下边界。',
        quote_src='—— 灵茶山艾府题解',
        idea=['矩形的左上角：自己是 1，左边和上边都不是 1',
              '矩形互不相邻，所以从左上角往下走到头是下边界 `ii`，往右走到头是右边界 `jj`',
              '每个格子最多被扫一次边，整体线性'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(nm)`，空间 `O(1)`',
                 '易错点：`jj` 要沿着下边界那一行 `a[ii]` 找，不是 `a[i]`；越界判断放在 `and` 前面',
                 '不用 visited 数组：矩形互不相邻 + 只认左上角，就不会重复'],
    ),
)
