CONFIG = dict(
    num=1451, title='重新排列句子中的单词', difficulty='Medium', category='字符串',
    author='yiduobo', technique='以（长度，原位置）为关键字排序',
    code='''
class Solution(object):
    def arrangeWords(self, text):
        words = text.split(' ')
        words[0] = chr(ord(words[0][0]) + 32) + words[0][1:]

        sorted_index = sorted(range(len(words)), key=lambda d:(len(words[d]), d))
        res = ' '.join([words[index] for index in sorted_index])
        return chr(ord(res[0]) - 32) + res[1:]
''',
    call='Solution().arrangeWords("To be or not to be")',
    expect='To be or to be not',
    views=[
        dict(type='array', var='words', label='words（原始顺序）', cell=130, h=190),
        dict(type='array', var='sorted_index', label='sorted_index（按 (长度, 原位置) 排好的下标）', cell=90, h=190),
        dict(type='text', h=80, size=30, fn=lambda S: f"`res` = {S['res']!r}" if 'res' in S else ''),
    ],
    watch=[('words', 'words'), ('sorted_index', 'sorted_index')],
    captions={
        'text.split': '按空格切成单词：`{words}`',
        'words[0] = chr': '首词首字母 `ord` 加 32 变小写 → `{words[0]!r}`',
        'sorted_index = sorted': '给每个下标 `d` 的关键字是 `(len, d)`：先比长度，==长度相同再比原位置== → `{sorted_index}`',
        'res = ': '按这个下标顺序取单词，用空格拼起来：`{res!r}`',
        'return': '最后把首字母 `ord` 减 32 变回大写 → `{ret!r}`',
    },
    cards=dict(
        one_liner='用（长度，原位置）做关键字，稳定性自己保证',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['句子首字母大写，单词间单个空格；按单词长度升序重排',
                 '长度相同保持原相对顺序，结果同样首字母大写',
                 '本视频：`"To be or not to be"` → `"To be or to be not"`'],
        quote='接下来将各个单词以长度为第一关键字，原始位置为第二关键字进行排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把第 0 个单词的首字母从大写改小写，免得排序后大写留在中间',
              '排序对象不是单词而是下标：关键字 `(len(words[d]), d)`，等长时下标小的在前',
              '拼接完成后把整句首字母改回大写'],
        summary=['原文为 Python 2 写法，仅删去了类型说明文档字符串，其余无需改动',
                 '时间 `O(n log n)`，空间 `O(n)`',
                 '易错：忘记先小写首词；大小写转换用 `ord ± 32`',
                 '对比灵神：灵神靠稳定排序保序，这里把原位置放进关键字显式保序'],
    ),
)
