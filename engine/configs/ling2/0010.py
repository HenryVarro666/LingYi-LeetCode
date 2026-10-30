S_ = 'aab'
P_ = 'c*a*b'


def _tf(b):
    return 'T' if b else 'F'


def _live(E):
    return E.get('_line') in (11, 12, 13, 15) and 'j' in E and 'i' in E


def _color(E, r, c, v):
    if _live(E):
        i, j, p, m = E['i'], E['j'], E['p'], E['m']
        star = j + 1 < m and p[j + 1] == '*'
        if (r, c) == (i, j):
            return 'yellow'
        if star and (r, c) == (i, j + 2):
            return 'blue'
        if star and (r, c) == (i + 1, j):
            return 'pink'
        if not star and (r, c) == (i + 1, j + 1):
            return 'purple'
    if E.get('_line') == 17 and (r, c) == (0, 0):
        return 'yellow'
    return 'green' if v is True else None


def _dim_star_cols(E):
    return None


def _text(E):
    if not _live(E):
        return '`f[i][j]`：`s` 的后缀 `s[i:]` 能否与 `p` 的后缀 `p[j:]` 匹配'
    i, j, s, p, n, m, f = E['i'], E['j'], E['s'], E['p'], E['n'], E['m'], E['f']
    star = j + 1 < m and p[j + 1] == '*'
    if star:
        return f'`{p[j]}*` 是整体：匹配零个 `f[{i}][{j + 2}]` 或 匹配一个 `f[{i + 1}][{j}]`' if i < n else \
               f'`{p[j]}*` 是整体：s 已空，只能匹配零个 → `f[{i}][{j + 2}]`'
    return f'普通字符 `{p[j]}`：`s[{i}]` 与它匹配，且 `f[{i + 1}][{j + 1}]`'


def _cap_ism(E, B, ret):
    i, j, s, p, n = E.i, E.j, E.s, E.p, E.n
    if i >= n:
        return f'`i = {n}`：`s` 的后缀是空串，`is_match = False`'
    if p[j] == '.':
        return f'`p[{j}] = "."` 匹配任意字符 → `is_match = True`'
    return f'`s[{i}] = "{s[i]}"`，`p[{j}] = "{p[j]}"` → `is_match = {E.is_match}`'


def _cap_star(E, B, ret):
    j, p, m = E.j, E.p, E.m
    if j + 1 < m and p[j + 1] == '*':
        return f'`p[{j + 1}] = "*"`：`p[{j}]p[{j + 1}] = "{p[j]}*"` 是一个==整体=='
    return f'`p[{j}] = "{p[j]}"` 后面不是 `*` → 单个字符匹配'


def _cap_f_star(E, B, ret):
    i, j, f = E.i, E.j, E.f
    a = f[i][j + 2]
    b = f[i + 1][j] if i + 1 < len(f) else False
    pre = f'`{E.p[j]}*` 是整体。'
    return (pre + f'`f[{i}][{j}]` = 零个 `f[{i}][{j + 2}]`={_tf(a)} 或 (`is_match`={_tf(E.is_match)} 且 一个 `f[{i + 1}][{j}]`={_tf(b)})'
            f' → =={_tf(f[i][j])}==') if i + 1 < len(f) else \
        pre + f'`s` 已空，只能匹配零个：`f[{i}][{j}]` = `f[{i}][{j + 2}]` = =={_tf(f[i][j])}=='


def _cap_f_one(E, B, ret):
    i, j, f = E.i, E.j, E.f
    if i + 1 >= len(f):
        return f'`{E.p[j]}` 后面不是 `*`，但 `s` 已空 → `f[{i}][{j}]` = ==F=='
    return f'单个字符：`f[{i}][{j}]` = `is_match`={_tf(E.is_match)} 且 `f[{i + 1}][{j + 1}]`={_tf(f[i + 1][j + 1])} → =={_tf(f[i][j])}=='


CONFIG = dict(
    num=10, title='正则表达式匹配', difficulty='Hard', category='多维动态规划',
    author='灵茶山艾府', technique='记忆化搜索 1:1 翻译成递推（后缀 DP）',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        n, m = len(s), len(p)
        f = [[False] * (m + 1) for _ in range(n + 1)]
        f[n][m] = True

        for i in range(n, -1, -1):
            for j in range(m - 1, -1, -1):
                if p[j] == '*':
                    continue
                is_match = i < n and (p[j] == '.' or p[j] == s[i])
                if j + 1 < m and p[j + 1] == '*':
                    f[i][j] = f[i][j + 2] or is_match and f[i + 1][j]
                else:
                    f[i][j] = is_match and f[i + 1][j + 1]

        return f[0][0]
''',
    call=f'Solution().isMatch({S_!r}, {P_!r})',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='table', var='f', label='f[i][j]（行 = s 的后缀起点 i，列 = p 的后缀起点 j；蓝 = 零个，粉 = 一个，紫 = 单字符）',
             rows=lambda E: [f'{k}:{E["s"][k]}' if k < len(E['s']) else f'{k}:∅' for k in range(len(E['s']) + 1)],
             cols=lambda E: [f'{E["p"][k]}' if k < len(E['p']) else '∅' for k in range(len(E['p']) + 1)],
             cell=96, h=560, color=_color),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('is_match', 'is_match'), ('f[0][0]', 'f[0][0]', 'green')],
    skip=['n, m = len', 'for j in range', "if p[j] == '*'", 'continue', 'f = [[False]', "if j + 1 < m and p[j + 1] == '*'"],
    captions={
        'f[n][m] = True': '`f[{n}][{m}] = True`：两个空串匹配（翻译自递归边界 `dfs(n, m) = true`）；其余先填 `False`',
        'for i in range': lambda E, B, ret: (f'`f[i]` 依赖 `f[i+1]` → `i` ==倒序==：现在算第 `i = {E.i}` 行（后缀 `"{E.s[E.i:]}"`）；`*` 列跳过'
                                             if 'i' not in B or B.i != E.i else '所有状态都算完了'),
        'is_match = ': _cap_ism,
        "if j + 1 < m and p[j + 1] == '*'": _cap_star,
        'f[i][j] = f[i][j + 2] or': _cap_f_star,
        'f[i][j] = is_match and': _cap_f_one,
        'return f[0][0]': '答案 `f[0][0]`（翻译自递归入口 `dfs(0, 0)`）= =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='p[j+1] 是 * 时，p[j] 和 * 是一个整体：匹配零个，或先匹配一个',
        complexity='时间 `O(nm)`，空间 `O(nm)`（可优化到 `O(m)`）',
        problem=['实现支持 `.` 和 `*` 的正则匹配：`.` 匹配任意单个字符',
                 '`*` 匹配零个或多个==前面那一个元素==；要匹配==整个== `s`',
                 '示例：`"aa"`、`"a"` → `false`；`"aa"`、`"a*"` → `true`',
                 '`"ab"`、`".*"` → `true`（`.*` 匹配任意多个任意字符）',
                 '演示：`s = "aab"`，`p = "c*a*b"` → `true`（`c*` 匹配零个，`a*` 匹配 `aa`）'],
        quote='如果 p[1] = *，那么 p[0] 和 p[1] 就是一个==整体==……我们可以先匹配一个字符……至于 s[1] 是否要与 p[0] 和 p[1] 匹配，那是下一步要做的事情（==这类似完全背包==）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, j)`：`s[i:]` 能否与 `p[j:]` 匹配',
              '`p[j+1] ≠ *`：`isMatch(i, j) ∧ dfs(i+1, j+1)`',
              '`p[j+1] = *`：`dfs(i, j+2) ∨ (isMatch(i, j) ∧ dfs(i+1, j))`',
              '1:1 翻译成递推：`f[i][j]` 依赖下标更大的状态 → `i`、`j` ==都倒序=='],
        after=[dict(heading='灵神的三步走', lines=[
            '① 记忆化搜索：`dfs(i, j)` + `@cache`，边界 `dfs(n, m) = true`',
            '② 1:1 翻译成递推（本视频）：`f[i][j]` 就是 `dfs(i, j)`',
            '③ 空间优化：`f[i]` 只依赖 `f[i+1]`，用一个数组 + `pre` 变量，空间 `O(m)`',
        ])],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '易错：不能把 `i = n` 当递归边界：`s` 空了，`p` 剩下的 `c*d*` 仍可匹配空串',
                 '易错：`is_match` 要先判断 `i < n`，否则越界',
                 '`*` 所在的列直接跳过：它总是和前一个字符一起处理'],
    ),
)
