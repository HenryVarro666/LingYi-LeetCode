def _ord_txt(S):
    s = S['s']
    a, b = ord(s[0]), ord(s[1])
    return (f"`ord('{s[0]}')` = {a}（{'奇' if a % 2 else '偶'}），`ord('{s[1]}')` = {b}（{'奇' if b % 2 else '偶'}）"
            f" → 奇偶性{'不同' if a % 2 != b % 2 else '相同'} → ==" + ('白格' if a % 2 != b % 2 else '黑格') + '==')


CONFIG = dict(
    num=1812, title='判断国际象棋棋盘中一个格子的颜色', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='ASCII 奇偶性',
    tags=[],
    code='''
class Solution:
    def squareIsWhite(self, s: str) -> bool:
        return ord(s[0]) % 2 != ord(s[1]) % 2
''',
    call='Solution().squareIsWhite("h3")',
    expect=True,
    views=[
        dict(type='string', var='s', h=200, cell=120, label='坐标 s'),
        dict(type='text', fn=_ord_txt, size=30),
    ],
    watch=['s'],
    captions={
        'return': "两个字符 ASCII 值的奇偶性==不同== → 白格；相同 → 黑格。这里 `{ord(s[0]) % 2} != {ord(s[1]) % 2}` → 返回 =={ret}==",
    },
    cards=dict(
        one_liner='看图找规律：字母和数字的 ASCII 奇偶不同就是白格',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给出棋盘格子坐标字符串，如 `"a1"`、`"h3"`',
                 '格子是白色返回 `true`，黑色返回 `false`',
                 '示例：`"a1"` → `false`，`"h3"` → `true`，`"c7"` → `false`',
                 '本视频演示 `"h3"`'],
        quote='根据题目中的图片，如果 s[0] 和 s[1] 的 ASCII 值的奇偶性不同，那么格子是白格，否则是黑格。',
        quote_src='—— 灵茶山艾府题解',
        idea=['看图：左下角 `a1` 是黑格，`a` 和 `1` 的 ASCII 值都是奇数 → ==奇偶相同是黑格==',
              '往右或往上走一格，颜色翻转，奇偶性也翻转，所以规律对整个棋盘成立',
              '不用转成数字下标，直接对 `ord` 取模比较即可'],
        after=[dict(heading='再验证两个示例', lines=[
            '`"a1"`：97 和 49 都是奇数 → 奇偶相同 → 黑格 → `false`',
            '`"c7"`：99 和 55 都是奇数 → 奇偶相同 → 黑格 → `false`',
            '`"h3"`：104 偶、51 奇 → 奇偶不同 → 白格 → `true`',
            '一行代码，不需要建棋盘、不需要循环'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`"1"` 的 ASCII 是 49（奇），`"a"` 是 97（奇）：起点同奇偶，所以左下角 `a1` 是黑格，和图一致',
                 '易错点：是奇偶==不同==为白格，别写反',
                 '相似题：3274. 检查棋盘方格颜色是否相同'],
    ),
)
