EDGES = [[0, 2], [1, 2], [2, 3], [0, 3]]
POS = {0: (0.04, 0.1), 1: (0.04, 0.9), 2: (0.5, 0.5), 3: (0.96, 0.5)}


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    if 'f' not in S or 'ind' not in S:
        return
    now, nxt = S.get('now'), S.get('next')
    done = set(S['q'][:S['l']]) if 'l' in S and 'q' in S else set()
    inq = set(S['q']) if 'q' in S else set()
    gw = (x1 - x0) * 0.56
    R = 32

    def P(u):
        fx, fy = POS[u]
        return x0 + 50 + fx * (gw - 100), y0 + 40 + fy * (y1 - y0 - 140)

    for a, b in EDGES:
        (ax, ay), (bx, by) = P(a), P(b)
        d = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        hot = now == a and nxt == b
        cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 4), by - uy * (R + 4)),
                 T['yellow'] if hot else T['muted'], 6 if hot else 3, 16 if hot else 12)
    for u in range(4):
        X, Y = P(u)
        if u == now:
            fill = T['blue']
        elif u in done:
            fill = T['green']
        elif u in inq:
            fill = T['cyan']
        else:
            fill = T['panel2']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill,
                     outline=T['yellow'] if u == nxt else T['border'], width=6 if u == nxt else 2)
        cv.text((X, Y), u, 30, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + R + 8), f"入度 {S['ind'][u]}", 20, T['orange'] if S['ind'][u] == 0 else T['muted'], anchor='mt')
    cv.text((x0 + 20, y1 - 22), '蓝 = 正在处理 now，绿 = 已出队，青 = 在队列里，黄圈 = next', 20, T['dim'], anchor='lm')
    lx = x0 + gw + 30
    cv.text((lx, y0 + 20), 'f[i]（i 的祖先集合）', 24, T['muted'], bold=True)
    for i in range(4):
        fresh = B.get('f') is not None and sorted(B['f'][i]) != sorted(S['f'][i])
        cv.text((lx, y0 + 70 + i * 54), f"f[{i}] = {{{', '.join(map(str, sorted(S['f'][i])))}}}", 30,
                T['yellow'] if fresh else T['text'], bold=fresh, mono=True)


def _ind(S, B, ret):
    nx = S.next
    if S.ind[nx] == 0:
        return f'`ind[{nx}]` 减到 0：{nx} 的前置节点全处理完了，f[{nx}] 已完整 → ==入队=='
    return f'`ind[{nx}] = {S.ind[nx]}`：还有前置节点没处理，先不入队'


CONFIG = dict(
    num=2192, title='有向无环图中一个节点的所有祖先', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='拓扑排序 + 集合并集',
    tags=['灵神题单', '图论算法', '难度分 1788'],
    code='''
class Solution(object):
    def getAncestors(self, n, edges):

        f = [set() for _ in range(n)]
        g = {}
        ind = [0] * n
        for x, y in edges:
            if x not in g:
                g[x] = set()
            g[x].add(y)
            ind[y] += 1
        
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)

        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                f[next].update(f[now])
                f[next].add(now)
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1

        res = []
        for i in range(n):
            res.append([])
            for j in range(n):
                if j in f[i]:
                    res[-1].append(j)
        
        return res
''',
    call='Solution().getAncestors(4, [[0,2],[1,2],[2,3],[0,3]])',
    expect=[[], [], [0, 1], [0, 1, 2]],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='queue', var='q', label='q（拓扑序队列）', h=120),
    ],
    watch=[('now', 'now', 'blue'), ('next', 'next', 'yellow'), ('l', 'l', 'cyan'), ('r', 'r', 'cyan')],
    skip=['f = [set()', 'g = {}', 'ind = [0]', 'for x, y in edges', 'if x not in g', 'g[x] = set()', 'l = 0', 'r = len(q)',
          'for index in range', 'for next in g.get', 'res.append([])', 'for j in range', 'for i in range(n)', 'if j in f[i]', 'r += 1', 'res = []', 'l += 1', 'q = []'],
    max_steps=90,
    captions={
        'g[x].add(y)': '建图：边 `{x} → {y}`，{y} 成为 {x} 的后继',
        'ind[y] += 1': '统计入度：`ind[{y}]` = {ind[y]}（前置节点个数）',
        'if ind[index] == 0': '`ind[{index}] = {ind[index]}`：入度为 0 才能作为拓扑排序起点',
        'q.append(index)': '`{index}` 没有前置节点 → 入队，队列 `{q}`',
        'while l < r': lambda S, B, ret: (f'队列还有元素（`l = {S.l} < r = {S.r}`）→ 继续' if S.l < S.r
                                          else f'`l = r = {S.r}`：队列空了，所有点的 f 都算完'),
        'now = q[l]': '取队头 `now = {now}`：它的 f 已经完整',
        'f[next].update(f[now])': '`{next}` 继承 `{now}` 的全部祖先：`f[{next}]` ∪= `{sorted(f[now])}`',
        'f[next].add(now)': '`{now}` 自己也是 `{next}` 的祖先：`f[{next}] = {sorted(f[next])}`',
        'ind[next] -= 1': '`{now} → {next}` 这条前置边处理完：`ind[{next}]` → {ind[next]}',
        'if ind[next] == 0': _ind,
        'q.append(next)': '入队：`q = {q}`',
        'res[-1].append(j)': '`{j}` 在 `f[{i}]` 里 → 加入 `res[{i}]`（按 j 升序，所以结果有序）',
        'return res': '集合转成升序列表：`{ret}`',
    },
    cards=dict(
        one_liner='拓扑排序：祖先集合 = 所有前置节点的祖先并集 + 前置节点本身',
        complexity='时间约 `O(n·(n+m))`，空间 `O(n²)`',
        problem=['有向无环图 `n` 个点，求每个点的所有祖先（能走到它的点），升序',
                 '示例：`n=5` 的完全图 → `[[],[0],[0,1],[0,1,2],[0,1,2,3]]`',
                 '本视频：`n=4`，边 `0→2,1→2,2→3,0→3`'],
        quote='非常典型的拓扑排序问题。使用f[i]表示i的所有祖先构成的集合，那么对于节点i而言，f[i]就是其所有前置节点对应f的并集，再加上其所有的前置节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 用集合存：多个前置节点的祖先会重复，集合自动去重',
              '拓扑序保证：处理 `now` 时，它的 `f[now]` ==已经完整==',
              '把 `now` 的祖先和 `now` 自己，一起传给它的每个后继'],
        summary=['时间 `O(n·(n+m))` 量级（集合并集），空间 `O(n²)`',
                 '==后继 += 自己的祖先 + 自己==，两步缺一不可',
                 '最后按 `j` 从小到大扫一遍集合，才能得到升序列表',
                 '依赖「无环」：有环时入度永远减不到 0',
                 '对比灵神：灵神用 DFS 枚举起点，yiduobo 用拓扑序一趟传递'],
    ),
)
