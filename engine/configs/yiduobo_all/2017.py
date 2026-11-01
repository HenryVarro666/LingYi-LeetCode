G = [[1, 3, 1, 15], [1, 3, 3, 1]]


def _col(S, i, j, v):
    k = S.get('index')
    if k is None or 'res' not in S:
        return None
    if i == 0 and j > k:
        return 'blue'
    if i == 1 and j < k:
        return 'pink'
    return None


def _txt(S):
    k = S.get('index')
    if k is None or 'res' not in S:
        return '`first[p]` = 第 0 行 p 之后的后缀和；`second[p]` = 第 1 行 p 之前的前缀和'
    return f"p = {k}：第二个机器人 `max(first[{k}], second[{k}])` = `max({S['first'][k]}, {S['second'][k]})` = =={max(S['first'][k], S['second'][k])}=="


CONFIG = dict(
    num=2017, title='网格游戏', difficulty='Medium', category='前缀和与差分',
    author='yiduobo', technique='后缀和 + 前缀和 + 枚举',
    tags=[],
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
    call=f'Solution().gridGame({G})',
    expect=7,
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 第 0 行 p 右边，粉 = 第 1 行 p 左边）', cell=96, h=250,
             color=_col, cursors=[(0, 'index', 'yellow'), (1, 'index', 'yellow')]),
        dict(type='array', var='first', label='first：第 0 行的后缀和（first[p] = p 右边之和）', cell=90, h=170, pointers={'index': 'yellow'}),
        dict(type='array', var='second', label='second：第 1 行的前缀和（second[p] = p 左边之和）', cell=90, h=170, pointers={'index': 'yellow'}),
        dict(type='text', fn=_txt, size=24, h=60),
    ],
    watch=[('n', 'n'), ('index', 'index', 'yellow'), ('res', 'res', 'green')],
    captions={
        'n = len(grid[0])': '列数 `n = {n}`',
        'first = [0]': '`first` 先放一个 0：最后一列右边什么也没有',
        'first.append': '从右往左累加第 0 行：`first` 末尾加入 `{first[-1]}`（`grid[0][{index}]` 右边及自己的和）',
        'first.reverse()': '反转后 `first[p]` = 第 0 行 `p + 1` 到末尾的后缀和 = {first}',
        'second = [0]': '`second` 先放一个 0：第 0 列左边什么也没有',
        'second.append': '从左往右累加第 1 行：`second` 末尾加入 `{second[-1]}`',
        'res = first[0]': '`p = 0` 时第二个机器人拿 `first[0] = {first[0]}`（第一个机器人一下来就拐），先当作答案',
        'for index in range(1, n)': lambda S, B, r: ('每一列都枚举完了' if B.get('index') == S.index and S.res != S.first[0]
                                                      else f'枚举第一个机器人在第 `{S.index}` 列向下走'),
        'res = min': lambda S, B, r: f'第二个机器人在 `first[{S.index}] = {S.first[S.index]}` 和 `second[{S.index}] = {S.second[S.index]}` 中取大 `{max(S.first[S.index], S.second[S.index])}`，第一个机器人要它最小：`res` = =={S.res}==',
        'return res': '最少能拿 =={res}==',
    },
    cards=dict(
        one_liner='第二个机器人只能拿「上行后缀」或「下行前缀」之一',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`2 x n` 网格，两个机器人从 `(0,0)` 走到 `(1,n-1)`，只能向右或向下',
                 '第一个走完清零；==第一个想让第二个得分最小，第二个想得分最大==',
                 '示例：`[[1,3,1,15],[1,3,3,1]]` → `7`'],
        quote='第一个机器人必然是在第0行走到位置p，然后向下走到第1行，再从第1行的位置p走到末尾。……第二个机器人显然会选择其中分数较大的那一条',
        quote_src='—— yiduobo 题解原文',
        idea=['分数都大于 0，所以第二个只会考虑两条路：上行 `p+1` 到末尾，或下行 `0` 到 `p-1`',
              '得分 `max(上行后缀和, 下行前缀和)`，先预处理好两个数组',
              '再一趟枚举 `p`，对所有 `max` 取最小'],
        summary=['时间 `O(n)`，空间 `O(n)`（两个辅助数组）',
                 '`first` 是倒着累加再 `reverse`，注意下标对应「p 右边」',
                 '`res` 初值 `first[0]` 对应第一个机器人在第 0 列就拐弯',
                 '对比灵神：灵神用两个变量滚动，空间 `O(1)`；这里显式存前后缀数组'],
    ),
)
