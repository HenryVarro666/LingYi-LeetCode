CONFIG = dict(
    num=1859, title='将句子排序', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按编号对号入座',
    tags=[],
    code='''
class Solution(object):
    def sortSentence(self, s):

        words = s.split(' ')
        res = [''] * len(words)
        for word in words:
            res[int(word[-1]) - 1] = word[:-1]
        
        return ' '.join(res)
''',
    call='Solution().sortSentence("is2 sentence4 This1 a3")',
    expect='This is a sentence',
    views=[
        dict(type='array', var='words', pointers={'word': 'blue'}, cell=170, h=210, label='words（打乱的单词）',
             color=lambda S, i, v: 'blue' if S.get('word') == v else None),
        dict(type='array', var='res', cell=170, h=210, label='res（按编号放好）',
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=['word', 'res'],
    captions={
        "words = s.split": '按空格拆开：`words = {words}`',
        "res = ['']": '最多 9 个词，先开 `{len(words)}` 个空位：`res = {res}`',
        'for word in words': '取出单词 `{word}`',
        'res[int(word[-1]) - 1]': '末位 `{word[-1]}` 是编号，放到下标 `{int(word[-1]) - 1}`，去掉编号存 `{word[:-1]}`',
        'return': '空位全部填满，用空格连起来：`{ret}`',
    },
    cards=dict(
        one_liner='末位数字就是下标，单词对号入座',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['打乱的句子里每个单词末尾带着 1~9 的原始位置编号',
                 '还原出原来的句子（不带编号）',
                 '示例：`"is2 sentence4 This1 a3"` → `"This is a sentence"`'],
        quote='由于最多只有9个单词，因此每个单词仅有最后一位表示其在句子中的下标。根据这一位将单词对号入座放置到答案数组中',
        quote_src='—— yiduobo 题解原文',
        idea=['不排序：直接准备等长的答案数组 `res`',
              '每个单词按末位编号减 1 放到对应格子，顺手去掉编号'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '编号从 1 开始，下标要 `-1`',
                 '最后用空格 `join`，不会多出前后空格',
                 '对比灵神：灵神排序，yiduobo 直接按编号放置，省去比较'],
    ),
)
