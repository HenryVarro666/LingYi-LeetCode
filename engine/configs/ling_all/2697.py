CONFIG = dict(
    num=2697, title='字典序最小回文串', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 贪心',
    tags=['贪心与思维', '难度分 1304'],
    code='''
class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        s = list(s)
        for i in range(len(s) // 2):
            x, y = s[i], s[-1 - i]
            if x > y: s[i] = y
            else: s[-1 - i] = x
        return ''.join(s)
''',
    call="Solution().makeSmallestPalindrome('cabzxb')",
    expect='babbab',
    views=[
        dict(type='text', fn=lambda S: (f"第 {S['i']} 对：`{S['x']}` 与 `{S['y']}`" + ('，相等' if S['x'] == S['y'] else '，不等，改大的')) if 'y' in S else '', size=30),
        dict(type='string', var='s', h=300,
             pointers={'i': 'blue'},
             color=lambda S, i, v: ('blue' if i == S['i'] else 'pink' if i == len(S['s']) - 1 - S['i'] else None) if 'i' in S and isinstance(S['s'], list) else None),
    ],
    watch=['i', 'x', 'y'],
    captions={
        's = list(s)': '字符串不可变，先转成列表，才能原地改',
        'for i in range': lambda S, B, r: (f'枚举左半边的下标 `i` = {S.i}，它的对称位置是 `-1 - i`' if B.get('i') != S.i else '左半边都枚举完，循环结束'),
        'x, y =': '取一对中心对称的字母：`x = s[{i}]` = {x}，`y = s[-1 - {i}]` = {y}',
        'if x > y': lambda S, B, r: (f"`{S.x} > {S.y}` → 把 x 改成 y，字典序更小" if S.x > S.y else f"`{S.x} <= {S.y}` → 把 y 改成 x（相等时等于没改）"),
        'else: s[-1 - i] = x': '走 else：`s[-1 - {i}]` 改成 `{x}`，结果 `{s}`',
        'return': "返回 `{''.join(s)}`",
    },
    cards=dict(
        one_liner='一对不同的字母只改一次，改大的变小的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给小写字符串 `s`，每步可替换一个字符，用最少次数变成回文串',
                 '最少次数方案不止一种时，取字典序最小的',
                 '示例：`"egcfe"` → `"efcfe"`；本视频：`"cabzxb"` → `"babbab"`'],
        quote='如果 x>y，那么把 x 修改成 y 更好，这样字典序更小。如果 x<y，那么把 y 修改成 x 更好，这样字典序更小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['中心对称的两个字母 `x != y` 时，改其中一个就能相同，所以每对最多 1 次',
              '该改哪一个？改大的，字典序最小',
              '把 `x = y` 合并进 `x < y` 的分支，少写一个 `elif`'],
        summary=['时间 `O(n)`，空间 `O(n)`（Python 字符串不可变，要转列表）',
                 '只枚举前一半：`range(len(s) // 2)`，中间字符不用管',
                 '对称下标是 `-1 - i`，不要写成 `-i`',
                 '灵神用 for 加下标，yiduobo 用 left/right 双指针，本质一样'],
    ),
)
