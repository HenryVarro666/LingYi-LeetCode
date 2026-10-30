def _done(S):
    if 'p' not in S or 'words' not in S:
        return 0
    return sum(len(w) for w in S['words'][:S['p']]) + S['now']


def _cmp(S, B, r):
    if S.p == len(S.words):
        return f'`p = {S.p}` 已经等于单词数：单词用完了，`s` 还有字符 → 返回 ==False=='
    return f'`p = {S.p}` 没超出数组 → 继续比较'


def _eq(S, B, r):
    w = S.words[S.p]
    c = w[S.now]
    if S.char != c:
        return f'`s` 里的 `{S.char}` ≠ `words[{S.p}][{S.now}] = {c}` → 不匹配，返回 ==False=='
    return f'`s` 里的 `{S.char}` = `words[{S.p}][{S.now}] = {c}` → 匹配'


CONFIG = dict(
    num=1961, title='检查字符串是否为数组前缀', difficulty='Easy', category='字符串',
    author='yiduobo', technique='双指针逐字符匹配',
    tags=[],
    code='''
class Solution(object):
    def isPrefixString(self, s, words):

        p = 0
        now = 0
        for char in s:
            if p == len(words):
                return False
            if char != words[p][now]:
                return False
            now += 1
            if now == len(words[p]):
                p += 1
                now = 0
        
        return now == 0
''',
    call="Solution().isPrefixString('ilovecode', ['i', 'love', 'code', 'x'])",
    expect=True,
    views=[
        dict(type='string', var='s', label='s（绿 = 已匹配的字符）', cell=80, h=200,
             pointers={'已匹配': 'pink'} if False else {},
             color=lambda S, i, v: 'green' if i < _done(S) else None),
        dict(type='array', var='words', label='words（蓝 = 正在匹配的单词）', cell=130, h=230,
             pointers={'p': 'blue'},
             color=lambda S, i, v: 'blue' if 'p' in S and i == S['p'] else None),
        dict(type='text', fn=lambda S: (f"已匹配 `{_done(S)}` 个字符；当前在 `words[{S['p']}]` 的第 `{S['now']}` 个字符" if 'now' in S else '')),
    ],
    watch=[('p', 'p', 'blue'), ('now', 'now', 'pink'), 'char'],
    captions={
        'p = 0': '`p`：当前匹配到 `words` 里第几个单词',
        'now = 0': '`now`：当前单词里的第几个字符',
        'for char in s': '取 `s` 的下一个字符 `char = {char}`',
        'if p == len(words)': _cmp,
        'return False': lambda S, B, r: '不能由前缀单词拼出 → 返回 ==False==',
        'if char != words[p][now]': _eq,
        'now += 1': '匹配成功，`now` → {now}',
        'if now == len(words[p])': lambda S, B, r: ('`now = %d` 等于单词 `%s` 的长度 → 这个单词整个匹配完了' % (S.now, S.words[S.p])) if S.now == len(S.words[S.p]) else ('`now = %d` 还没到单词 `%s` 末尾 → 继续下一个字符' % (S.now, S.words[S.p])),
        'p += 1': '换下一个单词：`p` → {p}',
        'now = 0': '新单词从第 0 个字符开始：`now = 0`',
        'return now == 0': lambda S, B, r: ('`now = %d`：停在单词结尾，`s` 恰由整数个单词拼成 → ==%s==' % (S.now, r)) if S.now == 0 else ('`now = %d`：停在某个单词中间，不是完整单词 → ==%s==' % (S.now, r)),
    },
    cards=dict(
        one_liner='两个指针：第几个单词、单词里第几个字符，边走边比',
        complexity='时间 `O(len(s))`，空间 `O(1)`',
        problem=['`s` 能否由 `words` 的前 `k` 个单词按顺序相连得到（`k` 为正数）',
                 '示例：`s = "iloveleetcode"`，`words = ["i","love","leetcode","apples"]` → `true`',
                 '本视频：`s = "ilovecode"`，`words = ["i","love","code","x"]` → `true`'],
        quote='使用两个变量p和now分别表示当前匹配到了数组中第p个单词的第now个字符，初始情况下p和now都是0。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历 `s`，每个字符对应 `words[p][now]`',
              '`now` 走到单词末尾就换下一个单词：`p += 1`，`now = 0`',
              '中途不匹配、或单词用完 `s` 还有剩余，都是 `False`'],
        summary=['时间 `O(len(s))`，空间 `O(1)`',
                 '易错点：最后要判断 `now == 0`，否则 `s` 在单词中间结束也会被当成 `True`',
                 '易错点：先判 `p == len(words)` 再访问 `words[p]`，避免越界',
                 '原文是 Python 2 风格，但本题代码在 Python 3 下无需改动'],
    ),
)
