def _lcp_col(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    ln = S.get('_line', 0)
    if i is None or j is None:
        return None
    if r == i and c == j and ln >= 10:
        return 'yellow'
    if ln in (13, 14, 15, 16, 17) and r == i and c == i + j:
        return 'yellow'
    return None


def _fcol(S, k, v):
    i = S.get('i')
    if i is None or S.get('_line', 0) < 13:
        return None
    if k == i:
        return 'yellow'
    j = S.get('j')
    if j is not None and S.get('_line', 0) in (14, 15) and k == i + j:
        return 'green'
    return None


CONFIG = dict(
    num=2430, title='对字母串可执行的最大删除数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + LCP 预处理',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2102'],
    code='''
class Solution:
    def deleteString(self, s: str) -> int:
        n = len(s)
        if len(set(s)) == 1:  # 特判全部相同的情况
            return n

        lcp = [[0] * (n + 1) for _ in range(n + 1)]  # lcp[i][j] 表示 s[i:] 和 s[j:] 的最长公共前缀
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i, -1):
                if s[i] == s[j]:
                    lcp[i][j] = lcp[i + 1][j + 1] + 1

        f = [0] * n
        for i in range(n - 1, -1, -1):
            for j in range(1, (n - i) // 2 + 1):
                if lcp[i][i + j] >= j:  # 说明 s[i:i+j] == s[i+j:i+2*j]
                    f[i] = max(f[i], f[i + j])  # 这里改成手动 if 更新会更快
            f[i] += 1
        return f[0]
''',
    call='Solution().deleteString("aabaab")',
    expect=3,
    skip=['n = len(s)', 'f = [0] * n', 'for j in range(n - 1, i, -1)', 'for j in range(1,'],
    views=[
        dict(type='string', var='s', label='s（蓝 = i 后缀起点，粉 = j，仅填表时）', h=150, cell=70, pointers={'i': 'blue', 'j if _line < 13 else None': 'pink'}, pointer_labels={'j if _line < 13 else None': 'j'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else ('pink' if k == S.get('j') and S.get('_line', 0) < 13 else None)),
        dict(type='table', var='lcp', label='lcp[i][j]（黄 = 当前格）', h=320, cell=46, rows=lambda S: list(range(len(S['lcp']))),
             cols=lambda S: list(range(len(S['lcp']))), color=_lcp_col),
        dict(type='array', var='f', label='f[i] = 删除后缀 s[i:] 的最大操作数', h=150, cell=70, color=_fcol),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'len(set(s)) == 1': lambda S, B, r: ('`s` 只有一种字母 → 每次删 1 个，直接 `n`' if len(set(S.s)) == 1 else '`s` 有不同字母，继续一般做法'),
        'lcp = [[0]': '`lcp[i][j]` = 后缀 `s[i:]` 与 `s[j:]` 的最长公共前缀，先全部置 0',
        8: lambda S, B, r: (f'`i = {S.i}`：倒着填，`lcp[i][·]` 依赖 `lcp[i+1][·]`' if S.i != B.get('i') else 'lcp 表填完'),
        14: lambda S, B, r: (f'`i = {S.i}`：`f[i]` 依赖更右边的 `f[i+j]`，所以倒着算' if S.i != B.get('i') else 'f 全部算完，答案是 `f[0]`'),
        'if s[i] == s[j]': lambda S, B, r: (f"`s[{S.i}] = {S.s[S.i]}` == `s[{S.j}] = {S.s[S.j]}` → 公共前缀可以在后面的基础上 +1" if S.s[S.i] == S.s[S.j]
                                           else f"`s[{S.i}] = {S.s[S.i]}` ≠ `s[{S.j}] = {S.s[S.j]}` → 公共前缀长度为 0"),
        'lcp[i][j] = lcp[i + 1][j + 1] + 1': '`lcp[{i}][{j}] = lcp[{i+1}][{j+1}] + 1` = =={lcp[i][j]}==',
        'if lcp[i][i + j] >= j': lambda S, B, r: (f'`lcp[{S.i}][{S.i + S.j}] = {S.lcp[S.i][S.i + S.j]} ≥ j = {S.j}` → `s[{S.i}:{S.i + S.j}] == s[{S.i + S.j}:{S.i + 2 * S.j}]`，==可以删掉前 j 个=='
                                                 if S.lcp[S.i][S.i + S.j] >= S.j else
                                                 f'`lcp[{S.i}][{S.i + S.j}] = {S.lcp[S.i][S.i + S.j]} < j = {S.j}` → 前 {S.j} 个和后面 {S.j} 个不相等，不能删'),
        'f[i] = max(f[i], f[i + j])': '删前 `{j}` 个后剩后缀 `s[{i+j}:]`：`f[{i}] = max({B.f[i]}, f[{i+j}]={f[i+j]})` = =={f[i]}==',
        'f[i] += 1': '再加上这次操作（最坏就是整个后缀一次删完，所以至少 1）：`f[{i}] = {f[i]}`',
        'return f[0]': '整个字符串 `s` 最多删 `f[0]` = =={ret}== 次',
    },
    cards=dict(
        one_liner='f[i] 表示后缀 s[i:] 的最大操作数，用 LCP 表 O(1) 判断前缀能不能删',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['每步可以删除整个 `s`，或者当前 `s` 的前 `i` 个字母等于接下来 `i` 个字母时删掉前 `i` 个',
                 '求删完 `s` 的==最大操作数==',
                 '示例：`"abcabcdabc"` → `2`；本视频：`"aabaab"` → `3`'],
        quote='定义 f[i] 表示删除后缀 s[i:] 所需的最大操作数……枚举删除字母的长度 j，如果 s[i:i+j] = s[i+j:i+2j]，那么可以删除，此时有转移 f[i] = f[i+j] + 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删掉前缀后剩下的就是后缀 → 状态定义成==后缀==的最大操作数',
              '判断两段子串相等：预处理 `lcp[i][j]`，`lcp[i][i+j] ≥ j` 即可',
              '`lcp` 倒着递推：`s[i] == s[j]` 时 `lcp[i][j] = lcp[i+1][j+1] + 1`'],
        summary=['时间、空间都是 `O(n^2)`',
                 '特判全部相同：答案就是 `n`（也避免这类用例最慢）',
                 '易错：`f[i]` 初值 0，最后统一 `+1`（对应整体删除这一步）；`j` 最大到 `(n-i)//2`',
                 '同类：Z 函数 / 后缀的前缀 LCP 题'],
    ),
)
