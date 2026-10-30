MAT = [[5, 2, 3], [1, 6, 4]]     # 两行互不相同，便于用 index 反查行号
K = 3


def _i(S):
    if 'row' not in S or 'matrix' not in S:
        return None
    i = S['matrix'].index(S['row'])
    if S['_line'] == 5 and len(S['a']) == (i + 1) * len(S['row']):    # for 循环结束的那一步
        return None
    return i


def _j(S):
    ln = S['_line']
    if 7 <= ln <= 10 and 'j' in S and 'row' in S:
        i = S['matrix'].index(S['row'])
        if ln == 7 and len(S['a']) == i * len(S['row']) + S['j'] + 1:   # 这一行扫完的那一步
            return None
        return S['j']
    return None


def _rj(S):
    """s 此刻已经异或到第几列（含）"""
    j = _j(S)
    if j is None:
        return -1
    return j if S['_line'] >= 9 else j - 1


def _gcolor(S, a, b, v):
    i, j = _i(S), _j(S)
    if i is None or j is None:
        return None
    if a <= i and b <= _rj(S):
        return 'blue'
    return None


def _ccolor(S, r, c, v):
    j = _j(S)
    if j is None:
        return None
    if c == j and S['_line'] in (8, 9):
        return 'yellow'
    if c < j or (c == j and S['_line'] >= 9):
        return 'blue'
    return None


def _acolor(S, idx, v):
    if S['_line'] == 10 and idx == len(S['a']) - 1:
        return 'green'
    if S['_line'] in (11, 12) and idx == len(S['a']) - S['k']:
        return 'green' if S['_line'] == 12 else None
    return None


def _text(S):
    if 'col_sum' not in S:
        return '目标值 = 左上角 `(0,0)`、右下角 `(i,j)` 的子矩阵异或和；异或自己等于 0，所以像前缀和一样累积'
    i, j, ln = _i(S), _j(S), S['_line']
    if ln == 11:
        return f"`a` 里一共 `{len(S['a'])}` 个目标值，从小到大排好了"
    if ln == 12:
        return f"第 `k = {S['k']}` 大：倒数第 `{S['k']}` 个"
    if i is None:
        return '所有行都处理完了，目标值都在 `a` 里'
    if j is None:
        return '这一行的右下角都枚举完了' if ln == 7 else '`col_sum[j]`：第 `j` 列、到当前行为止的异或和'
    if ln in (7, 8):
        return f"看 `matrix[{i}][{j}] = {S['matrix'][i][j]}`：先异或进第 `{j}` 列"
    return f"`(0,0)–({i},{j})` 的异或和：`col_sum[0] ^ … ^ col_sum[{j}]` = `{S['s']}`"


def _cap_for_row(S, B, r):
    if 'row' in B and B.row == S.row:
        return '所有行都处理完了'
    return f'第 `{S.matrix.index(S.row)}` 行：`col_sum` 保留着上面各行的列异或和'


def _cap_for_j(S, B, r):
    if 'j' in B and B.j == S.j and B.x == S.x:
        return '这一行扫完了'
    return f'枚举右下角 `({S.matrix.index(S.row)}, {S.j})`，`x = {S.x}`'


CONFIG = dict(
    num=1738, title='找出第 K 大的异或坐标值', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='二维前缀异或 · 列前缀异或和',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1671'],
    code='''
class Solution:
    def kthLargestValue(self, matrix: List[List[int]], k: int) -> int:
        a = []
        col_sum = [0] * len(matrix[0])
        for row in matrix:
            s = 0
            for j, x in enumerate(row):
                col_sum[j] ^= x
                s ^= col_sum[j]
                a.append(s)
        a.sort()
        return a[-k]
''',
    call=f'Solution().kthLargestValue({MAT}, {K})',
    expect=5,
    views=[
        dict(type='text', fn=_text, size=26, h=70),
        dict(type='grid', var='matrix', label='matrix（黄框 = 当前格 (i,j)，蓝 = 已异或进 s 的子矩阵）', cell=96, h=240,
             color=_gcolor, cursors=[(lambda S: _i(S), lambda S: _j(S), 'yellow')]),
        dict(type='array', var='col_sum', label='col_sum[j]：第 j 列到当前行的异或和（黄 = 刚更新）', cell=96, h=150,
             color=lambda S, c, v: _ccolor(S, 0, c, v)),
        dict(type='array', var='a', label='a：每个右下角的目标值（遍历顺序；绿 = 新加入 / 第 k 大）', cell=84, h=150,
             pointers={'len(a) - k if _line == 12 else None': 'green'}, pointer_labels={'len(a) - k if _line == 12 else None': 'a[-k]'},
             color=_acolor),
    ],
    watch=[('j', 'j', 'yellow'), ('x', 'x'), ('s', 's', 'blue'), ('k', 'k', 'green')],
    captions={
        'a = []': '`a` 收集每个坐标 `(i, j)` 的目标值',
        'col_sum = [0]': '`col_sum[j]`：第 `j` 列==当前遍历过的元素==的异或和，初始为 0',
        'for row in matrix': _cap_for_row,
        's = 0': '`s` 从 0 开始：每行从左往右把 `col_sum` 异或进来',
        'for j, x in enumerate(row)': _cap_for_j,
        'col_sum[j] ^= x': lambda S, B, r: f'`col_sum[{S.j}] = {B.col_sum[S.j]} ^ {S.x}` = =={S.col_sum[S.j]}==：第 `{S.j}` 列从第 0 行到第 `{_i(S)}` 行的异或和',
        's ^= col_sum[j]': lambda S, B, r: f'`s = {B.s} ^ {S.col_sum[S.j]}` = =={S.s}==：`col_sum[0] ^ … ^ col_sum[{S.j}]` 正好是 `(0,0)–({_i(S)},{S.j})` 的异或和',
        'a.append(s)': lambda S, B, r: f'`({_i(S)},{S.j})` 的目标值 =={S.s}== 放进 `a`，现在共 `{len(S.a)}` 个',
        'a.sort()': lambda S, B, r: f'从小到大排序：`{S.a}`（异或没有单调性，必须把所有目标值算出来再排）',
        'return a[-k]': '第 `k = {k}` 大 = 倒数第 `{k}` 个 `a[-{k}]` = =={ret}==（重复的值各算一个）',
    },
    cards=dict(
        one_liner='异或自己等于 0，二维前缀和那套直接用；算完所有目标值再排序',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`（快速选择可到 `O(mn)` 时间）',
        problem=['矩阵 `matrix`，坐标 `(a, b)` 的==目标值==是 `(0,0)` 到 `(a,b)` 所有元素的异或',
                 '求所有坐标目标值里==第 `k` 大==的那个（`k` 从 1 开始）',
                 '示例：`[[5,2],[1,6]]`，`k = 1` → `7`',
                 '本视频：`[[5,2,3],[1,6,4]]`，`k = 3` → `5`'],
        quote='遍历 matrix 的同时，计算 colSum[j]，表示第 j 列的当前遍历过的元素的异或和。……这也可以一边遍历 matrix 一边计算。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`col_sum[j]`：第 `j` 列到当前行的异或和',
              '`s` 把本行 `col_sum[0..j]` 异或起来，就是 `(0,0)–(i,j)` 的异或和',
              '目标值全部放进 `a`，排序后取 `a[-k]`'],
        summary=['时间 `O(mn log(mn))`，空间 `O(mn)`；用快速选择可降到 `O(mn)` 时间',
                 '方法一二维前缀异或和：`s[i][j]` 被抵消了，==要再异或一次==',
                 '异或没有单调性：不能边算边剪枝，只能全部算出来再找第 k 大',
                 '易错：第 `k` 大是 `a[-k]`，不是 `a[k]`；重复值各算一个'],
    ),
)
