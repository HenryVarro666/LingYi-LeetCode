def _top(S):
    ln = S['_line']
    if ln <= 13:
        if ln >= 8 and 'i' in S and 'j' in S:
            i, j = S['i'], S['j']
            return f"`f[{i}][{j}]`：从 `s[{i}]` 与 翻转后 `t[{j}]` 开头的子串，最长匹配多长"
        return '先把 `t` 翻转，问题变成：`s` 的子串与 `t` 的子串有多长的公共前缀'
    if ln <= 38:
        return '`calc`：`g[l][r]` = `s[l..r]` 是否回文；`best[i]` = 以 `i` 开头的最长回文长度'
    if 'i' in S and 'j' in S and ln >= 43:
        i, j = S['i'], S['j']
        return f"枚举 `s[{i}:]` 与 `t[{j}:]` 的起点：两端各取 `f` 对，中间补 `gs`/`gt` 的最长回文"
    return '两串的最长回文预处理完毕'


def _fcolor(S, r, c, v):
    if S['_line'] > 13 and S['_line'] < 43:
        return None
    if 'i' in S and 'j' in S and (r, c) == (S['i'], S['j']):
        return 'yellow'
    return None


def _gcolor(S, r, c, v):
    if 'left' in S and 'right' in S and (r, c) == (S['left'], S['right']) and S['_line'] <= 29:
        return 'yellow'
    return 'green' if v is True else None


CONFIG = dict(
    num=3504, title='子字符串连接后的最长回文串 II', difficulty='Hard', category='字符串',
    author='yiduobo', technique='翻转 t 的 LCP 动态规划 + 区间 DP 求最长回文',
    tags=['灵神题单', '字符串', '难度分 2398'],
    code='''
class Solution(object):
    def longestPalindrome(self, s, t):
        
        t = t[::-1]
        m = len(s)
        n = len(t)
        f = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if s[i] == t[j]:
                    f[i][j] = 1
                    if i + 1 < m and j + 1 < n:
                        f[i][j] += f[i + 1][j + 1]
        
        def calc(s):
            n = len(s)
            g = [[False] * n for _ in range(n)]
            for length in range(1, n + 1):
                for left in range(n):
                    right = left + length - 1
                    if right >= n:
                        break
                    
                    if left == right:
                        g[left][right] = True
                    elif left == right - 1:
                        g[left][right] = (s[left] == s[right])
                    else:
                        g[left][right] = (s[left] == s[right]) and g[left + 1][right - 1]
            
            best = [0] * (n + 1)
            for i in range(n):
                for j in range(n - 1, -1, -1):
                    if g[i][j]:
                        best[i] = j - i + 1
                        break
            
            return best
                        
        gs = calc(s)
        gt = calc(t)
        res = max(max(gs), max(gt))
        for i in range(m):
            for j in range(n):
                res = max(res, f[i][j] * 2 + max(gs[i + f[i][j]], gt[j + f[i][j]]))
        
        return res
''',
    call='Solution().longestPalindrome("ab", "ca")',
    expect=3,
    skip=['else:', 'elif', 'for length in range', 'for left in range', 'right = left + length - 1', 'if right >= n', 'if left == right:', 'for i in range(m - 1', 'n = len(s)', 'break', 9, 32, 33, 43, 44],
    max_steps=90,
    views=[
        dict(type='text', fn=_top, size=22, h=60),
        dict(type='string', var='s', label='s（calc 里是正在处理的那个串）', cell=48, h=95),
        dict(type='string', var='t', label='t（已翻转）', cell=48, h=95),
        dict(type='grid', var='f', label='f[i][j]：s[i:] 与 t[j:] 的最长公共前缀', cell=64, h=190, color=_fcolor,
             rows=lambda S: list(range(len(S['f']))), cols=lambda S: list(range(len(S['f'][0])))),
        dict(type='grid', var='g', label='g[l][r]：s[l..r] 是否回文', cell=64, h=200, color=_gcolor,
             rows=lambda S: list(range(len(S['g']))), cols=lambda S: list(range(len(S['g'])))),
        dict(type='array', var='best', label='best[i]：以 i 开头的最长回文长度', cell=52, h=105),
    ],
    watch=[('res', 'res', 'green'), ('gs', 'gs'), ('gt', 'gt')],
    captions={
        't = t[::-1]': '把 `t` 翻转成 `{t}`：这样「`s` 的前缀」和「`t` 的后缀对称」就变成了「两个子串相同」',
        'm = len(s)': '`m = {m}`',
        'f = [[0]': '`f[i][j]`：`s[i:]` 与（翻转后的）`t[j:]` 的最长匹配长度，从后往前填',
        'if s[i] == t[j]': lambda S, B, ret: (f"`s[{S.i}] = {S.s[S.i]}` == `t[{S.j}] = {S.t[S.j]}` → 匹配" if S.s[S.i] == S.t[S.j]
                                              else f"`s[{S.i}] = {S.s[S.i]}` ≠ `t[{S.j}] = {S.t[S.j]}` → `f[{S.i}][{S.j}] = 0`"),
        'f[i][j] = 1': '先记 1：这一对字符匹配',
        'if i + 1 < m and j + 1 < n': lambda S, B, ret: ('后面还有字符 → 可以接上 `f[i+1][j+1]`' if S.i + 1 < S.m and S.j + 1 < S.n else '已到边界，没有右下角，`f` 就是 1'),
        'f[i][j] += f[i + 1][j + 1]': '加上后一位的匹配长度 → `f[{i}][{j}]` = =={f[i][j]}==',
        'g = [[False]': '`g[left][right]`：`s[left..right]` 是否为回文，按长度从短到长填',
        25: '长度 1：单个字符一定是回文 → `g[{left}][{right}] = True`',
        27: '长度 2：两字符相等才是回文 → `g[{left}][{right}] = {g[left][right]}`',
        29: '长度 ≥ 3：两端相等且去掉两端后仍是回文 → `g[{left}][{right}] = {g[left][right]}`',
        'best = [0]': '`best[i]`：以 `i` 开头的最长回文长度，多开一位（下标 `n` 表示空串，值 0）',
        'if g[i][j]': lambda S, B, ret: (f'从 `i = {S.i}` 开头、`j` 从最右往左找：`g[{S.i}][{S.j}]` 为真，`s[{S.i}..{S.j}]` 是回文，第一个找到的就是最长的' if S.g[S.i][S.j]
                                          else f'从 `i = {S.i}` 开头：`g[{S.i}][{S.j}]` 为假，`j` 往左缩'),
        'best[i] = j - i + 1': '`best[{i}] = {j} - {i} + 1 = {best[i]}`',
        'return best': '返回 `best` = `{best}`',
        'gs = calc(s)': '对 `s` 算 `gs`：`s` 里从每个位置开始的最长回文（作为中间部分，取自 `s` 的后缀）',
        'gt = calc(t)': '对翻转后的 `t` 算 `gt`',
        'res = max(max(gs)': '只用一个串的情况（另一个子串为空）：`res = {res}`',
        'res = max(res, f[i][j]': '枚举 `i = {i}`、`j = {j}`：两端各 `f[{i}][{j}] = {f[i][j]}` 个字符 → `{f[i][j]} × 2`；中间取 `gs[{i + f[i][j]}] = {gs[i + f[i][j]]}` 与 `gt[{j + f[i][j]}] = {gt[j + f[i][j]]}` 的较大者 → `res` = =={res}==',
        'return res': '最长回文长度 =={ret}==',
    },
    cards=dict(
        one_liner='拼接后的回文 = 两端对称的部分 + 中间一段自成回文的部分',
        complexity='时间 `O(nm + n^2 + m^2)`，空间 `O(nm + n^2 + m^2)`',
        problem=['从 `s` 和 `t` 各选一个子串（可以为空），按顺序拼接',
                 '求能得到的==最长回文串==的长度',
                 '示例：`s = "abc"`，`t = "def"` → `1`；本视频：`s = "ab"`，`t = "ca"` → `3`（`a` + `ca` = `aca`）'],
        quote='其中两侧的sub_s的前缀和sub_t的后缀必须是对称的，而中间这个部分可以为空，也可以是sub_s或者sub_t的一部分，但是中间这一部分必须自成回文。',
        quote_src='—— yiduobo 题解原文',
        idea=['只取一个串：`s` 或 `t` 里最长的回文子串（区间 DP `g`）',
              '两个都取：把 `t` 翻转，`f[i][j]` 是两个后缀的最长公共前缀，两端各取 `f` 个字符',
              '中间一段取 `s` 里从 `i+f` 开头、或 `t` 里从 `j+f` 开头的最长回文，即 `best` 数组'],
        result='`a` + `b` + `a`：两端 `a` 对称，中间 `b` 自成回文 → `aba`，长度 3 ✓',
        summary=['时间 `O(nm + n^2 + m^2)`，`n, m <= 1000` 可行',
                 '`f` 要从后往前填，`f[i][j]` 依赖 `f[i+1][j+1]`',
                 '`best` 多开一位：`i + f` 可能等于 `n`，此时中间部分为空',
                 '原文本来就能在 Python 3 运行，代码未改动',
                 '对比灵神：灵神把「`|x| < |y|`」交给翻转复用，并用中心扩展；yiduobo 先翻转 `t`，用 `best` 一次覆盖两种中间段'],
    ),
)
