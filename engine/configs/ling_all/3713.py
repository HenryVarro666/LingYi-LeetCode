S0 = 'abac'


def _txt(S):
    if 'j' not in S or 'mx' not in S:
        return '平衡 ⇔ ==最大次数 × 字母种数 = 子串长度=='
    i, j = S['i'], S['j']
    L = j - i + 1
    k = len(S['cnt'])
    ok = '==相等 → 平衡==' if S['mx'] * k == L else '不相等'
    return f'子串 `{S["s"][i:j + 1]!r}`：`mx × kinds = {S["mx"]} × {k} = {S["mx"] * k}`，长度 `{L}` → {ok}'


def _if(S, B, ret):
    L = S.j - S.i + 1
    k = len(S.cnt)
    if S.mx * k == L:
        return f'`{S.mx} × {k} = {L}`：每种字母都出现了 `mx` 次 → 平衡子串'
    return f'`{S.mx} × {k} = {S.mx * k} ≠ {L}`：有字母次数少于 mx，不平衡'


CONFIG = dict(
    num=3713, title='最长的平衡子串 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举子串 · mx × kinds 判平衡',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
# 手写 max 更快
max = lambda a, b: b if b > a else a

class Solution:
    def longestBalanced(self, s: str) -> int:
        ans = 0
        for i in range(len(s)):
            cnt = defaultdict(int)
            mx = 0
            for j in range(i, len(s)):
                cnt[s[j]] += 1
                mx = max(mx, cnt[s[j]])
                if mx * len(cnt) == j - i + 1:
                    ans = max(ans, j - i + 1)
        return ans
''',
    call=f'Solution().longestBalanced({S0!r})',
    expect=3,
    max_steps=70,
    views=[
        dict(type='string', var='s', label='s（框 = 子串 [i, j]）', pointers={'i': 'blue', 'j': 'pink'},
             window=('i', 'j'), cell=110, h=240),
        dict(type='map', var='cnt', label='cnt（子串中每种字母的次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
        dict(type='text', fn=_txt, size=28, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('mx', 'mx', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'max = lambda': '手写 `max` 更快（行为和内置 max 一样）',
        'ans = 0': '`ans` 记录最长平衡子串的长度',
        'for i in range': lambda S, B, ret: (f'枚举左端点 `i = {S.i}`' if 'i' not in B or S.i != B.i else '所有左端点枚举完'),
        'cnt = defaultdict': '换了左端点，`cnt` 清空重新计数',
        'mx = 0': '`mx`：子串中出现次数的最大值',
        'for j in range': lambda S, B, ret: (f'右端点扩展到 `j = {S.j}`，子串 `{S.s[S.i:S.j + 1]!r}`'
                                             if 'j' not in B or S.j != B.j or not B.cnt else f'以 `i = {S.i}` 开头的子串枚举完'),
        'cnt[s[j]] += 1': '新字母 `{s[j]!r}` 计数 → `{cnt[s[j]]}`，种数 `kinds = {len(cnt)}`',
        'mx = max(mx': lambda S, B, ret: (f'`mx` 更新为 {S.mx}' if S.mx != B.mx else f'`mx` 仍为 {S.mx}'),
        'if mx * len(cnt)': _if,
        'ans = max(ans': lambda S, B, ret: (f'用长度 `{S.j - S.i + 1}` 更新答案 → `ans = {S.ans}`' if S.ans != B.ans
                                            else f'长度 `{S.j - S.i + 1}` 不比 `{S.ans}` 长，ans 不变'),
        'return ans': '最长平衡子串长度 =={ret}==',
    },
    cards=dict(
        one_liner='最大次数 × 字母种数 = 长度，就说明所有字母次数相同',
        complexity='时间 `O(n^2)`，空间 `O(|Σ|)`',
        problem=['子串中所有==不同字符的出现次数都相同==，称为平衡子串',
                 '求 `s` 的最长平衡子串长度，`n ≤ 1000`',
                 '示例：`"abbac"` → `4`（`"abba"`）；本视频 `"abac"` → `3`（`"bac"`）'],
        quote='设 mx = max(cnt)，设 kinds 为子串中的不同字母个数。==如果 mx·kinds = j−i+1，说明子串所有字母的出现次数均为 mx==，均相等。',
        quote_src='—— 灵茶山艾府题解（写法一 · 优化）',
        idea=['枚举左端点 i，右端点 j 往右扩，`cnt` 增量更新',
              '每个字母次数都 `≤ mx`，总和恰好 `mx × kinds` ⇔ 全都等于 mx',
              '`O(1)` 判断平衡，省掉 `len(set(cnt.values())) == 1` 的 `O(|Σ|)`'],
        summary=['时间 `O(n^2)`，空间 `O(|Σ|)`',
                 '`kinds` 直接用 `len(cnt)`：defaultdict 只在访问过的字母上建键',
                 '优化前写法 `len(set(cnt.values())) == 1`，时间 `O(n^2|Σ|)`',
                 '写法二「枚举右，维护左」用前缀差值 + mask 做哈希键，`O(n|Σ|^2)`，适用于 3714 题',
                 '易错：换左端点时 cnt 和 mx 都要重置'],
    ),
)
