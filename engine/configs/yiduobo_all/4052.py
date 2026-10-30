G = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
RS = [1, 2, 0]
CS = [2, 2, 1]


def _txt(S):
    ln = S.get('_line')
    if ln in (4, 5, 6) and 'k' in S and 'index' in S:
        return f"第 `{S['index']}` 行向左移 `{S['k']}` 位：后缀 `[{S['k']}:]` 接上前缀 `[:{S['k']}]`"
    if ln in (8, 9, 10, 11, 12) and 'k' in S and 'index' in S:
        return f"第 `{S['index']}` 列向上移 `{S['k']}` 位：取出 `col`，后缀拼前缀，再写回"
    return '先把每一行左移，再把每一列上移'


def _color(S, r, c, v):
    ln = S.get('_line')
    idx = S.get('index')
    if idx is None:
        return None
    if ln in (4, 5, 6) and r == idx:
        return 'blue'
    if ln in (8, 9, 10, 11, 12) and c == idx:
        return 'blue'
    return None


CONFIG = dict(
    num=4052, title='行列循环移位', difficulty='Easy', category='模拟',
    author='yiduobo', technique='按题意模拟（后缀拼前缀）',
    code='''
class Solution(object):
    def cyclicShift(self, n, grid, rowShift, colShift):
        
        for index, k in enumerate(rowShift):
            new_row = grid[index][k:] + grid[index][:k]
            grid[index] = new_row[:]
        
        for index, k in enumerate(colShift):
            col = [grid[r][index] for r in range(n)]
            new_col = col[k:] + col[:k]
            for r in range(n):
                grid[r][index] = new_col[r]
        
        return grid
''',
    call=f'Solution().cyclicShift(3, {G}, {RS}, {CS})',
    expect=[[7, 8, 5], [2, 3, 9], [6, 4, 1]],
    views=[
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='grid', var='grid', label='grid（蓝色 = 正在移位的行 / 列）', cell=96, h=330, color=_color),
        dict(type='array', var=lambda S: S.get('new_col') if S.get('_line') in (10, 11, 12) else (S.get('new_row') if S.get('_line') in (5, 6) else None),
             label='移位后的这一行 / 这一列', cell=84, h=150),
    ],
    watch=[('index', 'index', 'blue'), ('k', 'k', 'orange'), ('r', 'r', 'pink')],
    skip=['for r in range(n):', 'col = [grid'],
    max_steps=60,
    captions={
        'for index, k in enumerate(rowShift)': lambda S, B, ret: (f'第 `{S.index}` 行要向左移 `{S.k}` 位' if 'index' in S and ('index' not in B or S.index != B.index or S.get('_line') != B.get('_line')) and 'new_col' not in S else '行移位全部做完，接着处理列'),
        'new_row = grid': '`grid[{index}][{k}:] + grid[{index}][:{k}]`：后缀接前缀 → `{new_row}`',
        'grid[index] = new_row': '把移好的行写回：`grid[{index}] = {grid[index]}`',
        'for index, k in enumerate(colShift)': lambda S, B, ret: (f'第 `{S.index}` 列要向上移 `{S.k}` 位' if 'new_col' not in B or S.index != B.index else '列移位全部做完'),
        'new_col = col[k:]': '先把这一列取成 `col = {col}`，后缀接前缀 → `{new_col}`',
        'grid[r][index] = new_col[r]': '把 `new_col` 逐个写回第 `{index}` 列：`grid[{r}][{index}] = {new_col[r]}`',
        'return grid': '行、列都移完，返回 `grid`',
    },
    cards=dict(
        one_liner='先逐行左移，再逐列上移：后缀拼前缀',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n × n` 的 `grid`，`rowShift[i]` 是第 `i` 行向左循环移位的位数',
                 '`colShift[j]` 是第 `j` 列向上循环移位的位数；先移行，再移列',
                 '本视频：`rowShift=[1,2,0]`，`colShift=[2,2,1]` → `[[7,8,5],[2,3,9],[6,4,1]]`'],
        quote='直接按照题目要求，先枚举每一行，执行左移操作，然后枚举每一列，执行上移操作即可。在具体实现上，可以直接用后缀拼前缀的方式来达成移位的目标。',
        quote_src='—— yiduobo 题解',
        idea=['行是列表，左移 `k` 位就是 `row[k:] + row[:k]`',
              '列不连续，先用推导式取成 `col`，同样后缀拼前缀，再逐个写回',
              '题目要求先行后列，顺序不能换'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错点：列要先取出再写回；顺序必须先行后列',
                 '`new_row[:]` 是复制一份再赋值，这里直接赋值也可以',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
