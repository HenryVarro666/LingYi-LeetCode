CONFIG = dict(
    num=3296, title='移山所需的最少秒数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分时间 + 解一元二次不等式',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1850'],
    code='''
class Solution(object):
    def minNumberOfSeconds(self, mountainHeight, workerTimes):

        left = 1
        right = min(workerTimes) * (1 + mountainHeight) * mountainHeight // 2

        while left < right:
            mid = (left + right) // 2
            h = 0
            for t in workerTimes:
                h += int(sqrt(mid * 2.0 / t + 0.25) - 0.5)
            
            if h < mountainHeight:
                left = mid + 1
            else:
                right = mid

        return left
''',
    setup='from math import sqrt',
    call='Solution().minNumberOfSeconds(4, [2, 1, 1])',
    expect=3,
    views=[
        dict(type='array', var='workerTimes', label='workerTimes', h=170),
        dict(type='array', h=190, label='二分区间 [left, right]（时间，单位秒）',
             var=lambda S: list(range(S['left'], S['right'] + 1)) if 'right' in S and S['right'] - S['left'] < 12 else [],
             pointers={}),
        dict(type='text', h=130, fn=lambda S: (
            f"试 `mid = {S['mid']}` 秒：所有工人一共能降 ==`{S['h']}`== 米（山高 `{S['mountainHeight']}`）" if 'mid' in S and 'h' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', 'h', 'mountainHeight'],
    skip=['h = 0'],
    captions={
        'left = 1': '时间至少 `1` 秒，`left = 1`',
        'right = min': '上界取保守：最快的工人单干整座山 `{min(workerTimes)} × (1+{mountainHeight}) × {mountainHeight} // 2` = =={right}==',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，答案还在区间里，继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}`：区间收成一个点，结束'),
        'mid = ': '试探时间 `mid = ({B.left} + {B.right}) // 2` = =={mid}==：够不够把山降完？',
        'h += int': '工人 `t={t}`：解 `x(x+1)/2 ≤ {mid}/{t}`，最多降 `int(sqrt({mid}*2/{t}+0.25)-0.5)` 米，累计 `h` = =={h}==',
        'if h < mountainHeight': lambda S, B, r: (f'`h = {S.h} < {S.mountainHeight}`：时间不够 → 答案在 mid 右边' if S.h < S.mountainHeight
                                                  else f'`h = {S.h} ≥ {S.mountainHeight}`：时间够了 → mid 可能就是答案，往左找更小的'),
        'left = mid + 1': '`mid` 不够，丢掉它：`left = {left}`',
        'right = mid': '`mid` 够用，保留它：`right = {right}`（不能 -1，它可能就是答案）',
        'return left': '`left` 就是最少秒数 ==`{left}`==',
    },
    cards=dict(
        one_liner='时间越多，降得越多，二分「所需时间」',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['`workerTimes[i]` = 工人 i 降 1 米的秒数，降 `x` 米要 `t·(1+2+…+x)` 秒',
                 '工人同时工作，求把山降到 0 的最少秒数',
                 '示例：`mountainHeight = 4, workerTimes = [2,1,1]` → `3`'],
        quote='时间过去越久，工人们可以降低的山的总高度就越多，符合二分的性质，因此在这里可以二分将山的高度降低到0所需的时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['下界 `1`；上界取最快的工人单干整座山：`min(t) × (1+H) × H // 2`',
              '给定时间 `mid`，工人 t 降 x 米要满足 `t·x(x+1)/2 ≤ mid`',
              '解 `x² + x ≤ 2·mid/t` 得 `x ≤ sqrt(2·mid/t + 0.25) − 0.5`，向下取整',
              '总高度够就收右边界，不够就抬左边界'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`h >= mountainHeight` 时 `right = mid`，不要 -1',
                 '原文用浮点 `sqrt`，数很大时有精度风险；灵神用整数 `isqrt` 更稳',
                 '运行时 `sqrt` 需从 `math` 导入（原文省略了 import）'],
    ),
)
