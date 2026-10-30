_GONE = (92, 99, 110)  # 已排除：灰色


def _color(S, r, c, v):
    if 'i' not in S:
        return None
    if v == S['target'] and r == S['i'] and c == S['j']:
        return 'green'
    if r < S['i'] or c > S['j']:
        return _GONE
    return None


def _info(S):
    if 'i' not in S:
        return '每行从左到右升序，每列从上到下升序；==灰色==表示已排除'
    i, j, M, t = S['i'], S['j'], S['matrix'], S['target']
    if not (i < len(M) and j >= 0):
        return '行列全部排除'
    v = M[i][j]
    rel = '等于' if v == t else ('<' if v < t else '>')
    return f'当前右上角 `matrix[{i}][{j}] = {v}` {rel} `target = {t}`'


def _cap_lt(S, B, ret):
    i, j = S['i'], S['j']
    v, t = S['matrix'][i][j], S['target']
    if v < t:
        return f'`{v} < {t}`：{v} 是这一行剩余元素里==最大==的 → ==这一行全都小于 target==，整行排除'
    return f'`{v} > {t}`：{v} 是这一列剩余元素里==最小==的 → ==这一列全都大于 target==，整列排除'


CONFIG = dict(
    num=240, title='搜索二维矩阵 II', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='排除法 · 从右上角出发',
    code='''
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
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
    call='Solution().searchMatrix([[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24]], 13)',
    expect=True,
    views=[
        dict(type='text', h=56, size=27, fn=_info),
        dict(type='grid', var='matrix', cell=108, h=520, color=_color,
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('target', 'target', 'green')],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列，要找 `target = {target}`',
        'i, j = 0, n - 1': '从==右上角== `(0, {j})` 开始：它是第 0 行最大的、第 {j} 列最小的，==处在中间值==',
        'while i < m and j >= 0': lambda S, B, ret: ('还有剩余元素 → 继续' if S['i'] < S['m'] and S['j'] >= 0 else '没有剩余元素了 → 退出循环'),
        'if matrix[i][j] == target': lambda S, B, ret: (f'`matrix[{S["i"]}][{S["j"]}] == {S["target"]}` → ==找到了==' if S['matrix'][S['i']][S['j']] == S['target']
                                                        else f'`matrix[{S["i"]}][{S["j"]}] = {S["matrix"][S["i"]][S["j"]]}` ≠ `{S["target"]}`'),
        'if matrix[i][j] < target': _cap_lt,
        'i += 1': '排除第 `{B.i}` 行：`i` → `{i}`，新的右上角是 `matrix[{i}][{j}] = {matrix[i][j]}`',
        'j -= 1': '排除第 `{B.j}` 列：`j` → `{j}`，新的右上角是 `matrix[{i}][{j}] = {matrix[i][j]}`',
        'return True': '返回 `True`',
        'return False': '行列都排除完了，返回 `False`',
    },
    max_steps=60,
    cards=dict(
        one_liner='站在右上角，每比较一次就排除一整行或一整列',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['`m × n` 矩阵：==每行从左到右升序，每列从上到下升序==',
                 '判断 `target` 是否在矩阵中',
                 '例：动画里的 4×5 矩阵，`target = 13` → `true`'],
        quote='矩阵的四个角是最特殊的，左上角的值最小，右下角的值最大，另两个角的值居中。对于有序数据，从右上角或者左下角这种中间值开始，可以帮助我们排除不含答案的行列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['右上角：同行剩余元素中==最大==，同列剩余元素中==最小==',
              '比 target 小 → 这一行剩下的都更小，`i += 1`',
              '比 target 大 → 这一列剩下的都更大，`j -= 1`',
              '==O(1) 时间换来 O(m) 或 O(n) 的信息==，所以比暴力 `O(mn)` 快'],
        summary=['时间 `O(m+n)`：最多排除 `m+n-1` 行列；空间 `O(1)`',
                 '易错：从左上角或右下角出发不行——往两个方向走都变大（或都变小），没法排除',
                 '注意：逐行二分是 `O(m log n)`，灵神给了一组数据让“更快”的二分反而退化',
                 '从左下角出发也可以，方法对称；同类题：1351. 统计有序矩阵中的负数'],
    ),
)
