def _t(S):
    if 'd' not in S or 'i' not in S:
        return ''
    d = S['d']
    if S.get('k1') is None:
        return f"对角线 `d = i − j = {d}`"
    return f"`d = {d}`：上一个不同在 `k1 = {S['k1']}`，上上一个在 `k0 = {S['k0']}`，以 `i` 结尾的合法起点数 = `k1 − k0` = =={S['k1'] - S['k0']}=="


CONFIG = dict(
    num=1638, title='统计只差一个字符的子串数目', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='枚举对角线 + 记录最近两个不同位置',
    tags=[],
    code='''
class Solution:
    def countSubstrings(self, s: str, t: str) -> int:
        ans, n, m = 0, len(s), len(t)
        for d in range(1 - m, n):  # d=i-j, j=i-d
            i = max(d, 0)
            k0 = k1 = i - 1
            while i < n and i - d < m:
                if s[i] != t[i - d]:
                    k0 = k1  # 上上一个不同
                    k1 = i   # 上一个不同
                ans += k1 - k0
                i += 1
        return ans
''',
    call='Solution().countSubstrings("aba", "baba")',
    expect=6,
    views=[
        dict(type='string', var='s', label='s', h=170, cell=80,
             pointers={'i': 'blue', 'k1': 'orange', 'k0': 'purple'},
             color=lambda S, k, v: ('blue' if k == S.get('i') else None)),
        dict(type='string', var='t', label='t', h=170, cell=80,
             pointers={'i - d': 'pink'},
             color=lambda S, k, v: ('pink' if 'i' in S and 'd' in S and k == S['i'] - S['d'] else None)),
        dict(type='text', fn=_t, size=24, h=80),
    ],
    watch=['d', 'i', ('k0', 'k0', 'purple'), ('k1', 'k1', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans, n, m': '`ans` 计数，`n = {n}`、`m = {m}` 是两串长度',
        'for d in range': '枚举对角线 `d = i − j = {d}`：对齐 `s[i]` 和 `t[i−d]`，==子串对必然在同一条对角线上==',
        'i = max(d, 0)': '这条对角线上 `s` 的起点 `i = {i}`',
        'k0 = k1 = i - 1': '还没遇到不同字符：`k0 = k1 = {k0}`（起点前一格）',
        'while i < n': lambda S, B, r: (f"`i = {S.i}` 且 `i−d = {S.i - S.d}` 都没越界，继续" if (S.i < S.n and S.i - S.d < S.m) else '有一个串走到头了 → 这条对角线结束'),
        'if s[i] != t[i - d]': lambda S, B, r: (f"`s[{S.i}] = {S.s[S.i]!r}` ≠ `t[{S.i - S.d}] = {S.t[S.i - S.d]!r}` → ==出现不同字符==" if S.s[S.i] != S.t[S.i - S.d] else f"`s[{S.i}] = {S.s[S.i]!r}` = `t[{S.i - S.d}]` → 相同，不动"),
        'k0 = k1': '上一个不同退为上上一个：`k0 = {k0}`',
        'k1 = i': '当前位置成为最近的不同：`k1 = {k1}`',
        'ans += k1 - k0': '以 `i` 结尾、恰好含一个不同字符的起点在 `(k0, k1]` 内，共 `{k1} − {k0}` = =={k1 - k0}== 个 → `ans = {ans}`',
        'i += 1': '`i` 右移到 {i}',
        'return ans': '共 `{ans}` 对',
    },
    cards=dict(
        one_liner='同一条对角线上，只差一个字符的子串起点落在最近两个不同位置之间',
        complexity='时间 `O(nm)`，空间 `O(1)`',
        problem=['给两个字符串 `s`、`t`，统计 `s` 的子串与 `t` 的子串==恰好只有一个字符不同==的配对数',
                 '示例：`s="aba"`，`t="baba"`',
                 '结果 `6`'],
        quote='注意到 (i,j) 可以复用 (i-1,j-1) 的计算结果（类比动态规划），就可以进一步减少计算量。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `d = i − j`：每条对角线上，`s[i]` 对齐 `t[i−d]`',
              '以 `i` 结尾的子串对，起点要让区间内==恰好一个不同==：起点在 `(k0, k1]`',
              '`k1`、`k0` 是最近、次近的不同位置，每步贡献 `k1 − k0`'],
        summary=['时间 `O(nm)`，空间 `O(1)`',
                 '易错点：`k0 = k1 = i - 1` 的初值，保证没有不同时贡献为 0',
                 '`d` 的范围是 `1-m` 到 `n-1`，每条对角线起点 `max(d, 0)`',
                 '另一种写法：暴力枚举 `i, j, k` 立方复杂度也能过'],
    ),
)
