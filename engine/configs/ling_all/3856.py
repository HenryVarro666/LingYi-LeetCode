CONFIG = dict(
    num=3856, title='移除尾部元音字母', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='库函数 rstrip',
    code='''
class Solution:
    def trimTrailingVowels(self, s: str) -> str:
        return s.rstrip("aeiou")
''',
    call='Solution().trimTrailingVowels("beautifulidea")',
    expect='beautifulid',
    views=[
        dict(type='string', var='s', h=220, cell=60,
             color=lambda S, i, v: 'pink' if 's' in S and i >= len(S['s'].rstrip('aeiou')) else None),
        dict(type='text', fn=lambda S: f"`rstrip(\"aeiou\")` 从右往左删，直到遇到非元音字母", size=30),
    ],
    watch=['s'],
    captions={
        'return s.rstrip': lambda S, B, r: f'从末尾删掉所有属于 `aeiou` 的字母（红色部分）→ 返回 `"{r}"`；遇到非元音 `"{r[-1:]}"` 就停',
    },
    cards=dict(
        after=[dict(heading='朴素循环写法（原文思路）', lines=[
            '`while s and s[-1] in "aeiou":`',
            '`    s = s[:-1]`  每次去掉最后一个字母',
            '例：`beautifulidea` → 去 `a` → 去 `e` → 遇到 `d`，停',
            '`rstrip` 就是把这个循环交给库函数']),
            dict(heading='为什么答案是 beautifulid', lines=[
                '末尾依次是 `a`、`e`，都是元音，删掉',
                '再往前是 `d`，不是元音 → 立刻停止',
                '前面的 `eau`、`i` 虽然是元音，但不在尾部，保留'])],
        one_liner='循环去掉末尾元音，Python 一句 rstrip',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['去掉字符串 `s` 末尾的所有元音字母（`a e i o u`）',
                 '示例：`"idea"` → `"id"`，`"aeiou"` → `""`',
                 '本视频：`"beautifulidea"` → `"beautifulid"`'],
        quote='写个循环：如果 s 不为空且 s 的最后一个字母是元音，那么去掉 s 的最后一个字母。也可以用库函数做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['朴素写法：只要末尾是元音就删一个',
              '`s.rstrip("aeiou")` 把参数当作==字符集合==，从右边删到遇上集合外的字符为止'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计）',
                 '`rstrip` 的参数是字符集合，不是要删的子串',
                 '只删尾部，中间的元音不动'],
    ),
)
