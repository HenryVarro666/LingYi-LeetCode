_ANS = [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]


def _done(S):
    return 'i' not in S or S['matrix'][S['i']] == _ANS[S['i']]


def _color(S, i, j, v):
    if S['matrix'][i] == _ANS[i]:
        return 'green'
    if i == j:
        return 'purple'
    return None


def _cap_row(S, B, ret):
    if B.get('i') == S['i']:
        return '所有行处理完，旋转完成'
    i = S['i']
    if i == S['n'] - 1:
        return f'第 `{i}` 行：对角线上方已经没有元素，只需翻转'
    return f'第 `{i}` 行：先和第 `{i}` 列交换（转置），再翻转这一行'


def _cap_swap(S, B, ret):
    i, j = S['i'], S['j']
    a, b = B['row'][j], B['matrix'][j][i]
    return f'转置：交换 `matrix[{i}][{j}]` ↔ `matrix[{j}][{i}]`（关于主对角线对称）：`{a}` ↔ `{b}`'


def _cap_rev(S, B, ret):
    i = S['i']
    return (f'第 `{i}` 行已转置完 → ==马上行翻转==：`{B["row"]}` → `{S["row"]}`。'
            f'后面的循环不会再碰这一行，所以可以提前翻')


CONFIG = dict(
    num=48, title='旋转图像', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='转置 + 行翻转（合并成一个循环）',
    code='''
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i, row in enumerate(matrix):
            for j in range(i + 1, n):  # 遍历对角线上方元素，做转置
                row[j], matrix[j][i] = matrix[j][i], row[j]
            row.reverse()  # 行翻转
''',
    call='''
mat = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
Solution().rotate(mat)
mat
''',
    expect=_ANS,
    views=[
        dict(type='text', h=56, size=28, text='`(i, j)` ==转置==→ `(j, i)` ==行翻转==→ `(j, n−1−i)`　即顺时针转 90°'),
        dict(type='grid', var='matrix', cell=112, h=560, color=_color,
             cursors=[(lambda S: None if _done(S) else S.get('j'), 'i', 'pink'), (lambda S: None if _done(S) or 'j' not in S else S['i'], 'j', 'yellow')]),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('row', 'row')],
    skip=['for j in range(i + 1, n)'],
    captions={
        'n = len': '`n = {n}`：紫色是主对角线（转置的对称轴），绿色是已经转好的行',
        'for i, row in enumerate': _cap_row,
        'row[j], matrix[j][i] =': _cap_swap,
        'row.reverse()': _cap_rev,
    },
    max_steps=60,
    cards=dict(
        one_liner='两次翻转等于一次旋转：先转置，再把每一行翻转',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['把 `n × n` 的矩阵==原地==顺时针旋转 90°，不能另开矩阵',
                 '例：4×4 矩阵按行填 `1..16`',
                 '转完后第一行是 `[13,9,5,1]`：原来的第一列倒过来'],
        before=[dict(heading='(i, j) 去哪了？', lines=[
            '竖着看：第 `j` 列的元素去到第 `j` 行',
            '横着看：第 `i` 行的元素去到第 `n−1−i` 列',
            '所以 `(i, j) → (j, n−1−i)`']),
        ],
        quote='(i,j) → (j,n−1−i) 可以通过两次翻转操作得到：(i,j) 转置→ (j,i) 行翻转→ (j,n−1−i)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['转置：按主对角线翻转，`(i, j)` 去到 `(j, i)`',
              '行翻转：每一行左右翻转，`(j, i)` 去到 `(j, n−1−i)`',
              '写法二把两步合成一个循环：遍历==对角线上方==，每行转置完就直接翻转'],
        summary=['时间 `O(n²)`，空间 `O(1)`，全程原地',
                 '为什么能合并：第 `i` 行转置完后，后面只会碰第 `i+1` 行之后的元素',
                 '易错：转置时只交换对角线一侧，两侧都换会换回原样',
                 '写法一：先整体转置，再 `for row in matrix: row.reverse()`',
                 '思考：转 180° = 上下翻 + 左右翻；逆时针 90° = 转置 + 上下翻'],
    ),
)
