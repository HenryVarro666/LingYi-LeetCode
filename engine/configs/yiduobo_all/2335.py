AMT = [5, 4, 4]

CONFIG = dict(
    num=2335, title='装满杯子需要的最短总时长', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='两杯一起接的次数尽量多',
    tags=['灵神题单', '贪心与思维', '难度分 1360'],
    code='''
class Solution(object):
    def fillCups(self, amount):

        s = sum(amount)
        ma = max(amount)

        if ma > s - ma:
            return ma
        else:
            return (s + 1) // 2
''',
    call=f'Solution().fillCups({AMT})',
    expect=7,
    views=[
        dict(type='array', var='amount', label='amount（冷 / 温 / 热）', cell=120, h=200,
             color=lambda S, i, v: 'orange' if 'ma' in S and v == S['ma'] else None),
        dict(type='text', size=30, h=120,
             fn=lambda S: (f"最多的一种 `ma = {S['ma']}`，其余加起来 `s − ma = {S['s'] - S['ma']}`" if 'ma' in S else '')),
    ],
    watch=[('s', 's', 'cyan'), ('ma', 'ma', 'orange')],
    captions={
        's = sum': '`s` = 杯子总数 = =={s}==',
        'ma = max': '`ma` = 最多的那种 = =={ma}==',
        'if ma > s - ma': lambda S, B, r: f'`ma = {S.ma}`，其余 `s − ma = {S.s - S.ma}`：' + ('最多的一种比其余加起来还多 → ==每杯都得单独装=={}' if S.ma > S.s - S.ma else '其余杯子足够配对，==能一直两杯一起接=={}').format(''),
        'return ma': '其余杯子配完后剩下的 `ma` 杯只能单接 → 答案 =={ma}==',
        'return (s + 1)': '能一直两杯一起接，最后可能剩 1 杯单接 → `(s+1)//2` = =={ret}==',
    },
    cards=dict(
        one_liner='两杯一起接的次数越多，总时长越短',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每秒可装 2 杯==不同==类型的水，或 1 杯任意类型',
                 '`amount` 给出冷、温、热水各需几杯，求最少秒数',
                 '示例：`[5,4,4]` → `7`'],
        quote='对于本题，需要总时长最短，因此理想的情况就是两杯一起接的次数尽可能多。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 1753 题（移除石子的最大得分）思路一样：每次凑一对不同的',
              '若最多的一种比其余加起来还多：配不完，答案就是它的数量 `ma`',
              '否则总能两两配对，只剩奇数时多 1 秒：`(s + 1) // 2`'],
        before=[dict(heading='先看三个例子', lines=['`[1,4,2]` → `4`：温水 4 杯，其余只有 3 杯，温水必有 1 杯单接',
                                              '`[5,4,4]` → `7`：其余 8 杯够配，13 杯两两配对再多 1 秒',
                                              '`[5,0,0]` → `5`：只有一种水，只能一杯一杯接'])],
        after=[dict(heading='与 1753 题对照', lines=['1753 求同时取两堆石子的次数最多，本题求两杯一起接的次数最多',
                                                '都是「最大的一堆」与「其余之和」比大小',
                                                '最大的一堆更大 → 被它卡住；否则尽量两两配对'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错：向上取整要写 `(s + 1) // 2`',
                 '对比灵神：灵神写成 `max((s+1)//2, m)` 一行，yiduobo 分两种情况讨论'],
    ),
)
