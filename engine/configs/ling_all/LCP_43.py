DIRS = 'ESWN'
NAMES = ['东', '南', '西', '北']
_I = lambda S: S['_inner']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    d = _I(S)
    ds = S['ds']
    ps = [d.get(f'p{k}') for k in range(4)]
    if ps[0] is None:
        ps = [0, 0, 0, 0]
    chosen = {fr: to for fr, to in (d.get('a') or [])}
    cv.text((x0 + 18, y0 + 4), '四个车道（左 = 最靠近路口；灰 = 已通过，黄框 = 队首，绿 = 本秒放行）', 22, T['muted'], bold=True)
    cell = 76
    sx = x0 + 150
    y = y0 + 60
    rowh = 92
    for k in range(4):
        Y = y + k * rowh
        cv.text((x0 + 24, Y + 34), f'{NAMES[k]} {DIRS[k]}', 30, T['text'], anchor='lm', bold=True)
        cv.text((x0 + 24 + 92, Y + 34), f'p{k}={ps[k]}', 22, T['dim'], anchor='lm', mono=True)
        for i, c in enumerate(ds[k]):
            X = sx + i * cell + 70
            passed = i < ps[k]
            head = i == ps[k]
            fill = (52, 60, 72) if passed else T['panel2']
            if head and k in chosen:
                fill = T['green']
            cv.rect((X, Y, X + cell - 8, Y + 68), fill=fill, r=10, outline=T['yellow'] if head else T['border'], width=4 if head else 1)
            cv.text((X + (cell - 8) / 2, Y + 34), c, 34, T['bg'] if fill == T['green'] else (T['dim'] if passed else T['text']), anchor='mm', bold=True, mono=True)
        if k in chosen:
            cv.text((sx + 70 + max(len(ds[k]), 1) * cell + 10, Y + 34), f'→ 开往 {NAMES[chosen[k]]}', 24, T['green'], anchor='lm', bold=True)
    Y = y + 4 * rowh + 14
    sub = d.get('sub')
    if sub:
        cv.text((x0 + 24, Y), '本次枚举的放行方向：' + '、'.join(NAMES[k] for k in range(4) if sub >> k & 1), 26, T['blue'], bold=True)


def _txt(S):
    d = _I(S)
    if 'sub' not in d:
        return '`f(p0,p1,p2,p3)` = 东南西北各已走了 p0..p3 辆车时，走完剩下的车最少要几秒'
    return f"状态 `({d['p0']}, {d['p1']}, {d['p2']}, {d['p3']})`　已知最少 `res = {d.get('res')}`"


CONFIG = dict(
    num='LCP 43', title='十字路口的交通', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状态压缩枚举 · 记忆化搜索（Go 原文转写）',
    tags=['灵神题单·动态规划'],
    code='''
mp = {'E': 0, 'S': 1, 'W': 2, 'N': 3}  # 将方向字符映射到 0-3 上
valid = [  # 当前车去方向，另一辆车来方向，另一辆车去方向
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    [[0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [1, 0, 1, 0], [1, 1, 0, 0], [1, 1, 1, 0]],
]


# 两辆车 X 和 Y，将 X 旋转至方向 0 上，Y 跟着 X 一起旋转
# 这样上面就不用写一个很长的 valid 数组
def ok(fromX: int, toX: int, fromY: int, toY: int) -> bool:
    toX = (toX - fromX + 4) % 4
    fromY = (fromY - fromX + 4) % 4
    toY = (toY - fromX + 4) % 4
    return valid[toX][fromY][toY] == 1


class Solution:
    def trafficCommand(self, ds: List[str]) -> int:
        n0, n1, n2, n3 = len(ds[0]), len(ds[1]), len(ds[2]), len(ds[3])
        dp = [[[[0] * (n3 + 1) for _ in range(n2 + 1)] for _ in range(n1 + 1)] for _ in range(n0 + 1)]
        vis = [[[[False] * (n3 + 1) for _ in range(n2 + 1)] for _ in range(n1 + 1)] for _ in range(n0 + 1)]

        def f(p0: int, p1: int, p2: int, p3: int) -> int:
            res = 0
            if p0 == n0 and p1 == n1 and p2 == n2 and p3 == n3:
                return res
            if vis[p0][p1][p2][p3]:
                return dp[p0][p1][p2][p3]
            vis[p0][p1][p2][p3] = True
            try:
                ps = [p0, p1, p2, p3]
                res = int(1e9)
                for sub in range(1, 16):  # 枚举选择哪几个方向的车通行
                    a = []
                    s = sub
                    bad = False  # 对应 Go 的 continue outer
                    while s > 0:
                        frm = (s & -s).bit_length() - 1  # bits.TrailingZeros
                        if ps[frm] == len(ds[frm]):
                            bad = True
                            break
                        to = mp[ds[frm][ps[frm]]]
                        for q in a:
                            if not ok(frm, to, q[0], q[1]):
                                bad = True
                                break
                        if bad:
                            break
                        a.append((frm, to))
                        s &= s - 1
                    if bad:
                        continue
                    for p in a:
                        ps[p[0]] += 1
                    res = min(res, f(ps[0], ps[1], ps[2], ps[3]) + 1)
                    for p in a:
                        ps[p[0]] -= 1
                return res
            finally:
                dp[p0][p1][p2][p3] = res

        return f(0, 0, 0, 0)
''',
    call='Solution().trafficCommand(["W", "N", "", ""])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='calls', h=150),
    ],
    watch=[('sub', lambda S: S['_inner'].get('sub'), 'blue'), ('res', lambda S: S['_inner'].get('res'), 'green')],
    skip=['toX = (toX', 'fromY = (fromY', 'toY = (toY', 'a = []', 's = sub', 'bad = False', 'bad = True', 'break', 'if bad:', 'continue',
          'frm = (s', 'if ps[frm] == len', 'for q in a', 'for p in a:\n', 's &= s - 1', 'while s > 0', 'ps = [p0', 'n0, n1, n2, n3', 'try:', 'res = 0', 'ps[p[0]] -= 1', 'vis = [[[[False]'],
    captions={
        'mp = {': '把方向字符映射成 0-3：`E=0, S=1, W=2, N=3`',
        'valid = [': '`valid[toX][fromY][toY] = 1`：以「当前车从 0 方向出发」为参照，另一辆车 `fromY → toY` 与它路线不相交',
        'return valid[toX]': lambda B, S, r: (f'`valid[{S.toX}][{S.fromY}][{S.toY}] = {int(bool(r))}`：' + ('两车路线==不相交==，可以同一秒通行' if r else '两车路线==相交==，不能同一秒通行')),
        'dp = [[[[': '`dp[p0][p1][p2][p3]`：四条车道各走了 p 辆后，走完剩下的车最少几秒。演示按实际车数建表',
        'if p0 == n0 and': lambda B, S, r: ('所有车都走完了 → 还要 `0` 秒' if (S.p0, S.p1, S.p2, S.p3) == (S.n0, S.n1, S.n2, S.n3)
                                              else f'状态 `({S.p0}, {S.p1}, {S.p2}, {S.p3})`：还有车没走完'),
        'if vis[p0]': lambda B, S, r: ('这个状态已经算过 → 直接返回 `dp` 里的值' if S.vis[S.p0][S.p1][S.p2][S.p3] else '没算过，往下算'),
        'vis[p0][p1][p2][p3] = True': '标记 `({p0}, {p1}, {p2}, {p3})` 已访问',
        'res = int(1e9)': '`res` 先取一个很大的数，再对每种放行方案取最小',
        'for sub in range(1, 16)': lambda B, S, r: (f"`sub = {(S['_inner'].get('sub', 0) + 1):04b}`：枚举这一秒让哪几个方向（位 0-3 = 东南西北）的队首车通行，共 15 种非空选择"
                                                    if S['_inner'].get('sub', 0) < 15 else '15 种选择都枚举完了'),
        'to = mp[': "`{['东','南','西','北'][frm]}` 车道队首车开往 `{ds[frm][ps[frm]]}`（方向 {to}）",
        'if not ok(': '调用 `ok` 检查：它与已选的车 `{q}` 路线是否相交；相交这个组合就作废',
        'a.append': '选中：方向 {frm} 的车去往 {to}，`a = {a}`',
        'ps[p[0]] += 1': '放行 `a` 里的车：各车道位置变成 `{ps}`',
        'res = min(': '递归求剩余：`f{tuple(ps)}` + 这 1 秒，更新 `res`',
        'ps[p[0]] -= 1': '恢复现场 `ps = {ps}`；`res` 现在是 `{res}`',
        'return res': lambda B, S, r: ('这个状态没有车了：0 秒' if (S.p0, S.p1, S.p2, S.p3) == (S.n0, S.n1, S.n2, S.n3)
                                        else f'`({S.p0}, {S.p1}, {S.p2}, {S.p3})` 最少需要 =={S.res}== 秒'),
        'dp[p0][p1][p2][p3] = res': '`finally`（对应 Go 的 `defer`）：把 `res = {res}` 记进 `dp`',
        'return f(0, 0, 0, 0)': '从 `(0, 0, 0, 0)` 开始搜索：所有车都还没走',
    },
    max_events=200000,
    max_steps=58,
    cards=dict(
        one_liner='四条车道的进度是状态，每秒枚举放行哪几个方向，路线不相交才行',
        complexity='状态 `O(n^4)`（每道最多 20 辆），转移 `O(15·4)`',
        problem=['十字路口四个方向（东南西北）各有一队车，`directions[i]` 记录每辆车要开往的方向',
                 '每秒各车道只能走队首一辆，且路线不能相交，求最少几秒走完',
                 '示例：`["W","N","ES","W"]` → `2`；本视频：`["W","N","",""]` → `2`'],
        quote='两辆车 X 和 Y，将 X 旋转至方向 0 上，Y 跟着 X 一起旋转，这样上面就不用写一个很长的 valid 数组。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['状态 `(p0,p1,p2,p3)`：四条车道已经走掉的车数',
              '枚举这一秒让哪些车道队首通行（4 位二进制，15 种），任意两辆车用 `ok` 判断路线是否相交',
              '`f = min(f(下一状态) + 1)`，记忆化避免重复'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`defer` → `try/finally`，`continue outer` → 标志位）',
                 '原文开 `21^4` 的数组；演示时按实际车数 `n0..n3` 建 `dp/vis`，逻辑不变',
                 '`valid` 数组 Go 里是稀疏初始化，转写时补成完整的 `4×4×4`',
                 '易错：队首已走完的车道不能被选；选中的车两两都要通过 `ok`'],
    ),
)
