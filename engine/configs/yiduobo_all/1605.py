CONFIG = dict(
    num=1605, title='给定行和列的和求可行矩阵', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='逐行填充 · pos 记录当前列',
    tags=['贪心算法', '构造题', '难度分 1868'],
    code='''
class Solution(object):
    def restoreMatrix(self, rowSum, colSum):

        m = len(rowSum)
        n = len(colSum)
        res = [[0] * n for _ in range(m)]
        
        pos = 0
        for index in range(m):
            while colSum[pos] < rowSum[index]:
                res[index][pos] = colSum[pos]
                rowSum[index] -= colSum[pos]
                pos += 1
            
            res[index][pos] = rowSum[index]
            colSum[pos] -= rowSum[index]
        
        return res
''',
    call='Solution().restoreMatrix([14,9], [6,9,8])',
    expect=[[6, 8, 0], [0, 1, 8]],
    views=[
        dict(type='array', var='rowSum', h=150, label='rowSum（这一行还缺多少）', pointers={'index': 'blue'}, cell=70),
        dict(type='array', var='colSum', h=150, label='colSum（这一列还剩多少可分配）', pointers={'pos': 'pink'}, cell=70,
             dim=lambda S, k, v: k < S.get('pos', 0)),
        dict(type='grid', var='res', h=260, label='res（蓝框 = 当前填的位置）', cell=90,
             cursors=[('index', 'pos', 'blue')],
             color=lambda S, i, j, v: 'green' if v else None),
    ],
    watch=[('index', 'index', 'blue'), ('pos', 'pos', 'pink')],
    skip=['m = len', 'n = len', 'res = [[0]'],
    max_steps=60,
    captions={
        'pos = 0': '`pos` 记录当前填充的列，从第 0 列开始',
        'for index in range(m)': lambda S, B, r: ('所有行都处理完了，退出循环' if B.get('index') == S.index
                                              else f'逐行处理：第 `{S.index}` 行，需要凑出 `rowSum[{S.index}] = {S.rowSum[S.index]}`'),
        'while colSum[pos] < rowSum[index]': lambda S, B, r: (
            f'`colSum[{S.pos}] = {S.colSum[S.pos]} < rowSum[{S.index}] = {S.rowSum[S.index]}`：这一列全给这一行也不够 → ==整列分给它=='
            if S.colSum[S.pos] < S.rowSum[S.index]
            else f'`colSum[{S.pos}] = {S.colSum[S.pos]} ≥ rowSum[{S.index}] = {S.rowSum[S.index]}`：这一列足够 → 只需要取 `rowSum[{S.index}]`'),
        'res[index][pos] = colSum[pos]': '整列给这一行：`res[{index}][{pos}] = {colSum[pos]}`，这列用完',
        'rowSum[index] -= colSum[pos]': '这一行还缺 `rowSum[{index}] = {rowSum[index]}`，但没满足，要继续往后找列',
        'pos += 1': '`pos` 右移到第 {pos} 列，重复判断',
        'res[index][pos] = rowSum[index]': '这一行满足了：`res[{index}][{pos}] = rowSum[{index}] = {rowSum[index]}`，这一行结束',
        'colSum[pos] -= rowSum[index]': '这一列还剩 `colSum[{pos}] = {colSum[pos]}`，==pos 不动==，留给下一行继续用',
        'return res': '所有行都填完，返回 `res`',
    },
    cards=dict(
        one_liner='逐行填充：一列不够就整列给，够了就切一块，pos 只增不减',
        complexity='时间 `O(m+n)`（不计建矩阵），空间 `O(1)`',
        problem=['已知每行的和 `rowSum`、每列的和 `colSum`，构造任意一个非负整数矩阵',
                 '本质是 `m+n` 个方程解 `m×n` 个未知数，题目保证有解',
                 '本视频：`rowSum=[14,9]`，`colSum=[6,9,8]`',
                 '→ `[[6,8,0],[0,1,8]]`'],
        quote='若当前的colSum[pos] < rowSum[index]，那么就将pos这一列的值全部分配给index这一行，也就是说设置res[index][pos]为colSum[pos]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pos` 记录当前列。列不够：整列给当前行，`pos` 后移，行需求减少',
              '列够了：只切 `rowSum[index]`，这一行结束，列剩余留给下一行（pos 不动）',
              '总和相等，所以 `pos` 不会越界'],
        summary=['时间 `O(m+n)`（不计创建矩阵），空间 `O(1)`',
                 '易错：第二种情况 `pos` ==不能移动==，这一列可能还有剩余',
                 '`colSum[pos]` 与 `rowSum[index]` 相等时进入第二种，这一列恰好用完',
                 '对比灵神：灵神每步直接选行或列去掉；yiduobo 以行为主循环，内层 while 吃列',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
