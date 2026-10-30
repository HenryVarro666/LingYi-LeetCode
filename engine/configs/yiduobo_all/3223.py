CONFIG = dict(
    num=3223, title='操作后字符串的最短长度', difficulty='Medium', category='字符串',
    author='yiduobo', technique='计数 · 奇偶分类',
    code='''
class Solution(object):
    def minimumLength(self, s):
        res = 0
        freq = Counter(s)
        for f in freq.values():
            if f % 2 == 1:
                res += 1
            else:
                res += 2

        return res
''',
    call='Solution().minimumLength("abaacbcbb")',
    expect=5,
    views=[
        dict(type='string', var='s', h=200, label='s'),
        dict(type='map', var='freq', fmt=lambda k, v: f'{k}: {v}次', h=300),
        dict(type='text', size=32, fn=lambda S: f"`res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=['f', 'res'] if False else [('f', "f if 'f' in dir() else ''", 'blue')] if False else ['res'],
    captions={
        'res = 0': '`res` 累计最终剩下的字符个数',
        'freq = Counter': '先统计每种字符的出现次数：`freq` = {dict(freq)}',
        'for f in': '取下一个出现次数（取完就退出循环）：`f` = {f}',
        'if f % 2 == 1': '`{f} % 2 == 1` → {"成立：奇数次，最后必剩 1 个" if f % 2 == 1 else "不成立：偶数次，最后必剩 2 个"}',
        'res += 1': '奇数次的字符最后剩 1 个：`res` += 1 → =={res}==',
        'res += 2': '偶数次的字符最后剩 2 个：`res` += 2 → =={res}==',
        'return res': '所有字符剩下的总数 =={res}==',
    },
    cards=dict(
        one_liner='只要出现 ≥ 3 次就能成对删，奇数剩 1、偶数剩 2',
        complexity='时间 `O(n)`，空间 `O(1)`（字符集大小固定）',
        problem=['每次选 `s[i]`，若左右都有相同字符，就删去左右最近的各一个',
                 '求操作若干次后字符串的最短长度',
                 '示例：`"abaacbcbb"` → `5`'],
        quote='注意到题目中的删除并不要求字符相邻，那么只要某个字符串的出现次数大于等于三次，那么就可以从中删去两个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['删除不要求相邻：同一种字符只要有 3 个就能删 2 个',
              '出现奇数次 → 反复减 2，最终剩 1 个',
              '出现偶数次 → 反复减 2，最终剩 2 个（2 个已经无法再操作）',
              '先统计次数，再遍历累加：奇数加 1，偶数加 2'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：偶数次最少剩 2 个，不是 0',
                 '`Counter` 在 LeetCode 里已预置，无需 import',
                 '对比灵神：他把奇偶两支合成一个公式 `(c−1)%2+1`，思路相同'],
    ),
)
