CONFIG = dict(
    num=1451, title='重新排列句子中的单词', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按（长度, 原位置）排序', tags=[],
    code='''
class Solution(object):
    def arrangeWords(self, text):

        words = text.split(' ')
        words[0] = chr(ord(words[0][0]) + 32) + words[0][1:]

        sorted_index = sorted(range(len(words)), key=lambda d:(len(words[d]), d))
        res = ' '.join([words[index] for index in sorted_index])
        return chr(ord(res[0]) - 32) + res[1:]
''',
    call='Solution().arrangeWords("Keep calm and code on")',
    expect='On and keep calm code',
    views=[
        dict(type='array', var='words', label='words（原顺序）', h=200, cell=150,
             color=lambda S, i, v: 'blue' if i == 0 else None),
        dict(type='array', var='sorted_index', label='sorted_index（按 长度, 原位置 排好的下标）', h=200),
        dict(type='text', fn=lambda S: (f"`res` = =={S['res']}==" if 'res' in S else '长度：' + ' '.join(f"`{w}`={len(w)}" for w in S['words']) if 'words' in S else ''), size=30),
    ],
    watch=[('res', 'res', 'green')],
    captions={
        'words = text.split': '按空格切成单词：`{words}`',
        'words[0] = chr': '首字母是大写，先改成小写（ASCII 码 `+32`），否则 `Keep` 会被当成别的单词参与排序：`words[0] = {words[0]}`',
        'sorted_index = sorted': '对下标排序，==第一关键字是长度，第二关键字是原位置==：排序结果 `{sorted_index}`；长度相同时按原位置，保证稳定',
        "res = ' '.join": '按 `sorted_index` 的顺序取出单词再用空格拼起来：`{res}`',
        'return chr': '最后把第一个字母改回大写（码 `−32`）：`{ret}`',
    },
    cards=dict(
        one_liner='先把首字母改小写，按（长度，原位置）排序，再改回大写',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['句子首字母大写、单词用单个空格分隔',
                 '按单词长度升序重排，长度相同保持原相对顺序，格式不变',
                 '本视频：`Keep calm and code on` → `On and keep calm code`'],
        quote='首先按空格分离出各个单词，并将第0个单词的首字母从大写改为小写。接下来将各个单词以长度为第一关键字，原始位置为第二关键字进行排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序的是==下标==，key 是 `(len(words[d]), d)`',
              '把原位置 `d` 当第二关键字，长度相同时自然保持原顺序',
              '首尾各做一次大小写转换：`+32` 变小写，`−32` 变大写'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：首字母不先改小写，`Keep` 虽然长度不变但结果里大写位置会错',
                 '`ord/chr` 加减 32 只对英文字母成立，题目保证了这一点',
                 '原文已是 Python 3 可运行写法，无需改动'],
    ),
)
