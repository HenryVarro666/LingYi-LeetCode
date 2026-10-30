CONFIG = dict(
    num=1753, title='移除石子的最大得分', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='比较最大堆与其余之和',
    tags=['灵神题单', '难度分 1488'],
    code='''
class Solution(object):
    def maximumScore(self, a, b, c):

        max_num = max(a, b, c)
        if max_num <= a + b + c - max_num:
            return (a + b + c) // 2
        else:
            return a + b + c - max_num
''',
    call='Solution().maximumScore(2, 3, 9)',
    expect=5,
    views=[
        dict(type='text', size=34, fn=lambda S: f"三堆石子 `a={S['a']}`  `b={S['b']}`  `c={S['c']}`"),
        dict(type='bars', var=lambda S: [S['a'], S['b'], S['c']], label='三堆石子 (a, b, c)', h=300,
             color=lambda S, i, v: ('orange' if 'max_num' in S and v == S['max_num'] and i == [S['a'], S['b'], S['c']].index(S['max_num']) else None)),
        dict(type='text', size=32, fn=lambda S: (
            f"最大堆 `{S['max_num']}`  vs  其余两堆之和 `{S['a']+S['b']+S['c']-S['max_num']}`" if 'max_num' in S else '')),
    ],
    watch=['a', 'b', 'c', ('max_num', 'max_num', 'orange')],
    captions={
        'max_num = max': '先找出最大的一堆 `max_num = {max_num}`（三堆等价，设它为 a）',
        'if max_num <=': lambda S, B, r: (
            f'最大堆 `{S.max_num}` ≤ 其余之和 `{S.a+S.b+S.c-S.max_num}`：最大堆不会剩下，能一直两两配对 → 走整除分支'
            if S.max_num <= S.a + S.b + S.c - S.max_num else
            f'最大堆 `{S.max_num}` > 其余之和 `{S.a+S.b+S.c-S.max_num}`：其余石子全拿完，最大堆还有剩 → 走 else'),
        'return (a + b + c) // 2': '能全部配对：得分 `(a+b+c) // 2` = =={ret}==（奇数时剩一颗落单）',
        'return a + b + c - max_num': '其余石子每颗都配最大堆：得分 `{a}+{b}+{c}-{max_num}` = =={ret}==',
    },
    cards=dict(
        after=[dict(heading='再看两个例子', lines=['`4,4,6`：`6 <= 4+4`，得 `14 // 2 = 7`', '`1,8,8`：`8 <= 1+8`，得 `17 // 2 = 8`', '`2,3,9`：`9 > 2+3`，得 `2+3 = 5`，最大堆剩下 4 颗']), dict(heading='作者的推导路线', lines=['先看最特殊的 `a = b = c`，三堆轮流拿', '再看 `a = b >= c`：先拿 (a,b) 变成三堆相等', '`a > b > c`：先拿 (a,b) 使 b = c，这轮次 k 最后可约掉', '所以只剩比较 `a` 与 `b + c` 一个条件'])],
        one_liner='最大堆不比其余之和大，就能拿到总数的一半，否则只能拿其余之和',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['三堆石子 `a, b, c`，每回合从两个不同非空堆各取一颗，得 1 分',
                 '有两堆或以上为空时停止，求最大得分',
                 '本视频：`a=2, b=3, c=9` → `5`'],
        quote='若a <= b + c，那么答案就是(a + b + c) / 2，否则答案就是b + c',
        quote_src='—— yiduobo 题解原文',
        idea=['设 a ≥ b ≥ c。`a = b = c` 时按 (a,b)(a,c)(b,c) 轮流拿，得 `(a+b+c)/2`',
              '`a > b > c` 时先拿 (a,b) 直到 b = c，化成 a > b = c 的情形，再分两种',
              '最终只用比较 a 与 b + c，不用模拟每一步'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错点：`a = b` 时必然满足 `a <= b + c`，也落在整除分支',
                 '对比灵神：灵神写成 `min(s // 2, s - m)`，和这里的两个分支等价'],
    ),
)
