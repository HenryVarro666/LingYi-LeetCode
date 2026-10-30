G = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
RS = [1, 2, 0]
CS = [2, 2, 1]


def _txt(S):
    if 'row' in S and 'col' in S and 'i' in S and S.get('_line') in (7, 8):
        return (f"`ans[{S['i']}][{S['j']}]` 来自 `grid[{S['row']}][{S['col']}]` = =={S['grid'][S['row']][S['col']]}==")
    if 'row' in S and 'i' in S and S.get('_line') == 6:
        return f"列移位后，第 `{S['row']}` 行的元素来到第 `{S['i']}` 行"
    return '倒推：答案里的每个格子，原来在哪一行哪一列？'


CONFIG = dict(
    num=4052, title='行列循环移位', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='直接计算每个格子的来源',
    code='''
class Solution:
    def cyclicShift(self, n: int, grid: list[list[int]], rowShift: list[int], colShift: list[int]) -> list[list[int]]:
        ans = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                row = (i + colShift[j]) % n
                col = (j + rowShift[row]) % n
                ans[i][j] = grid[row][col]
        return ans
''',
    call=f'Solution().cyclicShift(3, {G}, {RS}, {CS})',
    expect=[[7, 8, 5], [2, 3, 9], [6, 4, 1]],
    views=[
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='grid', var='grid', label='grid（蓝框 = 这个答案格子的来源）', cell=84, h=250,
             cursors=[('row if _line == 8 else None', 'col', 'blue')]),
        dict(type='grid', var='ans', label='ans（黄框 = 正在填的格子）', cell=84, h=250,
             cursors=[('i', 'j', 'yellow')],
             color=lambda S, r, c, v: 'green' if 'i' in S and (r, c) < (S['i'], S['j']) else None),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('row', 'row', 'blue'), ('col', 'col', 'blue')],
    skip=['for j in range'],
    max_steps=60,
    captions={
        'ans = [[0]': '先造一个全 0 的 `{n} × {n}` 答案，不改 `grid`',
        'for i in range(n)': lambda S, B, ret: (f'填答案的第 `{S.i}` 行' if 'i' not in B or S.i != B.i else '所有行都填完了'),
        'row = (i + colShift[j]) % n': '列移位后，第 `{row}` 行的元素来到第 `{i}` 行：`({i} + {colShift[j]}) % {n} = {row}`',
        'col = (j + rowShift[row]) % n': '行移位后，第 `{row}` 行的第 `{col}` 列来到第 `{j}` 列：`({j} + {rowShift[row]}) % {n} = {col}`',
        'ans[i][j] = grid': '`ans[{i}][{j}] = grid[{row}][{col}]` = =={ans[i][j]}==',
        'return ans': '9 个格子都填好，返回 `ans`',
    },
    cards=dict(
        one_liner='倒推：每个答案格子来自哪一行哪一列',
        complexity='时间 `O(n^2)`，空间 `O(1)`（返回值不计）',
        problem=['`n × n` 网格，先按 `rowShift` 把每行向左循环移位，再按 `colShift` 把每列向上循环移位',
                 '返回移位后的网格',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]`，`rowShift=[1,2,0]`，`colShift=[2,2,1]` → `[[7,8,5],[2,3,9],[6,4,1]]`'],
        quote='答案 ans[i][j] 来自哪个格子？来自哪一行？列移位后，row = (i + colShift[j]) mod n 行移到了 i 行。来自哪一列？行移位后，row 行的 col = (j + rowShift[row]) mod n 列移到了 j 列。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['先做行移位、再做列移位：倒着想，先找行、再找列',
              '列移位决定来自哪一行：`row = (i + colShift[j]) % n`',
              '行移位决定来自哪一列：`col = (j + rowShift[row]) % n`'],
        summary=['时间 `O(n^2)`，空间 `O(1)`，不用真的移动任何元素',
                 '易错点：顺序要倒推，先用 `colShift[j]` 定行，再用 `rowShift[row]`（不是 `rowShift[i]`）',
                 '写法一按题意模拟：行用切片拼接，列用 `zip(*grid)` 取出再写回，同样 `O(n^2)`',
                 '原地修改可借助 189. 轮转数组 的技巧'],
    ),
)
