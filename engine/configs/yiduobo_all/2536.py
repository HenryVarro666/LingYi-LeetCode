def _fcolor(S, a, b, v):
    ln = S.get('_line', 0)
    if ln in (6, 7, 8, 9) and 'x2' in S:
        pts = {(S['x1'], S['y1']): 'green', (S['x2'] + 1, S['y1']): 'red', (S['x1'], S['y2'] + 1): 'red', (S['x2'] + 1, S['y2'] + 1): 'green'}
        return pts.get((a, b))
    if ln >= 14 and 'i' in S and 'j' in S and (a, b) == (S['i'], S['j']):
        return 'yellow'
    return None


def _rcolor(S, a, b, v):
    if 'i' in S and 'j' in S and S.get('_line', 0) >= 14:
        i, j = S['i'], S['j']
        if (a, b) == (i, j):
            return 'yellow'
        if (a, b) in ((i - 1, j), (i, j - 1)):
            return 'blue'
        if (a, b) == (i - 1, j - 1):
            return 'red'
    return None


def _fm(S):
    ln = S.get('_line', 0)
    if ln in (5, 6, 7, 8, 9) and 'x2' in S:
        return f"矩形 `({S['x1']},{S['y1']})~({S['x2']},{S['y2']})`：只改 f 的四个点：起点 +1，下方、右方 −1，右下 +1"
    if ln >= 14 and 'i' in S and 'j' in S:
        i, j = S['i'], S['j']
        return f"`res[{i}][{j}]` = 左上角 `(0,0)~({i},{j})` 里所有 f 之和"
    return '差分数组 f：只记录变化的「边界」，res 是它的二维前缀和'


def _gen(S, B, ret):
    i, j = B.i, B.j
    return f'`res[{i}][{j}] = res[{i-1}][{j}] + res[{i}][{j-1}] - res[{i-1}][{j-1}] + f[{i}][{j}]` = {B.res[i-1][j]} + {B.res[i][j-1]} − {B.res[i-1][j-1]} + {B.f[i][j]} = =={S.res[i][j]}=='


CONFIG = dict(
    num=2536, title='子矩阵元素加 1', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二维差分数组 + 前缀和递推',
    tags=['常用数据结构', '难度分 1583'],
    code='''
class Solution(object):
    def rangeAddQueries(self, n, queries):

        f = [[0] * (n + 1) for _ in range(n + 1)]
        for x1, y1, x2, y2 in queries:
            f[x1][y1] += 1
            f[x2 + 1][y1] -= 1
            f[x1][y2 + 1] -= 1
            f[x2 + 1][y2 + 1] += 1

        res = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        res[i][j] = f[i][j]
                    else:
                        res[i][j] = res[i][j - 1] + f[i][j]
                elif j == 0:
                    res[i][j] = res[i - 1][j] + f[i][j]
                else:
                    res[i][j] = res[i - 1][j] + res[i][j - 1] - res[i - 1][j - 1] + f[i][j]

        
        return res
''',
    call='Solution().rangeAddQueries(3, [[1,1,2,2],[0,0,1,1]])',
    expect=[[1, 1, 0], [1, 2, 1], [0, 1, 1]],
    views=[
        dict(type='text', fn=_fm, h=64),
        dict(type='grid', var='f', label='f 差分数组（(n+1)×(n+1)，多出的一行一列放「减回去」）', color=_fcolor, cell=64, h=300),
        dict(type='grid', var='res', label='res（黄 = 正在算，蓝 = 上/左，红 = 左上）', color=_rcolor, cell=64, h=230),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('(x1,y1)', lambda S: (S['x1'], S['y1']) if 'x1' in S else '-', 'green'),
           ('(x2,y2)', lambda S: (S['x2'], S['y2']) if 'x2' in S else '-', 'orange')],
    captions={
        'f = [[0]': '`f` 多开一行一列：`x2 + 1`、`y2 + 1` 可能等于 `n`',
        'for x1, y1, x2, y2 in queries': '取出一次修改：`({x1},{y1})` 到 `({x2},{y2})`',
        'f[x1][y1] += 1': '起点 `+1`：相当于 `[(x1,y1),(m,n)]` 整块加 1，`f[{x1}][{y1}] = {f[x1][y1]}`',
        'f[x2 + 1][y1] -= 1': '`-1`：把 `x2` 下方多加的部分减掉，`f[{x2+1}][{y1}] = {f[x2+1][y1]}`',
        'f[x1][y2 + 1] -= 1': '`-1`：把 `y2` 右方多加的部分减掉，`f[{x1}][{y2+1}] = {f[x1][y2+1]}`',
        'f[x2 + 1][y2 + 1] += 1': '`+1`：右下角被减了两次，补回一次，`f[{x2+1}][{y2+1}] = {f[x2+1][y2+1]}`',
        'res = [[0]': '`res` 是最终答案，`res[i][j]` = `f` 左上角矩形的元素和',
        'if i == 0': lambda S, B, r: f'`i = {B.i}`：' + ('==第一行==，没有上面一行' if B.i == 0 else '不是第一行'),
        15: lambda S, B, r: f'`j = {B.j}`：' + ('==左上角起点==，直接取 `f`' if B.j == 0 else '第一行，只能靠左边'),
        19: lambda S, B, r: f'`j = {B.j}`：' + ('==第一列==，只能靠上面' if B.j == 0 else '内部格子，上、左、左上都有'),
        'res[i][j] = f[i][j]': '起点：`res[0][0] = f[0][0] = {res[0][0]}`',
        'res[i][j] = res[i][j - 1] + f[i][j]': '第一行：`res[{i}][{j}] = 左边 + f[{i}][{j}]` = =={res[i][j]}==',
        'res[i][j] = res[i - 1][j] + f[i][j]': '第一列：`res[{i}][{j}] = 上边 + f[{i}][{j}]` = =={res[i][j]}==',
        'res[i - 1][j - 1] + f[i][j]': _gen,
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='先在差分数组 f 上只改四个点，最后用 res 递推出每格的值',
        complexity='时间 `O(n^2 + q)`，空间 `O(n^2)`',
        problem=['`n×n` 的全 0 矩阵，每个查询给出子矩阵 `(x1,y1)~(x2,y2)`，把里面每个元素 `+1`',
                 '返回所有查询之后的矩阵',
                 '示例：`n = 3, [[1,1,2,2],[0,0,1,1]]` → `[[1,1,0],[1,2,1],[0,1,1]]`'],
        quote='对应到二维差分数组中，就是将f[x1][y1]加上1，将f[x2 + 1][y1]以及f[x1][y2 + 1]减去1，然后将f[x2 + 1][y2 + 1]加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['一维：区间 `[l, r]` 加 1 = `f[l] += 1`、`f[r+1] -= 1`',
              '二维：整块 `[(x1,y1),(m,n)]` 加 1，再减去下方、右方两块，右下角被减了两次再加回',
              '`res[i][j]` 是 f 左上角矩形的和，用 `上 + 左 − 左上 + f[i][j]` 递推'],
        summary=['时间 `O(n^2 + q)`，空间 `O(n^2)`',
                 '`f` 要开 `(n+1)×(n+1)`：`x2 + 1` 可能等于 `n`',
                 '递推公式要处理第一行、第一列，避免下标变成 -1（Python 会绕到末尾，算错）',
                 '对比灵神：灵神把 diff 上、左各补一行一列 0，省掉 if 分支，并原地算前缀和'],
    ),
)
