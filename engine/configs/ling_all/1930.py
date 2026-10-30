STR = 'aabaca'
LET = sorted(set(STR))
L_CNT, L_SUF = 11, 12          # setup 循环里 `suf_cnt[ch] += 1` / `suf |= 1 << ch` 所在行
L_RET, L_PRE = 24, 21          # return 行、`pre |= ...` 行


def _mask(m):
    return ''.join(c for c in LET if m >> (ord(c) - 97) & 1)


def _pos(S):
    """s 里当前高亮的下标（建表循环 / 枚举中间循环），其余时刻返回 None"""
    ln = S['_line']
    if 'ans' in S and 'i' in S:
        return None if ln == L_RET else S['i']
    if 'ch' in S and 'suf_cnt' in S and ln <= L_SUF:
        k = sum(S['suf_cnt'])
        p = k if ln in (L_CNT, L_SUF) else k + 1
        return p if p < len(S['s']) else None
    return None


def _s_color(S, k, v):
    p = _pos(S)
    if p is None:
        return None
    if 'ans' not in S:                       # 第一步：统计 s[1:]
        return 'blue' if k == p else ('orange' if 1 <= k < p else None)
    if k == p:
        return 'blue'
    if k > p:
        return 'orange'
    return 'cyan' if k <= (p - 1 if S['_line'] >= L_PRE else p - 2) else None


def _table(S):
    if 'suf_cnt' not in S:
        return None
    cnt, suf, pre, ans = S['suf_cnt'], S.get('suf', 0), S.get('pre', 0), S.get('ans')
    return [[cnt[ord(c) - 97] for c in LET],
            [suf >> (ord(c) - 97) & 1 for c in LET],
            [pre >> (ord(c) - 97) & 1 for c in LET],
            [(_mask(ans[ord(c) - 97]) or '·') if ans else '·' for c in LET]]


def _t_color(S, i, j, v):
    if i == 0:
        return 'orange' if v else None
    if i == 1:
        return 'orange' if v else None
    if i == 2:
        return 'cyan' if v else None
    return 'green' if v != '·' else None


def _mid_col(S):
    if 'mid' in S and 'ans' in S and S['_line'] >= 17:
        return LET.index(chr(S['mid'] + 97))
    return None


def _total(S):
    return sum(m.bit_count() for m in S['ans'])


def _formula(S):
    ln = S['_line']
    if 'ans' not in S or 'mid' not in S or 'i' not in S or ln == L_RET:
        if ln == L_RET and 'ans' in S:
            return f'`ans` 里一共 ==`{_total(S)}`== 个 1，每个 1 是一个不同的回文子序列'
        return '先统计后缀，再枚举中间字母 `mid`：左右两侧都出现的字母 `alpha` 都能组成 `alpha mid alpha`'
    mid = chr(S['mid'] + 97)
    if ln >= 22:
        both = _mask(S['pre'] & S['suf'])
        return f'`mid = {mid}`：`pre & suf` = =={{{", ".join(both) or "空"}}}==，`ans[{mid}]` = =={{{", ".join(_mask(S["ans"][S["mid"]])) or "空"}}}=='
    if ln >= L_PRE:
        return f'`mid = {mid}`：`pre` = {{{", ".join(_mask(S["pre"])) or "空"}}}，`suf` = {{{", ".join(_mask(S["suf"])) or "空"}}}'
    return f'`i = {S["i"]}`，中间字母 `mid = s[i] = {mid}`'


CONFIG = dict(
    num=1930, title='长度为 3 的不同回文子序列', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举中间 · 前后缀分解 + 位运算去重',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1533'],
    code='''
class Solution:
    def countPalindromicSubsequence(self, s: str) -> int:
        n = len(s)
        ord_a = ord('a')

        # 统计 [1,n-1] 每个字母的个数
        suf_cnt = [0] * 26
        suf = 0
        for ch in s[1:]:
            ch = ord(ch) - ord_a
            suf_cnt[ch] += 1
            suf |= 1 << ch  # 把 ch 记录到二进制数 suf 中，表示后缀有 ch

        pre = 0
        ans = [0] * 26  # ans[mid] = 由 alpha 组成的二进制数
        for i in range(1, n - 1):  # 枚举中间字母 mid
            mid = ord(s[i]) - ord_a
            suf_cnt[mid] -= 1  # 撤销 mid 的计数，suf_cnt 剩下的就是后缀 [i+1,n-1] 每个字母的个数
            if suf_cnt[mid] == 0:  # 后缀 [i+1,n-1] 不包含 mid
                suf ^= 1 << mid  # 从 suf 中去掉 mid
            pre |= 1 << (ord(s[i - 1]) - ord_a)  # 把 s[i-1] 记录到二进制数 pre 中，表示前缀有 s[i-1]
            ans[mid] |= pre & suf  # 计算 pre 和 suf 的交集，|= 表示把交集中的字母加到 ans[mid] 中

        return sum(mask.bit_count() for mask in ans)  # mask 中的每个 1 对应着一个 alpha
''',
    call=f'Solution().countPalindromicSubsequence({STR!r})',
    expect=3,
    skip=['n = len(s)', 'ord_a = ord'],
    views=[
        dict(type='text', fn=_formula, size=28, h=90),
        dict(type='string', var='s', label='s（蓝 = 中间字母，青 = 前缀 [0,i-1]，橙 = 后缀 [i+1,n-1]）', cell=96,
             pointers={_pos: 'blue'}, pointer_labels={_pos: 'i'}, color=_s_color, h=250),
        dict(type='table', var=_table, rows=['cnt', 'suf', 'pre', 'ans'], cols=LET, cell=110,
             cursors=[(3, _mid_col, 'blue', 'mid')], color=_t_color,
             label='按字母列出：suf_cnt、suf、pre、ans', h=450),
        dict(type='text', size=22, h=90,
             text='`cnt` = 后缀里的个数；`suf`、`pre` = 二进制位（1 = 有）；`ans` 那一行的列是==中间字母 mid==，格里是两侧字母的集合'),
    ],
    watch=[('i', 'i', 'blue'), ('mid', lambda S: chr(S['mid'] + 97), 'pink'),
           ('pre', lambda S: _mask(S['pre']) or '空', 'cyan'), ('suf', lambda S: _mask(S['suf']) or '空', 'orange')],
    captions={
        'suf_cnt = [0] * 26': '`suf_cnt[c]` 统计后缀里字母 `c` 的个数（下标 0~25 对应 a~z）',
        'suf = 0': '`suf` 是一个二进制数：第 `c` 位是 1，表示后缀里有字母 `c`',
        'for ch in s[1:]': lambda S, B, ret: ('后缀统计完毕：`suf_cnt` 就是 `s[1:]` 每个字母的个数' if _pos(S) is None
                                              else f'先统计 `s[1:]`：看 `s[{_pos(S)}] = {S.s[_pos(S)]!r}`'),
        'ch = ord(ch)': '字母 `{chr(ch + 97)}` 的编号是 `{ch}`',
        'suf_cnt[ch] += 1': '`suf_cnt[{chr(ch + 97)}]` → {suf_cnt[ch]}',
        'suf |= 1 << ch': '把 `{chr(ch + 97)}` 记进 `suf`：后缀里有 `{chr(ch + 97)}` 了',
        'pre = 0': '`pre` 同理：前缀里有哪些字母，一开始是空集（只是个二进制数 0）',
        'ans = [0] * 26': '`ans[mid]`：以 `mid` 作中间字母时，两侧字母 `alpha` 组成的集合 —— ==集合天然去重==',
        'for i in range(1, n - 1)': lambda S, B, ret: ('中间字母都枚举完了' if 'i' in B and S.i == B.i
                                                       else f'枚举中间字母：`i = {S.i}`，两端不能当中间，所以 `i` 从 1 到 n-2'),
        'mid = ord(s[i])': '中间字母 `mid = s[{i}] = {chr(mid + 97)}`',
        'suf_cnt[mid] -= 1': '==撤销== `mid` 自己的计数：`suf_cnt[{chr(mid + 97)}]` → {suf_cnt[mid]}，剩下的就是后缀 `[i+1, n-1]` 的个数',
        'if suf_cnt[mid] == 0': lambda S, B, ret: (f'`suf_cnt[{chr(S.mid + 97)}] == 0`：后缀里已经没有 `{chr(S.mid + 97)}`'
                                                   if S.suf_cnt[S.mid] == 0
                                                   else f'`suf_cnt[{chr(S.mid + 97)}] = {S.suf_cnt[S.mid]}`：后缀里还有 `{chr(S.mid + 97)}`，`suf` 不用改'),
        'suf ^= 1 << mid': '把 `{chr(mid + 97)}` 从 `suf` 里去掉（异或翻转那一位）',
        'pre |= 1 << (ord(s[i - 1])': '把 `s[{i - 1}] = {s[i - 1]!r}` 记进 `pre`，现在 `pre` 就是前缀 `[0, i-1]` 的字母集合',
        'ans[mid] |= pre & suf': lambda S, B, ret: (
            f'`pre & suf` = {{{", ".join(_mask(S.pre & S.suf)) or "空"}}}：这些字母 `alpha` 两侧都有'
            + ('' if not (S.pre & S.suf) else ' → 可组成 ' + '、'.join(f'`{a}{chr(S.mid + 97)}{a}`' for a in _mask(S.pre & S.suf)))
            + f'；并进 `ans[{chr(S.mid + 97)}]`'
            + ('，==这些之前已经记过，不会重复计数==' if (S.pre & S.suf) and (B.ans[S.mid] | (S.pre & S.suf)) == B.ans[S.mid] else '')),
        'return sum(': '`ans` 里每个 1 对应一个 `alpha + mid + alpha` → 一共 `{sum(m.bit_count() for m in ans)}` 个',
    },
    max_steps=70,
    cards=dict(
        one_liner='枚举中间字母，前后缀各记一个“有没有”的二进制集合，取交集',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`，`|Σ| = 26`',
        problem=['数 `s` 中长度为 3 的==不同==回文子序列个数；相同内容只算一次',
                 '回文：第一个字母 = 第三个字母',
                 '示例：`"aabca"` → `3`（`aba`、`aaa`、`aca`）',
                 '本视频：`"aabaca"` → `3`（含重复的 `aaa`）'],
        quote='枚举 i=1,2,…,n-2，把 s[i] 当作子序列的第二个字母，那么对于第一、三个字母 α=a,b,…,z，我们需要判断：s 的前缀 [0,i-1] 中有没有 α？s 的后缀 [i+1,n-1] 中有没有 α？',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['先统计后缀字母个数；遍历到 `i` 时==撤销== `s[i]`，剩下的就是 `[i+1,n-1]`',
              '前缀有哪些字母：边遍历边记录',
              '“有没有”压缩成一个二进制数：`pre & suf` 一步求出两侧都有的字母',
              '`ans[mid]` 是集合（二进制数），相同的 `alpha + mid` 只会记一次'],
        summary=['时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
                 '易错：必须==先撤销== `suf_cnt[mid]` 再判断是否为 0，否则后缀会多出自己',
                 '`i` 从 1 到 n-2，两端不能作中间字母',
                 '方法一（枚举两侧）：每个字母取最左、最右两处，数中间有几种不同字母，`O(n|Σ|)`',
                 '方法二还有“优化前”写法：`pre_set` + `suf_cnt` + 集合去重，思路一致，本视频演示位运算版'],
    ),
)
