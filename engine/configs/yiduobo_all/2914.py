CONFIG = dict(
    num=2914, title='使二进制字符串变美丽的最少修改次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='拆成长度 2 的子串 · 逐对比较',
    tags=['灵神题单', '难度分 1480'],
    code='''
class Solution(object):
    def minChanges(self, s):

        res = 0
        for index in range(0, len(s), 2):
            if s[index] != s[index + 1]:
                res += 1
        
        return res
''',
    call='Solution().minChanges("10110100")',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（每 2 个字符一组）', h=260,
             window=('index', 'index+1'),
             color=lambda S, i, v: ('red' if 'index' in S and i // 2 * 2 == S['index'] and S['s'][S['index']] != S['s'][S['index'] + 1] else 'green' if 'index' in S and i // 2 * 2 == S['index'] and S['_line'] >= 7 else None)),
        dict(type='text', fn=lambda S: f"已发现 `{S['res']}` 组不相等，需要修改 `{S['res']}` 次" if 'res' in S else '', size=30),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计需要修改的次数',
        'for index in range': lambda S, B, r: ('已经没有下一对了，循环结束' if 'index' in B and B['index'] == S['index'] else f'步长为 2：这次看一对 `(s[{S.index}], s[{S.index+1}])`'),
        'if s[index] != s[index + 1]': lambda S, B, r: (f'`s[{S.index}] = {S.s[S.index]}` 与 `s[{S.index+1}] = {S.s[S.index+1]}` ' + ('不同 → 这一对要改一个字符' if S.s[S.index] != S.s[S.index + 1] else '相同 → 这一对已经美丽，不用改')),
        'res += 1': '改其中一个字符让这对相同：`res = {res}`',
        'return res': '所有对都处理完，最少修改 =={res}== 次',
    },
    cards=dict(
        one_liner='最终切成一个个长度 2 的小段，逐段比较两个字符',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`（长度为偶数），能分成若干偶数长度、只含 0 或只含 1 的子串就是「美丽」的',
                 '每次可把任一字符改成 0 或 1，求最少修改次数',
                 '本视频：`s = "10110100"` → `2`'],
        quote='构造一个较长的美丽子串显然是比构造若干个长度为2的美丽子串更容易的，因此最终字符串应该划分成若干个长度为2的子串，然后逐个计算将其变为美丽子串需要的操作数。',
        quote_src='—— yiduobo 题解原文',
        idea=['长的美丽子串能拆成长度 2 的美丽子串，所以只需考虑长度为 2 的段',
              '用步长 2 遍历，每次比较当前字符与下一个字符',
              '不同就要改一次，相同不用改，累加到 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：步长是 2；`index + 1` 不会越界（长度为偶数）',
                 '每对至多改 1 次：改任一个字符都能让这对相同',
                 '对比灵神：灵神用一行 `sum(...)` 统计，yiduobo 用循环 + 计数器',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
