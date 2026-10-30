def _top(S):
    if 'odd' in S:
        return f"落单（出现奇数次）的字符数 `odd = {S['odd']}`；要构造 `k = {S['k']}` 个回文串，需要 `odd ≤ k`"
    return f"`s` 有 `{len(S['s'])}` 个字符，要拆成 `k = {S['k']}` 个回文串"


CONFIG = dict(
    num=1400, title='构造 K 个回文字符串', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='统计奇数次字符 · 对比 k',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def canConstruct(self, s, k):

        if len(s) < k:
            return False

        cnt_dict = {}
        for char in s:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        odd = 0
        for index in range(26):
            cnt = cnt_dict.get(chr(index + 97), 0)
            if cnt % 2 == 1:
                odd += 1
        
        if k < odd:
            return False
        
        return True
''',
    call='Solution().canConstruct("annabelle", 2)',
    expect=True,
    skip=['for index in range(26)', 'cnt = cnt_dict.get', 'if cnt % 2 == 1'],
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='string', var='s', label='s（黄 = 正在统计的字符）', h=190, cell=80,
             color=lambda S, i, v: 'yellow' if 'char' in S and 'odd' not in S and i == sum(S['cnt_dict'].values()) - (0 if S['_line'] == 9 else 1) else None),
        dict(type='map', var='cnt_dict', label='cnt_dict：字符 → 出现次数（奇数 = 落单）', h=300, fmt=lambda k, v: f"'{k}' → {v}" + ('  落单' if v % 2 else '')),
    ],
    watch=['k', ('char', 'char', 'yellow'), ('odd', 'odd', 'pink')],
    captions={
        'if len(s) < k': lambda S, B, r: (f'`len(s) = {len(S.s)} < k = {S.k}`：每个字符至多单独成一个串，不够 → `False`' if len(S.s) < S.k
                                          else f'`len(s) = {len(S.s)} >= k = {S.k}`：每个字符单独成串最多能造 `{len(S.s)}` 个回文串，够了'),
        'cnt_dict = {}': '统计每个字符出现次数，找出==落单字符==',
        'for char in s': lambda S, B, r: (f"取下一个字符 `char = '{S.s[sum(S.cnt_dict.values())]}'`" if sum(S.cnt_dict.values()) < len(S.s)
                                          else '统计完毕：次数是奇数的字符就是落单字符'),
        'cnt_dict[char] =': "`'{char}'` 累计：`cnt_dict['{char}']` = =={cnt_dict[char]}==",
        'odd = 0': '`odd` 统计出现奇数次的字符种数',
        'odd += 1': lambda S, B, r: f"`'{chr(S.index + 97)}'` 出现 `{S.cnt}` 次（奇数）→ 有个落单字符，必须当某个回文串的中心：`odd` → =={S.odd}=="
                                    if 'index' in S else f'`odd` → {S.odd}',
        'if k < odd': lambda S, B, r: (f'`k = {S.k} < odd = {S.odd}`：落单字符比回文串还多 → `False`' if S.k < S.odd
                                       else f'`k = {S.k} >= odd = {S.odd}`：每个落单字符各当一个串的中心，够用'),
        'return False': lambda S, B, r: '串数不够或落单字符太多 → `False`',
        'return True': '剩下的成对字符可以随意分给各个回文串 → `True`',
    },
    cards=dict(
        one_liner='每个落单字符都要当一个回文串的中心，数一数就行',
        complexity='时间 `O(n)`，空间 `O(1)`（最多 26 种字母）',
        problem=['给定字符串 `s` 和整数 `k`',
                 '用 `s` 的==全部字符==构造恰好 `k` 个非空回文串，能否做到',
                 '示例：`"annabelle", k = 2` → `true`；`"leetcode", k = 3` → `false`'],
        quote='每个落单的字符都必须要形成一个奇数长度的回文串，于是一个自然的想法是统计落单字符的数目odd，若odd > k，那么答案必然为false。',
        quote_src='—— yiduobo 题解原文',
        idea=['`len(s) < k`：每个字符至多单独成串，凑不够 `k` 个 → `False`',
              '奇数长度回文串有一个中心字符，出现奇数次的字符各自占一个中心 → `odd > k` 则 `False`',
              '其余情况：成对字符可以拆开当中心、也可以放两侧，总能凑够 `k` 个 → `True`'],
        result='`odd = 1 ≤ k = 2`，`len(s) = 9 ≥ 2` → `True` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '两个条件缺一不可：`len(s) >= k` 且 `odd <= k`',
                 '只需要奇偶性，不需要真的构造出回文串',
                 '原文本来就能在 Python 3 运行，代码未改动'],
    ),
)
