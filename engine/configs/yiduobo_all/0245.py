CONFIG = dict(
    num=245, title='最短单词距离 III', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='最近位置 · same_flag 处理相同词',
    tags=[],
    code='''
class Solution(object):
    def shortestWordDistance(self, wordsDict, word1, word2):

        pos1 = pos2 = None
        if word1 == word2:
            same_flag = True
        else:
            same_flag = False

        res = len(wordsDict)
        for index, word in enumerate(wordsDict):
            if word == word1:
                if same_flag:
                    if pos1 is not None:
                        res = min(res, index - pos1)
                    pos1 = index
                else:
                    pos1 = index
                    if pos2 is not None:
                        res = min(res, pos1 - pos2)
            elif word == word2:
                pos2 = index
                if pos1 is not None:
                    res = min(res, pos2 - pos1)
        
        return res
''',
    call="Solution().shortestWordDistance(['practice','makes','perfect','coding','makes'], 'makes', 'makes')",
    expect=3,
    views=[
        dict(type='array', var='wordsDict', pointers={'index': 'blue', 'pos1': 'pink'}, h=260, cell=130,
             color=lambda S, i, v: 'pink' if v == S.get('word1') else None),
        dict(type='text', h=70, fn=lambda S: (f"`same_flag` = =={S['same_flag']}==　当前最小距离 `res` = =={S['res']}==" if 'res' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('pos1', 'pos1', 'pink'), ('pos2', 'pos2', 'green'),
           ('same_flag', 'same_flag', 'orange'), ('res', 'res', 'yellow')],
    captions={
        'pos1 = pos2 = None': '`pos1`、`pos2` 记两个词最近一次出现的下标，先都是 `None`',
        'if word1 == word2': lambda S, B, r: f'`word1 = {S.word1}`，`word2 = {S.word2}`：' + ('==两个词相同==，要特殊处理' if S.word1 == S.word2 else '不同，沿用 243 题做法'),
        'same_flag = True': '`same_flag = True`：只有一个词，下标要和==自己的上一次==比',
        'same_flag = False': '`same_flag = False`：两个词不同，走 243 题的逻辑',
        'res = len': '`res` 初值取数组长度 `{res}`',
        'for index, word': '看第 `{index}` 个单词 `{word}`',
        'if word == word1': lambda S, B, r: f'`{S.word}` 是 word1 吗？' + ('是' if S.word == S.word1 else '不是'),
        'if same_flag': lambda S, B, r: ('相同词情形：用上一次出现的位置算距离' if S.same_flag else '不同词情形：和 word2 的位置比'),
        'if pos1 is not None': lambda S, B, r: ('以前出现过 `makes`，可以算一次距离' if S.pos1 is not None else '这是它第一次出现，没有可比的位置'),
        'res = min(res, index - pos1)': '当前位置 `{index}` 与上一次 `{pos1}` 的距离 `{index - pos1}` → `res = {res}`',
        'pos1 = index': '记下 word1 最新出现的位置 `pos1 = {pos1}`',
        'if pos2 is not None': lambda S, B, r: ('word2 出现过，可以组成一对' if S.pos2 is not None else 'word2 还没出现过'),
        'res = min(res, pos1 - pos2)': '`res = min(.., {pos1} - {pos2})` → {res}',
        'elif word == word2': lambda S, B, r: f'`{S.word}` 是 word2 吗？' + ('是' if S.word == S.word2 else '不是，跳过'),
        'pos2 = index': '更新 word2 的位置 `pos2 = {pos2}`',
        'res = min(res, pos2 - pos1)': '`res = min(.., {pos2} - {pos1})` → {res}',
        'return res': '遍历结束，最短距离 `{res}`',
    },
    cards=dict(
        one_liner='相同词时，拿当前位置和它自己上一次出现的位置比',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['243 题的进阶：`word1` 和 `word2` ==可能是同一个单词==',
                 '求两个单词在数组中下标距离的最小值（两个下标必须不同）',
                 '本视频：`[practice, makes, perfect, coding, makes]`，`makes` 与 `makes` → `3`'],
        quote='对于相同的情况，可以在一开始先设置一个same_flag来表示两个单词是否相同，……就是用当前位置和word1上次出现的位置之差来更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `same_flag` 记下两词是否相同',
              '相同：每遇到一次，先和 `pos1`（上一次）算距离，再把 `pos1` 更新成当前',
              '不同：和 243 题完全一样'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '相同词时要==先算距离、再更新 pos1==，否则会算出距离 0',
                 '`word1 == word2` 时 `elif word == word2` 分支永远走不到',
                 '原文为 Python 2 风格，仅删去了类型说明文档字符串'],
    ),
)
