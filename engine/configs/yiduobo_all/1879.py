A1 = [1, 2]
A2 = [2, 3]
N = len(A1)


def _pos(box):
    x0, y0, x1, y1 = box
    W, H = x1 - x0, y1 - y0
    xs, xl, xr, xt = x0 + 60, x0 + W * 0.30, x0 + W * 0.68, x1 - 60
    top, gap = y0 + 100, (H - 190) / max(1, N - 1) if N > 1 else 0
    ys = [top + k * min(gap, 170) for k in range(N)]
    cy = (ys[0] + ys[-1]) / 2
    P = {}
    for k in range(N):
        P[k] = (xl, ys[k])
        P[k + N] = (xr, ys[k])
    P[2 * N] = (xs, cy)
    P[2 * N + 1] = (xt, cy)
    return P


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '二分图费用流：左 = nums1，右 = nums2，边上数字 = 异或值（费用）', 22, T['muted'], bold=True)
    if 'c' not in S or 'v' not in S:
        return
    c, v, n = S['c'], S['v'], S['n']
    if n != N:
        return
    s, t = 2 * N, 2 * N + 1
    P = _pos(box)
    line = S.get('_line')
    path = set()
    if 'fa' in S and S.get('dis') and S['dis'][t] is not None and line in (49, 50, 51, 52, 53, 54, 55):
        now = t
        fa = S['fa']
        while now != s and now in fa:
            path.add((fa[now], now))
            now = fa[now]
    used_edges = []
    for i in range(N):
        used_edges.append(((s, i), c[s][i] == 0))
        used_edges.append(((i + N, t), c[i + N][t] == 0))
        for j in range(N):
            used_edges.append(((i, j + N), c[i][j + N] == 0))
    for (a, b), used in used_edges:
        pa, pb = P[a], P[b]
        on_path = (a, b) in path
        colr = T['orange'] if on_path else (T['green'] if used else T['border'])
        cv.line([pa, pb], colr, 6 if (used or on_path) else 2)
        if a < N and N <= b < 2 * N:
            fx = 0.72
            mx, my = pa[0] + (pb[0] - pa[0]) * fx, pa[1] + (pb[1] - pa[1]) * fx
            wt = v[a][b]
            cv.rect((mx - 16, my - 13, mx + 16, my + 13), fill=T['bg'], r=6)
            cv.text((mx, my), wt, 20, T['green'] if used else (T['orange'] if on_path else T['muted']), anchor='mm', bold=True)
    dis = S.get('dis') or []
    now_n, nxt = S.get('now'), S.get('next')
    if line is not None and line < 35:
        now_n = nxt = None
    names = {s: '源', t: '汇'}
    for k, (px, py) in P.items():
        lab = names.get(k) or (A1[k] if k < N else A2[k - N])
        ring = None
        if k == now_n:
            ring = T['yellow']
        elif k == nxt:
            ring = T['pink']
        fill = T['panel2']
        if k in (s, t):
            fill = (70, 76, 86)
        cv.rect((px - 30, py - 30, px + 30, py + 30), fill=fill, r=30, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((px, py), lab, 28, T['text'], anchor='mm', bold=True)
        if k < N:
            cv.text((px - 38, py), f'#{k}', 17, T['dim'], anchor='rm', mono=True)
        if k < len(dis):
            d = dis[k]
            cv.text((px, py + 42), f'dis={d}' if d is not None else 'dis=∞', 18, T['cyan'] if d is not None else T['dim'], anchor='mt', bold=True, mono=True)
    cv.text((x0 + 18, y1 - 30), f"累计费用 res = {S.get('res', 0)}　　（绿线 = 已匹配，橙线 = 本轮找到的最短增广路）", 22, T['green'], anchor='lm', bold=True)


def _txt(S):
    if 'q' not in S or S.get('_line', 0) < 29:
        return '每轮用 SPFA 找一条费用最小的增广路，把流量加 1'
    q = S['q']
    return f"队列 `q = {q}`，已处理 `l = {S.get('l')}` 个；`dis` = {S.get('dis')}"


CONFIG = dict(
    num=1879, title='两个数组最小的异或值之和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二分图最优匹配 · 最小费用最大流（SPFA）',
    tags=['图论算法', '难度分 2145'],
    code='''
class Solution(object):
    def minimumXORSum(self, nums1, nums2):
        n = len(nums1)
        c = {x : {} for x in range(n + n + 2)}
        v = {x : {} for x in range(n + n + 2)}
        s = n + n
        t = n + n + 1
        for i in range(n):
            c[s][i] = 1
            c[i][s] = 0
            v[s][i] = 0
            v[i][s] = 0

            c[i + n][t] = 1
            v[i + n][t] = 0
            c[t][i + n] = 0
            v[t][i + n] = 0

            for j in range(n):
                c[i][j + n] = 1
                c[j + n][i] = 0
                v[i][j + n] = nums1[i] ^ nums2[j]
                v[j + n][i] = -(nums1[i] ^ nums2[j])

        res = 0
        while True:
            l = 0
            r = 1
            dis = [None] * (n + n + 2)
            dis[s] = 0
            q = [s]
            fa = {}
            used = set([s])

            while l < r:
                now = q[l]
                l += 1
                used.remove(now)
                for next in c[now]:
                    if c[now][next] > 0 and (dis[next] is None or dis[next] > dis[now] + v[now][next]):
                        dis[next] = dis[now] + v[now][next]
                        fa[next] = now
                        if next not in used:
                            used.add(next)
                            r += 1
                            q.append(next)

            if dis[t] is not None:
                res += dis[t]
                now = t
                while now != s:
                    c[fa[now]][now] -= 1
                    c[now][fa[now]] += 1
                    now = fa[now]
            else:
                break

        return res
''',
    call=f'Solution().minimumXORSum({A1!r}, {A2!r})',
    expect=2,
    skip=['c[s][i] = 1', 'c[i][s] = 0', 'v[s][i] = 0', 'v[i][s] = 0', 'c[i + n][t] = 1', 'v[i + n][t] = 0',
          'c[t][i + n] = 0', 'v[t][i + n] = 0', 'for j in range(n)', 'c[i][j + n] = 1', 'c[j + n][i] = 0',
          'v[i][j + n]', 'v[j + n][i]', 'l = 0', 'r = 1', 'dis[s] = 0', 'used = set', 'now = q[l]', 'used.remove',
          'for next in c[now]', 'dis[next] = ', 'fa[next] = now', 'if next not in used', 'used.add(next)', 'r += 1', 'l += 1',
          'while l < r', 'while now != s', 'now = fa[now]', 'c[now][fa[now]] += 1', 'dis = [None]', 'q = [s]', 'fa = {}', 'res = 0', 'now = t', 's = n + n', 't = n + n + 1'],
    max_steps=48,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=_txt, size=22, h=90),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'yellow'), ('next', 'next', 'pink')],
    captions={
        'c = {x': '`c[a][b]` 是 a→b 的剩余容量，节点 `0..n-1` 是 nums1，`n..2n-1` 是 nums2',
        'v = {x': '`v[a][b]` 是 a→b 的费用；反向边费用取负，方便「退流」',
        's = n + n': '源点 `s = {s}`',
        't = n + n + 1': '汇点 `t = {t}`',
        'for i in range(n)': lambda S, B, r: (f'建图（第 {S.i} 个数）：源→`nums1[{S.i}]` 容量 1 费用 0；`nums2` 各点→汇容量 1 费用 0；`nums1[{S.i}]` 向每个 nums2 连边，容量 1、费用 = 异或值' if 'i' in S else '图建好了'),
        'res = 0': '`res` 累计总费用：每找到一条增广路就加上它的费用',
        'while True': '每一轮：队列从源点出发做 SPFA（允许节点重复入队），`dis[x]` = 源点到 x 的最小费用，`fa[x]` 记前驱；找不到 s→t 的路就结束',
        'dis = [None]': '`dis[x]` = 源点到 x 的最小费用，None 表示还没到达',
        'q = [s]': '队列从源点出发（类似 BFS，但允许节点被重新入队）',
        'fa = {}': '`fa[x]` 记录最短路里 x 的上一个节点，用来回溯路径',
        'while l < r': lambda S, B, r: (f'队列里还有 `{S.r - S.l}` 个节点没处理 → 继续' if S.l < S.r else '队列空了，这一轮最短路算完'),
        'for next in c[now]': lambda S, B, r: (f'枚举 `{S.now}` 的出边：试试走向 `{S.next}`' if 'next' in S and B.get('now') != S.now or 'next' in S else '`now` 的出边都试完了'),
        'if c[now][next] > 0': lambda S, B, r: (
            f'边 `{S.now}→{S.next}`：容量 `{S.c[S.now][S.next]}`，费用 `{S.v[S.now][S.next]}`，'
            + ('容量为 0 → 走不通' if S.c[S.now][S.next] <= 0 else
               (f'`dis[{S.next}] = {B.dis[S.next]}` 比 `dis[{S.now}] + 费用 = {B.dis[S.now] + S.v[S.now][S.next]}` 更大 → ==松弛成功==，更新 `dis`' if B.dis[S.next] is not None and B.dis[S.next] > B.dis[S.now] + S.v[S.now][S.next]
                else ('还没到达过 → ==第一次到达==，入队' if B.dis[S.next] is None else '不比已有路更短 → 不更新')))),
        'dis[next] = ': '`dis[{next}]` 更新为 `{dis[next]}`：找到一条更便宜的路',
        'fa[next] = now': '记下 `{next}` 的前驱是 `{now}`',
        'if next not in used': '`{next}` 已在队列里吗？（`used` 记录是否在队列）→ {"不在，要入队" if next not in B.used else "已在队列，不用重复入队"}',
        'used.add(next)': '`{next}` 入队',
        'q.append(next)': '`dis[{next}] = {dis[next]}`，前驱 `{fa[next]}`，`{next}` 入队：`q = {q}`',
        'if dis[t] is not None': lambda S, B, r: (f'汇点可达，最小费用 `dis[t] = {S.dis[S.t]}` → 沿 `fa` 回溯这条增广路' if S.dis[S.t] is not None else '汇点不可达：所有数都匹配完了 → 结束'),
        'res += dis[t]': '这条路让匹配数 +1，总费用 `res = {res}`',
        'now = t': '从汇点沿 `fa` 往回走，逐条更新容量',
        'c[fa[now]][now] -= 1': '回溯路径：边 `{fa[now]}→{now}` 容量 −1，反向边 +1（以后可退流改选）',
        'c[now][fa[now]] += 1': '反向边容量加 1：以后可以「退流」，也就是改选别的匹配',
        'now = fa[now]': '回溯到 `{now}`',
        'break': '没有增广路了，退出',
        'return res': '最小异或值之和 =={ret}==',
    },
    cards=dict(
        one_liner='把「重新排列」看成二分图最小费用匹配，用费用流求',
        complexity='SPFA 费用流：每轮 `O(VE)`，共 `n` 轮；比 `O(2^n·n)` 状压 DP 更快',
        problem=['给两个长度 `n` 的数组，把 `nums2` 重新排列',
                 '使 `Σ nums1[i] XOR nums2[i]` 最小，返回这个和',
                 '示例：`[1,2]`、`[2,3]` → `2`（排成 `[3,2]`）'],
        quote='将nums1中和nums2中的每个数都视为图中的一个节点，……边的权重就是两个数的异或值，……这是一个典型的二分图最优匹配问题，经典的做法有KM算法，当然也可以使用费用流建模来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['源 → nums1 各点（容量 1，费用 0）；nums2 各点 → 汇（容量 1，费用 0）',
              'nums1 的每个数向 nums2 的每个数连边：容量 1，费用 = 异或值',
              '最大流 = n 就是每个点都用一次，最小费用 = 最小异或和',
              '每轮 SPFA 找最便宜的增广路，反向边费用为负，可以「反悔」'],
        summary=['时间：`n` 轮 SPFA，每轮最坏 `O(V·E)`，`V = 2n+2`，`E ≈ n²`',
                 '易错：反向边的容量初始为 0、费用取负，增广时正边 `-1`、反边 `+1`',
                 '`dis` 用 `None` 表示未到达；`used` 表示是否在队列里',
                 '原文已是 Python 3 可运行写法，只删了空行里多余的空格',
                 '另一种解法：状压 DP `f[mask]`，`n ≤ 14` 也能过'],
    ),
)
