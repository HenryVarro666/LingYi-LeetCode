CONFIG = dict(
    num=1880, title='检查某单词是否等于两单词之和', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='字符串转数字（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def isSumEqual(self, firstWord: str, secondWord: str, targetWord: str) -> bool:
        return self.str2int(firstWord) + self.str2int(secondWord) == self.str2int(targetWord)

    def str2int(self, s: str) -> int:
        x = 0
        for b in s:
            x = x * 10 + (ord(b) - ord('a'))
        return x
''',
    call='Solution().isSumEqual("acb", "cba", "cdb")',
    expect=True,
    views=[
        dict(type='string', var='s', pointers={}, cell=90, h=220,
             color=lambda S, i, v: 'blue' if S.get('b') == v and S.get('_line') else None),
        dict(type='text', size=32, h=90, fn=lambda S: f"当前数值 x = =={S['x']}==" if 'x' in S else ''),
    ],
    watch=['s', 'b', ('x', 'x', 'green')],
    captions={
        'return self.str2int(firstWord)': lambda S, B, r: f'三个单词分别转成数字，比较 `和 == 目标` → ==`{r}`==' if '_ret' in S else '先把三个单词分别转成数字再比较',
        'x = 0': '`x` 从 0 开始累积数值：`s = {s}`',
        'for b in s': '取字母 `{b}`，字母值是 `{ord(b) - ord("a")}`',
        'x = x * 10': '`x = {B.x} * 10 + {ord(b) - ord("a")}` → =={x}==（先左移一位十进制，再接上字母值）',
        'return x': '`{s}` 转成整数 `{x}`',
    },
    cards=dict(
        one_liner='字母值当作十进制数位，逐位拼出整数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母 `a~j` 对应 `0~9`，把单词的字母值连起来就是它的数值',
                 '判断 `firstWord + secondWord` 的数值是否等于 `targetWord` 的数值',
                 '示例：`"acb" + "cba" == "cdb"`，即 `21 + 210 == 231` → `true`'],
        quote='func str2int(s string) (x int) { for _, b := range s { x = x*10 + int(b-\'a\') } return }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['写一个 `str2int`：每读一个字母，`x` 先乘 10，再加字母值 `b - a`',
              '主函数只要比较 `str2int(first) + str2int(second) == str2int(target)`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`int(b-\'a\')` 写成 `ord(b) - ord(\'a\')`，`str2int` 作为同类的方法调用',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：前导 `a` 就是 0，如 `"aab"` 等于 1',
                 '长度最多 8，不会溢出'],
    ),
)
