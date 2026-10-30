S0 = "2523533"


def _cond(S):
    if 'x' not in S or 'cnt' not in S:
        return ''
    x, y, c = S['x'], S['y'], S['cnt']
    a = '==✓==' if x != y else '✗'
    b = '==✓==' if c[x] == int(x) else '✗'
    d = '==✓==' if c[y] == int(y) else '✗'
    return f"`x != y` {a}　　`cnt[{x}] == {x}`（{c[x]} vs {x}）{b}　　`cnt[{y}] == {y}`（{c[y]} vs {y}）{d}"


CONFIG = dict(
    num=3438, title='找到字符串中合法的相邻数字', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='Counter + pairwise',
    code='''
class Solution:
    def findValidPair(self, s: str) -> str:
        cnt = Counter(s)
        for x, y in pairwise(s):
            if x != y and cnt[x] == int(x) and cnt[y] == int(y):
                return x + y
        return ""
''',
    call=f'Solution().findValidPair("{S0}")',
    expect='23',
    views=[
        dict(type='string', var='s', label='s（蓝 = x，粉 = y，相邻的一对）', cell=84, h=240,
             pointers={'s.find(x+y)': 'blue', 's.find(x+y)+1': 'pink'}, pointer_labels={'s.find(x+y)': 'x', 's.find(x+y)+1': 'y'},
             window=('s.find(x+y)', 's.find(x+y)+1')),
        dict(type='map', var='cnt', label='cnt（每个数字出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170),
        dict(type='text', fn=_cond, size=24),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        'cnt = Counter(s)': '先统计每个数字出现的次数：`{dict(cnt)}`',
        'for x, y in pairwise(s)': lambda S, B, r: (f"取相邻的一对 `x = {S.x}`，`y = {S.y}`" if S.get('x') != B.get('x') or S.get('y') != B.get('y') or 'x' not in B else '所有相邻对都看过了'),
        'if x != y': lambda S, B, r: (f"`x = {S.x}`，`y = {S.y}`：`{S.x} != {S.y}`，`cnt[{S.x}] = {S.cnt[S.x]}` 要等于 {S.x}，`cnt[{S.y}] = {S.cnt[S.y]}` 要等于 {S.y} → "
                                       + ('==三条都满足，合法=='
                                          if S.x != S.y and S.cnt[S.x] == int(S.x) and S.cnt[S.y] == int(S.y)
                                          else ('有一条不满足，换下一对' if S.x != S.y else '两个数字相同，不合法，换下一对'))),
        'return x + y': '找到最先出现的合法相邻数字：`{x + y}`',
        'return ""': '没有合法的相邻数字，返回空字符串',
    },
    cards=dict(
        one_liner='先数每个数字出现几次，再从左到右找第一对满足条件的相邻数字',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`，`|Σ| = 10`',
        problem=['`s` 只含数字。相邻两个数字合法：==两数不相等==，且每个数字在 `s` 中出现的次数恰好等于它自己',
                 '从左到右找，返回==最先==出现的合法相邻数字，没有就返回空串',
                 '示例：`"2523533"` → `"23"`（`2` 出现 2 次，`3` 出现 3 次）'],
        quote='统计 s 中每个数字的出现次数。遍历 s，如果相邻数字满足要求，返回这两个数字组成的字符串。如果没有满足要求的相邻数字，返回空字符串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`Counter(s)` 一次统计完，之后每个相邻对 `O(1)` 判断',
              '`pairwise(s)` 直接给出相邻对 `(x, y)`，不用写下标',
              '三个条件：`x != y`、`cnt[x] == int(x)`、`cnt[y] == int(y)`'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '易错：`s` 里是字符，要 `int(x)` 才能和次数比较；出现次数统计的是整个 `s`，不是这一对',
                 '`x != y` 不能漏：`"22"` 里 `2` 出现 2 次也不合法',
                 '从左到右第一个命中就返回，所以答案是最先找到的那对'],
    ),
)
