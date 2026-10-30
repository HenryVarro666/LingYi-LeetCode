def _flow_draw(cv, S, B, box, T, C, W, n, left_txt, right_txt, title, wlabel, known=None, known_as_used=False):
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
        inu = live and (v in used or (known_as_used and kn(v)))
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


ST = [[1, 1, 0], [1, 0, 1], [0, 0, 1]]
MT = [[1, 0, 0], [0, 0, 1], [1, 1, 0]]


def _draw(cv, S, B, box, T):
    if 'v' not in S or 'c' not in S:
        cv.text((box[0] + 18, box[1] + 4), '（建图中）', 24, T['dim'])
        return
    n = S['n']
    s = S['s']
    _flow_draw(cv, S, B, box, T, S['c'], S['v'], n,
               lambda i: f"学生{i} {''.join(map(str, ST[i]))}", lambda j: f"导师{j} {''.join(map(str, MT[j]))}",
               '二分图：学生 → 导师，线上 = 不匹配的题数（费用）', '不匹配题数',
               known=lambda v: v == s or S['prev'][v] != -1, known_as_used=True)


def _fml(S):
    if 'res' not in S:
        return '边 `学生 i → 导师 j` 的费用 = 两人答案==不同==的题数 = `题数 − 兼容分`'
    return f'`res = m×n − 最小总费用` = {S["m"]*S["n"]} − {S["m"]*S["n"]-S["res"]} → ==当前 res = {S["res"]}=='


CONFIG = dict(
    num=1947, title='最大兼容性评分和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='二分图最优匹配 · 最小费用最大流',
    tags=['图论算法', '难度分 1704'],
    code='''
class Solution(object):
    def maxCompatibilitySum(self, students, mentors):

        n = len(students)
        s = n + n
        t = n + n + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        v = [[0] * (t + 1) for _ in range(t + 1)]
        for i in range(n):
            c[s][i] = 1
            c[i + n][t] = 1

        m = len(students[0])
        for i in range(n):
            for j in range(n):
                cnt = m
                for index in range(m):
                    if students[i][index] == mentors[j][index]:
                        cnt -= 1
                
                c[i][j + n] = 1
                v[i][j + n] = cnt
                v[j + n][i] = -cnt

        res = m * n
        while True:
            dis = [-1] * (t + 1)
            prev = [-1] * (t + 1)
            dis[s] = 0
            heap = []
            for i in range(n):
                if c[s][i] > 0:
                    heapq.heappush(heap, [v[s][i], s, i])
            
            while heap:
                d, p, now = heapq.heappop(heap)
                if dis[now] != -1 and d >= dis[now]:
                    continue
                
                dis[now] = d
                prev[now] = p
                for next in range(t + 1):
                    if c[now][next] > 0:
                        heapq.heappush(heap, [d + v[now][next], now, next])
            
            if dis[t] == -1:
                break

            res -= dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]

        return res
''',
    call=f'Solution().maxCompatibilitySum({ST}, {MT})',
    expect=8,
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'pink'), ('d', 'd', 'cyan'), ('dis[t]', lambda S: S['dis'][S['t']] if S.get('dis') else None, 'yellow')],
    skip=['n = len(students)', 't = n + n + 1', 'for i in range(n)', 'for j in range(n)', 'c[s][i] = 1', 'c[i + n][t] = 1', 'm = len(students[0])',
          'cnt = m', 'for index in range(m)', 'if students[i][index]', 'cnt -= 1', 'c[i][j + n] = 1', 'v[i][j + n] = cnt', 'v[j + n][i] = -cnt',
          'dis = [-1]', 'prev = [-1]', 'dis[s] = 0', 'heap = []', 'if c[s][i] > 0', 'heapq.heappush', 'while heap', 'heapq.heappop', 'if dis[now] != -1',
          '                    continue', 'dis[now] = d', 'for next in range', 'if c[now][next] > 0', 'now = t', 'while now != s', 'c[now][prev[now]] += 1',
          'now = prev[now]', 'while True', 'v = [[0]', 'c = [[0]', '                break'],
    captions={
        's = n + n': '建图：学生 `0..{n-1}`、导师 `{n}..{2*n-1}`，加源点 `s = {n+n}`、汇点 `t = {n+n+1}`',
        'res = m * n': '建好图：`s→学生`、`导师→t` 容量 1 费用 0；`学生→导师` 容量 1，费用 = ==两人答案不同的题数==。满分是 `m×n`，最后减去最小总费用',
        'prev[now] = p': lambda S, B, r: f'弹出堆里最短的 `{S.now}`：`dis = {S.d}`，前驱 `{S.p}`，确定下来并向外松弛',
        'if dis[t] == -1': lambda S, B, r: ('到不了汇点 `t` → 所有人都配好了，==结束==' if S.dis[S.t] == -1
                                            else f'`dis[t] = {S.dis[S.t]}`：找到一条 `s → t` 的最短路，还能再增广'),
        'res -= dis[t]': lambda S, B, r: f'这条增广路的费用 `{S.dis[S.t]}` 就是多损失的分数：`res = {B.res} − {S.dis[S.t]} = {S.res}`',
        'c[prev[now]][now] -= 1': lambda S, B, r: f'沿 `prev` 回溯推流经过边 `{B.prev[B.now]} → {B.now}`：容量 −1，反向边 +1（==允许后面反悔==）',
        'return res': '最大兼容性评分和 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='学生和导师就是二分图，最大评分和 = 最优匹配',
        complexity='时间约 `O(n^3·m)`，空间 `O(n^2)`',
        problem=['`m` 名学生、`m` 名导师，各自对 `n` 道题答 0/1；配对得分 = 答案相同的题数',
                 '一对一配对，求总得分最大',
                 '示例：`students=[[1,1,0],[1,0,1],[0,0,1]]`，`mentors=[[1,0,0],[0,0,1],[1,1,0]]` → `8`'],
        quote='题目给出的是一个标准的二分图，其中左侧节点为学生，右侧节点为老师，而每一对学生和老师之间存在一条边，权重为二人之间的兼容性评分。……这就是经典的最优匹配问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据范围小，状压 DP 能做；但==网络流 / 匹配==是更优选择',
              '求最大变求最小：边费用取「不匹配的题数」，最后答案 = 题数×人数 − 最小费用',
              '`s→学生`、`导师→t` 容量 1，`学生→导师` 容量 1；跑最小费用最大流'],
        summary=['每轮用堆做 Dijkstra 找 `s→t` 最短路（反向边费用为负，靠残量图保证正确），沿路增广',
                 '答案 `res = m×n − Σ 每轮 dis[t]`，不是直接累加',
                 '反向边容量 +1 让后面的增广能「改派」之前的配对',
                 '原文为 `class Solution(object)` 写法，代码本身已是 Python 3 可运行，未改动',
                 '同题另有 KM 算法、状压 DP；原文选网络流'],
    ),
)
