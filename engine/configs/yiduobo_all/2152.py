P = [[0, 0], [1, 1], [2, 2], [1, 3]]


def _bits(x):
    return [i for i in range(len(P)) if x >> i & 1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(P)
    ln = S.get('_line', 0)
    cand = S.get('candidate')
    state = S.get('state')
    line = S.get('line') if 'next_state' in S or ln >= 22 else None
    cv.text((x0 + 18, y0 + 4), '平面上的点（绿 = state 已覆盖，黄框 = 当前直线上的点）', 22, T['muted'], bold=True)
    pl, pr, pt, pb = x0 + 60, x1 - 60, y0 + 60, y1 - 50
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    sx = (pr - pl) / (max(xs) - min(xs) + 1)
    sy = (pb - pt) / (max(ys) - min(ys) + 1)
    sc = min(sx, sy)
    ox = (pl + pr) / 2 - sc * (max(xs) + min(xs)) / 2
    oy = (pt + pb) / 2 + sc * (max(ys) + min(ys)) / 2

    def pos(p):
        return ox + p[0] * sc, oy - p[1] * sc

    cv.line([(pl - 20, pb + 10), (pr + 20, pb + 10)], T['border'], 2)
    # 当前直线
    if line:
        b = _bits(line)
        if len(b) >= 2:
            a, c = pos(P[b[0]]), pos(P[b[-1]])
            dx, dy = c[0] - a[0], c[1] - a[1]
            cv.line([(a[0] - dx * 0.25, a[1] - dy * 0.25), (c[0] + dx * 0.25, c[1] + dy * 0.25)], T['yellow'], 4)
    elif 'f' not in S and 'i' in S and 'j' in S and S['j'] > S['i']:
        a, c = pos(P[S['i']]), pos(P[S['j']])
        dx, dy = c[0] - a[0], c[1] - a[1]
        cv.line([(a[0] - dx * 0.4, a[1] - dy * 0.4), (c[0] + dx * 0.4, c[1] + dy * 0.4)], T['blue'], 3)
    for i, p in enumerate(P):
        X, Y = pos(p)
        r = 22
        cov = state is not None and 'next_state' in S and state >> i & 1
        online = (line is not None and line >> i & 1) or ('f' not in S and 'j' in S and i in (S.get('i'), S.get('j')))
        fill = T['green'] if cov else T['panel2']
        cv.rect((X - r, Y - r, X + r, Y + r), fill=fill, outline=T['yellow'] if online else T['border'], width=5 if online else 2, r=r)
        cv.text((X, Y), i, 24, T['bg'] if cov else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 40), f'({p[0]},{p[1]})', 18, T['dim'], anchor='mt', mono=True)


def _fmt(S):
    n = len(P)
    return lambda S: ''


def _cap_check(S, B, r):
    return (f"点 `{S.k}` {'在' if r else '不在'} 直线 `({S.i},{S.j})` 上" if False else '')


CONFIG = dict(
    num=2152, title='穿过所有点的所需最少直线数量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状压 DP · 枚举所有直线',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def minimumLines(self, points):

        def check(p1, p2, p3):
            x1, y1 = p2[0] - p1[0], p2[1] - p1[1]
            x2, y2 = p3[0] - p1[0], p3[1] - p1[1]
            return x1 * y2 == x2 * y1
        
        candidate = set()
        n = len(points)
        for i in range(n):
            candidate.add((1 << i))
            for j in range(i + 1, n):
                now = (1 << i) | (1 << j)
                for k in range(j + 1, n):
                    if check(points[i], points[j], points[k]):
                        now |= (1 << k)
                candidate.add(now)

        f = [n] * (1 << n)
        f[0] = 0
        for state in range((1 << n)):
            for line in candidate:
                next_state = state | line
                f[next_state] = min(f[next_state], f[state] + 1)
        
        return f[-1]
''',
    call=f'Solution().minimumLines({P})',
    expect=2,
    skip=['x1, y1 =', 'x2, y2 =', 'for i in range(n)', 'for j in range(i', 'for k in range(j', 'now = (1 << i)',
          'for state in range', 'for line in candidate', 'next_state = state', 'if check(', 'n = len(points)', 'def check', 'candidate = set()'],
    max_steps=42,
    views=[
        dict(type='custom', draw=_draw, h=370),
        dict(type='array', var='f', label='f[state]：覆盖 state 里这些点的最少直线数（下标是二进制掩码）', h=170, cell=56,
             pointers={'state': 'blue', 'next_state': 'pink'},
             color=lambda S, i, v: 'green' if v < len(S['points']) else None),
        dict(type='text', h=60, size=26,
             fn=lambda S: (f"`state = {S['state']:0{len(P)}b}`，`line = {S['line']:0{len(P)}b}`，`next_state = {S['state'] | S['line']:0{len(P)}b}`"
                           if 'line' in S and 'state' in S else
                           (f"候选直线（掩码）：{sorted(S['candidate'])}" if 'candidate' in S else ''))),
    ],
    watch=[('state', 'state', 'blue'), ('line', 'line', 'yellow'), ('next_state', 'next_state', 'pink')],
    captions={
        'return x1 * y2': lambda S, B, r: (f"点 `{S.k}` 对直线 `({S.i},{S.j})`：叉积 `{S.x1} × {S.y2}` 与 `{S.x2} × {S.y1}`：{'相等 → ==三点共线==' if r else '不等 → 不共线'}"),
        'candidate.add((1 << i))': '只覆盖点 `{i}` 的直线（掩码 `{1 << i}`）：任何一个点都能单独用一条线穿过',
        'now |= (1 << k)': '点 `{k}` 也在直线 `({i},{j})` 上 → 把它并进这条线的掩码 `now = {now}`',
        'candidate.add(now)': '这条线穿过的点集 `now = {bin(now)[2:]}（十进制 {now}）` 加入候选；用 set 去重（同一条线只记一次）',
        'if check(': lambda S, B, r: f'检查点 `{S.k}` 是否也在直线 `({S.i},{S.j})` 上（叉积判共线）',
        'f = [n] * (1 << n)': '`f[state]` 初值取 `n`（每点一条线必然够用）',
        'f[0] = 0': '什么点都不用覆盖：`f[0] = 0`',
        'f[next_state] = min': '`state` 再加一条线 `line`：`f[{state}] + 1 = {B.f[state] + 1}` 与 `f[{next_state}]` 原值 `{B.f[next_state]}` 取小 → =={f[next_state]}==',
        'return f[-1]': '`f[-1]` = 全部点都被覆盖的最少直线数 = =={ret}=='
    },
    cards=dict(
        one_liner='先枚举所有能画的直线，再状压 DP 一条条地叠加覆盖',
        complexity='时间 `O(2^n · L + n^3)`，`L` 为候选直线数，空间 `O(2^n)`',
        problem=['给定平面上的点 `points`，用若干条直线穿过==所有点==',
                 '返回所需的==最少直线数==（点数不超过 10）',
                 '示例：`[[0,1],[2,3],[4,5],[4,3]]` → `2`；本视频：`[[0,0],[1,1],[2,2],[1,3]]` → `2`'],
        quote='令f[state]表示覆盖state中这些点所需的最少直线数量，那么对于f[state]，可以直接枚举所有可能的直线',
        quote_src='—— yiduobo 题解原文',
        idea=['点数 ≤ 10 → 用二进制掩码 `state` 表示「哪些点已被覆盖」',
              '两两枚举点得到直线，再用==叉积==找出这条线上的其他点，合成一个掩码',
              '每个 `state` 枚举所有候选直线 `line`：`f[state | line]` 用 `f[state] + 1` 更新'],
        summary=['时间 `O(2^n · L)`，`L ≤ n(n+1)/2`；空间 `O(2^n)`',
                 '易错：两点定线后还要枚举其他点，否则三点共线会被当成三条线',
                 '共线判断用整数叉积，避免用斜率除法产生精度问题',
                 '`state | line` 允许重叠覆盖，所以顺序无关、不会算错',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
