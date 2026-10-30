MATRIX, TARGET = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13


def _row_search_end(matrix, target):
    """(left, right) when yiduobo's first-column search breaks out — used only to tell the two phases apart
    in the views (both phases reuse the names left/right/mid)"""
    left, right = 0, len(matrix) - 1
    while left <= right:
        if left >= right - 1:
            return left, right
        mid = (left + right) // 2
        if matrix[mid][0] == target:
            return None
        elif matrix[mid][0] > target:
            right = mid - 1
        else:
            left = mid
    return None


PH1_END = _row_search_end(MATRIX, TARGET)


def _phase(S):
    if 'left' not in S:
        return 0
    if S.get('line') is None or (S['left'], S['right']) == PH1_END:
        return 1
    return 2


def _seq(S):
    if _phase(S) == 2:
        return S['matrix'][S['line']]
    return [row[0] for row in S['matrix']]


def _state(S):
    ph = _phase(S)
    if ph == 0:
        return '先确定 target 在==哪一行==，再到那一行里找'
    if ph == 1:
        s = f"第一次二分：在==第一列==里找行   范围 `[{S['left']}, {S['right']}]`（行号）"
        if S.get('line') is not None:
            s = f"第一次二分结束：target 只可能在==第 {S['line']} 行=="
        return s
    l, r = S['left'], S['right']
    return f"第二次二分：在==第 {S['line']} 行==里找   范围 `[{l}, {r}]`（列号）" + ('（空）' if l > r else '')


def _grid_color(S, i, j, v):
    ph = _phase(S)
    if ph == 1:
        if S.get('line') is not None:
            return 'green' if i == S['line'] else None
        return 'cyan' if j == 0 and S['left'] <= i <= S['right'] else None
    if ph == 2 and i == S['line']:
        return 'cyan' if S['left'] <= j <= S['right'] else None
    return None


def _cur_r(S):
    if 'mid' not in S:
        return None
    return S['line'] if _phase(S) == 2 else S['mid']


def _cur_c(S):
    if 'mid' not in S:
        return None
    return S['mid'] if _phase(S) == 2 else 0


def _near(S, B, ret):
    if B.left >= B.right - 1:
        return f'`left = {B.left}`、`right = {B.right}`：只剩相邻（或同一）两行 → ==直接判断是哪一行=='
    return f'`left = {B.left}`、`right = {B.right}`：范围里不止两行 → 继续二分'


def _eq(expr):
    def f(S, B, ret):
        v = eval(expr, {}, {'matrix': S.matrix, 'mid': S.mid, 'right': S.right, 'line': S.get('line')})
        if v == S.target:
            return f'`{expr} = {v}` 等于 target → ==找到了=='
        return f'`{expr} = {v} ≠ {S.target}`'
    return f


def _last(S, B, ret):
    v, t = S.matrix[S.right][0], S.target
    if v < t:
        return f'`matrix[right][0] = {v} < {t}`：第 right 行开头就比 target 小 → target 在第 `{S.right}` 行'
    return f'`matrix[right][0] = {v} > {t}`：第 right 行开头就比 target 大 → 只能在第 `{S.left}` 行'


def _col_gt(S, B, ret):
    v, t = S.matrix[S.mid][0], S.target
    if v > t:
        return f'`{v} > {t}`：第 {S.mid} 行开头就比 target 大 → target 在更上面的行'
    return f'`{v} < {t}`：target 可能就在第 {S.mid} 行，也可能在更下面'


def _row_gt(S, B, ret):
    v, t = S.matrix[S.line][S.mid], S.target
    if v > t:
        return f'`{v} > {t}` → target 只能在左边'
    return f'`{v} < {t}` → target 只能在右边'


CONFIG = dict(
    num=74, title='搜索二维矩阵', difficulty='Medium', category='二分查找',
    author='yiduobo', technique='两次二分：先第一列定行，再在行内找',
    code='''
class Solution(object):
    def searchMatrix(self, matrix, target):
        m = len(matrix)
        if m == 0:
            return False
        n = len(matrix[0])
        if n == 0:
            return False

        line = None
        if target < matrix[0][0]:
            return False
        elif target > matrix[m - 1][0]:
            line = m - 1
        else:
            left = 0
            right = m - 1
            while left <= right:
                if left >= right - 1:
                    if matrix[right][0] == target:
                        return True
                    elif matrix[right][0] < target:
                        line = right
                    else:
                        line = left
                    break
                mid = (left + right) // 2
                if matrix[mid][0] == target:
                    return True
                elif matrix[mid][0] > target:
                    right = mid - 1
                else:
                    left = mid

        left = 0
        right = n - 1
        while left <= right:
            mid = (left + right) // 2
            if matrix[line][mid] == target:
                return True
            elif matrix[line][mid] > target:
                right = mid - 1
            else:
                left = mid + 1

        return False
''',
    call=f'Solution().searchMatrix({MATRIX}, {TARGET})',
    expect=False,
    views=[
        dict(type='text', fn=_state, size=27),
        dict(type='array', var=_seq, label=' ', cell=110, h=250,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}, window=('left', 'right'),
             dim=lambda S, i, v: 'left' in S and not (S['left'] <= i <= S['right'])),
        dict(type='grid', var='matrix', label='matrix', h=290, cell=72,
             rows=lambda S: [f'{i}' for i in range(len(S['matrix']))],
             cursors=[(_cur_r, _cur_c, 'yellow')], color=_grid_color),
        dict(type='text', size=23, h=50, text='上方一维序列 = 当前正在二分的那一列 / 那一行；青色 = 剩余范围'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('line', 'line', 'green'), ('target', 'target')],
    skip=['if m == 0', 'if n == 0', 'left = 0', 'right = n - 1', 'while left <= right'],
    captions={
        3: '`m = {m}` 行（空矩阵直接返回 False）',
        6: '`n = {n}` 列',
        10: '`line = None`：先找出 target 位于==哪一行==',
        11: '`target = {target} < matrix[0][0] = {matrix[0][0]}`？不成立：没有比最小的数还小',
        13: '`target = {target} > matrix[m-1][0] = {matrix[m - 1][0]}`？不成立 → 需要对==第一列==二分',
        17: '对第一列二分：范围 `[{left}, {right}]`（行号）',
        19: _near,
        20: _eq('matrix[right][0]'),
        21: '返回 `True`',
        22: _last,
        23: '`line = right = {line}`',
        25: '`line = left = {line}`：target 只可能在==第 {line} 行==',
        26: '`break`：行已确定，跳出第一次二分',
        27: '`mid = ({left} + {right}) // 2 = {mid}`，看第一列 `matrix[{mid}][0] = {matrix[mid][0]}`',
        28: _eq('matrix[mid][0]'),
        29: '返回 `True`',
        30: _col_gt,
        31: '`right = mid - 1 = {right}`，范围 `[{left}, {right}]`',
        33: '`left = mid = {left}`：==保留住左边界==（第 mid 行可能就是答案）',
        38: '第二次二分（第 `{line}` 行）：`mid = ({left} + {right}) // 2 = {mid}`',
        39: _eq('matrix[line][mid]'),
        40: '返回 `True`',
        41: _row_gt,
        42: '`right = mid - 1 = {right}`，范围 `[{left}, {right}]`',
        44: '`left = mid + 1 = {left}`，范围 `[{left}, {right}]`',
        46: '`left = {left} > right = {right}`：这一行也找完了，没有 target → 返回 `False`',
    },
    cards=dict(
        one_liner='两次二分：先在第一列确定行，再到那一行里找',
        complexity='时间 `O(log m + log n)`，空间 `O(1)`',
        problem=['`m × n` 矩阵：每行非严格递增，且==每行第一个数大于上一行最后一个数==',
                 '判断 `target` 是否在矩阵中；要求 `O(log(m·n))`',
                 '示例：`[[1,3,5,7],[10,11,16,20],[23,30,34,60]]`，`3` → `true`；`13` → `false`'],
        quote='二分时需要找的是k，使其满足matrix[k][0] <= target且matrix[k + 1][0] > target，==因此二分的时候需要保留住左边界，即left = mid==而不是left = mid - 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先对==第一列==二分，确定 target 位于哪一行；再到那一行里普通二分',
              '边界：`target < matrix[0][0]` 直接 False；`target > matrix[m-1][0]` 直接定为最后一行',
              '找最后一个 `matrix[k][0] ≤ target` 的行 → `left = mid` 保留候选，剩两行时直接判断'],
        result='返回 `False`：第 1 行是 `[10,11,16,20]`，没有 13 ✓',
        summary=['两次二分：时间 `O(log m + log n) = O(log(mn))`，空间 `O(1)`',
                 '原文为 Python 2 写法：`/` 整除已改为 `//`，并删去了 `"""type"""` 文档字符串',
                 '`left = mid` 必须配合 `left >= right - 1` 时收尾，否则区间缩不动会死循环',
                 '对比灵神：把矩阵直接看成一维有序数组，一次二分，代码更短'],
    ),
)
