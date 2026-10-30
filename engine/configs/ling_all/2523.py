LO, HI = 10, 19
PR = [p for p in range(2, 80) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = HI - LO + 1
    cell = min(100, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys, ch = y0 + 190, cell * 0.9
    cv.text((x0 + 18, y0 + 4), f'数轴 [{LO}, {HI}]（绿 = 质数，由筛法预处理好的 primes 表给出）', 24, T['muted'], bold=True)

    def cx(v):
        return sx + (v - LO) * cell + cell / 2

    live = 'i' in S and 'p' in S
    i = S.get('i') if live else None
    a = PR[i] if i is not None and 0 <= i < len(PR) else None
    b = PR[i + 1] if i is not None and 0 <= i + 1 < len(PR) else None
    p, q = (S['p'], S['q']) if live else (-1, -1)
    for v in range(LO, HI + 1):
        X = sx + (v - LO) * cell
        pr = v in PR
        fill = T['green'] if pr else T['panel2']
        if pr and (v == a):
            fill = T['blue']
        if pr and (v == b) and live and b <= HI:
            fill = T['pink']
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), v, 34, T['bg'] if pr else T['dim'], anchor='mm', bold=True)
    # 指针
    if a is not None and LO <= a <= HI:
        cv.tri_up(cx(a), ys + ch + 22, 10, T['blue'])
        cv.text((cx(a), ys + ch + 38), 'primes[i]', 22, T['blue'], anchor='mt', bold=True)
    if b is not None:
        if LO <= b <= HI:
            cv.tri_up(cx(b), ys + ch + 22, 10, T['pink'])
            cv.text((cx(b), ys + ch + 38 + (30 if a is not None and a == b else 0)), 'primes[i+1]', 22, T['pink'], anchor='mt', bold=True)
        else:
            cv.text((x1 - 24, ys + ch + 38), f'primes[i+1] = {b} 超出 right', 22, T['pink'], anchor='ra', bold=True)
    # 当前最优间隙
    if p > 0 and LO <= p <= q <= HI:
        yy = ys - 28
        cv.line([(cx(p), yy), (cx(q), yy)], T['yellow'], 5)
        cv.line([(cx(p), yy), (cx(p), yy + 18)], T['yellow'], 5)
        cv.line([(cx(q), yy), (cx(q), yy + 18)], T['yellow'], 5)
        cv.text(((cx(p) + cx(q)) / 2, yy - 8), f'当前最优 [{p}, {q}]，间隙 {q - p}', 24, T['yellow'], anchor='mb', bold=True)
    # 这一步正在比较的间隙
    if a is not None and b is not None and a >= LO and b <= HI:
        yy = ys + ch + 120
        cv.line([(cx(a), yy), (cx(b), yy)], T['cyan'], 4)
        cv.text(((cx(a) + cx(b)) / 2, yy + 8), f'候选间隙 {b} − {a} = {b - a}', 24, T['cyan'], anchor='mt', bold=True)


def _cmp(S, B, ret):
    i = S.i
    a, b = PR[i], PR[i + 1]
    if B.p < 0:
        return f'`p < 0`：还没有答案，直接记下第一对 `[{a}, {b}]`（间隙 {b - a}）'
    if b - a < B.q - B.p:
        return f'间隙 `{b} − {a} = {b - a}` < 当前最小 `{B.q} − {B.p} = {B.q - B.p}` → ==更新答案== 为 `[{a}, {b}]`'
    return f'间隙 `{b} − {a} = {b - a}` 不小于当前最小 `{B.q - B.p}`（相等也不换，保证 `nums1` 最小）→ 不更新'


CONFIG = dict(
    num=2523, title='范围内最接近的两个质数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='线性筛预处理 · 二分 + 相邻质数枚举',
    tags=['灵神题单·数学算法', '难度分 1650'],
    code='''
MX = 10 ** 6 + 1
primes = []
is_prime = [True] * MX
for i in range(2, MX):
    if is_prime[i]:
        primes.append(i)
    for p in primes:
        if i * p >= MX: break
        is_prime[i * p] = False
        if i % p == 0: break
primes.extend((MX, MX))  # 保证下面下标不会越界

class Solution:
    def closestPrimes(self, left: int, right: int) -> List[int]:
        p = q = -1
        i = bisect_left(primes, left)
        while primes[i + 1] <= right:
            if p < 0 or primes[i + 1] - primes[i] < q - p:
                p, q = primes[i], primes[i + 1]
            i += 1
        return [p, q]
''',
    call='Solution().closestPrimes(10, 19)',
    expect=[11, 13],
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=['left', 'right', ('i', 'i', 'blue'), ('p', 'p', 'yellow'), ('q', 'q', 'yellow')],
    captions={
        'p = q = -1': '`[p, q]` 记录当前最优的相邻质数对，`-1` 表示还没有。质数表 `primes` 已经由上面的线性筛预处理好',
        'bisect_left(primes, left)': lambda S, B, r: f'二分找 `primes` 里第一个 `>= {S.left}` 的质数：`i = {S.i}`，即 `primes[{S.i}] = {PR[S.i]}`',
        'while primes[i + 1] <= right': lambda S, B, r: (f'`primes[{S.i + 1}] = {PR[S.i + 1]} <= {S.right}`：下一个质数还在范围内 → 看这对相邻质数' if PR[S.i + 1] <= S.right
                                                     else f'`primes[{S.i + 1}] = {PR[S.i + 1]} > {S.right}`：下一个质数超出范围 → 枚举结束（末尾补的 `MX` 让这里不会越界）'),
        'if p < 0': _cmp,
        'p, q = ': '记下新的最优对：`[p, q] = [{p}, {q}]`',
        'i += 1': '往后挪一格，比较下一对相邻质数：`i` → {i}',
        'return': '范围内最小间隙的质数对：=={ret}==',
    },
    cards=dict(
        one_liner='先筛出质数表，再扫一遍相邻质数找最小间隙',
        complexity='时间 `O(right)`（忽略预处理），空间 `O(1)`',
        problem=['在 `[left, right]` 内找两个质数 `nums1 < nums2`，使差最小',
                 '差相同取 `nums1` 最小的一对；不存在则返回 `[-1, -1]`',
                 '示例：`left=10, right=19` → `[11,13]`（`[17,19]` 间隙相同但更靠后）'],
        quote='分两步：1. 筛质数……2. 找 [left,right] 范围内的最小质数间隙（prime gap），暴力枚举范围内的所有相邻质数即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最近的两个质数一定是质数表里相邻的两项，不用枚举所有数对',
              '用二分找到第一个 `>= left` 的质数，然后往后一个个比较相邻的间隙',
              '表尾额外塞两个 `10^6+1`，`primes[i+1]` 永远不会越界'],
        summary=['预处理一次线性筛 `O(U)`；查询只扫范围内的质数，约 `O(right/log right)`',
                 '间隙用严格 `<` 更新：相同间隙保留靠前的一对（题目要求 `nums1` 最小）',
                 '没有质数对时 `p, q` 保持 `-1`，直接返回 `[-1, -1]`',
                 '题解另给了埃氏筛版本（只是预处理不同），视频用最后的线性筛写法；预处理在代码最上方，不单步演示'],
    ),
)
