GRID = [[4, 25], [5, 20]]


def _txt(S):
    line = S.get('_line', 0)
    if line < 20:
        return '`two` / `five`：每格含因子 2 / 5 的个数；尾随零 = `min(因子 2 总数, 因子 5 总数)`'
    if line < 47:
        return '`v_*` 纵向前缀和，`h_*` 横向前缀和：任意一段路径的因子总数都能 `O(1)` 取出'
    return f'枚举拐点 `({S["i"]},{S["j"]})`（黄框）：竖直取上或下、水平取左或右，路径延伸到边界'


def _comb(S, B, r):
    i, j = S.i, S.j
    return (f'拐点 `({i},{j})` 自己是 `{S.two[i][j]}` 个 2、`{S.five[i][j]}` 个 5；'
            f'竖直取上或下、水平取左或右，四种组合各取 `min(2 的总数, 5 的总数)`；上 + 左 = =={S.up_left}==')


CONFIG = dict(
    num=2245, title='转角路径的乘积中最多能有几个尾随零', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举拐点 + 行列前缀和',
    tags=['灵神题单·常用数据结构', '难度分 2037'],
    code='''
class Solution(object):
    def maxTrailingZeros(self, grid):

        m = len(grid)
        n = len(grid[0])

        two = [[0] * n for _ in range(m)]
        five = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                now = grid[i][j]
                while now % 2 == 0:
                    two[i][j] += 1
                    now //= 2
                while now % 5 == 0:
                    five[i][j] += 1
                    now //= 5

        v_two =[[0] * n for _ in range(m)]
        v_five = [[0] * n for _ in range(m)]
        h_two = [[0] * n for _ in range(m)]
        h_five = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0:
                    v_two[i][j] = two[i][j]
                    v_five[i][j] = five[i][j]
                else:
                    v_two[i][j] = v_two[i - 1][j] + two[i][j]
                    v_five[i][j] = v_five[i - 1][j] + five[i][j]

                if j == 0:
                    h_two[i][j] = two[i][j]
                    h_five[i][j] = five[i][j]
                else:
                    h_two[i][j] = h_two[i][j - 1] + two[i][j]
                    h_five[i][j] = h_five[i][j - 1] + five[i][j]
        
        res = 0
        for i in range(m):
            for j in range(n):
                if i == 0:
                    up_two = 0
                    up_five = 0
                else:
                    up_two = v_two[i - 1][j]
                    up_five = v_five[i - 1][j]
                
                down_two = v_two[m - 1][j] - v_two[i][j]
                down_five = v_five[m - 1][j] - v_five[i][j]

                if j == 0:
                    left_two = 0
                    left_five = 0
                else:
                    left_two = h_two[i][j - 1]
                    left_five = h_five[i][j - 1]
                
                right_two = h_two[i][n - 1] - h_two[i][j]
                right_five = h_five[i][n - 1] - h_five[i][j]

                up_left = min(up_two + left_two + two[i][j], up_five + left_five + five[i][j])
                up_right = min(up_two + right_two + two[i][j], up_five + right_five + five[i][j])
                down_left = min(down_two + left_two + two[i][j], down_five + left_five + five[i][j])
                down_right = min(down_two + right_two + two[i][j], down_five + right_five + five[i][j])

                res = max(res, up_left, up_right, down_left, down_right)
        
        return res
''',
    call=f'Solution().maxTrailingZeros({GRID})',
    expect=3,
    views=[
        dict(type='text', fn=_txt),
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '')], label='grid', h=210, cell=84),
        dict(type='grid', var='two', cursors=[('i', 'j', 'yellow', '')], label='two（因子 2）', h=190, cell=70),
        dict(type='grid', var='five', cursors=[('i', 'j', 'yellow', '')], label='five（因子 5）', h=190, cell=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    skip=['m = len', 'n = len', 'two = [[', 'five = [[', 'v_two =[[', 'v_five = [[', 'h_two = [[', 'h_five = [[',
          'for i in range(m)', 'for j in range(n)', 'now = grid', 'while now', 'now //=', 'if i == 0', 'if j == 0',
          'v_five[i][j] =', 'h_five[i][j] =', 'up_five =', 'down_five =', 'left_five =', 'right_five =', 'res = 0', 'up_two = 0', 'left_two = 0'],
    max_steps=90,
    captions={
        14: '`grid[{i}][{j}] = {grid[i][j]}`：当前剩 `{now}` 还能被 2 整除 → `two[{i}][{j}]` 记到 {two[i][j]}',
        17: '`grid[{i}][{j}] = {grid[i][j]}`：当前剩 `{now}` 还能被 5 整除 → `five[{i}][{j}]` 记到 {five[i][j]}',
        27: '纵向前缀和（`v_five` 同步）：第 0 行没有上一行，`v_two[0][{j}] = two[0][{j}]` = {v_two[0][j]}',
        30: '纵向前缀和：`v_two[{i}][{j}] = v_two[{i - 1}][{j}] + two[{i}][{j}]` = {v_two[i][j]}',
        34: '横向前缀和（`h_five` 同步）：第 0 列没有左邻，`h_two[{i}][0] = two[{i}][0]` = {h_two[i][0]}',
        37: '横向前缀和：`h_two[{i}][{j}] = h_two[{i}][{j - 1}] + two[{i}][{j}]` = {h_two[i][j]}',
        47: '拐点上方的竖直段（最上一行没有上方，记 0）：`up_two = v_two[{i - 1}][{j}]` = {up_two}',
        50: '拐点下方的竖直段：`down_two = v_two[末行] − v_two[{i}][{j}]` = {down_two}',
        57: '拐点左边的水平段（最左一列没有左边，记 0）：`left_two = h_two[{i}][{j - 1}]` = {left_two}',
        60: '拐点右边的水平段：`right_two = h_two[{i}][末列] − h_two[{i}][{j}]` = {right_two}',
        63: _comb,
        64: '上 + 右：`min(因子 2, 因子 5)` = =={up_right}==',
        65: '下 + 左：`min(因子 2, 因子 5)` = =={down_left}==',
        66: '下 + 右：`min(因子 2, 因子 5)` = =={down_right}==',
        68: '`res` 取四种拐法与旧 `res` 的最大值：`{B.res if "res" in B else 0}` → =={res}==',
        'return res': '最优拐点给出最多的尾随零：`{res}` 个',
    },
    cards=dict(
        one_liner='枚举拐点，上下左右四段都用行列前缀和一次取出',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里每格是正整数，路径最多拐一次弯（一横一竖）',
                 '求路径乘积的尾随零个数最大值',
                 '本视频：`[[4,25],[5,20]]` → `3`（`4×25×20 = 2000`）'],
        quote='对于这类有明确分割点的问题，还是按照通常的做法，枚举这个分割点的位置，即枚举转角这个角的坐标。',
        quote_src='—— yiduobo 题解原文',
        idea=['尾零数 = `min(因子 2 个数, 因子 5 个数)`，先算出每格的 `two`、`five`',
              '矩阵里没有 0，数字越多越好 → 拐点定了，上下选一边、左右选一边，全部延伸到边界',
              '每行每列预处理前缀和，四段的因子总数 `O(1)` 取出，四种组合取最大'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '拐点所在格只加一次：`up` / `down` 不含拐点，`left` / `right` 也不含，最后再加 `two[i][j]`',
                 '原文是 Python 2 写法，整数除法 `now /= 2`、`now /= 5` 已改为 `//=`',
                 '对比灵神：灵神只扫列、行用前缀；这里行列各一套前缀表'],
    ),
)
