def _late(S):
    # 步骤 2 做完后（本例第 2 行已全部置 0）进入“处理第 0 行/第 0 列”阶段，此时循环变量 i 指的是列号，不画格子光标
    return S['matrix'][2][1:] == [0, 0, 0]


def _ci(S):
    return None if ('i' not in S or _late(S)) else S['i']


def _cap_col0(S, B, ret):
    i = S['i']
    v = B['matrix'][i][0]
    if v == 0:
        return f'`matrix[{i}][0] == 0`（青框）→ ==第 0 列要置 0==：记在 `first_column`，不占用 `matrix[0][0]`'
    return f'先看第 0 列：`matrix[{i}][0] = {v}`（青框），不是 0'


def _cap_if1(S, B, ret):
    i, j = S['i'], S['j']
    v = B['matrix'][i][j]
    if v == 0:
        return f'`matrix[{i}][{j}] == 0` → 第 {i} 行、第 {j} 列都要置 0，把这两件事==记到第 0 个元素上=='
    return f'`matrix[{i}][{j}] = {v}`，不是 0'


def _cap_row_mark(S, B, ret):
    i = S['i']
    if i == 0:
        return '`matrix[0][0] = 0`：按约定，==它表示“第 0 行要置 0”==（第 0 列另有 `first_column`）'
    return f'`matrix[{i}][0] = 0`：第 {i} 行要置 0'


def _cap_check(S, B, ret):
    i, j = S['i'], S['j']
    r, c = B['matrix'][i][0], B['matrix'][0][j]
    who = ([f'第 {i} 行要置 0'] if r == 0 else []) + ([f'第 {j} 列要置 0'] if c == 0 else [])
    head = f'查标记：`matrix[{i}][0] = {r}`，`matrix[0][{j}] = {c}`'
    return head + (f' → =={"、".join(who)}==' if who else ' → 都不是 0，保留')


def _status(S):
    if 'matrix' not in S or 'first_column' not in S:
        return '约定：`matrix[0][0]` 管==第 0 行==，变量 `first_column` 管==第 0 列=='
    r0 = '要清零' if S['matrix'][0][0] == 0 else '不清零'
    c0 = '要清零' if S['first_column'] else '不清零'
    return f'第 0 行：`matrix[0][0]` → =={r0}==　　第 0 列：`first_column` → =={c0}=='


def _cell_color(S, i, j, v):
    if v != 0:
        return None
    return 'purple' if (i == 0 or j == 0) else 'red'


CONFIG = dict(
    num=73, title='矩阵置零', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='第 0 行/列做标记 + first_column',
    code='''
class Solution(object):
    def setZeroes(self, matrix):
        m = len(matrix)
        n = len(matrix[0])

        first_column = False
        for i in range(m):
            if matrix[i][0] == 0:
                first_column = True
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if matrix[0][0] == 0:
            for i in range(n):
                matrix[0][i] = 0
        if first_column:
            for i in range(m):
                matrix[i][0] = 0

        return matrix
''',
    call='Solution().setZeroes([[1, 2, 0, 4], [5, 6, 7, 8], [0, 9, 1, 1]])',
    expect=[[0, 0, 0, 0], [0, 6, 0, 8], [0, 0, 0, 0]],
    views=[
        dict(type='text', h=56, size=26, text='==紫色==是第 0 行/第 0 列里的标记 0，红色是其他 0；==青框==是本行的行标记'),
        dict(type='grid', var='matrix', cell=125, h=470, color=_cell_color,
             cursors=[(_ci, '0', 'cyan'), (_ci, 'j', 'yellow')]),
        dict(type='text', h=60, size=28, fn=_status),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('first_column', 'first_column', 'purple')],
    skip=['for j in range(1, n)', 'for i in range(n)', '            for i in range(m)'],
    captions={
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列',
        'first_column = False': '`first_column`：第 0 列要不要置 0 的==单独标记==（`matrix[0][0]` 留给第 0 行）',
        7: lambda S, B, ret: ('步骤 1 扫完' if B.get('i') == S['i'] == S['m'] - 1
                              else f'步骤 1：扫第 `{S["i"]}` 行' + ('（==第 0 行也要扫==，它的 0 也得记下来）' if S['i'] == 0 else '')),
        8: _cap_col0,
        'first_column = True': '`first_column = True`：等到最后再把第 0 列整列置 0',
        'if matrix[i][j] == 0': _cap_if1,
        12: _cap_row_mark,
        'matrix[0][j] = 0': '`matrix[0][{j}] = 0`：第 {j} 列要置 0',
        'for i in range(1, m)': lambda S, B, ret: ('步骤 2 结束' if B.get('i') == S['i'] == S['m'] - 1 and B.get('j') == S['n'] - 1
                                                   else f'步骤 2：按标记处理第 `{S["i"]}` 行（第 0 行、第 0 列先不动，它们还是标记）'),
        'if matrix[i][0] == 0 or': _cap_check,
        'matrix[i][j] = 0': '`matrix[{i}][{j}] = 0`',
        'if matrix[0][0] == 0': lambda S, B, ret: ('`matrix[0][0] == 0` → 按约定是==第 0 行要置 0== → 整行清零' if B['matrix'][0][0] == 0
                                                   else '`matrix[0][0]` 不是 0 → 第 0 行不用置 0'),
        'matrix[0][i] = 0': '`matrix[0][{i}] = 0`',
        'if first_column': lambda S, B, ret: ('`first_column = True` → 第 0 列整列置 0。==必须排在第 0 行之后==：先改第 0 列会把 `matrix[0][0]` 变 0，误清第 0 行'
                                              if S['first_column'] else '`first_column = False`，第 0 列不动'),
        'matrix[i][0] = 0': '`matrix[{i}][0] = 0`',
        'return matrix': '返回 `matrix`（题目只要求原地修改，这个 `return` 可有可无）',
    },
    max_steps=70,
    cards=dict(
        one_liner='第 0 行、第 0 列当标记；`matrix[0][0]` 一格记不下两件事，就再加一个变量',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m × n` 矩阵里某个元素是 0，就把它==所在的整行和整列==都设为 0',
                 '要求==原地==修改，最好只用常数额外空间',
                 '示例：`[[1,2,0,4],[5,6,7,8],[0,9,1,1]]`',
                 '→ `[[0,0,0,0],[0,6,0,8],[0,0,0,0]]`'],
        quote='若matrix[0][0]为0，无法确定是第0行需要置0，还是第0列需要置0。于是我添加了一个标记，表示第0列是否需要置0，matrix[0][0]则用来表示第0行是否需要置0。',
        quote_src='—— yiduobo 题解',
        idea=['步骤 1：扫描矩阵，把 0 所在行、列的==第 0 个元素==置 0',
              '步骤 2：扫第 0 行、第 0 列，把标记为 0 的列、行全部置 0',
              '`matrix[0][0]` 管不了两件事 → 只管第 0 行，第 0 列交给 `first_column`'],
        summary=['时间 `O(mn)`，空间 `O(1)`（只多一个布尔变量）',
                 '步骤 1 中第 0 列单独判断，`j` 从 1 开始，不会误写 `matrix[0][0]`',
                 '易错：收尾时==先处理第 0 行，再处理第 0 列==，顺序反了会误清第 0 行',
                 '只删去了 `"""type ..."""` 文档字符串，其余照搬（兼容 Python 3）'],
    ),
)
