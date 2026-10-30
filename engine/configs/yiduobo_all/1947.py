def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    c, v = S.get('c'), S.get('v')
    n = S.get('n')
    if c is None or n is None or v is None or 't' not in S:
        return
    s, t = S['s'], S['t']
    dis, prev = S.get('dis'), S.get('prev')
    now = S.get('now')
    H = y1 - y0 - 140
    P = {s: (x0 + 70, y0 + 80 + H / 2), t: (x1 - 70, y0 + 80 + H / 2)}
    for i in range(n):
        fy = y0 + 80 + H * (i + 0.5) / n
        P[i] = (x0 + (x1 - x0) * 0.33, fy)
        P[i + n] = (x0 + (x1 - x0) * 0.67, fy)
    cv.text((x0 + 18, y0 + 4), '网络流：绿 = 已选边（流量 1），黄 = 本次最短增广路；边上的数 = 费用（不匹配的题数）', 21, T['muted'], bold=True)
    path = set()
    if dis is not None and prev is not None and dis[t] != -1 and S.get('_line', 0) >= 0 and 'res' in S and S.get('_phase_path'):
        pass
    # 增广路：dis[t] 已得到时沿 prev 回溯
    if dis is not None and prev is not None and dis[t] != -1:
        k = t
        guard = 0
        while k != s and k != -1 and guard < 20:
            path.add((prev[k], k))
            k = prev[k]
            guard += 1
    edges = [(s, i) for i in range(n)] + [(i + n, t) for i in range(n)] + [(i, j + n) for i in range(n) for j in range(n)]
    for a, b in edges:
        used = c[a][b] == 0 and c[b][a] > 0
        hot = (a, b) in path or (b, a) in path
        col = T['yellow'] if hot else (T['green'] if used else T['border'])
        cv.line([P[a], P[b]], col, 7 if (hot or used) else 3)
        if a < n and b >= n and b < 2 * n:
            fr = 0.5 if b - n == a else 0.25
            mx, my = (P[a][0] * (1 - fr) + P[b][0] * fr), (P[a][1] * (1 - fr) + P[b][1] * fr)
            cv.rect((mx - 20, my - 15, mx + 20, my + 15), fill=T['bg'], r=8)
            cv.text((mx, my), v[a][b], 24, T['green'] if used else T['text'], anchor='mm', bold=True)
    names = {s: '源 s', t: '汇 t'}
    for k, (X, Y) in P.items():
        nm = names.get(k, f'学生{k}' if k < n else f'导师{k - n}')
        col = None
        if k == now:
            col = 'pink'
        elif dis is not None and dis[k] != -1:
            col = 'blue'
        R = 44
        cv.rect((X - R, Y - R, X + R, Y + R), fill=T[col] if col else T['panel2'], outline=T['border'], r=R)
        cv.text((X, Y), nm, 22, T['bg'] if col else T['text'], anchor='mm', bold=True)
        if dis is not None and dis[k] != -1:
            cv.text((X, Y + R + 8), f'dis={dis[k]}', 22, T['yellow'], anchor='mt', bold=True)


CONFIG = dict(
    num=1947, title='最大兼容性评分和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='最小费用最大流（二分图最优匹配）',
    tags=['灵神题单·动态规划', '灵神题单·图论算法', '难度分 1704'],
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
    call='Solution().maxCompatibilitySum([[0,1,1],[1,1,0]], [[1,0,0],[1,1,0]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=500),
        dict(type='text', fn=lambda S: (f"最小费用 = 已累计 `{S['m'] * S['n'] - S['res']}`，答案 `res = m×n − 费用 = {S['res']}`" if 'res' in S and 'm' in S and 'n' in S else ''), h=60, size=26),
        dict(type='heap', var='heap', fmt=lambda x: f'{x[0]}:{x[1]}→{x[2]}', label='堆 heap（费用 : 来路→去向）', h=110),
    ],
    skip=['n = len', 's = n + n', 't = n + n + 1', 'c = [[0]', 'v = [[0]', 'for i in range(n)', 'c[s][i] = 1', 'c[i + n][t] = 1', 'm = len', 'for j in range(n)',
          'cnt = m', 'for index in range(m)', 'if students[', 'cnt -= 1', 'c[i][j + n] = 1', 'v[i][j + n] = cnt', 'v[j + n][i] = -cnt',
          'while True', 'for next in range', 'if c[now][next] > 0', 'dis = [-1]', 'prev = [-1]', 'heap = []', 'now = t', 'prev[now] = p'],
    max_steps=68,
    watch=['d', 'p', 'now', ('res', 'res', 'green')],
    captions={
        'res = m * n': '图建好了：源 `s` → 学生（容量 1，费用 0）；学生 → 导师（容量 1，费用 = 不匹配的题数）；导师 → 汇 `t`。`res` 先取总分上限 `m×n = {res}`，后面减去最小费用',
        'dis[s] = 0': '每轮找一条最小费用的增广路：`dis` 记最小费用，`prev` 记来路（源点 `dis = 0`）',
        'if c[s][i] > 0': '源点到学生 `{i}` 还有容量 → 费用 `{v[s][i]}` 入堆',
        'heapq.heappush(heap, [v[s][i]': lambda S, B, r: f'学生 `{S.i}` 入堆：`[{S.v[S.s][S.i]}, s, {S.i}]`',
        'while heap': lambda S, B, r: '堆里还有候选，取费用最小的' if S.heap else '堆空了：这一轮搜索结束',
        'd, p, now = heapq.heappop': lambda S, B, r: f'弹出费用最小的：到节点 `{S.now}` 费用 `{S.d}`，来路 `{"s" if S.p == S.s else S.p}`',
        'if dis[now] != -1': lambda S, B, r: (f'`dis[{S.now}] = {S.dis[S.now]}` 已有更小或相等的费用（`{S.d} >= {S.dis[S.now]}`）→ 跳过' if S.dis[S.now] != -1 and S.d >= S.dis[S.now]
                                                else f'节点 `{S.now}` 第一次出堆，费用 `{S.d}` 就是最小的'),
        'continue': '过期的候选，丢掉',
        'dis[now] = d': '确定 `dis[{now}] = {d}`，来路 `prev[{now}] = {p}`',
        'heapq.heappush(heap, [d + v': '从 `{now}` 出发的边 `{now}→{next}` 还有容量：候选费用 `{d} + ({v[now][next]})` = `{d + v[now][next]}` 入堆{"（反向边，费用为负）" if v[now][next] < 0 else ""}',
        'if dis[t] == -1': lambda S, B, r: '`t` 到不了：已经没有增广路 → 结束' if S.dis[S.t] == -1 else f'`t` 的最小费用 `dis[t] = {S.dis[S.t]}`：找到一条增广路',
        'res -= dis[t]': '这条增广路的费用 `{dis[t]}` 是被浪费掉的评分 → `res = {B.res} − {dis[t]} = {res}`',
        'while now != s': lambda S, B, r: '沿 `prev` 从 `t` 回溯到 `s`，逐条更新容量' if S.now != S.s else '回到源点 `s`：这条增广路更新完了',
        'c[prev[now]][now] -= 1': '正向边用掉：`c[{prev[now]}][{now}]` → 0',
        'c[now][prev[now]] += 1': '反向边容量 +1，以后可以「退回」这条匹配（反向边费用为负）',
        'now = prev[now]': '回到上一个节点 `{now}`',
        'return res': '最大兼容性评分和 `{res}`',
    },
    cards=dict(
        one_liner='二分图最优匹配 = 最小费用最大流：费用取「不匹配的题数」',
        complexity='建图 `O(m² n)`，每轮最短路 `O(V² log V)`，共 `m` 轮；空间 `O(m²)`',
        problem=['`m` 名学生、`m` 名导师，各答 `n` 个 0/1 问题',
                 '配对评分 = 两人答案相同的题数；求一一配对后评分和的最大值',
                 '本视频：2 名学生、2 名导师，每人 3 道题 → `3`'],
        quote='题目给出的是一个标准的二分图，左侧节点为学生，右侧节点为老师，每一对学生和老师之间存在一条边，权重为二人之间的兼容性评分。……实际上，这就是经典的最优匹配问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['建图：源点→学生、导师→汇点，容量 1 费用 0；学生→导师容量 1，费用 = 题数 − 兼容性得分',
              '做一次最小费用最大流，最小费用就是「浪费掉」的得分',
              '答案 = 题目总数 × 人数 − 最小费用'],
        summary=['原文为 Python 2 风格，在 Python 3 下无需改动，代码照搬',
                 '时间约 `O(m × V² log V)`，`V = 2m + 2`；空间 `O(m²)`',
                 '易错点：反向边费用要取相反数，这样后面的增广路才能「撤销」之前的匹配',
                 '`res = m * n` 是总题数乘人数，最后减去最小费用',
                 '作者说明：原文提到 KM 算法也可做，这里选择网络流；对比灵神用 KM'],
    ),
)
