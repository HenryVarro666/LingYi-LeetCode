# ---- 折线图：横轴 = 车所在的加油站，纵轴 = 油量 s（从 0 号站出发、允许为负）。右半边是把数组复制一份后的折线，
# ---- 循环结束时画出来：总油量 >= 0 时复制段不会跌破谷底（示例 1），< 0 时会跌破（示例 2）
G1, C1 = [1, 2, 3, 4, 5], [3, 4, 5, 1, 2]
G2, C2 = [2, 3, 4], [3, 4, 3]
L_FOR, L_RET = 4, 10


def _prefix(gas, cost):
    P = [0]
    for g, c in zip(gas, cost):
        P.append(P[-1] + g - c)
    return P


def _npts(S, B):
    """折线已经画到第几个点（含起点）"""
    n = len(S['gas'])
    if 'i' not in S:
        return 1
    ln = S.get('_line')
    if ln == L_RET:
        return n + 1
    if ln == L_FOR:
        return S['i'] + 1 if ('i' not in B or B['i'] != S['i']) else n + 1
    return S['i'] + 2


def draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    gas, cost = S.get('gas'), S.get('cost')
    if gas is None:
        return
    n = len(gas)
    P = _prefix(gas, cost)
    k = _npts(S, B)
    done = k == n + 1 and S.get('_line') in (L_FOR, L_RET)
    copy = [P[n] + v for v in P]
    lo = min(P + copy + [0])
    hi = max(P + copy + [0])
    L, R = x0 + 70, x1 - 30
    top, bot = y0 + 70, y1 - 100
    sx = (R - L) / (2 * n)
    sy = (bot - top) / max(1, hi - lo)

    def pt(x, v):
        return L + x * sx, bot - (v - lo) * sy

    cv.text((x0 + 18, y0 + 4), '油量折线图（从 0 号站出发，允许为负）', 24, T['muted'], bold=True)
    # zero line + grid labels
    zx0, zy = pt(0, 0)
    cv.dashed((L, zy), (R, zy), T['dim'], 2)
    cv.text((L - 10, zy), '0', 20, T['muted'], anchor='rm', mono=True)
    for x in range(2 * n + 1):
        X, _ = pt(x, lo)
        cv.text((X, bot + 46), str(x % n), 18, T['dim'] if x > n else T['muted'], anchor='mt', mono=True)
    cv.text((pt(n, lo)[0] + (R - pt(n, lo)[0]) / 2, bot + 72), '复制的一段（gas + gas）', 18, T['dim'], anchor='mt')
    cv.line([(pt(n, lo)[0], top - 10), (pt(n, lo)[0], bot + 8)], T['border'], 2)
    # first half
    pts = [pt(x, P[x]) for x in range(k)]
    if len(pts) > 1:
        cv.line(pts, T['blue'], 4)
    mi = S.get('ans', 0)
    for x in range(k):
        X, Y = pts[x]
        isnew = x == k - 1 and not done and 'i' in S
        cv.d.ellipse((X - 7, Y - 7, X + 7, Y + 7), fill=T['yellow'] if isnew else T['blue'])
        if x:
            cv.text((X, Y - 12), str(P[x]), 19, T['text'], anchor='mb', bold=True)
    # valley marker
    if 'ans' in S:
        mi = S['ans']
        X, Y = pt(mi, P[mi])
        cv.d.ellipse((X - 14, Y - 14, X + 14, Y + 14), outline=T['green'], width=4)
        cv.text((X + 18, Y + 6), f'谷底 = {mi} 号站', 19, T['green'], anchor='lt', bold=True)
    if done:
        cpts = [pt(n + x, copy[x]) for x in range(n + 1)]
        bad = min(copy) < min(P)
        cc = T['red'] if bad else T['cyan']
        for a, b in zip(cpts, cpts[1:]):
            cv.dashed(a, b, cc, 3, 10, 6)
        for x in range(1, n + 1):
            X, Y = cpts[x]
            cv.d.ellipse((X - 5, Y - 5, X + 5, Y + 5), fill=cc)
        _, my = pt(0, min(P))
        cv.dashed((pt(mi, 0)[0], my), (R, my), T['green'], 2, 6, 6)
        msg = ('总油量 < 0：复制段跌破谷底 → 从谷底出发也会变负' if bad
               else '总油量 ≥ 0：从谷底往后，折线再也不会低于谷底')
        cv.text((R, top - 30), msg, 20, cc, anchor='ra', bold=True)


def _for(S, B, ret):
    if 'i' not in B or B.i != S.i:
        return f'在 `{S.i}` 号站：加油 `g = {S.g}`，开往 `{S.i + 1}` 号站耗油 `c = {S.c}`'
    return '一圈走完（油量允许为负，所以一定能“走完”）'


def _if(S, B, ret):
    if S.s < S.min_s:
        return f'`s = {S.s} < min_s = {S.min_s}`：==更低的谷底== → 记下来'
    return f'`s = {S.s} ≥ min_s = {S.min_s}`：不是新谷底'


def _ret(S, B, ret):
    if S.s < 0:
        return f'`s = {S.s} < 0`：gas 之和 < cost 之和，油不够跑一圈 → 返回 ==-1=='
    return f'`s = {S.s} ≥ 0`：已经在谷底了，怎么走都是向上 → 返回谷底 =={ret}== 号站'


CONFIG = dict(
    num=134, title='加油站', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='折线图 · 从油量最低点出发',
    tags=['面试经典150'],
    code='''
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        ans = min_s = s = 0  # s 表示油量，min_s 表示最小油量
        for i, (g, c) in enumerate(zip(gas, cost)):
            s += g - c  # 在 i 处加油，然后从 i 到 i+1
            if s < min_s:
                min_s = s  # 更新最小油量
                ans = i + 1  # 注意 s 减去 c 之后，汽车在 i+1 而不是 i
        # 循环结束后，s 即为 gas 之和减去 cost 之和
        return -1 if s < 0 else ans
''',
    call=f'[Solution().canCompleteCircuit({G1}, {C1}), Solution().canCompleteCircuit({G2}, {C2})]',
    expect=[3, -1],
    views=[
        dict(type='array', var='gas', label='gas（加油量）', cell=80, h=118, pointers={'i': 'blue'}),
        dict(type='array', var='cost', label='cost（开到下一站的耗油）', cell=80, h=118, index=False),
        dict(type='custom', draw=draw, h=440),
    ],
    watch=[('i', 'i', 'blue'), 'g', 'c', ('s', 's', 'yellow'), ('min_s', 'min_s', 'green'), ('ans', 'ans', 'green')],
    captions={
        'ans = min_s = s = 0': lambda S, B, r: ('假设从 0 号站出发，油量 `s = 0`；`min_s` 记最小油量，`ans` 记它出现在几号站'
                                                if S.gas == G1 else '示例 2：同样从 0 号站出发，画油量折线'),
        'for i, (g, c)': _for,
        's += g - c': '在 `{i}` 处加油再开到 `{i + 1}`：`s += {g} − {c}` → 油量 =={s}==',
        'if s < min_s': _if,
        'min_s = s': '更新最小油量：`min_s = {min_s}`',
        'ans = i + 1': '`ans = {i} + 1 = {ans}`：s 减去 c 之后，汽车在 ==i+1== 而不是 i',
        'return -1 if': _ret,
    },
    cards=dict(
        one_liner='已经在谷底了，怎么走都是向上',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['环路上 `n` 个加油站：在 `i` 站加油 `gas[i]`，开到 `i+1` 站耗油 `cost[i]`',
                 '油箱起始为空、容量无限；能绕一圈就返回出发站编号（唯一），否则返回 `-1`',
                 '示例 1：`gas = [1,2,3,4,5], cost = [3,4,5,1,2]` → `3`',
                 '示例 2：`gas = [2,3,4], cost = [3,4,3]` → `-1`（本视频两个都跑）'],
        quote='我们可以先计算从 0 号加油站出发的油量变化，然后从中找到==油量最低==时所处的加油站，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['画出从 0 号站出发的油量折线（允许为负）',
              '从==最低点==出发，相当于把折线整体上移到最低点为 0 → 之后不会再变负',
              'gas 之和 < cost 之和时油不够跑一圈，答案一定是 `-1`'],
        summary=['时间 `O(n)`，一次遍历；空间 `O(1)`',
                 '易错：`ans = i + 1` 而不是 `i`，因为 `s` 已经减去了开往 `i+1` 的耗油',
                 '不会算出 `ans = n`：那样的话最后一轮 `s < min_s ≤ 0`，返回的是 `-1`',
                 '复制一份折线：总油量 ≥ 0 时复制段不会比第一段的最低点更低'],
    ),
)
