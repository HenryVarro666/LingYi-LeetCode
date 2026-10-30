G = [[1, 7, 3], [9, 8, 2], [4, 5, 6]]


def _on(S, i, j):
    return 'k' in S and i - j + S['n'] == S['k']


def _written(S, i, j):
    """这一步里已经写回的格子（zip 循环里列号小于当前 j，或刚好是当前 j 且已执行赋值）"""
    ln, cj = S.get('_line'), S.get('j')
    if ln not in (13, 14) or not isinstance(cj, int):
        return False
    return j < cj or (j == cj and (ln == 14 or cj == S.get('max_j')))


def _cell(S, i, j, v):
    if S.get('_line') == 15 or not _on(S, i, j):
        return None
    return 'green' if _written(S, i, j) else 'blue'


def _hint(S):
    if 'k' not in S or S.get('_line') == 15:
        return '右上角在第一排，左下角在最后一排；每条对角线满足 `i − j + n = k`'
    k, n, m = S['k'], S['n'], S['m']
    if 'min_j' not in S or S.get('_line', 0) < 10:
        side = '右上' if n - k > 0 else '左下（含主对角线）'
        return f'第 `{k}` 条对角线 `i − j + n = {k}`，在{side}三角形'
    d = '降序' if S['min_j'] == 0 else '升序'
    side = '左下（含主对角线）' if S['min_j'] == 0 else '右上'
    return f'`j ∈ [{S["min_j"]}, {S.get("max_j", "?")}]`，{side}三角形 → =={d}=='


CONFIG = dict(
    num=3446, title='按对角线进行矩阵排序', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举对角线 k=i−j+n · 模拟排序',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1373'],
    code='''
class Solution:
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        # 第一排在右上，最后一排在左下
        # 每排从左上到右下
        # 令 k=i-j+n，那么右上角 k=1，左下角 k=m+n-1
        for k in range(1, m + n):
            # 核心：计算 j 的最小值和最大值
            min_j = max(n - k, 0)  # i=0 的时候，j=n-k，但不能是负数
            max_j = min(m + n - 1 - k, n - 1)  # i=m-1 的时候，j=m+n-1-k，但不能超过 n-1
            a = [grid[k + j - n][j] for j in range(min_j, max_j + 1)]  # 根据 k 的定义得 i=k+j-n
            a.sort(reverse = min_j==0)
            for j, val in zip(range(min_j, max_j + 1), a):
                grid[k + j - n][j] = val
        return grid
''',
    call=f'Solution().sortMatrix({G})',
    expect=[[8, 2, 3], [9, 6, 7], [4, 5, 1]],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前对角线，绿 = 已按顺序写回的格子）', cell=110, h=370,
             color=_cell, cursors=[('k + j - n if _line in (13, 14) else None', 'j if _line in (13, 14) else None', 'pink')]),
        dict(type='array', var='a', label='a（这条对角线取出的数，排序后原样放回；粉 = 正在放回的）', cell=96, h=190,
             color=lambda S, i, v: 'pink' if S.get('_line') in (13, 14) and isinstance(S.get('j'), int) and i == S['j'] - S['min_j'] else None),
        dict(type='text', fn=_hint, size=26, h=90),
    ],
    watch=[('k', 'k', 'blue'), ('min_j', 'min_j', 'cyan'), ('max_j', 'max_j', 'orange'), ('a', 'a', 'green')],
    captions={
        'm, n = len': '`m = {m}`，`n = {n}`：一共 `m + n − 1 = {m + n - 1}` 条对角线',
        'for k in range': lambda S, B, r: (f'第 `k = {S.k}` 条对角线（`i − j + n = {S.k}`）：右上角 k=1，往左下依次枚举'
                                           if 'k' in B and S.k != B.k or 'k' not in B else '所有对角线都处理完了'),
        'min_j = max': '`j` 最小：第一排 `i = 0` 时 `j = n − k = {n - k}`，但不能为负，与 0 取大 → `min_j = {min_j}`',
        'max_j = min': '`j` 最大：最后一排 `i = m − 1` 时 `j = m+n−1−k = {m + n - 1 - k}`，但不能超过 `n−1 = {n - 1}`，取小 → `max_j = {max_j}`',
        'a = [grid': '按 `i = k + j − n` 取出对角线：`a = {a}`',
        'a.sort': lambda S, B, r: (f'`min_j == 0`：对角线从第一列开始 → 左下三角（含主对角线）→ ==降序==：`a = {S.a}`'
                                   if S.min_j == 0 else
                                   f'`min_j = {S.min_j} > 0`：对角线不过第一列 → 右上三角 → ==升序==：`a = {S.a}`'),
        'for j, val in zip': lambda S, B, r: ('这条对角线写完了' if 'val' in B and 'j' in B and S.j == B.j and S.val == B.val
                                              else f'`j = {S.j}`，取排好序的 `val = {S.val}`'),
        'grid[k + j - n][j] = val': '写回 `grid[{k + j - n}][{j}] = {val}`',
        'return grid': '每条对角线都排好了 → 返回 `grid`',
    },
    cards=dict(
        one_liner='对角线上 i−j 是定值：一条条取出、排序、放回',
        complexity='时间 `O(n² log n)`，空间 `O(n)`',
        problem=['`n × n` 的矩阵 `grid`：左下三角（含主对角线）的每条对角线按==非递增==排序',
                 '右上三角的每条对角线按==非递减==排序，返回新矩阵',
                 '示例：`[[1,7,3],[9,8,2],[4,5,6]]` → `[[8,2,3],[9,6,7],[4,5,1]]`'],
        quote='对于每条对角线，行号 i 减列号 j 是一个定值。……设 k=i-j+n，那么右上角那条对角线的 k=1，左下角那条对角线的 k=m+n-1。枚举 k，就相当于一条一条地枚举对角线。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k = i − j + n` 相同 → 在同一条对角线上；知道 `j` 就知道 `i = k + j − n`',
              '算出每条对角线 `j` 的最小值 `max(n−k, 0)` 和最大值 `min(m+n−1−k, n−1)`',
              '`min_j > 0` 在右上三角（升序），否则降序；排完按原位置放回'],
        summary=['时间 `O(n² log n)`：`O(n)` 次、每次排序 `O(n log n)`',
                 '易错：`k = i − j + n` 里加 `n` 是为了让 `k` 从 1 开始，不用处理负下标',
                 '`min_j == 0` 才降序（含主对角线），写成 `min_j > 0` 升序会把方向搞反',
                 '同类：1329 将矩阵按对角线排序、2711 对角线上不同值的数量差'],
    ),
)
