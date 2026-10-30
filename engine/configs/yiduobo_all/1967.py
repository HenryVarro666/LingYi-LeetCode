CODE = '''
class Solution:
    def numOfStrings(self, patterns, word):

        res = 0
        for pattern in patterns:
            f = [0]
            pos = 0
            for index in range(1, len(pattern)):
                while pos > 0 and pattern[pos] != pattern[index]:
                    pos = f[pos - 1]
                if pattern[pos] == pattern[index]:
                    pos += 1
                f.append(pos)

            pos = 0
            for char in word:
                while pos > 0 and pattern[pos] != char:
                    pos = f[pos - 1]
                if pattern[pos] == char:
                    pos += 1
                if pos == len(pattern):
                    res += 1
                    break

        return res
'''
_L = CODE.strip('\n').split('\n')
_MATCH_FROM = [i for i, t in enumerate(_L, 1) if t.strip() == 'pos = 0'][1]


def _wp(S):
    if S['_line'] >= _MATCH_FROM and 'char' in S:
        return S['word'].index(S['char'])
    return None


def _ip(S):
    if S['_line'] < _MATCH_FROM:
        return S.get('index')
    return None


def _pp(S):
    return S.get('pos')


def _top(S):
    if 'pattern' not in S:
        return ''
    p = S['pattern']
    if S['_line'] < _MATCH_FROM:
        return f"第一步：给 `{p}` 建失败数组 `f = {S.get('f')}`（每个前缀的最长相同前后缀）"
    return f"第二步：用 `f` 在 `{S['word']}` 里匹配 `{p}`，`pos` = 已匹配的长度"


def _pcol(S, i, v):
    pos = S.get('pos')
    if pos is not None and i < pos and S['_line'] >= _MATCH_FROM:
        return 'green'
    return None


CONFIG = dict(
    num=1967, title='作为子字符串出现在单词中的字符串数目', difficulty='Easy', category='字符串',
    author='yiduobo', technique='逐个模式串 KMP 匹配',
    tags=['灵神题单', '字符串'],
    code=CODE,
    call='Solution().numOfStrings(["aba", "bc"], "abc")',
    expect=1,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='word', label='word', cell=70, pointers={_wp: 'blue'}, pointer_labels={_wp: 'char'}, h=230),
        dict(type='string', var='pattern', label='pattern（绿 = 已匹配的前缀）', cell=70,
             pointers={_ip: 'pink', _pp: 'cyan'}, pointer_labels={_ip: 'index', _pp: 'pos'}, color=_pcol, h=230),
        dict(type='array', var='f', label='f（失败数组）', cell=70, h=190),
    ],
    max_steps=90, skip=['f.append(pos)'],
    watch=['pattern', ('pos', 'pos', 'cyan'), ('f', 'f'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计有多少个模式串出现在 word 中',
        'for pattern in patterns': '枚举模式串 `{pattern}`：先建它的失败数组，再去 word 里匹配',
        'f = [0]': '`f[i]` = `pattern[:i+1]` 的最长相同前后缀长度；单个字符一定是 0',
        'for index in range(1, len(pattern))': '用 `pattern[{index}] = {pattern[index]}` 去延长前缀',
        'while pos > 0 and pattern[pos] != pattern[index]': lambda S, B, r: (
            f"`pos = {S.pos}`：`{S.pattern[S.pos]}` ≠ `{S.pattern[S.index]}` → ==失配，回退==" if S.pos > 0 and S.pattern[S.pos] != S.pattern[S.index]
            else f"`pos = {S.pos}`：不用回退（pos 为 0 或已相等）"),
        'pos = f[pos - 1]': '前缀不能再延长 → 退到更短的相同前后缀：`pos = f[{B.pos}-1] = {pos}`',
        'if pattern[pos] == pattern[index]': lambda S, B, r: (
            f"`{S.pattern[S.pos]}` == `{S.pattern[S.index]}` → 前后缀又长了一位" if S.pattern[S.pos] == S.pattern[S.index]
            else f"`{S.pattern[S.pos]}` ≠ `{S.pattern[S.index]}` → 这个位置没有相同前后缀，f 记 0"),
        'pos += 1': '`pos` → {pos}',
        'f.append(pos)': '`f[{index}] = {pos}`，失败数组加一项',
        'pos = 0': lambda S, B, r: ('`pos` 清零，准备去 word 里匹配' if S['_line'] >= _MATCH_FROM
                                    else '`pos` 表示当前最长的相同前后缀长度'),
        'for char in word': '读入 word 的字符 `{char}`',
        'while pos > 0 and pattern[pos] != char': lambda S, B, r: (
            f"`pos = {S.pos}`：`pattern[{S.pos}] = {S.pattern[S.pos]}` ≠ `{S.char}` → ==失配，按 f 回退==" if S.pos > 0 and S.pattern[S.pos] != S.char
            else f"`pos = {S.pos}`：不用回退"),
        'if pattern[pos] == char': lambda S, B, r: (
            f"`{S.pattern[S.pos]}` == `{S.char}` → 匹配上一位" if S.pattern[S.pos] == S.char
            else f"`{S.pattern[S.pos]}` ≠ `{S.char}` → 这一位没匹配上，`pos` 保持 {S.pos}"),
        'if pos == len(pattern)': lambda S, B, r: (
            f"`pos == len(pattern) = {len(S.pattern)}` → ==整个模式串匹配完了=="
            if S.pos == len(S.pattern) else f"`pos = {S.pos} < {len(S.pattern)}`，继续读下一个字符"),
        'res += 1': '`{pattern}` 是 word 的子串，`res` → {res}；不用再找了，`break`',
        'break': '已经确认出现过，跳出去换下一个模式串',
        'return res': '一共 `{res}` 个模式串出现在 word 中',
    },
    cards=dict(
        one_liner='模式串不多不长：逐个用 KMP 判断是不是子串',
        complexity='时间 `O(L + n·m)`（`m` 个模式串），空间 `O(len(pattern))`',
        problem=['给 `patterns` 和 `word`，数有多少个模式串是 `word` 的==子字符串==',
                 '示例：`["a","abc","bc","d"]`，`"abc"` → `3`',
                 '本视频：`["aba","bc"]`，`"abc"` → `1`'],
        quote='由于题目的数据规模较小，因此可以直接枚举每个pattern，然后暴力检测其是否是word的子串。我在这里采用了kmp做匹配，可以稍微起到点优化的作用。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，直接==枚举每个 pattern==，判断它是否出现在 word 中',
              '判断用 KMP：先建失败数组 `f`，匹配失败时 `pos` 按 `f` 回退而不是从头来',
              '只要匹配满一次（`pos == len(pattern)`）就计数并 `break`'],
        result='`"bc"` 出现了，`"aba"` 没有 → 1 ✓',
        summary=['时间 `O(m·(len(pattern)+n))`，空间 `O(len(pattern))`',
                 '匹配成功要立刻 `break`，否则同一个 pattern 可能被重复计数',
                 '`while pos > 0` 回退时必须写在 `if` 判断之前',
                 '本题直接 `pattern in word` 也能过；KMP 是练习，原文自称“稍微起到点优化的作用”',
                 '原文是 Python 2 风格（`class Solution(object)`），在 Python 3 下无需改动'],
    ),
)
