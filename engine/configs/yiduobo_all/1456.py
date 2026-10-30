V = 'aeiou'


def _win(S):
    """(l, r) of current window"""
    idx = S.get('index')
    if idx is None:
        return None
    if 'res' not in S:          # 初始化阶段：窗口 = s[0..index]
        return (0, idx)
    if idx < S['k']:
        return (0, S['k'] - 1)
    return (idx - S['k'] + 1, idx)


def _in(S, B, ret):
    c = S.s[S.index]
    if c in V:
        return f'`s[{S.index}] = {c!r}` 是元音'
    return f'`s[{S.index}] = {c!r}` 不是元音'


def _out(S, B, ret):
    c = S.s[S.index - S.k]
    if c in V:
        return f'滑出的 `s[{S.index - S.k}] = {c!r}` 是元音 → 要减掉'
    return f'滑出的 `s[{S.index - S.k}] = {c!r}` 不是元音，不用减'


CONFIG = dict(
    num=1456, title='定长子串中元音的最大数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='先建初始窗口，再滑入滑出',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1263'],
    code='''
class Solution(object):
    def maxVowels(self, s, k):

        cnt = 0
        v_set = set(['a', 'e', 'i', 'o', 'u'])
        for index in range(k):
            if s[index] in v_set:
                cnt += 1
        
        res = cnt
        for index in range(k, len(s)):
            if s[index] in v_set:
                cnt += 1
            if s[index - k] in v_set:
                cnt -= 1
            res = max(res, cnt)
        
        return res
''',
    call='Solution().maxVowels("leetcode", 3)',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（框 = 当前窗口；绿 = 元音）', cell=100, h=260,
             pointers={'index': 'blue'}, window=(lambda S: (_win(S) or (None, None))[0], lambda S: (_win(S) or (None, None))[1]),
             color=lambda S, i, v: 'green' if v in V else None),
        dict(type='text', h=110, size=32,
             fn=lambda S: (f"窗口 `{S['s'][_win(S)[0]:_win(S)[1] + 1]!r}`：元音数 `cnt = {S['cnt']}`" if _win(S) and 'cnt' in S
                           else '窗口长度固定为 k：==滑入一个、滑出一个==')),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'cnt = 0': '`cnt`：窗口内元音字符的数目',
        'v_set = set': '用集合存 5 个元音，判断 `in` 是 `O(1)`',
        'for index in range(k)': lambda S, B, r: ('初始窗口统计完毕' if 'index' in B and S.index == B.index
                                          else f'初始化窗口 `s[:{S.k}]`：看 `s[{S.index}]`'),
        'if s[index] in v_set': _in,
        'cnt += 1': lambda S, B, r: (f'元音 `s[{S.index}]` 计入：`cnt` → {S.cnt}' if 'res' not in S else f'元音 `s[{S.index}]` 滑入窗口：`cnt` → {S.cnt}'),
        'res = cnt': '初始窗口 `{s[:k]!r}` 有 `{cnt}` 个元音，==答案先初始化为它==',
        'for index in range(k, len(s))': lambda S, B, r: (f'窗口向后移一格：`s[{S.index}]` 滑入，`s[{S.index - S.k}]` 滑出'
                                                          if 'index' in B and S.index != B.index else '窗口已滑到末尾'),
        'if s[index - k] in v_set': _out,
        'cnt -= 1': '元音 `s[{index - k}]` 滑出窗口：`cnt` → {cnt}',
        'res = max(res, cnt)': '窗口 `{s[index - k + 1:index + 1]!r}` 有 {cnt} 个元音：`res = max({B.res}, {cnt}) = {res}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='先数好第一个窗口，之后每次只看滑入和滑出的字符',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `s` 中长度为 `k` 的子串最多含几个元音（a e i o u）',
                 '示例：`s = "abciiidef", k = 3` → `3`',
                 '本视频：`s = "leetcode", k = 3` → `2`'],
        quote='首先初始化窗口为s[:k]，统计其中元音字符的数目now，并初始化答案为now。接下来将窗口向后移动，根据滑入和滑出的字符更新now同时更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['两段循环：第一段数出 `s[:k]` 的元音数，作为答案初值',
              '第二段窗口右移：滑入 `s[index]`、滑出 `s[index − k]`',
              '每次移动后用 `cnt` 更新 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '滑出的是 `s[index − k]`：新窗口是 `[index−k+1, index]`',
                 '别忘了用初始窗口初始化答案，否则 `len(s) == k` 时会漏',
                 '原文为 Python 2 风格，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神一个循环写「入-更新-出」，yiduobo 拆成「建窗口 + 滑动」两段'],
    ),
)
