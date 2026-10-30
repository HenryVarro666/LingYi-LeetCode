def _graph(cv, box, T, title, POS, EDGES, fill, label=None, ecol=None, elab=None, directed=False, ring=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 21, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 120, y1 - y0 - 110
    P = {k: (x0 + 60 + Wd * a, y0 + 66 + Hd * b) for k, (a, b) in POS.items()}
    R = 30
    for e in EDGES:
        a, b = e[0], e[1]
        col, wd = ecol(e) if ecol else (T['border'], 4)
        (ax, ay), (bx, by) = P[a], P[b]
        if directed:
            d = max(1.0, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5)
            ux, uy = (bx - ax) / d, (by - ay) / d
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 3), by - uy * (R + 3)), col, wd, head=16)
        else:
            cv.line([P[a], P[b]], col, wd)
        if elab:
            mx, my = (ax + bx) / 2, (ay + by) / 2
            s = elab(e)
            cv.rect((mx - 22, my - 16, mx + 22, my + 16), fill=T['bg'], r=8)
            cv.text((mx, my), s, 22, col, anchor='mm', bold=True)
    for k, (px, py) in P.items():
        f = fill(k)
        cv.rect((px - R, py - R, px + R, py + R), fill=f or T['panel2'], outline=T['border'], r=R)
        cv.text((px, py), k if label is None else label(k), 32, T['bg'] if f else T['muted'], anchor='mm', bold=True)
        if ring is not None and ring == k:
            cv.rect((px - R - 10, py - R - 10, px + R + 10, py + R + 10), outline=T['text'], width=5, r=R + 10)


POS = {0: (0.05, 0.15), 4: (0.28, 0.15), 5: (0.51, 0.15), 1: (0.76, 0.10), 2: (0.94, 0.85), 3: (0.58, 0.85)}
EDGES = [(1, 2), (2, 3), (3, 1), (0, 4), (4, 5)]


def _draw(cv, S, B, box, T):
    bugs = S.get('bugs')
    bugs = set(bugs) if bugs is not None else set()
    ln = S.get('_line', 0)
    inner = S.get('_inner') or {}
    cur = inner.get('x') if (17 <= ln <= 21 or 25 <= ln <= 27 or 30 <= ln <= 32) else None
    _graph(cv, box, T, '方法调用图（箭头 a→b 表示 a 调用 b；红 = bugs 里的可疑方法，白环 = 当前正在处理）', POS, EDGES,
           lambda k: T['red'] if k in bugs else None, directed=True, ring=cur,
           ecol=lambda e: ((T['red'], 5) if e[0] in bugs and e[1] in bugs else (T['border'], 4)))


CONFIG = dict(
    num=3310, title='移除可疑的方法', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS 找可疑方法 + 入度判断', tags=['灵神题单·图论算法', '难度分 1711'],
    code='''
class Solution(object):
    def remainingMethods(self, n, k, invocations):

        bugs = set()
        bugs.add(k)

        g = [set() for _ in range(n)]
        ind = [0] * n
        for x, y in invocations:
            if y not in g[x]:
                g[x].add(y)
                ind[y] += 1
            
        q = [k]
        head, tail = 0, 1
        while head < tail:
            for x in q[head : tail]:
                for y in g[x]:
                    if y not in bugs:
                        bugs.add(y)
                        q.append(y)
            
            head, tail = tail, len(q)

        for x in bugs:
            for y in g[x]:
                ind[y] -= 1
        
        flag = True
        for x in bugs:
            if ind[x] > 0:
                flag = False
        
        res = []
        for x in range(n):
            if x not in bugs or not flag:
                res.append(x)
        
        return res
''',
    call='Solution().remainingMethods(6, 1, [[1,2],[2,3],[3,1],[0,4],[4,5]])',
    expect=[0, 4, 5],
    views=[
        dict(type='custom', draw=_draw, h=270),
        dict(type='array', var='ind', label='ind（入度：被多少个方法调用）', h=150,
             color=lambda S, i, v: ('red' if i in (S.get('bugs') or ()) else None)),
        dict(type='set', var='bugs', label='bugs（可疑方法）', fmt=lambda x: str(x), h=90),
        dict(type='array', var='q', label='q（BFS 队列）', h=110),
    ],
    watch=['x', 'y', ('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('flag', 'flag', 'green')],
    captions={
        'bugs = set()': '`bugs` 收集所有可疑方法',
        'bugs.add(k)': '方法 `k = {k}` 自己就是可疑方法',
        'g = [set()': '`g[x]` 是方法 x 直接调用的方法集合',
        'ind = [0] * n': '`ind[i]` 是入度：有多少个方法调用了 i',
        'if y not in g[x]': lambda S, B, r: (f'边 `{S.x}→{S.y}` 第一次出现 → 记录' if S.y not in S.g[S.x] else f'边 `{S.x}→{S.y}` 重复了，不再计入度'),
        'g[x].add(y)': '记下 `{x}→{y}`',
        'ind[y] += 1': '`ind[{y}] = {ind[y]}`：`{y}` 又多了一个调用者',
        'q = [k]': 'BFS 队列从 `k` 开始',
        'head, tail = 0, 1': '`q[head:tail]` 是当前这一层，现在只有 `k`',
        'while head < tail': lambda S, B, r: (f'这一层 `q[{S.head}:{S.tail}]` 非空，继续扩展' if S.head < S.tail else '没有新的层了 → 所有可疑方法都找到了'),
        'if y not in bugs': lambda S, B, r: (f'`{S.x}` 调用了 `{S.y}`，它还不在 bugs → 新的可疑方法' if S.y not in S.bugs else f'`{S.y}` 已经是可疑方法，跳过'),
        'bugs.add(y)': '`{y}` 被可疑方法调用 → ==也是可疑方法==',
        'q.append(y)': '`{y}` 入队，下一层再扩展它',
        'head, tail = tail, len(q)': '这一层处理完，下一层范围是 `q[{head}:{tail}]`',
        'ind[y] -= 1': '扣掉「来自可疑方法」的调用：`ind[{y}] = {ind[y]}`',
        'flag = True': '`flag` 表示能不能删，先假设能',
        'if ind[x] > 0': lambda S, B, r: (f'可疑方法 `{S.x}` 的入度 = `{S.ind[S.x]}` > 0 → 还有==正常方法==在调用它' if S.ind[S.x] > 0 else f'可疑方法 `{S.x}` 入度扣完为 0 → 调用者全是可疑方法'),
        'flag = False': '有正常方法调用可疑方法 → 不能删，`flag = False`',
        'if x not in bugs or not flag': lambda S, B, r: (f'`{S.x}` 保留' if (S.x not in S.bugs or not S.flag) else f'`{S.x}` 是可疑方法且可以删 → 不加入结果'),
        'res.append(x)': '保留方法 `{x}` → `res = {res}`',
        'return res': '剩下的方法：=={ret}==',
    },
    skip=['res = []'],
    max_steps=140,
    cards=dict(
        one_liner='BFS 标出可疑方法，用入度判断有没有「外人」在调用',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`invocations[i] = [a, b]`：方法 a 调用了方法 b，方法 `k` 有 bug',
                 '`k` 及其直接/间接调用的方法都是可疑方法，要全部移除',
                 '只要还有正常方法调用可疑方法，就一个都不删',
                 '本例：`n=6, k=1` → `[0,4,5]`'],
        quote='对于方法k，以及所有被它直接或者间接调用的方法，都被称为可疑方法。……在建图时更新所有方法的入度，每个方法的入度就代表这个方法被多少其他方法调用过。',
        quote_src='—— yiduobo 题解原文',
        idea=['建有向图并同时记下每个方法的入度',
              '从 `k` 做 BFS，遍历到的都是可疑方法',
              '把「可疑方法发出的边」从入度里扣掉：==若可疑方法入度仍 > 0，说明被正常方法调用==，不能删'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '`g[x]` 用集合去重，避免重复边把入度算多',
                 '入度扣减只扣「可疑 → 可疑」的边，所以扣完应全为 0',
                 '本例没有正常方法调用可疑方法，所以真正删除；否则返回 `[0..n-1]`',
                 '对照灵神：灵神 DFS 标记后直接枚举边判断「非可疑 → 可疑」，不需要入度'],
    ),
)
