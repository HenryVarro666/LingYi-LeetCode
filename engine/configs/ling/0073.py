def _cap_if1(S, B, ret):
    i, j = S['i'], S['j']
    v = B['matrix'][i][j]
    if v == 0:
        return f'`matrix[{i}][{j}] == 0` → ==第 {i} 行、第 {j} 列都要清零==，去第 0 行/第 0 列做标记'
    return f'`matrix[{i}][{j}] = {v}`，不是 0，跳过'


def _cap_mark(S, B, ret):
    i, j = S['i'], S['j']
    if j == 0:
        return (f'`matrix[{i}][0] = 0` 记“第 {i} 行有 0”；`matrix[0][0] = 0` 记“==第 0 列有 0==”'
                f'（写法三让 `matrix[0][0]` 兼任第 0 列的标记）')
    return f'记标记：`matrix[{i}][0] = 0` ← 第 {i} 行有 0；`matrix[0][{j}] = 0` ← ==第 {j} 列有 0=='


def _cap_rev(S, B, ret):
    if B.get('j') == 0 and S['j'] == 0:
        return '本行倒着扫完了'
    j = S['j']
    if j == S['n'] - 1:
        return f'第二遍，第 {S["i"]} 行：==倒着==从 `j = {j}` 开始，让第 0 列最后才被修改'
    return f'倒着走：`j = {j}`'


def _cap_check(S, B, ret):
    i, j = S['i'], S['j']
    r, c = B['matrix'][i][0], B['matrix'][0][j]
    ok = r == 0 or c == 0
    who = []
    if r == 0:
        who.append(f'第 {i} 行有 0')
    if c == 0:
        who.append(f'第 {j} 列有 0')
    if j == 0:
        head = f'查标记：`matrix[{i}][0] = {r}`，`matrix[0][0] = {c}`（第 0 列的标记）'
    else:
        head = f'查标记：行标记 `matrix[{i}][0] = {r}`，列标记 `matrix[0][{j}] = {c}`'
    return head + (f' → =={"、".join(who)}==，要清零' if ok else ' → 都不是 0，保留')


def _cap_zero(S, B, ret):
    i, j = S['i'], S['j']
    if j == 0:
        if B['matrix'][i][0] == 0:
            return f'`matrix[{i}][0] = 0`（它本来就是 0），第 {i} 行处理完'
        return (f'`matrix[{i}][0] = 0`：它是本行==最后==被改的格子。'
                f'若正着扫先改它，本行后面的格子会==全被误清==')
    return f'`matrix[{i}][{j}] = 0`'


def _cap_first_row(S, B, ret):
    if S['first_row_has_zero']:
        return '第一行原本就有 0 → 整行清零'
    return '第一行原本没有 0 → 它里面的 0 全是列标记，==恰好就是最终答案==，不用再改'


def _flag_line(S):
    if 'i' not in S or 'j' not in S:
        return '第 0 列 `matrix[i][0]` 记“第 i 行有 0”，第 0 行 `matrix[0][j]` 记“第 j 列有 0”'
    M, i, j = S['matrix'], S['i'], S['j']
    return f'青框 行标记 `matrix[{i}][0] = {M[i][0]}`　　紫框 列标记 `matrix[0][{j}] = {M[0][j]}`'


def _cell_color(S, i, j, v):
    if v != 0:
        return None
    return 'orange' if (i == 0 or j == 0) else 'red'


CONFIG = dict(
    num=73, title='矩阵置零', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='第一行/第一列当标记 · O(1) 空间',
    code='''
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        first_row_has_zero = 0 in matrix[0]

        for i in range(1, m):
            for j in range(n):
                if matrix[i][j] == 0:
                    matrix[i][0] = matrix[0][j] = 0

        for i in range(1, m):
            # 倒着遍历，避免提前把 matrix[i][0] 改成 0，误认为这一行要全部变成 0
            for j in range(n - 1, -1, -1):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if first_row_has_zero:
            for j in range(n):
                matrix[0][j] = 0
''',
    call='''
mat = [[1, 2, 3, 4], [5, 6, 7, 8], [0, 9, 0, 1]]
Solution().setZeroes(mat)
mat
''',
    expect=[[0, 2, 0, 4], [0, 6, 0, 8], [0, 0, 0, 0]],
    views=[
        dict(type='text', h=56, size=26, text='==橙色==是标记：第 0 列记“哪行有 0”，第 0 行记“哪列有 0”；红色是普通的 0'),
        dict(type='grid', var='matrix', cell=125, h=470, color=_cell_color,
             cursors=[('i', '0', 'cyan'), ('0', 'j', 'purple'), ('i', 'j', 'yellow')]),
        dict(type='text', h=60, size=28, fn=_flag_line),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'first_row_has_zero'],
    skip=['for j in range(n):'],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'first_row_has_zero = 0 in': '第一行等会儿要当“列标记”，会被改写 → ==先记下它原本有没有 0==：`{first_row_has_zero}`',
        6: lambda S, B, ret: ('第一遍扫完，标记都记好了' if B.get('i') == S['i'] == S['m'] - 1
                              else f'第一遍：扫第 `{S["i"]}` 行（第 0 行本身就是标记行，从 1 开始），每行连第 0 列一起扫'),
        'if matrix[i][j] == 0': _cap_if1,
        'matrix[i][0] = matrix[0][j] = 0': _cap_mark,
        11: lambda S, B, ret: ('第二遍结束' if B.get('i') == S['i'] == S['m'] - 1 and B.get('j') == 0
                               else f'第二遍：按标记给第 `{S["i"]}` 行清零'),
        'for j in range(n - 1': _cap_rev,
        'if matrix[i][0] == 0 or': _cap_check,
        'matrix[i][j] = 0': _cap_zero,
        'if first_row_has_zero': _cap_first_row,
        'matrix[0][j] = 0': '`matrix[0][{j}] = 0`',
    },
    max_steps=70,
    cards=dict(
        one_liner='把第 0 行、第 0 列当“记事本”，记下哪些行列要清零',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m × n` 矩阵里某个元素是 0，就把它==所在的整行和整列==都设为 0',
                 '要求==原地==修改；进阶：只用常量额外空间',
                 '示例：`[[1,2,3,4],[5,6,7,8],[0,9,0,1]]`',
                 '→ `[[0,2,0,4],[0,6,0,8],[0,0,0,0]]`'],
        before=[dict(heading='一步步优化', lines=[
            '规则：`i` 行有 0 ==或== `j` 列有 0，`matrix[i][j]` 就变成 0',
            '方法一：数组 `row_has_zero`、`col_has_zero` 记录，空间 `O(m+n)`',
            '方法二：把这两个数组==搬进矩阵的第 0 列和第 0 行==，空间 `O(1)`',
            '写法三：`matrix[0][0]` 兼任“第 0 列有 0”，第二遍倒着扫']),
        ],
        quote='回想一下 Excel 表格，通常用第一行和第一列保存汇总信息。对于本题，能否把数据保存到 matrix 的第一行和第一列中呢？',
        quote_src='—— 灵茶山艾府题解',
        idea=['不能发现 0 就立刻清整行整列：==新写的 0 会被误当成原来的 0==',
              '第一行会被标记覆盖 → 一开始先用 `first_row_has_zero` 记下原状',
              '第二遍==倒着==扫每一行：`matrix[i][0]` 最后才改，不会提前把整行“误判”成要清零'],
        summary=['时间 `O(mn)`，空间 `O(1)`（只多一个布尔变量）',
                 '易错：发现 0 就立刻清行清列 → 连锁误判（示例 1 会把最右列也清掉）',
                 '易错：第二遍若正着扫，`matrix[i][0]` 先变 0，后面整行都被误清',
                 '第一行最后单独处理；写法一/二改用变量或“先改第一列再改第一行”，道理相同'],
    ),
)
