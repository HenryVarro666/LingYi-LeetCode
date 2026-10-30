def _pair(S):
    if 'x' not in S or 'y' not in S:
        return f'`word = "{S["s"]}"`：每相邻两个字母之间，需要补 `(y − x − 1) mod 3` 个字母'
    x, y = chr(S['x']), chr(S['y'])
    k = (S['y'] - S['x'] + 2) % 3
    fill = {0: '无需插入', 1: '插入 1 个', 2: '插入 2 个'}[k]
    return f"相邻 `'{x}'` → `'{y}'`：`(ord(y) − ord(x) + 2) % 3 = {k}`，=={fill}=="


def _fix(S):
    s = S['s']
    if 'ans' not in S:
        return '先看两端：开头应是 a，结尾应是 c'
    return f'当前累计插入 `ans = {S["ans"]}`'


def _loop(S, B, ret):
    if B.get('x') == S['x'] and B.get('y') == S['y']:
        return '相邻对都取完了，`pairwise` 迭代结束'
    return f"取下一对相邻字母：`x = '{chr(S.x)}'`，`y = '{chr(S.y)}'`"


CONFIG = dict(
    num=2645, title='构造有效字符串的最少插入数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='考虑相邻字母 · 模 3',
    tags=['贪心与思维'],
    code='''
class Solution:
    def addMinimum(self, s: str) -> int:
        ans = ord(s[0]) - ord(s[-1]) + 2
        for x, y in pairwise(map(ord, s)):
            ans += (y - x + 2) % 3
        return ans
''',
    call='Solution().addMinimum("aacb")',
    expect=5,
    views=[
        dict(type='text', fn=_pair, size=28, h=60),
        dict(type='string', var='s', label='s（"abc" 要循环：a → b → c → a …）', cell=110, h=170),
        dict(type='text', fn=_fix, size=28, h=60),
        dict(type='text', fn=lambda S: '补完后：`a[bc] | a[b]c | [a]b[c]` = `abcabcabc`，共 9 个字母 − 4 个原有 = 5', size=24, h=60),
    ],
    watch=[('ans', 'ans', 'green'), ('x', "chr(x)", 'blue'), ('y', "chr(y)", 'pink')],
    captions={
        'ans = ord(s[0])': '两端合并：开头缺 `s[0] − a` 个，结尾缺 `c − s[-1]` 个 → `ord(s[0]) − ord(s[-1]) + 2` = `{ord(s[0])} − {ord(s[-1])} + 2` = =={ans}==',
        'for x, y in pairwise': _loop,
        'ans += (y - x + 2) % 3': lambda S, B, r: (f"`('{chr(S.y)}' − '{chr(S.x)}' + 2) % 3 = {S.y - S.x + 2} % 3 = {(S.y - S.x + 2) % 3}`"
                                                    f"：这两个字母之间要补 {(S.y - S.x + 2) % 3} 个 → `ans = {S.ans}`"),
        'return ans': '所有相邻对都处理完，一共插入 =={ans}== 个字母',
    },
    cards=dict(
        one_liner='相邻两字母之间缺几个，加起来再补两端',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['可以在 `word` 任意位置插入 `a`、`b`、`c`，使它成为 `"abc"` 重复若干次',
                 '求最少插入次数',
                 '示例：`"b"` → `2`；`"aaa"` → `6`；`"abc"` → `0`'],
        quote='使 s 有效的话，我们需要在 x 和 y 之间插入 y−x−1 个字母。考虑到这可能是个负数，可以通过如下技巧转换在 [0,2] 内：(y−x−1+3) mod 3。',
        quote_src='—— 灵茶山艾府题解',
        idea=['看相邻两个字母 `x`、`y`：中间要补 `(y − x − 1) mod 3` 个',
              '例：`a → c` 补 `b`（1 个）；`a → a` 补 `bc`（2 个）；`c → a` 不用补',
              '开头不是 a 要补 `s[0] − a` 个，结尾不是 c 要补 `c − s[-1]` 个，合并为 `s[0] − s[-1] + 2`'],
        result='`"aacb"`：两端 1 + 三对相邻字母 2 + 1 + 1 = 5',
        after=[dict(heading='另一种写法：数 abc 的个数', lines=[
            '设最后由 `t` 个 `abc` 组成，插入数 = `3t − n`',
            '相邻 `x < y` 能在同一个 abc 内；`x ≥ y` 必须换一个 abc',
            '`t = 1 +` （`x ≥ y` 的次数），例如 `"aacb"`：`t = 1 + 2 = 3`，`9 − 4 = 5`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`y − x − 1` 可能为负，所以加 3 再取模，合并后写成 `+ 2`',
                 '两端的补充可以合并成 `ord(s[0]) − ord(s[-1]) + 2`',
                 '另一种写法：`t * 3 − len(s)`，`t = 1 + sum(x >= y)`'],
    ),
)
