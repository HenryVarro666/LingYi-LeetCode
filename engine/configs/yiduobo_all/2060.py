def _cells(S):
    f = S.get('f')
    out = {}
    if not f:
        return out
    for i, row in enumerate(f):
        for j, c in enumerate(row):
            if c:
                out[f'f[{i}][{j}]'] = sorted(c)
    return out


def _col(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    return None


CONFIG = dict(
    num=2060, title='同源字符串检测', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[i][j] 存长度差集合（前推式 DP）',
    tags=['灵神题单·动态规划', '难度分 2804'],
    code='''
class Solution(object):
    def possiblyEquals(self, s1, s2):

        m = len(s1)
        n = len(s2)
        f = [[set() for _ in range(n + 1)] for _ in range(m + 1)]
        f[0][0].add(0)

        for i in range(m + 1):
            for j in range(n + 1):
                for k in f[i][j]:
                    if k > 0:
                        p = j
                        now = 0
                        while p < n and p < j + 3 and s2[p] >= '1' and s2[p] <= '9':
                            now = now * 10 + int(s2[p])
                            f[i][p + 1].add(k - now)
                            p += 1
                    
                        if j < n and (s2[j] < '1' or s2[j] > '9'):
                            f[i][j + 1].add(k - 1)

                    elif k < 0:
                        p = i
                        now = 0
                        while p < m and p < i + 3 and s1[p] >= '1' and s1[p] <= '9':
                            now = now * 10 + int(s1[p])
                            f[p + 1][j].add(k + now)
                            p += 1
                        
                        if i < m and (s1[i] < '1' or s1[i] > '9'):
                            f[i + 1][j].add(k + 1)
                    
                    else:
                        if i < m and j < n and s1[i] == s2[j] and k == 0:
                            f[i + 1][j + 1].add(0)
                        
                        p = i
                        now = 0
                        while p < m and p < i + 3 and s1[p] >= '1' and s1[p] <= '9':
                            now = now * 10 + int(s1[p])
                            f[p + 1][j].add(now)
                            p += 1
                        
                        p = j
                        now = 0
                        while p < n and p < j + 3 and s2[p] >= '1' and s2[p] <= '9':
                            now = now * 10 + int(s2[p])
                            f[i][p + 1].add(-now)
                            p += 1

        return 0 in f[m][n]
''',
    call='Solution().possiblyEquals("a2b", "3b")',
    expect=True,
    views=[
        dict(type='string', var='s1', label='s1（m = 3）', cell=70, h=150, pointers={'i': 'blue'}),
        dict(type='string', var='s2', label='s2（n = 2）', cell=70, h=150, pointers={'j': 'pink'}),
        dict(type='table', var=lambda S: [[len(c) for c in row] for row in S['f']] if S.get('f') else [[0]],
             label='f[i][j] 里元素个数（黄 = 当前 (i, j)）', h=190, cell=52, color=_col),
        dict(type='map', var=_cells, label='非空的 f[i][j]：k = s1 比 s2 多的长度', fmt=lambda k, v: f'{k} = {v}', h=240, font=24),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'orange')],
    skip=['m = len', 'n = len', 'for j in range', 'for k in f', 'p = i', 'p = j', 'now = 0', 'now = now * 10', 'p += 1'],
    captions={
        'f = [[set()': '`f[i][j]` 是集合：`s1[:i]` 与 `s2[:j]` 匹配时，原串长度差 `k = len1 − len2` 的所有可能',
        'f[0][0].add(0)': '起点：什么都没读，长度差 `0`',
        'for i in range': lambda B, S, r: (f'`i = {S.i + 1}`：按 `i`、`j` 从小到大推，保证 `f[i][j]` 用到时已填完' if S.i + 1 <= S.m else '所有状态都填完了，看结果'),
        'if k > 0': lambda B, S, r: (f'`f[{S.i}][{S.j}]` 里有 `k = {S.k}`：==s1 多出 {S.k} 个字符== → 只尝试用 s2 补位' if S.k > 0
                                      else f'`k = {S.k}` 不大于 0，看下一种情况'),
        'while p < n and p < j + 3': lambda B, S, r: ('s2 从 `j` 起最多 3 位数字，连成 `now`，当作 s2 的一段长度来补位' if S.p < S.n and S.s2[S.p] in '123456789' and S.p < S.j + 3
                                                         else '没有（更多）数字可展开'),
        'f[i][p + 1].add(k - now)': '用 s2 的数字 `{now}` 补位：`k − now = {k - now}` → 加入 `f[{i}][{p+1}]`',
        'if j < n and (s2[j] < ': lambda B, S, r: (f'`s2[{S.j}] = {S.s2[S.j]!r}` 是字母 → 可以抵掉 s1 多出的一个字符' if S.j < S.n and not ('1' <= S.s2[S.j] <= '9')
                                                      else '`s2[j]` 是数字（或已读完），不能当字母补位'),
        'f[i][j + 1].add(k - 1)': '字母补位：`k − 1 = {k - 1}` → 加入 `f[{i}][{j+1}]`',
        'elif k < 0': lambda B, S, r: (f'`k = {S.k} < 0`：==s2 多出 {-S.k} 个字符== → 只尝试用 s1 补位' if S.k < 0 else '`k = 0`：既不多也不少 → 走最后一种情况'),
        'while p < m and p < i + 3': lambda B, S, r: ('s1 从 `i` 起最多 3 位数字，连成 `now`' if S.p < S.m and S.s1[S.p] in '123456789' and S.p < S.i + 3
                                                         else '没有（更多）数字可展开'),
        'f[p + 1][j].add(k + now)': '用 s1 的数字 `{now}` 补位：`k + now = {k + now}` → 加入 `f[{p+1}][{j}]`',
        'if i < m and (s1[i] < ': lambda B, S, r: (f'`s1[{S.i}] = {S.s1[S.i]!r}` 是字母 → 抵掉 s2 多出的一个字符' if S.i < S.m and not ('1' <= S.s1[S.i] <= '9')
                                                      else '`s1[i]` 是数字（或已读完），不能当字母补位'),
        'f[i + 1][j].add(k + 1)': '字母补位：`k + 1 = {k + 1}` → 加入 `f[{i+1}][{j}]`',
        'if i < m and j < n and s1[i] == s2[j]': lambda B, S, r: (f'`k = 0`：长度相同。`s1[{S.i}] = {S.s1[S.i]!r}`，`s2[{S.j}] = {S.s2[S.j]!r}`' + ('，相同 → 一起前进' if S.s1[S.i] == S.s2[S.j] else '，不同')
                                                                    if S.i < S.m and S.j < S.n else '`k = 0`：有一边已读完，不能配字母'),
        'f[i + 1][j + 1].add(0)': '两边字母相同，一起前进：`f[{i+1}][{j+1}]` 加入 `0`',
        'f[p + 1][j].add(now)': '`k = 0` 时 s1 展开数字：s1 多出 `{now}` → 加入 `f[{p+1}][{j}]`',
        'f[i][p + 1].add(-now)': '`k = 0` 时 s2 展开数字：s2 多出 `{now}` → 加入 `f[{i}][{p+1}]`（即 `k = −{now}`）',
        'return 0 in f[m][n]': '`f[{m}][{n}]` = {sorted(f[m][n])}：含 `0` → 两边读完且长度差 0 → =={ret}=='
    },
    max_steps=90,
    cards=dict(
        one_liner='f[i][j] 记下长度差 k：谁多出来，就只让另一边去补',
        complexity='时间 `O(m·n·K)`，空间 `O(m·n·K)`，`K` 是集合大小（约 1000）',
        problem=['`s1`、`s2` 是编码串：数字表示一段子串被替换成了它的长度',
                 '问是否存在同一个原字符串，能同时编码成 `s1` 和 `s2`',
                 '示例：`"l123e"` 和 `"44"` → `true`；本视频：`"a2b"` 与 `"3b"` → `true`'],
        quote='因此在某一时刻k大于等于0时，这些数字始终是要被s2中的字符匹配掉的，因此在这里没必要继续考虑往里面添加s1的字符，而是尝试添加s2中的字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j][k]`：`s1` 前 `i`、`s2` 前 `j` 个字符，`s1` 比 `s2` 多出 `k` 个可用字符',
              '`k > 0` 只让 s2 补（数字或字母），`k < 0` 只让 s1 补，`k = 0` 两边都可以展开或配字母',
              '`k` 实际取值稀疏，改成每格一个集合，最后看 `0 in f[m][n]`'],
        summary=['时间 `O(m·n·K)`，`K` 为每格集合大小（约 ±1000）',
                 '易错：数字最多连续 3 位，每多读一位都要单独转移',
                 '易错：`k = 0` 时字母只能和对面字母相等才能同时前进',
                 '原文为 Python 2 风格，本题代码无需改动（仅删去了类型说明文档字符串）',
                 '对比灵神：他用递归 + `vis` 去重；这里是顺序填表，用集合存稀疏的 `k`'],
    ),
)
