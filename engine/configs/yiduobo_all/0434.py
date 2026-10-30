CONFIG = dict(
    num=434, title='字符串中的单词数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='直接 split',
    code='''
class Solution(object):
    def countSegments(self, s):

        return len(s.split())
''',
    call='Solution().countSegments("Hello, my  name is John")',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（注意有连续两个空格）', h=200),
        dict(type='text', h=80, fn=lambda S: "`s.split()` = " + str(S['s'].split()) if 's' in S else ''),
        dict(type='text', h=80, fn=lambda S: "单词数 = ==" + str(len(S['s'].split())) + "==" if 's' in S else ''),
    ],
    watch=[('s', 's'), ('words', 's.split()', 'blue')],
    captions={
        'return': '`split()` 不带参数：==按任意连续空白切分，并丢掉空串==，得到 `{s.split()}`，长度就是单词数 =={ret}==',
    },
    cards=dict(
        one_liner='单词数 = 按空白切分后的段数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['单词是不含空格的连续字符，统计字符串里有多少个单词',
                 '单词之间可能有多个空格，开头结尾也可能有空格',
                 '示例：`"Hello, my name is John"` → `5`'],
        quote='比较基础的题目，直接split即可。各种高级语言现在应该都支持这个操作了。',
        quote_src='—— yiduobo 题解',
        idea=['不用手写状态机，直接调用语言自带的 `split`',
              '无参 `split()` 会合并连续空白，空串不会出现在结果里',
              '所以 `len(s.split())` 就是答案'],
        after=[dict(heading='split() 与 split(" ")', lines=['`"a  b".split()` → `[\'a\', \'b\']`', '`"a  b".split(" ")` → `[\'a\', \'\', \'b\']`', '后者多出空串，会多算一个单词'])],
        before=[dict(heading='先想想手写怎么做', lines=['扫描字符，遇到「非空格且前一个是空格或开头」就算一个新单词', '需要处理首尾空格、连续空格，容易写错边界', '语言自带的 `split()` 已经帮我们处理好了'])],
        summary=['时间 `O(n)`，空间 `O(n)`（切出来的列表）',
                 '易错点：别写成 `split(" ")`，连续空格会产生空串，多算单词',
                 '空串或全是空格时，`split()` 返回 `[]`，答案为 0'],
    ),
)
