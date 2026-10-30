CONFIG = dict(
    num=1455, title='检查单词是否为句中其他单词的前缀', difficulty='Easy', category='字符串',
    author='yiduobo', technique='枚举单词 · 逐字符比前缀', tags=[],
    code='''
class Solution(object):
    def isPrefixOfWord(self, sentence, searchWord):

        l = len(searchWord)

        for index, word in enumerate(sentence.split(' ')):
            if len(word) < l:
                continue

            flag = True
            for p in range(l):
                if word[p] != searchWord[p]:
                    flag = False
                    break
                
            if flag:
                return index + 1

        return -1
''',
    call="Solution().isPrefixOfWord('i love eating burger', 'burg')",
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"第 `{S['index']+1}` 个单词 `{S['word']}`，比较第 `{S['p']}` 位：`{S['word'][S['p']]}` 对 `{S['searchWord'][S['p']]}`" if 'p' in S and 'word' in S and S['p'] < len(S['word']) and S['p'] < len(S['searchWord']) and S.get('_line') is not None else '逐个单词检查：是不是以 searchWord 开头')),
        dict(type='string', var='word', pointers={'p': 'blue'}, label='当前单词 word', h=150),
        dict(type='string', var='searchWord', pointers={'p': 'pink'}, label='searchWord', h=150),
        dict(type='array', var=lambda S: S['sentence'].split(' '), pointers={'index': 'yellow'}, label='sentence 按空格拆开', h=150, cell=150),
    ],
    watch=[('index', 'index', 'yellow'), ('p', 'p', 'blue'), ('flag', 'flag', 'green')],
    captions={
        'l = len': '前缀长度 `l = {l}`：单词至少要有 `{l}` 个字符才可能匹配',
        'enumerate': '取出第 `{index}` 个单词 `{word}`（题目下标从 1 开始，返回时要 +1）',
        'if len(word) < l': lambda S, B, r: f"`len({S['word']}) = {len(S['word'])}`，比 `l = {S['l']}` {'短' if len(S['word']) < S['l'] else '不短'}" + ('：不可能是前缀，跳过这个词' if len(S['word']) < S['l'] else '，继续比'),
        'continue': '太短，直接看下一个单词',
        'flag = True': '先假设 `{word}` 以 `{searchWord}` 开头',
        'for p in range': lambda S, B, r: ('`searchWord` 的每一位都比完了，循环结束' if S['p'] == S['l'] - 1 and B.get('p') == S['p'] and S['flag'] and S['l'] > 1 else f"比较第 `{S['p']}` 个字符"),
        'if word[p] != searchWord[p]': lambda S, B, r: f"`{S['word'][S['p']]}` 和 `{S['searchWord'][S['p']]}` " + ('不同 → 前缀不成立' if S['word'][S['p']] != S['searchWord'][S['p']] else '相同 → 继续比下一位'),
        'flag = False': '有一位不同，标记 ==flag = False==',
        'break': '不必再比后面的字符，换下一个单词',
        'if flag': lambda S, B, r: '`flag` 仍为真：每一位都相同 → 这个单词就是答案' if S['flag'] else '`flag` 为假，不是前缀，继续下一个单词',
        'return index + 1': '返回第一个满足的下标 `{index}` + 1 = ==`{index+1}`==（下标从 1 开始）',
        'return -1': '所有单词都不是前缀，返回 -1',
    },
    cards=dict(
        one_liner='句子很短，直接逐个单词、逐个字符比前缀',
        complexity='时间 `O(n·l)`，空间 `O(n)`',
        problem=['句子 `sentence` 由单词组成，用单个空格隔开',
                 '找出 `searchWord` 是哪个单词的前缀，返回 ==最小的下标==（从 1 开始），没有返回 `-1`',
                 '示例：`"i love eating burger"`，`"burg"` → `4`'],
        quote='由于这里句子的数目以及长度都比较小，同时只需要判断是否为前缀，因此可以直接枚举每个句子，逐个判断单词是否为该句子的前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，不需要字典树，暴力枚举就够',
              '先比长度：单词比 `searchWord` 短，必然不是前缀',
              '再逐位比较，一位不同就 `break`；全部相同就返回 `index + 1`'],
        summary=['时间 `O(n·l)`，`n` 是句子长度，`l` 是 searchWord 长度；空间 `O(n)`（split 的结果）',
                 '易错点：题目下标从 1 开始，返回 `index + 1`',
                 '易错点：先判断 `len(word) < l`，否则 `word[p]` 会越界',
                 '要返回最小下标，所以从左到右找到第一个就立刻返回'],
    ),
)
