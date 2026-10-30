CONFIG = dict(
    num=1859, title='将句子排序', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按末位数字对号入座', tags=[],
    code='''
class Solution(object):
    def sortSentence(self, s):

        words = s.split(' ')
        res = [''] * len(words)
        for word in words:
            res[int(word[-1]) - 1] = word[:-1]
        
        return ' '.join(res)
''',
    call="Solution().sortSentence('is2 sentence4 This1 a3')",
    expect='This is a sentence',
    views=[
        dict(type='array', var='words', label='words（打乱的单词，蓝 = 当前处理）', h=240, cell=170,
             color=lambda S, i, v: 'blue' if S.get('word') == v and S['_line'] >= 7 else None),
        dict(type='array', var='res', label='res（按位置放好的单词）', h=240, cell=170,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=['word', ('word[-1]', "word[-1] if 'word' in S else ''", 'blue')],
    captions={
        'words = s.split': '按空格拆开：`{words}`，一共 {len(words)} 个单词',
        'res = [': '准备 `{len(words)}` 个空位，等着把单词放进去',
        'for word in words': lambda S, B, r: (f'取出单词 `{S.word}`' if S.word != B.get('word') else '单词都处理完了，循环结束'),
        'res[int': '末位数字 `{word[-1]}` → 放到下标 `{int(word[-1]) - 1}`，去掉数字存 `{word[:-1]}`',
        "' '.join": '`res` 已按顺序排好，用空格连起来：=={ret}==',
    },
    cards=dict(
        one_liner='单词末位的数字就是它的位置，直接对号入座',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['句子被打乱，每个单词末尾带着从 1 开始的位置数字',
                 '还原出原来的句子（去掉数字）',
                 '示例：`"is2 sentence4 This1 a3"` → `"This is a sentence"`'],
        quote='由于最多只有9个单词，因此每个单词仅有最后一位表示其在句子中的下标。根据这一位将单词对号入座放置到答案数组中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 `split(\' \')` 拆出单词',
              '最多 9 个单词，所以位置只占 ==最后一位==',
              '`res[位置-1] = word[:-1]`，最后用空格 `join`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '位置从 1 开始，下标要 `-1`',
                 '去掉数字用 `word[:-1]`；数字用 `word[-1]`（最多 9 个词，所以一位就够）',
                 '原文为 Python 2 风格，但在 Python 3 下同样可运行，代码未改动'],
    ),
)
