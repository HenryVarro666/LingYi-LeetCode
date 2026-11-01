CONFIG = dict(
    num=2068, title='检查两个字符串是否几乎相等', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表记录次数之差', tags=[],
    code='''
class Solution(object):
    def checkAlmostEquivalent(self, word1, word2):

        char_diff = {}
        for char in word1:
            char_diff[char] = char_diff.get(char, 0) + 1
        
        for char in word2:
            char_diff[char] = char_diff.get(char, 0) - 1

        for diff in char_diff.values():
            if abs(diff) > 3:
                return False

        return True
''',
    call="Solution().checkAlmostEquivalent('abcdeef', 'abaaacc')",
    expect=True,
    skip=['for char in word1', 'for char in word2', 'for diff in'],
    views=[
        dict(type='string', var='word1', label='word1（遍历时 +1）', cell=80, h=130,
             pointers={}),
        dict(type='string', var='word2', label='word2（遍历时 −1）', cell=80, h=130),
        dict(type='map', var='char_diff', label='char_diff（出现次数之差，word1 − word2）',
             fmt=lambda k, v: f"'{k}': {v}", h=260, font=30),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"`abs({S['diff']}) = {abs(S['diff'])}`，上限是 3" if 'diff' in S else ''),
    ],
    watch=[('char', 'char'), ('diff', 'diff', 'orange')],
    captions={
        'char_diff = {}': '用哈希表 `char_diff` 记每个字符在 word1 与 word2 中次数之差',
        'char_diff[char] = char_diff.get(char, 0) + 1': 'word1 里的 `{char}`：次数 +1 → `char_diff[{char!r}] = {char_diff[char]}`',
        'char_diff[char] = char_diff.get(char, 0) - 1': 'word2 里的 `{char}`：次数 −1 → `char_diff[{char!r}] = {char_diff[char]}`',
        'for diff in': '看下一种字符的差值 `diff = {diff}`',
        'if abs(diff) > 3': '`abs({diff}) = {abs(diff)}` 是否大于 3 → {"==大于，答案是 False==" if abs(diff) > 3 else "没超过，继续"}',
        'return False': '有字符差值大于 3，返回 ==False==',
        'return True': '所有字符的差值都不超过 3，返回 ==True==',
    },
    cards=dict(
        one_liner='哈希表记下每个字符次数之差，有一个超过 3 就不行',
        complexity='时间 `O(n)`，空间 `O(26)`',
        problem=['两字符串中每个字母出现次数之差都 ==不超过 3== 才算几乎相等',
                 '示例：`"aaaa"`、`"bccb"` → `false`',
                 '本视频：`"abcdeef"`、`"abaaacc"` → `true`'],
        quote='使用哈希表记录每个字符在word1中出现次数与word2中出现次数之差，接下来遍历每种字符出现次数之差，如果有差值大于3次的字符，那么答案就是false。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历 word1：每个字符的计数 `+1`；遍历 word2：每个字符的计数 `-1`',
              '这样哈希表里存的就是 ==word1 − word2== 的次数差',
              '最后遍历所有差值，绝对值大于 3 就返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(26)`',
                 '易错点：差值可能为负，要取 `abs`',
                 '只在某个字符串里出现的字符也会进表，用 `get(char, 0)` 处理',
                 '代码为 Python 3 可直接运行，原文未改动'],
    ),
)
