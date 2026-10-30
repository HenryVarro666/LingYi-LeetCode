CONFIG = dict(
    num=2186, title='制造字母异位词的最小步骤数 II', difficulty='Medium', category='字符串',
    author='yiduobo', technique='字符计数 · 差的绝对值',
    code='''
class Solution(object):
    def minSteps(self, s, t):

        s_cnt = {}
        t_cnt = {}
        for char in s:
            s_cnt[char] = s_cnt.get(char, 0) + 1
        for char in t:
            t_cnt[char] = t_cnt.get(char, 0) + 1
        
        res = 0
        for index in range(26):
            char = chr(index + 97)
            res += abs(s_cnt.get(char, 0) - t_cnt.get(char, 0))
        
        return res
''',
    call='Solution().minSteps("aab", "bcc")',
    expect=4,
    views=[
        dict(type='string', var='s', label='s', h=150),
        dict(type='string', var='t', label='t', h=150),
        dict(type='map', var='s_cnt', h=170),
        dict(type='map', var='t_cnt', h=170),
    ],
    watch=[('index', 'index', 'blue'), 'char', ('res', 'res', 'green')],
    captions={
        's_cnt[char] = ': '统计 s：`{char}` 出现 `{s_cnt[char]}` 次',
        't_cnt[char] = ': '统计 t：`{char}` 出现 `{t_cnt[char]}` 次',
        'res = 0': '`res` 累计需要追加的字符总数',
        'for index in range(26)': '按 26 个小写字母逐个检查，`index = {index}`',
        'char = chr': '`index + 97` 转成字母 `{char}`',
        'res += abs': '`{char}`：s 有 {s_cnt.get(char, 0)}，t 有 {t_cnt.get(char, 0)} → 差 `{abs(s_cnt.get(char, 0) - t_cnt.get(char, 0))}`，少的一边补这么多个：`res` = {res}',
        'return res': '每种字母的差累加起来 = ==`{res}`== 步',
    },
    skip=['for char in s', 'for char in t'],
    max_steps=60,
    cards=dict(
        one_liner='每种字母补齐两边的个数差，差的绝对值之和就是答案',
        complexity='时间 `O(n + m + 26)`，空间 `O(26)`',
        problem=['每步可以给 `s` 或 `t` 追加任意一个字符',
                 '求让 `s` 和 `t` 互为字母异位词的最少步数',
                 '示例：`s="leetcode", t="coats"` → `7`；本视频用 `"aab"`、`"bcc"` → `4`'],
        quote='因此只需统计两个字符串中每种字符出现的次数，然后遍历每种字符，添加若干当前遍历到的字符直到两个字符串中该字符的数目相等',
        quote_src='—— yiduobo 题解原文',
        idea=['每步只能加一个字符：想让某个字母个数相等，只能给少的一边补',
              '某个字母要补的次数 = 两边个数之差的绝对值',
              '各个字母互不影响，累加即可'],
        summary=['时间 `O(n + m)`，空间 `O(26)`',
                 '字母没出现过要用 `get(char, 0)`，否则 KeyError',
                 '只遍历 26 个小写字母，不会漏掉只在一边出现的字母',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
