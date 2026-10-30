def _top(S):
    if 'f' not in S:
        return '`f[i]`：以 `s[i]` 结尾的子串，最长能匹配到 `s` 前缀的长度（KMP 的 next 数组）'
    line = S.get('_line', 0)
    if line <= 12:
        return f'KMP 求 `f`：`pos = {S["pos"]}` 是当前已匹配的前缀长度；`f = {S["f"]}`'
    if line <= 16:
        return f'`g[k]` = 匹配 `k` 个字符的前缀出现的次数；先对每个 `f[i]` 计一次：`g = {S["g"]}`'
    return f'从后往前：把 `g[i]` 传给 `g[f[i-1]]`（套娃的更短匹配）：`g = {S["g"]}`'


def _gcol(S, k, v):
    line, idx, f = S.get('_line', 0), S.get('index'), S.get('f')
    if line < 16 or idx is None or not f or idx >= len(f):
        return None
    if line == 16 and k == f[idx]:
        return 'green'
    if line == 19 and idx >= 1 and k == f[idx - 1]:
        return 'green'
    return None


CONFIG = dict(
    num=2223, title='构造字符串的总得分和', difficulty='Hard', category='字符串',
    author='yiduobo', technique='KMP next 数组 + 次数 DP',
    tags=['灵神题单', '字符串', '难度分 2220'],
    code='''
class Solution(object):
    def sumScores(self, s):

        pos = 0
        f = [0]
        n = len(s)
        for index in range(1, n):
            while pos > 0 and s[pos] != s[index]:
                pos = f[pos - 1]
            if s[pos] == s[index]:
                pos += 1
            f.append(pos)

        g = [0] * n
        for index in range(n):
            g[f[index]] += 1
        
        for index in range(n - 1, 0, -1):
            g[f[index - 1]] += g[index]

        return n + sum(g[1:])
''',
    call='Solution().sumScores("ababcab")',
    expect=11,
    views=[
        dict(type='text', fn=_top, size=25, h=80),
        dict(type='string', var='s', label='s（粉 = s[index]，蓝 = s[pos]）', cell=76, h=210,
             pointers={'index if _line <= 12 else -9': 'pink', 'pos if _line <= 12 else -9': 'blue'},
             pointer_labels={'index if _line <= 12 else -9': 'index', 'pos if _line <= 12 else -9': 'pos'},
             color=lambda S, k, v: 'pink' if k == S.get('index') and S.get('_line', 0) <= 13 else None),
        dict(type='array', var='f', label='f（next 数组）', cell=76, h=215,
             pointers={'index': 'pink'}),
        dict(type='array', var='g', label='g（g[k]：匹配长度 ≥ k 的后缀个数；g[0] 不计）', cell=76, h=190,
             color=_gcol),
    ],
    watch=[('pos', 'pos', 'blue'), ('index', 'index', 'pink'), ('n', 'n')],
    captions={
        'pos = 0': '`pos` 表示已经匹配上的前缀长度，也是下一个要比较的前缀下标',
        'f = [0]': '`f[0] = 0`：单个字符没有真前缀可匹配',
        'n = len': '`n = {n}`',
        'for index in range(1, n)': lambda S, B, ret: (f"用 `s[{S.index}] = {S.s[S.index]}` 去扩展匹配" if len(S.f) < len(S.s)
                                                      else '`s` 的每个位置都处理完了，`f` 构造完毕'),
        'for index in range(n):': lambda S, B, ret: (f'枚举 `index = {S.index}`' if not (B.get('index') == S.index and S.index == len(S.s) - 1)
                                                     else '`f` 里每个值都计过一次了'),
        'for index in range(n - 1': lambda S, B, ret: ('从大到小枚举：先传长的，再传短的' if B.get('index') == S.index == len(S.s) - 1
                                                       else ('传递完毕，`g` 里是每个匹配长度的出现次数' if B.get('index') == S.index == 1
                                                             else f'`index = {S.index}`')),
        'while pos > 0': lambda S, B, ret: (
            f"`s[{S.pos}] = '{S.s[S.pos]}'` ≠ `s[{S.index}] = '{S.s[S.index]}'`：失配，==回退==到 `f[{S.pos - 1}]` = {S.f[S.pos - 1]}"
            if S.pos > 0 and S.s[S.pos] != S.s[S.index] else
            ('`pos = 0`，没法再回退了' if S.pos == 0 else f"`s[{S.pos}] = s[{S.index}] = '{S.s[S.pos]}'`，不用回退")),
        'pos = f[pos - 1]': '回退：`pos` → `{pos}`（上一个更短的前缀匹配）',
        'if s[pos] == s[index]': lambda S, B, ret: (
            f"`s[{S.pos}] = '{S.s[S.pos]}'` == `s[{S.index}] = '{S.s[S.index]}'` → 匹配长度加一"
            if S.s[S.pos] == S.s[S.index] else f"`s[{S.pos}] = '{S.s[S.pos]}'` ≠ `s[{S.index}] = '{S.s[S.index]}'` → 匹配长度为 0"),
        'pos += 1': '`pos` → `{pos}`',
        'f.append(pos)': '`f[{index}] = {pos}`：以 `s[{index}]` 结尾的子串最长匹配前缀 {pos}',
        'g = [0] * n': '`g[k]`：能匹配前缀 `k` 个字符的子串出现==次数==。长度改成次数，避免重复算同一个后缀',
        'g[f[index]] += 1': '`f[{index}] = {f[index]}`，所以 `g[{f[index]}]` += 1 → {g[f[index]]}',
        'g[f[index - 1]] += g[index]': ('`g[{index}] = {g[index]}` 次：这些匹配的更短前缀（长度 `{f[index - 1]}`）也同样出现 → '
                                       '`g[{f[index - 1]}]` 加上 `{g[index]}` = {g[f[index - 1]]}'),
        'return n + sum': '`n + sum(g[1:])` = `{n}` + `{sum(g[1:])}` = =={ret}==：整串本身加上其余所有匹配',
    },
    cards=dict(
        one_liner='用 next 数组统计「前缀出现次数」，套娃往回累加',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s_i` 是 `s` 的长度为 `i` 的后缀，得分 = 与 `s` 的最长公共前缀长度',
                 '求所有后缀得分之和（整串得分是 `n`）',
                 '示例：`babab` → `9`；本视频：`ababcab`'],
        quote='将统计长度转化为统计次数……令g[i]表示能与字符串前缀匹配i个字符的子串出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`next[i]` 只记最长的匹配，且同一个后缀会被多个 `next` 重复覆盖 → ==改数次数==',
              '`g[f[i]] += 1` 先计最长匹配；长度 `i` 的匹配也意味着更短的前缀 `f[i-1]` 的匹配',
              '从大到小 `g[f[i-1]] += g[i]`，一路套娃传下去；最后 `n + sum(g[1:])`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`g[0]` 不计入：长度为 0 的匹配没有得分',
                 '不能直接累加 `next`：同一个后缀会重复算，而且漏掉更短的后缀',
                 '必须从大到小传递 `g`，否则次数还没累加完整',
                 '原文已是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：他直接用 Z 函数一趟得到每个后缀的 LCP'],
    ),
)
