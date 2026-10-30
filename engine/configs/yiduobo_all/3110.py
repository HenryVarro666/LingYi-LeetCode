CONFIG = dict(
    num=3110, title='字符串的分数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 累加差值', tags=[],
    code='''
class Solution(object):
    def scoreOfString(self, s):

        res = 0
        for index in range(1, len(s)):
            res += abs(ord(s[index]) - ord(s[index - 1]))
        
        return res
''',
    call='Solution().scoreOfString("hello")',
    expect=13,
    views=[
        dict(type='string', var='s', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: ('green' if 'index' in S and i == S['index'] - 1 else None)),
        dict(type='text', size=34, fn=lambda S: (f"`|{ord(S['s'][S['index']])} − {ord(S['s'][S['index']-1])}|` = =={abs(ord(S['s'][S['index']])-ord(S['s'][S['index']-1]))}==") if 'index' in S and 1 <= S['index'] < len(S['s']) else ''),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计分数',
        'for index in': lambda S, B, r: (f"`index = {S.index}`：比较 `s[{S.index}]` 和前一个 `s[{S.index-1}]`" if 'index' not in B or B.index != S.index else '`index` 已走完 → 循环结束'),
        'res += abs': '`|ord({s[index]!r}) − ord({s[index - 1]!r})|` = `|{ord(s[index])} − {ord(s[index - 1])}|` = {abs(ord(s[index]) - ord(s[index - 1]))} → `res` = =={res}==',
        'return res': '所有相邻差累加：=={res}==',
    },
    cards=dict(
        one_liner='从下标 1 起，当前字符与前一个字符的差累加',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['分数 = 相邻字符 ASCII 码之差的绝对值之和', '示例：`"hello"` → `13`', '示例：`"zaz"` → `50`'],
        quote='从下标1开始向后一趟遍历，将当前字符与前一个字符ascii码之差的绝对值累加到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标从 1 开始，才有“前一个字符”可比', '`ord` 取 ASCII 码，`abs` 取绝对值', '一趟遍历，边走边加'],
        summary=['时间 `O(n)`，空间 `O(1)`', '循环从 1 开始，避免 `s[-1]` 误当“前一个”',
                 '代码原样照搬，Python 3 可直接运行',
                 '对比灵神：灵神用 `pairwise` 一行写完，这里是显式下标'],
    ),
)
