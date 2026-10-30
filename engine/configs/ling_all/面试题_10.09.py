M = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24]]


def _txt(S):
    if 'j' not in S or 'i' not in S:
        return ''
    i, j = S['i'], S['j']
    m = len(S['matrix'])
    if i >= m or j < 0:
        return '剩余区域为空 → 没找到'
    v, t = S['matrix'][i][j], S['target']
    rel = '==等于==' if v == t else ('小于' if v < t else '大于')
    return f'右上角 `matrix[{i}][{j}] = {v}` {rel} `target = {t}`；剩余区域：第 {i}~{m - 1} 行 × 第 0~{j} 列'


CONFIG = dict(
    num='面试题 10.09', title='排序矩阵查找', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='右上角出发 · 排除一行或一列',
    code='''
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix:
            return False
        m, n = len(matrix), len(matrix[0])
        i, j = 0, n - 1  # 从右上角开始
        while i < m and j >= 0:  # 还有剩余元素
            if matrix[i][j] == target:
                return True  # 找到 target
            if matrix[i][j] < target:
                i += 1  # 这一行剩余元素全部小于 target，排除
            else:
                j -= 1  # 这一列剩余元素全部大于 target，排除
        return False
''',
    call=f'Solution().searchMatrix({M!r}, 13)',
    expect=True,
    views=[
        dict(type='grid', var='matrix', label='matrix（黄框 = 当前右上角；青色 = 剩余区域，无色 = 已排除）', cell=96, h=400,
             cursors=[('i', 'j', 'yellow')],
             color=lambda S, r, c, v: ('green' if ('target' in S and v == S['target']) else
                                       'cyan' if ('i' in S and 'j' in S and r >= S['i'] and c <= S['j']) else None)),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('target', 'target', 'green')],
    skip=['m, n = len'],
    captions={
        'if not matrix': '空矩阵直接返回 `False`',
        'i, j = 0, n - 1': '从==右上角== `({i}, {j})` 开始：它是所在行最大、所在列最小',
        'while i < m': lambda S, B, r: (f'剩余区域是第 `{B.i}`~`{B.m - 1}` 行 × 第 `0`~`{B.j}` 列，还有元素，继续'
                                        if B.i < B.m and B.j >= 0 else f'`i = {B.i}`、`j = {B.j}` 越界：剩余元素为空'),
        'if matrix[i][j] == target': '`matrix[{i}][{j}] = {matrix[i][j]}` 和 `target = {target}` 比：{"相等" if matrix[i][j] == target else "不相等"}',
        'return True': '找到 `target`，返回 `True`',
        'if matrix[i][j] < target': '`{matrix[i][j]} < {target}`？{"是" if matrix[i][j] < target else "否"}：{"这一行里它已是最大，其余都更小" if matrix[i][j] < target else "这一列里它已是最小，其余都更大"}',
        'i += 1': '这一行剩余元素全部小于 `target` → ==排除整行==，`i` 下移到 {i}',
        'j -= 1': '这一列剩余元素全部大于 `target` → ==排除整列==，`j` 左移到 {j}',
        'return False': '区域排空仍没找到，返回 `False`',
    },
    cards=dict(
        one_liner='右上角是一行最大、一列最小：每次比较排除一整行或一整列',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['`m × n` 矩阵，每行每列都升序，判断 `target` 是否存在',
                 '示例：`target = 5` 返回 `true`，`target = 20` 返回 `false`',
                 '本视频：4×5 矩阵，`target = 13` → `True`'],
        quote='这一行剩余元素全部小于 target，排除；这一列剩余元素全部大于 target，排除。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['从右上角出发，它比同行其余数都大、比同列其余数都小',
              '它小于 `target`：整行都不可能，`i += 1`；大于 `target`：整列都不可能，`j -= 1`',
              '剩余区域不断缩小，最多走 `m + n` 步'],
        summary=['时间 `O(m+n)`，空间 `O(1)`',
                 '易错：循环条件是 `i < m and j >= 0`，两个下标都要判界',
                 '也可以从左下角开始，方法类似（左上、右下角不行：无法判断往哪走）',
                 '先判空矩阵，再取 `len(matrix[0])`'],
    ),
)
