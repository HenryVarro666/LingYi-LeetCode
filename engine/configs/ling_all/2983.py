def _keep(name):
    last = [None]

    def f(S):
        v = S.get(name)
        if isinstance(v, (list, tuple, str)):
            last[0] = v
        return last[0]
    return f


def _case(S):
    if 'l2' not in S or 'r2' not in S or 'l1' not in S or 'r1' not in S:
        return ''
    l1, r1, l2, r2 = S['l1'], S['r1'], S['l2'], S['r2']
    if r2 <= r1:
        kind = '==区间包含=='
    elif r1 < l2:
        kind = '==区间不相交=='
    else:
        kind = '==区间相交但不包含=='
    return f'`[l1, r1] = [{l1}, {r1}]`（s），`[l2, r2] = [{l2}, {r2}]`（t）→ {kind}'


CONFIG = dict(
    num=2983, title='回文串重新排列查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 三种区间关系分类讨论',
    tags=['前缀和', '难度分 2780'],
    code='''
class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        # 分成左右两半，右半反转
        n = len(s) // 2
        t = s[n:][::-1]
        s = s[:n]

        # 预处理三种前缀和
        sum_s = [[0] * 26 for _ in range(n + 1)]
        for i, b in enumerate(s):
            sum_s[i + 1] = sum_s[i][:]
            sum_s[i + 1][ord(b) - ord('a')] += 1

        sum_t = [[0] * 26 for _ in range(n + 1)]
        for i, b in enumerate(t):
            sum_t[i + 1] = sum_t[i][:]
            sum_t[i + 1][ord(b) - ord('a')] += 1

        sum_ne = list(accumulate((x != y for x, y in zip(s, t)), initial=0))

        # 计算子串中各个字符的出现次数，闭区间 [l,r]
        def count(sum: List[List[int]], l: int, r: int) -> List[int]:
            return [x - y for x, y in zip(sum[r + 1], sum[l])]

        def subtract(s1: List[int], s2: List[int]) -> List[int]:
            for i, s in enumerate(s2):
                s1[i] -= s
                if s1[i] < 0:
                    return False
            return s1

        def check(l1: int, r1: int, l2: int, r2: int, sumS: List[List[int]], sumT: List[List[int]]) -> bool:
            # [0,l1-1] 有 s[i] != t[i] 或者 [max(r1,r2)+1,n-1] 有 s[i] != t[i]
            if sum_ne[l1] > 0 or sum_ne[n] - sum_ne[max(r1, r2) + 1] > 0:
                return False
            if r2 <= r1:  # 区间包含
                return count(sumS, l1, r1) == count(sumT, l1, r1)
            if r1 < l2:  # 区间不相交
                # [r1+1,l2-1] 都满足 s[i] == t[i]
                return sum_ne[l2] - sum_ne[r1 + 1] == 0 and \\
                    count(sumS, l1, r1) == count(sumT, l1, r1) and \\
                    count(sumS, l2, r2) == count(sumT, l2, r2)
            # 区间相交但不包含
            s1 = subtract(count(sumS, l1, r1), count(sumT, l1, l2 - 1))
            s2 = subtract(count(sumT, l2, r2), count(sumS, r1 + 1, r2))
            return s1 and s2 and s1 == s2

        ans = [False] * len(queries)
        for i, (l1, r1, c, d) in enumerate(queries):
            l2, r2 = n * 2 - 1 - d, n * 2 - 1 - c
            ans[i] = check(l1, r1, l2, r2, sum_s, sum_t) if l1 <= l2 else \\
                     check(l2, r2, l1, r1, sum_t, sum_s)
        return ans
''',
    call='Solution().canMakePalindromeQueries("aabcbcaa", [[0,2,4,6],[0,0,4,5],[1,2,5,6]])',
    expect=[True, True, False],
    views=[
        dict(type='string', var=_keep('s'), label='s（左半）', h=170, window=('l1', 'r1'), cell=70),
        dict(type='string', var='t', label='t（右半反转）', h=170, window=('l2', 'r2'), window_color='orange', cell=70),
        dict(type='array', var='sum_ne', label='sum_ne：前缀里 s[i] ≠ t[i] 的个数', h=170, cell=70),
        dict(type='text', fn=lambda S: _case(S) if S.get('_line', 0) >= 35 else '', size=30),
    ],
    watch=['n', 'l1', 'r1', 'l2', 'r2', ('ans', 'ans', 'green')],
    max_steps=70,
    skip=['sum_s[i + 1]', 'sum_t[i + 1]', 'for i, b in enumerate(s)', 'for i, b in enumerate(t)', 'ans = [False]', 'def ', 'for _ in', 'for i, s in enumerate(s2)', 's1[i] -= s', 'if s1[i] < 0'],
    captions={
        'n = len(s) // 2': '一半长度 `n = {n}`',
        't = s[n:][::-1]': '右半反转得到 `t = {t!r}`：回文 = ==s 和 t 逐位相同==',
        's = s[:n]': '左半 `s = {s!r}`',
        'sum_s = [[0]': '预处理 `sum_s`：`s` 每个前缀里 26 个字母各出现几次（下面循环逐个累加，省略）',
        'sum_t = [[0]': '同样预处理 `sum_t`',
        'sum_ne = list': '`sum_ne[i]`：前 i 位里 `s[i] != t[i]` 的个数 = `{sum_ne}`',
        'l2, r2 = ': '右半反转了，`c, d` 换成 `l2 = {l2}`，`r2 = {r2}`；`l1 = {l1}`，`r1 = {r1}`',
        'if sum_ne[l1] > 0': lambda S, B, r: (f'不能动的两头必须 s[i] = t[i]：`sum_ne[{S.l1}] = {S.sum_ne[S.l1]}`，右端 `{S.sum_ne[S.n] - S.sum_ne[max(S.r1, S.r2) + 1]}` → ' + ('有不同，直接 ==false==' if S.sum_ne[S.l1] > 0 or S.sum_ne[S.n] - S.sum_ne[max(S.r1, S.r2) + 1] > 0 else '两头都相同，继续')),
        'if r2 <= r1': '`r2 = {r2}` {"<=" if r2 <= r1 else ">"} `r1 = {r1}` → {"==区间包含==" if r2 <= r1 else "不包含"}',
        'return count(sumS, l1, r1) == count(sumT, l1, r1)': lambda S, B, r: f'包含：`s` 在 `[{S.l1},{S.r1}]` 可随意排列，只要和 `t` 同区间字符次数相同 → =={r}==',
        'if r1 < l2': '`r1 = {r1}` {"<" if r1 < l2 else ">="} `l2 = {l2}` → {"==不相交==" if r1 < l2 else "==相交但不包含=="}',
        'return sum_ne[l2]': lambda S, B, ret: f'不相交：中间 `[{S.r1+1}, {S.l2-1}]` 逐位相同，且两段各自的字母次数要相等',
        's1 = subtract': '`s` 的 `[{l1},{r1}]` 字符次数，减去 `t` 的 `[{l1},{l2-1}]`（这段必须靠 s 来配）→ `s1` 是剩余字符',
        's2 = subtract': '`t` 的 `[{l2},{r2}]` 字符次数，减去 `s` 的 `[{r1+1},{r2}]` → `s2` 是剩余字符',
        'return s1 and s2': lambda S, B, r: f'相交：不够配（出现负数）就 false；剩下的 `s1`、`s2` 必须相等 → =={bool(r)}==',
        'return [x - y': lambda S, B, ret: f'区间 `[{S.l}, {S.r}]` 内各字母次数：`' + str({chr(97 + i): v for i, v in enumerate(ret) if v}) + '`',
        30: lambda S, B, ret: ('配不上：出现负数 → `False`' if ret is False else f'减完剩下的字母次数：`' + str({chr(97 + i): v for i, v in enumerate(ret) if v}) + '`'),
        'return ans': '全部查询答完：`{ans}`',
    },
    cards=dict(
        one_liner='切成 s 和反转的 t，回文 = 两串相等；可动区间看次数、不可动区间看逐位相同',
        complexity='时间 `O((n+q)·26)`，空间 `O(n·26)`',
        problem=['长为偶数 `n` 的 `s`，每个查询 `[a,b,c,d]`：重排 `s[a:b]` 和 `s[c:d]`（一个在左半，一个在右半）',
                 '问能不能变成回文串，查询互相独立',
                 '示例：`"abcabc"`，`[[1,1,3,5],[0,2,5,5]]` → `[true,true]`；本视频用 `"aabcbcaa"`'],
        quote='把输入的字符串记作大写 S。为方便计算，把 S 均分为左右两个字符串，其中右半部分反转。左半和右半分别记作 s 和 t。',
        quote_src='—— 灵茶山艾府题解',
        idea=['右半反转后，回文 = `s` 和 `t` 逐位相同；询问的 `c, d` 换成 `n*2-1-d, n*2-1-c`',
              '三个前缀和：`sum_s`、`sum_t` 统计字符次数，`sum_ne` 统计 `s[i] != t[i]`',
              '`[0,l1-1]` 和 `[max(r1,r2)+1,n-1]` 不能动，必须 `sum_ne` 为零；再按区间包含、不相交、相交三类判断'],
        summary=['时间 `O((n+q)|Σ|)`，|Σ| = 26',
                 '要保证 `l1 <= l2`，否则交换 s、t 的角色再调用 `check`',
                 '相交时 `subtract` 出现负数就是配不上，要及时返回 false',
                 '视频里 `sum_s`、`sum_t` 的构建循环省略了逐步动画'],
    ),
)
