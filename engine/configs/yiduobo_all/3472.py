S0 = 'abc'
K0 = 1


def _live(S):
    return all(x in S for x in ('start', 'end', 'r', 'length')) and S.get('end', 99) < len(S0) and S['end'] - S['start'] == S['length'] - 1


def _cell(S, a, b, v):
    if not _live(S):
        return None
    st, e = S['start'], S['end']
    if (a, b) == (st, e):
        return 'yellow'
    if e - st >= 1 and (a, b) in ((st + 1, e), (st, e - 1)):
        return 'blue'
    if e - st >= 2 and (a, b) == (st + 1, e - 1):
        return 'green'
    return None


def _formula(S):
    if not _live(S):
        return '`f[start][end][r]`：区间 `[start, end]`，还剩 `r` 次操作时的最长回文子序列'
    st, e, r = S['start'], S['end'], S['r']
    return f'当前 `f[{st}][{e}][{r}]`（`s[{st}]={S0[st]}`，`s[{e}]={S0[e]}`，剩 `r={r}`）'


def _dis(S, B, ret):
    return (f'较大 `{S.ma}`、较小 `{S.mi}`：往下变 `{ord(S.ma) - ord(S.mi)}` 步，绕过 z→a 要 `{ord(S.mi) + 26 - ord(S.ma)}` 步 → `dis = {S.dis}`')


def _cmp(S, B, ret):
    if S.dis <= S.r:
        return f'`dis = {S.dis} ≤ r = {S.r}`：次数够，两端可以变成一样'
    return f'`dis = {S.dis} > r = {S.r}`：次数不够，两端配不成对'


CONFIG = dict(
    num=3472, title='至多 K 次操作后的最长回文子序列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间 DP · 按区间长度递推 · 带剩余操作数',
    tags=['灵神题单', '动态规划', '难度分 1884'],
    code='''
class Solution(object):
    def longestPalindromicSubsequence(self, s, k):

        n = len(s)
        f = [[[None] * (k + 1) for _ in range(n)] for _ in range(n)]

        for length in range(1, n + 1):
            for start in range(n):
                end = start + length - 1
                if end >= n:
                    break
                for r in range(k + 1):
                    if length == 1:
                        f[start][end][r] = 1
                    else:
                        ma = max(s[start], s[end])
                        mi = min(s[start], s[end])
                        dis = min(ord(ma) - ord(mi), ord(mi) + 26 - ord(ma))

                        if length == 2:
                            if dis <= r:
                                f[start][end][r] = 2
                            else:
                                f[start][end][r] = 1
                        else:
                            f[start][end][r] = max(f[start + 1][end][r], f[start][end - 1][r])
                            if dis <= r:
                                f[start][end][r] = max(f[start][end][r], f[start + 1][end - 1][r - dis] + 2)

        return f[0][n - 1][k]
''',
    call=f'Solution().longestPalindromicSubsequence({S0!r}, {K0})',
    expect=2,
    skip=['for start in range', 'for r in range', 'end = start + length - 1', 'ma = max', 'mi = min', 'if end >= n', 'else:'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（蓝 = start，粉 = end）', h=200, cell=80, pointers={'start': 'blue', 'end': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='[[c[r] for c in row] for row in f]', label='当前 r 对应的 f[start][end][r]（黄 = 正在算，蓝/绿 = 依赖）', h=380, cell=70,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_cell),
    ],
    watch=[('length', 'length', 'green'), ('start', 'start', 'blue'), ('end', 'end', 'pink'), ('r', 'r', 'cyan'), ('dis', 'dis', 'orange')],
    captions={
        'n = len(s)': '`n = {n}`',
        'f = [[[None]': '`f[start][end][r]`：区间 `[start, end]`、==还剩 r 次==操作时的答案',
        'for length in range': lambda S, B, r: (f'区间长度 `length = {S.length}`：==先算短区间，再算长区间==' if S.get('length') != B.get('length') else '所有长度都算完了'),
        'if length == 1': lambda S, B, r: (f'`[{S.start}, {S.end}]` 只有一个字符' if S.length == 1 else f'`[{S.start}, {S.end}]` 有 {S.length} 个字符，看两端'),
        'f[start][end][r] = 1': lambda S, B, r: ('单个字符必然回文：`f = 1`' if S.length == 1 else f'两端配不上，只留一个：`f[{S.start}][{S.end}][{S.r}] = 1`'),
        'dis = min': _dis,
        'if length == 2': lambda S, B, r: ('只有两个字符，不用看里面' if S.length == 2 else '区间多于两个字符，里面还有内容'),
        'break': '`start` 已排到末尾，这个长度算完 → 换下一个长度',
        'if dis <= r': _cmp,
        'f[start][end][r] = 2': '两端改成一样，留下两个：`f = 2`',
        'f[start][end][r] = max(f[start + 1]': '先放弃一端：`max(f[{start+1}][{end}][{r}], f[{start}][{end-1}][{r}])` = =={f[start][end][r]}==',
        'f[start + 1][end - 1][r - dis] + 2': '保留两端：剩 `{r} - {dis}` 次，里面 `[{start+1}, {end-1}]` 的答案 `+ 2`，取最大 = =={f[start][end][r]}==',
        'return f[0][n - 1][k]': '整个区间 `[0, {n-1}]`、剩 `k = {k}` 次 → =={ret}==',
    },
    cards=dict(
        one_liner='区间 DP 再携带一维：区间还剩几次操作机会',
        complexity='时间 `O(n^2 k)`，空间 `O(n^2 k)`',
        problem=['字符串 `s` 和整数 `k`，可把任意位置的字符改成字母表中相邻的字符（`a` 和 `z` 相邻）',
                 '最多操作 `k` 次，求 `s` 的最长回文子序列长度',
                 '示例：`s = "abced"`，`k = 2` → `3`；本视频：`"abc"`，`k = 1` → `2`'],
        quote='考虑到本题的数据规模，完全可以直接令f[start][end][r]表示对于s中的区间[start, end]，在还剩下r次操作机会时可以得到的最长回文子序列长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间只有一个字符：`f = 1`；两个字符：能配对就是 2，否则 1',
              '更长的区间：放弃一端 `max(f[start+1][end][r], f[start][end-1][r])`',
              '想留两端，得 `dis ≤ r`：用 `f[start+1][end-1][r-dis] + 2`',
              '`dis` = 直接变（差值）与绕 z→a（`ord(mi)+26-ord(ma)`）的较小值'],
        summary=['时间、空间都是 `O(n^2 k)`',
                 '递推要先算短区间，所以==外层枚举区间长度==',
                 '易错：`dis` 有两条路，取较小；`r - dis` 不能为负，要先判断 `dis <= r`',
                 '原文已是 Python 3 可运行的写法，代码未做改动',
                 '对比灵神：灵神把 `k` 放第一维，并先判断「整串能否直接改成回文」'],
    ),
)
