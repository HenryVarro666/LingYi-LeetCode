S0 = 'abba'


def _pals(s):
    """按中心扩展法的顺序列出所有回文子串 (l, r)"""
    n = len(s)
    out = []
    for i in range(2 * n - 1):
        l, r = i // 2, (i + 1) // 2
        while l >= 0 and r < n and s[l] == s[r]:
            out.append((l, r))
            l -= 1
            r += 1
    return out


PALS = _pals(S0)


def _live(S):
    return isinstance(S.get('l'), int) and isinstance(S.get('r'), int) and 'i' in S


def _color(S, i, v):
    if not _live(S):
        return None
    c = S['i']
    if i in (c // 2, (c + 1) // 2):
        return 'orange'  # 回文中心
    return None


def _is_pal(S):
    if not _live(S) or S.get('_line') not in (7, 8):
        return False
    l, r = S['l'], S['r']
    return 0 <= l and r < len(S0) and S0[l] == S0[r]


def _found(S):
    k = S.get('ans')
    if not isinstance(k, int):
        return None
    return [S0[l:r + 1] for l, r in PALS[:k]]


def _text(S):
    if not _live(S):
        return ''
    i = S['i']
    a, b = i // 2, (i + 1) // 2
    kind = '奇回文，中心是一个字母' if a == b else '偶回文，中心是两个字母之间'
    return f"中心 `i = {i}`：`l, r = {i}//2, {i + 1}//2 = {a}, {b}`（{kind}）"


def _cap_for(S, B, ret):
    if 'i' in B and S.get('i') == B.get('i'):
        return f'`2n - 1 = {2 * len(S.s) - 1}` 个回文中心都枚举完了'
    i = S.i
    if i == 0:
        return f'枚举回文中心 `i = 0`（共 `2n - 1 = {2 * len(S.s) - 1}` 个：{len(S.s)} 个字母 + {len(S.s) - 1} 个空隙）'
    return f'下一个回文中心 `i = {i}`'


def _cap_lr(S, B, ret):
    l, r = S.l, S.r
    if l == r:
        return f'`i` 是偶数 → `l = r = {l}`，从单个字母 `"{S.s[l]}"` 开始扩展'
    return f'`i` 是奇数 → `l = {l}, r = {r}`，从相邻两个字母 `"{S.s[l]}{S.s[r]}"` 开始扩展'


def _cap_while(S, B, ret):
    l, r, s, n = B.l, B.r, B.s, len(B.s)
    if l < 0 or r >= n:
        return f'`l = {l}`，`r = {r}`：==出界== → 这个中心扩展结束'
    if s[l] != s[r]:
        return f'`s[{l}] = "{s[l]}" ≠ s[{r}] = "{s[r]}"` → 不是回文，再往外也不会是 → 停止'
    return f'`s[{l}] == s[{r}] = "{s[l]}"`：`s[{l}..{r}] = "{s[l:r + 1]}"` 是回文'


CONFIG = dict(
    num=647, title='回文子串', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='中心扩展法（奇偶合并：枚举 2n-1 个中心）',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        for i in range(2 * n - 1):
            l, r = i // 2, (i + 1) // 2
            while l >= 0 and r < n and s[l] == s[r]:
                ans += 1
                l -= 1
                r += 1
        return ans
''',
    call=f'Solution().countSubstrings({S0!r})',
    expect=6,
    views=[
        dict(type='text', fn=_text, h=64),
        dict(type='string', var='s', label='s（橙 = 回文中心，框 = 当前回文 s[l..r]）', cell=110, h=260,
             pointers={'l': 'blue', 'r': 'pink'},
             window=(lambda S: S['l'] if _is_pal(S) else None, lambda S: S['r'] if _is_pal(S) else None),
             color=_color),
        dict(type='array', var=_found, label='已经数到的回文子串（按中心顺序）', cell=110, h=170),
    ],
    watch=[('i', 'i', 'orange'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('ans', 'ans', 'green')],
    skip=['n = len(s)', 'l -= 1'],
    captions={
        'ans = 0': '`ans` 统计回文子串个数',
        'for i in range': _cap_for,
        'l, r = i // 2': _cap_lr,
        'while l >= 0': _cap_while,
        'ans += 1': '数到一个：`ans` → =={ans}==（`"{s[l:r + 1]}"`）',
        'r += 1': '向两边各扩一位：`l` → {l}，`r` → {r}',
        'return ans': '一共 =={ret}== 个回文子串',
    },
    max_steps=60,
    cards=dict(
        one_liner='每个回文串都有中心：枚举中心，向两边扩展，扩一次就多一个',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['统计字符串 `s` 中==回文子串==的数目（位置不同的相同子串分别计数）',
                 '示例：`"abc"` → `3`；`"aaa"` → `6`',
                 '本视频：`"abba"` → `6`（a, b, b, a, bb, abba）'],
        quote='原理请看 5. 最长回文子串 · 我的题解。包含==奇偶分开，奇偶合并==的写法。',
        quote_src='—— 灵茶山艾府题解（方法一：中心扩展法）',
        idea=['奇回文中心是字母，偶回文中心是空隙：一共 `2n - 1` 个中心',
              '==奇偶合并==：`l, r = i // 2, (i + 1) // 2`，`i` 偶数时 `l == r`',
              '`s[l] == s[r]` 就多一个回文，`l -= 1, r += 1` 继续；不等则外层也不可能是回文'],
        summary=['时间 `O(n²)`：每个中心最多扩展 `O(n)` 次；空间 `O(1)`',
                 '别漏偶回文：只枚举 `n` 个字母中心会漏掉 `"bb"`、`"abba"`',
                 '一旦 `s[l] != s[r]` 就停：外面再包几层也不是回文',
                 '方法二 Manacher：利用对称性复用 `half_len`，`O(n)`，累加 `half_len[i] // 2`'],
    ),
)
