CONFIG = dict(
    num=2186, title='制造字母异位词的最小步骤数 II', difficulty='Medium', category='字符串',
    author='yiduobo', technique='两个字典计数 · 逐字母求差',
    tags=[],
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
    call='Solution().minSteps("abca", "bcd")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s', cell=80, h=110),
        dict(type='string', var='t', label='t', cell=80, h=110),
        dict(type='map', var='s_cnt', label='s_cnt', fmt=lambda k, v: f"'{k}': {v}", h=120, font=30),
        dict(type='map', var='t_cnt', label='t_cnt', fmt=lambda k, v: f"'{k}': {v}", h=120, font=30),
        dict(type='text', fn=lambda S: (f"字母 `'{S['char']}'`：s 有 {S['s_cnt'].get(S['char'], 0)} 个，t 有 {S['t_cnt'].get(S['char'], 0)} 个，差 ==" 
                                         f"{abs(S['s_cnt'].get(S['char'], 0) - S['t_cnt'].get(S['char'], 0))}==") if 'index' in S and 'char' in S else '', size=28),
    ],
    watch=[('char', 'char', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        's_cnt = {}': '`s_cnt` 统计 s 中各字母次数',
        't_cnt = {}': '`t_cnt` 统计 t 中各字母次数',
        's_cnt[char] =': "s 的 `'{char}'` 次数 → `{s_cnt[char]}`",
        't_cnt[char] =': "t 的 `'{char}'` 次数 → `{t_cnt[char]}`",
        'res = 0': '`res` 累计总共要添加的字符数',
        'for index in range(26)': lambda S, B, ret: f"枚举字母 `'{chr(S.index + 97)}'`（第 {S.index} 个）",
        'res += abs': lambda S, B, ret: (f"`'{S.char}'`：两串次数差 `{abs(S.s_cnt.get(S.char, 0) - S.t_cnt.get(S.char, 0))}`，"
                                         f"加这么多个字母才能补平 → `res` = =={S.res}=="),
        'return res': '所有字母的差之和 `{res}` 就是最少步数',
    },
    skip=['char = chr'],
    max_steps=90,
    cards=dict(
        one_liner='每步只能加一个字符，所以每种字母补的次数就是次数之差',
        complexity='时间 `O(n+m+26)`，空间 `O(26)`',
        problem=['每步给 `s` 或 `t` 追加一个任意字符，求让两串互为字母异位词的最少步数',
                 '示例：`s = "leetcode"`，`t = "coats"` → `7`',
                 '本视频：`s = "abca"`，`t = "bcd"` → `3`'],
        quote='添加若干当前遍历到的字符直到两个字符串中该字符的数目相等，那么添加的次数就是两个字符串中该字符出现次数之差的绝对值。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用两个字典各自统计字母出现次数', '再枚举 26 个字母，次数少的一方补到和另一方一样多', '补的次数 = 次数之差的绝对值，累加得答案'],
        summary=['时间 `O(n+m)`，空间 `O(26)`',
                 '字典用 `get(char, 0)`：没出现过的字母次数当 0',
                 '枚举 `0~25` 再 `chr(index + 97)` 转成字母，覆盖所有小写字母'],
    ),
)
