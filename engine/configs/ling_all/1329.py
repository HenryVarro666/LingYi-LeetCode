MAT = [[3, 3, 1, 1], [2, 2, 1, 2], [1, 1, 1, 2]]


def _on(S, i, j):
    return 'k' in S and S.get('_line') in (5, 6, 7, 8) and i - j == S['k']


def _written(S, i):
    ln, ci = S.get('_line'), S.get('i')
    if ln != 8 or not isinstance(ci, int):
        return False
    return i <= ci


def _cell(S, i, j, v):
    if not _on(S, i, j):
        return None
    return 'green' if _written(S, i) else 'blue'


def _ci(S):
    return S['i'] if S.get('_line') == 8 else None


def _cj(S):
    return S['i'] - S['k'] if S.get('_line') == 8 else None


def _hint(S):
    ln = S.get('_line')
    if 'k' not in S or ln not in (5, 6, 7, 8):
        return '同一条对角线上 `i − j` 是定值 `k`：从右上角那条开始，一条条排序'
    k, n = S['k'], S['n']
    if 'left_i' not in S:
        return f'`k = {k}`：这条对角线上每个格子都满足 `i − j = {k}`'
    return f'`k = {k}`：`i ∈ [{S["left_i"]}, {S["right_i"]})`，列号 `j = i − k`'


CONFIG = dict(
    num=1329, title='将矩阵按对角线排序', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举对角线 k=i−j · 取出排序再放回',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1548'],
    code='''
class Solution:
    def diagonalSort(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        for k in range(1 - n, m):  # k = i - j
            left_i, right_i = max(k, 0), min(k + n, m)
            a = sorted(mat[i][i - k] for i in range(left_i, right_i))
            for i in range(left_i, right_i):
                mat[i][i - k] = a[i - left_i]
        return mat
''',
    call=f'Solution().diagonalSort({MAT})',
    expect=[[1, 1, 1, 1], [1, 2, 2, 2], [1, 2, 3, 3]],
    skip=[7],
    views=[
        dict(type='grid', var='mat', label='mat（蓝 = 当前对角线，绿 = 已按升序写回的格子，粉框 = 正在写的格子）', cell=100, h=340,
             color=_cell, cursors=[(_ci, _cj, 'pink')]),
        dict(type='array', var='a', label='a（这条对角线排序后的结果）', cell=96, h=190),
        dict(type='text', fn=_hint, size=26, h=90),
    ],
    watch=[('k', 'k', 'blue'), ('left_i', 'left_i', 'cyan'), ('right_i', 'right_i', 'orange'), ('a', 'a', 'green')],
    captions={
        'm, n = len': '`m = {m}`，`n = {n}`：对角线条数 `m + n − 1 = {m + n - 1}`',
        'for k in range': lambda S, B, r: ((f'第 `k = {S.k}` 条对角线（`i − j = {S.k}`），从右上角开始' if 'k' not in B
                                            else f'下一条：`k = {S.k}`（`i − j = {S.k}`）') if 'k' not in B or S.k != B.k
                                           else '所有对角线都排好了'),
        5: '`i` 下限 `max({k}, 0) = {left_i}`（`j = 0` 时 `i = k`），上限 `min(k+n, m) = {right_i}`（开区间）',
        6: lambda S, B, r: (f'取出对角线 `{[S.mat[i][i - S.k] for i in range(S.left_i, S.right_i)]}`，从小到大排序 → `a = {S.a}`'),
        'mat[i][i - k] = a[i - left_i]': '放回 `mat[{i}][{i - k}] = a[{i - left_i}] = {a[i - left_i]}`',
        'return mat': '每条对角线都升序了 → 返回 `mat`',
    },
    cards=dict(
        one_liner='同一条对角线上 i−j 为定值：一条条取出、排序、放回',
        complexity='时间 `O(mn log min(m,n))`，空间 `O(min(m,n))`',
        problem=['`m × n` 矩阵，把每条右下方向的对角线上的数按==升序==排好',
                 '对角线从最上面一行或最左边一列的某个元素出发，沿右下方向走',
                 '示例：`[[3,3,1,1],[2,2,1,2],[1,1,1,2]]` → `[[1,1,1,1],[1,2,2,2],[1,2,3,3]]`'],
        quote='一条对角线上的坐标满足什么性质？……行下标减列下标等于一个定值 k。考虑从右上第一条对角线开始，一条一条地排序，直到左下最后一条对角线结束。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k = i − j`：第一条（右上角）`k = 1 − n`，最后一条（左下角）`k = m − 1`',
              '知道 `i` 就知道 `j = i − k`；`i` 取 `[max(k, 0), min(k+n, m))`',
              '把 `mat[i][i−k]` 收集排序，再依次填回同一批格子'],
        summary=['时间 `O(mn log min(m,n))`：对角线长度至多 `min(m,n)`',
                 '易错：`i` 的范围是==左闭右开== `[max(k,0), min(k+n,m))`',
                 '`k` 从 `1 − n` 到 `m − 1`，共 `m + n − 1` 条',
                 '另有一种原地排序写法（Go 的 Less/Swap），本视频用辅助数组 `a`',
                 '同类：3446 按对角线排序（分升降序）、2711 对角线上不同值'],
    ),
)
