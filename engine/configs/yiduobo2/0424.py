# ---- 注意：for char in char_set 的枚举顺序取决于字符串哈希（每次运行可能不同），字幕都按当前变量现算，不依赖顺序
S_IN, K_IN = 'BAAAB', 1
N = len(S_IN)


def _live(S):
    return 'l' in S and 'r' in S and 'rest_k' in S


def _color(S, i, v):
    if not _live(S):
        return None
    if S['l'] <= i < S['r'] or (S.get('_line') in (16, 17) and i == S['r']):
        return 'green' if v == S['char'] else 'orange'
    return None


def _letters(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cs = S.get('char_set')
    if not cs:
        return
    cv.text((x0 + 18, y0 + 4), 'char_set（黄 = 当前假设的字母）', 24, T['muted'], bold=True)
    cur = S.get('char') if 'l' in S else None
    x = x0 + 24
    for ch in sorted(cs):
        hot = ch == cur
        cv.rect((x, y0 + 46, x + 70, y0 + 116), fill=T['yellow'] if hot else T['panel2'], r=10)
        cv.text((x + 35, y0 + 81), ch, 34, T['bg'] if hot else T['text'], anchor='mm', bold=True, mono=True)
        x += 86
    if 'res' in S:
        cv.text((x1 - 30, y0 + 81), f"res = {S['res']}", 40, T['green'], anchor='rm', bold=True, mono=True)


def _dim(S, i, v):
    return _live(S) and i < S['l']


def _info(S):
    if not _live(S):
        if 'char_set' in S and S['char_set']:
            return f"出现过的字母：`{sorted(S['char_set'])}`，逐个假设它是最终的重复字母"
        return ''
    l, r, ch = S['l'], S['r'], S['char']
    rep = sum(1 for c in S['s'][l:r] if c != ch) + (S.get('_line') == 17)
    return f"假设全变 =={ch}==：窗口 `[{l},{r})` 长 `{r - l}`，替换了 `{rep}` 个，`rest_k = {S['rest_k']}`"


def _outer(S, B, ret):
    l, res = B.l, B.res
    if l < N and N - l > res:
        return f'`l = {l}`，后面还剩 `{N - l}` 个字符 `> res = {res}` → 继续'
    if l >= N:
        return '`l` 走到末尾，这个字母枚举完毕'
    return f'后面只剩 `{N - l}` 个字符 `≤ res = {res}`：==不可能更长==，提前结束这个字母'


def _inner(S, B, ret):
    r, ch, rk = B.r, B.char, B.rest_k
    if r >= N:
        return '`r` 到末尾了，停止扩展'
    c = S.s[r]
    if c == ch:
        return f'`s[{r}] = {c!r}` 就是 `{ch!r}` → `r` 可以往右扩'
    if rk > 0:
        return f'`s[{r}] = {c!r}` ≠ `{ch!r}`，但 `rest_k = {rk} > 0` → 替换掉它，往右扩'
    return f'`s[{r}] = {c!r}` ≠ `{ch!r}` 且 `rest_k = 0` → 扩不动了'


CNT = [0]   # for char in char_set 执行到第几次（字幕按步骤顺序各求值一次）


def _for_char(S, B, ret):
    CNT[0] += 1
    if CNT[0] <= len(S.char_set):
        return f'第 {CNT[0]} 个字母：假设最终的重复字母是 =={S.char}=='
    return '所有字母都枚举完了'


CONFIG = dict(
    num=424, title='替换后的最长重复字符', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='枚举最终字母 + 滑动窗口',
    tags=['字节30天'],
    code='''
class Solution(object):
    def characterReplacement(self, s, k):
        if len(s) == 0:
            return 0

        char_set = set()
        for char in s:
            char_set.add(char)

        res = 0
        for char in char_set:
            l = r = 0
            rest_k = k
            while l < len(s) and len(s) - l > res:
                while r < len(s) and ((s[r] == char) or (s[r] != char and rest_k > 0)):
                    if s[r] != char:
                        rest_k -= 1
                    r += 1
                if r - l > res:
                    res = r - l

                if s[l] != char:
                    rest_k += 1
                l += 1

        return res
''',
    call=f'Solution().characterReplacement({S_IN!r}, {K_IN})',
    expect=4,
    skip=[3, 7, 8],
    views=[
        dict(type='text', fn=_info, h=70),
        dict(type='string', var='s', h=280, cell=100, window=('l', lambda S: S['r'] - 1 if _live(S) else None),
             pointers={'l': 'blue', 'r': 'pink'}, color=_color, dim=_dim,
             label='s（窗口 [l, r)：绿 = 本来就是该字母，橙 = 被替换，暗 = 已滑出）'),
        dict(type='custom', draw=_letters, h=150),
    ],
    watch=[('char', 'char', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), 'rest_k', ('res', 'res', 'green')],
    captions={
        'char_set = set()': '题目保证只有大写字母：收集 `s` 中出现的字母，==逐个假设它是最终答案里的字母==',
        'res = 0': lambda S, B, r: (CNT.__setitem__(0, 0), f'`char_set = {sorted(S.char_set)}`；`res` 记录最长长度')[1],
        'for char in char_set': _for_char,
        'l = r = 0': '窗口 `[l, r)` 从头开始，先是空的',
        'rest_k = k': '还能替换 `rest_k = {rest_k}` 次',
        'while l < len(s) and': _outer,
        'while r < len(s) and': _inner,
        'if s[r] != char': lambda S, B, r: (f'`{S.s[S.r]!r}` 不是 `{S.char!r}` → 这次扩展用的是替换' if S.s[S.r] != S.char
                                            else f'`{S.s[S.r]!r}` 本来就是 `{S.char!r}`，不用替换'),
        'rest_k -= 1': '用掉一次替换：`rest_k = {rest_k}`',
        'r += 1': '`r` → `{r}`，窗口 `[{l}, {r})` 长 `{r - l}`',
        'if r - l > res': lambda S, B, r: (f'窗口长 `{S.r - S.l}` > `res = {S.res}` → 更新答案' if S.r - S.l > S.res
                                           else f'窗口长 `{S.r - S.l}` ≤ `res = {S.res}`，不更新'),
        'res = r - l': '`res = {res}`',
        'if s[l] != char': lambda S, B, r: (f'`s[{S.l}] = {S.s[S.l]!r}` 之前被替换过 → 滑出后==把替换次数还回来=='
                                            if S.s[S.l] != S.char else f'`s[{S.l}]` 本来就是 `{S.char!r}`，直接滑出'),
        'rest_k += 1': '`rest_k` 还回来 → `{rest_k}`',
        'l += 1': '左边界右移：`l` → `{l}`',
        'return res': '所有字母都试过 → 返回 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='枚举最终是哪个字母，再用滑动窗口框出最长的一段',
        complexity='时间 `O(26n)`，空间 `O(26)`',
        problem=['字符串 `s` 只含大写字母，最多可以把 `k` 个字符换成任意大写字母',
                 '求替换后==只含同一字母==的最长子串长度',
                 '示例：`s = "AABABBA", k = 1` → `4`（把中间的 B 换成 A：`AAAA`）',
                 '本视频：`s = "BAAAB", k = 1` → `4`'],
        quote='设其为最终答案中出现的字母，然后通过滑动窗口的方法从左往右进行框选……在l滑出去之后则需要将k加上1。',
        quote_src='—— yiduobo 题解',
        idea=['枚举最终的字母 `char`，问题变成：最多把 `k` 个非 `char` 换掉，最长能框多长',
              '`r` 能扩：`s[r] == char`，或者还有替换次数（用掉一次）',
              '`l` 右移时，若 `s[l] != char`，说明它被替换过，==把次数还回来=='],
        summary=['时间 `O(26n)`：每个字母一趟，`l`、`r` 都只往右走',
                 '剪枝：`len(s) − l ≤ res` 时后面不可能更长，直接换下一个字母',
                 '易错：`l` 滑出时只有 `s[l] != char` 才 `rest_k += 1`',
                 '集合的枚举顺序不固定，但每个字母都会试到，答案不受影响',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
