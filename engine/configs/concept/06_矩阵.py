GRAY = (64, 70, 80)


def _grid_color(S, i, j, v):
    if 'target' in S and 'i' in S:             # 240：被排除的行列变灰
        if i < S['i'] or j > S['j']:
            return GRAY
        if (i, j) == (S['i'], S['j']) and v == S['target']:
            return 'green'
        return None
    if 'n' in S:                               # 48：按原来的行上色，看它们去哪
        return ['blue', 'pink', 'green'][(v - 1) // 3]
    return None


def _formula(S):
    if 'target' in S and 'i' in S:
        i, j, t = S['i'], S['j'], S['target']
        if not (i < len(S['matrix']) and j >= 0):
            return '没有剩余元素'
        v = S['matrix'][i][j]
        if v == t:
            return f'`matrix[{i}][{j}] = {v}` ==等于== target {t}'
        if v < t:
            return f'`matrix[{i}][{j}] = {v}` < {t}：这一行左边都更小 → ==排除第 {i} 行=='
        return f'`matrix[{i}][{j}] = {v}` > {t}：这一列下面都更大 → ==排除第 {j} 列=='
    if 'target' in S:
        return '模板① 排除法：从右上角出发（行里最大、列里最小）'
    if 'row' in S:
        return '② 每一行翻转：`(j, i) → (j, n-1-i)`'
    if 'n' in S:
        return '① 转置：沿主对角线交换 `(i, j) ↔ (j, i)`'
    return ''


def _t(S):
    return 'n' in S and 'row' not in S and 'i' in S and 'j' in S


_seen = set()


def _for_j(S, B, ret):
    if 'j' not in S or S.i == 0:
        return f'第 `{S.i}` 行在对角线左下没有格子，跳过'
    key = (S.i, S.j)
    if key in _seen:
        return f'第 `{S.i}` 行左下部分换完'
    _seen.add(key)
    return f'`j = {S.j}`：准备交换 `({S.i},{S.j})` 和 `({S.j},{S.i})`'


CONFIG = dict(
    num=None, title='矩阵 · 通用思想与模板', author='概念讲解', category='矩阵',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def search_matrix(matrix, target):     # 240. 排除法
    i, j = 0, len(matrix[0]) - 1       # 从右上角出发
    while i < len(matrix) and j >= 0:  # 还有剩余元素
        if matrix[i][j] == target:
            return True
        if matrix[i][j] < target:
            i += 1                     # 这一行剩下的都更小
        else:
            j -= 1                     # 这一列剩下的都更大
    return False

def rotate(matrix):                    # 48. 两次翻转 = 一次旋转
    n = len(matrix)
    for i in range(n):                 # ① 转置
        for j in range(i):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:                 # ② 每行翻转
        row.reverse()
    return matrix
''',
    call='''
a = search_matrix([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 13)
b = rotate([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
(a, b)
''',
    expect=(True, [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var='matrix', label='matrix', color=_grid_color, cell=96,
             cursors=[(lambda S: S['i'] if 'target' in S or _t(S) else None,
                       lambda S: S['j'] if 'target' in S or _t(S) else None, 'yellow', '(i,j)'),
                      (lambda S: S['j'] if _t(S) else None, lambda S: S['i'] if _t(S) else None, 'pink', '(j,i)')],
             h=470),
        dict(type='text', fn=lambda S: ('灰色 = 已排除：==每一步删掉一整行或一整列== → 最多 `m + n` 步' if 'target' in S else
                                        ('颜色 = 原来的行：第 0 行（蓝）最后到了 ==最后一列==' if 'n' in S else '')),
             size=26, h=60),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'target', 'n', ('row', 'row')],
    captions={
        'i, j = 0, len': '模板①：从右上角 `({i}, {j})` 出发——它是这一行最大、这一列最小',
        'while i < len': lambda S, B, ret: (f'`({S.i}, {S.j})` 还在矩阵里，继续' if S.i < len(S.matrix) and S.j >= 0
                                            else '出界：所有行列都排除了'),
        'if matrix[i][j] == target': lambda S, B, ret: (
            f'`matrix[{S.i}][{S.j}] = {S.matrix[S.i][S.j]}` == {S.target} → ==找到==' if S.matrix[S.i][S.j] == S.target
            else f'`matrix[{S.i}][{S.j}] = {S.matrix[S.i][S.j]}` ≠ {S.target}'),
        'return True': '找到 target，返回 `True`：只看了 ==m + n 级别== 个格子',
        'if matrix[i][j] < target': lambda S, B, ret: (
            f'`{S.matrix[S.i][S.j]} < {S.target}`：它是这一行（剩余部分）的最大值，整行都太小'
            if S.matrix[S.i][S.j] < S.target else
            f'`{S.matrix[S.i][S.j]} > {S.target}`：它是这一列（剩余部分）的最小值，整列都太大'),
        'i += 1': '排除第 `{i - 1}` 行，`i` → {i}：花 `O(1)` 就丢掉了 ==一整行== 的信息',
        'j -= 1': '排除第 `{j + 1}` 列，`j` → {j}：花 `O(1)` 就丢掉了 ==一整列== 的信息',
        'n = len': '模板② 旋转 90°：`(i, j)` 要去 `(j, n-1-i)`，==拆成两次翻转==',
        'for i in range(n)': lambda S, B, ret: (f'转置第 `{S.i}` 行：只交换对角线左下的格子' if B.get('i') != S.i
                                                else '转置完成：第 j 列变成了第 j 行'),
        'for j in range(i)': _for_j,
        'matrix[i][j], matrix[j][i]': '交换 `({i},{j})` ↔ `({j},{i})`：`{matrix[i][j]}` 和 `{matrix[j][i]}` 互换位置',
        'for row in matrix': lambda S, B, ret: (f'取一行 `{S.row}` 准备翻转' if B.get('row') != S.row
                                                else '所有行都翻转好了'),
        'row.reverse()': '翻转这一行 → `{row}`',
        'return matrix': '完成顺时针旋转 90°：==原地== 修改，`O(1)` 额外空间',
    },
    cards=dict(
        one_liner='把二维问题拆成坐标变换、方向数组和「每步排除一行 / 一列」',
        complexity='遍历类 `O(mn)`；有序矩阵搜索 `O(m + n)`；空间 `O(1)`',
        problem_heading='什么时候用？',
        problem=['要求原地 / `O(1)` 空间 → 借第一行、第一列当标记（73）',
                 '按圈、按方向走 → 方向数组 `DIRS` + 撞墙右转（54）',
                 '旋转、翻转 → 写出坐标变换，拆成两次翻转（48）',
                 '行和列都有序 → 从右上角出发，每步排除一行或一列（240）'],
        before=[dict(heading='核心概念：坐标变换 & 排除法', lines=[
            '方向数组 `DIRS = (0,1),(1,0),(0,-1),(-1,0)`，`di = (di+1) % 4` 即右转',
            '旋转 90°：`(i,j) → (j,i) → (j,n-1-i)`，即 ==转置 + 每行翻转==',
            '右上角是「行最大、列最小」：比 target 小删行，比 target 大删列',
            '原地标记：第一行 / 第一列当记录本，先单独记下它俩自己有没有 0']),
        ],
        idea_heading='两位作者怎么说',
        quote='利用 matrix 行列有序的性质，我们可以==用 O(1) 的时间获取 O(m) 或 O(n) 的信息==。相比之下，O(mn) 的暴力查找（一个一个地找），每次花费 O(1) 的时间，只获取了 O(1) 的信息。',
        quote_src='—— 灵茶山艾府 · 240. 搜索二维矩阵 II',
        idea=['灵神 48 先推坐标 `(i,j) → (j,n-1-i)`，再拆成 ==转置 + 行翻转==',
              'yiduobo 48 / 54 的统一视角：==从外向内一圈一圈==，四条边轮转或依次输出',
              '240：灵神从右上角、yiduobo 从左下角出发，都是每步排除一行或一列'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`73` 矩阵置零：第一行 / 第一列当标记，先记下它俩自己有没有 0',
                 '`54` 螺旋矩阵：`DIRS` 方向数组，出界或访问过就右转',
                 '`48` 旋转图像：转置 + 每行翻转（或一圈一圈四边轮换）',
                 '`240` 搜索二维矩阵 II：右上角出发，每步排除一行或一列',
                 '易错：73 第一行列要最后处理；54 非方阵会剩单行 / 单列'],
    ),
)
