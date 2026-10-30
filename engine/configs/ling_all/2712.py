def _txt(S):
    if 'ans' not in S:
        return '相邻两个字符不同，就必须翻转一次；翻前缀或翻后缀，取便宜的'
    if 'i' not in S:
        return f"`n = {S['n']}`，`ans = 0`"
    i, n = S['i'], S['n']
    if i >= n:
        return f'所有相邻对都处理完，==ans = {S["ans"]}=='
    a, b = S['s'][i - 1], S['s'][i]
    if a == b:
        return f"`s[{i-1}] = {a}` 与 `s[{i}] = {b}` 相同 → 不用花钱，`ans = {S['ans']}`"
    return f"`s[{i-1}] ≠ s[{i}]`：翻前缀 `{i}`，翻后缀 `{n - i}` → 取 =={min(i, n - i)}==，`ans = {S['ans']}`"


CONFIG = dict(
    num=2712, title='使所有字符相等的最小成本', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='相邻对独立 · min(i, n-i)',
    tags=['灵神题单', '难度分 1791'],
    code='''
class Solution:
    def minimumCost(self, s: str) -> int:
        n = len(s)
        ans = 0
        for i in range(1, n):
            if s[i - 1] != s[i]:
                ans += min(i, n - i)
        return ans
''',
    call="Solution().minimumCost('010101')",
    expect=9,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='string', var='s', h=300, label='s',
             pointers={'i - 1': 'blue', 'i': 'pink'},
             color=lambda S, k, v: ('blue' if 'i' in S and k == S['i'] - 1 and S['i'] < S['n'] else
                                    'pink' if 'i' in S and k == S['i'] and S['i'] < S['n'] else None),
             dim=lambda S, k, v: False),
    ],
    watch=['n', ('i', 'i', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`，反转后缀的成本是 `n - i`',
        'ans = 0': '`ans` 累加每对相邻不同字符的最小成本',
        'for i in range': lambda S, B, r: ('检查相邻一对 `s[%d]` 和 `s[%d]`' % (S.i - 1, S.i)) if ('i' not in B or S.i != B.i) else '所有相邻对检查完毕',
        'if s[i - 1] != s[i]': lambda S, B, r: ("`s[%d] = %s` ≠ `s[%d] = %s` → ==必须翻转==，不然这两个字符永远不相等" % (S.i - 1, S.s[S.i - 1], S.i, S.s[S.i])) if S.s[S.i - 1] != S.s[S.i] else ("`s[%d] = %s` == `s[%d] = %s` → 已经相等，不用管" % (S.i - 1, S.s[S.i - 1], S.i, S.s[S.i])),
        'ans += min': '翻前缀花 `i = {i}`，翻后缀花 `n - i = {n - i}` → 取小的：`ans = {B.ans} + {min(i, n - i)} = {ans}`',
        'return ans': '每对相邻字符互相独立，成本相加 = ==最小成本 {ans}==',
    },
    cards=dict(
        one_liner='相邻字符不同就必须翻转，每对独立，取前缀/后缀较小者',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`，可翻转前缀 `[0,i]`（成本 `i+1`）或后缀 `[i,n-1]`（成本 `n-i`）',
                 '求让所有字符相等的最小成本',
                 '示例：`"0011"` → `2`；`"010101"` → `9`'],
        quote='反转操作只会改变 s[i-1] 与 s[i] 是否相等，不会改变其他相邻字符是否相等，所以每对相邻字符其实是互相独立的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s[i-1] != s[i]` 时必须翻：翻前缀 `s[0..i-1]` 成本 `i`，翻后缀 `s[i..n-1]` 成本 `n-i`',
              '翻转不改变其他相邻对是否相等 → 每个不相等的位置==独立==处理',
              '每处花 `min(i, n-i)`，累加即答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '成本是前缀长 `i` / 后缀长 `n-i`，别混成 `i+1`',
                 '只统计相邻不同的位置，相同的位置不花钱',
                 '灵神还给了 `pairwise` 的一行写法 `sum(min(i, len(s)-i) ...)`'],
    ),
)
