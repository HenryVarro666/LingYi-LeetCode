CONFIG = dict(
    num=1392, title='最长快乐前缀', difficulty='Hard', category='字符串',
    author='yiduobo', technique='KMP next 数组末项',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def longestPrefix(self, s):

        f = [0]
        n = len(s)
        pos = 0
        for index in range(1, n):
            while pos > 0 and s[pos] != s[index]:
                pos = f[pos - 1]
            if s[pos] == s[index]:
                pos += 1
            f.append(pos)
        
        return s[:f[-1]]
''',
    call='Solution().longestPrefix("aabaaab")',
    expect='aab',
    views=[
        dict(type='string', var='s', label='s（绿 = 当前匹配上的前缀 s[:pos]）', cell=84, h=270,
             pointers={'pos': 'blue', 'index': 'pink'},
             color=lambda S, k, v: ('green' if S.get('pos') and k < S['pos'] else None)),
        dict(type='array', var='f', label='f[i]：s[:i+1] 中最长的「前缀 = 后缀」长度', cell=84, h=200),
        dict(type='text', size=28, h=80, fn=lambda S: (
            f"答案 = `s[:f[-1]]` = `s[:{S['f'][-1]}]` = =={S['s'][:S['f'][-1]]}==" if S.get('_line') == 14 and 'f' in S
            else '快乐前缀：既是前缀又是后缀（不能是整个字符串）的最长子串')),
    ],
    watch=[('index', 'index', 'pink'), ('pos', 'pos', 'blue'), ('f', 'f', 'green')],
    captions={
        'f = [0]': '`f[i]` 就是 kmp 的 next 数组；单个字符没有真前缀，`f[0] = 0`',
        'n = len': '`n = {n}`',
        'pos = 0': '`pos` 表示当前已经匹配上的前缀长度',
        'for index in range': '`index = {index}`：看 `s[{index}]` 能不能接在已匹配的前缀 `s[:pos]` 后面',
        'while pos > 0 and s[pos] != s[index]': lambda S, B, r: (
            f"`s[{S.pos}] = {S.s[S.pos]}` ≠ `s[{S.index}] = {S.s[S.index]}`：失配，`pos` 退到 `f[{S.pos-1}] = {S.f[S.pos-1]}`，试更短的前缀" if S.pos > 0 and S.s[S.pos] != S.s[S.index]
            else '`pos = 0` 或已经相等，不再回退'),
        'pos = f[pos - 1]': '不从头比，借助已有的 `f` 回退：`pos` → {pos}',
        'if s[pos] == s[index]': lambda S, B, r: (
            f"`s[{S.pos}] = {S.s[S.pos]}` == `s[{S.index}]` → 前缀能再延长一位" if S.s[S.pos] == S.s[S.index]
            else f"`s[{S.pos}] = {S.s[S.pos]}` ≠ `s[{S.index}] = {S.s[S.index]}` → 以 `s[{S.index}]` 结尾没有可匹配的前缀"),
        'pos += 1': '`pos` → {pos}',
        'f.append(pos)': '`f[{index}] = {pos}`：以 `s[{index}]` 结尾的最长快乐前缀长度',
        'return s[:f[-1]]': lambda S, B, r: f"`f[-1] = {S.f[-1]}`：整个 s 的最长「前缀 = 后缀」长度 → 答案 `\"{r}\"`",
    },
    cards=dict(
        one_liner='最长快乐前缀 = kmp 的 next 数组最后一项',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['快乐前缀：==既是前缀、又是后缀==的非空子串（不含 s 本身）',
                 '返回 `s` 的最长快乐前缀，没有则返回空串',
                 '示例：`"level"` → `"l"`；`"ababab"` → `"abab"`；本视频：`"aabaaab"` → `"aab"`'],
        quote='next[-1]表示的就是字符串s中最长的，且满足与前缀相同的后缀的长度，那么s[:next[-1]]就是我们要求的答案了。',
        quote_src='—— yiduobo 题解原文',
        idea=['回忆 kmp：`f[i]` 是以第 i 个字符结尾、能和前缀匹配的最长长度',
              '整个字符串的 `f[-1]`，正是最长的「后缀 = 前缀」长度',
              '所以只需建好 next 数组，返回 `s[:f[-1]]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`f[-1] = 0` 时 `s[:0]` 就是空串，正好符合「没有则返回空」',
                 '建 `f` 时失配要用 `pos = f[pos - 1]` 回退，而不是 `pos = 0`',
                 '原文就是这段 kmp 建表代码，没有 Python 2 特有写法，无需改动'],
    ),
)
