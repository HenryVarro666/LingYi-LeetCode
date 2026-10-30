def _flow_draw(cv, S, B, box, T, C, W, n, left_txt, right_txt, title, wlabel, known=None):
    """二分图费用流：s -> 左(0..n-1) -> 右(n..2n-1) -> t；C 容量矩阵，W 费用矩阵"""
    x0, y0, x1, y1 = box
    s, t = 2 * n, 2 * n + 1
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    top, bot = y0 + 120, y1 - 40
    gap = (bot - top) / max(1, n - 1) if n > 1 else 0
    ys = [top + i * gap for i in range(n)]
    ymid = (top + bot) / 2
    w_ = x1 - x0
    HW = 68
    XS, XL, XR, XT = x0 + 50, x0 + 70 + HW + 30, x1 - 70 - HW - 30, x1 - 50
    pos = {s: (XS, ymid), t: (XT, ymid)}
    hw = {s: 26, t: 26}
    for i in range(n):
        pos[i] = (XL, ys[i])
        pos[n + i] = (XR, ys[i])
        hw[i] = HW
        hw[n + i] = HW
    dis, prev, used, now = S.get('dis'), S.get('prev'), S.get('used') or set(), S.get('now')
    live = dis is not None and prev is not None
    kn = known or (lambda v: dis[v] is not None)
    path = set()
    if live and now is not None:
        b = now
        guard = 0
        while b is not None and b != s and guard < 20 and prev[b] is not None and prev[b] != -1:
            path.add((prev[b], b))
            b = prev[b]
            guard += 1

    def edge(a, b, lab=None, frac=0.5):
        (ax, ay), (bx, by) = pos[a], pos[b]
        saturated = C[a][b] == 0
        if (a, b) in path:
            col, wd = T['yellow'], 7
        elif saturated:
            col, wd = T['green'], 5
        else:
            col, wd = (62, 70, 82), 2
        cv.line([(ax + hw[a], ay), (bx - hw[b], by)], col, wd)
        if lab is not None:
            ax2, bx2 = ax + hw[a], bx - hw[b]
            mx, my = ax2 + (bx2 - ax2) * frac, ay + (by - ay) * frac
            tw = cv.tlen(lab, 20, True) + 10
            cv.rect((mx - tw / 2, my - 14, mx + tw / 2, my + 14), fill=T['bg'], r=6)
            cv.text((mx, my), lab, 20, col if (saturated or (a, b) in path) else T['muted'], anchor='mm', bold=True)

    for i in range(n):
        edge(s, i)
        edge(n + i, t)
        for j in range(n):
            edge(i, n + j, W[i][n + j], 0.3 + 0.1 * ((i + j) % 3))
    names = {s: 's', t: 't'}
    for v, (X, Y) in pos.items():
        isnow = live and v == now
        inu = live and v in used
        fill = T['panel2']
        out = T['border']
        if inu:
            out = T['cyan']
        if isnow:
            out = T['pink']
        h_ = hw[v]
        cv.rect((X - h_, Y - 26, X + h_, Y + 26), fill=fill, outline=out, width=5 if (isnow or inu) else 2, r=26)
        if v < n:
            cv.text((X, Y), left_txt(v), 21, T['blue'], anchor='mm', bold=True)
        elif v < 2 * n:
            cv.text((X, Y), right_txt(v - n), 21, T['orange'], anchor='mm', bold=True)
        else:
            cv.text((X, Y), names[v], 24, T['text'], anchor='mm', bold=True)
        if live and kn(v):
            cv.text((X, Y - 30), f'd={dis[v]}', 19, T['cyan'], anchor='mb', bold=True)
    cv.text((x0 + 18, y0 + 36), f'线上数字 = {wlabel}；绿 = 已流过，黄 = 当前最短路，青圈 = 已确定', 19, T['dim'])


S0 = [3, 4, 1]
K0 = 1


def _draw(cv, S, B, box, T):
    if 'c' not in S:
        cv.text((box[0] + 18, box[1] + 4), '（建图中）', 24, T['dim'])
        return
    n = S['n']
    _flow_draw(cv, S, B, box, T, S['c'], S['cost'], n,
               lambda i: f"锁{i}（需{S['strength'][i]}）", lambda j: f"第{j + 1}个 x={1 + K0 * j}",
               '二分图：锁 → 开锁位置，线上 = 等待分钟数（费用）', '费用')


def _fml(S):
    if 'dis' not in S or S.get('dis') is None:
        return '边 `锁 i → 第 j 个开` 的费用 = `(strength[i] − 1) // (1 + K·j) + 1`'
    return f'已选出的最少总时间 `res` = =={S.get("res", 0)}=='


def _pick(S, B, ret):
    return f'取 dis 最小的未确定点 `nxt = {S.nxt}`（`dis = {S.min_dis}`），从它出发松弛'


def _upd(S, B, ret):
    t = S.t
    path = []
    b = t
    while b is not None and b != S.s:
        path.append(b)
        b = S.prev[b]
    path.append(S.s)
    names = lambda v: 's' if v == S.s else 't' if v == S.t else (f'锁{v}' if v < S.n else f'位{v - S.n}')
    return '最短路：' + ' → '.join(names(v) for v in reversed(path)) + f'，费用 `{S.dis[S.t]}`'


CONFIG = dict(
    num=3376, title='破解锁的最少时间 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='最小费用最大流（锁 ↔ 开锁位置的匹配）',
    tags=['图论算法', '动态规划', '难度分 1793'],
    code='''
class Solution(object):
    def findMinimumTime(self, strength, K):
        
        n = len(strength)
        s = n + n
        t = n + n + 1

        c = [[0] * (t + 1) for _ in range(t + 1)]
        cost = [[0] * (t + 1) for _ in range(t + 1)]

        for i in range(n):
            c[s][i] = 1
        
        for j in range(n, n + n):
            c[j][t] = 1
        
        for i in range(n):
            for j in range(n, n + n):
                c[i][j] = 1
                cost[i][j] = (strength[i] - 1) // (1 + K * (j - n)) + 1
                cost[j][i] = -cost[i][j]
        
        res = 0
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                nxt = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + cost[now][index]):
                        dis[index] = dis[now] + cost[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        nxt = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res
                
                used.add(nxt)
                now = nxt

            res += dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]
''',
    call=f'Solution().findMinimumTime({S0}, {K0})',
    expect=4,
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'pink'), ('nxt', 'nxt', 'cyan'), ('dis[t]', lambda S: S['dis'][S['t']] if S.get('dis') else None, 'yellow')],
    skip=['n = len(strength)', 'for i in range(n)', 'for j in range(n, n + n)', 'for index in range', 'if c[now][index] > 0', 'dis[index] = dis[now]',
          'prev[index] = now', 'if index in used', 'used.remove(index)', 'if index not in used', 'nxt = index', 'min_dis = dis[index]',
          'min_dis = None', 'nxt = None', 'while t not in used', 'cost[j][i] = -cost[i][j]', 'c[j][t] = 1', 'c[i][j] = 1', 'used = set',
          'prev = [None]', 'dis[s] = 0', 'now = s', 'now = t', 'while now != s', 'c[now][prev[now]] += 1', 'dis = [None]',
          'c[s][i] = 1', 'cost[i][j] = (strength', 't = n + n + 1', 'now = prev[now]', 'used.add(nxt)', 'while True', 'if min_dis is None'],
    captions={
        's = n + n': '建图：锁 `0..{n-1}`，开锁位置 `{n}..{2*n-1}`，再加源点 `s = {n+n}`、汇点 `t = {n+n+1}`',
        'c = [[0]': '`c[a][b]` 是边 `a → b` 的剩余容量',
        'cost = [[0]': '`cost[a][b]` 是边的费用，反向边费用取负（可以“退回”）',
        'res = 0': '图建好了：`s→锁`、`位置→t` 容量 1 费用 0；`锁 i→第 j 个开` 容量 1，费用 = ==等待分钟数==（线上数字）。`res` 累计总费用，每轮找 `s→t` 最短路并推流 1',
        'now = nxt': lambda S, B, r: f'取 dis 最小且未确定的点 `{S.nxt}`（`dis = {S.min_dis}`）并确定它，下一步从它出发松弛邻边',
        'res += dis[t]': lambda S, B, r: f'`s → t` 最短路确定：费用 `{S.dis[S.t]}` → `res = {B.res} + {S.dis[S.t]} = {S.res}`；接着沿 `prev` 从 `t` 回溯推流',
        'c[prev[now]][now] -= 1': lambda S, B, r: f'推流经过边 `{B.prev[B.now]} → {B.now}`：容量 −1，反向边 +1（==以后可以反悔，改派位置==）',
        'return res': '再也找不到增广路：总费用 `{ret}`，也就是最少 `{ret}` 分钟',
    },
    max_steps=60,
    cards=dict(
        one_liner='把「锁放在第几个开」当成二分图匹配，跑一次最小费用流',
        complexity='时间 `O(n^3)` 量级（每次增广 `O(n^2)`），空间 `O(n^2)`',
        problem=['`strength[i]` 是开第 `i` 把锁所需能量，每分钟能量加 `x`；开锁后能量清零，`x` 增加 `K`',
                 '`x` 初始为 1，求开完所有锁的最少分钟数',
                 '本视频：`strength = [3,4,1], K = 1` → `4`'],
        quote='如果以全排列中的位置来看待第几个开的锁的话，本题就可以视为有n把锁和n个位置，需要将这些锁分配到这些位置上，每个位置都需要分配一把，而分配的代价就是上面的等待时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `j` 个开锁时 `X = (j-1)·K + 1`，锁 `i` 的等待时间 `(strength[i]-1)//X + 1` ==只取决于它排第几个==',
              '于是「锁 → 位置」的分配代价是一张表：二分图最小费用匹配，不用枚举全排列',
              '建图：`s→锁`、`锁→位置`（费用 = 等待时间）、`位置→t`，容量都是 1'],
        summary=['最小费用最大流：每轮找最短路（带负边的 Dijkstra 式松弛），沿路增广；总费用即答案',
                 '反向边费用取负，允许后面的增广「反悔」前面的匹配',
                 '`n` 到 80 时（第 3385 题）状压 DP 不行，费用流依旧可做',
                 '对比灵神：灵神主推排列回溯 + 剪枝，`n ≤ 8` 够用；费用流是他的「方法三」，适合 `n` 更大',
                 '原文变量名为 `K`；代码未改动，本身已是 Python 3 写法'],
    ),
)
