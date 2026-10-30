W = [[6, 1, 4], [3, 2, 5]]

CONFIG = dict(
    num=3603, title='交替方向的最小路径代价 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='网格 DP · 上一格代价 + 上一格等待',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1639'],
    code='''
class Solution(object):
    def minCost(self, m, n, waitCost):
        
        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    f[i][j] = 1
                elif i == 0:
                    if j == 1:
                        f[i][j] = 3
                    else:
                        f[i][j] = f[i][j - 1] + waitCost[i][j - 1] + (i + 1) * (j + 1)
                elif j == 0:
                    if i == 1:
                        f[i][j] = 3
                    else:
                        f[i][j] = f[i - 1][j] + waitCost[i - 1][j] + (i + 1) * (j + 1)
                else:
                    f[i][j] = min(f[i][j - 1] + waitCost[i][j - 1], f[i - 1][j] + waitCost[i - 1][j]) + (i + 1) * (j + 1)
        
        return f[-1][-1]
''',
    call=f'Solution().minCost(2, 3, {W})',
    expect=16,
    skip=['for i in range', 'for j in range', 'for _ in range'],
    views=[
        dict(type='grid', var='waitCost', label='waitCost（黄 = 当前格）', cell=84, h=190,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='table', var='f', label='f[i][j]：走到 (i,j) 的最小代价（尚未等待）', cell=100, h=230,
             color=lambda S, i, j, v: 'yellow' if (i, j) == (S.get('i'), S.get('j')) and S.get('_line') in (8, 11, 13, 16, 18, 20) else None),
        dict(type='text', fn=lambda S: '`f[i][j]` = 上一格的 `f` + 在上一格的等待 + 进入 `(i+1)*(j+1)`', size=24, h=50),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow')],
    captions={
        'f = [[0]': '`f[i][j]` 表示走到 `(i, j)` 所需的最小代价',
        'f[i][j] = 1': '`(0,0)`：只付进入成本 `1*1 = 1`',
        'f[i][j] = 3': '`({i},{j})` 是第一步：`1 + 2 = 3`，起点不用等待，所以不加 waitCost',
        'f[i][j] = f[i][j - 1] +': '第 0 行只能从左来：`f[{i}][{j}] = {f[i][j-1]} + 等待 {waitCost[i][j-1]} + 进入 {(i+1)*(j+1)}` = =={f[i][j]}==',
        'f[i][j] = f[i - 1][j] +': '第 0 列只能从上来：`f[{i}][{j}] = {f[i-1][j]} + 等待 {waitCost[i-1][j]} + 进入 {(i+1)*(j+1)}` = =={f[i][j]}==',
        'f[i][j] = min(': '取左 `{f[i][j-1]}+{waitCost[i][j-1]}` 与上 `{f[i-1][j]}+{waitCost[i-1][j]}` 的较小者，再加进入 `{(i+1)*(j+1)}` = =={f[i][j]}==',
        'return f[-1][-1]': '终点不用等待，`f[-1][-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='走到一格前，必须先在上一格等 1 秒：f 里加上一格的等待',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['进入 `(i,j)` 成本 `(i+1)*(j+1)`，在 `(i,j)` 等待成本 `waitCost[i][j]`',
                 '奇数秒向右/下移动，偶数秒原地等待 1 秒',
                 '求到达 `(m-1,n-1)` 的最小成本',
                 '本视频：`[[6,1,4],[3,2,5]]` → `16`'],
        quote='除了第一秒进入(0, 0)，并走到(0, 1)或者(1, 0)外，其他所有奇数秒的行动之前，必然存在一个偶数秒的等待。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j] = min(f[i-1][j] + waitCost[i-1][j], f[i][j-1] + waitCost[i][j-1]) + (i+1)*(j+1)`',
              '即「上一格的代价 + 在上一格等待 + 进入本格」',
              '`(0,0)`、`(0,1)`、`(1,0)` 单独赋值，第 0 行/列只有一个来源'],
        summary=['时间/空间 `O(mn)`',
                 '易错：等待发生在==离开的那一格==，所以加的是上一格的 waitCost',
                 '易错：`(0,1)`、`(1,0)` 前面只有起点，不需要等待，直接是 3',
                 '对比灵神：灵神把等待算进每格，起点终点再抵消；yiduobo 把等待算在转移上'],
    ),
)
