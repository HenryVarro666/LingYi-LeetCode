CONFIG = dict(
    num=720, title='词典中最长的单词', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='按长度排序 + 集合',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def longestWord(self, words):

        word_set = set()
        res = ''
        for word in sorted(words, key=lambda d:len(d)):
            if len(word) == 1 or word[:-1] in word_set:
                word_set.add(word)
                if (len(word) > len(res)) or (len(word) == len(res) and word < res):
                    res = word
        
        return res
''',
    call='Solution().longestWord(["a", "banana", "app", "appl", "ap", "apply", "apple"])',
    expect='apple',
    views=[
        dict(type='array', var='words', label='words（原始词典）', cell=130, h=240,
             color=lambda S, i, v: ('green' if v == S.get('res') else ('yellow' if v == S.get('word') else None))),
        dict(type='set', var='word_set', label='word_set（能一个字母一个字母拼出来的词）', fmt=lambda x: x, h=170, font=30),
        dict(type='text', h=90, size=32,
             fn=lambda S: ('当前词 `%s`：去掉最后一个字符 → `%s`，%s' % (
                 S['word'], S['word'][:-1],
                 '在集合里' if S['word'][:-1] in S['word_set'] else '不在集合里')) if 'word' in S else '按长度从短到长依次处理'),
    ],
    watch=[('word', 'word', 'yellow'), ('res', 'res', 'green')],
    captions={
        'word_set = set()': '`word_set` 存所有“能逐个字母加出来”的单词，先是空集合',
        "res = ''": '答案 `res` 先是空串',
        'for word in sorted': lambda S, B, ret: ('所有词都处理完了' if ('word' in B and B.word == S.word) else f'按长度从短到长取下一个词：`{S.word}`'),
        'if len(word) == 1': lambda S, B, ret: (
            f'`{S.word}`：长度为 1，或者去掉末位的 `{S.word[:-1]}` 已在集合里？→ '
            + ('==成立，它能被逐步拼出==' if (len(S.word) == 1 or S.word[:-1] in S.word_set) else '不成立，它拼不出来，跳过')),
        'word_set.add': '`{word}` 的所有前缀都在词典里了，加入 `word_set`，后面更长的词可以接着它',
        'if (len(word) > len(res))': lambda S, B, ret: (
            f'比较 `{S.word}` 和当前答案 `{S.res!r}`：更长，或一样长但字典序更小 → '
            + ('==更新答案==' if (len(S.word) > len(S.res) or (len(S.word) == len(S.res) and S.word < S.res)) else '不更新')),
        'res = word': '答案更新为 `{res}`',
        'return res': '返回最长且字典序最小的 `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='先按长度排序，一层一层拼出能用的词',
        complexity='时间 `O(n log n + L)`（L 为总长度），空间 `O(L)`',
        problem=['给一个单词列表 `words`，找出其中最长的单词',
                 '要求：它的每个前缀也都在 `words` 里；等长取字典序最小',
                 '本视频：`["a","banana","app","appl","ap","apply","apple"]` → `apple`'],
        quote='用一个set来储存所有可以通过添加字符形成的单词，然后将词典中的词按长度进行排序之后遍历词典。若某个单词的长度为1，或者其去除最后一个字符后在set中，那么就将该词加入到set中，同时更新答案。',
        quote_src='—— yiduobo 题解',
        idea=['排序后，比某个词短一位的前缀一定已经处理过了',
              '只需检查“去掉最后一个字符”是否在集合里，一路链条就不会断',
              '加入集合的同时和 `res` 比长度，一样长就取字典序小的'],
        summary=['时间：排序 `O(n log n)`，空间：集合 `O(L)`',
                 '==只检查去掉末位的那一个前缀==就够，因为更短的前缀已经被检查过',
                 '易错点：等长时要比字典序，`word < res`'],
    ),
)
