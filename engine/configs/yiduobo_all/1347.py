CONFIG = dict(
    num=1347, title='制造字母异位词的最小步骤', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='字符计数 · 求公共部分',
    code='''
class Solution(object):
    def minSteps(self, s, t):

        s_cnt = {}
        t_cnt = {}
        for char in s:
            s_cnt[char] = s_cnt.get(char, 0) + 1
        for char in t:
            t_cnt[char] = t_cnt.get(char, 0) + 1
        
        res = len(s)
        for char, cnt in s_cnt.items():
            res -= min(cnt, t_cnt.get(char, 0))
        
        return res
''',
    call='Solution().minSteps("leetcode", "practice")',
    expect=5,
    views=[
        dict(type='string', var='s', h=150, label='s'),
        dict(type='string', var='t', h=150, label='t'),
        dict(type='map', var='s_cnt', h=190, label='s_cnt'),
        dict(type='map', var='t_cnt', h=190, label='t_cnt'),
    ],
    watch=['char', ('res', 'res', 'green')],
    captions={
        's_cnt = {}': '`s_cnt` 统计 `s` 里每个字符出现几次',
        't_cnt = {}': '`t_cnt` 统计 `t` 里每个字符出现几次',
        's_cnt[char] =': '`s` 里的 `{char}` 次数 → =={s_cnt[char]}==',
        't_cnt[char] =': '`t` 里的 `{char}` 次数 → =={t_cnt[char]}==',
        'res = len(s)': '先假设 `s` 的每个字符都要改：`res = {res}`',
        'for char, cnt in s_cnt': '看 `s` 里的字符 `{char}`（`s` 中出现 {cnt} 次）',
        'res -= min': '`{char}` 在两边最多能配上 `min({cnt}, {t_cnt.get(char, 0)})` 个，这些不用改 → `res = {res}`',
        'return res': '剩下配不上的字符都要替换：返回 =={ret}==',
    },
    cards=dict(
        one_liner='两边共有的字符不用改，其余都要换',
        complexity='时间 `O(n)`，空间 `O(1)`（字符集固定）',
        problem=['给等长字符串 `s` 和 `t`，每步可把 `t` 中任意字符换成任意字符',
                 '求使 `t` 成为 `s` 的字母异位词的最少步数',
                 '示例：`s = "leetcode"`，`t = "practice"` → `5`'],
        quote='分别统计两个字符串中每个字符出现的次数，然后对于每个字符，计算其同时出现在两个字符串中的次数，这些字符是不需要修改的',
        quote_src='—— yiduobo 题解原文',
        idea=['异位词 = 字符种类和次数都相同',
              '字符 `c` 在两边都有，能保留 `min(s_cnt[c], t_cnt[c])` 个',
              '答案 = 总长度 − 所有可保留的个数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`t_cnt` 里没有的字符要用 `.get(char, 0)`',
                 '只遍历 `s_cnt` 即可，`t` 独有的字符不会多算',
                 '原文已是 Python 3 可运行的写法，代码未改动'],
    ),
)
