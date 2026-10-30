M = [[2, -5, 3], [-4, 1, 6], [7, -3, 9]]


def _pos(S):
    """(i, j) of the element being processed; abs values inside each row are distinct"""
    ln = S.get('_line')
    row, x = S.get('row'), S.get('x')
    if row is None or ln is None or ln < 5 or ln > 11:
        return None
    i = M.index(list(row))
    if ln == 5 or x is None:
        return (i, None)
    try:
        return (i, [abs(v) for v in row].index(abs(x)))
    except ValueError:
        return (i, None)


def _done(S, r, c):
    ln = S.get('_line') or 0
    if ln >= 13:
        return True
    p = _pos(S)
    if p is None:
        return False
    i, j = p
    if j is None:
        return r < i
    if (r, c) < (i, j):
        return True
    # current cell counts as done once total already includes it (also covers the end-of-row L6 step)
    pre = sum(abs(M[a][b]) for a in range(3) for b in range(3) if (a, b) <= (i, j))
    return (r, c) == (i, j) and S.get('total') == pre


def _mn_cell(S, r, c):
    return (S.get('_line') or 0) >= 13 and abs(M[r][c]) == S.get('mn')


def _color(S, r, c, v):
    if _mn_cell(S, r, c):
        return 'orange'
    if _done(S, r, c):
        return 'green'
    if v < 0:
        return 'pink'
    return None


def _text(S, B):
    ln = S.get('_line') or 0
    terms = [str(abs(M[r][c])) for r in range(3) for c in range(3) if _done(S, r, c)]
    if ln == 14:
        return f"奇数个负数 → 绝对值最小的 =={S['mn']}== 必须带负号：`{B['total']} − 2 × {S['mn']}` = =={S['total']}=="
    if ln == 13:
        odd = '奇数 → 必然剩下一个负数' if S['neg_cnt'] % 2 else '偶数 → 全部可以变成非负数'
        return f"负数个数 `neg_cnt = {S['neg_cnt']}`：{odd}"
    if not terms:
        return '先把所有数当成==绝对值==累加，同时数负数个数、记最小绝对值'
    return f"`total` = {' + '.join(terms)} = =={sum(int(t) for t in terms)}=="


def _cap_row(S, B, ret):
    if S.get('row') is not None and (B.get('row') is None or list(S['row']) != list(B['row'])):
        return f"进入第 {M.index(list(S['row']))} 行 `{list(S['row'])}`"
    return '所有行遍历完毕'


def _cap_x(S, B, ret):
    if 'x' in B and S['x'] == B['x']:
        return '这一行遍历完了'
    p = _pos(S)
    return f"取出 `matrix[{p[0]}][{p[1]}]`：`x = {S['x']}`"


def _cap_if(S, B, ret):
    x = S['x']
    if x < 0:
        return f'`x = {x} < 0` → 负数：计数，再取绝对值'
    return f'`x = {x}` 不是负数 → 直接累加'


CONFIG = dict(
    num=1975, title='最大方阵和', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='脑筋急转弯 + 分类讨论',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        total = neg_cnt = 0
        mn = inf
        for row in matrix:
            for x in row:
                if x < 0:
                    neg_cnt += 1
                    x = -x  # 先把负数都变成正数
                mn = min(mn, x)
                total += x

        if neg_cnt % 2:
            total -= mn * 2  # 给绝对值最小的数添加负号
        return total
''',
    call=f'Solution().maxMatrixSum({M})',
    expect=38,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='grid', var='matrix', label='matrix（粉 = 负数，绿 = 已按绝对值累加，橙 = 最小绝对值，黄框 = 当前 x）',
             cursors=[(lambda S: (_pos(S) or (None, None))[0], lambda S: (_pos(S) or (None, None))[1], 'yellow', 'x')],
             color=_color, cell=120, h=440),
    ],
    watch=[('x', 'x', 'yellow'), ('neg_cnt', 'neg_cnt', 'pink'), ('mn', 'mn', 'orange'), ('total', 'total', 'green')],
    captions={
        'total = neg_cnt = 0': '`total` 累加==绝对值==，`neg_cnt` 数负数个数',
        'mn = inf': '`mn` 记录所有数的==最小绝对值==（最后可能要给它添负号）',
        'for row in matrix': _cap_row,
        'for x in row': _cap_x,
        'if x < 0': _cap_if,
        'neg_cnt += 1': '负数个数 → `{neg_cnt}`：每次操作改两个数的符号，==负数个数的奇偶性不变==',
        'x = -x': '先把负数都变成正数：`x` = {x}（负号最后统一结算）',
        'mn = min': '`mn = min({B.mn}, {x})` = {mn}',
        'total += x': '`total += {x}` → `{total}`',
        'if neg_cnt % 2': lambda S, B, ret: (f'`neg_cnt = {S.neg_cnt}` 是==奇数== → 最终必然剩下奇数个负数，剩一个最优'
                                              if S.neg_cnt % 2 else
                                              f'`neg_cnt = {S.neg_cnt}` 是偶数 → 所有数都能变成非负数'),
        'total -= mn * 2': '给绝对值最小的数添加负号：先加过 `{mn}`，要改成 `−{mn}`，所以减 `2 × {mn}` → =={total}==',
        'return total': '最大方阵和 = =={ret}==',
    },
    cards=dict(
        one_liner='负号能两两抵消：只看负数个数的奇偶性',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['`n × n` 方阵，每次把==相邻==两个数同时乘以 `-1`，可操作任意次',
                 '求操作后方阵元素和的==最大值==',
                 '示例：`[[1,2,3],[-1,-2,-3],[1,2,3]]` → `16`',
                 '本视频：`[[2,-5,3],[-4,1,6],[7,-3,9]]` → `38`'],
        before=[dict(heading='脑筋急转弯：任意两个数都能一起变号', chapter='② 思路', lines=[
            '一行里的 `a, b, c`：先翻 `(a, b)`，再翻 `(b, c)`',
            '`b` 被翻了两次符号不变，效果等于==只翻了 `a` 和 `c`==',
            '沿着一条路径重复这样做，任意两个格子都能同时变号',
        ])],
        quote='虽然题目规定我们只能操作相邻的元素，但我们可以通过多次操作，把任意两个元素都乘以 −1。每次操作，恰好改变两个数的正负号。',
        quote_src='—— 灵茶山艾府题解',
        idea_heading='分类讨论',
        idea=['偶数个负数 → 可以把所有数都变成非负数',
              '奇数个负数且没有 0 → 剩一个负数最优，给==绝对值最小==的数',
              '奇数个负数且有 0 → 拿 0 抵掉最后一个负号；代码无需特判，此时 `mn = 0`'],
        summary=['时间 `O(n²)`，空间 `O(1)`：只遍历一遍',
                 '关键不变量：负数个数的==奇偶性==不会因操作改变',
                 '易错：奇数时减的是 `2 × mn`，因为 `mn` 已经被加进 `total`',
                 '有 0 时 `mn = 0`，`total` 不受影响，==无需特判==',
                 '`mn` 取的是绝对值最小：它可能本来是正数（本例的 1）'],
    ),
)
