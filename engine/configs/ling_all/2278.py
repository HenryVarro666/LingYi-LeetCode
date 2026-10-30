def _txt(S):
    if 'letter' not in S:
        return ''
    s, l = S['s'], S['letter']
    c = s.count(l)
    return f"`s` 中共 `{len(s)}` 个字符，`'{l}'` 出现 =={c}== 次：`{c} × 100 // {len(s)}` = =={c * 100 // len(s)}=="


CONFIG = dict(
    num=2278, title='字母在字符串中的百分比', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='统计个数 · 整除',
    tags=[],
    code='''
class Solution:
    def percentageLetter(self, s: str, letter: str) -> int:
        return s.count(letter) * 100 // len(s)
''',
    call='Solution().percentageLetter("foobarbaz", "o")',
    expect=22,
    views=[
        dict(type='string', var='s', label='s（绿 = 等于 letter 的字符）', cell=90, h=250,
             color=lambda S, i, v: 'green' if v == S['letter'] else None),
        dict(type='text', h=120, size=30, fn=_txt),
    ],
    watch=[('letter', 'letter', 'green'), ('len(s)', 'len(s)', 'blue'), ('s.count(letter)', 's.count(letter)', 'orange')],
    captions={
        'return s.count': '`s.count(letter) = {s.count(letter)}`，乘 100 得 `{s.count(letter) * 100}`，再 `// {len(s)}`（整除就是向下取整）→ =={s.count(letter) * 100 // len(s)}==',
    },
    cards=dict(
        one_liner='数出 letter 的个数 c，答案是 100c 除以 n 向下取整',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['返回 `s` 中等于 `letter` 的字符所占的百分比，==向下取整==',
                 '示例：`s = "foobar"`，`letter = "o"` → `33`',
                 '本视频：`s = "foobarbaz"`，`letter = "o"` → `22`（2/9）'],
        quote='统计 s 中 letter 的个数，记作 c。根据题意，答案为 ⌊100c / n⌋，其中 n 是 s 的长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用 `s.count(letter)` 一次统计出 `c`',
              '先乘 100 再整除 `n`，Python 的 `//` 就是向下取整',
              '整个函数只有一行 `return`，所以重点是理解公式 ⌊100c / n⌋'],
        after=[dict(heading='为什么先乘 100', lines=['`2 / 9 × 100 = 22.2…`，向下取整得 `22`', '`2 * 100 // 9 = 200 // 9 = 22`，一步到位', '如果先算 `2 // 9` 会得到 `0`，再乘 100 还是 `0`，错'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：要==先乘 100 再除==；先除会变成 0 或小数',
                 '用 `//` 而不是 `/`，否则返回浮点数'],
    ),
)
