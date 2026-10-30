G = [[1, 3, 1, 15], [1, 3, 3, 1]]


def _cell(S, i, j, v):
    if 'res' not in S or 'index' not in S:
        return None
    p = S['index']
    if i == 0 and j > p:
        return 'green'
    if i == 1 and j < p:
        return 'orange'
    if (i == 0 and j <= p) or (i == 1 and j >= p):
        return 'pink'
    return None


def _fn(S):
    if 'res' not in S or 'index' not in S:
        return '第一个机器人在第 0 行走到下标 p 再下到第 1 行；第二个只能拿「第 0 行 p 之后」或「第 1 行 p 之前」'
    p = S['index']
    return (f'第一个机器人在 `p = {p}` 下楼：第二个拿 `max(first[{p}], second[{p}])` = '
            f'`max({S["first"][p]}, {S["second"][p]})` = =={max(S["first"][p], S["second"][p])}==')


CONFIG = dict(
    num=2017, title='网格游戏', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前缀和 + 后缀和 · 枚举拐点',
    tags=['前缀和', '博弈'],
    code='''
class Solution(object):
    def gridGame(self, grid):

        n = len(grid[0])
        first = [0]
        for index in range(n - 1, 0, -1):
            first.append(first[-1] + grid[0][index])
        first.reverse()

        second = [0]
        for index in range(n - 1):
            second.append(second[-1] + grid[1][index])
        
        res = first[0]
        for index in range(1, n):
            res = min(res, max(first[index], second[index]))
        
        return res
''',
    call=f'Solution().gridGame({G!r})',
    expect=7,
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 第 0 行 p 之后，橙 = 第 1 行 p 之前，粉 = 第一个机器人的路）', cell=110, h=250,
             color=_cell),
        dict(type='array', var='first', label='first：第 0 行的后缀和（first[p] = grid[0][p+1:] 之和）', cell=84, h=150, index=True),
        dict(type='array', var='second', label='second：第 1 行的前缀和（second[p] = grid[1][:p] 之和）', cell=84, h=150, index=True),
        dict(type='text', h=70, size=28, fn=_fn),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'n = len(grid[0])': '只有两行，列数 `n = {n}`',
        'first = [0]': '先造第 0 行的==后缀和==：`first[p]` = `grid[0][p+1:]` 之和，最后一格是 0',
        'first.append': '从右往左累加：`first` 加入 `{first[-1]}`（加上 `grid[0][{index}]`）',
        'first.reverse()': '反转后 `first[p]` 对应「p 右边所有格子」之和：`{first}`',
        'second = [0]': '再造第 1 行的==前缀和==：`second[p]` = `grid[1][:p]` 之和',
        'second.append': '从左往右累加：`second` 加入 `{second[-1]}`（加上 `grid[1][{index}]`）',
        'res = first[0]': '先假设第一个机器人在 `p = 0` 就下楼，第二个拿走第 0 行剩下的：`res = {res}`',
        'for index in range(1, n)': '第一个机器人在 `p = {index}` 下楼',
        'res = min(res, max(': lambda S, B, ret: (
            f'第二个取 `max(first[{S.index}], second[{S.index}])` = `max({S.first[S.index]}, {S.second[S.index]})` = '
            f'`{max(S.first[S.index], S.second[S.index])}`；第一个要它最小：`res = min({B.res}, …)` = =={S.res}=='),
        'return res': '所有拐点里第二个机器人得分的最小值：`{res}`',
    },
    cards=dict(
        one_liner='第一个机器人在哪下楼，第二个就只能拿「上面剩余」或「下面剩余」的较大者',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`2 x n` 的网格，两个机器人都从左上走到右下，只能右 / 下走',
                 '第一个先走并把走过的格子清零，第二个再走；第一个要让第二个得分最小',
                 '示例：`[[1,3,1,15],[1,3,3,1]]` → `7`'],
        quote='第一个机器人必然是在第0行走到位置p，然后向下走到第1行，再从第1行的位置p走到末尾。……第二个机器人显然会选择其中分数较大的那一条。',
        quote_src='—— yiduobo 题解原文',
        idea=['网格只有两行：第一个机器人只需决定在哪一列 `p` 下楼',
              '第二个机器人的好路只有两条：拿第 0 行 `p` 之后的，或第 1 行 `p` 之前的',
              '得分 = `max(第 0 行后缀和, 第 1 行前缀和)`，枚举 `p` 取最小'],
        summary=['时间 `O(n)`，空间 `O(n)`（可优化成 `O(1)`）',
                 '`first` 是后缀和（先倒着累加再 reverse），`second` 是前缀和',
                 '易错：`p` 处的两格被第一个机器人拿走，后缀和从 `p+1` 起、前缀和到 `p-1` 止',
                 '分数都是正数，所以第二个只会选这两条路之一'],
    ),
)
