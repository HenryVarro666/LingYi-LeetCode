_GONE = (92, 99, 110)  # 已排除：灰色


def _color(S, r, c, v):
    if 'y' not in S:
        return None
    if v == S['target'] and r == S['x'] and c == S['y']:
        return 'green'
    if r > S['x'] or c < S['y']:
        return _GONE
    return None


def _info(S):
    if 'y' not in S:
        return '每行从左到右升序，每列从上到下升序；==灰色==表示已排除'
    x, y, M, t = S['x'], S['y'], S['matrix'], S['target']
    if not (x >= 0 and y < len(M[0])):
        return '行列全部排除'
    v = M[x][y]
    rel = '等于' if v == t else ('<' if v < t else '>')
    return f'当前左下角 `matrix[{x}][{y}] = {v}` {rel} `target = {t}`'


def _cap_gt(S, B, ret):
    x, y = S['x'], S['y']
    v, t = S['matrix'][x][y], S['target']
    if v > t:
        return (f'`{v} > {t}`：性质 2，以 `({x},{y})` 为左上角的子矩阵里它最小 → '
                f'==第 {x} 行剩下的都比 target 大==，排除这一行')
    return f'`{v} > {t}` 不成立'


CONFIG = dict(
    num=240, title='搜索二维矩阵 II', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='排除法 · 从左下角出发',
    code='''
class Solution(object):
    def searchMatrix(self, matrix, target):
        x = len(matrix) - 1
        y = 0

        while x >= 0 and y < len(matrix[0]):
            if matrix[x][y] == target:
                return True
            elif matrix[x][y] > target:
                x -= 1
            else:
                y += 1

        return False
''',
    call='Solution().searchMatrix([[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24]], 12)',
    expect=True,
    views=[
        dict(type='text', h=56, size=27, fn=_info),
        dict(type='grid', var='matrix', cell=108, h=520, color=_color,
             cursors=[('x', 'y', 'yellow', '(x,y)')]),
    ],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('target', 'target', 'green')],
    captions={
        'x = len(matrix) - 1': '从==左下角==出发：`x = {x}`（最后一行）',
        'y = 0': '`y = 0`（第一列）。左下角是本列最大、本行最小，==两条性质都能用上==',
        'while x >= 0': lambda S, B, ret: ('还有没排除的行和列 → 继续' if S['x'] >= 0 and S['y'] < len(S['matrix'][0]) else '行列都排除完 → 退出'),
        'if matrix[x][y] == target': lambda S, B, ret: (f'`matrix[{S["x"]}][{S["y"]}] == {S["target"]}` → ==找到了==' if S['matrix'][S['x']][S['y']] == S['target']
                                                        else f'`matrix[{S["x"]}][{S["y"]}] = {S["matrix"][S["x"]][S["y"]]}` ≠ `{S["target"]}`'),
        'elif matrix[x][y] > target': lambda S, B, ret: (_cap_gt(S, B, ret) if S['matrix'][S['x']][S['y']] > S['target']
                                                         else f'`{S["matrix"][S["x"]][S["y"]]} < {S["target"]}`：性质 1，以 `({S["x"]},{S["y"]})` 为右下角的子矩阵里它最大 → ==第 {S["y"]} 列剩下的都比 target 小==，排除这一列'),
        'x -= 1': '排除第 `{B.x}` 行：`x` → `{x}`，新的左下角 `matrix[{x}][{y}] = {matrix[x][y]}`',
        'y += 1': '排除第 `{B.y}` 列：`y` → `{y}`，新的左下角 `matrix[{x}][{y}] = {matrix[x][y]}`',
        'return True': '返回 `True`',
        'return False': '返回 `False`',
    },
    max_steps=60,
    cards=dict(
        one_liner='从左下角出发，每次排除最后一行或第一列',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['`m × n` 矩阵：==每行从左到右升序，每列从上到下升序==',
                 '判断 `target` 是否在矩阵中',
                 '例：动画里的 4×5 矩阵，`target = 12` → `true`'],
        before=[dict(heading='先想二分？', lines=[
            '第一反应是行列二分，但这里==不满足“前一行的元素都小于后一行”==',
            '比如找 `5`：对行二分会找到 `3` 那一行，答案却在 `2` 那一行',
            '→ 需要另想办法：利用行、列各自有序的性质']),
        ],
        quote='1、以(0, 0)为左上角，(x, y)为右下角的矩阵中，最大值就是(x, y)；2、以(x, y)为左上角，(m - 1, n - 1)为右下角的矩阵中，最小值就是(x, y)',
        quote_src='—— yiduobo 题解',
        idea=['从左下角 `(m-1, 0)` 开始查找，两条性质都能用上',
              'target 小于它 → 由性质 2，==这一行都不可能==，`x -= 1`',
              'target 大于它 → 由性质 1，==这一列都不可能==，`y += 1`'],
        summary=['时间 `O(m+n)`：每次排除一行或一列；空间 `O(1)`',
                 '左下角、右上角都可以；左上角、右下角不行（两个方向同增或同减）',
                 '`while` 条件越界 → 行列都排除完 → 返回 `False`',
                 '只删去了 `"""type ..."""` 文档字符串，其余照搬（兼容 Python 3）'],
    ),
)
