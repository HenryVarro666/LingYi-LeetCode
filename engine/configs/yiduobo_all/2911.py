S0, K0 = 'abcac', 2


def _fcolor(S, r, c, v):
    if S.get('_line', 0) >= 24 and 'p' in S and 'i' in S:
        if (r, c) == (S['p'], S['i'] - 1):
            return 'green'
        return None
    if r == S.get('i') and c == S.get('j') and S.get('_line', 0) < 24:
        return 'yellow'
    return None


def _gcolor(S, r, c, v):
    if 'p' in S and 'i' in S and 'j' in S and S.get('_line', 0) >= 24:
        if (r, c) == (S['i'], S['j']):
            return 'yellow'
        if (r, c) == (S['p'], S['j'] - 1):
            return 'blue'
    return None


def _text(S):
    if S.get('_line', 0) >= 24 and 'p' in S and 'i' in S and 'j' in S:
        return f'`g[{S["i"]}][{S["j"]}]` = min( `g[p][{S["j"]-1}]` + `cost(p, {S["i"]-1})` )，`p = {S["p"]}`'
    return '`f[i][j]` = 把 `s[i..j]` 变成半回文串的最小代价（`None` = 长度 1，没有合法 `d`）'


CONFIG = dict(
    num=2911, title='得到 K 个半回文串的最少修改次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='先预处理 cost，再枚举断点划分 DP',
    tags=['灵神题单', '动态规划', '难度分 2608'],
    code='''
class Solution(object):
    def minimumChanges(self, s, k):

        n = len(s)
        f = [[None] * n for _ in range(n)]
        for i in range(n - 1):
            for j in range(i + 1, n):
                length = j - i + 1
                for d in range(1, length):
                    if length % d == 0:
                        cnt = 0
                        for offset in range(d):
                            left = i + offset
                            right = j - d + offset + 1
                            while left < right:
                                if s[left] != s[right]:
                                    cnt += 1
                                left += d
                                right -= d
                            
                        if f[i][j] is None or f[i][j] > cnt:
                            f[i][j] = cnt
        
        g = [[None] * (k + 1) for _ in range(n + 1)]
        g[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                for p in range(i):
                    if g[p][j - 1] is None:
                        continue
                    if f[p][i - 1] is None:
                        continue
                    if g[i][j] is None or g[i][j] > g[p][j - 1] + f[p][i - 1]:
                        g[i][j] = g[p][j - 1] + f[p][i - 1]
        
        return g[-1][-1]
''',
    call=f'Solution().minimumChanges({S0!r}, {K0})',
    expect=1,
    max_steps=60,
    skip=['cnt = 0', 'length = j', 'left += d', 'right -= d', 'for offset in range', 'left = i + offset',
          'right = j - d', 'g[0][0] = 0', 'continue', 'n = len(s)'],
    views=[
        dict(type='table', var='f', label='f[i][j]：s[i..j] 的最小代价（行 i，列 j）', h=300, cell=64,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_fcolor),
        dict(type='table', var='g', label='g[i][j]：前 i 个字符切成 j 段的最小代价', h=360, cell=64,
             rows=lambda S: [f'前{k}个' for k in range(len(S0) + 1)], cols=lambda S: [f'{k}段' for k in range(K0 + 1)],
             color=_gcolor),
        dict(type='text', fn=_text, size=24, h=60),
    ],
    watch=['i', 'j', 'd', 'cnt', 'p'],
    captions={
        'f = [[None]': '`f[i][j]` 记 `s[i..j]` 的最小代价，先全设 `None`（长度 1 的串没有合法因子 `d`）',
        'for i in range(n - 1)': '预处理：子串左端 `i = {i}`（长度至少 2，所以只到 `n-2`）',
        'for j in range(i + 1': '子串右端 `j = {j}`：子串 `s[{i}..{j}]` = `{s[i:j+1]!r}`',
        'for d in range(1, length)': '枚举 `d = {d}`，必须小于长度 `{length}`',
        'if length % d == 0': lambda S, B, r: (f'`{S.length} % {S.d} == 0`：`d` 整除长度，可以分组' if S.length % S.d == 0
                                               else f'`{S.length} % {S.d} != 0`：不是因子，跳过'),
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：这一组还没配完' if S.left < S.right
                                               else f'`left = {S.left} >= right = {S.right}`：这一组指针相遇，配完'),
        'if s[left] != s[right]': lambda S, B, r: (f'`s[{S.left}] = {S.s[S.left]!r}` ≠ `s[{S.right}] = {S.s[S.right]!r}`：回文要求相等 → 要改 1 个' if S.s[S.left] != S.s[S.right]
                                                   else f'`s[{S.left}] = {S.s[S.left]!r}` = `s[{S.right}] = {S.s[S.right]!r}`：已经匹配，不用改'),
        'cnt += 1': '`cnt = {cnt}`',
        'if f[i][j] is None or': lambda S, B, r: ('`f[i][j]` 还是 `None` 或比 `cnt` 大 → 用 `cnt` 更新' if S.f[S.i][S.j] is None or S.f[S.i][S.j] > S.cnt
                                                  else f'`f[{S.i}][{S.j}] = {S.f[S.i][S.j]}` 已经不大于 `cnt = {S.cnt}`，保持'),
        'f[i][j] = cnt': '各个 `d` 里取最小：`f[{i}][{j}] = {cnt}`',
        'g = [[None]': '`g[i][j]`：前 `i` 个字符切成 `j` 段的最小代价；`g[0][0] = 0`，其余 `None` = 不可能',
        'for i in range(1, n + 1)': '现在看前 `i = {i}` 个字符',
        'for j in range(1, k + 1)': '切成 `j = {j}` 段',
        'for p in range(i)': lambda S, B, r: (f'枚举最后一段的起点 `p = {S.p}`：最后一段是 `s[{S.p}..{S.i-1}]`，前面 `{S.p}` 个字符切成 `{S.j-1}` 段' if S.p != B.get('p') or S.i != B.get('i') or S.j != B.get('j')
                                              else '`p` 枚举完了'),
        'if g[p][j - 1] is None': lambda S, B, r: ('前面 `p` 个字符切不成 `j-1` 段 → 此路不通，跳过' if S.g[S.p][S.j - 1] is None
                                                   else f'`g[{S.p}][{S.j-1}] = {S.g[S.p][S.j-1]}`：前缀可行'),
        'if f[p][i - 1] is None': lambda S, B, r: ('最后一段长度 1，不可能是半回文串 → 跳过' if S.f[S.p][S.i - 1] is None
                                                   else f'最后一段 `s[{S.p}..{S.i-1}]` 代价 `f = {S.f[S.p][S.i-1]}`'),
        'if g[i][j] is None or g[i][j] >': '候选 `g[{p}][{j-1}] + f[{p}][{i-1}]` = `{g[p][j-1] + f[p][i-1]}`，比当前 `g[{i}][{j}]` 小就更新',
        'g[i][j] = g[p][j - 1] + f[p][i - 1]': '更新：`g[{i}][{j}] = {g[i][j]}`',
        'return g[-1][-1]': '前 `n` 个字符切成 `k` 段：=={g[-1][-1]}==',
    },
    cards=dict(
        one_liner='先把所有子串的代价算好，再枚举最后一段的起点',
        complexity='时间 `O(n³)`，空间 `O(n²)`',
        problem=['把 `s` 切成 `k` 段，每段改成半回文串，求最少修改字符数',
                 '半回文：选因子 `d`，下标模 `d` 同余的字符组成的每组都是回文',
                 '示例：`s = "abcac", k = 2` → `1`'],
        quote='令g[i][j]表示前i个字符，切分成j个半回文子串所需的最小代价，那么对于g[i][j]，可以枚举前j - 1个回文子串的终点p',
        quote_src='—— yiduobo 题解原文',
        idea=['`cost(l, r)` 可以先预处理：字符串是常量，每个子串枚举 `d` 取最小',
              '一个 `d` 下，`offset` 从 0 到 `d-1`，每组两个指针 `left/right` 以 `d` 为步长往中间走',
              '`g[i][j] = min(g[p][j-1] + cost(p, i-1))`，不可行的状态用 `None` 表示'],
        summary=['外面三层循环看似 `O(n⁴)`，但内两层合起来每个字符只访问一遍 → 预处理 `O(n³)`',
                 'DP 部分是 `O(n² k)`：`i`、`j`、`p` 三层循环',
                 '易错：长度 1 的子串 `f` 保持 `None`，转移时必须跳过',
                 '对比灵神：yiduobo 用「前 i 个字符 / 切 j 段」的二维表，灵神用「分 i+1 段」且把表压成一维'],
    ),
)
