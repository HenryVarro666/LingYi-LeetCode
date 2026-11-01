CONFIG = dict(
    num=2114, title='句子中的最多单词数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='逐字符数空格', tags=[],
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
    call='Solution().mostWordsFound(["please wait", "continue to win", "i think so"])',
    expect=3,
    views=[
        dict(type='array', var=lambda S: list(range(len(S['sentences']))), label='第几个句子（粉 = 当前）', cell=64, h=120,
             color=lambda S, i, v: 'pink' if 'sentence' in S and S['sentences'][i] == S['sentence'] else None),
        dict(type='string', var='sentence', label='sentence（黄 = 空格）', cell=36, h=180,
             color=lambda S, i, v: 'yellow' if v == ' ' else None),
        dict(type='text', fn=lambda S: f"`cnt = {S['cnt']}`（空格数 + 1）" if 'cnt' in S else '', size=28),
    ],
    watch=[('sentence', 'sentence', 'pink'), ('char', 'char', 'blue'), ('cnt', 'cnt'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录最多单词数',
        'for sentence in': '看下一个句子：`{sentence}`',
        'cnt = 1': '`cnt = 1`：单词数 = 空格数 + 1，先把最后一个单词算上',
        'for char in': '看字符 `{char}`',
        "if char == ' '": '`{char!r} == " "` → {"是空格，说明又多一个单词" if char == " " else "不是空格，跳过"}',
        'cnt += 1': '遇到空格：`cnt` → =={cnt}==',
        'res = max': '`res = max({B.res}, {cnt}) = {res}`',
        'return res': '最多的句子有 `{res}` 个单词',
    },
    cards=dict(
        one_liner='句子里没有多余空格，单词数 = 空格数 + 1',
        complexity='时间 `O(L)`，空间 `O(1)`',
        problem=['每个句子由单个空格隔开的单词组成，求单词最多的句子的单词数',
                 '示例：`["please wait", "continue to fight", "continue to win"]` → `3`',
                 '本视频：`["please wait", "continue to win", "i think so"]` → `3`'],
        quote='由于句子中没有多余的空格，那么可以将问题转化为统计每个句子中空格的数目。若某个句子中空格的数目为cnt，那么句子中单词的数目就是cnt + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt` 从 `1` 起，每碰到一个空格就加一',
              '数完一个句子就用 `max` 更新 `res`',
              '一趟遍历，取最大值'],
        summary=['时间 `O(L)`，空间 `O(1)`',
                 '`cnt` 初值是 `1`，不是 `0`',
                 '代码与原文一致，Python 3 下可直接运行（无需修改）',
                 '对比灵神：灵神直接用 `count` 数空格，这里手写循环数'],
    ),
)
