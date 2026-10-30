G = [[0, 1, 1], [1, 0, 1], [0, 0, 1]]


def _cell(S, i, j, v):
    return 'green' if v == 1 else None


CONFIG = dict(
    num=2482, title='行和列中一和零的差值', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · 0 当成 -1 统计行列和',
    tags=[],
    code='''
class Solution:
    def onesMinusZeros(self, grid: List[List[int]]) -> List[List[int]]:
        r = [0] * len(grid)
        c = [0] * len(grid[0])
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                r[i] += x * 2 - 1
                c[j] += x * 2 - 1  # 1 -> 1, 0 -> -1
        for i, x in enumerate(r):
            for j, y in enumerate(c):
                grid[i][j] = x + y
        return grid
''',
    call=f'Solution().onesMinusZeros({G!r})',
    expect=[[0, 0, 4], [0, 0, 4], [-2, -2, 2]],
    views=[
        dict(type='grid', var='grid', label='grid（先放 0/1，后面直接被覆盖成答案）', cursors=[('i', 'j', 'yellow', '(i,j)')], h=330, cell=96,
             color=_cell),
        dict(type='array', var='r', label='r[i]：第 i 行 (1 的个数 − 0 的个数)', h=170, color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='array', var='c', label='c[j]：第 j 列 (1 的个数 − 0 的个数)', h=170, color=lambda S, i, v: 'pink' if S.get('j') == i else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('x', 'x', 'yellow')],
    captions={
        'r = [0]': '`r[i]` 记第 `i` 行 “1 的个数 − 0 的个数”',
        'c = [0]': '`c[j]` 记第 `j` 列同样的差；列数 `{len(c)}`',
        'r[i] += x * 2 - 1': '`grid[{i}][{j}] = {x}`：{"1 → +1" if x else "0 → -1"}，`r[{i}]` → =={r[i]}==',
        'c[j] += x * 2 - 1': '同一格也计入列：`c[{j}]` → =={c[j]}==',
        'grid[i][j] = x + y': '`diff[{i}][{j}] = r[{i}] + c[{j}] = {x} + {y}` = =={x+y}==（直接写回 grid）',
        'return grid': '`grid` 已被改写成差值矩阵：`{grid}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='把 0 当成 −1：一的个数减零的个数，就是一次求和',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['二进制矩阵 `grid`，`diff[i][j] = 行 i 的一数 + 列 j 的一数 − 行 i 的零数 − 列 j 的零数`',
                 '返回差值矩阵 `diff`',
                 '示例：`[[0,1,1],[1,0,1],[0,0,1]]` → `[[0,0,4],[0,0,4],[-2,-2,2]]`'],
        quote='优化 1：由于行和列都可以看成是 1 的个数减去 0 的个数，所以统计的时候，可以把 0 当成 -1。优化 2：答案可以直接填到 grid 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`onesRow − zerosRow` 就是整行 “1 记 +1、0 记 −1” 的和，用 `x*2-1` 一步得到',
              '所以 `diff[i][j] = r[i] + c[j]`，只要两个数组',
              '答案直接写回 `grid`，不再开 `m × n` 的新矩阵'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`',
                 '`x * 2 - 1`：1 → 1，0 → −1',
                 '易错：写回 `grid` 之前必须先统计完整个矩阵，所以是两轮循环',
                 '题目保证 `m*n ≤ 1e5`，行或列可能很长'],
    ),
)
