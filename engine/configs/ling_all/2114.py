CONFIG = dict(
    num=2114, title='句子中的最多单词数', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='数空格（Go 原文转写）', tags=[],
    code='''
class Solution:
    def mostWordsFound(self, sentences: List[str]) -> int:
        ans = 0
        for s in sentences:
            cnt = s.count(" ") + 1
            if cnt > ans:
                ans = cnt
        return ans
''',
    call='Solution().mostWordsFound(["please wait", "continue to fight", "continue to win", "i think so too"])',
    expect=4,
    views=[
        dict(type='array', var=lambda S: list(range(len(S['sentences']))), label='第几个句子（粉 = 当前句子）', cell=64, h=130,
             color=lambda S, i, v: 'pink' if 's' in S and S['sentences'][i] == S['s'] and i == S['sentences'].index(S['s']) else None),
        dict(type='string', var=lambda S: S.get('s'), label='s（黄 = 空格；单词数 = 空格数 + 1）', cell=36, h=170,
             color=lambda S, i, v: 'yellow' if v == ' ' else None),
        dict(type='text', fn=lambda S: f"空格 `{S['s'].count(' ')}` 个 → 单词 `{S['s'].count(' ')}+1` = =={S['s'].count(' ')+1}==" if 's' in S else '', size=26),
    ],
    watch=[('s', 's', 'pink'), ('cnt', 'cnt', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录目前见过的最多单词数，初始 0',
        'for s in sentences': '看下一个句子：`{s}`',
        'cnt = s.count': '空格 `{s.count(" ")}` 个，单词比空格多一个：`cnt` = =={cnt}==（不用 split，省额外空间）',
        'if cnt > ans': '`{cnt} > {ans}` → {"更多，更新答案" if cnt > ans else "不比 ans 多，跳过"}',
        'ans = cnt': '`ans = {ans}`：新的最多单词数',
        'return ans': '所有句子看完，最多 `{ans}` 个单词',
    },
    cards=dict(
        one_liner='单词数 = 空格数 + 1，数空格就不用 split',
        complexity='时间 `O(L)`，空间 `O(1)`',
        problem=['每个句子由单个空格隔开的单词组成，求单词最多的句子的单词数',
                 '示例：`["please wait", "continue to fight", "continue to win"]` → `3`',
                 '本视频：再加一句 `"i think so too"`，答案 `4`'],
        quote='如果用 split 做会有额外的空间开销，统计空格个数则可以做到 O(1) 的空间复杂度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['句首句尾没有多余空格、单词间只有一个空格',
              '所以单词数就是 `s.count(" ") + 1`',
              '边遍历边维护最大值'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`strings.Count` → `s.count`）',
                 '时间 `O(L)`，空间 `O(1)`',
                 '易错点：别忘了 +1；空格数是单词数减一'],
    ),
)
