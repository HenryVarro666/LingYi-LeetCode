CONFIG = dict(
    num=748, title='最短补全词', difficulty='Easy', category='字符串',
    author='yiduobo', technique='字符计数哈希表',
    code='''
class Solution(object):
    def shortestCompletingWord(self, licensePlate, words):

        target_dict = {}
        for char in licensePlate:
            if char >= 'a' and char <= 'z':
                target_dict[char] = target_dict.get(char, 0) + 1
            elif char >= 'A' and char <= 'Z':
                char = chr(ord(char) + 32)
                target_dict[char] = target_dict.get(char, 0) + 1
        
        res = None
        for word in words:
            if res is not None and len(word) >= len(res):
                continue

            word_dict = {}
            for char in word:
                word_dict[char] = word_dict.get(char, 0) + 1
            
            flag = True
            for char in target_dict:
                if word_dict.get(char, 0) < target_dict[char]:
                    flag = False
                    break
            
            if flag:
                res = word

        return res
''',
    call='Solution().shortestCompletingWord("1s3 Ps", ["pest", "steps", "stripe"])',
    expect='steps',
    max_steps=130,
    views=[
        dict(type='string', var='licensePlate', label='licensePlate（只统计字母，忽略大小写）', cell=64, h=150,
             color=lambda S, i, v: 'blue' if S.get('char') == v and S['_line'] <= 10 else None),
        dict(type='map', var='target_dict', label='target_dict（牌照需要的字母次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=28),
        dict(type='array', var='words', label='words（蓝 = 当前单词，绿 = 当前答案 res）', cell=130, h=170,
             color=lambda S, i, v: 'blue' if S.get('word') == v and S['_line'] > 12 else 'green' if S.get('res') == v else None),
        dict(type='map', var='word_dict', label='word_dict（当前单词的字母次数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=28),
    ],
    watch=['char', 'word', 'flag', ('res', 'res', 'green')],
    captions={
        'target_dict = {}': '`target_dict`：牌照里每个字母需要出现的次数',
        'for char in licensePlate': '看牌照字符 `{char!r}`',
        "if char >= 'a'": '`{char!r}` 是小写字母？{"是，直接计数" if "a" <= char <= "z" else "不是"}',
        "elif char >= 'A'": '`{char!r}` 是大写字母？{"是，转成小写再计数" if "A" <= char <= "Z" else "不是（数字或空格），忽略"}',
        'char = chr(ord(char) + 32)': '大写加 32 就是对应小写：`char = {char!r}`',
        'target_dict[char] =': '`target_dict[{char!r}]` = {target_dict[char]}',
        'res = None': '`res` 保存当前最短的补全词，一开始还没有',
        'for word in words': '检查单词 `{word}`',
        'if res is not None and len': '小优化：已有答案 `{res}`，当前 `{word}` 长度 {len(word)}，{"不比答案短，跳过" if res is not None and len(word) >= len(res) else "有机会更短，继续检查"}',
        'continue': '长度不占优，直接看下一个单词',
        'word_dict = {}': '给 `{word}` 建一个新的次数表',
        'for char in word': '统计单词字母 `{char!r}`',
        'word_dict[char] =': '`word_dict[{char!r}]` = {word_dict[char]}',
        'flag = True': '先假设 `{word}` 满足条件',
        'for char in target_dict': '逐个检查牌照需要的字母 `{char!r}`',
        'if word_dict.get(char, 0) <': '`{char!r}`：单词里有 `{word_dict.get(char, 0)}` 个，需要 `{target_dict[char]}` 个 → {"不够" if word_dict.get(char, 0) < target_dict[char] else "够了"}',
        'flag = False': '有字母不够，`{word}` 不是补全词',
        'break': '已经不满足，不必再看其余字母',
        'if flag': '`{word}` {"是补全词" if flag else "不是补全词"}',
        'res = word': '`{word}` 满足且比原答案短 → `res = {res}`',
        'return res': '最短补全词是 `{res}`',
    },
    cards=dict(
        one_liner='统计牌照字母次数，逐个单词比对，保留最短的',
        complexity='时间 `O(L + 总字符数)`，空间 `O(1)`（字母表大小）',
        problem=['给牌照 `licensePlate` 和单词列表 `words`',
                 '补全词：包含牌照里所有字母（忽略大小写和数字空格），次数不能少',
                 '返回最短的补全词，同样长取最靠前的',
                 '示例：`"1s3 Ps"`，`["pest","steps","stripe"]` → `"steps"`'],
        quote='统计牌照中每个字符出现的次数，然后遍历每个单词，统计单词中每个字符出现的次数。若满足条件，且当前单词的长度比答案的长度要短，那么就更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把牌照里的字母统一成小写并计数',
              '对每个单词也计数，检查牌照需要的字母次数是否都够',
              '小优化：长度不比当前答案短的单词，先跳过再统计'],
        summary=['时间 `O(总字符数)`，空间 `O(1)`',
                 '易错点：牌照大写字母要转小写；数字和空格忽略',
                 '提前跳过 `len(word) >= len(res)`，同长度保留靠前的那个',
                 '原文为 Python 2 风格，在 Python 3 下无需修改即可运行'],
    ),
)
