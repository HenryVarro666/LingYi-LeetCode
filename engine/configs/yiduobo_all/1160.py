CONFIG = dict(
    num=1160, title='拼写单词', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表 · 字母计数',
    tags=[],
    code='''
class Solution(object):
    def countCharacters(self, words, chars):

        char_dict = {}
        for char in chars:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        res = 0
        for word in words:
            tmp_dict = {}
            for char in word:
                tmp_dict[char] = tmp_dict.get(char, 0) + 1
            flag = True
            for char in tmp_dict:
                if tmp_dict[char] > char_dict.get(char, 0):
                    flag = False
                    break
            
            if flag:
                res += len(word)
        
        return res
''',
    call='Solution().countCharacters(["cat", "bt", "hat"], "atach")',
    expect=6,
    views=[
        dict(type='array', var='words', label='words', cell=130, h=200,
             pointers={'cur': 'blue'} if False else {},
             color=lambda S, i, v: 'blue' if S.get('word') == v else None),
        dict(type='string', var='chars', label='chars（可用字母，每个只能用一次）', cell=80, h=150),
        dict(type='map', var='char_dict', label='char_dict（chars 里每个字母的个数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=30),
        dict(type='map', var='tmp_dict', label='tmp_dict（当前单词的字母个数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=30),
    ],
    watch=['word', 'flag', ('res', 'res', 'green')],
    captions={
        'char_dict[char] =': '`char_dict[{char!r}]` = {char_dict[char]}：chars 中字母 `{char}` 累计 {char_dict[char]} 个',
        'tmp_dict[char] =': '`tmp_dict[{char!r}]` = {tmp_dict[char]}：单词 `{word}` 中字母 `{char}` 累计 {tmp_dict[char]} 个',
        'for word in words': '看下一个单词 `{word}`：能不能用 chars 里的字母拼出来',
        'if tmp_dict[char] >': lambda S, B, r: (
            f"单词要 `{S.char}` ×{S.tmp_dict[S.char]}，chars 只有 ×{S.char_dict.get(S.char, 0)}"
            + ('：==不够用== → 拼不出' if S.tmp_dict[S.char] > S.char_dict.get(S.char, 0) else '：够用 → 检查下一个字母')),
        'flag = False': '有字母不够 → `flag = False`，这个单词作废，直接 `break`',
        'res += len(word)': '所有字母都够用 → 掌握了 `{word}`，`res` += {len(word)} → =={res}==',
        'return res': '所有单词检查完，答案 ==`{res}`==',
    },
    cards=dict(
        one_liner='单词每个字母的个数，都不超过 chars 里的个数',
        complexity='时间 `O(L)`（所有字符总数），空间 `O(1)`',
        problem=['给一个单词列表 `words` 和一个字母表 `chars`',
                 '`chars` 里每个字母只能用一次，能拼出的单词就算「掌握」',
                 '返回所有掌握的单词长度之和',
                 '示例：`["cat","bt","hat"]`，`"atach"` → `6`（`cat` 和 `hat`）'],
        quote='分别统计出每个单词以及chars中每个字母出现的次数，然后一趟遍历，若当前的单词中所有字母出现的次数都小于等于chars中对应字母出现的次数，那么说明掌握了当前的单词',
        quote_src='—— yiduobo 题解原文',
        idea=['先给 `chars` 建一张字母计数表 `char_dict`',
              '每个单词再建自己的计数表 `tmp_dict`',
              '逐个字母比较：单词需要的 `>` chars 拥有的，就拼不出'],
        summary=['时间 `O(L)`，字母表只有 26 个，空间 `O(1)`',
                 '`char_dict.get(char, 0)`：单词里出现了 chars 没有的字母，当作 0 个',
                 '每个单词都要重新建 `tmp_dict`，不能和 `char_dict` 共用，否则会互相污染',
                 '原文为 Python 2 风格的类写法，代码本身在 Python 3 可直接运行，未改动'],
    ),
)
