def _rooted(edges, root=0):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    kids, seen, qq = {}, {root}, [root]
    for x in qq:
        for y in adj.get(x, []):
            if y not in seen:
                seen.add(y)
                kids.setdefault(x, []).append(y)
                qq.append(y)
    return kids


def _layout(kids, root=0):
    pos, slot = {}, [0]

    def go(x, d):
        ks = kids.get(x, [])
        if not ks:
            pos[x] = (slot[0], d)
            slot[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            pos[x] = ((pos[ks[0]][0] + pos[ks[-1]][0]) / 2, d)
    go(root, 0)
    return pos, slot[0], max(d for _, d in pos.values()) + 1


def _pre(kids, root=0):
    order, end = [], {}

    def go(x):
        order.append(x)
        for k in kids.get(x, []):
            go(k)
        end[x] = len(order) - 1
    go(root)
    return order, end


def _draw_tree(cv, box, T, kids, pos, nl, nd, node_fn, edge_fn=None, title='', rad=28):
    import math
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    top, bot = y0 + 90, y1 - 66
    dy = min(120, (bot - top) / max(nd - 1, 1))
    dx = min(150, (x1 - x0 - 160) / max(nl - 1, 1))
    cx = (x0 + x1) / 2 - dx * (nl - 1) / 2
    P = lambda n: (cx + pos[n][0] * dx, top + pos[n][1] * dy)
    for a, ks in kids.items():
        for b in ks:
            (ax, ay), (bx, by) = P(a), P(b)
            e = edge_fn(a, b) if edge_fn else {}
            col = e.get('color', T['border'])
            w = e.get('width', 3)
            L = math.hypot(bx - ax, by - ay)
            ux, uy = (bx - ax) / L, (by - ay) / L
            p0, p1 = (ax + ux * rad, ay + uy * rad), (bx - ux * rad, by - uy * rad)
            ar = e.get('arrow')
            if ar == 'down':
                cv.arrow(p0, p1, col, w, 14)
            elif ar == 'up':
                cv.arrow(p1, p0, col, w, 14)
            elif e.get('dashed'):
                cv.dashed(p0, p1, col, w)
            else:
                cv.line([p0, p1], col, w)
            if e.get('label') is not None:
                mx, my = (ax + bx) / 2, (ay + by) / 2
                lx, ly = mx + (18 if bx >= ax else -18) + (-uy * 0), my - 4
                cv.text((lx + (10 if bx >= ax else -10), ly), e['label'], 22, e.get('lcolor', T['yellow']), anchor='mm', bold=True)
    for n in pos:
        X, Y = P(n)
        s = node_fn(n)
        fill = s.get('fill', T['panel2'])
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=s.get('outline', T['border']), width=s.get('ow', 2))
        cv.text((X, Y), n, 26, s.get('tc', T['text']), anchor='mm', bold=True)
        if s.get('sub'):
            cv.text((X, Y + rad + 6), s['sub'], 20, s.get('subc', T['muted']), anchor='mt', bold=True)
        if s.get('tag'):
            cv.text((X + rad + 8, Y), s['tag'], 19, s.get('tagc', T['yellow']), anchor='lm', bold=True)

_CODE = '''
class Solution(object):
    def reachableNodes(self, n, edges, restricted):

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            
            g[x].add(y)
            g[y].add(x)
        
        q = [0]
        l = 0
        r = 1
        used = set(restricted)
        used.add(0)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                if next not in used:
                    used.add(next)
                    q.append(next)
                    r += 1
        
        return len(q)
'''
_LINES = _CODE.strip('\n').split('\n')
_EDGES = [[0, 1], [0, 2], [0, 5], [0, 4], [3, 2], [6, 5]]
_RES = [4, 2, 1]
_KIDS = _rooted(_EDGES)
_POS, _NL, _ND = _layout(_KIDS)


def _draw(cv, S, B, box, T):
    g, q = S.get('g'), S.get('q')
    src = _LINES[S['_line'] - 1]
    now = S.get('now') if q is not None and 'while' not in src and 'return' not in src else None
    nxt = S.get('next') if now is not None else None
    used = S.get('used')

    def node(n):
        if n in _RES:
            return dict(fill=T['red'], tc=T['bg'], tag='受限', tagc=T['red'])
        if n == now:
            return dict(fill=T['green'], tc=T['bg'], outline=T['yellow'], ow=5, tag='now', tagc=T['yellow'])
        if q is not None and n in q:
            return dict(fill=T['green'], tc=T['bg'], tag='next' if n == nxt else None, tagc=T['pink'])
        if n == nxt:
            return dict(outline=T['pink'], ow=5, tag='next', tagc=T['pink'])
        return {}

    def edge(a, b):
        if now is not None and nxt is not None and {a, b} == {now, nxt}:
            return dict(color=T['yellow'], width=6)
        if g is not None and b in g.get(a, ()):
            return dict(color=T['blue'], width=4)
        return dict(color=T['dim'], dashed=True, width=3)
    _draw_tree(cv, box, T, _KIDS, _POS, _NL, _ND, node, edge, '图（红 = 受限，绿 = 已入队，黄 = 正在处理的 now）')


CONFIG = dict(
    num=2368, title='受限条件下可到达节点的数目', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS：受限点不入队',
    tags=['链表树与回溯', '难度分 1477'],
    code=_CODE,
    call='Solution().reachableNodes(7, [[0,1],[0,2],[0,5],[0,4],[3,2],[6,5]], [4,2,1])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='q', label='队列 q（蓝箭头 = 队头 l）', pointers={'l': 'blue'}, cell=64, h=120),
        dict(type='set', var='used', label='used（受限点 + 已入队的点）', h=90),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('now', lambda S: S.get('now') if 'q' in S else None, 'yellow'), ('next', lambda S: S.get('next') if 'q' in S else None, 'pink')],
    skip=['if x not in g', 'g[x] = set()', 'if y not in g', 'g[y] = set()'],
    max_steps=95,
    captions={
        'g = {}': '`g` 是邻接表：`g[x]` 存和 x 相连的所有点',
        'for x, y in edges': lambda S, B, ret: (f'取一条边 `({S.x}, {S.y})`' if B.get('x') != S.x or B.get('y') != S.y
                                                else '所有边都读完了，图建好了'),
        'g[x].add(y)': '`g[{x}]` 里加 `{y}`',
        'g[y].add(x)': '无向图，反过来 `g[{y}]` 里加 `{x}`',
        'q = [0]': 'BFS 从 `0` 号节点出发：`q = [0]`',
        'l = 0': '`l` 是队头下标，`q[l]` 是下一个要处理的点',
        'r = 1': '`r` 是队尾，队里现在有 `r = 1` 个点',
        'used = set(restricted)': '把受限点直接放进 `used`：==以后既不访问，也不会入队== → `{used}`',
        'used.add(0)': '`0` 已经在队里，也标记成已用，防止回头',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：队里还有没处理的点 → 继续' if S.l < S.r
                                          else f'`l = {S.l} = r = {S.r}`：队列处理完了 → 结束'),
        'now = q[l]': '取队头：`now = q[{l}] = {now}`',
        'l += 1': '`now` 出队：`l` → {l}',
        'for next in': lambda S, B, ret: (f'枚举 `{S.now}` 的邻居 `next = {S.next}`' if S.get('next') is not None and B.get('next') != S.next or B.get('now') != S.now and S.get('next') is not None
                                          else f'`{S.now}` 的邻居都看完了'),
        'if next not in used': lambda S, B, ret: (f'`{S.next}` 不在 `used` 里 → 第一次到，==可以入队==' if S.next not in S.used
                                                   else f'`{S.next}` 已经在 `used` 里（受限或已入队）→ 跳过'),
        'used.add(next)': '先标记 `{next}` 已用，别的点不会重复入队',
        'q.append(next)': '`{next}` 入队 → `q = {q}`',
        'r += 1': '队尾后移：`r` → {r}',
        'return len(q)': '队列里每个点都是从 0 出发能到的 → 共 =={ret}== 个',
    },
    cards=dict(
        one_liner='BFS 时受限点不访问、不入队，队列长度就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，从节点 `0` 出发，==不能访问受限节点==，最多能到几个点',
                 '示例：`restricted = [4, 2, 1]`，`0` 的邻居 `1、2、4` 都受限',
                 '只剩 `0 → 5 → 6` 能走，答案 `3`'],
        quote='直接从0号节点开始进行bfs，在过程中既不要访问受限节点，也不要将其加入到bfs队列中。bfs完成后，队列的长度就是可到节点的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把受限点放进 `used`，BFS 里 `next not in used` 一判断就把它们挡在门外',
              '队列 `q` 里装的全是真正到达过的点，所以最后 `len(q)` 就是答案',
              '`l`、`r` 是手写的队头、队尾，不用 `deque`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '==受限点要预先放进 used==，否则会被当成普通点入队',
                 '`0` 也要标记成已用，不然会从邻居走回 `0`',
                 '原文是 Python 2 风格写法，本题代码在 Python 3 下无需改动',
                 '对比灵神：灵神建树时就不连受限边，再 DFS 计数；这里保留全图，BFS 时拦截'],
    ),
)
