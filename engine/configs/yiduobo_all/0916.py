CONFIG = dict(
    num=916, title='单词子集', difficulty='Medium', category='字符串',
    author='yiduobo', technique='B 中字母最大频次 + 逐个检查 A',
    code='''
class Solution(object):
    def wordSubsets(self, A, B):

        char_dict = {}
        for word in B:
            tmp_dict = {}
            for char in word:
                tmp_dict[char] = tmp_dict.get(char, 0) + 1
            for char in tmp_dict:
                char_dict[char] = max(char_dict.get(char, 0), tmp_dict[char])
        
        res = []
        for word in A:
            tmp_dict = {}
            for char in word:
                tmp_dict[char] = tmp_dict.get(char, 0) + 1
            flag = True
            for char in char_dict:
                if tmp_dict.get(char, 0) < char_dict[char]:
                    flag = False
                    break
            
            if flag:
                res.append(word)
        
        return res
''',
    call='Solution().wordSubsets(["cab","boo","book"], ["b","oo"])',
    expect=['boo', 'book'],
    max_steps=100,
    views=[
        dict(type='array', var='B', h=150, index=False, label='B', color=lambda S, i, v: 'blue' if S.get('word') == v and S.get('_line', 0) < 14 else None),
        dict(type='map', var='char_dict', h=190, label='char_dict：B 中每个字母需要的最大次数', font=26),
        dict(type='array', var='A', h=150, index=False, label='A', color=lambda S, i, v: 'green' if v in S.get('res', []) else ('yellow' if S.get('word') == v and S.get('_line', 0) >= 14 else None)),
        dict(type='map', var='tmp_dict', h=190, label='tmp_dict：当前单词的字母次数', font=26),
        dict(type='array', var='res', h=120, label='res'),
    ],
    watch=['word', 'char', ('flag', 'flag', 'orange')],
    captions={
        'char_dict = {}': '`char_dict`：记录每个字母在 B 的==任意一个单词==里出现的最大次数',
        'for word in B': lambda S, B, r: ('`B` 遍历完' if B.get('word') == S['word'] else f'处理 B 的单词 `{S.word}`'),
        'for char in word': '看单词里的字母 `char = {char!r}`',
        'for char in tmp_dict': '看 `{word}` 里的字母 `char = {char!r}`',
        'for char in char_dict': '看需求表里的字母 `char = {char!r}`',
        'tmp_dict[char] = tmp_dict.get': '数字母：`tmp_dict[{char!r}]` = {tmp_dict[char]}',
        'char_dict[char] = max': '`char_dict[{char!r}] = max({B.char_dict.get(char, 0)}, {tmp_dict[char]})` = =={char_dict[char]}==（取各单词的最大需求）',
        'res = []': 'B 的需求统计完毕。逐个检查 A 里的单词',
        'for word in A': lambda S, B, r: ('`A` 遍历完' if B.get('word') == S['word'] and B.get('res') is not None and S['word']==B['word'] else f'检查 A 的单词 `{S.word}`'),
        'flag = True': '先假设 `{word}` 满足所有字母需求',
        'if tmp_dict.get': '`{char!r}`：`{word}` 里有 `{tmp_dict.get(char, 0)}` 个，需要 `{char_dict[char]}` 个 → {"==不够==" if tmp_dict.get(char, 0) < char_dict[char] else "够了"}',
        'flag = False': '有字母不够 → `{word}` 不是通用单词',
        'break': '已经不满足，不用再查其他字母',
        'if flag': lambda S, B, r: (f'`{S.word}` 满足所有需求 → 加入答案' if S.flag else f'`{S.word}` 被淘汰'),
        'res.append': '`{word}` 是通用单词，`res = {res}`',
        'return res': '返回通用单词 `{ret}`',
    },
    cards=dict(
        one_liner='把 B 合并成「每个字母至少要几个」，再逐个检查 A',
        complexity='时间 `O(总字符数)`，空间 `O(字母表)`',
        problem=['`b` 是 `a` 的子集：`b` 里每个字母出现的次数都不超过 `a` 里的次数',
                 '若 `B` 中每个单词都是 `a` 的子集，`a` 就是通用单词，求 `A` 中所有通用单词',
                 '本视频：`A = [cab, boo, book]`，`B = [b, oo]` → `[boo, book]`'],
        quote='每个字符在B中各个单词出现次数中的最大值依然是小于等于a中对应字母的出现次数的，因此可以先统计每个字母在B中各个单词中出现次数的最大值，然后再逐个遍历A中的单词进行判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['`B` 里所有单词都要是子集 → 每个字母取各单词中出现次数的==最大值==',
              '这样 `B` 被合并成一份「字母需求表」`char_dict`',
              '对 `A` 的每个单词统计字母次数，每个需求字母都不少于要求才保留'],
        summary=['时间 `O(|A|·L + |B|·L)`，空间 `O(26)`',
                 '易错点：要的是各单词中的==最大值==，不是总和（`b`、`oo` 需要 `b:1, o:2`）',
                 '不在 `tmp_dict` 里的字母要用 `get(char, 0)`，否则 KeyError',
                 '`break` 是剪枝：一个字母不够就不用再看别的字母'],
    ),
)
