def _fc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    ln = S.get('_line', 0)
    if i is None or j is None:
        return None
    if r == i and c == j:
        return 'yellow'
    if ln in (19, 20) and r == i + 0 and c == j:
        return 'yellow'
    return None


def _gc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None or S.get('_line', 0) < 16:
        return None
    if k == i:
        return 'yellow'
    if j is not None and k == j and S.get('_line', 0) in (19, 20):
        return 'green'
    return None


CONFIG = dict(
    num=2430, title='对字母串可执行的最大删除数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='后缀 DP + 全部后缀 LCP',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2102'],
    code='''
class Solution(object):
    def deleteString(self, s):

        n = len(s)
        s += '#'

        f = [[0] * (n + 1) for _ in range(n + 1)]
        f[n - 1][n] = 0
        for i in range(n - 2, -1, -1):
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    f[i][j] = f[i + 1][j + 1] + 1
        
        g = [1] * n
        for i in range(n - 2, -1, -1):
            for j in range(i + 1, n):
                if f[i][j] >= j - i:
                    g[i] = max(g[i], g[j] + 1)
        
        return g[0]
''',
    call='Solution().deleteString("aabaab")',
    expect=3,
    skip=['n = len(s)', "s += '#'", 'f[n - 1][n] = 0', 'for j in range(i + 1, n)'],
    views=[
        dict(type='string', var='s', label='s（末尾补的 # 是哨兵；蓝 = i，粉 = j）', h=200, cell=64, pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else ('pink' if k == S.get('j') else None)),
        dict(type='table', var='f', label='f[i][j] = 后缀 i 与后缀 j 的最长公共前缀', h=320, cell=46,
             rows=lambda S: list(range(len(S['f']))), cols=lambda S: list(range(len(S['f']))), color=_fc),
        dict(type='array', var='g', label='g[i] = 后缀 s[i:] 最多能删几次', h=150, cell=64, color=_gc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'f = [[0]': '`f[i][j]`：以 i 开头与以 j 开头的两个后缀的最长公共前缀，先置 0',
        'for i in range(n - 2, -1, -1)': lambda S, B, r: (f'`i = {S.i}`' + ('：由 `f[i+1][j+1]` 推出 `f[i][j]`，所以 i 从后往前' if S._line == 9 else '：`g[i]` 要用到 `g[j]`（j > i），所以 i 从后往前')
                                                          if S.i != B.get('i') else ('LCP 表算完' if S._line == 9 else 'g 全部算完，答案是 `g[0]`')),
        'if s[i] == s[j]': lambda S, B, r: (f"`s[{S.i}] = {S.s[S.i]}` == `s[{S.j}] = {S.s[S.j]}` → 两个后缀的公共前缀比 `f[{S.i+1}][{S.j+1}]` 多 1" if S.s[S.i] == S.s[S.j]
                                           else f"`s[{S.i}] = {S.s[S.i]}` ≠ `s[{S.j}] = {S.s[S.j]}` → 公共前缀是 0"),
        'f[i][j] = f[i + 1][j + 1] + 1': '`f[{i}][{j}] = f[{i+1}][{j+1}] + 1` = =={f[i][j]}==',
        'g = [1] * n': '`g[i]` 先置 1：这个后缀可以==一次全删==',
        'if f[i][j] >= j - i': lambda S, B, r: (f'`f[{S.i}][{S.j}] = {S.f[S.i][S.j]} ≥ j − i = {S.j - S.i}` → 后缀 i 开头的 {S.j - S.i} 个字母 == 后缀 j 开头的 {S.j - S.i} 个，==可以删掉前面这一段=='
                                               if S.f[S.i][S.j] >= S.j - S.i else
                                               f'`f[{S.i}][{S.j}] = {S.f[S.i][S.j]} < j − i = {S.j - S.i}` → 前缀不够长，不能删到 j'),
        'g[i] = max(g[i], g[j] + 1)': '删掉 `s[{i}:{j}]` 后剩后缀 j：`g[{i}] = max({B.g[i]}, g[{j}] + 1 = {g[j]+1})` = =={g[i]}==',
        'return g[0]': '整串最多删 `g[0]` = =={ret}== 次',
    },
    cards=dict(
        one_liner='g[i] 记后缀的最大删除次数；删前缀要求「后缀 i 与后缀 j 的 LCP ≥ j − i」',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['每次可以删整个字符串，或在前 `i` 个字母 == 接下来 `i` 个字母时删前 `i` 个',
                 '求删空字符串的==最多操作次数==',
                 '示例：`"abcabcdabc"` → `2`；本视频：`"aabaab"` → `3`'],
        quote='令g[i]表示字符串中从i开始的后缀最多可以删除的次数……i到j - 1之间字符串必须与以j开头的长度为j - i的字符串完全一致，也就是以i开头的后缀与以j开头的后缀的最长公共前缀必须大于等于j - i。',
        quote_src='—— yiduobo 题解原文',
        idea=['`g[i]` 初值 1（一次全删）；枚举 `j`：删掉 `s[i:j]`，剩下后缀 j',
              '合法条件：`f[i][j] ≥ j − i`，其中 `f` 是所有后缀两两的 LCP',
              '`f[i][j] = f[i+1][j+1] + 1`（首字母相同时），用 `O(n^2)` DP 预处理'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错：`g` 的初值是 1，不是 0；`i` 从 `n-2` 倒着算，`g[n-1]` 恒为 1',
                 '末尾补 `#` 让 `f[i+1][j+1]` 不越界',
                 '对比灵神：灵神 `f` 初值 0 最后 `+1`，并对全部相同字母特判；yiduobo 直接 `g=1` 起步，枚举 `j` 而不是长度'],
    ),
)
