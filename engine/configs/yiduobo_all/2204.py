EDGES = [[0, 1], [0, 2], [0, 3], [1, 2], [2, 6], [3, 4], [3, 5], [6, 7], [6, 8]]
POS = {0: (0.12, 0.30), 1: (0.12, 0.85), 2: (0.34, 0.55), 3: (0.34, 0.08), 4: (0.64, 0.00),
       5: (0.52, 0.30), 6: (0.62, 0.62), 7: (0.86, 0.45), 8: (0.86, 0.90)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '无向图（橙 = 已被剥掉的叶子，蓝 = 环上的点，绿 = 刚算出距离）', 22, T['muted'], bold=True)
    gx0, gy0, gw, gh = x0 + 60, y0 + 70, (x1 - x0) - 120, (y1 - y0) - 160
    P = {k: (gx0 + v[0] * gw, gy0 + v[1] * gh) for k, v in POS.items()}
    d, inq, linked, res = S.get('d'), S.get('inq'), S.get('linked'), S.get('res')
    peeled = lambda i: inq is not None and inq[i]
    fin = res is not None
    for x, y in EDGES:
        a, b = P[x], P[y]
        gone = (peeled(x) and linked and linked[x] == y) or (peeled(y) and linked and linked[y] == x)
        if gone:
            cv.dashed(a, b, T['dim'], 3)
        else:
            cv.line([a, b], T['muted'], 4)
    now = S.get('now')
    for i, (px, py) in P.items():
        col = (60, 66, 76)
        if peeled(i):
            col = T['orange']
        elif fin:
            col = T['blue']
        if now == i and not fin:
            col = T['yellow']
        r = 30
        cv.d.ellipse((px - r, py - r, px + r, py + r), fill=col, outline=T['border'], width=3)
        cv.text((px, py), i, 30, T['bg'] if col != (60, 66, 76) else T['text'], anchor='mm', bold=True)
        if fin or d is not None:
            cv.rect((px + r + 2, py - 16, px + r + 84, py + 22), fill=T['bg'], r=6)
        if fin:
            cv.text((px + r + 6, py + 4), f'dis={res[i]}', 22, T['green'], anchor='lm', bold=True)
        elif d is not None:
            cv.text((px + r + 6, py + 4), f'度={d[i]}', 22, T['cyan'], anchor='lm', bold=True)


CONFIG = dict(
    num=2204, title='无向图中到环的距离', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='拓扑排序剥叶子 + 倒推',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def distanceToCycle(self, n, edges):
        
        d = [0] * n
        g = [[] for _ in range(n)]
        for x, y in edges:
            d[x] += 1
            d[y] += 1
            g[x].append(y)
            g[y].append(x)
        
        q = []
        inq = [False] * n
        for index in range(n):
            if d[index] == 1:
                q.append(index)
                inq[index] = True
        
        linked = [None] * n
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                if not inq[next]:
                    linked[now] = next
                    d[next] -= 1
                    if d[next] == 1:
                        q.append(next)
                        inq[next] = True
                        tail += 1

        res = [0] * n
        for now in q[::-1]:
            res[now] = res[linked[now]] + 1
        
        return res
''',
    call='Solution().distanceToCycle(9, %s)' % EDGES,
    expect=[0, 0, 0, 1, 2, 2, 1, 2, 2],
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='array', var='q', label='队列 q（剥叶子的顺序）', pointers={'head': 'blue'}, h=170),
    ],
    watch=['now', 'head', 'tail', ('q', 'q', 'orange')],
    skip=['d = [0] * n', 'g = [[]', 'for x, y in edges', 'd[x] += 1', 'd[y] += 1', 'g[x].append', 'g[y].append',
          'q = []', 'inq = [', 'for index in range', 'linked = [None]', 'head, tail', 'tail += 1', 'res = [0]',
          'q.append(index)', 'inq[index] = True', 'head += 1', 'for next in g[now]', 'for now in q[::-1]'],
    max_steps=90,
    captions={
        'if d[index] == 1': lambda S, B, r: (f'`d[{S.index}] = 1` → 叶子，必不在环上，入队' if S.d[S.index] == 1
                                              else f'`d[{S.index}] = {S.d[S.index]}`，不是叶子，先放着'),
        'if not inq[next]': lambda S, B, r: (f'`{S.next}` 还没被剥掉 → 它是 `{S.now}` 唯一剩下的邻居' if not S.inq[S.next]
                                              else f'`{S.next}` 已在队里（是更早剥掉的叶子）→ 跳过'),
        'linked[now] = next': '记下：`{now}` 的对面是 `{next}`，`dis[{now}] = dis[{next}] + 1`（以后倒推）',
        'd[next] -= 1': '删掉叶子 `{now}` 和它的边，`{next}` 的度减为 `{d[next]}`',
        'if d[next] == 1': lambda S, B, r: (f'`{S.next}` 的度变成 1 → 新的叶子，入队' if S.d[S.next] == 1
                                             else f'`{S.next}` 的度是 `{S.d[S.next]}`（≥ 2）→ 还连着别的点，暂不剥'),
        'while head < tail': lambda S, B, r: ('队里还有叶子没处理，继续' if S.head < S.tail else '队空了：图中剩下的就是环，环上点距离为 0'),
        'now = q[head]': '取出队首叶子 `{now}`',
        'res[now] = res[linked[now]] + 1': '倒推：`res[{now}] = res[{linked[now]}] + 1` = =={res[now]}==（后剥的离环更近，所以倒着算）',
        'return res': '全部点到环的距离：`{res}`',
    },
    cards=dict(
        one_liner='不停剥掉度为 1 的叶子，剩下的就是环，再倒着推距离',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向连通图，==恰好有一个环==，`n` 个点、`n` 条边',
                 '求每个点到环上最近点的距离（环上的点距离为 0）',
                 '示例：`n = 9`，输出 `[0,0,0,1,2,2,1,2,2]`'],
        quote='度为1的节点，这些度为1的节点必然不在环中。如果将这些节点以及与之相连的边从图中移除，就可能得到另一批新的度为1的节点，那么只需重复这个过程，直到图中仅剩那个环为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['度为 1 的点一定不在环上：入队、删边，邻居度数减 1',
              '邻居度数变成 1 又成了新叶子，如此一层层剥，剩下的全在环上',
              '每个被剥的点记下「对面」的点：`dis[叶子] = dis[对面] + 1`',
              '倒着遍历队列：后剥的先算，对面的距离一定已经算好'],
        summary=['时间 `O(n)`：每个点入队一次，每条边处理一次',
                 '环上的点永远不会变成度 1，所以 `res` 保持 0',
                 '倒序遍历队列是关键：保证 `res[linked[now]]` 已经算完',
                 '原文为 Python 2 风格，但在 Python 3 下无需改动，代码照搬',
                 '同类：灵神讲的「基环树 + 拓扑排序」，无向版本改成判断度数 1'],
    ),
)
