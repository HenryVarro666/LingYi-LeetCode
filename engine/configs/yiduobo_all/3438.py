S0 = "2523533"


def _cond(S):
    if 'index' not in S or 'cnt' not in S or S['_line'] < 9:
        return ''
    s, i, c = S['s'], S['index'], S['cnt']
    p, q = s[i - 1], s[i]
    a = '==✓==' if p != q else '✗'
    b = '==✓==' if c[int(p)] == int(p) else '✗'
    d = '==✓==' if c[int(q)] == int(q) else '✗'
    return f"`s[{i-1}] != s[{i}]` {a}　　`cnt[{p}] == {p}`（{c[int(p)]} vs {p}）{b}　　`cnt[{q}] == {q}`（{c[int(q)]} vs {q}）{d}"


CONFIG = dict(
    num=3438, title='找到字符串中合法的相邻数字', difficulty='Easy', category='字符串',
    author='yiduobo', technique='先计数，再从下标 1 扫描相邻对',
    code='''
class Solution(object):
    def findValidPair(self, s):
        
        cnt = [0] * 10
        for digit in s:
            cnt[int(digit)] += 1
        
        for index in range(1, len(s)):
            if s[index] != s[index - 1] and cnt[int(s[index - 1])] == int(s[index - 1]) and cnt[int(s[index])] == int(s[index]):
                return s[index - 1: index + 1]
        
        return ""
''',
    call=f'Solution().findValidPair("{S0}")',
    expect='23',
    views=[
        dict(type='string', var='s', label='s（蓝 = s[index-1]，粉 = s[index]）', cell=84, h=240,
             pointers={'index-1': 'blue', 'index': 'pink'}, window=('index-1', 'index')),
        dict(type='array', var='cnt', label='cnt[d] = 数字 d 出现的次数（下标 = 数字）', cell=70, h=190,
             color=lambda S, k, v: 'yellow' if S.get('digit') is not None and S['_line'] == 6 and k == int(S['digit']) else None),
        dict(type='text', fn=_cond, size=24),
    ],
    watch=[('digit', 'digit', 'yellow'), ('index', 'index', 'pink')],
    captions={
        'cnt = [0] * 10': '数字只有 `1`~`9`，开长度 10 的数组，下标 `d` 记数字 `d` 的出现次数',
        'for digit in s': lambda S, B, r: (f'第一趟：统计次数，当前数字 `{S.digit}`' if sum(S.cnt) < len(S.s) else '统计完毕'),
        'cnt[int(digit)] += 1': '数字 `{digit}` 出现一次：`cnt[{digit}] = {cnt[int(digit)]}`',
        'for index in range(1, len(s))': lambda S, B, r: (f'第二趟：从下标 1 开始，看 `s[{S.index - 1}]` 和 `s[{S.index}]`（`{S.s[S.index - 1]}{S.s[S.index]}`）' if S.get('index') != B.get('index') or 'index' not in B else '没有找到合法对'),
        'if s[index] != s[index - 1]': lambda S, B, r: (f"`{S.s[S.index - 1]}` ≠ `{S.s[S.index]}`：{S.s[S.index - 1] != S.s[S.index]}；`cnt[{S.s[S.index - 1]}] = {S.cnt[int(S.s[S.index - 1])]}`（要 {S.s[S.index - 1]}）；`cnt[{S.s[S.index]}] = {S.cnt[int(S.s[S.index])]}`（要 {S.s[S.index]}） → "
                                                         + ('==合法==' if (S.s[S.index] != S.s[S.index - 1] and S.cnt[int(S.s[S.index - 1])] == int(S.s[S.index - 1]) and S.cnt[int(S.s[S.index])] == int(S.s[S.index])) else '不合法，继续')),
        'return s[index - 1: index + 1]': '返回这一对：`{s[index - 1: index + 1]}`',
        'return ""': '没有合法对，返回空字符串',
    },
    cards=dict(
        one_liner='第一趟数出每个数字的次数，第二趟从下标 1 逐对检查',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 只含数字。相邻两数合法：==两数不等==，且各自在 `s` 中出现次数等于自身数值',
                 '返回最先出现的合法相邻数字，没有则返回空串',
                 '示例：`"2523533"` → `"23"`'],
        quote='由于需要判断某个数出现的次数是否恰好就等于其自身的数值，那么就需要先进行一趟遍历，统计每种数字出现的次数。接下来再从下标1开始进行一趟遍历，判断当前的s[index - 1]以及s[index]是否符合题目给出的条件就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt = [0] * 10`，用数组下标当数字，比哈希表简单',
              '第二趟枚举 `index` 从 1 开始，左边是 `s[index - 1]`，右边是 `s[index]`',
              '三个条件写在一个 `if` 里，第一个命中就返回切片 `s[index - 1: index + 1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`（`cnt` 固定 10 个格子）',
                 '易错：`s` 的元素是字符，下标和比较都要先 `int(...)`',
                 '`range(1, len(s))` 才不会让 `s[index - 1]` 越界到 `s[-1]`',
                 '原文为 Python 2 风格，代码无需修改，Python 3 直接可运行',
                 '对比灵神：灵神用 `Counter` + `pairwise`，不用下标；这里手动计数并用下标扫描'],
    ),
)
