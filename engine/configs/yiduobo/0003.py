def _f_upto(s, r):
    """f[0..r]: best left boundary for each right end (same recurrence as the article)"""
    f, left = [], 0
    for i in range(r + 1):
        pos = s.find(s[i], left, i)
        if pos >= 0:
            left = pos + 1
        f.append(left)
    return f


def _f_text(S):
    if 'right' not in S:
        return '`f[i]`：以 `s[i]` 为右边界时的最优左边界'
    s, r = S['s'], S['right']
    f = _f_upto(s, r)
    if S['left'] != f[-1]:          # left for this right not decided yet
        f = f[:-1]
    cells = ', '.join(str(x) for x in f)
    return f"`f = [{cells}]`　（`left` 就是滚动的 `f[i]`）"


def _find_text(S):
    if 'pos' not in S or 'right' not in S:
        return ''
    s, l, r, ch = S['s'], S['left'], S['right'], S['char']
    return f"在 `s[{l}:{r}]` = `\"{s[l:r]}\"` 中找 `\"{ch}\"` → `pos = {S['pos']}`" + ('（红色格子）' if S['pos'] >= 0 else '')


def _color(S, i, v):
    p = S.get('pos')
    if p is not None and p >= 0 and i == p and 'right' in S and v == S['char'] and p < S['right']:
        return 'red'
    return None


def _if_pos(S, B, ret):
    if S.pos >= 0 and S.left == 0:
        return f'出现过（区间内无重复，所以==只会出现一次==）→ 左边界移到 `pos + 1 = {S.pos + 1}`'
    if S.pos >= 0:
        return f'出现过 → 左边界跳到 `pos + 1 = {S.pos + 1}`'
    return f'没出现过 → `f[{S.right}] = f[{S.right - 1}]`，左边界不动' if S.right > 0 else '`f[0] = 0`'


def _if_len(S, B, ret):
    L = S.right - S.left + 1
    if L > S.res:
        return f'子串 `"{S.s[S.left:S.right + 1]}"` 长 `{L}` > `res = {S.res}`'
    return f'长度 `{L}` 不超过 `res = {S.res}`'


CONFIG = dict(
    num=3, title='无重复字符的最长子串', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='动态规划：滚动维护最优左边界',
    code='''
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        left = 0
        res = 0
        for right, char in enumerate(s):
            pos = s.find(char, left, right)
            if pos >= 0:
                left = pos + 1
            if right - left + 1 > res:
                res = right - left + 1
        return res
''',
    call='Solution().lengthOfLongestSubstring("abcabcbb")',
    expect=3,
    views=[
        dict(type='text', fn=_f_text),
        dict(type='string', var='s', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             color=_color, cell=96, h=280, label='s'),
        dict(type='text', fn=_find_text, size=30),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('char', 'char', 'yellow'), 'pos', ('res', 'res', 'green')],
    captions={
        'left = 0': '`left`：滚动维护的==最优左边界==，`f[0] = 0`',
        'res = 0': '`res` 记录答案',
        'for right, char in': lambda S, B, r: ('枚举结束' if 'right' in B and B.right == S.right
                                               else f'右边界 `i = {S.right}`，字符 `"{S.char}"`'),
        'pos = s.find': lambda S, B, r: (f'只需考察 `[f[i−1], i−1]` = `s[{S.left}:{S.right}]` = `"{S.s[S.left:S.right]}"` 中是否出现过 `"{S.char}"`：`pos = {S.pos}`'
                                         if S.right <= 1 else f'在 `"{S.s[S.left:S.right]}"` 中找 `"{S.char}"`：`pos = {S.pos}`'),
        'if pos >= 0': _if_pos,
        'left = pos + 1': '`f[{right}] = pos + 1 = {left}`',
        'if right - left + 1 > res': _if_len,
        'res = right - left + 1': '更新 `res = {res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='`f[i]` 是以 `s[i]` 结尾时的最优左边界，只依赖 `f[i−1]`',
        complexity='时间 `O(n·|Σ|)`，空间 `O(1)`',
        problem=['给定字符串 `s`，找出其中==不含重复字符==的最长子串的长度',
                 '示例：`"abcabcbb"` → `3`（`"abc"`）'],
        quote='只需要考察在==f[i - 1]到i - 1这个区间==中是否已经出现过s[i]。如果未出现过，那么有f[i] = f[i - 1]。如果出现过……f[i] = pos + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：以 `s[i]` 为右边界时的最优左边界；`f[0] = 0`',
              '`[f[i−1], i−1]` 内必然无重复，所以 `s[i]` 在其中==最多出现一次==',
              '左边界单调递增；`f[i]` 只与 `f[i−1]` 有关 → 用一个 `left` 滚动维护'],
        summary=['`left` 只增不减；`find` 扫的窗口无重复，长度 ≤ 字符集大小 → `O(n·|Σ|)`（原文记作 `O(n)`）',
                 '易错：`s.find(char, left, right)` 查的是 `[left, right)`，不含 right 自己',
                 '原文还给了 `O(n³)` 暴力：枚举头尾再检查重复',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用计数 + `while` 一步步缩窗；yiduobo 直接跳到 `pos + 1`'],
    ),
)
