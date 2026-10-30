CONFIG = dict(
    num=1078, title='Bigram 分词', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟扫描匹配相邻两词',
    code='''
class Solution(object):
    def findOcurrences(self, text, first, second):

        word_list = text.split(' ')
        res = []
        for index in range(len(word_list) - 2):
            if word_list[index] == first and word_list[index + 1] == second:
                res.append(word_list[index + 2])
        
        return res
''',
    call="Solution().findOcurrences('we will we will rock you', 'we', 'will')",
    expect=['we', 'rock'],
    views=[
        dict(type='array', var='word_list', pointers={'index': 'blue'}, window=('index', 'index'), h=230, cell=120),
        dict(type='array', var='res', h=150, label='res（答案）'),
    ],
    watch=['first', 'second', 'index', ('res', 'res', 'green')],
    captions={
        'word_list = text.split': '按空格切成单词数组：`{word_list}`',
        'res = []': '`res` 存所有跟在 `first second` 后面的单词',
        'for index in range': '`index = {index}`：只扫到倒数第 3 个，因为还要看 `index+1`、`index+2`',
        'if word_list[index] == first': lambda S, B, r: (f"`word_list[{S.index}] = {S.word_list[S.index]!r}` 与 `first = {S.first!r}` 相等吗？"
                                                         + (f" 是 → 再看下一个 `{S.word_list[S.index+1]!r}` 是否等于 `second = {S.second!r}`"
                                                            if S.word_list[S.index] == S.first else " 否 → 这个位置不可能是开头")),
        'res.append': '连续两词都对上了 → 第三个词 `{word_list[index+2]}` 加入答案：`res = {res}`',
        'return res': '扫描结束，答案 `{res}`',
    },
    cards=dict(
        one_liner='把单词当字符，找 first second 后面的第三个词',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定 `text`，以及两个单词 `first`、`second`',
                 '找出所有 `first second third` 连续出现的情况，返回每个 `third`',
                 '示例：`we will we will rock you`，`first=we`，`second=will` → `[we, rock]`'],
        quote='一趟扫描，对于当前的index，若list[index]等于first，且list[index + 1]等于second，那么就将list[index + 2]加入到答案当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先切成单词数组，这样问题就变成数组上的相邻三元组匹配',
              '下标只需扫到 `len - 3`，保证 `index + 2` 不越界',
              '作者补充：若是 n-gram，可把每个单词看成一个字母，用 KMP 做匹配'],
        summary=['时间 `O(n)`，空间 `O(n)`（切分后的数组）',
                 '循环上界是 `len(word_list) - 2`，写成 `len` 会越界',
                 '匹配可以重叠：`we will we will` 中间的 `we` 既是结尾也是下一次开头',
                 '原文文字说按逗号分割，代码实际按空格 `split(\' \')`，以代码为准'],
    ),
)
