GRID = [[7, 2, 9], [1, 5, 0], [2, 6, 6]]
K = 20


def _s_view(S):
    """还没算出来的格子显示成 ·（本题元素非负，且 grid[0][0] > 0，所以前缀和算出来后一定 > 0）"""
    s = S.get('s')
    if s is None:
        return None
    return [[v if v != 0 else None for v in r] for r in s]


def _cell(S, r, c, v):
    i, j, line = S.get('i'), S.get('j'), S.get('_line', 0)
    if i is None or j is None or 'k' not in S:
        return None
    if (r, c) == (i, j):
        if line < 13:
            return None
        if line <= 21:
            return 'yellow'
        return 'green' if v <= S['k'] else 'red'
    # 按行优先，前面的格子已经判断过：绿 = 计入，红 = 超过 k
    if (r, c) < (i, j):
        return 'green' if v <= S['k'] else 'red'
    return None


def _use(S, r, c, v):
    """formula 用到的格子：上 = 蓝，左 = 粉，左上 = 橙（被多加一次，要减掉）"""
    i, j, line = S.get('i'), S.get('j'), S.get('_line', 0)
    if i is None or j is None or 'k' not in S:
        return _cell(S, r, c, v)
    if (r, c) == (i, j) and 13 <= line <= 21:
        return 'yellow'
    if line == 15 and (r, c) == (i, j - 1):
        return 'pink'
    if line == 17 and (r, c) == (i - 1, j):
        return 'blue'
    if line == 19:
        if (r, c) == (i - 1, j):
            return 'blue'
        if (r, c) == (i, j - 1):
            return 'pink'
        if (r, c) == (i - 1, j - 1):
            return 'orange'
    return _cell(S, r, c, v)


def _formula(S):
    i, j, line = S.get('i'), S.get('j'), S.get('_line', 0)
    if i is None or j is None or 's' not in S:
        return '`s[i][j]` = 左上角 `(0,0)` 到 `(i,j)` 的子矩阵元素和；每算出一个，和 `k` 比一比'
    s, g, k = S['s'], S['grid'], S['k']
    if line == 13:
        return f'`s[0][0] = grid[0][0]` = =={s[i][j]}=='
    if line == 15:
        return f'第 0 行：`s[0][{j}] = s[0][{j - 1}] + grid[0][{j}]` = {s[i][j - 1]} + {g[i][j]} = =={s[i][j]}=='
    if line == 17:
        return f'第 0 列：`s[{i}][0] = s[{i - 1}][0] + grid[{i}][0]` = {s[i - 1][j]} + {g[i][j]} = =={s[i][j]}=='
    if line == 19:
        return (f'`s[{i}][{j}]` = 上 {s[i - 1][j]} + 左 {s[i][j - 1]} − 左上 {s[i - 1][j - 1]} + 自己 {g[i][j]} = =={s[i][j]}==')
    if line in (21, 22):
        v = s[i][j]
        return f'`s[{i}][{j}] = {v}` {"≤" if v <= k else ">"} `k = {k}`' + ('：计入' if v <= k else '：不计')
    return '按行从左到右、从上到下，一格一格算前缀和'


CONFIG = dict(
    num=3070, title='元素和小于等于 k 的子矩阵的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二维前缀和 · 上 + 左 − 左上 + 自己',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1499'],
    code='''
class Solution(object):
    def countSubmatrices(self, grid, k):

        m = len(grid)
        n = len(grid[0])

        s = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        s[i][j] = grid[i][j]
                    else:
                        s[i][j] = s[i][j - 1] + grid[i][j]
                elif j == 0:
                    s[i][j] = s[i - 1][j] + grid[i][j]
                else:
                    s[i][j] = s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1] + grid[i][j]

                if s[i][j] <= k:
                    res += 1

        return res
''',
    call=f'Solution().countSubmatrices({GRID}, {K})',
    expect=6,
    views=[
        dict(type='grid', var='grid', label='grid（黄框 = 当前格 (i,j)）', h=250, cell=76,
             cursors=[('i', 'j if _line >= 10 else None', 'yellow')]),
        dict(type='table', var=_s_view, label='s（前缀和表：蓝 = 上，粉 = 左，橙 = 左上要减掉；绿 = ≤ k 计入，红 = 超过 k）',
             h=270, cell=76, color=_use),
        dict(type='text', fn=_formula, size=26, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'red'), ('res', 'res', 'green')],
    skip=['m = len', 'n = len'],
    captions={
        's = [[0]': '`s[i][j]`：左上角 `(0,0)` 到 `(i,j)` 的子矩阵元素和，先全放 0',
        'res = 0': '`res` 统计 `s[i][j] <= k` 的个数',
        'for i in range': lambda S, B, r: ('所有格子都算完了' if ('i' in B and S.i == B.i)
                                           else '第 `{}` 行'.format(S.i)),
        'for j in range': lambda S, B, r: ('这一行算完了' if ('j' in B and S.j == B.j and S.i == B.i)
                                           else '算 `s[{}][{}]`：右下角是 `({}, {})` 的子矩阵和'.format(S.i, S.j, S.i, S.j)),
        11: lambda S, B, r: ('`i == 0`：第 0 行，没有「上面」可以借用' if S.i == 0
                                      else '`i = {}` 不是第 0 行，先看是不是第 0 列'.format(S.i)),
        12: lambda S, B, r: ('`j == 0`：就是左上角 `(0,0)`，子矩阵只有它自己' if S.j == 0
                                      else '`j = {}`：第 0 行里只能借用左边的前缀和'.format(S.j)),
        's[i][j] = grid[i][j]': '`s[0][0] = grid[0][0]` = =={s[0][0]}==',
        's[i][j] = s[i][j - 1] + grid[i][j]': '只有左边：`s[{i}][{j}]` = `s[{i}][{j-1}]` + `grid[{i}][{j}]` = {s[i][j-1]} + {grid[i][j]} = =={s[i][j]}==',
        16: lambda S, B, r: ('`j == 0`：第 0 列，只能借用上面的前缀和' if S.j == 0
                                        else '`j = {}`：上、左、左上都存在，用完整公式'.format(S.j)),
        's[i][j] = s[i - 1][j] + grid[i][j]': '只有上面：`s[{i}][{j}]` = `s[{i-1}][{j}]` + `grid[{i}][{j}]` = {s[i-1][j]} + {grid[i][j]} = =={s[i][j]}==',
        's[i][j] = s[i - 1][j] + s[i][j - 1]': ('上面 + 左边：「左上」那块被加了两次 → 减一次；再加上自己：'
                                               '{s[i-1][j]} + {s[i][j-1]} − {s[i-1][j-1]} + {grid[i][j]} = =={s[i][j]}=='),
        'if s[i][j] <= k': lambda S, B, r: ('`s[{}][{}] = {} ≤ k = {}`：这个子矩阵合格'.format(S.i, S.j, S.s[S.i][S.j], S.k) if S.s[S.i][S.j] <= S.k
                                            else '`s[{}][{}] = {} > k = {}`：超过 k，不计'.format(S.i, S.j, S.s[S.i][S.j], S.k)),
        'res += 1': '`res` → =={res}==',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='标准二维前缀和：上面 + 左边 − 左上角 + 自己',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['非负整数矩阵 `grid` 和整数 `k`',
                 '数有多少个「包含左上角 `grid[0][0]`」且元素和 `≤ k` 的子矩阵',
                 '示例：`[[7,2,9],[1,5,0],[2,6,6]]`，`k=20` → `6`',
                 '这些子矩阵正好和右下角 `(i,j)` 一一对应'],
        quote='二者相加可以互相填补除nums[i][j]之外的最后一行以及最后一列，但是(i - 1, j - 1)为右下角的子矩阵将被计算两次，因此需要减掉。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s[i][j]`：以 `(i,j)` 为右下角、`(0,0)` 为左上角的子矩阵和',
              '去掉最后一行 `s[i-1][j]` + 去掉最后一列 `s[i][j-1]`：==左上那块算了两遍==',
              '所以减去 `s[i-1][j-1]`，再加上 `grid[i][j]` 自己',
              '第 0 行、第 0 列借不到上面 / 左边，要分开写'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：边界分支别漏；不分支的话 `i-1`、`j-1` 会越界',
                 '代码本身是 Python 3 可运行的写法，原样照搬',
                 '对比灵神：灵神一行行累加列和，超过 k 就 break，空间只要 `O(n)`'],
    ),
)
