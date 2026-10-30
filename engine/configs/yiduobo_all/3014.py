def _txt(S):
    if 'index' not in S:
        return '频率大的字符放在前面：排名 0-7 按 1 次，8-15 按 2 次……'
    return f"排名 `{S['index']}`，出现 `{S['f']}` 次 → 累计 =={S['res']}=="


CONFIG = dict(
    num=3014, title='输入单词需要的最少按键次数 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='频率排序 · 按排名算次数',
    code='''
class Solution(object):
    def minimumPushes(self, word):

        freq = Counter(word)
        res = 0
        for index, f in enumerate(sorted(freq.values(), reverse=True)):
            if index < 8:
                res += f
            elif index < 16:
                res += f * 2
            elif index < 24:
                res += f * 3
            else:
                res += f * 4
        
        return res
''',
    call="Solution().minimumPushes('abcdefghijkl')",
    expect=16,
    views=[
        dict(type='string', var='word', label='word', cell=70, h=170,
             color=lambda S, i, v: ['blue', 'green', 'orange', 'pink'][min(i // 8, 3)]),
        dict(type='map', var='freq', label='freq（字符出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=260, font=26),
        dict(type='text', fn=_txt, h=90, size=30),
    ],
    watch=['index', 'f', ('res', 'res', 'green')],
    captions={
        'freq = Counter': '统计每种字符的出现次数：`{dict(freq)}`',
        'enumerate': '频率从大到小排序后，第 `{index}` 名，出现 `f = {f}` 次',
        'if index < 8': lambda S, B, r: (f'排名 `{S.index}` < 8？是：前 8 名在各键第 1 个字母上，按 1 次' if S.index < 8
                                         else f'排名 `{S.index}` < 8？不是，看下一档'),
        8: '排名靠前：每次只按 1 次 → `res += {f}` = {res}',
        'elif index < 16': '排名 `{index}` < 16？第 8-15 名在各键第 2 个字母，按 2 次',
        'res += f * 2': '每次按 2 次：`res += {f} × 2` = =={res}==',
        'elif index < 24': '排名 `{index}` < 24？第 3 个字母，按 3 次',
        'res += f * 3': '`res += {f} × 3` = {res}',
        'res += f * 4': '剩下的都在第 4 个字母：`res += {f} × 4` = {res}',
        'return res': '按键总次数 =={res}==',
    },
    cards=dict(
        one_liner='频率高的字符放前面，按键次数 = 频率 × 所在档位',
        complexity='时间 `O(n + 26 log 26)`，空间 `O(1)`',
        problem=['`word` 由不同小写字母组成，可把 2~9 键重新映射字母',
                 '同一个键上第 `j` 个字母要按 `j` 次，求最少总按键数',
                 '本视频：`"abcdefghijkl"` → `16`'],
        quote='为了使得按键次数最少，就应该让频率高的字符尽量靠前。',
        quote_src='—— yiduobo 题解原文',
        idea=['统计每种字符的次数，从大到小排列',
              '排名 0-7 在第 1 档，8-15 在第 2 档，16-23 在第 3 档，其余第 4 档',
              '不用真的映射：次数 × 档位累加即可（本题字母互异，每个次数都是 1）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '本题字母互不相同，频率全为 1；第 3016 题可重复，代码同样适用',
                 '易错：键数是 8，档位每 8 名上一档',
                 '原文为 Python 2 风格，只删去了类型说明，代码无需改动',
                 '对比灵神：灵神直接用 `n` 推公式；yiduobo 按频率排序，更通用'],
    ),
)
