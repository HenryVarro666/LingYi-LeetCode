CONFIG = dict(
    num=3931, title='检查相邻数字差', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='all + pairwise',
    tags=[],
    code='''
class Solution:
    def isAdjacentDiffAtMostTwo(self, s: str) -> bool:
        return all(abs(x - y) <= 2 for x, y in pairwise(map(ord, s)))
''',
    call='Solution().isAdjacentDiffAtMostTwo("13289")',
    expect=False,
    views=[
        dict(type='text', size=28, fn=lambda S: '`pairwise(map(ord, s))` 依次给出相邻两个字符的编码 `(x, y)`'),
        dict(type='string', var='s', label='s', cell=110, h=200),
        dict(type='array', var=lambda S: [abs(ord(S['s'][i]) - ord(S['s'][i - 1])) for i in range(1, len(S['s']))],
             label='相邻差 abs(x - y)（绿 = ≤ 2 合格，红 = 超限，灰 = 短路后不再看）', cell=110, h=220,
             color=lambda S, i, v: 'green' if v <= 2 else 'red',
             dim=lambda S, i, v: any(abs(ord(S['s'][k + 1]) - ord(S['s'][k])) > 2 for k in range(i))),
        dict(type='text', size=26, fn=lambda S: '第一个红格就让 `all` 立刻返回 ==False==，后面的不用再算'),
    ],
    watch=[('len(s)', 'len(s)', 'blue')],
    captions={
        'return all': lambda S, B, r: '差分别是 ' + ', '.join(str(abs(ord(S.s[i]) - ord(S.s[i - 1]))) for i in range(1, len(S.s))) + '：到第一个 `> 2` 的（==6==）`all` 就短路返回 `False`；若全部 `<= 2` 才是 `True`',
    },
    cards=dict(
        one_liner='相邻字符的差都不超过 2：all 一行搞定',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数字字符串 `s`，相邻两个数字的绝对差都 `≤ 2` 返回 `true`，否则 `false`',
                 '示例：`"132"` → `true`；`"129"` → `false`',
                 '本视频：`"13289"`，`|2-8| = 6` 超限 → `false`'],
        quote='遍历 s，如果 |s[i]-s[i-1]| > 2，返回 false。如果正常遍历完毕，返回 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`map(ord, s)`：字符转 ASCII 码，数字字符的码值差等于数字差，不用 `int()`',
              '`pairwise` 依次给出 `(s[0],s[1])`、`(s[1],s[2])` ……',
              '`all(...)` 遇到第一个不满足的就短路返回 `False`'],
        before=[dict(heading='三个小工具', lines=[
            '`map(ord, s)`：把每个字符变成编码，`"1"→49，"3"→51 …`',
            '`pairwise(it)`：相邻配对，`a b c d → (a,b) (b,c) (c,d)`',
            '`all(cond for ...)`：全部为真才真，遇到假立刻停'])],
        summary=['时间 `O(n)`，空间 `O(1)`（`pairwise` 是迭代器）',
                 '`ord` 直接相减：`ord("8") - ord("2") = 6`，省去 `int()`',
                 '`pairwise` 需要 Python 3.10+；`all` 遇到 `False` 即短路',
                 '写成显式循环就是：`for i in range(1, n)`，比较 `s[i]` 与 `s[i-1]`'],
    ),
)
