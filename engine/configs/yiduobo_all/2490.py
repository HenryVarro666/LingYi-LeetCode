CONFIG = dict(
    num=2490, title='回环句', difficulty='Easy', category='字符串',
    author='yiduobo', technique='先看首尾 · split 后比相邻单词',
    tags=[],
    code='''
class Solution(object):
    def isCircularSentence(self, sentence):

        if sentence[0] != sentence[-1]:
            return False
        
        words = sentence.split(' ')
        for index in range(1, len(words)):
            if words[index][0] != words[index - 1][-1]:
                return False
        
        return True
''',
    call='Solution().isCircularSentence("ab bc ca")',
    expect=True,
    views=[
        dict(type='string', var='sentence', label='sentence', cell=84, h=150,
             color=lambda S, k, v: 'blue' if k in (0, len(S['sentence']) - 1) else None),
        dict(type='array', var='words', label='words（蓝 = 当前单词，粉 = 前一个单词）', cell=150, h=200,
             pointers={'index': 'blue'},
             color=lambda S, k, v: ('blue' if 'index' in S and k == S['index'] else
                                    'pink' if 'index' in S and k == S['index'] - 1 else None)),
    ],
    watch=[('index', 'index', 'blue')],
    captions={
        'if sentence[0] != sentence[-1]': "首字符 `'{sentence[0]}'`，尾字符 `'{sentence[-1]}'`：相同才可能首尾相接",
        'words = sentence.split': '按空格拆成单词：`{words}`',
        'for index in range': '看第 `{index}` 个单词，与前一个单词比较',
        'if words[index][0] != words[index - 1][-1]': lambda S, B, ret: (
            f"前一个单词 `{S.words[S.index-1]}` 的尾 `'{S.words[S.index-1][-1]}'` "
            f"{'==' if S.words[S.index][0] == S.words[S.index-1][-1] else '≠'} "
            f"当前单词 `{S.words[S.index]}` 的首 `'{S.words[S.index][0]}'`"
            + (' → 接得上，继续' if S.words[S.index][0] == S.words[S.index-1][-1] else ' → 接不上')),
        'return True': '首尾相同，且所有相邻单词都接得上 → `True`',
        'return False': '有一处接不上 → `False`',
    },
    cards=dict(
        one_liner='先判首尾，再把句子拆成单词逐对比较',
        complexity='时间 `O(n)`，空间 `O(n)`（拆分出的单词）',
        problem=['单词用单个空格分隔；每个单词的末字符要等于下一个单词的首字符',
                 '最后一个单词的末字符要等于第一个单词的首字符',
                 '本视频：`"ab bc ca"` → `true`'],
        quote='首先判断句子的首尾是否相同，接下来按空格将句子分离成单词，判断相邻单词间前一个单词的最后一个字符是否与后一个单词的第一个字符相同即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['句子首字符 = 第一个单词的首字符，句子尾字符 = 最后一个单词的末字符',
              '所以首尾检查只需比较 `sentence[0]` 与 `sentence[-1]`',
              '剩下的相邻单词对，用 `split(\' \')` 后从 1 开始比较'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`index` 从 1 开始，才能和 `index - 1` 比较',
                 '只有一个单词时循环不执行，只靠首尾检查',
                 '原文本身就是 Python 3 可运行的写法，未做修改'],
    ),
)
