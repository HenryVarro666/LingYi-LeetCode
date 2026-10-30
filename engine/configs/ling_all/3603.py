W = [[6, 1, 4], [3, 2, 5]]


def _fv(S):
    f = S.get('f')
    if f is None:
        return None
    return ['∞' if x == float('inf') else x for x in f]


def _cur(S, i, j, v):
    return None


CONFIG = dict(
    num=3603, title='交替方向的最小路径代价 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='转化成最小路径和 + 一维空间优化',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1639'],
    code='''
# 手写 min 更快
min = lambda a, b: b if b < a else a

class Solution:
    def minCost(self, m: int, n: int, waitCost: List[List[int]]) -> int:
        f = [inf] * (n + 1)
        f[1] = -waitCost[0][0]
        for i, row in enumerate(waitCost):
            for j, c in enumerate(row):
                f[j + 1] = min(f[j], f[j + 1]) + c + (i + 1) * (j + 1)
        return f[n] - waitCost[-1][-1]
''',
    call=f'Solution().minCost(2, 3, {W})',
    expect=16,
    skip=['min = lambda', 'for i, row', 'for j, c in'],
    views=[
        dict(type='grid', var='waitCost', label='waitCost（黄 = 当前格 (i,j)）', cell=84, h=210,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='array', var=_fv, label='f（f[j+1] = 走到当前行第 j 列的最小代价，含该格等待）', cell=100, h=190,
             pointers={'j': 'blue'}),
        dict(type='text', fn=lambda S: (f"格子代价 = 等待 `{S['c']}` + 进入 `({S['i']+1})×({S['j']+1}) = {(S['i']+1)*(S['j']+1)}`"
                                         if 'c' in S and 'i' in S else '每格代价 = `waitCost + (i+1)*(j+1)`，转成最小路径和'), size=24, h=50),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'blue'), 'c'],
    captions={
        'f = [inf]': '`f` 长 `n+1`，初始全是 `inf`：下标 0 是出界哨兵',
        'f[1] = -waitCost[0][0]': '起点不需要等待：先填 `-waitCost[0][0] = {f[1]}`，算 `f[1]` 时会被加回来抵消',
        'f[j + 1] = min': lambda S, B, r: (f'`f[{S.j+1}] = min(左 {B.f[S.j]}, 上 {B.f[S.j+1]}) + {S.c} + {(S.i+1)*(S.j+1)}` = =={S.f[S.j+1]}=='
                                           .replace('inf', '∞')),
        'return f[n]': '终点不需要等待：`f[{n}] - waitCost[-1][-1] = {f[n]} - {waitCost[-1][-1]}` = =={ret}==',
    },
    cards=dict(
        one_liner='进入后必须等、等完必须走：每格代价固定，变成最小路径和',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['进入 `(i,j)` 成本 `(i+1)*(j+1)`，等待成本 `waitCost[i][j]`',
                 '奇数秒必须向右/下走，偶数秒必须原地等 1 秒',
                 '求从 `(0,0)` 到 `(m-1,n-1)` 的最小总成本',
                 '本视频：`m=2, n=3, waitCost=[[6,1,4],[3,2,5]]` → `16`'],
        quote='所以问题相当于每个单元格的值为 waitCost[i][j] + (i+1)·(j+1)，在此基础上求最小路径和。这样就转化成 64 题了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['进入一格后下一秒必等，等完又必须走：每格的「等待 + 进入」捆在一起',
              '起点和终点不用等待：起点初值填 `-waitCost[0][0]`，终点最后减掉',
              '只依赖上一行，把二维 `f` 压成一维'],
        summary=['时间 `O(mn)`，空间 `O(n)`；灵神还给了记忆化、二维递推、原地改 `waitCost` 的写法',
                 '易错：起点、终点都无需等待，别多算',
                 '易错：`f[0]` 与下一行的哨兵必须是 `inf`，一维数组更新时 `f[j+1]` 还是上一行的值',
                 '同类题：64. 最小路径和'],
    ),
)
