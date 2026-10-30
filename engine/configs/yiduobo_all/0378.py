def _counting(S):
    i = S.get('_inner', {})
    return 'x' in i and 'cnt' in i and 'mid' in i


def _cell(S, i, j, v):
    if not _counting(S):
        return None
    return 'green' if j < S['y'] and v <= S['mid'] else None


def _cur_x(S):
    if _counting(S) and S['x'] >= 0 and S['y'] < S['n']:
        return S['x']
    return None


def _info(S):
    if _counting(S):
        return f"数 `<= mid = {S['mid']}` 的个数：从==左下角==出发，一列一列往右数"
    if 'l' in S and 'r' in S:
        return f"答案在闭区间 `[{S['l']}, {S['r']}]` 里"
    return '二分答案：边界是 `matrix[0][0]` 和 `matrix[n-1][n-1]`'


def _cmp(S, B, r):
    x, y, mid = S.x, S.y, S.mid
    v = S.matrix[x][y]
    if v <= mid:
        return f'`matrix[{x}][{y}] = {v} <= {mid}`：它和上面共 `{x + 1}` 个都 `<= {mid}` → 计入，==x 不动==看下一列'
    return f'`matrix[{x}][{y}] = {v} > {mid}`：太大了，在第 {y} 列==往上==找更小的'


CONFIG = dict(
    num=378, title='有序矩阵中第 K 小的元素', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 + 逐列计数',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def kthSmallest(self, matrix, k):

        n = len(matrix)

        l = matrix[0][0]
        r = matrix[n - 1][n - 1]
        while l < r:
            mid = (l + r) // 2

            x = n - 1
            y = 0
            cnt = 0
            while x >= 0 and y < n:
                if matrix[x][y] <= mid:
                    cnt += x + 1
                    y += 1
                else:
                    x -= 1

            if cnt >= k:
                r = mid
            else:
                l = mid + 1

        return l
''',
    call='Solution().kthSmallest([[1,5,9],[10,11,13],[12,13,15]], 8)',
    expect=13,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='grid', var='matrix', label='matrix（绿 = 已计入 cnt，黄框 = (x, y)）', cell=110, h=420,
             color=_cell, cursors=[(_cur_x, 'y', 'yellow', '(x,y)')]),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'orange'), ('cnt', 'cnt', 'green'), ('k', 'k')],
    captions={
        'n = len': '`n = {n}`',
        'l = matrix[0][0]': '答案下界：最小值 `l = {l}`',
        'r = matrix[n - 1][n - 1]': '答案上界：最大值 `r = {r}`',
        'while l < r': lambda S, B, r: (f'`[{S.l}, {S.r}]` 里不止一个数，继续二分' if S.l < S.r
                                        else f'`l == r = {S.l}`：答案确定'),
        'mid = (l + r) // 2': '猜 `mid = ({l} + {r}) // 2` = =={mid}==',
        'cnt = 0': '从==左下角== `({x}, 0)` 出发、`cnt = 0`：左下角是第 0 列最大的数',
        'if matrix[x][y] <= mid': _cmp,
        'cnt += x + 1': '`cnt += {B.x} + 1` → =={cnt}==',
        'if cnt >= k': lambda S, B, r: (f'`cnt = {S.cnt} >= k = {S.k}`：第 k 小 `<= {S.mid}`' if S.cnt >= S.k
                                        else f'`cnt = {S.cnt} < k = {S.k}`：第 k 小 `> {S.mid}`'),
        'r = mid': '收缩上界 `r = {r}`',
        'l = mid + 1': '`mid` 不可能是答案，`l = mid + 1 = {l}`',
        'return l': '返回 `l = {ret}`',
    },
    skip=['x = n - 1', 'y = 0', 'while x >= 0', 'y += 1', 'x -= 1'],
    max_steps=90,
    cards=dict(
        one_liner='二分答案；每次从左下角逐列数出 <= mid 的个数',
        complexity='时间 `O(n log(max − min))`，空间 `O(1)`',
        problem=['`n x n` 矩阵每行、每列都升序，求排序后第 `k` 小的元素（重复也算）',
                 '要求内存优于 `O(n²)`',
                 '示例：`[[1,5,9],[10,11,13],[12,13,15]]`，`k = 8` → `13`'],
        quote='对于第j + 1列，必然有 matrix[i + 1][j + 1] > matrix[i + 1][j] > k，因此可以直接从matrix[i][j + 1]开始检测第j + 1行中有多少个数小于等于k',
        quote_src='—— yiduobo 题解原文',
        idea=['第 y 列从下往上找到第一个 `<= mid` 的位置 x：这一列有 `x + 1` 个',
              '右边一列在 x 之下的数更大，==不用回头==，直接从 `(x, y+1)` 继续',
              '`O(n + n)` 数完后二分：`cnt >= k` 收上界，否则 `l = mid + 1`'],
        summary=['二分 `log(max − min)` 次，每次计数 `O(2n)`；空间 `O(1)`',
                 '闭区间写法：`while l < r`，`r = mid` / `l = mid + 1`，最后 `l` 就是答案',
                 '计数用 `<=` 不是 `<`：重复元素要全部算上',
                 '对比灵神：灵神从右上角按行数、开区间二分；yiduobo 从左下角按列数',
                 '原文为 Python 2 写法，`mid = (l + r) / 2` 已改为 `//`，并删去空文档字符串'],
    ),
)
