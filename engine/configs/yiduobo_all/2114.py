CONFIG = dict(
    num=2114, title='句子中的最多单词数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='数空格 + 1',
    tags=[],
    code='''
class Solution(object):
    def mostWordsFound(self, sentences):

        res = 0
        for sentence in sentences:
            cnt = 1
            for char in sentence:
                if char == ' ':
                    cnt += 1
            res = max(res, cnt)

        return res
''',
    call="Solution().mostWordsFound(['hi you', 'a b c d', 'go on'])",
    expect=4,
    skip=['res = 0'],
    views=[
        dict(type='array', var='sentences', label='sentences（绿 = 当前最多单词的句子，蓝框 = 正在统计的句子）', cell=150, h=230, font=24,
             color=lambda S, i, v: 'blue' if 'sentence' in S and S['sentence'] == v else None),
        dict(type='string', var=lambda S: S.get('sentence'), label='当前句子（黄 = 空格）', cell=60, h=200,
             color=lambda S, i, v: 'yellow' if v == ' ' else None),
        dict(type='text', size=30, h=90,
             fn=lambda S: f"空格数 + 1 = 单词数：`cnt = {S['cnt']}`，目前最大 `res = {S['res']}`" if 'cnt' in S and 'sentence' in S else ''),
    ],
    watch=[('cnt', 'cnt', 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt = 1': '没有多余空格：先记 1 个单词，==单词数 = 空格数 + 1==，所以 `cnt` 从 1 开始',
        'for char in sentence': '逐个字符扫描这个句子',
        "if char == ' '": lambda S, B, r: (f"`char = '{S.char}'` 是空格 → 又一个单词的分隔" if S.char == ' ' else f"`char = '{S.char}'` 不是空格，跳过"),
        'cnt += 1': '遇到空格：下一个单词开始，`cnt` → {cnt}',
        'res = max': '这个句子共 `{cnt}` 个单词：`res = max({B.res}, {cnt}) = {res}`',
        'return res': '所有句子统计完，最多单词数 `{res}`',
    },
    cards=dict(
        one_liner='句子没有多余空格：单词数 = 空格数 + 1',
        complexity='时间 `O(总字符数)`，空间 `O(1)`',
        problem=['`sentences[i]` 是由单个空格隔开的句子，求单个句子里的最多单词数',
                 '示例：`["please wait", "continue to fight", "continue to win"]` → `3`',
                 '本视频：`["hi you", "a b c d", "go on"]` → `4`'],
        quote='由于句子中没有多余的空格，那么可以将问题转化为统计每个句子中空格的数目。若某个句子中空格的数目为cnt，那么句子中单词的数目就是cnt + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['单词之间恰好一个空格，首尾没有空格 → 空格数 + 1 就是单词数',
              '每个句子扫一遍，数出空格，`cnt` 从 1 起步',
              '一趟遍历取各句 `cnt` 的最大值作为答案'],
        summary=['时间 `O(总字符数)`，空间 `O(1)`，不用 `split` 省去额外数组',
                 '易错点：`cnt` 初值是 1 不是 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
