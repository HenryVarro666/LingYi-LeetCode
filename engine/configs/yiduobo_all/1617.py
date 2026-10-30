# ---------- 一般树的自绘（custom 视图）：按 children 布局，状态完全由当前步的变量推出 ----------
import math as _m


def _tree_pos(children, root, box, top=56, bottom=40):
    x0, y0, x1, y1 = box
    depth, leaf_x, pos = {}, [0], {}

    def go(u, d):
        depth[u] = d
        ks = children.get(u, [])
        if not ks:
            pos[u] = leaf_x[0]
            leaf_x[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            pos[u] = sum(pos[k] for k in ks) / len(ks)
    go(root, 0)
    nl, md = max(1, leaf_x[0]), max(depth.values()) + 1
    sp = min(110, (x1 - x0 - 60) / nl)
    dy = min(100, (y1 - y0 - top - bottom) / max(1, md))
    rad = max(16, min(26, sp * 0.36, dy * 0.3))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * (nl - 1)) / 2
    P = {u: (sx + pos[u] * sp, y0 + top + depth[u] * dy + rad) for u in depth}
    return P, rad


def _preorder(children, root):
    out = []

    def go(u):
        out.append(u)
        for k in children.get(u, []):
            go(k)
    go(root)
    return out


def _ancestors(parent, u):
    out = []
    while u is not None and u in parent:
        u = parent[u]
        if u is not None:
            out.append(u)
    return out


def draw_gtree(cv, T, box, children, root, parent, cur, hot=None, finished=(), badge=None, bad_edges=(),
               label_fn=None, color_fn=None, title=None, node_color=None):
    """cur: 当前递归节点；hot: 当前正在考察的子节点；finished: 已返回的节点集合；badge: {节点: 文字}"""
    P, rad = _tree_pos(children, root, box)
    if title:
        cv.text((box[0] + 18, box[1] + 4), title, 22, T['muted'], bold=True)
    for u, ks in children.items():
        for k in ks:
            bad = (u, k) in bad_edges
            isc = hot is not None and u == cur and k == hot
            c = T['pink'] if isc else (T['red'] if bad else T['border'])
            if bad and not isc:
                cv.dashed(P[u], P[k], c, 3, 10, 7)
            else:
                cv.line([P[u], P[k]], c, 6 if isc else 3)
    anc = set(_ancestors(parent, cur)) if cur is not None else set()
    for u, (X, Y) in P.items():
        fill, outl, w, tc = T['panel2'], T['border'], 2, T['text']
        if u in finished:
            fill, tc = T['green'], T['bg']
        if node_color and node_color(u):
            fill, tc = T[node_color(u)], T['bg']
        if u in anc:
            outl, w = T['yellow'], 4
        if u == hot:
            outl, w = T['pink'], 5
        if u == cur:
            outl, w = T['blue'], 5
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outl, width=w)
        cv.text((X, Y), label_fn(u) if label_fn else u, int(rad * 0.95), tc, anchor='mm', bold=True)
        if badge and u in badge:
            s = badge[u]
            bw = cv.tlen(s, 19, bold=True) + 14
            cv.rect((X - bw / 2, Y + rad + 4, X + bw / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
            cv.text((X, Y + rad + 16), s, 19, T['green'], anchor='mm', bold=True)


def _subtree(children, u):
    out = [u]
    for k in children.get(u, []):
        out += _subtree(children, k)
    return out


def fin_set(CH, ORDER, PAR, x, y, line, call_line, for_line, ret_line, yb):
    """已返回的节点：x 之前先序出现且不在栈上的、x 已处理完的孩子子树、（return 行上的）x 自己"""
    if x is None:
        return set()
    anc = set(_ancestors(PAR, x))
    fin = {u for u in ORDER[:ORDER.index(x)] if u not in anc}
    ks = CH[x]
    ended = (y is not None and yb == y and line == for_line) or line == ret_line
    if ended:
        for k in ks:
            fin |= set(_subtree(CH, k))
    elif y in ks:
        for k in ks:
            if ks.index(k) < ks.index(y) or (k == y and line > call_line):
                fin |= set(_subtree(CH, k))
    if line == ret_line:
        fin.add(x)
    return fin

N = 3
ROOT = 1   # 只用于布局：路径 0-1-2 以 1 为中心画
CH = {1: [0, 2], 0: [], 2: []}


def _g(S, k):
    return S['_inner'].get(k)


def _bits(m):
    return {i for i in range(N) if m >> i & 1}


def _draw(cv, S, B, box, T):
    inner = S.get('_inner', {})
    state = S.get('state')
    ms = _bits(state) if isinstance(state, int) else set()
    q = inner.get('q') if isinstance(inner.get('q'), list) else []
    node, nxt = inner.get('node'), inner.get('next')
    line = S.get('_line', 0)
    started = isinstance(inner.get('l'), int)

    def nc(u):
        if started and u in q:
            return 'green'
        if u in ms:
            return 'cyan'
        return None
    hot = nxt if (node is not None and nxt is not None and line in (IF_LINE, RM_LINE, APP_LINE)) else None
    draw_gtree(cv, T, box, CH, ROOT, {}, node if (started and line in (IF_LINE, RM_LINE, APP_LINE)) else None, hot, set(), None, (),
               label_fn=lambda u: f'{u}', node_color=nc,
               title='树（城市编号从 0 开始；青 = 在子集里，绿 = BFS 已访问，灰 = 不在子集里）')
CODE = '''
class Solution(object):
    def countSubgraphsForEachDiameter(self, n, edges):

        res = [0] * (n - 1)
        g = {index : set() for index in range(n)}
        print(g)
        for x, y in edges:
            x -= 1
            y -= 1
            g[x].add(y)
            g[y].add(x)

        for state in range(1, 1 << n):
            node_set = set()
            for index in range(n):
                if state & (1 << index):
                    node_set.add(index)
                    s = index

            if len(node_set) == 1:
                continue
            
            node_set.remove(s)
            q = [s]
            l = 0
            r = 1
            while l < r:
                new_r = r
                for node in q[l : r]:
                    for next in g[node]:
                        if next in node_set:
                            node_set.remove(next)
                            q.append(next)
                            new_r += 1
                
                l, r = r, new_r
            
            if len(node_set) > 0:
                continue
            
            u = q[-1]
            node_set = set(q)
            node_set.remove(u)
            step = 0
            q = [u]
            l = 0
            r = 1
            while l < r:
                new_r = r
                step += 1
                for node in q[l : r]:
                    for next in g[node]:
                        if next in node_set:
                            node_set.remove(next)
                            q.append(next)
                            new_r += 1
                
                l, r = r, new_r

            res[step - 2] += 1
        
        return res
'''
_CL = CODE.strip('\n').split('\n')


def _ln(sub, k=0):
    return [i + 1 for i, t in enumerate(_CL) if sub in t][k]


IF_LINES = [i + 1 for i, t in enumerate(_CL) if 'if next in node_set' in t]
IF_LINE = IF_LINES[0]
RM_LINE = _ln('node_set.remove(next)')
APP_LINE = _ln('q.append(next)')


def _sub(S):
    st = S.get('state')
    return '{' + ','.join(str(i) for i in range(N) if st >> i & 1) + '}'


def _cap_state(S, B, r):
    st = S.state
    ns = S.node_set
    if len(ns) == 1:
        return f"子集 `{_sub(S)}`：只有 1 个城市，没有距离，跳过"
    return f"子集 `{_sub(S)}`：从 `s = {S.s}` 出发 BFS 判连通"


def _cap_if(S, B, r):
    nx, nd = _g(S, 'next'), _g(S, 'node')
    return (f"`{nd}` 的邻居 `{nx}` 还没访问 → 访问" if nx in S.node_set
            else f"`{nd}` 的邻居 `{nx}` 已访问或不在子集 → 跳过")


def _cap_conn(S, B, r):
    if len(S.node_set) > 0:
        return f"还剩 `{sorted(S.node_set)}` 没访问到 → ==不连通==，不是树，跳过"
    return f"`{len(S.q)}` 个城市全访问到 → 连通，是一棵树"


CONFIG = dict(
    num=1617, title='统计子树中城市之间最大距离', difficulty='Hard',
    category='链表、二叉树与回溯',
    author='yiduobo', technique='枚举子集 + 双 BFS 求直径',
    tags=['动态规划', '数学算法', '难度分 2309'],
    code=CODE,
    call='Solution().countSubgraphsForEachDiameter(3, [[1,2],[2,3]])',
    expect=[2, 1],
    views=[
        dict(type='custom', draw=_draw, h=230),
        dict(type='array', var=lambda S: _g(S, 'q') if isinstance(_g(S, 'q'), list) else [], label='BFS 队列 q', cell=70, h=150),
        dict(type='array', var=lambda S: S.get('res') if isinstance(S.get('res'), list) else [], label='res[d-1]：直径恰好为 d 的子树数', cell=84, h=130),
    ],
    watch=[('state', 'state', 'blue'), ('node_set', lambda S: sorted(S['_inner'].get('node_set')) if isinstance(S['_inner'].get('node_set'), set) else None, 'yellow'),
           ('l', lambda S: _g(S, 'l'), 'blue'), ('r', lambda S: _g(S, 'r'), 'pink'), ('u', lambda S: S.get('u'), 'orange'), ('step', lambda S: S.get('step'), 'green')],
    captions={
        'res = [0] * (n - 1)': '`res[d-1]` 记录距离恰为 `d` 的子树数；先建图 `g`',
        'if len(node_set) == 1': _cap_state,
        'while l < r': lambda S, B, r_: (f"这一轮有 `{S.r - S.l}` 个点要扩展" if S.l < S.r else '这一轮没有新点了，BFS 结束'),
        'for node in q[l : r]': lambda S, B, r_: f"扩展 `{_g(S, 'node')}`，看它的邻居",
        'if next in node_set': _cap_if,
        'l, r = r, new_r': lambda S, B, r_: (f"本轮完，下一轮 `q[{S.l}:{S.r}]`" if S.l < S.r else '没有新点了，BFS 结束'),
        'node_set.remove(next)': '`{next}` 标记已访问',
        'q.append(next)': '`{next}` 入队：`q = {q}`',
        'if len(node_set) > 0': _cap_conn,
        'u = q[-1]': '队尾 `u = {u}` 最远，==是直径端点==；再从 `u` BFS 数轮数',
        'res[step - 2] += 1': '直径 = `step - 1 = {step - 1}` → `res = {res}`',
        'return res': '子集都处理完：`res = {ret}`',
    },
    skip=['print(g)', 'for x, y in edges', 'x -= 1', 'y -= 1', 'g[x].add(y)', 'g[y].add(x)', 'g = {index', 'node_set = set()', 'for index in range(n)',
          'if state & (1 << index)', 'node_set.add(index)', 's = index', 'for state in range', 'continue', 'l = 0', 'r = 1', 'new_r = r', 'new_r += 1',
          'for next in g[node]', 'while l < r', 'for node in q[l : r]', 'step += 1', 'node_set.remove(u)', 'step = 0', 'node_set = set(q)', 'node_set.remove(s)', 'q = [s]', 'q = [u]'],
    max_steps=130,
    cards=dict(
        one_liner='暴力枚举每个子集：先 BFS 判连通，再双 BFS 求直径',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`',
        problem=['`n` 个城市组成一棵树，对每个 `d = 1..n-1`',
                 '数出「最大距离恰好为 `d` 的连通子集」有多少个',
                 '本视频：`n = 3`，`edges = [[1,2],[2,3]]` → `[2, 1]`'],
        quote='由于数据规模非常小，指数级算法是很容想到的。直接枚举树中有哪些节点，然后求这些点构成的子树的直径。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`state` 的每一位表示城市选不选，共 `2^n - 1` 个非空子集',
              '先从任一点 BFS：没访问完整个子集，说明不连通，丢掉',
              '再用经典「双 BFS」：最远点 `u` 是直径端点，从 `u` BFS 的轮数 − 1 = 直径'],
        result='运行结束，返回 `[2, 1]`：直径 1 的有 `{0,1}`、`{1,2}`，直径 2 的有 `{0,1,2}`',
        summary=['时间 `O(n·2^n)`，空间 `O(n)`；原文也提到没想出多项式解法',
                 '易错：BFS 返回的轮数 = 距离 + 1，所以 `res[step - 2]`（距离 `step - 1`，再 −1 做下标）',
                 '易错：不连通的子集要先排除；单点子集直径为 0，直接跳过',
                 '对比灵神：灵神用 DFS 树形 DP，一遍求连通性和直径；yiduobo 用两趟 BFS',
                 '原文为 Python 2 写法，`print g` 已改为 `print(g)`（调试输出，视频中跳过）'],
    ),
)
