import math as _m


def _rng(S):
    if 'left' not in S or 'right' not in S:
        return '二分时间：时间越长，修好的车越多'
    return f"答案在闭区间 `[{S['left']}, {S['right']}]` 内，left == right 时就是答案"


def _cnt(S):
    if 'mid' not in S or 'ranks' not in S:
        return ''
    mid = S['mid']
    done = S.get('cnt', 0) if 'r' in S else 0
    parts = [f"r={r}: {int(_m.sqrt(mid * 1.0 / r))}" for r in S['ranks']]
    tot = sum(int(_m.sqrt(mid * 1.0 / r)) for r in S['ranks'])
    return f"`mid = {mid}` 时各人能修：{'，'.join(parts)} → 合计 =={tot}== / 需要 {S['cars']}"


CONFIG = dict(
    num=2594, title='修车的最少时间', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 累加 sqrt(mid/r)',
    tags=['灵神题单·二分算法', '难度分 1915'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def repairCars(self, ranks, cars):

        n = len(ranks)

        left = 1
        right = (cars // n + 1) ** 2 * max(ranks)
        while left < right:
            mid = (left + right) // 2
            cnt = 0
            for r in ranks:
                cnt += int(sqrt(mid * 1.0 / r))
            
            if cnt >= cars:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().repairCars([4,2,3,1], 10)',
    expect=16,
    views=[
        dict(type='array', var='ranks', label='ranks（能力值）', pointers={}, h=230, cell=110),
        dict(type='text', h=110, size=30, fn=_rng),
        dict(type='text', h=170, size=30, fn=_cnt),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', ('cnt', 'cnt', 'green'), ('cars', 'cars', 'yellow')],
    skip=['for r in ranks', 'n = len'],
    captions={
        'n = len': '`n = {n}` 个工人',
        'left = 1': '下界 `left = 1`',
        'right = (': '上界：假设活平均分给每人，每人约 `cars//n + 1 = {cars // n + 1}` 辆，最慢的人 `max(ranks)` 要 `r·n²` → `right = {right}`',
        'while left < right': lambda S, B, r: (f'`{S.left} < {S.right}`，区间没缩成一点 → 继续' if S.left < S.right
                                               else f'`left = right = {S.left}` → 区间缩成一点，结束'),
        'mid = ': '`mid = ({left} + {right}) // 2 = {mid}`：试试 {mid} 分钟够不够',
        'cnt = 0': '`cnt` 清零，累计 {mid} 分钟内能修好的车',
        'cnt += ': lambda S, B, ret: f'能力值 `{S.r}`：`sqrt({S.mid} / {S.r}) = {_m.sqrt(S.mid * 1.0 / S.r):.2f}` 取整 → 修 `{int(_m.sqrt(S.mid * 1.0 / S.r))}` 辆，`cnt = {S.cnt}`',
        'if cnt >= cars': lambda S, B, r: (f'`cnt = {S.cnt}` {">=" if S.cnt >= S.cars else "<"} `cars = {S.cars}` → '
                                           f'{"时间足够" if S.cnt >= S.cars else "时间不够"}'),
        'right = mid': '时间足够 → 答案 ≤ mid，`right = {right}`',
        'left = mid + 1': '时间不够 → 答案 > mid，`left = {left}`',
        'return left': '`left` 就是最少时间：=={left}==',
    },
    cards=dict(
        one_liner='时间越长修得越多：二分时间，逐个工人累加辆数',
        complexity='时间 `O(n·log(上界))`，空间 `O(1)`',
        problem=['能力值 `r` 的工人修 `n` 辆车要 `r·n²` 分钟，所有人同时开工',
                 '求修完 `cars` 辆车的最少时间',
                 '示例：`ranks=[4,2,3,1]`，`cars=10` → `16`'],
        quote='修车的时间越长，就有越多的车可以被修好，也就是说本题可以通过二分答案来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['对当前 `mid`，遍历每个工人：能力值 `r` 修 `sqrt(mid / r)` 辆（取整）',
              '累加得 `cnt`：`cnt >= cars` → 上界收到 mid；否则下界 `mid + 1`',
              '上界用 `(cars//n + 1)² × max(ranks)` 估计，闭区间 `left < right` 二分'],
        summary=['时间 `O(n·log(上界))`，空间 `O(1)`',
                 '原文为 Python 2 写法，`/` 整数除法已改为 `//`，`sqrt` 在 setup 里 `from math import sqrt`',
                 '`sqrt` 是浮点数，数值很大时有精度风险；灵神用 `isqrt` 更稳',
                 '对比灵神：灵神用开区间 + 上界 `min(ranks)·cars²`，这里是闭区间 + 平均估计的上界'],
    ),
)
