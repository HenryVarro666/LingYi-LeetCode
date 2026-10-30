S0 = 'bcdaxe'


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j < i or S.get('_line', 0) in (11, 12):
        return None if not (v is True) else 'green'
    if v is True:
        base = 'green'
    else:
        base = None
    if r == i and c == j:
        return 'yellow'
    if j > i and r == i + 1 and c == j - 1 and S.get('_line', 0) in (14, 15):
        return 'cyan'
    return base


def _fcell(S, k, v):
    return 'yellow' if k == S.get('i') and S.get('_line', 0) >= 25 else None


CONFIG = dict(
    num=3563, title='移除相邻字符后字典序最小的字符串', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP + 线性 DP（递推）',
    tags=['灵神题单', '动态规划', '难度分 2585'],
    code='''
def is_consecutive(x: int, y: int) -> bool:
    d = abs(x - y)
    return d == 1 or d == 25

class Solution:
    def lexicographicallySmallestString(self, s: str) -> str:
        a = list(map(ord, s))  # 避免反复调用 ord
        n = len(s)

        can_be_empty = [[False] * n for _ in range(n)]
        for i in range(n - 2, -1, -1):
            can_be_empty[i + 1][i] = True  # 空串
            for j in range(i + 1, n, 2):
                # 性质 2
                if is_consecutive(a[i], a[j]) and can_be_empty[i + 1][j - 1]:
                    can_be_empty[i][j] = True
                    continue
                # 性质 3
                for k in range(i + 1, j - 1, 2):
                    if can_be_empty[i][k] and can_be_empty[k + 1][j]:
                        can_be_empty[i][j] = True
                        break

        f = [''] * (n + 1)
        for i in range(n - 1, -1, -1):
            # 包含 s[i]
            res = s[i] + f[i + 1]
            # 不包含 s[i]，注意 s[i] 不能单独消除，必须和其他字符一起消除
            for j in range(i + 1, n, 2):
                if can_be_empty[i][j]:  # 消除 s[i] 到 s[j]
                    res = min(res, f[j + 1])
            f[i] = res
        return f[0]
''',
    call=f'Solution().lexicographicallySmallestString({S0!r})',
    expect='baxe',
    skip=['a = list(map', 'n = len(s)', 'for j in range', 'for k in range', 'continue', 'break', 'd = abs', 'return d =='],
    views=[
        dict(type='string', var='s', label='s（蓝 = i，粉 = j）', h=215, cell=80, pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='table', var='can_be_empty', label='can_be_empty[i][j]：s[i..j] 能否完全消除（绿 = 能）', h=320, cell=54,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_cell),
        dict(type='array', var='f', label='f[i]：后缀 s[i:] 能得到的字典序最小字符串', h=190, cell=110,
             pointers={'i': 'blue'}, color=_fcell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'purple'), ('res', 'res', 'green')],
    captions={
        'can_be_empty = [[False]': '`can_be_empty[i][j]`：`s[i..j]` 能否被完全消除，先全设为 False',
        'for i in range(n - 2': lambda S, B, r: ('`i = %d`：区间 DP 的左端点倒序，保证 `i+1` 行已算好' % S.i if 'i' not in B or B.i != S.i or S.i != 0 else '左端点枚举完毕，所有区间的「能否消除」都算好了'),
        'can_be_empty[i + 1][i] = True': '空串一定能消除：`can_be_empty[{i+1}][{i}] = True`',
        'if is_consecutive': lambda S, B, r: (
            f'性质 2：`s[{S.i}]={S.s[S.i]}` 与 `s[{S.j}]={S.s[S.j]}` ' + ('==连续==' if abs(S.a[S.i] - S.a[S.j]) in (1, 25) else '不连续')
            + f'，且中间 `[{S.i+1}, {S.j-1}]` ' + ('能消除' if S.can_be_empty[S.i + 1][S.j - 1] else '不能消除') + ' → '
            + ('成立' if abs(S.a[S.i] - S.a[S.j]) in (1, 25) and S.can_be_empty[S.i + 1][S.j - 1] else '不成立')),
        'can_be_empty[i][j] = True': '`s[{i}..{j}]` 能完全消除（像一对括号包住可消除的内部）',
        'if can_be_empty[i][k]': '性质 3：在 `k={k}` 处切开，`[{i},{k}]` 和 `[{k+1},{j}]` 是否都能消除',
        'f = [': '`f[i]` = 后缀 `s[i:]` 的最优答案，`f[n]` 是空串',
        'for i in range(n - 1': lambda S, B, r: ('`i = %d`：后缀 DP，倒序枚举；越靠前的字符对字典序影响越大' % S.i if S.i != B.get('i') or S.get('res') is None or S.i != 0 or S.f[0] == '' else '后缀都算完了，答案在 `f[0]`'),
        'res = s[i] + f[i + 1]': '情况一：保留 `s[{i}]`，答案 = `{s[i]!r}` + `f[{i+1}]` = =={res!r}==',
        'if can_be_empty[i][j]': lambda S, B, r: (
            f'情况二：`s[{S.i}..{S.j}]` ' + ('==能消除==，可以直接跳到 `f[%d]`' % (S.j + 1) if S.can_be_empty[S.i][S.j] else '不能消除，跳过')),
        'res = min(res, f[j + 1])': '消除 `s[{i}..{j}]` 后剩 `f[{j+1}]` = {f[j+1]!r}，与现有最优取小：`res` = =={res!r}==',
        'f[i] = res': '`f[{i}] = {res!r}`',
        'return f[0]': '整个字符串的答案 `f[0]` = =={ret!r}==',
    },
    cards=dict(
        one_liner='能消除的子串像合法括号；再用后缀 DP 选「留还是消」',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['每次可删掉一对相邻且字母表上连续的字符（`a` 与 `z` 也算），删除后左右合并',
                 '返回操作任意次后==字典序最小==的字符串',
                 '示例：`"zdce"` → `"zdce"`（删了反而更大）；本视频：`"bcdaxe"` → `"baxe"`'],
        quote='如果把一对「连续」字符看成一对左右括号，那么消除的子串一定是一个合法括号字符串。',
        quote_src='—— 灵茶山艾府题解（前言）',
        idea=['第一个区间 DP：`s[i..j]` 能消除 = 两端连续且中间能消除，或能切成两段都能消除',
              '线性 DP：`f[i]` = 后缀 `s[i:]` 的最小串；保留 `s[i]`，或消掉 `s[i..j]` 跳到 `f[j+1]`',
              '被消除的子串长度必为偶数，所以 `j`、`k` 的步长是 2'],
        summary=['时间 `O(n^3)`，空间 `O(n^2)`',
                 '易错：`s[i]` 不能单独消除，必须和别的字符一起，所以 `j` 从 `i+1` 起',
                 '易错：不是能消就消，样例 `"zdce"` 保留更小',
                 '灵神还给了记忆化搜索写法（写法一），这里演示递推（写法二）',
                 '同类：区间 DP「能否完全消除」，类似合法括号匹配'],
    ),
)
