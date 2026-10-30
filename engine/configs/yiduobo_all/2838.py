CONFIG = dict(
    num=2838, title='英雄可以获得的最大金币数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 单调双指针 + 前缀和',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maximumCoins(self, heroes, monsters, coins):

        info = sorted(zip(monsters, coins))
        res = [0] * len(heroes)

        p = 0
        s = 0
        for index, power in sorted(enumerate(heroes), key=lambda d:d[1]):
            while p < len(info) and info[p][0] <= power:
                s += info[p][1]
                p += 1

            res[index] = s

        return res
''',
    call='Solution().maximumCoins([4, 9, 1, 6], [2, 6, 3, 9], [10, 20, 5, 30])',
    expect=[15, 65, 0, 35],
    views=[
        dict(type='array', var='heroes', label='heroes（英雄能力值，按下标 index 写结果）', h=190,
             pointers={'index': 'blue'}),
        dict(type='table', var='info', label='info = 按能力值排序的 (怪物能力, 金币)；绿 = 已经能打败', h=210,
             cols=['能力', '金币'], rows=lambda S: [str(i) for i in range(len(S['info']))],
             color=lambda S, i, j, v: ('green' if 'p' in S and i < S['p'] else None)),
        dict(type='array', var='res', label='res（每个英雄的金币总数，按原下标）', h=190, pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and i == S['index'] and 's' in S else None),
        dict(type='text', size=30, h=70, fn=lambda S: (f"当前英雄 power = ==`{S['power']}`==，已打败 `{S['p']}` 只怪物，金币 s = ==`{S['s']}`==" if 'power' in S and 'p' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('power', 'power', 'cyan'), ('p', 'p', 'pink'), ('s', 's', 'orange')],
    captions={
        'info = sorted': '怪物按能力值升序排好：`info = {info}`，能力强的怪排后面',
        'res = [0]': '`res` 按英雄的==原始下标==存答案',
        'p = 0': '`p`：下一个还没打败的怪物下标；它只增不减',
        's = 0': '`s`：已打败怪物的金币总和',
        'for index, power': '英雄按能力值从小到大处理：这次是原下标 `{index}`、能力 `{power}`',
        'while p < len(info)': lambda S, B, r: (f"怪物 `info[{S.p}]` 能力 {S['info'][S.p][0]} {'<=' if S['info'][S.p][0] <= S.power else '>'} 英雄 {S.power} → " + ('打得过，继续吃' if S['info'][S.p][0] <= S.power else '打不过，停') if S.p < len(S['info']) else '怪物全部扫完，停'),
        's += info[p][1]': '拿下这只怪的金币 `{info[p][1]}`：`s` = =={s}==',
        'p += 1': '`p` 右移到 {p}：下一只怪物',
        'res[index] = s': '英雄（原下标 `{index}`）最多拿到 ==`{s}`== 金币',
        'return res': '全部英雄处理完，返回 `{res}`',
    },
    cards=dict(
        one_liner='英雄和怪物都排序，p 只前进不回头，边走边累加金币',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n + m)`',
        problem=['每个英雄有能力值，每个怪物有能力值和金币',
                 '英雄能打败所有能力值不超过自己的怪物，求每个英雄最多拿多少金币',
                 '本视频：英雄 `[4,9,1,6]`，怪物 `[2,6,3,9]`，金币 `[10,20,5,30]` → `[15,65,0,35]`'],
        quote='对于排序后的英雄heroes[i]，若其能击败的最大的怪物是monsters[j]，那么对于heroes[i + 1]，其能击败的最大的怪物monsters[k]必然满足k >= j。',
        quote_src='—— yiduobo 题解原文',
        idea=['能力越强的英雄，能打败的怪物集合越大，是前一个的超集',
              '英雄从弱到强处理，`p` 指向第一只打不过的怪，只增不减',
              '金币和 `s` 一路累加，每个英雄直接写到原下标 `res[index]`'],
        summary=['排序 `O(n log n + m log m)`，双指针扫描 `O(n + m)`',
                 '英雄要带着原下标排序（`enumerate`），否则答案顺序会乱',
                 '能力值相等也能打败，所以是 `<=`',
                 '原文为 Python 2 风格，本题代码无需修改，仅去掉多余空行'],
    ),
)
