CONFIG = dict(
    num=2609, title='最长平衡子字符串', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='分段统计 · 相邻两段取 min',
    tags=[],
    code='''
class Solution:
    def findTheLongestBalancedSubstring(self, s: str) -> int:
        ans = pre = cur = 0
        for i, c in enumerate(s):
            cur += 1
            if i == len(s) - 1 or c != s[i + 1]:  # i 是连续相同段的末尾
                if c == '1':
                    ans = max(ans, min(pre, cur) * 2)
                pre = cur
                cur = 0
        return ans
''',
    call="Solution().findTheLongestBalancedSubstring('01000111')",
    expect=6,
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, h=260,
             color=lambda S, i, v: ('green' if v == '0' else 'cyan') if 'i' in S and i <= S['i'] else None),
        dict(type='text', fn=lambda S: f"上一段长度 `pre = {S['pre']}`，当前段已数到 `cur = {S['cur']}`" if 'pre' in S else '', size=32),
        dict(type='text', fn=lambda S: (f"这一对 0/1 段最长平衡串 = `2 × min({S['pre']}, {S['cur']})` = =={2 * min(S['pre'], S['cur'])}==" if S.get('_line') == 8 and 'cur' in S else ''), size=32),
    ],
    watch=['i', 'c', ('pre', 'pre', 'blue'), ('cur', 'cur', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = pre = cur': '`ans` 记最长平衡串长度；`pre` 是上一段的长度，`cur` 是当前段已数到的长度',
        'cur += 1': '看到 `s[{i}] = {c}`：当前这段连续相同字符多了一个，`cur = {cur}`',
        'if i == len(s) - 1': lambda S, B, r: (f'`s[{S.i}]` 是这一段的末尾吗？' + ('是（已是最后一个字符）' if S.i == len(S.s) - 1 else ('是：下一个字符 `' + S.s[S.i + 1] + '` 不同' if S.c != S.s[S.i + 1] else '不是：下一个字符相同，继续数'))),
        "if c == '1'": lambda S, B, r: ('这一段是 1：上一段一定是 0，两段拼成 `0…01…1`，可以算平衡串' if S.c == '1' else '这一段是 0：它还要等后面的 1 才能配成平衡串，先不算'),
        'ans = max': '平衡串里 0 和 1 一样多：取两段中短的那段长度 ×2：`2 × min({pre}, {cur})` = {2*min(pre, cur)}，`ans = {B.ans} → {ans}`',
        'pre = cur': '这一段结束，变成“上一段”：`pre = {pre}`',
        'cur = 0': '`cur` 清零，准备数下一段',
        'return ans': '最长平衡子字符串长度 `{ans}`',
    },
    cards=dict(
        one_liner='把字符串切成连续段，相邻的 0 段和 1 段取 min 再乘 2',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串，平衡子串：所有 0 在 1 之前，且 0 和 1 个数相等',
                 '求最长平衡子串的长度（空串也算，答案可为 0）',
                 '示例：`"01000111"` → `6`（即 `"000111"`）'],
        quote='记录上一段连续相同字符个数 pre，以及当前连续相同字符个数 cur。如果当前字符是 1，那么上一段的字符是 0，这两段可以组成一个 01 串，当前这个 01 串的最大长度就是 2·min(pre, cur)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一次遍历，把相同字符连成一段，只记 `pre` 和 `cur` 两个长度',
              '段结束且是 1：这一段 1 与前面那段 0 相邻，能配成 `2 × min(pre, cur)`',
              '段结束就把 `cur` 交给 `pre`，`cur` 清零，继续数下一段'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：只有当前段是 1 才更新答案；连续的两个 0 段不会出现，因为相同字符会连成一段',
                 '`i == len(s) - 1` 放在前面，保证最后一段也能结算，且不会越界'],
    ),
)
