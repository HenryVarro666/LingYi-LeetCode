CONFIG = dict(
    num=1880, title='检查某单词是否等于两单词之和', difficulty='Easy', category='字符串',
    author='yiduobo', technique='字符串转数字',
    tags=[],
    code='''
class Solution(object):
    def isSumEqual(self, firstWord, secondWord, targetWord):

        return self.word_sum(firstWord) + self.word_sum(secondWord) == self.word_sum(targetWord)
    
    def word_sum(self, s):
        res = 0
        for char in s:
            res = res * 10 + ord(char) - 97
        
        return res
''',
    call='Solution().isSumEqual("acb", "cba", "cdb")',
    expect=True,
    views=[
        dict(type='string', var='s', cell=90, h=220,
             color=lambda S, i, v: 'blue' if S.get('char') == v else None),
        dict(type='text', size=32, h=90, fn=lambda S: f"当前数值 res = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=['s', 'char', ('res', 'res', 'green')],
    captions={
        'return self.word_sum(firstWord)': '三个单词各算一个数，判断 first + second 是否等于 target',
        'res = 0': '`res` 从 0 开始：要转换 `{s}`',
        'for char in s': '字符 `{char}`，`ord({char}) - 97` = {ord(char) - 97}',
        'res = res * 10': '`res = {B.res} * 10 + {ord(char) - 97}` → =={res}==（`a` 的 ASCII 是 97，减去它得字母值）',
        'return res': '`{s}` → `{res}`',
    },
    cards=dict(
        one_liner='`ord(c) - 97` 是字母值，按十进制逐位累加',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母 `a~j` 对应 `0~9`，把单词的字母值连起来就是它的数值',
                 '判断 `firstWord + secondWord` 的数值是否等于 `targetWord` 的数值',
                 '示例：`"acb" + "cba" == "cdb"`，即 `21 + 210 == 231` → `true`'],
        quote='直接按照题目中字符与数字的对应关系计算出三个单词对应的数值，然后判断是否满足两数之和等于目标数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`word_sum` 里 `res = res * 10 + ord(char) - 97`，就是逐位拼十进制数',
              '三个单词各转一次，最后比较两数之和与目标'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ord(char) - 97` 中 97 是 `a` 的 ASCII 码',
                 '前导 `a` 对应 0，不影响数值',
                 '原文为 Python 2 风格，本题无需改动代码',
                 '对比灵神：写法相同，灵神用 `b - \'a\'`，yiduobo 直接写 97'],
    ),
)
