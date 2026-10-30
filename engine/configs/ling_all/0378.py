def _in_check(S):
    return 'mx' in S.get('_inner', {})


def _cell(S, i, j, v):
    if not _in_check(S):
        return None
    return 'green' if i < S['i'] and v <= S['mx'] else None


def _info(S):
    if _in_check(S):
        return f"check({S['mx']})：数一数 `<= {S['mx']}` 的有多少个，够不够 `k = {S['k']}` 个"
    if 'left' in S and 'right' in S:
        return f"开区间 `({S['left']}, {S['right']})`：`left` 一定不够 k 个，`right` 一定够"
    return '第 k 小 = 最小的 x，使 `<= x` 的数==至少==有 k 个'


def _cmp(S, B, r):
    i, j, mx = S.i, S.j, S.mx
    v = S.matrix[i][j]
    if v > mx:
        return f'`matrix[{i}][{j}] = {v} > {mx}`：它下面的数更大 → ==第 {j} 列往下都不行=='
    return f'`matrix[{i}][{j}] = {v} <= {mx}`：它左边的数更小 → ==第 {i} 行前 {j + 1} 个都行=='


CONFIG = dict(
    num=378, title='有序矩阵中第 K 小的元素', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 双指针计数',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)

        def check(mx: int) -> bool:
            cnt = 0  # matrix 中的 <= mx 的元素个数
            i, j = 0, n - 1  # 从右上角开始
            while i < n and j >= 0 and cnt < k:
                if matrix[i][j] > mx:
                    j -= 1  # 排除第 j 列
                else:
                    cnt += j + 1  # 从 matrix[i][0] 到 matrix[i][j] 都 <= mx
                    i += 1
            return cnt >= k

        left, right = matrix[0][0] - 1, matrix[-1][-1]
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call='Solution().kthSmallest([[1,5,9],[10,11,13],[12,13,15]], 8)',
    expect=13,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='grid', var='matrix', label='matrix（绿 = 已计入 cnt，黄框 = (i, j)）', cell=110, h=420,
             color=_cell, cursors=[(lambda S: S['i'] if _in_check(S) and S['i'] < S['n'] and S['j'] >= 0 else None,
                                    'j', 'yellow', '(i,j)')]),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'orange'),
           ('cnt', lambda S: S['_inner'].get('cnt'), 'green'), ('k', 'k')],
    captions={
        'n = len': '`n = {n}`',
        'i, j = 0, n - 1': '`check({mx})`：从==右上角== `(0, {j})` 出发数 `cnt`，往左变小、往下变大',
        'while i < n and j >= 0 and cnt < k': lambda S, B, r: (
            f'`cnt = {S.cnt} >= k`：已经够了，==提前结束==' if S.cnt >= S.k else
            ('走出矩阵，统计完毕' if not (S.i < S.n and S.j >= 0) else f'`({S.i}, {S.j})` 在矩阵内且 `cnt = {S.cnt} < k`，继续')),
        'if matrix[i][j] > mx': _cmp,

        'cnt += j + 1': '`cnt += {j} + 1` → =={cnt}==，下一行',
        'return cnt >= k': lambda S, B, r: f'`cnt = {S.cnt}` ' + ('`>= k`（够了就提前停）' if r else '`< k`') + f' → 返回 =={r}==',
        'left, right = ': '开区间 `({left}, {right})`：`{left}` 一定不满足，`{right}` 一定满足',
        'while left + 1 < right': lambda S, B, r: (
            f'区间 `({S.left}, {S.right})` 不空，继续二分' if S.left + 1 < S.right else
            f'`left + 1 == right`：区间空了，答案就是 `right = {S.right}`'),
        'mid = (left + right) // 2': '猜答案 `mid = ({left} + {right}) // 2` = =={mid}==',
        'if check(mid)': '调用 `check({mid})`：`<= {mid}` 的数够不够 `k = {k}` 个？',
        'right = mid': '`check({mid})` ==成立==：答案 `<= {mid}`，`right` → {right}',
        'left = mid': '`check({mid})` ==不成立==：答案 `> {mid}`，`left` → {left}',
        'return right': '返回 `right = {ret}`：最小的满足条件的数',
    },
    skip=['cnt = 0', 'while i < n', 'j -= 1', 'i += 1'],
    max_steps=90,
    cards=dict(
        one_liner='第 k 小 = 最小的 x，使 <= x 的数至少有 k 个 → 二分猜答案',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['`n x n` 矩阵每行、每列都升序，求排序后第 `k` 小的元素（重复也算）',
                 '要求内存优于 `O(n²)`',
                 '示例：`[[1,5,9],[10,11,13],[12,13,15]]`，`k = 8` → `13`'],
        quote='第 k 小等价于：求最小的 x，满足 ≤ x 的数==至少==有 k 个。（注意是至少不是恰好）',
        quote_src='—— 灵茶山艾府题解',
        idea=['x 越大越容易凑够 k 个 → 单调，可以==二分猜答案==',
              '判定：从右上角出发，`> mx` 就排除这一列，否则这一行左边全算进 `cnt`',
              '开区间写法：`check(mid)` 成立更新 `right`，最后返回 `right`'],
        summary=['二分 `O(log U)` 次，每次双指针 `O(n)`；空间 `O(1)`',
                 '开区间初值：`left = matrix[0][0] - 1` 一定不够，`right = matrix[-1][-1]` 一定够',
                 '答案一定在矩阵里：否则 `check(ans - 1)` 也成立，与二分结果矛盾',
                 '`cnt < k` 时才继续数：够了就提前退出',
                 '题解另给了 `bisect_left` 库函数写法，思路相同'],
    ),
)
