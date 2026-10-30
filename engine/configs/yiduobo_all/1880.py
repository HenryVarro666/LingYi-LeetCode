def _val(w):
    r = 0
    for c in w:
        r = r * 10 + ord(c) - 97
    return r


CONFIG = dict(
    num=1880, title='检查某单词是否等于两单词之和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='字母值拼接成数',
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
        dict(type='string', var='s', label='当前单词 s', cell=96, h=200),
        dict(type='text', size=40, h=120,
             fn=lambda S: f"`{S['char']}` 的字母值 = `{ord(S['char']) - 97}`，`res` = =={S['res']}==" if 'char' in S and 'res' in S else ''),
    ],
    watch=['s', 'char', ('res', 'res', 'green')],
    max_steps=80,
    captions={
        'return self.word_sum(firstWord)': lambda S, B, r: f'分别算出三个单词的数值，再比较 `a + b == c` 是否成立（本例 `{_val(S.firstWord)}` + `{_val(S.secondWord)}` 对 `{_val(S.targetWord)}`）',
        'res = 0': '开始计算一个单词的数值，`res = 0`',
        'for char in s': '取下一个字母（取完就结束循环），`char` 当前为 `{char}`',
        'res = res * 10': '先把已有数值左移一位再加字母值：`{B.res} × 10 + {ord(char)} − 97` = =={res}==',
        'return res': '这个单词的数值是 `{res}`',
    },
    cards=dict(
        one_liner='字母值 a=0…j=9，逐位拼成十进制数再相加比较',
        complexity='时间 `O(L)`，空间 `O(1)`，`L` 为单词长度',
        problem=['字母值从 0 开始：`a→0, b→1, ...`，单词的数值 = 字母值按顺序连接成的整数',
                 '判断 `firstWord` 与 `secondWord` 的数值之和是否等于 `targetWord` 的数值',
                 '示例：`acb`=21，`cba`=210，`cdb`=231 → `true`'],
        quote='直接按照题目中字符与数字的对应关系计算出三个单词对应的数值，然后判断是否满足两数之和等于目标数。',
        quote_src='—— yiduobo 题解原文',
        idea=['把单词当十进制数读：每读一个字母，`res = res * 10 + 字母值`',
              '字母值 = `ord(char) - 97`；前导 a 值为 0，自然被丢掉',
              '三个单词各算一次，最后比较 `a + b == c`'],
        summary=['时间 `O(L)`，空间 `O(1)`',
                 '`ord(char) - 97` 得到 0 起算的字母值，别写成 1 起算',
                 '前导的 `a` 不影响数值，所以 `aaa` 和 `a` 都是 0',
                 '单词最长 8 位，数值不会溢出'],
    ),
)
