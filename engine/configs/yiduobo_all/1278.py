S0 = 'abcde'
K0 = 3


def _fc(S, r, c, v):
    ln = S.get('_line')
    if ln in (9, 10, 11, 12, 13) and S.get('l') is not None and S.get('i') is not None and 'g' not in S:
        i, l = S['i'], S['l']
        if (r, c) == (i, l):
            return 'yellow'
        if (r, c) == (i + 1, l - 2):
            return 'blue'
        return None
    if 'cut_pos' in S and ln in (20, 21, 22, 23) :
        if (r, c) == (S['cut_pos'] + 1, S['i'] - S['cut_pos']):
            return 'blue'
    if 'g' in S and S.get('j') == 1 and ln in (20, 21, 22) and (r, c) == (0, S['i'] + 1):
        return 'blue'
    return None


def _gc(S, r, c, v):
    if 'g' not in S or S.get('i') is None or S.get('j') is None:
        return None
    if (r, c) == (S['i'], S['j']):
        return 'yellow'
    cp = S.get('cut_pos')
    if cp is not None and S.get('_line') in (22, 23, 24) and (r, c) == (cp, S['j'] - 1):
        return 'blue'
    return 'green' if v is not None else None


def _txt(S):
    if 'g' not in S:
        i, l = S.get('i'), S.get('l')
        if i is None or l is None:
            return '`f[i][l]`：从 `i` 开始、长 `l` 的子串改成回文的最少次数'
        s = S['s']
        return f'子串 `s[{i}..{i + l - 1}]` = `{s[i:i + l]}`：两端 `{s[i]}` 和 `{s[i + l - 1]}`，里面是 `f[{i + 1}][{l - 2}]`'
    i, j, cp = S.get('i'), S.get('j'), S.get('cut_pos')
    if i is None or j is None:
        return '`g[i][j]`：前 `i+1` 个字符切成 `j` 份并改成回文的最少次数'
    if j > 1 and cp is not None and S.get('_line') in (22, 23, 24):
        return f'前 `{cp + 1}` 个字符分 `{j - 1}` 份 `g[{cp}][{j - 1}]` + 最后一段 `s[{cp + 1}..{i}]` 的 `f[{cp + 1}][{i - cp}]`'
    return f'`g[{i}][{j}]`：前 `{i + 1}` 个字符切成 `{j}` 份'


CONFIG = dict(
    num=1278, title='分割回文串 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='两个 DP：回文代价 f + 切分 g',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1979'],
    code='''
class Solution(object):
    def palindromePartition(self, s, k):

        n = len(s)
        f = [[0] * (n + 1) for _ in range(n)]
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                if s[i] == s[i + l - 1]:
                    f[i][l] = f[i + 1][l - 2]
                else:
                    f[i][l] = f[i + 1][l - 2] + 1
        
        g = [[None] * (k + 1) for _ in range(n)]
        for j in range(1, k + 1):
            for i in range(j - 1, n):
                if j == 1:
                    g[i][j] = f[0][i + 1]
                else:
                    for cut_pos in range(j - 2, i):
                        if g[i][j] is None or g[i][j] > g[cut_pos][j - 1] + f[cut_pos + 1][i - cut_pos]:
                            g[i][j] = g[cut_pos][j - 1] + f[cut_pos + 1][i - cut_pos]

        return g[n - 1][k]
''',
    call=f'Solution().palindromePartition({S0!r}, {K0})',
    expect=1,
    skip=['n = len(s)', 'for i in range(n - l + 1)', 'else:'],
    views=[
        dict(type='string', var='s', label='s', h=140, cell=70,
             color=lambda S, k, v: ('blue' if S.get('l') is not None and 'g' not in S and S['i'] <= k <= S['i'] + S['l'] - 1 else None)),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='table', var='f', label='f[i][l]（行 i = 起点，列 l = 长度；黄 = 当前，蓝 = 依赖）', h=270, cell=56,
             rows=lambda S: list(range(len(S['s']))), cols=lambda S: list(range(len(S['s']) + 1)), color=_fc),
        dict(type='table', var=lambda S: S.get('g') or [[None] * (S['k'] + 1) for _ in S['s']],
             label='g[i][j]（行 i = 前 i+1 个字符，列 j = 份数）', h=270, cell=56,
             rows=lambda S: list(range(len(S['s']))), cols=lambda S: list(range(S['k'] + 1)), color=_gc),
    ],
    max_steps=54,
    watch=[('l', 'l', 'purple'), ('i', 'i', 'blue'), ('j', 'j', 'yellow'), ('cut_pos', 'cut_pos', 'pink')],
    captions={
        'f = [[0] * (n + 1)': '`f[i][l]`：从 `i` 起长 `l` 的子串改成回文串的最少次数；长 0、1 的默认是 0',
        'for l in range(2, n + 1)': lambda S, B, r: (f'子串长度 `l = {S.l}`：由短到长，短的先算好' if S.get('l') != B.get('l') else 'f 全部算完，开始切分'),
        'if s[i] == s[i + l - 1]': lambda S, B, r: (f'`s[{S.i}] = {S.s[S.i]}`，`s[{S.i + S.l - 1}] = {S.s[S.i + S.l - 1]}`：'
                                                   + ('相等 → 首末==无须处理==' if S.s[S.i] == S.s[S.i + S.l - 1] else '不等 → 要改其中一个，==代价 +1==')),
        'f[i][l] = f[i + 1][l - 2]': lambda S, B, r: f'`f[{S.i}][{S.l}] = f[{S.i + 1}][{S.l - 2}]' + ('' if S._line == 9 else ' + 1') + f'` = =={S.f[S.i][S.l]}==',
        'g = [[None]': '`g[i][j]`：前 `i+1` 个字符切成 `j` 份并改成回文的最少次数',
        'for j in range(1, k + 1)': lambda S, B, r: (f'份数 `j = {S.j}`' if S.get('j') != B.get('j') else '`k` 份都算完了'),
        'for i in range(j - 1, n)': lambda S, B, r: (f'`i = {S.i}`：前 `{S.i + 1}` 个字符分 `{S.j}` 份（至少要有 `j` 个字符）' if B.get('i') != len(S.s) - 1 else f'`j = {S.j}` 的所有 `i` 都算完'),
        'if j == 1': lambda S, B, r: ('`j = 1`：不用切，整段改成回文' if S.j == 1 else '`j > 1`：枚举前 `j-1` 份的右边界 `cut_pos`'),
        'g[i][j] = f[0][i + 1]': '`g[{i}][1] = f[0][{i + 1}]` = =={g[i][j]}==',
        'for cut_pos in range': lambda S, B, r: (f'`cut_pos` 最小 `j-2 = {S.j - 2}`：前面要留够 `j-1` 份' if not (S.get('cut_pos') == B.get('cut_pos') and S.get('i') == B.get('i') and S.get('j') == B.get('j')) else '`cut_pos` 枚举完'),
        'if g[i][j] is None or': lambda S, B, r: (
            '`g[{}][{}]` 还没值 → 直接记下'.format(S.i, S.j) if S.g[S.i][S.j] is None
            else f'`{S.g[S.i][S.j]}` vs `g[{S.cut_pos}][{S.j - 1}] + f[{S.cut_pos + 1}][{S.i - S.cut_pos}]` = `{S.g[S.cut_pos][S.j - 1]} + {S.f[S.cut_pos + 1][S.i - S.cut_pos]}` → '
                 + ('==更小，更新==' if S.g[S.i][S.j] > S.g[S.cut_pos][S.j - 1] + S.f[S.cut_pos + 1][S.i - S.cut_pos] else '不更新')),
        'return g[n - 1][k]': '整个 `s` 切成 `{k}` 份的最少修改 = =={ret}==',
    },
    cards=dict(
        one_liner='先算每段改成回文的代价，再枚举切点做划分 DP',
        complexity='时间 `O(n^2·k)`，空间 `O(n^2)`',
        problem=['字符串 `s` 可以修改若干字母，再切成 `k` 个非空子串，每个子串都要是回文串',
                 '求最少修改次数',
                 '示例：`s = "abcde", k = 3` → `1`'],
        quote='题目中有两种操作，一种是修改某个字符，另一种是将一个大串分割成若干个小串。首先，我们可以先考虑修改字符的情况……',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][l]`：从 `i` 起长 `l` 的子串变回文；首末相同 `f[i+1][l-2]`，不同再 `+1`',
              '`g[i][j]`：前 `i+1` 个字符切 `j` 份；`j = 1` 就是 `f[0][i+1]`',
              '`j > 1` 枚举前 `j-1` 份的右边界 `cut_pos`，最后一段只改字符'],
        summary=['时间 `O(n^2·k)`，空间 `O(n^2)`',
                 '易错：`f[i+1][l-2]` 在 `l = 2` 时是长度 0，默认 0',
                 '`cut_pos` 范围 `j-2 .. i-1`，要给前 `j-1` 份留够字符',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：灵神用 `min_change[l][r]` 按区间端点，并滚动去掉了份数这一维'],
    ),
)
