def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '费用流：边上数字 = 异或费用，绿色粗线 = 已被流量占用', 22, T['muted'], bold=True)
    if 'c' not in S or 'v' not in S or 'n' not in S:
        return
    n, c, v = S['n'], S['c'], S['v']
    s, t = 2 * n, 2 * n + 1
    dis = S.get('dis') or [None] * (2 * n + 2)
    W, H = x1 - x0, y1 - y0
    pos = {s: (x0 + 70, y0 + H * 0.52), t: (x1 - 70, y0 + H * 0.52)}
    gap = min(120, (H - 120) / max(n, 1))
    for i in range(n):
        pos[i] = (x0 + W * 0.30, y0 + H * 0.52 + (i - (n - 1) / 2) * gap)
        pos[i + n] = (x0 + W * 0.70, y0 + H * 0.52 + (i - (n - 1) / 2) * gap)
    path = set()
    if S.get('_line', 0) >= 51 and 'now' in S and 'fa' in S:
        k = S['now']
        while k in S['fa'] and k != s:
            path.add((S['fa'][k], k))
            k = S['fa'][k]
    edges = [(s, i) for i in range(n)] + [(i + n, t) for i in range(n)] + [(i, j + n) for i in range(n) for j in range(n)]
    for a, b in edges:
        used = c[a][b] == 0
        col = T['green'] if used else T['border']
        if (a, b) in path:
            col = T['yellow']
        (ax, ay), (bx, by) = pos[a], pos[b]
        cv.line([(ax, ay), (bx, by)], col, 6 if used or col == T['yellow'] else 2)
        if a < n and b >= n and b < 2 * n:
            mx, my = ax + (bx - ax) * 0.3, ay + (by - ay) * 0.3
            cv.text((mx, my - 14), v[a][b], 22, T['text'] if used else T['muted'], anchor='mm', bold=True)
    names = {s: '源', t: '汇'}
    for k, (px, py) in pos.items():
        col = T['blue'] if k < n else T['pink'] if k < 2 * n else T['purple']
        if S.get('now') == k and S.get('_line', 0) >= 37:
            col = T['yellow']
        cv.rect((px - 32, py - 24, px + 32, py + 24), fill=col, r=10)
        lab = names.get(k) or (f'n1={S["nums1"][k]}' if k < n else f'n2={S["nums2"][k - n]}')
        cv.text((px, py), lab, 20, T['bg'], anchor='mm', bold=True)
        d = dis[k] if k < len(dis) else None
        cv.text((px, py + 42), f'dis={d if d is not None else "∞"}', 20, T['cyan'], anchor='mm', bold=True)


CONFIG = dict(
    num=1879, title='两个数组最小的异或值之和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='最小费用最大流（SPFA 增广）',
    tags=['图论算法', '动态规划', '难度分 2145'],
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
    call='Solution().minimumXORSum([1,2], [2,3])',
    expect=2,
    skip=['c[s][i]', 'c[i][s]', 'v[s][i]', 'v[i][s]', 'c[i + n][t]', 'v[i + n][t]', 'c[t][i + n]', 'v[t][i + n]',
          'c[i][j + n] = 1', 'c[j + n][i] = 0', 'v[i][j + n]', 'v[j + n][i]', 'for j in range(n)',
          's = n + n', 't = n + n + 1', 'l = 0', 'r = 1', 'q = [s]', 'fa = {}', 'used = set', 'dis[s] = 0',
          'l += 1', 'c[now][fa[now]] += 1', 'now = fa[now]', 'while now != s', 'while l < r', 'res = 0', 'if c[now][next] > 0', 'for next in c', 'if next not in used', 'used.remove', 'used.add', 'r += 1', 'q.append', 'fa[next] = now'],
    max_steps=60,
    views=[
        dict(type='custom', draw=_draw, h=480),
        dict(type='array', var=lambda S: ['∞' if d is None else d for d in S['dis']] if 'dis' in S else [], label='dis：源到各点的最小费用（SPFA 松弛）', h=170, cell=70,
             pointers={'now': 'yellow'}),
        dict(type='array', var=lambda S: S['q'][S['l']:] if 'q' in S else [], label='队列 q（还没取出的点）', h=140, cell=70),
    ],
    watch=['res', 'now', 'next', ('dis[t]', "dis[t] if dis[t] is not None else '无路'", 'green')],
    captions={
        'n = len': '`n = {n}`：两边各 `{n}` 个点',
        'c = {x': '`c[a][b]` = 边 a→b 的剩余容量，每个点一个字典',
        'v = {x': '`v[a][b]` = 边的费用；反向边费用取负',
        'for i in range(n)': '`i = {i}`：建边 源→n1[{i}]、n2[{i}]→汇（容量 1，费用 0）；n1[{i}] 连向每个 n2，费用 = 异或值',
        'res = 0': '`res` 累计总费用',
        'while True': '再找一条最便宜的增广路',
        'dis = [None]': '每轮重新做 SPFA：`dis` 全部置为无穷（None）',
        'now = q[l]': '从队列取出点 `{now}`，去松弛它的出边',
        'if c[now][next] > 0': lambda S, B, r: (f'边 `{S.now}→{S.next}`：容量 {S.c[S.now][S.next]}，费用 {S.v[S.now][S.next]}，当前 `dis[{S.next}]` = {S.dis[S.next] if S.dis[S.next] is not None else "∞"} → ' + ('走这条更便宜，==松弛==' if S.c[S.now][S.next] > 0 and (S.dis[S.next] is None or S.dis[S.next] > S.dis[S.now] + S.v[S.now][S.next]) else '没有容量或不更便宜，跳过')),
        'dis[next] = dis[now]': '边 `{now}→{next}` 有容量，费用 {v[now][next]}：`dis[{next}]` 从 {B.dis[next] if B.dis[next] is not None else "∞"} 松弛为 `{dis[now]} + {v[now][next]}` = =={dis[next]}==',
        'if dis[t] is not None': lambda S, B, r: (f'汇点可达，这轮最便宜的路费用 `dis[t] = {S.dis[S.t]}`' if S.dis[S.t] is not None else '汇点已不可达：流量已经满了 → 结束'),
        'res += dis[t]': '`res += {dis[t]}` → =={res}==',
        'now = t': '沿 `fa` 从汇点倒着走回源，给路径上的边退流',
        'c[fa[now]][now] -= 1': '路径边 `{fa[now]}→{now}` 容量 -1（用掉），反向边容量 +1（以后可以“反悔”）；再退到 `{fa[now]}`',
        'now = fa[now]': '回退一步：`now = {now}`',
        'break': '没有增广路了，跳出',
        'return res': '最小异或和 = =={ret}==',
    },
    cards=dict(
        one_liner='把配对看成二分图，用最小费用流选出 n 条边',
        complexity='SPFA 费用流，点 `2n+2`、边 `O(n²)`，最多增广 `n` 次',
        problem=['把 `nums2` 重新排列，使 `Σ nums1[i] XOR nums2[i]` 最小',
                 '`n ≤ 14`，`nums` 值 `≤ 10^7`',
                 '示例：`nums1=[1,2]`，`nums2=[2,3]` → `2`'],
        quote='将nums1中的每个数与nums2中的每个数都连上一条边，边的权重就是两个数的异或值，……这是一个典型的二分图最优匹配问题，……我在这里采用的是费用流建模。',
        quote_src='—— yiduobo 题解原文',
        idea=['源→nums1 每点、nums2 每点→汇：容量 1、费用 0，保证每个数只用一次',
              'nums1 每点→nums2 每点：容量 1，费用 = 两数异或',
              '每轮 SPFA 找最便宜的增广路，沿路退流（反向边费用取负），累计费用'],
        summary=['题目 `n ≤ 14` 也可状压 DP，但图论角度（KM / 费用流）更好',
                 '反向边费用为负，所以要用 SPFA（队列版 Bellman-Ford），不能用 Dijkstra',
                 '易错：每轮增广都要重置 `dis`、`fa`、`used`',
                 '原文是 Python 2 写法的类声明 `class Solution(object)`，在 Python 3 中直接可运行，代码未改动'],
    ),
)
