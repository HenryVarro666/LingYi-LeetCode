def _top(S):
    if 'length' not in S:
        return '把 `s1` 的后缀和 `s2` 的前缀重叠起来，重叠越长，拼出来的串越短'
    n, m, L = S['n'], S['m'], S['length']
    a, b = S['s1'][n - L:], S['s2'][:L]
    c, d = S['s2'][m - L:], S['s1'][:L]
    return f'重叠长度 `{L}`：`s1` 后缀 `{a}` vs `s2` 前缀 `{b}`；`s2` 后缀 `{c}` vs `s1` 前缀 `{d}`'


def _w1(S):
    return None


CONFIG = dict(
    num=3571, title='最短超级串 II', difficulty='Easy', category='字符串',
    author='yiduobo', technique='枚举重叠长度（从大到小）',
    tags=['灵神题单', '字符串', '难度分 2800'],
    code='''
class Solution(object):
    def shortestSuperstring(self, s1, s2):
        
        if s1.find(s2) != -1:
            return s1
        if s2.find(s1) != -1:
            return s2

        n = len(s1)
        m = len(s2)
        for length in range(min(n, m) - 1, 0, -1):
            if s1[n - length:] == s2[:length]:
                return s1 + s2[length:]
            if s2[m - length:] == s1[:length]:
                return s2 + s1[length:]
        
        return s1 + s2
''',
    call='Solution().shortestSuperstring("abcde", "cdefg")',
    expect='abcdefg',
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='s1', label='s1（蓝框 = 参与比较的后缀 / 前缀）', cell=84, h=190,
             window=('n - length', 'n - 1'), color=lambda S, i, v: 'blue' if 'length' in S and i >= S['n'] - S['length'] else None),
        dict(type='string', var='s2', label='s2（粉框 = 参与比较的前缀）', cell=84, h=190,
             window=('0', 'length - 1'), color=lambda S, i, v: 'pink' if 'length' in S and i < S['length'] else None),
        dict(type='text', fn=lambda S: '答案 = `s1 + s2[length:]`，即去掉重叠部分再拼接' if 'length' in S else '', size=24, h=60),
    ],
    watch=[('length', 'length', 'blue'), 'n', 'm'],
    captions={
        'if s1.find(s2) != -1': lambda S, B, ret: ('`s1` 已经包含 `s2` → 直接用 `s1`' if S.s1.find(S.s2) != -1
                                                   else '`s1` 里找不到 `s2`，继续'),
        'return s1\n': '`s1` 完全包含 `s2`，答案就是 `s1`',
        'if s2.find(s1) != -1': lambda S, B, ret: ('`s2` 已经包含 `s1` → 直接用 `s2`' if S.s2.find(S.s1) != -1
                                                   else '`s2` 里也找不到 `s1`，需要拼接'),
        'n = len': '`n = {n}`，`s1` 的长度',
        'm = len': '`m = {m}`，`s2` 的长度',
        'for length in range': lambda S, B, ret: (f'枚举重叠长度 `length = {S.length}`，==从大到小==：先试最长的重叠，拼出来最短'
                                                  if 'length' in S else '没有任何重叠'),
        'if s1[n - length:] == s2[:length]': lambda S, B, ret: (
            f"`s1` 后缀 `{S.s1[S.n - S.length:]}` == `s2` 前缀 `{S.s2[:S.length]}` → ==重叠成功=="
            if S.s1[S.n - S.length:] == S.s2[:S.length]
            else f"`s1` 后缀 `{S.s1[S.n - S.length:]}` ≠ `s2` 前缀 `{S.s2[:S.length]}`，这个方向不行"),
        'return s1 + s2[length:]': '`s1` 在前，去掉 `s2` 前面重叠的 `{length}` 个字符 → `{ret}`',
        'if s2[m - length:] == s1[:length]': lambda S, B, ret: (
            f"`s2` 后缀 `{S.s2[S.m - S.length:]}` == `s1` 前缀 `{S.s1[:S.length]}` → ==重叠成功=="
            if S.s2[S.m - S.length:] == S.s1[:S.length]
            else f"`s2` 后缀 `{S.s2[S.m - S.length:]}` ≠ `s1` 前缀 `{S.s1[:S.length]}`，这个方向也不行，`length` 减一"),
        'return s2 + s1[length:]': '`s2` 在前，去掉 `s1` 前面重叠的 `{length}` 个字符 → `{ret}`',
        'return s1 + s2\n': '完全没有重叠，只能直接拼接 → `{ret}`',
    },
    cards=dict(
        one_liner='先判包含，再找最长重叠：s1 后缀 = s2 前缀（或反过来）',
        complexity='时间 `O(min(n, m) * (n + m))`，空间 `O(n + m)`',
        problem=['给两个字符串 `s1`、`s2`（长度都不超过 100），求同时包含两者作为子串的==最短==字符串',
                 '多个答案任意返回一个',
                 '示例：`aba`、`bab` → `abab`；本视频：`abcde`、`cdefg` → `abcdefg`'],
        quote='s1的后缀与s2的前缀重叠的部分越多，s就越短；而对于后面这种情况，s1的前缀与s2的后缀重叠的部分越多，s就越短。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理特殊情况：一个串包含另一个，答案就是较长的那个',
              '否则要么 s1 在前、s2 在后，要么反过来；中间能重叠就去掉重叠',
              '数据规模小，==从大到小==枚举重叠长度，第一个成功的就最短'],
        result='重叠 `cde` 后拼成 `abcdefg`，长度 7 = 5 + 5 - 3 ✓',
        summary=['时间 `O(min(n, m) * (n + m))`，空间 `O(n + m)`',
                 '枚举 `length` 从 `min(n, m) - 1` 起：整串包含的情况已被前面特判',
                 '两个方向都要试：`s1` 在前，或 `s2` 在前',
                 '没有任何重叠时直接 `s1 + s2`',
                 '原文已是 Python 3 可运行的写法，代码未改动'],
    ),
)
