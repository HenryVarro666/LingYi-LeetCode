from collections import Counter as _C

S0 = 'aabbc'


def _win(S):
    c, L = S.get('cnt'), S.get('sub_len')
    if c is None or L is None or 'tot_char' not in S:
        return None
    s = S['s']
    w = sum(c.values())
    if w < L:
        return (0, w - 1) if w else None
    if w > L:
        i = S['index']
        return (i, i + L)
    if 'index' in S and 'char' in S:
        a = S['index'] + 1
        if a + L <= len(s) and _C(s[a:a + L]) == _C(c):
            return (a, a + L - 1)
    return (0, L - 1)


def _lo(S):
    r = _win(S)
    return None if r is None else r[0]


def _hi(S):
    r = _win(S)
    return None if r is None else r[1]


def _info(S):
    if 'sub_len' not in S:
        return '枚举等计数子串里的不同字符数 `tot_char`，长度 = `tot_char × count`'
    return f'`tot_char = {S["tot_char"]}` 种字符 × 每种 `{S["count"]}` 次 → 窗口长 `sub_len = {S["sub_len"]}`'


def _cnt(S):
    c = S.get('cnt')
    if not c or 'sub_len' not in S or sum(c.values()) != S['sub_len']:
        return ''
    ok = all(v == S['count'] for v in c.values())
    return f'窗口 `{dict(c)}`：' + ('==每种都恰好 count 次，计 1 个==' if ok else '有字符次数 ≠ count，不计')


CONFIG = dict(
    num=2067, title='等计数子串的数量', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举字符种数 + 定长滑窗',
    tags=[],
    code='''
class Solution(object):
    def equalCountSubstrings(self, s, count):

        def check(cnt):
            for v in cnt.values():
                if v != count:
                    return 0
            return 1

        res = 0
        n = len(s)
        for tot_char in range(1, 27):
            sub_len = tot_char * count
            cnt = {}
            if sub_len <= n:
                for char in s[:sub_len]:
                    cnt[char] = cnt.get(char, 0) + 1
                res += check(cnt)

                for index, char in enumerate(s[sub_len:]):
                    cnt[char] = cnt.get(char, 0) + 1
                    cnt[s[index]] -= 1
                    if cnt[s[index]] == 0:
                        cnt.pop(s[index])
                    res += check(cnt)

        return res
''',
    call=f'Solution().equalCountSubstrings({S0!r}, 2)',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（框 = 当前长为 sub_len 的窗口）', cell=100, h=230,
             window=(_lo, _hi)),
        dict(type='map', var='cnt', label='cnt（窗口内各字符次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=34),
        dict(type='text', h=90, size=28, fn=_info),
        dict(type='text', h=70, size=28, fn=_cnt),
    ],
    watch=[('tot_char', 'tot_char', 'orange'), ('sub_len', 'sub_len', 'cyan'), ('count', 'count', 'purple'), ('res', 'res', 'green')],
    captions={
        'def check(cnt)': '`check`：窗口里每种字符的次数都等于 `count` 才返回 1',
        'res = 0': '`res` 统计等计数子串个数',
        'n = len(s)': '`n = {n}`',
        'for tot_char in range': lambda S, B, r: (f'枚举不同字符数 `tot_char = {S.tot_char}`' if not ('tot_char' in B and S.tot_char == B.tot_char) else '`tot_char` 枚举完，没有更多了'),
        'sub_len = tot_char * count': lambda S, B, r: (f'`sub_len = {S.tot_char} × {S.count} = {S.sub_len}`：{S.tot_char} 种字符、每种 {S.count} 次，子串长必为 {S.sub_len}；'
                                                       + (f'放得下 `≤ n = {S.n}`，开始滑窗' if S.sub_len <= S.n else f'`> n = {S.n}`，放不下，这一轮跳过')),
        'cnt = {}': '这一轮窗口的计数 `cnt` 清空',
        'for char in s[:sub_len]': '先把第一个窗口 `{s[:sub_len]!r}` 的字符逐个计数',
        'cnt[char] = cnt.get(char, 0) + 1': lambda S, B, r: (f'`{S.char!r}` 进入窗口：`cnt[{S.char!r}] = {S.cnt[S.char]}`'),
        'for index, char in enumerate(s[sub_len:])': lambda S, B, r: (f'窗口右移：`{S.char!r}` 从右边进入，`s[{S.index}] = {S.s[S.index]!r}` 将从左边离开'
                                                                      if not ('index' in B and S.index == B.index and 'char' in B and S.char == B.char) else '这一轮窗口滑完'),
        'cnt[s[index]] -= 1': '左端的 `{s[index]!r}` 离开窗口：`cnt[{s[index]!r}] = {cnt[s[index]]}`',
        'if cnt[s[index]] == 0': lambda S, B, r: (f'`{S.s[S.index]!r}` 的次数变成 0，不在窗口里了' if S.cnt[S.s[S.index]] == 0 else f'`{S.s[S.index]!r}` 还剩 `{S.cnt[S.s[S.index]]}` 次，保留'),
        'cnt.pop(s[index])': '把次数为 0 的键删掉，否则 `check` 会把 0 当成「次数 ≠ count」',
        'for v in cnt.values()': '逐个检查窗口里每种字符的次数',
        'if v != count': lambda S, B, r: (f'`{S.v} ≠ {S.count}`：这个窗口不行，返回 0' if S.v != S.count else f'`{S.v} == {S.count}`：这种字符合格，继续看下一种'),
        'return 0': '返回 0',
        'return 1': '所有字符都恰好 `{count}` 次，返回 1',
        'res += check(cnt)': lambda S, B, r: (f'`res = {S.res}`' + ('：==又找到一个等计数子串==' if 'res' in B and S.res != B.res else '')),
        'return res': '等计数子串共 =={res}== 个',
    },
    skip=['cnt = {}', 'n = len(s)', 'if sub_len <= n', 'return 0'],
    max_steps=80,
    cards=dict(
        one_liner='枚举不同字符数 k，子串长度 = k × count，再滑窗',
        complexity='时间 `O(26·n)`，空间 `O(26)`',
        problem=['等计数子串：子串里==每种出现的字符==都恰好出现 `count` 次',
                 '`s` 只含小写字母，求等计数子串的个数',
                 '示例：`s="aaabcbbcc", count=3` → `3`；本视频：`s="aabbc", count=2` → `3`'],
        quote='由于题目中的s仅有小写字符构成，那么所有的等计数子串中的不同字符数量必然在1到26之间，于是可以枚举这个不同字符的数量tot_char，这样就得到出现了tot_char个不同字符的等计数子串的长度sub_len = tot_char * count。',
        quote_src='—— yiduobo 题解原文',
        idea=['不同字符数只有 1~26 种 → 枚举 `tot_char`',
              '每种恰好 `count` 次 → 子串长度 `sub_len = tot_char × count` 就固定了',
              '定长窗口从左滑到右，用 `cnt` 维护次数，每个窗口 `check` 一次'],
        summary=['时间 `O(26·n)`（`check` 最多遍历 26 个键），空间 `O(26)`',
                 '易错：次数减到 0 的字符要 `pop` 掉，否则 `check` 会误判',
                 '`sub_len > n` 时这一轮直接跳过',
                 '原文是 Python 2 风格，在 Python 3 下无需改动',
                 '同类：2953 统计完全子字符串（枚举种数 + 定长窗口）'],
    ),
)
