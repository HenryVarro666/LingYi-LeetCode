S_ = 'aab'
P_ = 'a*b'
DEP = {  # 行号 -> 依赖的格子（相对 i, j）及颜色
    14: [((0, -2), 'cyan')],
    21: [((-1, -1), 'purple')],
    23: [((0, -2), 'cyan')],
    24: [((0, -2), 'cyan')],
    26: [((0, -1), 'blue'), ((-1, 0), 'pink'), ((-1, -1), 'purple')],
    27: [((0, -1), 'blue'), ((-1, 0), 'pink'), ((-1, -1), 'purple')],
    29: [((-1, -1), 'purple')],
}


def _tf(b):
    return 'T' if b else 'F'


def _table(E):
    f = E.get('f')
    if f is None:
        return None
    n, m = len(E['s']), len(E['p'])
    return [row[:m + 1] for row in f[:n + 1]]


def _color(E, r, c, v):
    line = E.get('_line')
    if 'i' in E and 'j' in E and line in range(10, 32):
        i, j = E['i'], E['j']
        if (r, c) == (i, j):
            return 'yellow'
        for (di, dj), col in DEP.get(line, []):
            if (r, c) == (i + di, j + dj):
                return col
    return 'green' if v is True else None


def _text(E):
    line = E.get('_line')
    if line in (23, 24, 26, 27) and 'j' in E:
        return '`*` 表示前一个字符出现 ==0 次== `f[i][j-2]` / ==1 次== `f[i][j-1]` / ==2 次== `f[i-1][j-1]` / ==多次== `f[i-1][j]`'
    return '`f[i][j]`：`s` 的==前 i 个==字符与 `p` 的==前 j 个==字符能否匹配'


def _cap_for_i(E, B, ret):
    if 'i' in B and B.i == E.i:
        return '全部算完'
    if E.i == 0:
        return '第 0 行：`s` 是==空串==，只有 `x*x*…` 这样的 `p` 才能匹配它'
    return f'第 `i = {E.i}` 行：`s` 的前 {E.i} 个字符 `"{E.s[:E.i]}"`'


def _cap_true0(E, B, ret):
    return '`f[0][0] = True`：两边都是空串，能匹配'


def _cap_star0(E, B, ret):
    j = E.j
    return f'`p[{j - 1}]` 是 `*`，且 `f[0][{j - 2}]` 能匹配空串 → `*` 表示 `p[{j - 2}]` 出现 0 次 → `f[0][{j}] = True`'


def _cap_false0(E, B, ret):
    j = E.j
    if E.p[j - 1] != '*':
        return f'`p[{j - 1}] = "{E.p[j - 1]}"` 不是 `*`：==出现了字符又没有星号兜底==，匹配不了空串 → `F`'
    return f'`f[0][{j - 2}] = F` → `f[0][{j}] = F`'


def _cap_j0(E, B, ret):
    return f'`j = 0`：`p` 是空串，`s` 不空 → `f[{E.i}][0] = False`'


def _cap_dot(E, B, ret):
    i, j = E.i, E.j
    return f'`p[{j - 1}] = "."` 一定能匹配 `s[{i - 1}]` → `f[{i}][{j}] = f[{i - 1}][{j - 1}]` = {_tf(E.f[i][j])}'


def _cap_star_if(E, B, ret):
    i, j = E.i, E.j
    if j >= 2 and E.f[i][j - 2]:
        return f'`*` 表示 `p[{j - 2}]` 出现 ==0 次==：`f[{i}][{j - 2}] = T` → 成立'
    return f'`*` 表示出现 0 次：`f[{i}][{j - 2}] = F`，不行 → 再看能否出现 1 次及以上'


def _cap_star_char(E, B, ret):
    i, j, p, s = E.i, E.j, E.p, E.s
    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
        return f'`p[{j - 2}] = "{p[j - 2]}"` 能匹配 `s[{i - 1}] = "{s[i - 1]}"` → `*` 可以表示它出现 1 次、2 次或多次'
    return f'`p[{j - 2}] = "{p[j - 2]}"` ≠ `s[{i - 1}] = "{s[i - 1]}"` → 只能出现 0 次，而那也不行 → `F`'


def _cap_star_or(E, B, ret):
    i, j, f = E.i, E.j, E.f
    return (f'1 次 `f[{i}][{j - 1}]`={_tf(f[i][j - 1])}，2 次 `f[{i - 1}][{j - 1}]`={_tf(f[i - 1][j - 1])}，'
            f'多次 `f[{i - 1}][{j}]`={_tf(f[i - 1][j])} → `f[{i}][{j}]` = =={_tf(f[i][j])}==')


def _cap_same(E, B, ret):
    i, j = E.i, E.j
    return f'`p[{j - 1}] = s[{i - 1}] = "{E.s[i - 1]}"` → `f[{i}][{j}] = f[{i - 1}][{j - 1}]` = =={_tf(E.f[i][j])}=='


def _cap_diff(E, B, ret):
    i, j = E.i, E.j
    return f'`p[{j - 1}] = "{E.p[j - 1]}"` ≠ `s[{i - 1}] = "{E.s[i - 1]}"` → `F`'


CONFIG = dict(
    num=10, title='正则表达式匹配', difficulty='Hard', category='多维动态规划',
    author='yiduobo', technique='前缀 DP：分情况讨论 p[j-1]',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def isMatch(self, s, p):
        len_s = len(s)
        len_p = len(p)

        f = [[False] * (len_p + 2) for index in range(len_s +2)]

        for i in range(len_s + 1):
            for j in range(len_p + 1):
                if i == 0:
                    if j == 0:
                        f[i][j] = True
                    elif p[j - 1] == '*' and f[i][j - 2]:
                        f[i][j] = True
                    else:
                        f[i][j] = False
                else:
                    if j == 0:
                        f[i][j] = False
                    elif p[j - 1] == '.':
                        f[i][j] = f[i - 1][j - 1]
                    elif p[j - 1] == '*':
                        if j >= 2 and f[i][j - 2]:
                            f[i][j] = True
                            continue
                        if p[j - 2] == '.' or p[j -2] == s[i - 1]:
                            f[i][j] = f[i][j] or f[i][j - 1] or f[i - 1][j] or f[i - 1][j - 1]
                    elif p[j - 1] == s[i - 1]:
                        f[i][j] = f[i - 1][j - 1]
                    else:
                        f[i][j] = False

        return f[len_s][len_p]
''',
    call=f'Solution().isMatch({S_!r}, {P_!r})',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=60, size=26),
        dict(type='table', var=_table, label='f[i][j]（青 = 0 次，蓝 = 1 次，紫 = 2 次 / 左上，粉 = 多次）',
             rows=lambda E: ['∅'] + list(E['s']), cols=lambda E: ['∅'] + list(E['p']), cell=110, h=560, color=_color),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('f[len_s][len_p]', 'f[len_s][len_p]', 'green')],
    skip=['len_s = len', 'len_p = len', 'f = [[False]', 'for j in range', 10, 11, 13, 18, 20, 22, 25, 28],
    captions={
        'for i in range': _cap_for_i,
        12: _cap_true0,
        14: _cap_star0,
        16: _cap_false0,
        19: _cap_j0,
        21: _cap_dot,
        23: _cap_star_if,
        24: lambda E, B, ret: f'`f[{E.i}][{E.j}] = True`，`continue`',
        26: _cap_star_char,
        27: _cap_star_or,
        29: _cap_same,
        31: _cap_diff,
        'return f[len_s][len_p]': '`f[len_s][len_p]` = `f[{len_s}][{len_p}]` 就是答案 → =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j]：s 前 i 个与 p 前 j 个能否匹配，按 p[j-1] 是什么分情况',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['实现支持 `.` 和 `*` 的正则匹配：`.` 匹配任意单个字符',
                 '`*` 匹配零个或多个==前面那一个元素==；要匹配==整个== `s`',
                 '示例：`"aa"`、`"a"` → `false`；`"aa"`、`"a*"` → `true`',
                 '演示：`s = "aab"`，`p = "a*b"` → `true`'],
        quote='拿到题的第一想法是做一个自动机，但是忘了怎么弄了，所以还是老老实实用dp来做。==f[i][j]表示s中的前i个字符与p中的前j个字符是否能匹配上==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p[j-1]` 是 `.` 或等于 `s[i-1]`：`f[i][j] = f[i-1][j-1]`',
              '`p[j-1]` 是 `*`：`p[j-2]` 出现 0 次看 `f[i][j-2]`',
              '若 `p[j-2]` 能匹配 `s[i-1]`：1 次看 `f[i][j-1]`，2 次看 `f[i-1][j-1]`',
              '多次：从 `s[i-2]` 起就靠 `*` 匹配了 → 看 `f[i-1][j]`',
              '`i = 0` 行：只有 `*` 能让 `p` 匹配空串'],
        summary=['时间 `O(nm)`，空间 `O(nm)`；原文：两重循环，平方的复杂度',
                 '易错：第 0 行要单独处理——`a*b*` 也能匹配空串',
                 '`f` 多开了一行一列（`+2`），代码里没用到，只是防越界',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神用后缀定义 `dfs(i, j)`，`*` 只分「零个 / 先匹配一个」两种'],
    ),
)
