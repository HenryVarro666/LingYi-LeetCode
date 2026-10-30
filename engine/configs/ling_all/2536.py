def _q(S):
    return (S['r1'], S['c1'], S['r2'], S['c2']) if 'r2' in S else None


def _dcolor(S, a, b, v):
    q = _q(S)
    ln = S.get('_line', 0)
    if ln in (6, 7, 8, 9) and q:
        r1, c1, r2, c2 = q
        pts = {(r1 + 1, c1 + 1): 'green', (r1 + 1, c2 + 2): 'red', (r2 + 2, c1 + 1): 'red', (r2 + 2, c2 + 2): 'green'}
        return pts.get((a, b))
    if ln >= 12 and 'i' in S and 'j' in S:
        i, j = S['i'], S['j']
        if (a, b) == (i + 1, j + 1):
            return 'yellow'
        if (a, b) in ((i + 1, j), (i, j + 1)):
            return 'blue'
        if (a, b) == (i, j):
            return 'red'
    return None


def _acolor(S, i, j, v):
    if 'i' in S and 'j' in S and (i, j) == (S['i'], S['j']) and S.get('_line', 0) >= 12:
        return 'yellow'
    return None


def _fm(S):
    ln = S.get('_line', 0)
    q = _q(S)
    if ln in (5, 6, 7, 8, 9) and q:
        r1, c1, r2, c2 = q
        return f'查询 `({r1},{c1})~({r2},{c2})`：左上 +1，右上 −1，左下 −1，右下 +1（下标整体偏移 1）'
    if ln >= 12 and 'i' in S and 'j' in S:
        i, j = S['i'], S['j']
        return f'`diff[{i+1}][{j+1}]` 累加 左 `{S["diff"][i+1][j]}` + 上 `{S["diff"][i][j+1]}` − 左上 `{S["diff"][i][j]}`'
    return '二维差分：每次查询只改 4 个格子；最后做二维前缀和还原'


CONFIG = dict(
    num=2536, title='子矩阵元素加 1', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='二维差分 + 二维前缀和',
    tags=['常用数据结构', '难度分 1583'],
    code='''
class Solution:
    def rangeAddQueries(self, n: int, queries: List[List[int]]) -> List[List[int]]:
        # 二维差分
        diff = [[0] * (n + 2) for _ in range(n + 2)]
        for r1, c1, r2, c2 in queries:
            diff[r1 + 1][c1 + 1] += 1
            diff[r1 + 1][c2 + 2] -= 1
            diff[r2 + 2][c1 + 1] -= 1
            diff[r2 + 2][c2 + 2] += 1

        # 原地计算 diff 的二维前缀和，然后填入答案
        ans = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                diff[i + 1][j + 1] += diff[i + 1][j] + diff[i][j + 1] - diff[i][j]
                ans[i][j] = diff[i + 1][j + 1]
        return ans
''',
    call='Solution().rangeAddQueries(3, [[1,1,2,2],[0,0,1,1]])',
    expect=[[1, 1, 0], [1, 2, 1], [0, 1, 1]],
    views=[
        dict(type='text', fn=_fm, h=64),
        dict(type='grid', var='diff', label='diff（上方多一行 0、左侧多一列 0，共 (n+2)×(n+2)）', color=_dcolor, cell=64, h=330),
        dict(type='grid', var='ans', label='ans', color=_acolor, cell=64, h=220),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('r1,c1', lambda S: (S['r1'], S['c1']) if 'r1' in S else '-', 'green'),
           ('r2,c2', lambda S: (S['r2'], S['c2']) if 'r2' in S else '-', 'orange')],
    captions={
        'diff = [[0]': '`diff` 比答案多一行一列（上、左各补 0 防越界，下、右各多 1 防 `+2` 越界）',
        'for r1, c1, r2, c2 in queries': '取出查询：左上 `({r1},{c1})`，右下 `({r2},{c2})`',
        'diff[r1 + 1][c1 + 1] += 1': '左上角 `+1`：从这里往右下的所有格子都被 +1，`diff[{r1+1}][{c1+1}] = {diff[r1+1][c1+1]}`',
        'diff[r1 + 1][c2 + 2] -= 1': '右上角外侧 `-1`：把多出右边的部分减掉，`diff[{r1+1}][{c2+2}] = {diff[r1+1][c2+2]}`',
        'diff[r2 + 2][c1 + 1] -= 1': '左下角外侧 `-1`：把多出下边的部分减掉，`diff[{r2+2}][{c1+1}] = {diff[r2+2][c1+1]}`',
        'diff[r2 + 2][c2 + 2] += 1': '右下角外侧 `+1`：上面两次 −1 把这块减了两次，补回来，`diff[{r2+2}][{c2+2}] = {diff[r2+2][c2+2]}`',
        'ans = [[0]': '`ans` 是 n×n 的答案矩阵',
        'diff[i + 1][j + 1] +=': '二维前缀和：`diff[{i+1}][{j+1}]` = 自己 + 左 + 上 − 左上（左上被重复算了一次）= =={diff[i+1][j+1]}==',
        'ans[i][j] = diff': '前缀和就是这个格子被加的次数：`ans[{i}][{j}] = {ans[i][j]}`',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='每次查询只改差分矩阵的 4 个角，最后一次二维前缀和还原',
        complexity='时间 `O(n^2 + q)`，空间 `O(n^2)`',
        problem=['`n×n` 的全 0 矩阵，每次查询把左上 `(r1,c1)`、右下 `(r2,c2)` 的子矩阵全部 `+1`',
                 '返回所有查询之后的矩阵',
                 '示例：`n = 3, [[1,1,2,2],[0,0,1,1]]` → `[[1,1,0],[1,2,1],[0,1,1]]`'],
        quote='用二维差分 O(1) 处理每个 queries[i]。然后计算二维差分矩阵的二维前缀和，即为答案。代码实现时，可以在二维差分矩阵最上面添加一行 0，最左边添加一列 0，这样计算二维前缀和无需考虑下标越界。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`+1` 打在左上角，右边界外、下边界外各 `-1`，右下角外 `+1` 补回重复减的部分',
              '前缀和把「影响向右下扩散」还原成每格的值',
              '补一行一列 0，前缀和公式不用判断边界，所以下标都 `+1`'],
        summary=['时间 `O(n^2 + q)`，空间 `O(n^2)`',
                 '易错：差分下标整体偏移 1，右下角用 `r2 + 2`、`c2 + 2`',
                 '前缀和公式：`自己 + 左 + 上 - 左上`',
                 '也可以建 `n×n` 的 diff 原地计算，最后直接返回 diff',
                 '同类题：一维差分 → 二维差分，见题单 §2.2'],
    ),
)
