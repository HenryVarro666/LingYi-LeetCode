CONFIG = dict(
    num=243, title='最短单词距离', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='记录最近位置 · 一趟遍历',
    tags=[],
    code='''
class Solution(object):
    def shortestDistance(self, wordsDict, word1, word2):

        pos1 = pos2 = None
        res = len(wordsDict)
        for index, word in enumerate(wordsDict):
            if word == word1:
                pos1 = index
                if pos2 is not None:
                    res = min(res, pos1 - pos2)
            elif word == word2:
                pos2 = index
                if pos1 is not None:
                    res = min(res, pos2 - pos1)
        
        return res
''',
    call="Solution().shortestDistance(['practice','makes','perfect','coding','makes'], 'makes', 'coding')",
    expect=1,
    views=[
        dict(type='array', var='wordsDict', pointers={'index': 'blue', 'pos1': 'pink', 'pos2': 'green'}, h=260, cell=130,
             color=lambda S, i, v: 'pink' if v == 'makes' else ('green' if v == 'coding' else None)),
        dict(type='text', h=70, fn=lambda S: f"当前最小距离 `res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('pos1', 'pos1', 'pink'), ('pos2', 'pos2', 'green'), ('res', 'res', 'yellow')],
    captions={
        'pos1 = pos2 = None': '`pos1`、`pos2`：word1、word2 ==最后一次出现==的下标，还没见过 → `None`',
        'res = len': '`res` 初值取 `len(wordsDict)`，比任何真实距离都大',
        'for index, word': '看第 `{index}` 个单词 `{word}`',
        'if word == word1': lambda S, B, r: f'`{S.word}` 是 word1（`{S.word1}`）吗？' + ('是' if S.word == S.word1 else '不是'),
        'pos1 = index': '更新 word1 的最近位置：`pos1 = {pos1}`',
        'if pos2 is not None': lambda S, B, r: ('word2 在前面出现过，可以组成一对' if S.pos2 is not None else 'word2 还没出现过，先不算'),
        'res = min(res, pos1': '后面的是 word1：用它和前面最近的 word2 比距离 `{pos1} - {pos2}` → `res = {res}`',
        'elif word == word2': lambda S, B, r: f'`{S.word}` 是 word2（`{S.word2}`）吗？' + ('是' if S.word == S.word2 else '不是，跳过'),
        'pos2 = index': '更新 word2 的最近位置：`pos2 = {pos2}`',
        'if pos1 is not None': lambda S, B, r: ('word1 在前面出现过，可以组成一对' if S.pos1 is not None else 'word1 还没出现过，先不算'),
        'res = min(res, pos2': '后面的是 word2：用它和前面最近的 word1 比距离 `{pos2} - {pos1}` → `res = {res}`',
        'return res': '遍历结束，最短距离 `{res}`',
    },
    cards=dict(
        one_liner='对后出现的那个词，只需看另一个词最近一次出现在哪',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给单词数组 `wordsDict` 和其中两个不同的单词 `word1`、`word2`',
                 '求这两个单词在数组中下标距离的 ==最小值==',
                 '本视频：`[practice, makes, perfect, coding, makes]`，`makes` 与 `coding` → `1`'],
        quote='最终答案必然是由一前一后两个单词计算得到的，那么对于出现在后面的这个单词而言，需要知道的就是另一个单词在当前位置之前最后一次出现的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案一定是「一前一后」的一对单词',
              '用 `pos1`、`pos2` 记两个词最后一次出现的下标',
              '遇到目标词：先用当前位置和另一个词的 `pos` 更新答案，再更新自己的 `pos`'],
        summary=['时间 `O(n)`，空间 `O(1)`，只遍历一趟',
                 '另一个 `pos` 还是 `None` 时不能相减，要先判断',
                 '更新答案用的是==离当前最近==的那次，所以每次都覆盖旧位置',
                 '原文为 Python 2 风格，仅删去了类型说明文档字符串'],
    ),
)
