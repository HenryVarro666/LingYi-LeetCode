def _p1(S):
    return S.get('j') if 'pre' not in S else None


def _p2(S):
    return S.get('pre')


def _pre_pos(S):
    """第二轮里，s[:i] 已经贪心匹配到的 t 下标"""
    s, t, i = S['s'], S['t'], S['i'] + (1 if S['_line'] == 19 else 0)
    out, k = [], 0
    for idx, c in enumerate(t):
        if k < i and c == s[k]:
            out.append(idx)
            k += 1
    return out


def _t_color(S, idx, v):
    if 'pre' in S:
        if idx in _pre_pos(S):
            return 'green'
        if idx == S['pre'] - (1 if S['_line'] == 19 else 0):
            return 'cyan'
        if idx in S['suf'][S['i'] + 1:]:
            return 'orange'
        return None
    if 'suf' in S and idx in S['suf'][1:] and S['suf'][1:].count(idx) and idx >= S.get('j', 0) + 1:
        return 'orange'
    return None


def _s_color(S, k, v):
    if 'pre' in S:
        return 'green' if k < S['i'] else None
    i = S.get('i')
    if i is not None and k > i:
        return 'orange'
    return None


def _top(S):
    if 'pre' in S and S['pre'] < len(S['t']) and S['i'] < len(S['s']) - 1 and 'ans' in S:
        i = S['i']
        p = S['pre'] - (1 if S['_line'] == 19 else 0)
        return f"枚举 i={i}：前缀贴左 `pre={p}`，后缀贴右 `suf[{i+1}]={S['suf'][i+1]}`，间隔 `{S['suf'][i+1]} − {p}`"
    if 'pre' in S:
        return '第二轮：从左往右贴着匹配前缀，用 suf 算间隔'
    return '第一轮：从右往左，把 s 的后缀贴到 t 的最右边'


CONFIG = dict(
    num=4026, title='工位的最大间隔', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前后缀分解 · 子序列双指针',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·动态规划', '难度分 1675'],
    code='''
class Solution:
    def maximumGap(self, s: str, t: str) -> int:
        n = len(s)
        suf = [0] * n  # s[i:] 是 t[suf[i]:] 的子序列
        j = len(t) - 1
        for i in range(n - 1, 0, -1):
            while t[j] != s[i]:  # 题目保证 s 是 t 的子序列，下标不会越界
                j -= 1
            suf[i] = j
            j -= 1

        ans = pre = 0
        for i in range(n - 1):
            while t[pre] != s[i]:
                pre += 1
            # 此时 s[:i+1] 是 t[:pre+1] 的子序列
            # 此时 s[i+1:] 是 t[suf[i+1]:] 的子序列
            ans = max(ans, suf[i + 1] - pre)
            pre += 1
        return ans
''',
    call="Solution().maximumGap('abcb', 'abbcbdcb')",
    expect=5,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（橙 = 已被 suf 贴右的后缀，绿 = 已被 pre 贴左的前缀）', cell=84,
             pointers={'i': 'pink'}, color=_s_color),
        dict(type='string', var='t', label='t（橙 = suf 记下的位置，绿 = pre 贴左匹配的位置）', cell=84,
             pointers={_p1: 'blue', _p2: 'cyan'}, pointer_labels={_p1: 'j', _p2: 'pre'}, color=_t_color),
        dict(type='array', var='suf', label='suf[i]：s[i:] 最靠右能从 t 的哪个下标开始', cell=84, pointers={'i': 'pink'}),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), ('pre', 'pre', 'cyan'), ('suf', 'suf', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'n = len(s)': '`s = "{s}"`，`t = "{t}"`：要在 t 里找一个恰好等于 s 的子序列，让某两个相邻下标差最大',
        'suf = [0] * n': '`suf[i]`：让后缀 `s[i:]` ==尽量靠右==匹配时，`s[i]` 落在 t 的哪个下标',
        'j = len(t) - 1': '先从 t 的最右边开始，往左给 s 的后缀找位置：`j = {j}`',
        'for i in range(n - 1, 0, -1)': lambda S, B, r: ('`suf` 算完了：`s[1:]` 到 `s[n-1:]` 的最右位置都已记下' if S.get('i') == B.get('i') else
                                                         f'`i` 从右往左枚举 s 的每个字母（`i = 0` 不用算，因为 `suf[0]` 用不上）：`i = {S.i}`'),
        'while t[j] != s[i]': lambda S, B, r: (f"`t[{S.j}] = '{S.t[S.j]}'` ≠ `s[{S.i}] = '{S.s[S.i]}'` → 这个位置用不上，`j` 继续往左"
                                                 if S.t[S.j] != S.s[S.i] else f"`t[{S.j}] = '{S.t[S.j]}'` == `s[{S.i}]` → 找到了，且是最靠右的"),
        'j -= 1': lambda S, B, r: ('`j -= 1` 跳过不匹配的字母' if S.t[B.j] != S.s[S.i] else f'`j` → {S.j}，下一个字母只能在它左边找'),
        'suf[i] = j': '`suf[{i}] = {j}`：后缀 `s[{i}:]` 最靠右从 `t[{j}]` 开始',
        'ans = pre = 0': '第二轮：`pre` 是前缀在 t 里的位置，从最左边开始贴',
        'for i in range(n - 1)': lambda S, B, r: ('相邻的工人对都枚举完了' if S.i == B.get('i') else f'枚举 `i`：把 `s[i]` 和 `s[i+1]` 当作相邻的两名工人 → `i = {S.i}`'),
        'while t[pre] != s[i]': lambda S, B, r: (f"`t[{S.pre}] = '{S.t[S.pre]}'` ≠ `s[{S.i}] = '{S.s[S.i]}'` → `pre` 往右"
                                                   if S.t[S.pre] != S.s[S.i] else f"`t[{S.pre}] = '{S.t[S.pre]}'` == `s[{S.i}]` → `s[:{S.i+1}]` 已经贴在最左边"),
        'pre += 1': lambda S, B, r: ('`pre += 1` 往右找' if S.t[B.pre] != S.s[S.i] else f'`pre` → {S.pre}，下一个字母只能放它右边'),
        'ans = max': '前缀贴左：`j_i = {pre}`；后缀贴右：`j_(i+1) = suf[{i+1}] = {suf[i+1]}` → 间隔 `{suf[i+1] - pre}`，`ans = max({B.ans}, {suf[i+1] - pre}) = =={ans}==`',
        'return ans': '所有相邻位置都枚举过了，最大间隔 `{ans}`',
    },
    skip=['pre = 0'],
    cards=dict(
        one_liner='枚举断点：前缀贴最左，后缀贴最右，差值最大',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['`t` 里找一个等于 `s` 的子序列（下标 `j_0 < j_1 < ...`），让相邻下标差 `j_(i+1) − j_i` 的最大值最大',
                 '示例：`s = "cbc"`，`t = "cbcdbc"` → `4`',
                 '本视频：`s = "abcb"`，`t = "abbcbdcb"` → `5`'],
        quote='考虑枚举 i。那么 j_i 越小越好，j_(i+1) 越大越好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`j_i` 越小越好 → `s[:i+1]` 在 t 里==尽量靠左==；`j_(i+1)` 越大越好 → `s[i+1:]` ==尽量靠右==',
              '这是两个独立的问题：先从右往左算 `suf`，再从左往右一边算 `pre` 一边更新答案',
              '答案 = 对所有 `i` 取 `suf[i+1] − pre[i]` 的最大值（`pre` 不用开数组）'],
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '题目保证 s 是 t 的子序列，所以两个 while 不会越界',
                 '`suf` 只需要 `i = 1..n-1`，所以第一轮循环到 1 为止；只有一名工人时第二轮不执行，答案 0',
                 '`pre += 1` 要在更新答案之后，下一个字母才能放在更右边',
                 '和 392 判断子序列、2565 前后缀分解是同一类技巧'],
    ),
)
