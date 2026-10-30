NUMS = [2, 3]
SLOTS = 2
N = len(NUMS)


def _pos(box):
    x0, y0, x1, y1 = box
    W, H = x1 - x0, y1 - y0
    xs, xl, xr, xt = x0 + 60, x0 + W * 0.30, x0 + W * 0.68, x1 - 60
    top = y0 + 110
    yl = [top + k * 170 for k in range(N)]
    yr = [top + k * 170 for k in range(SLOTS)]
    cy = (top + top + 170 * (max(N, SLOTS) - 1)) / 2
    P = {}
    for k in range(N):
        P[k] = (xl, yl[k])
    for k in range(SLOTS):
        P[N + k] = (xr, yr[k])
    P[N + SLOTS] = (xs, cy)
    P[N + SLOTS + 1] = (xt, cy)
    return P


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '费用流：左 = nums，右 = 篮子（括号 = 剩余容量），边上数字 = 损失 nums[i] − (nums[i] & 篮号)', 20, T['muted'], bold=True)
    if 'c' not in S or 'v' not in S or S.get('n') != N:
        return
    c, v = S['c'], S['v']
    s, t = N + SLOTS, N + SLOTS + 1
    P = _pos(box)
    line = S.get('_line')
    path = set()
    if S.get('dis') and S['dis'][t] != -1 and line in (43, 44, 45, 46, 47, 48) and 'prev' in S:
        now = t
        prev = S['prev']
        while now != s and prev[now] != -1:
            path.add((prev[now], now))
            now = prev[now]
    edges = []
    for i in range(N):
        edges.append(((s, i), c[s][i] == 0))
        for j in range(N, N + SLOTS):
            edges.append(((i, j), c[i][j] == 0))
    for j in range(N, N + SLOTS):
        edges.append(((j, t), c[j][t] < 2))
    for (a, b), used in edges:
        pa, pb = P[a], P[b]
        on_path = (a, b) in path
        colr = T['orange'] if on_path else (T['green'] if used else T['border'])
        cv.line([pa, pb], colr, 6 if (used or on_path) else 2)
        if a < N and N <= b < N + SLOTS:
            mx, my = pa[0] + (pb[0] - pa[0]) * 0.72, pa[1] + (pb[1] - pa[1]) * 0.72
            cv.rect((mx - 16, my - 13, mx + 16, my + 13), fill=T['bg'], r=6)
            cv.text((mx, my), v[a][b], 20, T['green'] if used else (T['orange'] if on_path else T['muted']), anchor='mm', bold=True)
    dis = S.get('dis') or []
    cur = S.get('now') if line is not None and line >= 30 else None
    for k, (px, py) in P.items():
        if k == s:
            lab = '源'
        elif k == t:
            lab = '汇'
        elif k < N:
            lab = NUMS[k]
        else:
            lab = f'篮{k - N + 1}'
        ring = T['yellow'] if k == cur else None
        fill = (70, 76, 86) if k in (s, t) else T['panel2']
        cv.rect((px - 32, py - 32, px + 32, py + 32), fill=fill, r=32, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((px, py), lab, 24 if k >= N and k not in (s, t) else 28, T['text'], anchor='mm', bold=True)
        if N <= k < N + SLOTS:
            cv.text((px + 40, py), f'({c[k][t]})', 20, T['muted'], anchor='lm', bold=True, mono=True)
        if k < len(dis):
            d = dis[k]
            cv.text((px, py + 44), f'dis={d}' if d != -1 else 'dis=?', 18, T['cyan'] if d != -1 else T['dim'], anchor='mt', bold=True, mono=True)
    cv.text((x0 + 18, y1 - 30), f"总收益上限 sum(nums) = {sum(NUMS)}，当前 res = {S.get('res')}（每条增广路减去它的损失）", 22, T['green'], anchor='lm', bold=True)


def _txt(S):
    if 'heap' not in S or S.get('_line', 0) < 24:
        return '损失小 = 与和大：把 `nums[i] & 篮号` 的差额当费用，求最小费用'
    return f"堆 `heap` 里有 {len(S['heap'])} 个候选 `[累计费用, 来自, 到达]`；`dis` = {S.get('dis')}"


CONFIG = dict(
    num=2172, title='数组的最大与和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='最小费用最大流 · 损失转最小费用',
    tags=['图论算法', '难度分 2392'],
    code='''
class Solution(object):
    def maximumANDSum(self, nums, numSlots):
        n = len(nums)
        s = n + numSlots
        t = s + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        v = [[0] * (t + 1) for _ in range(t + 1)]

        for i in range(n):
            c[s][i] = 1
        for j in range(n, n + numSlots):
            c[j][t] = 2
        for i in range(n):
            for j in range(n, n + numSlots):
                c[i][j] = 1
                v[i][j] = nums[i] - (nums[i] & (j - n + 1))
                v[j][i] = -v[i][j]

        res = sum(nums)
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
    call=f'Solution().maximumANDSum({NUMS!r}, {SLOTS})',
    expect=4,
    skip=['c[s][i] = 1', 'for j in range(n, n + numSlots)', 'c[j][t] = 2', 'c[i][j] = 1', 'v[i][j] = ', 'v[j][i] = ',
          'dis[s] = 0', 'heap = []', 'prev = [-1]', 'for i in range(n)', 'for next in range(t + 1)', 'while heap', 'now = t',
          'while now != s', 'now = prev[now]', 'if c[now][next] > 0', 'if c[s][i] > 0', 'c[now][prev[now]] += 1', 'dis = [-1]'],
    max_steps=60,
    views=[
        dict(type='custom', draw=_draw, h=460),
        dict(type='text', fn=_txt, size=22, h=90),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'yellow'), ('d', 'd', 'cyan')],
    captions={
        'n = len(nums)': '`n = {n}` 个数；节点 `0..n-1` 是数字，`n..n+numSlots-1` 是篮子',
        's = n + numSlots': '源点 `s = {s}`',
        't = s + 1': '汇点 `t = {t}`',
        'c = [[0]': '`c[a][b]` 是 a→b 的剩余容量',
        'v = [[0]': '`v[a][b]` 是 a→b 的费用',
        'for i in range(n)': lambda S, B, r: ('建图：源→每个数（容量 1，每个数必须用一次）；篮子→汇（容量 2，每个篮子最多放两个）；数→每个篮子（容量 1），费用 = 放进去的==损失== `nums[i] − nums[i] & 篮号`' if 'i' in S and S.get('_line') == 9 else '图建好了'),
        'res = sum(nums)': '`res` 先取上限 `sum(nums) = {res}`：每个数最多拿到 `nums[i]` 本身；放进篮子会有损失，损失越小越好',
        'while True': '每一轮：从源点出发，用最短路（Dijkstra 风格）找一条最小损失的增广路，找不到就结束',
        'heapq.heappush(heap, [v[s][i]': '数 `{i}` 还没放 → 作为起点入堆，费用 `{v[s][i]}`',
        'd, p, now = heapq.heappop': '弹出堆里累计费用最小的：到达节点 `{now}`，费用 `d = {d}`，来自 `{p}`',
        'if dis[now] != -1': lambda S, B, r: (f'`dis[{S.now}] = {S.dis[S.now]}` 已有、且 `d = {S.d}` 不更小 → 跳过' if (S.dis[S.now] != -1 and S.d >= S.dis[S.now]) else f'`{S.now}` 第一次被确定（或更便宜）→ 处理它'),
        'continue': '这个候选没有更优，丢弃',
        'dis[now] = d': '`dis[{now}] = {d}`：到节点 `{now}` 的最小费用确定',
        'prev[now] = p': '`prev[{now}] = {p}`：记前驱，之后沿它还原路径',
        'heapq.heappush(heap, [d + v': '边 `{now}→{next}` 还有容量，费用 `{v[now][next]}`：候选 `{[d + v[now][next], now, next]}` 入堆',
        'if dis[t] == -1': lambda S, B, r: (f'汇点不可达（`dis[t] = -1`）：所有数都放好了 → 结束' if S.dis[S.t] == -1 else f'汇点可达，最小损失 `dis[t] = {S.dis[S.t]}` → 沿 `prev` 增广'),
        'res -= dis[t]': '总和减去这条路的损失：`res = {res}`',
        'c[prev[now]][now] -= 1': '回溯路径：边 `{prev[now]}→{now}` 容量 −1，反向边 +1（可退流）',
        'break': '没有增广路了，退出',
        'return res': '最大与和 =={ret}==',
    },
    cards=dict(
        one_liner='先假设每个数都拿满，再把「损失」当费用求最小',
        complexity='最小费用最大流，每轮一次最短路，共 `n` 轮',
        problem=['`nums` 有 `n` 个数，`numSlots` 个篮子（编号 1 起），每个篮子最多 2 个数',
                 '与和 = 每个数与所在篮子编号按位与，求最大与和',
                 '示例：`nums = [2,3]`，`numSlots = 2` → `4`'],
        quote='从题目的数据规模来看可以使用状态压缩动态规划，但是更好的做法是将其转化为网络流来求解。……这里写成nums[i] - nums[i] & (j + 1)的目的是将最大与和转化为最小损失，方便最短路的运算。',
        quote_src='—— yiduobo 题解原文',
        idea=['源→每个数：容量 1（每个数必须用一次）',
              '数→篮子：容量 1，费用 = `nums[i] − (nums[i] & 篮号)`（损失）',
              '篮子→汇：容量 2（每篮最多两个数）',
              '总收益上限 `sum(nums)`，减去最小总损失就是答案'],
        summary=['`nums[i] & 篮号 ≤ nums[i]`，所以损失 ≥ 0，转成最小化问题',
                 '增广时正边容量 −1、反边 +1，反边费用为相反数，允许「反悔」',
                 '易错：篮子容量是 2，不是 1；篮号从 1 开始，所以用 `j - n + 1`',
                 '原文已是 Python 3 可运行写法，只删了空行里多余的空格',
                 '对比灵神：灵神用状压 DP（`4^numSlots`），题解后半也提到费用流'],
    ),
)
