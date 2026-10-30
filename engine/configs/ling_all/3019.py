def _txt(S):
    x, y = S.get('x'), S.get('y')
    if x is None or y is None:
        return '大小写字母 ASCII 的低 5 位相同：`& 31` 之后相等就是同一个键'
    a, b = ord(x) & 31, ord(y) & 31
    return f"`ord('{x}') & 31 = {a}`，`ord('{y}') & 31 = {b}` → " + ('==不同键，计 1 次==' if a != b else '同一个键')


CONFIG = dict(
    num=3019, title='按键变更的次数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='相邻比较 · & 31 忽略大小写',
    code='''
class Solution:
    def countKeyChanges(self, s: str) -> int:
        return sum(ord(x) & 31 != ord(y) & 31 
                   for x, y in pairwise(s))
''',
    call="Solution().countKeyChanges('aAbBcCaA')",
    expect=3,
    views=[
        dict(type='string', var='s', label='s', cell=90, h=200),
        dict(type='text', fn=lambda S: '低 5 位编码：`' + ' '.join(str(ord(c) & 31) for c in S['s']) + '`（相邻不同处 = 换键）', h=110, size=30),
        dict(type='text', fn=_txt, h=100, size=30),
    ],
    watch=['x', 'y'],
    captions={
        'return sum': '遍历相邻字符 `(x, y)`，`& 31` 不同才算按键变更，最后求和',
        'for x, y': '`x = {x!r}`，`y = {y!r}`：{"低 5 位相同 → 同一个键" if ord(x) & 31 == ord(y) & 31 else "低 5 位不同 → ==换了按键=="}',
    },
    cards=dict(
        one_liner='大小写字母的低 5 位相同，`& 31` 后比相邻字符',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 是用户输入，相邻两次按的不是同一个键就算一次变更',
                 'Shift / Caps Lock 不算，所以 `a` 和 `A` 是同一个键',
                 '示例：`"aAbBcC"` → `2`；本视频：`"aAbBcCaA"` → `3`'],
        quote='对于同一字母的大写和小写，ASCII 值的二进制的低 5 位是相同的，所以只需统计 s[i-1] & 31 != s[i] & 31 的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['大写 `A`=65、小写 `a`=97，相差 32，二进制只差第 6 位',
              '`& 31` 取低 5 位，大小写变成同一个数',
              '用 `pairwise` 取相邻对，不相等就计 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：只统计相邻字符，`s[0]` 之前没有按键，不算变更',
                 '另一种写法：`pairwise(s.lower())` 直接比较，思路一样',
                 '位运算技巧：`& 31` 忽略大小写，`^ 32` 切换大小写'],
        after=[dict(heading='逐对检查本例', lines=['`aA`、`bB`、`cC`、`aA`：每对内部低 5 位相同',
                                                 '`A→b`、`B→c`、`C→a`：三处低 5 位不同',
                                                 '所以按键变更 `3` 次'])],
    ),
)
