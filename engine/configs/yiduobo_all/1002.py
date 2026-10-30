CONFIG = dict(
    num=1002, title='查找常用字符', difficulty='Easy', category='哈希表',
    author='yiduobo', technique='字符计数取最小',
    tags=[],
    code='''
class Solution(object):
    def commonChars(self, A):

        char_dict = {}

        for char in A[0]:
            char_dict[char] = char_dict.get(char, 0) + 1

        for word in A[1:]:
            tmp_dict = {}
            for char in word:
                tmp_dict[char] = tmp_dict.get(char, 0) + 1

            for asc in range(97, 123):
                char = chr(asc)
                char_dict[char] = min(char_dict.get(char, 0), tmp_dict.get(char, 0))

        res = []
        for char in char_dict:
            res.extend([char] * char_dict[char])
        
        return res
''',
    call="Solution().commonChars(['cool', 'lock'])",
    expect=['c', 'o', 'l'],
    views=[
        dict(type='array', var='A', h=130, label='A'),
        dict(type='map', var='char_dict', h=300, label='char_dict（当前累计的最小次数）'),
        dict(type='map', var='tmp_dict', h=200, label='tmp_dict（当前单词的次数）'),
        dict(type='array', var='res', h=110, label='res'),
    ],
    watch=['word', 'char', 'asc', ('res', 'res', 'green')],
    skip=['tmp_dict = {}', 'res = []', 'for asc in range', 'char = chr(asc)'],
    max_steps=60,
    captions={
        'char_dict[char] = char_dict.get(char, 0) + 1': '第一个单词里 `{char}` 的次数 → `char_dict[{char!r}] = {char_dict[char]}`',
        'tmp_dict[char] = tmp_dict.get': '数当前单词 `{word}`：`{char}` 出现 `{tmp_dict[char]}` 次',
        'char_dict[char] = min': '字母 `{char}`：之前最小 `{B.char_dict.get(char, 0)}`，这个单词有 `{tmp_dict.get(char, 0)}` → 取小 ==`{char_dict[char]}`==',
        'for char in char_dict': '`{char}` 在所有单词中至少出现 `{char_dict[char]}` 次',
        'res.extend': '`{char}` 重复 `{char_dict[char]}` 次加入答案：`res = {res}`',
        'return res': '所有单词都有的字符：`{res}`',
    },
    cards=dict(
        one_liner='每个字母的答案次数 = 各单词中该字母次数的最小值',
        complexity='时间 `O(26·n·L)`，空间 `O(26)`',
        problem=['给一组小写单词 `A`，返回所有单词里都出现的字符（含重复次数）',
                 '例如某字符在每个单词都出现 2 次，答案里就要有 2 个',
                 '示例：`["cool","lock"]` → `["c","o","l"]`（顺序不限）'],
        quote='统计每个字符串中各个字符出现的次数，然后对于每个字符而言，这些字符串统计的出现次数中的最小值即为答案中对应字符出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先数第一个单词，当作初始上限',
              '每来一个单词，数出它的次数，再对 26 个字母逐个取 `min`',
              '最后按次数把字母重复写进答案'],
        summary=['时间 `O(26·n·L)`，空间 `O(26)`',
                 '易错点：单词里没出现的字母次数要当 0，所以用 `get(char, 0)`',
                 '不能只遍历当前单词的字母，否则 `char_dict` 里多余的字母压不下来，所以遍历 97..122',
                 '原文变量名 `A` 保持不变，代码未改动'],
    ),
)
