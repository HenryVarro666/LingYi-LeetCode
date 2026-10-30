S1, S2, S3 = 'aab', 'dbb', 'aadbbb'

CODE = '''
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        n, m = len(s1), len(s2)
        if n + m != len(s3):
            return False

        f = [[False] * (m + 1) for _ in range(n + 1)]
        f[0][0] = True
        for j, y in enumerate(s2):
            f[0][j + 1] = y == s3[j] and f[0][j]
        for i, x in enumerate(s1):
            f[i + 1][0] = x == s3[i] and f[i][0]
            for j, y in enumerate(s2):
                f[i + 1][j + 1] = x == s3[i + j + 1] and f[i][j + 1] or \\
                                  y == s3[i + j + 1] and f[i + 1][j]
        return f[n][m]
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, s in enumerate(_LINES) if sub in s][0]


L_ROW0 = _ln('f[0][j + 1] =')
L_COL0 = _ln('f[i + 1][0] =')
L_CELL = _ln('f[i + 1][j + 1] =')
L_CELL2 = L_CELL + 1


def _where(S):
    """当前这一步在算哪个格子：('row0', j) / ('col0', i) / ('cell', i, j) / None"""
    ln = S.get('_line')
    if ln == L_ROW0:
        return ('row0', S['j'])
    if ln == L_COL0:
        return ('col0', S['i'])
    if ln in (L_CELL, L_CELL2):
        return ('cell', S['i'], S['j'])
    return None


def _cur(S):
    w = _where(S)
    if w is None:
        return None, None
    if w[0] == 'row0':
        return 0, w[1] + 1
    if w[0] == 'col0':
        return w[1] + 1, 0
    return w[1] + 1, w[2] + 1


def _k3(S):
    """s3 里正在匹配的下标"""
    w = _where(S)
    if w is None:
        return None
    if w[0] in ('row0', 'col0'):
        return w[1]
    return w[1] + w[2] + 1


def _color(S, r, c, v):
    w = _where(S)
    if w is not None:
        if w[0] == 'row0' and (r, c) == (0, w[1]):
            return 'pink'
        if w[0] == 'col0' and (r, c) == (w[1], 0):
            return 'blue'
        if w[0] == 'cell':
            i, j = w[1], w[2]
            if (r, c) == (i, j + 1):
                return 'blue'                        # 上：s3 的这个字母来自 s1
            if (r, c) == (i + 1, j):
                return 'pink'                        # 左：来自 s2
    return 'green' if v is True else None


def _formula(S):
    w = _where(S)
    f = S.get('f')
    if w is None or f is None:
        return '`f[i+1][j+1]`：`s3` 前 `i+j+2` 个字母能否由 `s1` 前 `i+1` 个和 `s2` 前 `j+1` 个交错组成'
    if w[0] == 'row0':
        j = w[1]
        return f'第 0 行（不用 s1）：`s2[{j}]={S2[j]}` vs `s3[{j}]={S3[j]}`，且左边 `{f[0][j]}` → =={f[0][j + 1]}=='
    if w[0] == 'col0':
        i = w[1]
        return f'第 0 列（不用 s2）：`s1[{i}]={S1[i]}` vs `s3[{i}]={S3[i]}`，且上边 `{f[i][0]}` → =={f[i + 1][0]}=='
    i, j = w[1], w[2]
    k = i + j + 1
    a = S1[i] == S3[k] and f[i][j + 1]
    b = S2[j] == S3[k] and f[i + 1][j]
    return (f'`s3[{k}]={S3[k]}`：来自 s1 `{S1[i]}`·上 `{f[i][j + 1]}` → `{a}`；'
            f'来自 s2 `{S2[j]}`·左 `{f[i + 1][j]}` → `{b}`')


def _cap_row0(S, B, ret):
    j = S.j
    ok = S.f[0][j + 1]
    head = '第 0 行：s1 一个字母都不用，`s3` 前缀只能==全部来自 s2==。' if j == 0 else ''
    if ok:
        return head + f'`s2[{j}] = s3[{j}] = {S2[j]}` 且左边为 True → `f[0][{j + 1}] = True`'
    if S2[j] != S3[j]:
        return head + f'`s2[{j}] = {S2[j]}` ≠ `s3[{j}] = {S3[j]}` → `f[0][{j + 1}] = False`'
    return head + f'左边已经是 False → `f[0][{j + 1}] = False`'


def _cap_col0(S, B, ret):
    i = S.i
    ok = S.f[i + 1][0]
    head = '第 0 列：s2 一个字母都不用，`s3` 前缀只能==全部来自 s1==。' if i == 0 else f'外层换到 `x = s1[{i}] = {S1[i]}`。'
    if ok:
        return head + f'`s1[{i}] = s3[{i}] = {S1[i]}` 且上边为 True → `True`'
    if S1[i] != S3[i]:
        return head + f'`s1[{i}] = {S1[i]}` ≠ `s3[{i}] = {S3[i]}` → `False`'
    return head + '上边已经是 False → `False`'


_pending = set()   # 来自 s1 不成立时，这一行会触发两次（先算 or 左边，再算右边并赋值）


def _cap_cell(S, B, ret):
    i, j, f = S.i, S.j, S.f
    k = i + j + 1
    a = S1[i] == S3[k] and f[i][j + 1]
    if a:
        return (f'`s3[{k}] = {S3[k]}` 可以是 s1 的最后一个字母 `s1[{i}]`，且==上边== `f[{i}][{j + 1}]` 为 True'
                f' → `or` 短路，`f[{i + 1}][{j + 1}] = True`')
    if (i, j) not in _pending:
        _pending.add((i, j))
        why = (f'`s1[{i}] = {S1[i]}` ≠ `s3[{k}] = {S3[k]}`' if S1[i] != S3[k]
               else f'字母相同，但上边 `f[{i}][{j + 1}]` 是 False')
        return f'来自 s1？{why} → 不行，再看 `or` 右边：来自 s2'
    _pending.discard((i, j))
    if f[i + 1][j + 1]:
        return f'来自 s2：`s2[{j}] = s3[{k}] = {S3[k]}`，且==左边== `f[{i + 1}][{j}]` 为 True → `f[{i + 1}][{j + 1}] = True`'
    why = (f'`s2[{j}] = {S2[j]}` ≠ `s3[{k}] = {S3[k]}`' if S2[j] != S3[k]
           else f'字母相同，但左边 `f[{i + 1}][{j}]` 是 False')
    return f'来自 s2？{why} → 两条路都不通，`f[{i + 1}][{j + 1}] = False`'


CONFIG = dict(
    num=97, title='交错字符串', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='记忆化搜索 → 1:1 翻译成递推',
    tags=['字节30天', '面试经典150'],
    code=CODE,
    call=f'Solution().isInterleave({S1!r}, {S2!r}, {S3!r})',
    expect=True,
    skip=['for j, y in enumerate(s2)', 'for i, x in enumerate(s1)', 'f = [[False]', L_CELL2],
    views=[
        dict(type='text', fn=_formula, h=64, size=26),
        dict(type='string', var='s3', label='s3（黄框 = 正在决定来源的字母）', cell=72,
             color=lambda S, i, v: 'yellow' if i == _k3(S) else None,
             dim=lambda S, i, v: _k3(S) is not None and i > _k3(S)),
        dict(type='table', var='f', label='f（行头 = s1 的字母，列头 = s2 的字母；蓝 = 上（来自 s1），粉 = 左（来自 s2））',
             rows=lambda S: ['∅'] + list(S1), cols=lambda S: ['∅'] + list(S2),
             cursors=[(lambda S: _cur(S)[0], lambda S: _cur(S)[1], 'yellow')], color=_color, cell=96, h=440),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('f[n][m]', 'f[n][m]', 'green')],
    captions={
        'n, m = len': '`n = {n}`，`m = {m}`',
        'if n + m != len(s3)': '`{n} + {m} = {len(s3)}`：长度对得上（==对不上直接返回 False==）',
        'f[0][0] = True': '`f[0][0] = True`：三个空串，翻译自递归边界 `dfs(-1, -1) = True`',
        L_ROW0: _cap_row0,
        L_COL0: _cap_col0,
        L_CELL: _cap_cell,
        'return f[n][m]': '`f[n][m]` 翻译自递归入口 `dfs(n-1, m-1)`：返回 =={ret}==',
    },
    cards=dict(
        one_liner='从右往左看 s3 的最后一个字母：它来自 s1 还是 s2？',
        complexity='时间 `O(nm)`，空间 `O(nm)`（可优化到 `O(m)`）',
        problem=['判断 `s3` 能否由 `s1` 和 `s2` ==交错==组成（保持各自字母的相对顺序）',
                 '示例：`s1 = "aabcc"`，`s2 = "dbbca"`，`s3 = "aadbbcbcac"` → `true`',
                 '本视频：`s1 = "aab"`，`s2 = "dbb"`，`s3 = "aadbbb"` → `true`'],
        quote='从右往左思考，如果 s3 的最后一个字母 c 来自 s1 的最后一个字母，那么去掉 s1 和 s3 的最后一个字母……==这些问题都是和原问题相似的、规模更小的子问题==。',
        quote_src='—— 灵茶山艾府题解（一、寻找子问题）',
        idea=['`dfs(i,j)`：`s3[:i+j+2]` 能否由 `s1[:i+1]` 和 `s2[:j+1]` 交错组成',
              '`s3[i+j+1]` 来自 `s1[i]` → `dfs(i-1,j)`；来自 `s2[j]` → `dfs(i,j-1)`，==有一个成立即可==',
              '边界 `dfs(-1,-1) = True`；先判断 `n + m == len(s3)`',
              '1:1 翻译成递推：`f[i+1][j+1]` 就是 `dfs(i,j)`，第 0 行 / 列单独算'],
        after=[dict(heading='记忆化搜索 → 递推：逐项对照', lines=[
            '`dfs(i, j)` ↔ `f[i+1][j+1]`（下标整体 +1）',
            '`dfs(-1, -1) = True` ↔ `f[0][0] = True`',
            '来自 s1：`dfs(i-1, j)` ↔ 上 `f[i][j+1]`；来自 s2：`dfs(i, j-1)` ↔ 左 `f[i+1][j]`',
            '递归入口 `dfs(n-1, m-1)` ↔ 答案 `f[n][m]`'])],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '易错：别忘了先判断 `n + m == len(s3)`，否则下标会越界',
                 '易错：比较的是 `s3[i+j+1]`，写入的是 `f[i+1][j+1]`',
                 '`|n - m| <= 1` 是多余条件：交替涂色，段数差自然不超过 1',
                 '空间优化：一个长为 `m+1` 的数组，类似完全背包==正序遍历=='],
    ),
)
