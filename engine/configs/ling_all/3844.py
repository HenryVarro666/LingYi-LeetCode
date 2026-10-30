def _top(S):
    if 'i' not in S:
        return '中心扩展：先正常扩展到失配，再==删掉一个字母==（`s[l]` 或 `s[r]`）继续扩展'
    inner = S.get('_inner', {})
    if 'l' in S and 'r' in S:
        if S.get('_line') in (7, 8, 9, 10, 11):
            return f"`expand({S['l']}, {S['r']})`：已用掉一次删除，继续向外找匹配"
        return f"枚举中心 `i = {S['i']}`：当前 `l = {S['l']}`，`r = {S['r']}`"
    return ''


CONFIG = dict(
    num=3844, title='最长的准回文子字符串', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='中心扩展 + 失配时删一个',
    tags=['灵神题单', '字符串', '难度分 1990'],
    code='''
class Solution:
    def almostPalindromic(self, s: str) -> int:
        n = len(s)
        ans = 0

        def expand(l: int, r: int) -> None:
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            nonlocal ans
            ans = max(ans, r - l - 1)  # [l+1, r-1] 是回文串

        for i in range(2 * n - 1):
            l, r = i // 2, (i + 1) // 2
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            expand(l - 1, r)  # 删除 s[l]，继续扩展
            expand(l, r + 1)  # 删除 s[r]，继续扩展
            if ans >= n:  # 优化：提前返回答案
                return n
        return ans
''',
    call='Solution().almostPalindromic("abca")',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='string', var='s', label='s（l、r 是当前向外扩展的两端；绿 = 已匹配的回文）', cell=84, h=250,
             pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, k, v: 'green' if 'l' in S and 'r' in S and S['l'] < k < S['r'] else None),
        dict(type='text', fn=lambda S: f"目前最长准回文 `ans = {S['ans']}`（`n = {S['n']}`，到 `n` 就能直接返回）" if 'ans' in S and 'n' in S else '', size=24, h=60),
    ],
    watch=[('i', 'i'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('ans', 'ans', 'green')],
    skip=['n = len', 'ans = 0', 'nonlocal ans', 'l, r = i'],
    captions={
        'for i in range': '枚举回文中心 `i = {i}`（共 `2n-1` 个：字母本身或相邻两字母之间）',
        'while l >= 0': lambda S, B, ret: (
            (f"`s[{S.l}] = {S.s[S.l]}` == `s[{S.r}] = {S.s[S.r]}` → ==继续向外=="
             if 0 <= S.l and S.r < len(S.s) and S.s[S.l] == S.s[S.r]
             else (f"到边界了（`l = {S.l}`，`r = {S.r}`），不能再扩展" if not (0 <= S.l and S.r < len(S.s))
                   else f"`s[{S.l}] = {S.s[S.l]}` ≠ `s[{S.r}] = {S.s[S.r]}` → 失配，必须删一个字母才能继续"))),
        'l -= 1': '`l` → {l}',
        'r += 1': '`r` → {r}',
        'ans = max': '扩展结束：长度 `r - l - 1 = {r}-({l})-1 = {r-l-1}`，更新 `ans = {ans}`',
        'expand(l - 1, r)': '第一次扩展停下（失配或越界）：==删掉 `s[l]`==，从 `l-1` 和 `r` 继续扩展',
        'expand(l, r + 1)': '另一种：==删掉 `s[r]`==，从 `l` 和 `r+1` 继续扩展',
        'if ans >= n': lambda S, B, ret: (f'`ans = {S.ans} >= n = {S.n}`：整串都是准回文，提前返回' if S.ans >= S.n
                                          else f'`ans = {S.ans} < n = {S.n}`，继续下一个中心'),
        'return n': '整串长度 `n = {n}` 已经达到上限，直接返回',
        'return ans': '所有中心都试过，最长准回文串长度 `{ans}`',
    },
    max_steps=120,
    cards=dict(
        one_liner='先扩展到失配，再删一个字母继续扩展，两种取最大',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['一个子串==恰好删掉一个字符==后变成回文，就是准回文串',
                 '求 `s` 中最长准回文子串的长度',
                 '示例：`"abca"` → `5`（取 `"zabba"`，删 `z` 得 `"abba"`）'],
        quote='如果发现 s[l]≠s[r]，那么必须删除字母，才能继续扩展：选择删除 s[l]，从 l-1 和 r 开始，继续向左向右扩展。选择删除 s[r]，从 l 和 r+1 开始，继续向左向右扩展。两种情况取最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举最终答案的回文中心，正常向外扩展，直到 `s[l] ≠ s[r]`',
              '此时必须删字母：删 `s[l]` 就从 `(l-1, r)` 继续，删 `s[r]` 就从 `(l, r+1)` 继续',
              '提前删（还没失配就删）不会更优，所以只在首次失配时删'],
        summary=['时间 `O(n^2)`，空间 `O(1)`；`ans >= n` 时提前返回',
                 '易错：`expand` 返回的回文长度是 `r - l - 1`，它没算上被删的那个字母，所以删字母后的子串更长一格',
                 '回文本身也算准回文（删中心字母），这一点被中心扩展自然覆盖',
                 '方法二：Manacher + 后缀数组 `O(n log n)`，常数大，实际不如方法一'],
    ),
)
