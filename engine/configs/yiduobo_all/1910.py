def _s_color(S, i, v):
    if 'index' not in S:
        return None
    if i == S['index']:
        return 'blue'
    return None


def _p_color(S, i, v):
    return 'green' if 'pos' in S and i < S['pos'] else None


def _txt(S):
    if 'index' not in S:
        return '先给 `part` 求前缀函数 `f`：`f[i]` = `part[0..i]` 最长的相等真前后缀长度'
    return f"`pos = {S['pos']}`：当前已经匹配了 `part` 的前 {S['pos']} 个字符；`g` 保存每个保留字符对应的 pos，用来回档"


CONFIG = dict(
    num=1910, title='删除一个字符串中所有出现的给定子字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='KMP + 栈式回档',
    tags=[],
    code='''
class Solution:
    def removeOccurrences(self, s, part):

        f = []
        m = len(part)

        pos = 0
        f.append(0)
        for index in range(1, m):
            while pos > 0 and part[pos] != part[index]:
                pos = f[pos - 1]
            if part[pos] == part[index]:
                pos += 1
            f.append(pos)

        pos = 0
        res = []
        g = []
        for index in range(len(s)):
            res.append(s[index])
            while pos > 0 and part[pos] != s[index]:
                pos = f[pos - 1]
            if part[pos] == s[index]:
                pos += 1
            g.append(pos)
            if pos == m:
                for _ in range(m):
                    res.pop()
                    g.pop()
                if g:
                    pos = g[-1]
                else:
                    pos = 0
        
        return ''.join(res)
''',
    call='Solution().removeOccurrences("daabcbc", "abc")',
    expect='d',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前读到的字符）', cell=90, h=140,
             pointers={'index': 'blue'}, color=_s_color),
        dict(type='string', var='part', label='part（绿 = 已匹配的前缀，长度 pos）', cell=90, h=140,
             color=_p_color),
        dict(type='array', var='res', label='res（当前保留的字符，相当于栈）', cell=84, h=130),
        dict(type='array', var='g', label='g（res 每个位置对应的 pos，回档用）', cell=84, h=130),
        dict(type='array', var='f', label='f（part 的前缀函数）', cell=84, h=120),
        dict(type='text', size=26, h=80, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('pos', 'pos', 'green'), ('m', 'm', 'purple'), ('res', "''.join(res) if 'res' in locals() else ''", 'orange')],
    captions={
        'f = []': '`f` 用来放 `part` 的前缀函数',
        'm = len(part)': '`part` 长度 `m = {m}`',
        'f.append(0)': '`f[0] = 0`：单个字符没有真前后缀',
        'for index in range(1, m)': lambda S, B, ret: (f'求 `f[{S.index}]`：看 `part[{S.index}] = {S.part[S.index]!r}` 能否接在当前前缀后面'
                                                    if 'index' in S and 1 <= S.index < S.m else '前缀函数求完了'),
        'while pos > 0 and part[pos] != part[index]': lambda S, B, ret: (
            f'`part[{S.pos}] = {S.part[S.pos]!r}` ≠ `part[{S.index}] = {S.part[S.index]!r}`：失配，`pos` 退到 `f[pos−1]` = {S.f[S.pos - 1]}'
            if S.pos > 0 and S.part[S.pos] != S.part[S.index] else '不用回退'),
        'if part[pos] == part[index]': lambda S, B, ret: (
            f'`part[{S.pos}] == part[{S.index}]` → 前缀能多延长一位' if S.part[S.pos] == S.part[S.index]
            else f'`part[{S.pos}] ≠ part[{S.index}]` → `pos` 保持 {S.pos}'),
        'pos += 1': '`pos` → `{pos}`',
        'f.append(pos)': '`f[{index}] = {pos}`',
        'res = []': '`res` 是保留下来的字符（栈）',
        'g = []': '`g` 记录 `res` 里每个字符之后的匹配长度 `pos`，用于删除后==回档==',
        'for index in range(len(s))': lambda S, B, ret: (f'读 `s[{S.index}] = {S.s[S.index]!r}`' if S.get('index') != B.get('index') or 'index' not in B else '`s` 读完了'),
        'res.append(s[index])': '先把 `{s[index]!r}` 放进 `res`：`{res}`',
        'while pos > 0 and part[pos] != s[index]': lambda S, B, ret: (
            f'`part[{S.pos}] = {S.part[S.pos]!r}` ≠ `{S.s[S.index]!r}`：失配，`pos` 按 `f` 退到 {S.f[S.pos - 1]}'
            if S.pos > 0 and S.part[S.pos] != S.s[S.index] else '能接上或 pos 已是 0，不用回退'),
        'if part[pos] == s[index]': lambda S, B, ret: (
            f'`part[{S.pos}] = {S.part[S.pos]!r}` == `{S.s[S.index]!r}` → 匹配长度加一' if S.part[S.pos] == S.s[S.index]
            else f'`part[{S.pos}] = {S.part[S.pos]!r}` ≠ `{S.s[S.index]!r}` → 匹配长度保持 {S.pos}'),
        'g.append(pos)': '记下这个位置的匹配长度：`g = {g}`',
        'if pos == m': lambda S, B, ret: (f'`pos == m = {S.m}`：`res` 末尾刚好是一个 `part`，要==删掉==' if S.pos == S.m
                                          else f'`pos = {S.pos} < m`，还没匹配完整'),
        'res.pop()': '`res` 末尾弹出一个字符 → `{res}`',
        'g.pop()': '`g` 同步弹出 → `{g}`：这样连删 `m` 个',
        'if g:': lambda S, B, ret: (f'`g` 不空：回档，`pos` 取 `g[-1]` = {S.g[-1]}' if S.g
                                    else '`g` 空了：回到最开始，`pos = 0`'),
        'pos = g[-1]': '`pos` 回到 `{pos}`：删掉之后继续接着旧的匹配状态走，可能又拼出新的 `part`',
        'pos = 0': '`pos = 0`',
        'return': "全部读完，`res` 拼起来返回 `{ret!r}`",
    },
    skip=['f = []', 'm = len', 'for _ in range(m)', 'f.append(0)'],
    max_steps=90,
    cards=dict(
        one_liner='KMP 匹配，命中就弹栈，pos 靠 g 回档',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['反复删除 `s` 中==最左边==的子串 `part`，直到不再含有 `part`',
                 '返回最终剩下的字符串',
                 '示例：`s = "daabcbaabcbc", part = "abc"` → `"dab"`'],
        quote='再出现匹配后需要将其从答案中删去，同时用来表示part前缀匹配长度的变量pos也需要回档。关于回档，最简单的想法就是将匹配过程中的所有pos都储存起来。',
        quote_src='—— yiduobo 题解',
        idea=['数据不大，平方暴力可行；yiduobo 选更好的 ==KMP==',
              '一边读字符一边放进 `res`，同时用 `g` 记下每个位置的 `pos`',
              '`pos == m` 就弹出 `m` 个字符，`pos` 取 `g[-1]`（空则为 0）'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '易错：删除后 `pos` 必须回档，否则 `abc` 删掉后拼出的新 `abc` 会漏掉',
                 '`g` 为空时 `pos` 要置 0，不能访问 `g[-1]`',
                 '同类题：栈 + 字符串匹配的消除问题'],
    ),
)
