D, R = [3, 1], [2, 3]


def _cand(S):
    if 'right' not in S or 'o' not in S:
        return []
    return list(range(0, (D[0] + D[1]) * S['l'] + 1))  # 下标 = 小时数，0 只占位


def _ccol(S, i, v):
    if 'left' not in S:
        return None
    if v == 0:
        return None
    if v < S['left']:
        return 'red'
    if v >= S['right'] and S['left'] < S['right']:
        return 'green'
    if S['left'] == S['right'] and v == S['left']:
        return 'green'
    return None


def _cycle(S):
    if 'o' not in S:
        return []
    l = S['l']
    row = []
    for h in range(1, l):
        a, b = h % R[0] == 0, h % R[1] == 0
        row.append('只B' if a else '只A' if b else '都可')
    return [row]


def _cyc_col(S, i, j, v):
    return {'只A': 'blue', '只B': 'pink', '都可': 'green'}.get(v)


def _top(S):
    if 'need_both' in S and 'mid' in S and S['_line'] in (21, 22, 23, 24, 25):
        nb = S['need_both']
        cap = S['both'] * S['rnd'] + S['t'] - S['t'] // R[1] - S['t'] // R[0]
        return f"`mid = {S['mid']}`：要占用共用时段 `{nb[0]} + {nb[1]} = {nb[0] + nb[1]}`，共用时段有 `{cap}` 个"
    if 'o' in S:
        return f"周期 `l = {S['l']}` 的前 `l−1` 小时：只 A `o[0] = {S['o'][0]}`、只 B `o[1] = {S['o'][1]}`" + (f"、都可 `{S['both']}`" if 'both' in S else '')
    return '以 `lcm(r1, r2)` 为周期：周期内不会出现两台同时充电'


def _if(S, B, ret):
    nb = S.need_both
    cap = S.both * S.rnd + S.t - S.t // R[1] - S.t // R[0]
    if nb[0] + nb[1] <= cap:
        return f'`{nb[0]} + {nb[1]} ≤ {cap}`：共用时段够用 → `{S.mid}` 小时==可以完成=='
    return f'`{nb[0]} + {nb[1]} > {cap}`：共用时段不够 → `{S.mid}` 小时==完成不了=='


CONFIG = dict(
    num=3733, title='完成所有送货任务的最少时间', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='lcm 周期分段 · 二分答案',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 2513'],
    code='''
class Solution(object):
    def minimumTime(self, d, r):
        
        x, y = r
        l = x * y
        while y:
            x, y = y, x % y
        
        l //= x

        o = [(l - 1) // r[1], (l - 1) // r[0]]
        both = l - 1 - o[0] - o[1]
        
        left = 1
        right = (d[0] + d[1]) * l
        while left < right:
            mid = (left + right) // 2
            rnd = mid // l
            t = mid % l
            need_both = [max(0, d[0] - o[0] * rnd - t // r[1]), max(0, d[1] - o[1] * rnd - t // r[0])]
            if need_both[0] + need_both[1] <= both * rnd + t - t // r[1] - t // r[0]:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call=f'Solution().minimumTime({D}, {R})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=25, h=80),
        dict(type='table', var=_cycle, label='一个周期内第 1…l−1 小时谁能送货', h=150, rows=['可送'],
             cols=lambda S: [str(h) for h in range(1, S['l'])] if 'o' in S else [], color=_cyc_col, cell=88),
        dict(type='array', var=_cand, label='候选总时间（红 = 不可行，绿 = 可行）', cell=29, index=False,
             color=_ccol, pointers={'left': 'red', 'mid': 'yellow', 'right': 'green'}, dim=lambda S, i, v: i == 0, h=200),
    ],
    watch=[('left', 'left', 'red'), ('mid', 'mid', 'yellow'), ('right', 'right', 'green'),
           'rnd', 't', 'need_both'],
    captions={
        'x, y = r': '先求 `lcm(r1, r2)`：`x = {x}`, `y = {y}`',
        'l = x * y': '`l = x * y = {l}`，再除以 gcd',
        'while y:': lambda S, B, r: ('辗转相除继续' if S.y else f'`y = 0`：gcd = `{S.x}`'),
        'x, y = y, x % y': '辗转相除：`x = {x}`, `y = {y}`',
        'l //= x': '`l = lcm = {l}`：以它为周期，==周期内不会两台同时充电==',
        'o = [': '`o[0] = (l−1)//r2 = {o[0]}`：B 充电时只有 A 能送；`o[1] = (l−1)//r1 = {o[1]}`',
        'both = l - 1': '`both = {l}−1−{o[0]}−{o[1]} = {both}`：两台都能送的时段',
        'left = 1': '二分总时间：下界 `left = 1`',
        'right = (d[0]': '上界给大一点：每个周期只送一次也够 → `right = (d1+d2)·l = {right}`',
        'while left < right': lambda S, B, r: (f'区间 `[{S.left}, {S.right}]` 还有多个候选，继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}`，二分结束'),
        'mid = (left': '猜 `mid = ({left} + {right}) // 2 = {mid}` 小时',
        'rnd = mid // l': '经过完整周期 `rnd = {mid} // {l} = {rnd}`',
        't = mid % l': '剩余时间 `t = {mid} % {l} = {t}`',
        'need_both = [': '两台都==先用自己独占的时段==，不够的才占共用时段：`need_both = {need_both}`',
        'if need_both[0]': _if,
        'right = mid': '可行 → 答案 `≤ {mid}`：`right = {right}`',
        'left = mid + 1': '不可行 → 答案 `> {mid}`：`left = {left}`',
        'return left': '最少需要 =={ret}== 小时',
    },
    cards=dict(
        one_liner='以 lcm 为周期，把时间分成只 A、只 B、都可三类，二分总时间',
        complexity='时间 `O(log(r1·r2) + log((d1+d2)·l))`，空间 `O(1)`',
        problem=['两架无人机分别要送 `d1`、`d2` 次，每次 1 小时，同一小时只能一架送',
                 '无人机 `i` 在 `r_i` 的倍数小时充电，不能送货；求最少总时间',
                 '示例：`d = [3,1], r = [2,3]` → `5`'],
        quote='两台无人机都应该==优先使用只有这台无人机可以送货的时段==，不够的时候再通过占用两台都可以送货的时段来进行补充。',
        quote_src='—— yiduobo 题解原文',
        idea=['周期 `l = lcm(r1, r2)` 内（前 `l−1` 小时）：只 A、只 B、都可三类时段',
              '对 `mid`：完整周期 `rnd` 个 + 剩余 `t` 小时，分别数三类时段',
              '独占时段不够的部分加起来 `≤` 共用时段，就可行'],
        summary=['时间 `O(log(r1·r2) + log((d1+d2)·l))`，空间 `O(1)`',
                 '周期最后一小时是 `l` 的倍数，两台都在充电，所以只数前 `l−1` 小时',
                 '上界取 `(d1+d2)·l` 偏大但安全，二分只多几轮',
                 '原文为 Python 2 风格（已用 `//`），代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神直接列三个不等式，推出 `d + (d−1)//(r−1)` 的公式'],
    ),
)
