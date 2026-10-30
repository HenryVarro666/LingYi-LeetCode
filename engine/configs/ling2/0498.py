MAT = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def _order(m, n):
    out = []
    for k in range(m + n - 1):
        lo, hi = max(k - m + 1, 0), min(k, n - 1)
        js = range(lo, hi + 1) if k % 2 == 0 else range(hi, lo - 1, -1)
        out += [(k - j, j) for j in js]
    return out


def _color(S, i, j, v):
    if 'ans' not in S:
        return None
    order = _order(len(S['mat']), len(S['mat'][0]))
    done = order[:len(S['ans'])]
    if done and (i, j) == done[-1] and S.get('_line') in (10, 13):
        return 'yellow'
    if (i, j) in done:
        return 'green'
    if 'k' in S and i + j == S['k']:
        return 'blue'
    return None


def _info(S):
    if 'k' not in S:
        return '对角线上 `i + j` 是定值 `k`：`k = 0, 1, …, m+n−2` 一条条枚举'
    k = S['k']
    s = f"第 `k = {k}` 条对角线（`i + j = {k}`）"
    if 'max_j' in S and S.get('_line', 0) >= 7:
        s += f"：`j ∈ [{S['min_j']}, {S['max_j']}]`，" + ('偶数 → j 从小到大（↗）' if k % 2 == 0 else '奇数 → j 从大到小（↙）')
    return s


CONFIG = dict(
    num=498, title='对角线遍历', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='枚举 k = i + j · 算出 j 的范围',
    tags=['热题173'],
    code='''
class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        m, n = len(mat), len(mat[0])
        ans = []
        for k in range(m + n - 1):
            min_j = max(k - m + 1, 0)
            max_j = min(k, n - 1)
            if k % 2 == 0:  # 偶数从左到右
                for j in range(min_j, max_j + 1):
                    ans.append(mat[k - j][j])
            else:  # 奇数从右到左
                for j in range(max_j, min_j - 1, -1):
                    ans.append(mat[k - j][j])
        return ans
''',
    call=f'Solution().findDiagonalOrder({MAT})',
    expect=[1, 2, 4, 7, 5, 3, 6, 8, 9],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='grid', var='mat', label='mat（蓝 = 当前对角线，黄 = 刚取的，绿 = 已取）', h=380, cell=100,
             color=_color, rows=lambda S: list(range(len(S['mat']))), cols=lambda S: list(range(len(S['mat'][0])))),
        dict(type='array', var='ans', label='ans', cell=70, h=140),
    ],
    watch=[('k', 'k', 'blue'), ('min_j', 'min_j'), ('max_j', 'max_j'), ('j', 'j', 'yellow'), ('i = k - j', 'k - j')],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列；对角线编号 `k = i + j` 从 `0` 到 `m + n − 2 = {m + n - 2}`',
        'ans = []': '`ans` 存遍历结果',
        'for k in range': lambda S, B, ret: (f'枚举第 `k = {S.k}` 条对角线：上面的格子都满足 `i + j = {S.k}`'
                                             if S.get('k') != B.get('k') else '所有对角线都遍历完了'),
        'min_j = max': lambda S, B, ret: (
            f'`i` 最大取 `m − 1` 时 j 最小：`k − m + 1 = {S.k - S.m + 1}`' + ('，==不能是负数==' if S.k - S.m + 1 < 0 else '')
            + f' → `min_j = {S.min_j}`' if S.k == 0 else f'`min_j = max({S.k} − {S.m} + 1, 0) = {S.min_j}`'),
        'max_j = min': lambda S, B, ret: (
            f'`i = 0` 时 j 最大：`k = {S.k}`，==不能超过 n − 1== → `max_j = {S.max_j}`' if S.k == 0
            else f'`max_j = min({S.k}, {S.n - 1}) = {S.max_j}`' + ('（被 `n − 1` 截住）' if S.k > S.n - 1 else '')),
        'if k % 2 == 0': lambda S, B, ret: (f'`k = {S.k}` 是偶数：==从左下往右上==走，j 从小到大' if S.k % 2 == 0
                                            else f'`k = {S.k}` 是奇数：==从右上往左下==走，j 从大到小'),
        'ans.append': '`j = {j}` → `i = k − j = {k - j}`，取 `mat[{k - j}][{j}] = {ans[-1]}`',
        'return ans': '每条对角线按奇偶交替方向走完：返回 `{ret}`',
    },
    skip=['for j in range'],
    cards=dict(
        one_liner='同一条对角线上 i + j 相等：枚举 k = i + j，奇偶决定方向',
        complexity='时间 `O(mn)`，空间 `O(1)`（不计返回值）',
        problem=['按对角线==之字形==的顺序，返回 `m × n` 矩阵的所有元素',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,2,4,7,5,3,6,8,9]`'],
        quote='对于每条对角线，==行号 i 加列号 j 是一个定值==。设 k=i+j……枚举 k=0,1,2,…,m+n−2，就相当于在从左上到右下，一条一条地枚举对角线。',
        quote_src='—— 灵茶山艾府题解',
        idea=['知道 j 就知道 `i = k − j`，只要算出每条对角线上 j 的范围',
              '`min_j = max(k − m + 1, 0)`（i 最大为 m−1），`max_j = min(k, n − 1)`（i 最小为 0）',
              '`k` 偶数 j 从小到大，奇数 j 从大到小，把 `mat[k−j][j]` 加入答案'],
        result='返回 `[1,2,4,7,5,3,6,8,9]` ✓',
        summary=['时间 `O(mn)`：每个格子恰好访问一次；空间 `O(1)`',
                 '易错：j 的上下界要同时考虑 `i`、`j` 都不出界',
                 '这是遍历对角线的==模板==：相似题 3446、2711、1329'],
    ),
)
