def _rng(S):
    if 'left' not in S or 'right' not in S:
        return '二分答案：答案 t 越大，能修的车越多'
    return f"开区间 `({S['left']}, {S['right']})`：答案在 ==right== 一侧，left 一定不行"


def _cnt(S):
    if 'mid' not in S or 'ranks' not in S:
        return ''
    mid = S['mid']
    parts = [f"r={r}: {isqrt(mid // r)}" for r in S['ranks']]
    tot = sum(isqrt(mid // r) for r in S['ranks'])
    return f"`t = {mid}` 时各人能修：{'，'.join(parts)} → 共 =={tot}== / 需要 {S['cars']}"


CONFIG = dict(
    num=2594, title='修车的最少时间', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 开区间',
    tags=['灵神题单·二分算法', '难度分 1915'],
    code='''
class Solution:
    def repairCars(self, ranks: List[int], cars: int) -> int:
        left = 0
        right = min(ranks) * cars * cars
        while left + 1 < right:  # 开区间
            mid = (left + right) // 2
            if sum(isqrt(mid // r) for r in ranks) >= cars:
                right = mid  # 满足要求
            else:
                left = mid
        return right  # 最小的满足要求的值
''',
    call='Solution().repairCars([4,2,3,1], 10)',
    expect=16,
    views=[
        dict(type='array', var='ranks', label='ranks（能力值，越小修得越快）', pointers={}, h=220, cell=110),
        dict(type='text', h=110, size=30, fn=_rng),
        dict(type='text', h=170, size=30, fn=_cnt),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', ('cars', 'cars', 'yellow')],
    captions={
        'left = 0': '开区间左端点 `left = 0`：0 分钟一定修不完',
        'right = min': '右端点 `right = min(ranks) × cars² = {right}`：最快的人一个人修完全部，一定满足',
        'while left + 1 < right': lambda S, B, r: (f'`{S.left} + 1 < {S.right}`，开区间里还有数 → 继续二分'
                                                   if S.left + 1 < S.right else f'`{S.left} + 1 >= {S.right}`：开区间空了 → 结束'),
        'mid = ': '取中间的时间 `mid = ({left} + {right}) // 2 = {mid}`',
        'if sum(': lambda S, B, r: (f'`t = {S.mid}`：每人修 `isqrt(t // r)` 辆，合计 `{sum(isqrt(S.mid // x) for x in S.ranks)}` '
                                    f'{">=" if sum(isqrt(S.mid // x) for x in S.ranks) >= S.cars else "<"} `{S.cars}` → '
                                    f'{"修得完" if sum(isqrt(S.mid // x) for x in S.ranks) >= S.cars else "修不完"}'),
        'right = mid': '`{mid}` 分钟够用 → 答案 ≤ mid，`right` 收到 =={right}==',
        'left = mid': '`{mid}` 分钟不够 → 答案 > mid，`left` 提到 =={left}==',
        'return right': '`right` 就是最小的满足要求的时间：=={right}==',
    },
    cards=dict(
        one_liner='先猜时间 t，数一数每个人能修几辆，再二分',
        complexity='时间 `O(n·log(m·c²))`，空间 `O(1)`',
        problem=['`ranks[i]` 是能力值：能力值 `r` 的人修 `n` 辆车要 `r·n²` 分钟',
                 '所有人同时开工，求修完 `cars` 辆车的最少时间',
                 '示例：`ranks=[4,2,3,1]`，`cars=10` → `16`'],
        quote='如果已知修车的时间 t，我们可以算出每个人在 t 分钟内能修好多少辆车。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`r·n² <= t` 解得 `n <= sqrt(t / r)`，每人最多修 `floor(sqrt(t/r))` 辆',
              '把大家的辆数加起来 `>= cars` 就说明 t 够用；t 越大越容易，==有单调性==',
              '上界取 `min(ranks)·cars²`：最快的人独自修完；开区间写法，check 为真就更新 right'],
        summary=['时间 `O(n log(m c²))`；灵神还给了优化：用 Counter 合并相同能力值，每次最多 100 种',
                 '`isqrt(mid // r)`：整数开方，不会有浮点误差（在 2^53 内）',
                 '开区间写法：check(mid) 为真更新的是谁，最后就返回谁',
                 '另一种写法：`bisect_left(range(...), cars, key=s)` 一行搞定'],
    ),
)
