D, R = [3, 1], [2, 3]
HOURS = 8


def _grid(S):
    r1, r2 = R
    return [['充' if h % r1 == 0 else '' for h in range(1, HOURS + 1)],
            ['充' if h % r2 == 0 else '' for h in range(1, HOURS + 1)],
            ['都充' if h % r1 == 0 and h % r2 == 0 else '' for h in range(1, HOURS + 1)]]


def _gcol(S, i, j, v):
    if not v:
        return None
    return 'red' if i < 2 else 'purple'


def _top(S):
    if isinstance(S['_inner'].get('r'), int) and isinstance(S['_inner'].get('d'), int):
        d, r = S['_inner']['d'], S['_inner']['r']
        return f"`f({d}, {r})`：每 `{r}` 小时只能工作 `{r - 1}` 小时，充电 `floor(({d}−1)/({r}−1)) = {(d - 1) // (r - 1)}` 次"
    return '三个必要条件：`d1 ≤ t − floor(t/r1)`、`d2 ≤ t − floor(t/r2)`、`d1+d2 ≤ t − floor(t/L)`'


def _fcap(S, B, ret):
    d, r = S.d, S.r
    k = (d - 1) // (r - 1)
    if d == D[0] + D[1] and r != R[0] and r != R[1]:
        who = '合计条件：两架一共 `d1+d2` 次，只有 `L` 的倍数时刻都不能送'
    elif (d, r) == (D[0], R[0]):
        who = 'A 的条件：A 只能用不充电的时间'
    else:
        who = 'B 的条件：B 只能用不充电的时间'
    return f'{who} → `{d} + ({d}−1)//({r}−1) = {ret}`（中途==充电 {k} 次==）'


CONFIG = dict(
    num=3733, title='完成所有送货任务的最少时间', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='三个不等式 · 数学公式',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 2513'],
    code='''
class Solution:
    def minimumTime(self, d: List[int], r: List[int]) -> int:
        d1, d2 = d
        r1, r2 = r
        l = lcm(r1, r2)

        def f(d: int, r: int) -> int:
            return d + (d - 1) // (r - 1)

        return max(f(d1, r1), f(d2, r2), f(d1 + d2, l))
''',
    setup='from math import lcm  # LeetCode 环境预置',
    call=f'Solution().minimumTime({D}, {R})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='table', var=_grid, label=f'第 1–{HOURS} 小时的充电情况（d = {D}, r = {R}）', h=260,
             rows=['A 充电', 'B 充电', '都充电'], cols=[str(h) for h in range(1, HOURS + 1)], color=_gcol, cell=90),
        dict(type='text', size=26, h=150, fn=lambda S: ('只能用 A：B 充电的时刻；只能用 B：A 充电的时刻' if 'l' not in S else
             f"`L = lcm({S['r1']}, {S['r2']}) = {S['l']}`：只有 `L` 的倍数时刻两架==都在充电==，这时谁也送不了")),
        dict(type='calls', h=120),
    ],
    watch=['d1', 'd2', 'r1', 'r2', ('l', 'l', 'purple')],
    captions={
        'd1, d2 = d': '`d1 = {d1}`、`d2 = {d2}`：两架无人机各自要送的次数',
        'r1, r2 = r': '`r1 = {r1}`、`r2 = {r2}`：A 在 `r1` 的倍数时刻充电，B 在 `r2` 的倍数时刻充电',
        'l = lcm': '`l = lcm({r1}, {r2}) = {l}`：A、B 同时充电的周期',
        'def f(': '`f(d, r)`：满足 `t − floor(t/r) ≥ d` 的最小 `t`',
        'return d + (d - 1)': _fcap,
        'return max(': '依次算出三个不等式各自的最小 `t`，==取最大值才能同时满足==',
    },
    cards=dict(
        result='`max(5, 1, 4) = 5`：A 的条件最紧，最少需要 ==5 小时==',
        one_liner='三个不等式各求最小 t，取最大值；每个 t = d + (d−1)//(r−1)',
        complexity='时间 `O(log max(r1, r2))`（算 lcm），空间 `O(1)`',
        problem=['两架无人机分别要送 `d1`、`d2` 次，每次 1 小时，同一小时只能一架送',
                 '无人机 `i` 在 `r_i` 的倍数小时充电，不能送货；求最少总时间',
                 '示例：`d = [3,1], r = [2,3]` → `5`'],
        quote='对于给定的 (d,r)，最小的 t 等于 d 加上充电时长……每经过 r 小时，就需要花 1 小时充电（最后一段不需要充电）。或者说，==每 r 小时只能工作 r−1 小时==。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['A 能用的时间 `t − floor(t/r1)` 要 `≥ d1`，B 同理 `≥ d2`',
              '两架合计 `d1+d2` 不超过「非同时充电」的时间 `t − floor(t/L)`',
              '三个不等式==必要且充分==，各解出最小 `t` 再取 max'],
        summary=['时间 `O(log max(r1, r2))`，空间 `O(1)`',
                 '`d` 小时分成 `ceil(d/(r−1))` 段，充电次数是段数减一 `= (d−1)//(r−1)`',
                 '第三个条件用的是 `lcm(r1, r2)`，不是 `r1 * r2`',
                 '方法一：二分答案 `t`，开区间 `(d1+d2−1, 2(d1+d2)−1)`，`check` 就是这三个不等式'],
    ),
)
