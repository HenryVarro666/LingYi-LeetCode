S0 = 'bbabab'


def _live(S):
    return all(x in S for x in ('i', 'j', 'length', 'f')) and S['j'] < len(S0) and S['j'] - S['i'] == S['length'] - 1


def _cell(S, a, b, v):
    if not _live(S):
        return None
    i, j = S['i'], S['j']
    if (a, b) == (i, j):
        return 'yellow'
    if S0[i] == S0[j]:
        return 'green' if (a, b) == (i + 1, j - 1) else None
    return 'blue' if (a, b) in ((i + 1, j), (i, j - 1)) else None


def _nz(S, a, b):
    d = {chr(97 + k): v for k, v in enumerate(S['f'][a][b]) if v}
    return '，'.join(f'`{c}`:{v}' for c, v in d.items()) if d else '全是 0'


def _formula(S):
    if not _live(S):
        return '`f[i][j][k]`：区间 `i..j`、==最外侧字母为 k== 的最长合法回文子序列'
    i, j = S['i'], S['j']
    ch = f'`s[{i}]={S0[i]}`，`s[{j}]={S0[j]}`'
    return f'{ch}；本格 `f[{i}][{j}]` 里非 0 的：{_nz(S, i, j)}'


CONFIG = dict(
    num=1682, title='最长回文子序列 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间 DP · 多记一维最外侧字母',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def longestPalindromeSubseq(self, s):

        n = len(s)
        f = [[[0] * 26 for j in range(n)] for i in range(n)]

        for length in range(2, n + 1):
            for i in range(n):
                j = i + length - 1
                if j >= n:
                    break

                for k in range(26):
                    f[i][j][k] = max(f[i + 1][j][k], f[i][j - 1][k])
                
                if s[i] == s[j]:
                    k = ord(s[i]) - 97
                    for t in range(26):
                        if k == t:
                            continue
                        f[i][j][k] = max(f[i][j][k], f[i + 1][j - 1][t] + 2)
        
        return max(f[0][-1])
''',
    call=f'Solution().longestPalindromeSubseq({S0!r})',
    expect=4,
    skip=['if j >= n', 'for i in range(n)', 'j = i + length - 1', 'for k in range(26)', 'f[i][j][k] = max(f[i + 1][j][k]', 'for t in range(26)', 'if k == t', 'continue',
          'f[i][j][k] = max(f[i][j][k], f[i + 1][j - 1][t] + 2)'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（蓝 = i，粉 = j）', h=190, cell=80, pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_formula, size=22, h=60),
        dict(type='table', var='[[max(c) for c in row] for row in f]', label='每个区间所有「最外侧字母」中最大的 f（黄 = 正在算，蓝/绿 = 依赖）', h=380, cell=62,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_cell),
    ],
    watch=[('length', 'length', 'green'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'orange')],
    captions={
        'n = len(s)': '`n = {n}`',
        'f = [[[0]': '`f[i][j][k]`：区间 `i..j`、==最外侧字母是 k==（0~25 对应 a~z）的最长回文长度，多这一维才能保证相邻不重复',
        'for length in range': lambda S, B, r: (f'区间长度 `length = {S.length}`：==先算短区间==' if S.get('length') != B.get('length') else '所有区间都算完了'),
        'break': '这个长度算完，换下一个长度',
        'if s[i] == s[j]': lambda S, B, r: (f'`s[{S.i}] = {S.s[S.i]}`，`s[{S.j}] = {S.s[S.j]}`：先放弃一端取 `max(f[i+1][j], f[i][j-1])`；' + ('两端相同，可以配对' if S.s[S.i] == S.s[S.j] else '两端不同，不能配对')),
        'k = ord': lambda S, B, r: (f'最外侧字母 `k = {S.k}`（`{S.s[S.i]}`）：枚举内层字母 `t ≠ k`，取 `f[{S.i+1}][{S.j-1}][t]` 的最大值 `{max(S.f[S.i+1][S.j-1][t] for t in range(26) if t != S.k)}`，`+ 2` 配对 → ==`f[{S.i}][{S.j}][{S.k}]` 至少 {max(S.f[S.i][S.j][S.k], max(S.f[S.i+1][S.j-1][t] for t in range(26) if t != S.k) + 2)}=='
                 ),
        'return max(f[0][-1])': '整串所有最外侧字母里取最大 → =={ret}==',
    },
    cards=dict(
        one_liner='区间 DP 多记一维：最外侧是哪个字母，配对时内层必须不同',
        complexity='时间 `O(26 · n^2)`，空间 `O(26 · n^2)`',
        problem=['求 `s` 的最长「好回文子序列」：回文、长度为偶数、除了正中间的两个字符外相邻字符不相同',
                 '返回它的长度',
                 '示例：`s = "bbabab"` → `4`（`"baab"`）'],
        quote='最直观的想法就是在原始动态规划状态表示的基础上加上最外层字符的信息。令f[i][j][k]表示字符串中第i到第j个字符中，以字符k为最外侧字符的回文子序列的最长长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['放弃一端：`f[i][j][k] = max(f[i+1][j][k], f[i][j-1][k])`',
              '`s[i] == s[j]` 时两端配对，最外侧字母 `k = s[i]`',
              '内层最外侧字母 `t` 必须 `≠ k`：`f[i+1][j-1][t] + 2`，枚举 `t` 取最大',
              '答案是 `max(f[0][-1])`，各最外侧字母里取最大'],
        summary=['时间、空间都是 `O(26 · n^2)`',
                 '易错：配对时内层最外侧字母 `t` 要 `≠ k`，否则出现相邻重复',
                 '长度为 1 的区间本题不算（回文必须偶数长度），初值全 0',
                 '原文已是 Python 3 可运行的写法，代码未做改动',
                 '视频里省略了 26 次内层枚举的逐步展示，只显示结果'],
    ),
)
