def _col(S, i, v):
    if 'm' not in S:
        return None
    n, m = len(S['s']), S['m']
    if S['_line'] >= 7 and 'ans' in S:   # 最后一步：前缀里的 0 变成前导零
        if i < n - m and v == '0':
            return 'green'
    if i >= n - m:
        return 'blue' if S['_line'] >= 6 else 'cyan'
    return None


def _dim(S, i, v):
    if 'm' not in S or S['_line'] < 7:
        return False
    n, m = len(S['s']), S['m']
    return i < n - m and v != '0'


def _txt(S):
    if 'm' not in S:
        return f"`k = {S['k']}`（二进制 `{S['k']:b}`），要在 `s` 里取尽量长的子序列，数值不超过 `k`"
    n, m, s, k = S['n'], S['m'], S['s'], S['k']
    suf = s[-m:]
    if 'ans' not in S:
        return f"`k` 的二进制长 `m = {m}`；`s` 的长 `m` 后缀 `{suf}` = {int(suf, 2)}，对比 `k = {k}`"
    if S['_line'] >= 7:
        return f"后缀 `{s[n-S['ans']:]}` 之前，前缀 `{s[:n-m]}` 里的 0 全部拿来当前导零：`{S['ans']}` + `{s[:-m].count('0')}`"
    return f"取后缀长度 `ans = {S['ans']}`（数值不超过 `k`）"


CONFIG = dict(
    num=2311, title='小于等于 K 的最长二进制子序列', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='贪心 · 后缀 + 前导零',
    tags=['灵神题单', '难度分 1840'],
    code='''
class Solution:
    def longestSubsequence(self, s: str, k: int) -> int:
        n, m = len(s), k.bit_length()
        if n < m:  # int(s, 2) < k
            return n  # 全选
        ans = m if int(s[-m:], 2) <= k else m - 1  # 后缀长度
        return ans + s[:-m].count('0')  # 添加前导零
''',
    call="Solution().longestSubsequence('1001010', 5)",
    expect=5,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='string', var='s', h=300, label='s', color=_col, dim=_dim),
    ],
    watch=['n', ('m', 'm', 'blue'), 'k', ('ans', 'ans', 'green')],
    captions={
        'n, m = len': '`n = {n}`；`k = {k}` 的二进制长度 `m = {m}`。==任何长 m-1 的二进制数一定小于 k==',
        'if n < m': lambda S, B, r: ('`n = %d < m = %d`：s 整个都比 k 小 → 全选' % (S.n, S.m)) if S.n < S.m else ('`n = %d >= m = %d`：s 比 k 长（或等长），不能直接全选' % (S.n, S.m)),
        'return n': '`s` 比 `k` 的二进制还短 → 全选，答案 `n`',
        'ans = m if': lambda S, B, r: ('长 m 的后缀 `%s` = %d %s k = %d → %s' % (S.s[-S.m:], int(S.s[-S.m:], 2), '<=' if int(S.s[-S.m:], 2) <= S.k else '>', S.k, ('可以整段选，后缀长 ==%d==' % S.ans) if int(S.s[-S.m:], 2) <= S.k else ('太大，只能选长 m-1 的后缀（一定小于 k）→ ==%d==' % S.ans))),
        'return ans +': '前缀 `{s[:-m]}` 里的 `0` 有 `{s[:-m].count(chr(48))}` 个：都当前导零加在后缀前面，数值不变 → ==ans = {ans} + {s[:-m].count(chr(48))} = {ans + s[:-m].count(chr(48))}==',
    },
    cards=dict(
        one_liner='选 s 的后缀，再把前缀里所有 0 当作前导零补上',
        complexity='时间 `O(n)`，空间 `O(n)`（或 `O(1)`）',
        problem=['二进制串 `s` 和正整数 `k`，求数值 `<= k` 的最长子序列长度',
                 '子序列可以有前导 0，空串视为 0',
                 '示例：`s = "1001010", k = 5` → `5`（如 `"00010"`）'],
        quote='子序列越靠右，我们能添加的前导零就越多，子序列就越长。贪心地，选 s 的后缀作为子序列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `k` 的二进制长 `m`：任何长 `m-1` 的子序列都小于 `k`',
              '选长 `m` 的后缀 `<= k` 就选它，否则退而选长 `m-1` 的后缀',
              '后缀前面的前缀里，==每个 0 都能当前导零白捡==，1 则不能（会变大）'],
        before=[dict(heading='先看一个反例：后缀太大怎么办', lines=[
            '`s = 1001110`，`k = 101`：长 3 的后缀 `110` 大于 `k`',
            '退一步选长 2 的后缀 `10`（长 `m-1` 一定小于 `k`），前面补 2 个前导零 → `0010`，长 4',
            '想选 `100`、`101` 这种长 3 的子序列？它们只比 `0` + `10` 多 1 位，却==占掉了本可当前导零的 0==，不会更优']),
        ],
        summary=['时间 `O(n)`，空间 `O(n)`（切片），手写遍历可 `O(1)`',
                 '`n < m` 时 `s` 一定比 `k` 小，直接全选',
                 '比较的是长 `m` 的后缀的数值，不是整个 `s`',
                 '思考题：子序列改成子串怎么做？'],
    ),
)
