S0 = '())'


def _fmt_set(x):
    if x is None:
        return '·'
    return '{' + ', '.join(repr(t) for t in sorted(x)) + '}'


def _fmap(S):
    f = S.get('f')
    if f is None:
        return None
    out = {}
    for l in range(len(f)):
        for r in range(l, len(f)):
            if f[l][r] is not None:
                out[f'f[{l}][{r}]'] = _fmt_set(f[l][r])
    return out


def _seg(S):
    l, r = S.get('left'), S.get('right')
    if l is None:
        return ''
    return f"当前区间 `s[{l}..{r}] = {S0[l:r + 1]!r}`"


def _cur(S, B, ret):
    return f'`s[{S.left}..{S.right}] = {S0[S.left:S.right + 1]!r}`'


def _memo(S, B, ret):
    l, r = S.left, S.right
    if S.f[l][r] is not None:
        return f'{_cur(S, B, ret)} 已经算过（`g = {S.g[l][r]}`）→ ==记忆化==，直接返回'
    return f'{_cur(S, B, ret)} 还没算过 → 开始求解'


def _leaf(S, B, ret):
    if S.left == S.right:
        return f'只有一个字符 `{S0[S.left]!r}`（情况 1）'
    return '不止一个字符'


def _paren(S, B, ret):
    c = S0[S.left]
    if c not in ['(', ')']:
        return f'`{c!r}` 不是括号 → 直接保留'
    return f'`{c!r}` 单独一个括号一定不合法 → 必须删掉'


def _sl(S, B, ret):
    c = S0[S.left]
    if c != '(':
        return f'情况 2：左端 `s[{S.left}] = {c!r}` 不是 `(` → 先算 `s[{S.left + 1}..{S.right}]`'
    return f'左端是 `(`，情况 2 不成立'


def _sl2(S, B, ret):
    if S0[S.left] == ')':
        return f'左端是 `)`：它左边没有能配对的 `(`，==必须删去=='
    return '左端是普通字符：保留它'


def _sr(S, B, ret):
    c = S0[S.right]
    if c != ')':
        return f'情况 3：右端 `s[{S.right}] = {c!r}` 不是 `)` → 先算 `s[{S.left}..{S.right - 1}]`'
    return f'右端是 `)`，情况 3 不成立 → 形如 `(…)`'


def _two(S, B, ret):
    if S.left == S.right - 1:
        return '就是 `()`：本身合法，删 0 个'
    return f'形如 `(XX…)`（情况 4）：两种选择——保留两端，或找分割点'


def _cut_if(S, B, ret):
    if S.cut_len < B.min_len:
        return f'`cut_len = {S.cut_len}` < `min_len = {B.min_len}` → ==更优==，只保留这个分割点'
    if S.cut_len == B.min_len:
        return f'`cut_len = {S.cut_len}` = `min_len` → 一样好，记下这个分割点'
    return f'`cut_len = {S.cut_len}` > `min_len = {B.min_len}` → 不如现有方案'


CONFIG = dict(
    num=301, title='删除无效的括号', difficulty='Hard', category='多维动态规划',
    author='yiduobo', technique='区间 DP · 记忆化搜索',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def removeInvalidParentheses(self, s):

        if not s:
            return ['']

        f = [[None] * len(s) for _ in range(len(s))]
        g = [[None] * len(s) for _ in range(len(s))]
        self.dfs(0, len(s) - 1, s, f, g)

        return f[0][len(s) - 1]

    def dfs(self, left, right, s, f, g):
        if f[left][right] is not None:
            return

        if left == right:
            if s[left] not in ['(', ')']:
                f[left][right] = set([s[left]])
                g[left][right] = 0
            else:
                f[left][right] = set([''])
                g[left][right] = 1
            return

        if s[left] != '(':
            self.dfs(left + 1, right, s, f, g)
            if s[left] == ')':
                f[left][right] = f[left + 1][right]
                g[left][right] = g[left + 1][right] + 1
            else:
                f[left][right] = set([s[left] + x for x in f[left + 1][right]])
                g[left][right] = g[left + 1][right]
            return

        if s[right] != ')':
            self.dfs(left, right - 1, s, f, g)
            if s[right] == '(':
                f[left][right] = f[left][right - 1]
                g[left][right] = g[left][right - 1] + 1
            else:
                f[left][right] = set([x + s[right] for x in f[left][right - 1]])
                g[left][right] = g[left][right - 1]
            return

        if left == right - 1:
            f[left][right] = set(['()'])
            g[left][right] = 0
            return

        self.dfs(left + 1, right - 1, s, f, g)
        f[left][right] = set(['(' + x + ')' for x in f[left + 1][right - 1]])
        min_len = g[left + 1][right - 1]

        choose_pos = []
        for cut_pos in range(left, right):
            self.dfs(left, cut_pos, s, f, g)
            self.dfs(cut_pos + 1, right, s, f, g)
            cut_len = g[left][cut_pos] + g[cut_pos + 1][right]
            if cut_len < min_len:
                min_len = cut_len
                choose_pos = [cut_pos]
            elif cut_len == min_len:
                choose_pos.append(cut_pos)

        if min_len != g[left + 1][right - 1]:
            f[left][right] = set()

        for cut_pos in choose_pos:
            for first_part in f[left][cut_pos]:
                for second_part in f[cut_pos + 1][right]:
                    f[left][right].add(first_part + second_part)

        g[left][right] = min_len
''',
    call=f'Solution().removeInvalidParentheses({S0!r})',
    result_fn=sorted,
    expect=['()'],
    skip=['if not s:', 15, 24, 34, 44, 49, 'choose_pos = []', 70, 71],
    views=[
        dict(type='string', var='s', window=('left', 'right'), pointers={'cut_pos': 'pink'}, h=175, cell=90,
             label='s（框 = 当前区间 [left, right]，cut_pos = 分割点）'),
        dict(type='table', var='g', label='g[left][right]：这一段最少删几个括号', h=200, cell=62,
             rows=lambda S: [f'l={i}' for i in range(len(S0))], cols=lambda S: [f'r={j}' for j in range(len(S0))],
             cursors=[('left', 'right', 'yellow', '')]),
        dict(type='map', var=_fmap, label='f[left][right]：对应的合法字符串集合', h=145, font=21, fmt=lambda k, v: f'{k} = {v}'),
        dict(type='calls', h=105, hide=('s', 'f', 'g')),
    ],
    watch=[('min_len', 'min_len', 'orange'), ('cut_pos', 'cut_pos', 'pink'), ('cut_len', 'cut_len'),
           ('choose_pos', 'choose_pos', 'green')],
    captions={
        'f = [[None]': '`f[l][r]`：`s[l..r]` 删最少括号后的合法字符串集合',
        'g = [[None]': '`g[l][r]`：`s[l..r]` ==至少要删几个括号==才合法',
        'self.dfs(0, len(s) - 1': '记忆化搜索整段 `s[0..{len(B.s) - 1}]`',
        'if f[left][right] is not None': _memo,
        'if left == right:': _leaf,
        "if s[left] not in ['(', ')']": _paren,
        "f[left][right] = set([''])": '删掉它只剩空串：`f = {{\'\'}}`',
        23: '`g[{left}][{right}] = 1`：删了 1 个括号',
        20: '`g[{left}][{right}] = 0`：不用删',
        "if s[left] != '('": _sl,
        27: '递归求 `s[{B.left + 1}..{B.right}]`',
        "if s[left] == ')'": _sl2,
        'f[left][right] = f[left + 1][right]': '`f[{left}][{right}] = f[{left + 1}][{right}] = {fmt(f[left][right], 20)}`',
        'g[left][right] = g[left + 1][right] + 1': '在 `g[{left + 1}][{right}]` 的基础上删去 `s[{left}]`：`g = {g[left][right]}`',
        "if s[right] != ')'": _sr,
        'if left == right - 1': _two,
        "f[left][right] = set(['()'])": '`f[{left}][{right}] = {{\'()\'}}`',
        48: '`g[{left}][{right}] = 0`',
        51: '选择 1：==保留两端括号==，先求中间 `s[{B.left + 1}..{B.right - 1}]`',
        "f[left][right] = set(['(' + x": '中间的每个解两边套上括号：`f[{left}][{right}] = {fmt(f[left][right], 20)}`',
        'min_len = g[left + 1][right - 1]': '保留两端的代价 `min_len = g[{left + 1}][{right - 1}] = {min_len}`',
        'for cut_pos in range(left, right)': lambda S, B, ret: (f'选择 2：在 `cut_pos = {S.cut_pos}` 处切开，两段分别求解'
                                                               if B.get('cut_pos') != S.cut_pos or B['_line'] != S['_line'] else '分割点枚举完'),
        57: '求左段 `s[{B.left}..{B.cut_pos}]`',
        58: '求右段 `s[{B.cut_pos + 1}..{B.right}]`',
        'cut_len = g[left][cut_pos]': '`cut_len = g[{left}][{cut_pos}] + g[{cut_pos + 1}][{right}] = {cut_len}`',
        'if cut_len < min_len': _cut_if,
        'min_len = cut_len': '`min_len` → {min_len}，`choose_pos = {choose_pos}`',
        'elif cut_len == min_len': lambda S, B, ret: '`cut_len == min_len` → 追加分割点' if S.cut_len == S.min_len else f'`{S.cut_len}` ≠ `{S.min_len}`：不记录',
        'choose_pos.append(cut_pos)': '`choose_pos = {choose_pos}`',
        'if min_len != g[left + 1][right - 1]': lambda S, B, ret: ('分割更优 → 丢掉"保留两端"的解，`f` 清空' if S.min_len != S.g[S.left + 1][S.right - 1]
                                                                  else f'`min_len` 仍是 `{S.min_len}`：保留两端的解也是最优的，保留'),
        'for cut_pos in choose_pos': lambda S, B, ret: ('拼接完毕' if 'first_part' in B
                                                       else f'对最优分割点 `{S.cut_pos}`：左段的解 × 右段的解，两两拼接'),
        'f[left][right].add(': '`{first_part!r} + {second_part!r}` → 加入 `f[{left}][{right}]`（集合自动去重）',
        'g[left][right] = min_len': '`g[{left}][{right}] = {g[left][right]}`',
        'return f[0][len(s) - 1]': '答案 `f[0][{len(s) - 1}] = {fmt(ret, 20)}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='g[l][r] 记最少删几个、f[l][r] 记所有解，按端点分情况转移',
        complexity='状态 `O(n^2)`，转移枚举分割点 `O(n)` → `O(n^3)`（不计集合合并）',
        problem=['删除==最少数量==的无效括号，使字符串有效；返回所有可能结果',
                 '字符串里除了括号还可能有字母',
                 '示例：`"()())()"` → `["(())()","()()()"]`；`")("` → `[""]`',
                 '本视频：`"())"` → `["()"]`'],
        quote='g[left][right]表示s中left到right这一段==至少需要删除几个括号==才能达成合法的状态，f[left][right]则为g[left][right]所对应的==合法状态的集合==。',
        quote_src='—— yiduobo 题解原文',
        idea=['情况 1：单字符，括号必删；情况 2/3：左端不是 `(` 或右端不是 `)`，处理端点后缩小区间',
              '情况 4：形如 `(XX…X)`：保留两端，转移自 `f[l+1][r-1]`',
              '或者在中间找分割点 `cut_pos`，`g` 更小（或相等）时拼接两段的解'],
        result='`f[0][2] = {\'()\'}`，删 1 个括号 ✓',
        summary=['状态 `O(n^2)`，每个状态枚举分割点，共 `O(n^3)`（另加集合合并）',
                 '易错：分割更优时要先把"保留两端"的解清空，相等时两种都要',
                 '`f` 用集合：不同分割可能拼出同一个字符串，自动去重',
                 '原文为 Python 2 风格，只删去了文档字符串；返回值是 `set`',
                 '常见解法是 BFS/回溯，yiduobo 用的是==区间 DP=='],
    ),
)
