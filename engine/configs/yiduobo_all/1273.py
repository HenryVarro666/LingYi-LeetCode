def _layout_tree(n, edges, root=0):
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)
    pos, nxt = {}, [0]

    def go(x, fa, d):
        ch = [y for y in g[x] if y != fa]
        if not ch:
            pos[x] = (nxt[0], d)
            nxt[0] += 1
        else:
            for y in ch:
                go(y, x, d + 1)
            pos[x] = (sum(pos[y][0] for y in ch) / len(ch), d)
    go(root, -1, 0)
    return pos, nxt[0], max(d for _, d in pos.values()) + 1


def _draw_tree(cv, box, T, n, edges, fill, sub, ring=None, title='', subcolor='muted', inner=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    pos, w, h = _layout_tree(n, edges)
    sp = min(170, (x1 - x0 - 60) / max(1, w))
    R = max(18, min(28, sp * 0.36))
    dy = min(120, (y1 - y0 - 70 - 2 * R - 40) / max(1, h - 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * w) / 2 + sp / 2
    P = {k: (sx + a * sp, y0 + 60 + R + d * dy) for k, (a, d) in pos.items()}
    for a, b in edges:
        (ax, ay), (bx, by) = P[a], P[b]
        if pos[a][1] > pos[b][1]:
            (ax, ay), (bx, by) = (bx, by), (ax, ay)
        cv.line([(ax, ay), (bx, by)], T['dim'], 3)
    for k, (cx, cy) in P.items():
        c = fill.get(k)
        cv.rect((cx - R, cy - R, cx + R, cy + R), fill=T[c] if c else T['panel2'], outline=T['yellow'] if k == ring else T['border'],
                width=5 if k == ring else 3, r=R)
        cv.text((cx, cy), k, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        s = sub.get(k)
        if s not in (None, ''):
            tw = cv.tlen(s, 21, bold=True) + 10
            cv.rect((cx - tw / 2, cy + R + 4, cx + tw / 2, cy + R + 32), fill=T['panel'], r=6)
            cv.text((cx, cy + R + 8), s, 21, T[subcolor], anchor='mt', bold=True)


SNAP = {}
DONE = {}


def trk(fn=None, rec=None, reset=False):
    """caption wrapper: remember which nodes have returned (node -> returned value), keyed by this step's innermost-locals object"""
    def cap(S, B, ret):
        if reset:
            DONE.clear()
        if rec is not None:
            kv = rec(S, B, ret)
            if kv is not None:
                DONE[kv[0]] = kv[1]
        SNAP[id(S['_inner'])] = dict(DONE)
        return fn(S, B, ret) if callable(fn) else None
    return cap


def _done(S):
    return SNAP.get(id(S['_inner']), {})


def fill_caps(code, caps):
    """give every other statement line a tracking (default-text) caption"""
    out = dict(caps)
    for l in code.strip('\n').split('\n'):
        s = l.strip()
        if not s or s.startswith(('def ', 'class ', '#')) or any(k in l for k in out):
            continue
        out[s] = trk()
    return out
PARENT = [-1, 0, 0, 1, 2, 2, 2]
VALUE = [1, -2, 4, 0, -2, -1, -1]
EDGES = [[p, i] for i, p in enumerate(PARENT) if p >= 0]


def _draw(cv, S, B, box, T):
    value, f = S.get('value'), S.get('f')
    if value is None or f is None:
        return
    seen, inner = _done(S), S['_inner']
    q = S.get('q')
    cur = inner.get('now')
    fill, sub = {}, {}
    for i in range(len(value)):
        sub[i] = f'{value[i]}' + (f' → {f[i]}' if i in seen else '')
        if q is not None:
            if i in q:
                fill[i] = 'green'
            elif f[i] == 0:
                fill[i] = 'red'
    if q is None and cur is not None:
        fill[cur] = 'blue'
    _draw_tree(cv, box, T, len(value), EDGES, fill, sub, ring=cur,
               title='树（节点值 → 子树和 f；层序阶段：绿 = 保留进队列，红 = 子树和为 0 被删）')


def _info(S):
    q = S.get('q')
    if q is None:
        return '第 2 步：自底向上算每个节点的子树和 `f`'
    return f'第 3 步：层序遍历只走 `f != 0` 的节点，队列 `q` = ==[{", ".join(map(str, q))}]==（{len(q)} 个）'


CODE = '''
class Solution(object):
    def deleteTreeNodes(self, nodes, parent, value):

        childs = {index : set() for index in range(nodes)}
        for index, fa in enumerate(parent):
            if fa == -1:
                root = index
            else:
                childs[fa].add(index)
        
        f = [0] * nodes

        def dfs(now):
            f[now] = value[now]
            for c in childs[now]:
                dfs(c)
                f[now] += f[c]

        dfs(root)
        
        if f[root] == 0:
            return 0
        
        q = [root]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for c in childs[now]:
                if f[c] != 0:
                    q.append(c)
                    tail += 1
        
        return len(q)
'''
CAPS = {
    'childs = {index': trk(lambda S, B, r: '为每个节点准备一个孩子集合 `childs`', reset=True),
    'root = index': trk(lambda S, B, r: f'`parent[{S.index}] == -1` → 节点 `{S.index}` 是根'),
    'f = [0] * nodes': trk(lambda S, B, r: '`f[i]`：以 `i` 为根的子树里所有节点值之和（建树已完成：`parent` 的每一项都登记成了孩子）'),
    'f[now] = value[now]': trk(lambda S, B, r: f'进入节点 `{S.now}`：子树和先是自己的值 `f[{S.now}] = {S.f[S.now]}`', rec=lambda S, B, r: (S.now, True)),
    'for c in childs[now]': trk(lambda S, B, r: (f'`{S.now}` 的下一个孩子 `{S.c}`' if S['_inner'].get('c') != B['_inner'].get('c') or 'c' not in B['_inner']
                                                  else f'`{S.now}` 的孩子都处理完了，`f[{S.now}] = {S.f[S.now]}` 就是它的子树和')
                                if 'now' in S['_inner'] and not S.get('q') else None),
    'dfs(c)': trk(lambda S, B, r: f'先递归孩子 `{B.c}`，等它的子树和 `f[{B.c}]` 算好'),
    'f[now] += f[c]': trk(lambda S, B, r: f'孩子 `{B.c}` 的子树和 `{S.f[B.c]}` 累加进来：`f[{S.now}] = {B.f[S.now]} + {S.f[B.c]} = {S.f[S.now]}`'),
    'dfs(root)': trk(lambda S, B, r: '从根开始，算出每个节点的子树和'),
    'if f[root] == 0': trk(lambda S, B, r: f'`f[root] = {S.f[S.root]}` ' + ('== 0 → 整棵树都被删，返回 `0`' if S.f[S.root] == 0 else '≠ 0 → 整棵树不会被删，继续层序遍历')),
    'q = [root]': trk(lambda S, B, r: '第 3 步：从根开始层序遍历，==子树和为 0 的孩子整棵不要==；队列最终长度就是答案'),
    'while head < tail': trk(lambda S, B, r: f'`head = {S.head}`，`tail = {S.tail}`：' + ('队列里还有没处理的节点' if S.head < S.tail else '队列处理完了')),
    'now = q[head]': trk(lambda S, B, r: f'取出队首节点 `{S.now}`，`head` 后移'),
    'for c in childs[now]': None,
    'if f[c] != 0': trk(lambda S, B, r: f'孩子 `{S.c}`：`f[{S.c}] = {S.f[S.c]}` ' + ('≠ 0 → 这棵子树保留，入队' if S.f[S.c] != 0 else '== 0 → ==整棵子树被删==，不入队，也不用再往下看')),
    'q.append(c)': trk(lambda S, B, r: f'`q` 末尾加入 `{S.c}`，当前队列 {S.q}（`tail` 同时 +1）'),
    'return len(q)': trk(lambda S, B, r: f'队列里剩下 `{r}` 个节点就是保留下来的节点数'),
}
CAPS['for c in childs[now]'] = trk(lambda S, B, r: (f'`{S.now}` 的下一个孩子 `{S.c}`' if S['_inner'].get('c') != B['_inner'].get('c') else
                                                    f'`{S.now}` 的孩子都处理完了' + ('' if S.get('q') else f'，`f[{S.now}] = {S.f[S.now]}` 就是它的子树和')))
CONFIG = dict(
    num=1273, title='删除树节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='递归求子树和 + 层序数保留节点', tags=['灵神题单·链表树与回溯'],
    code=CODE,
    call=f'Solution().deleteTreeNodes(7, {PARENT}, {VALUE})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=390),
        dict(type='text', fn=_info, h=50),
        dict(type='calls', h=150),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('f', 'f', 'green'), ('q', 'q', 'orange')],
    captions=fill_caps(CODE, CAPS),
    skip=['for index, fa in enumerate', 'if fa == -1', 'childs[fa].add', 'head, tail = 0, 1', 'head += 1', 'tail += 1'],
    max_steps=120,
    cards=dict(
        one_liner='先算每棵子树的和，再从根往下数还没被删的节点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一棵树有 `nodes` 个节点，`parent[i]` 是 `i` 的父节点（根是 `-1`），`value[i]` 是节点值',
                 '把 ==子树节点值之和为 0== 的子树整棵删掉，返回剩下的节点数',
                 '示例：`nodes=7, parent=[-1,0,0,1,2,2,2], value=[1,-2,4,0,-2,-1,-1]` → `2`'],
        quote='本题就应该从根节点向下进行层序遍历，将上层的节点值之和为0的子树删除，对于删除的子树则无需继续往下进行遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['先遍历 `parent` 建树，找到根',
              '递归算出每个节点的子树和 `f[now]`',
              '从根层序遍历，只让 `f != 0` 的孩子入队；==最终队列长度就是答案=='],
        result='队列里只有 `[0, 1]`：节点 2、3 的子树和为 0，连同其子孙被删，剩 2 个节点',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：整棵树的和为 0（`f[root] == 0`）要单独返回 `0`，否则会把根算进答案',
                 '子树和为 0 就整棵删，哪怕子孙里有和不为 0 的节点（如 `[1,-1]`），所以 BFS 遇到 `f == 0` 直接不入队',
                 '原文 Python 代码在 Python 3 下可直接运行，没有修改'],
    ),
)
