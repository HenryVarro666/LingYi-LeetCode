def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    edges = S['edges']
    g = {}
    for a, b in edges:
        g.setdefault(a, []).append(b)
        g.setdefault(b, []).append(a)
    n = len(g)
    pos, dep, nxt = {}, {}, [0]

    def go(x, fa, d):
        kids = [y for y in sorted(g[x]) if y != fa]
        if not kids:
            pos[x] = nxt[0]
            nxt[0] += 1
        else:
            for y in kids:
                go(y, x, d + 1)
            pos[x] = sum(pos[y] for y in kids) / len(kids)
        dep[x] = d
    go(0, -1, 0)
    mw, md = max(nxt[0] - 1, 1), max(dep.values())
    cv.text((x0 + 18, y0 + 4), '无向树：黄 = 当前这一层，绿 = 已访问，蓝 = 本轮 BFS 起点', 22, T['muted'], bold=True)
    R = 30
    w, h = x1 - x0 - 2 * R - 80, y1 - y0 - 2 * R - 90
    P = {k: (x0 + 40 + R + pos[k] / mw * w, y0 + 56 + R + dep[k] / max(md, 1) * h) for k in g}
    for a, b in edges:
        cv.line([P[a], P[b]], T['dim'], 4)
    q, head, tail = S.get('q', []), S.get('head', 0), S.get('tail', 0)
    vis = S.get('vis', set())
    layer = set(q[head:tail]) if 'head' in S else set()
    start = q[0] if q else None
    for k in g:
        cx, cy = P[k]
        c = None
        if k in layer:
            c = 'yellow'
        elif k == start:
            c = 'blue'
        elif k in vis:
            c = 'green'
        cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=T[c] if c else T['panel2'], outline=T['border'], width=3)
        cv.text((cx, cy), k, 28, T['bg'] if c else T['text'], anchor='mm', bold=True)


def _info(S):
    if 'q' not in S:
        return ''
    if 'res' in S:
        return f"第 2 轮 BFS：从最远点 `{S['q'][0]}` 出发，已走了 `res = {S['res']}` 层"
    return f"第 1 轮 BFS：从 `0` 出发，找离它最远的点（队列最后一个）"


_t = dict(k=0, nb=0)


def _while(S):
    _t['k'] = 0
    return None


def _fornow(S, B, r):
    if _t['k'] < S.tail - S.head:
        _t['k'] += 1
        _t['nb'] = 0
        return f'取出这一层的下一个点 `{S._inner["now"]}`'
    return '这一层的点都处理完了'


def _fornext(S, B, r):
    nbs = sorted(S._inner['g'][S._inner['now']])
    if _t['nb'] < len(nbs):
        _t['nb'] += 1
        return f'看 `{S._inner["now"]}` 的邻居 `{S._inner["next"]}`'
    return f'`{S._inner["now"]}` 的邻居都看完了'


CONFIG = dict(
    num=1245, title='树的直径', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='两次 BFS',
    tags=['动态规划', '链表树与回溯'],
    code='''
class Solution(object):
    def treeDiameter(self, edges):

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            g[x].add(y)

            if y not in g:
                g[y] = set()
            g[y].add(x)
        
        q = [0]
        vis = set([0])
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                for next in g.get(now, set()):
                    if next not in vis:
                        q.append(next)
                        vis.add(next)
            
            head, tail = tail, len(q)
        
        now = q[-1]
        q = [now]
        res = 0
        vis = set([now])
        head, tail = 0, 1
        while head < tail:
            res += 1
            for now in q[head : tail]:
                for next in g.get(now, set()):
                    if next not in vis:
                        q.append(next)
                        vis.add(next)
            
            head, tail = tail, len(q)
        
        return res - 1
''',
    call='Solution().treeDiameter([[0,1],[1,2],[1,3],[3,4]])',
    expect=3,
    skip=['g = {}', 'for x, y in edges', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()', 'g[x].add', 'g[y].add'],
    max_steps=120,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='array', var='q', label='队列 q（黄框 = 当前这一层 q[head:tail]）', window=('head', 'tail - 1'),
             pointers={'head': 'blue'}, h=190),
        dict(type='text', fn=_info, h=60, size=24),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('res', 'res', 'green')],
    captions={
        'q = [0]': '第一轮 BFS：任选一个点（0）出发，队列 `q = [0]`',
        'vis = set([0])': '`vis` 记录已经入队的点，防止走回头路',
        'head, tail = 0, 1': '`q[head:tail]` 表示当前这一层：现在只有起点',
        'while head < tail': lambda S, B, r: _while(S) or (f'这一层有 `{S.tail - S.head}` 个点，继续扩展' if S.head < S.tail else '这一层是空的 → BFS 结束，最后入队的点离起点最远'),
        'for now in q': _fornow,
        'for next in g.get': _fornext,
        'if next not in vis': lambda S, B, r: (f'`{S.next}` 没访问过 → 放进下一层' if S.next not in B.vis else f'`{S.next}` 已访问过 → 跳过（它是父亲）'),
        'q.append(next)': '`{next}` 加到队列末尾：队列 → {q}',
        'vis.add(next)': '标记 `{next}` 已访问',
        'head, tail = tail, len(q)': '这一层结束：新的一层是 `q[{head}:{tail}]` = {q[head:tail]}',
        'now = q[-1]': '第一轮最后入队的点 `{now}` 离 0 最远，它必是直径的一个端点',
        'q = [now]': '第二轮 BFS：从端点 `{now}` 出发',
        'res = 0': '`res` 数层数',
        'vis = set([now])': '重新开始记录已访问',
        'res += 1': '又走了一层：`res = {res}`',
        'return res - 1': '最后一层是空层，多数了一次 → 直径 = `res - 1` = =={ret}==',
    },
    cards=dict(
        one_liner='两次 BFS：先找最远点，再从最远点出发数层数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一棵无向树的边 `edges`，求直径：树中任意两点最长路径的==边数==',
                 '示例：`[[0,1],[0,2]]` → `2`',
                 '本视频：5 个点，直径是 `4-3-1-0`，共 3 条边'],
        quote='最经典的做法就是两次bfs，即从树中任意节点开始bfs走到距离最远的节点，然后从这个最远的节点再进行一次bfs走到最远的节点，这两个节点的距离就是树的直径了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先建邻接表 `g`（点 → 邻居集合）',
              '第一轮从 0 出发 BFS，最后入队的点必是某条直径的端点',
              '第二轮从这个端点 BFS，层数 `res` 减 1 就是直径'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`q[head:tail]` 是一层；`head, tail = tail, len(q)` 切到下一层',
                 '最后循环多数一层空层，所以返回 `res - 1`',
                 '`vis` 第二轮要重置；只有一个点（无边）时 `g` 为空，用 `g.get` 兜底',
                 '原文是 Python 2 风格写法，在 Python 3 下无需改动'],
    ),
)
