EDGES = [[0, 1, 3], [1, 2, 2], [2, 4, 4], [0, 3, 1], [3, 4, 5]]
POS = {0: (0.08, 0.5), 1: (0.32, 0.15), 2: (0.62, 0.15), 3: (0.32, 0.85), 4: (0.92, 0.5)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '图（边上是修复成本；亮线 = 成本 ≤ mid 可走；绿点 = BFS 已到达）', 22, T['muted'], bold=True)
    gx0, gx1 = x0 + 90, x1 - 90
    gy0, gy1 = y0 + 90, y1 - 40
    P = {k: (gx0 + a * (gx1 - gx0), gy0 + b * (gy1 - gy0)) for k, (a, b) in POS.items()}
    mid = S.get('mid')
    vis = S['vis'] if (mid is not None and 'vis' in S) else set()
    for u, v, w in EDGES:
        ok = mid is not None and w <= mid
        col = T['cyan'] if ok else T['border']
        cv.line([P[u], P[v]], col, 6 if ok else 3)
        mx, my = (P[u][0] + P[v][0]) / 2, (P[u][1] + P[v][1]) / 2
        cv.rect((mx - 22, my - 18, mx + 22, my + 18), fill=T['panel2'], r=8)
        cv.text((mx, my), w, 26, T['text'] if ok else T['dim'], anchor='mm', bold=True)
    for k, (px, py) in P.items():
        on = k in vis
        cv.rect((px - 34, py - 34, px + 34, py + 34), fill=T['green'] if on else T['panel2'],
                outline=T['orange'] if k == 4 else T['border'], width=5 if k == 4 else 2, r=34)
        cv.text((px, py), k, 34, T['bg'] if on else T['text'], anchor='mm', bold=True)
    cv.text((P[0][0], P[0][1] + 52), '起点', 20, T['muted'], anchor='mt')
    cv.text((P[4][0], P[4][1] + 52), '终点 n-1', 20, T['orange'], anchor='mt')
    if mid is not None:
        cv.text((x1 - 18, y0 + 4), f"mid = {mid}", 26, T['yellow'], anchor='ra', bold=True)


def _found(S, B, r):
    return '已到达终点' if S['n'] - 1 in S['vis'] else '终点还没到'


CONFIG = dict(
    num=3807, title='修复边以遍历图的最小成本', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 + 按层 BFS',
    tags=['二分算法', '图论算法'],
    code='''
class Solution(object):
    def minCost(self, n, edges, k):
        
        ma = 0
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))
            ma = max(ma, w)
        
        left = 1
        right = ma + 1

        while left < right:
            mid = (left + right) // 2
            q = [0]
            vis = set([0])
            head, tail = 0, 1
            step = 0
            while head < tail and step < k:
                for x in q[head: tail]:
                    for y, w in g[x]:
                        if w <= mid and y not in vis:
                            vis.add(y)
                            q.append(y)
                if n - 1 in vis:
                    break
                
                head, tail = tail, len(q)
                step += 1

            if n - 1 in vis:
                right = mid
            else:
                left = mid + 1
        
        if left == ma + 1:
            res = -1
        else:
            res = left
        
        return res
''',
    call=f'Solution().minCost(5, {EDGES}, 3)',
    expect=4,
    skip=['ma = 0', 'g = [[]', 'g[x].append', 'g[y].append', 'ma = max', 'head, tail = 0, 1', 'step = 0', 'for y, w in g[x]', 'for x in q[head', 'vis.add', 'q.append', 'vis = set', 'step += 1', 'q = [0]'],
    max_steps=110,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var=lambda S: S['q'] if 'q' in S and 'mid' in S else None, label='q（按层推进：head~tail 是当前这一层）',
             cell=80, pointers={'head': 'blue', 'tail': 'pink'}, h=170),
        dict(type='text', h=70, size=30,
             fn=lambda S: f"二分区间 `[{S['left']}, {S['right']})`" + (f"，试 `mid = {S['mid']}`，已走 `{S['step']}`/`{S['k']}` 层" if 'mid' in S and 'step' in S else '') if 'left' in S else ''),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('step', 'step'), ('k', 'k')],
    captions={
        'right = ma + 1': '上界取 `ma + 1 = {right}`：连它都不行，说明无解 → 返回 -1',
        'left = 1': '`money` 最小从 1 试起：`left = 1`',
        'while left < right': lambda S, B, r: (f'`left = {B.left} < right = {B.right}`：答案还在区间里，继续二分' if B.left < B.right
                                               else f'`left = right = {B.left}`：二分结束，最小可行成本就是它'),
        'mid = (left + right)': '`money` 越大可走的边越多 → 能二分。试 `mid = {mid}`：从 0 做 BFS，只走成本 ≤ {mid} 的边',
                'while head < tail and step < k': lambda S, B, r: (
            f'本层还有节点且只走了 `{B.step}` 步 < k={B.k}：再扩展一层' if B.head < B.tail and B.step < B.k
            else '队列空了，或已用满 k 步 → 这个 mid 判定结束'),
                'if w <= mid and y not in vis': lambda S, B, r: (
            f'边 `{B.x}→{B.y}` 成本 `{B.w}` ≤ {B.mid} 且没访问过 → ==可走=='
            if B.w <= B.mid and B.y not in B.vis
            else (f'边 `{B.x}→{B.y}` 成本 `{B.w}` > {B.mid}：修不起，跳过' if B.w > B.mid else f'`{B.y}` 已访问，跳过')),
                26: lambda S, B, r: ('终点已经在 `vis` 里 → 提前结束这次判定' if B.n - 1 in B.vis else '终点还没到，继续下一层（`q[head:tail]` 是下一层）'),
        'head, tail = tail, len(q)': '这一层走完（`step` 加 1，至多 k 步）：下一层 = 刚入队的 `q[{head}:{tail}]`',
        32: lambda S, B, r: ('`n-1` 在 `vis` 里 → 这个 mid 可行' if B.n - 1 in B.vis else '`n-1` 不在 `vis` 里 → 这个 mid 不够'),
        'right = mid': '`mid = {mid}` 够用 → 答案 ≤ mid，收缩上界 `right = {right}`',
        'left = mid + 1': '`mid = {mid}` 不够 → 答案 > mid，`left = {left}`',
        'if left == ma + 1': lambda S, B, r: ('`left` 停在 ma+1 → 连最大边权都到不了，无解' if B.left == B.ma + 1
                                              else f'`left = {B.left}` ≤ ma，说明确实找到了可行成本'),
        'res = left': '答案 `res = {res}`',
        'return res': '最小成本是 `{res}`',
    },
    cards=dict(
        one_liner='money 越大越容易到达：二分 money，BFS 判定',
        complexity='时间 `O((n+m) log W)`，空间 `O(n+m)`',
        problem=['无向图 `n` 个点，每条边有修复成本 `w`，初始全部损坏',
                 '求最小的 `money`：只修成本 ≤ money 的边，从 0 出发==至多走 k 条边==到 `n-1`',
                 '不存在则返回 -1',
                 '本视频：5 个点、`k = 3` → `4`'],
        quote='随着money的增大，就相当于在之前可用边的基础上新增了一些可用边，从0到达n - 1的可能性就越大，因此在这里可以==二分答案==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`money` 变大，可用边只增不减 → 单调，可以二分',
              '判定 `mid`：从 0 开始 BFS 扩展 k 轮，只走 `w <= mid` 的边',
              '`n-1` 进了 `vis` 就说明够用，收缩上界；否则 `left = mid + 1`'],
        summary=['时间 `O((n+m) log W)`，`W` 是最大边权',
                 '上界取 `ma + 1` 当哨兵：二分结束若 `left == ma + 1` 就是无解',
                 '易错：BFS 必须==按层==扩展并限制 `step < k`，不是普通的最短路',
                 '原文为 Python 2 风格，代码无需改动（整数除法已写成 `//`）'],
    ),
)
