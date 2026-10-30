FLOWER = ['blue', 'pink', 'green', 'orange']


def _cur(S):
    inn = S.get('_inner') or {}
    return inn.get('now', S.get('x'))


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    n = S['n']
    color = S.get('color')
    g = S.get('g') or {}
    cur = _cur(S) if color is not None else None
    nbrs = set(g.get(cur, ())) if cur is not None else set()
    cv.text((x0 + 18, y0 + 4), '花园（黄框 = 当前 dfs 到的点，粉框 = 它的邻居；灰 = 还没染色）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 14
    R = min((x1 - x0) / 2 - 90, (y1 - y0) / 2 - 62)
    pos = {}
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        pos[k + 1] = (cx + R * math.cos(a), cy + R * math.sin(a))
    for a, b in S['paths']:
        hot = cur is not None and ((a == cur and b in nbrs) or (b == cur and a in nbrs))
        cv.line([pos[a], pos[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    for v in range(1, n + 1):
        X, Y = pos[v]
        c = color[v] if color is not None else 0
        fill = T[FLOWER[c - 1]] if 1 <= c <= 4 else T['panel2']
        if v == cur:
            cv.rect((X - 38, Y - 38, X + 38, Y + 38), outline=T['yellow'], width=5, r=38)
        elif v in nbrs:
            cv.rect((X - 36, Y - 36, X + 36, Y + 36), outline=T['pink'], width=4, r=36)
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=fill, outline=T['border'], width=2, r=30)
        cv.text((X, Y), v, 30, T['bg'] if 1 <= c <= 4 else T['muted'], anchor='mm', bold=True)
    for k in range(4):
        X, Y = x1 - 150, y0 + 40 + k * 34
        cv.rect((X, Y, X + 24, Y + 24), fill=T[FLOWER[k]], r=6)
        cv.text((X + 34, Y + 12), f'花 {k + 1}', 22, T['text'], anchor='lm')


def _cand(S):
    cd = S.get('candidate')
    if cd is None:
        return ''
    cur = _cur(S)
    parts = []
    for v in range(1, S['n'] + 1):
        s = '{' + ','.join(str(k) for k in sorted(cd[v])) + '}'
        parts.append(f'==点{v} {s}==' if v == cur else f'点{v} {s}')
    return '各点还能用的花：' + '　'.join(parts)


CONFIG = dict(
    num=1042, title='不邻接植花', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='dfs 染色 · 候选集删减',
    tags=['灵神题单', '难度分 1712'],
    code='''
class Solution(object):
    def gardenNoAdj(self, n, paths):

        g = {}
        for x, y in paths:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        color = [0] * (n + 1)
        candidate = [set([1, 2, 3, 4]) for _ in range(n + 1)]
        for x in range(1, n + 1):
            if color[x] == 0:
                self.dfs(x, color, candidate, g)
        
        return color[1:]
    
    def dfs(self, now, color, candidate, g):
        c = candidate[now].pop()
        color[now] = c
        if now in g:
            for next in g[now]:
                if color[next] == 0 and c in candidate[next]:
                    candidate[next].remove(c)
            for next in g[now]:
                if color[next] == 0:
                    self.dfs(next, color, candidate, g)
''',
    call='Solution().gardenNoAdj(5, [[1,2],[2,3],[3,1],[3,4],[4,5]])',
    expect=[1, 2, 3, 1, 2],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: S['color'][1:], label='color[1:]（从左到右依次是点 1~5，0 = 未染色）', index=False, h=150,
             color=lambda S, i, v: (FLOWER[v - 1] if 1 <= v <= 4 else None)),
        dict(type='text', fn=_cand, h=60, size=26),
        dict(type='calls', h=130, hide=('color', 'candidate', 'g')),
    ],
    watch=[('now', "now", 'yellow'), ('c', 'c', 'cyan'), ('next', 'next', 'pink')],
    captions={
        'g = {}': '`g` 邻接表：点 → 邻居集合',
        'g[x].add(y)': '路径 `{x}`-`{y}`：双向，两边都把对方加进邻居集合',
        'color = [0]': '`color[x]` 是点 x 的花，0 = 还没染；下标从 1 开始，所以长度 `n+1`',
        'candidate = ': '每个点各有一份候选集 `{{1,2,3,4}}`，邻居用掉的花会从里面删掉',
        'for x in range': lambda S, B, r: ('点都检查完了，循环结束' if getattr(B, 'x', None) == S.x and S.x == S.n else f'依次检查点 `{S.x}`（图可能不连通，所以每个点都要试一次）'),
        'if color[x] == 0': lambda S, B, r: (f'`color[{S.x}] = 0`：还没染色 → 从它开始 ==dfs==' if S.color[S.x] == 0
                                              else f'`color[{S.x}] = {S.color[S.x]}`：已被 dfs 染过，跳过'),
        'self.dfs(x': '从点 `{x}` 出发 dfs',
        'c = candidate[now].pop()': '点 `{now}` 从候选集里取一种花：`c = {c}`（邻居用过的已被删掉，一定还剩）',
        'color[now] = c': '点 `{now}` 染成花 ==`{c}`==；接着遍历它的邻居：==先删候选，再递归==',
        'if color[next] == 0 and c in': lambda S, B, r: (
            f'邻居 `{S.next}` 还没染色，候选里有 `{S.c}` 吗？{"有 → 删掉" if S.c in S.candidate[S.next] else "没有，不用删"}'
            if S.color[S.next] == 0 else f'邻居 `{S.next}` 已经染过色，不用管'),
        'candidate[next].remove(c)': '邻居 `{next}` 不能再用花 `{c}`，候选集 → `{sorted(candidate[next])}`',
        'if color[next] == 0:': lambda S, B, r: (f'邻居 `{S.next}` 还没染色 → 递归染它' if S.color[S.next] == 0
                                                  else f'邻居 `{S.next}` 已染色，跳过'),
        'self.dfs(next': '递归进入点 `{now}`：它的候选集已排除邻居用掉的花，现为 `{sorted(candidate[now])}`',
        'return color[1:]': '所有点都染好，去掉下标 0 → `{ret}`',
    },
    skip=['for x, y in paths', 'x not in g', 'y not in g', 'g[x] = set()', 'g[y] = set()', 'g[y].add(x)', 'for next in g[now]:', 'if now in g'],
    max_steps=120,
    cards=dict(
        one_liner='度数至多 3，邻居最多挡 3 种花，总剩一种',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`n` 个花园，`paths` 为双向路径，每个花园至多 3 条路',
                 '每园种 1~4 号花之一，==相连的两园花不同==，返回任一方案',
                 '示例：`n=4, paths=[[1,2],[3,4]]` → `[1,2,1,2]`'],
        quote='对于任意节点而言，即使其相邻的三个节点都是不同的颜色，那么依然剩下一种颜色可以使用，因此实际上完全不需要什么复杂的策略',
        quote_src='—— yiduobo 题解原文',
        idea=['每个点配一个候选集 `{1,2,3,4}`，染色时从中 `pop` 一种花',
              '染完一个点，立刻把这种花从==未染色邻居==的候选集中删掉',
              '再对未染色的邻居 dfs；每个点度数 ≤ 3，候选集永远不会被删空'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：图可能不连通，所以外层要对每个未染色点都启动 dfs',
                 '候选集只删==未染色==邻居的；已染色邻居的花已经定下，不会冲突（它染时已把花从本点候选里删了）',
                 '原文可直接在 Python 3 运行，未做修改（`set.pop()` 取到哪种花不限，答案任一可行）',
                 '对比灵神：灵神按编号一遍扫，查邻居已用颜色；yiduobo 反过来，染色时向邻居“广播”禁用的颜色'],
    ),
)
