def _txt(S):
    c = S['coordinates']
    a, b = ord(c[0]), int(c[1])
    t = a + b
    return f"`ord('{c[0]}')` + `{b}` = {a} + {b} = {t}（{'奇数' if t % 2 else '偶数'}） → ==" + ('白格' if t % 2 else '黑格') + '=='


CONFIG = dict(
    num=1812, title='判断国际象棋棋盘中一个格子的颜色', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='行列编号之和的奇偶',
    tags=[],
    code='''
class Solution(object):
    def squareIsWhite(self, coordinates):

        return (ord(coordinates[0]) + int(coordinates[1])) % 2 == 1
''',
    call='Solution().squareIsWhite("h3")',
    expect=True,
    views=[
        dict(type='string', var='coordinates', h=200, cell=120, label='coordinates'),
        dict(type='text', fn=_txt, size=30),
    ],
    watch=['coordinates'],
    captions={
        'return': "`ord(列)` + `int(行)` = {ord(coordinates[0]) + int(coordinates[1])}，对 2 取余 = {(ord(coordinates[0]) + int(coordinates[1])) % 2}，等于 1 → 白格，返回 =={ret}==",
    },
    cards=dict(
        one_liner='行号 + 列号为偶数是黑格，为奇数是白格',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`coordinates` 是棋盘格子坐标，如 `"a1"`',
                 '白格返回 `true`，黑格返回 `false`',
                 '示例：`"a1"` → `false`，`"h3"` → `true`',
                 '本视频演示 `"h3"`'],
        quote='假设棋盘的列也是从1到8编号对应a到h，那么行和列相加为偶数时对应的格子为黑色，否则为白色。',
        quote_src='—— yiduobo 题解原文',
        idea=['把列 a~h 记成 1~8，左下角 `a1`：`1 + 1 = 2` 是偶数 → 黑格',
              '相邻格子行或列差 1，和的奇偶翻转 → 颜色翻转',
              '`ord` 取 a~h 的 ASCII 码，97 是奇数，奇偶性与 1~8 恰好相同，可以直接用'],
        after=[dict(heading='再验证两个示例', lines=[
            '`"a1"`：`97 + 1 = 98` 偶数 → 不等于 1 → 黑格 → `false`',
            '`"c7"`：`99 + 7 = 106` 偶数 → 黑格 → `false`',
            '`"h3"`：`104 + 3 = 107` 奇数 → 白格 → `true`',
            '和灵神比：这里用「行列编号和」的棋盘直觉，不看字符 ASCII 的对比'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`ord(coordinates[0])` 与 1~8 的编号奇偶一致，所以不必减 `ord("a")`',
                 '行号字符要用 `int()` 转成数字再相加',
                 '原文为 Python 2 风格，本题无需改动，代码照搬原文'],
    ),
)
