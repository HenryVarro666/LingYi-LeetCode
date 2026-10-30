import math as _m

_P = [True] * 100
_P[1] = False   # 代码里 is_prime[0] 仍是 True，所以 0 也走不了
for _i in range(2, 100):
    if _P[_i]:
        for _j in range(_i * _i, 100, _i):
            _P[_j] = False
N0, M0 = 10, 12


def _fin(v):
    return isinstance(v, int) and v < 10 ** 6


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    dis = S.get('dis')
    x = S.get('x') if 'dis_x' in S else None
    y = S.get('y') if 'y' in S and S.get('_line') is not None else None
    cv.text((x0 + 18, y0 + 4), '数字 0~99 排成表（红 = 质数不能走，蓝 = 当前 x，橙 = 暂定 dis，绿 = 已出堆定下）', 20, T['muted'], bold=True)
    cell = min((x1 - x0 - 60) / 10, (y1 - y0 - 60) / 10)
    sx = x0 + ((x1 - x0) - cell * 10) / 2
    sy = y0 + 46
    for v in range(100):
        r, c = divmod(v, 10)
        X, Y = sx + c * cell, sy + r * cell
        d = dis[v] if dis is not None else None
        if _P[v]:
            fill, tc = (74, 40, 48), T['dim']
        elif v == x:
            fill, tc = T['blue'], T['bg']
        elif y is not None and v == y and 'new_d' in S and S['new_d'] < (d if d is not None else 10 ** 9) + 1 and v == y:
            fill, tc = T['yellow'], T['bg']
        elif d is not None and _fin(d) and 'dis_x' in S and d <= S['dis_x']:
            fill, tc = T['green'], T['bg']
        elif d is not None and _fin(d):
            fill, tc = T['orange'], T['bg']
        else:
            fill, tc = T['panel2'], T['muted']
        cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6)
        cv.text((X + cell / 2, Y + cell * 0.36), v, int(cell * 0.38), tc, anchor='mm', bold=True, mono=True)
        if d is not None and _fin(d) and not _P[v]:
            cv.text((X + cell / 2, Y + cell * 0.74), d, int(cell * 0.26), tc, anchor='mm', mono=True)
        if v == M0:
            cv.rect((X, Y, X + cell, Y + cell), outline=T['pink'], width=4, r=8)
        if v == N0:
            cv.rect((X, Y, X + cell, Y + cell), outline=T['yellow'], width=4, r=8)


def _txt(S, B):
    if 'dis_x' not in S:
        return f'从 `n = {N0}` 出发，目标 `m = {M0}`；途中每个数都不能是质数，代价 = 经过的所有数之和'
    s = f"弹出 `({S['dis_x']}, {S['x']})`：已花代价 `{S['dis_x']}`（含起点和 `{S['x']}`）"
    return s


CONFIG = dict(
    num=3377, title='使两个整数相等的数位操作', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='Dijkstra · 数位当边',
    tags=['灵神题单·图论算法', '难度分 2186'],
    code='''
class Solution:
    def minOperations(self, n: int, m: int) -> int:
        if is_prime[n] or is_prime[m]:
            return -1
        len_n = len(str(n))
        dis = [inf] * (10 ** len_n)
        dis[n] = n
        h = [(n, n)]
        while h:
            dis_x, x = heappop(h)
            if x == m:
                return dis_x
            if dis_x > dis[x]:
                continue
            v = x
            pow10 = 1
            while v:
                v, d = divmod(v, 10)
                if d > 0:  # 减少
                    y = x - pow10
                    if not is_prime[y] and (new_d := dis_x + y) < dis[y]:
                        dis[y] = new_d
                        heappush(h, (new_d, y))
                if d < 9:  # 增加
                    y = x + pow10
                    if not is_prime[y] and (new_d := dis_x + y) < dis[y]:
                        dis[y] = new_d
                        heappush(h, (new_d, y))
                pow10 *= 10
        return -1
''',
    setup='''
MX = 10000
is_prime = [True] * MX
is_prime[1] = False
for i in range(2, MX):
    if is_prime[i]:
        for j in range(i * i, MX, i):
            is_prime[j] = False
''',
    call=f'Solution().minOperations({N0}, {M0})',
    expect=85,
    max_steps=68,
    skip=['v = x', 'pow10 = 1', 'pow10 *= 10'],
    views=[
        dict(type='text', fn=_txt, h=44, size=22),
        dict(type='custom', draw=_draw, h=540),
        dict(type='heap', var='h', label='h（最小堆，元素 = (已花代价, 当前数)）', h=95, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('dis_x', 'dis_x', 'blue'), ('x', 'x', 'blue'), ('d', 'd'), ('y', 'y', 'yellow'), ('new_d', 'new_d', 'orange')],
    captions={
        'if is_prime[n]': '起点或终点是质数：==任意时刻都不能是质数==，直接 `-1`（示例 3）',
        'len_n =': '两个数位数相同，状态都在 `{len_n}` 位数以内',
        'dis = [inf]': '`n` 位数最多 `10^len_n` 个状态，`dis[x]`：从 n 变到 x 的最小代价，先设 ∞',
        'dis[n] = n': '起点本身也要计入代价：`dis[{n}] = {n}`',
        'h = [(n, n)]': '堆里放 `(代价, 数)`，起点入堆',
        'dis_x, x = heappop': '弹出代价最小的数 `x = {x}`（代价 `{dis_x}`）：边权 y > 0，它的最短路已确定',
        'if x == m': lambda S, B, r: f'`x == m = {S.m}`：==首次出堆就是最短==，返回 `{S.dis_x}`' if S.x == S.m else '还没到 m，继续',
        'return dis_x': '到达目标，返回最小代价 `{ret}`',
        'if dis_x > dis[x]': lambda S, B, r: f'`{S.dis_x} > dis[{S.x}] = {S.dis[S.x]}`：==x 之前出堆过==，旧记录，跳过' if S.dis_x > S.dis[S.x] else f'`{S.dis_x} == dis[{S.x}]`：首次出堆，去枚举它的邻居',
        'v, d = divmod': '取出一位 `d = {d}`，这位的权值是 `pow10 = {pow10}`',
        'if d > 0': lambda S, B, r: f'这位是 `{S.d}`，大于 0，==可以减 1==' if S.d > 0 else f'这位是 `0`，不能再减',
        'y = x - pow10': lambda S, B, r: f"这一位减 1：`y = {S.x} - {S.pow10}` = =={S.y}=={'（质数，不能走）' if _P[S.y] else ''}",
        'if d < 9': lambda S, B, r: f'这位是 `{S.d}`，小于 9，==可以加 1==' if S.d < 9 else f'这位是 `9`，不能再加',
        'y = x + pow10': lambda S, B, r: f"这一位加 1：`y = {S.x} + {S.pow10}` = =={S.y}=={'（质数，不能走）' if _P[S.y] else ''}",
        'if not is_prime[y]': lambda S, B, r: (f'`{S.y}` 是质数 → 不能走' if _P[S.y] else (f'`new_d = {S.dis_x} + {S.y} = {S.dis_x + S.y}`，对比 `dis[{S.y}] = {S.dis[S.y] if S.dis[S.y] < 10**6 else "∞"}` → ' + ('==更小，更新==' if S.dis_x + S.y < S.dis[S.y] else '不更小，不更新'))),
        'dis[y] = new_d': '更新 `dis[{y}] = {new_d}`',
        'heappush': '`({new_d}, {y})` 入堆（懒更新，旧记录以后会被跳过）',
    },
    cards=dict(
        one_liner='每个非质数是一个点，操作一次是一条边，边权 = 新数',
        complexity='时间 `O(M log M)`，空间 `O(M)`',
        problem=['`n` 和 `m` 位数相同；每次把 `n` 的某位加 1（非 9）或减 1（非 0）',
                 '`n` 任何时刻都不能是质数；代价 = 变化过程中==所有值之和==',
                 '示例：`n = 10, m = 12` → `85`（10→20→21→22→12）；变不过去返回 `-1`',
                 '本视频用示例 1，数字都在 0~99 内'],
        quote='对每个非质数 x，在 x 和 x 操作一次得到的数 y（非质数）之间连一条有向边，边权为 y。答案就是从 n 到 m 的最短路长度，加上 n。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把「数」看成点，「改一位」看成边：==边权是改完的数 y==，都是正数 → Dijkstra',
              '不用真连边：出堆时按位拆数，现算 `x ± pow10`',
              '起点 `n` 本身也计入代价，所以 `dis[n] = n`'],
        summary=['时间 `O(M log M)`，`M = n log n`；筛质数的预处理没计入',
                 '本视频把埃氏筛放在运行前准备（`is_prime` 表），代码面板只显示 Dijkstra 部分',
                 '`is_prime[0]` 在筛里仍是 True，所以 0 也不能走；易错：`dis[n] = n`，不是 0；`n` 或 `m` 是质数直接 `-1`',
                 '`new_d := dis_x + y` 用了海象运算符，Python 3.8+',
                 '同类：Dijkstra 在隐式图上，边现算而不建图'],
    ),
)
