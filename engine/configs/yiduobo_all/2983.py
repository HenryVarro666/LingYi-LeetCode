def _cmp(S):
    if 'sx' not in S or 'ty' not in S or 'tx' not in S or 'sy' not in S:
        return ''
    sx, sy, tx, ty = S['sx'], S['sy'], S['tx'], S['ty']
    if sy < tx:
        kind = '==不相交=='
    elif ty <= sy:
        kind = '==相互包含=='
    else:
        kind = '==部分重叠=='
    return f's 的可调整段 `[{sx}, {sy}]`，t 的可调整段 `[{tx}, {ty}]`（下标从 1 起）→ {kind}'


CONFIG = dict(
    num=2983, title='回文串重新排列查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀计数 + same 前缀 + 三类区间',
    tags=['前缀和', '难度分 2780'],
    code='''
class Solution(object):
    def canMakePalindromeQueries(self, s, queries):

        n = len(s) // 2
        t = s[len(s) : n - 1 : -1]
        s = s[:n]

        char_s = [Counter()]
        char_t = [Counter()]
        same = [0]

        for index in range(n):
            char_s.append(char_s[-1].copy())
            char_s[-1][s[index]] += 1

            char_t.append(char_t[-1].copy())
            char_t[-1][t[index]] += 1

            same.append(same[-1])
            if s[index] == t[index]:
                same[-1] += 1

        def check_same(x, y):
            if x > y:
                return True
            return same[y] == same[x - 1] + y - x + 1
        
        def check_char(x, y):
            for char in char_s[y]:
                if char_s[y][char] - char_s[x - 1][char] != char_t[y][char] - char_t[x - 1][char]:
                    return False
            return True

        def check(s, t, sx, sy, tx, ty, char_s, char_t):
            if sy < tx:
                return check_same(1, sx - 1) and check_char(sx, sy) and \\
                        check_same(sy + 1, tx - 1) and check_char(tx, ty) and check_same(ty + 1, n)

            elif ty <= sy:
                return check_same(1, sx - 1) and check_char(sx, sy) and check_same(sy + 1, n)
            
            else:
                if not check_same(1, sx - 1) or not check_same(ty + 1, n):
                    return False

                char_subs = Counter()
                for char in char_s[sy]:
                    char_subs[char] = char_s[sy][char] - char_s[sx - 1][char]

                char_subt = Counter()
                for char in char_t[ty]:
                    char_subt[char] = char_t[ty][char] - char_t[tx - 1][char]

                for char in char_t[tx - 1]:
                    cnt = char_t[tx - 1][char] - char_t[sx - 1][char]
                    if cnt > char_subs[char]:
                        return False
                    char_subs[char] -= cnt

                for char in char_s[ty]:
                    cnt = char_s[ty][char] - char_s[sy][char]
                    if cnt > char_subt[char]:
                        return False
                    char_subt[char] -= cnt
                
                for char in char_s[ty]:
                    if char_s[ty][char] - char_s[sx - 1][char] != char_t[ty][char] - char_t[sx - 1][char]:
                        return False

                return True

        res = []
        for sx, sy, tx, ty in queries:
            sx += 1
            sy += 1
            tx, ty = n + n - ty, n + n - tx

            if sx > tx:
                res.append(check(t, s, tx, ty, sx, sy, char_t, char_s))
            else:
                res.append(check(s, t, sx, sy, tx, ty, char_s, char_t))

        return res
''',
    call='Solution().canMakePalindromeQueries("aabcbcaa", [[0,2,4,6],[0,0,4,5],[1,2,5,6]])',
    expect=[True, True, False],
    views=[
        dict(type='string', var='s', label='s（左半，下标从 0 起；框 = 可调整）', h=170, cell=70,
             color=lambda S, i, v: 'cyan' if 'sx' in S and 'sy' in S and S['sx'] - 1 <= i <= S['sy'] - 1 else None),
        dict(type='string', var='t', label='t（右半反转）', h=170, cell=70,
             color=lambda S, i, v: 'orange' if 'tx' in S and 'ty' in S and S['tx'] - 1 <= i <= S['ty'] - 1 else None),
        dict(type='array', var='same', label='same：前缀里 s[i] = t[i] 的个数', h=170, cell=70),
        dict(type='text', fn=lambda S: _cmp(S) if S.get('_line', 0) >= 33 else '', size=28),
    ],
    watch=['n', 'sx', 'sy', 'tx', 'ty', ('res', 'res', 'green')],
    max_steps=70,
    skip=['char_s.append', 'char_t.append', 'char_s[-1][s[index]]', 'char_t[-1][t[index]]', 'same.append', 'same[-1] += 1', 'char_s = [Counter', 'char_t = [Counter', 'sx += 1', 'sy += 1',
          'for index in range(n)', 'for char in char_s[sy]', 'char_subs[char] = char_s', 'for char in char_t[ty]', 'char_subt[char] =',
          'cnt = char_t', 'cnt = char_s[ty][char] - char_s[sy]', 'char_subs[char] -= cnt', 'char_subt[char] -= cnt', 'for char in char_t[tx - 1]', 'for char in char_s[ty]', 'for char in char_s[y]', 'if x > y', 'if sx > tx', 'res = []', 's = s[:n]'],
    captions={
        'n = len(s) // 2': '一半长度 `n = {n}`',
        't = s[len(s)': '把后半部分翻转：`t = {t!r}`，回文就变成==两个串相等==',
        's = s[:n]': '前半 `s = {s!r}`',
        'same = [0]': '`char_s`、`char_t`：前缀里每种字符的次数；`same`：前缀里 `s[i] = t[i]` 的个数',
        'if s[index] == t[index]': '位置 `{index}`：`s = {s[index]!r}`，`t = {t[index]!r}`，同时更新两份字符计数；{"相同 → `same` 加 1" if s[index] == t[index] else "不同 → `same` 不变"}',
        'tx, ty = n + n - ty': '右半反转后，查询区间对应到 `t` 上：`tx = {tx}`，`ty = {ty}`（`sx = {sx}`，`sy = {sy}`，都从 1 起）；要保证 s 的区间在左边，否则交换 s、t',
        'if sx > tx': '`sx = {sx}` {">" if sx > tx else "<="} `tx = {tx}` → {"交换 s、t，保证 s 的区间在左边" if sx > tx else "不用交换"}',
        'if sy < tx': '`sy = {sy}` {"<" if sy < tx else ">="} `tx = {tx}` → {"==不相交==：5 段，1、3、5 要相同，2、4 比次数" if sy < tx else "有重叠"}',
        'elif ty <= sy': '`ty = {ty}` {"<=" if ty <= sy else ">"} `sy = {sy}` → {"==相互包含==：3 段，两头要相同，中间比次数" if ty <= sy else "==部分重叠=="}',
        'return check_same(1, sx - 1) and check_char(sx, sy) and check_same(sy + 1, n)': '包含：`[1, {sx-1}]` 和 `[{sy+1}, {n}]` 必须逐位相同，`[{sx}, {sy}]` 内字符次数要相同',
        'return check_same(1, sx - 1) and check_char(sx, sy) and \\': '不相交：1、3、5 段逐位相同，2、4 段字符次数相同',
        'if not check_same(1, sx - 1)': '部分重叠：先看不能调整的两头 `[1, {sx-1}]` 和 `[{ty+1}, {n}]` 是否相同',
        'char_subs = Counter()': '`char_subs`：统计 s 在 `[{sx},{sy}]` 里的字符次数（循环省略）',
        'char_subt = Counter()': '`char_subt`：统计 t 在 `[{tx},{ty}]` 里的字符次数（循环省略）',
        25: '区间为空（`x > y`），当作相同',
        'if char_s[y][char] - char_s[x - 1][char] !=': '字符 `{char!r}`：s 里 `{char_s[y][char] - char_s[x - 1][char]}` 个，t 里 `{char_t[y][char] - char_t[x - 1][char]}` 个 → {"相同" if char_s[y][char] - char_s[x - 1][char] == char_t[y][char] - char_t[x - 1][char] else "不同"}',
        26: lambda S, B, ret: f'`same[{S.y}] − same[{S.x-1}] = {S.same[S.y] - S.same[S.x-1]}`，区间长 `{S.y-S.x+1}` → ' + ('==逐位相同==' if ret else '有位置不同'),
        31: '字符次数不同 → `False`',
        32: '每种字符次数都相同 → `True`',
        44: '不能调整的两头有不同 → `False`',
        'if cnt > char_subs[char]': '`{char!r}`：t 在 `[{sx}, {tx-1}]` 需要 `{cnt}` 个，s 的可调整段里有 `{char_subs[char]}` 个 → {"不够，==False==" if cnt > char_subs[char] else "够，扣掉"}',
        'if cnt > char_subt[char]': '`{char!r}`：s 在 `[{sy+1}, {ty}]` 需要 `{cnt}` 个，t 的可调整段里有 `{char_subt[char]}` 个 → {"不够，==False==" if cnt > char_subt[char] else "够，扣掉"}',
        'if char_s[ty][char] - char_s[sx - 1][char] != ': '整个大区间 `[{sx}, {ty}]` 里 `{char!r}` 的次数：s 与 t {"不同 → False" if char_s[ty][char] - char_s[sx - 1][char] != char_t[ty][char] - char_t[sx - 1][char] else "相同"}',
        70: '两头相同、两头配上、整体次数一致 → 中间那段也一定能配 → `True`',
        'res.append(check': lambda S, B, ret: '调用 `check` 判断这个查询',
        'return res': '全部查询答完：`{res}`',
    },
    cards=dict(
        one_liner='后半翻转后回文 = 两串相等；不能动的逐位比，能动的比字符次数',
        complexity='时间 `O((n+q)·|Σ|)`，空间 `O(n·|Σ|)`',
        problem=['长为偶数 `n` 的 `s`，每个查询 `[a,b,c,d]`：重排左半 `s[a:b]` 和右半 `s[c:d]`',
                 '问能否变成回文串，查询互相独立',
                 '示例：`"abcabc"`，`[[1,1,3,5],[0,2,5,5]]` → `[true,true]`；本视频用 `"aabcbcaa"`'],
        quote='可调整的部分，需要两个字符串在特定区间内每种字符出现的次数都一样；对于不可以调整的部分，则要求完全相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['三个前缀数组：`char_s`、`char_t` 记字符次数，`same` 记 `s[i] = t[i]` 的个数',
              '`same[y] − same[x−1] = y−x+1` 说明 `[x, y]` 逐位相同；字符次数相减比较',
              '区间 `[sx,sy]`、`[tx,ty]` 三类：不相交 5 段、相互包含 3 段、部分重叠要先配两头再比整体'],
        summary=['时间 `O((n+q)·|Σ|)`，空间 `O(n·|Σ|)`',
                 '查询下标要 `+1` 变成从 1 起，才好配合前缀数组',
                 '右半反转后，区间 `[c,d]` 变成 `[n+n−d, n+n−c]`',
                 '部分重叠：配完两头后，只要整个大区间 `[sx, ty]` 字符次数一致，中间那段自然能配',
                 '对比灵神：灵神先交换保证 `l1 <= l2`，用 `subtract` 返回剩余字符；yiduobo 直接用 `Counter` 逐字符比较'],
    ),
)
