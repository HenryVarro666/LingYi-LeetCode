SETUP = '''
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []
    def __repr__(self):
        return f'Node({self.val})'

n4, n5 = Node(4), Node(5)
n2 = Node(2, [n4, n5])
n3 = Node(3)
root = Node(1, [n2, n3])
p, q = n2, n5   # 把 p=2 整棵子树移到它的后代 q=5 下面
'''

def _lay(root):
    pos, dep, nxt = {}, {}, [0]

    def go(nd, d):
        if not nd.children:
            pos[id(nd)] = nxt[0]
            nxt[0] += 1
        else:
            for c in nd.children:
                go(c, d + 1)
            pos[id(nd)] = (pos[id(nd.children[0])] + pos[id(nd.children[-1])]) / 2
        dep[id(nd)] = d
    go(root, 0)
    return pos, dep, max(dep.values()), max(nxt[0] - 1, 1)


def _ser(t):
    if t is None:
        return ''
    s = str(t.val)
    if t.children:
        s += '(' + ' '.join(_ser(c) for c in t.children) + ')'
    return s


def _tree(cv, box, root, T, color_fn, tag=None, R=28):
    """在 box 内画一棵 N 叉树；color_fn(node) -> 颜色名或 None"""
    x0, y0, x1, y1 = box
    pos, dep, md, mw = _lay(root)
    w, h = x1 - x0 - 2 * R - 120, y1 - y0 - 2 * R - 8
    P, nodes = {}, []

    def walk(nd):
        nodes.append(nd)
        fx = 0.5 if mw == 1 and len(pos) == 1 else pos[id(nd)] / mw
        P[id(nd)] = (x0 + 60 + R + fx * w, y0 + R + 4 + dep[id(nd)] / max(md, 1) * h)
        for c in nd.children:
            walk(c)
    walk(root)
    for nd in nodes:
        for c in nd.children:
            cv.line([P[id(nd)], P[id(c)]], T['dim'], 4)
    for nd in nodes:
        cx, cy = P[id(nd)]
        c = color_fn(nd)
        cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=T[c] if c else T['panel2'],
                     outline=T['border'], width=3)
        cv.text((cx, cy), nd.val, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
    if tag:
        cv.text((x0 + 8, y0 + 4), tag, 20, T['muted'], bold=True)
    return P


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pr = S.get('p_root')
    top = pr.children[0] if pr is not None and pr.children else S['root']
    p, q, now = S['p'], S['q'], S.get('now')
    vis = S.get('vis') or set()
    ids = {id(n) for n in vis}
    _tree(cv, (x0, y0 + 34, x1, y1 - 6), top, T,
          lambda n: 'orange' if n is p else ('pink' if n is q else ('yellow' if n is now else ('purple' if id(n) in ids else None))),
          '树（橙 = p，粉 = q，紫 = p 往上的路径 vis，黄 = now）')


def _fa(S):
    return {(k.val if k.val is not None else '假根'): (v.val if v.val is not None else '假根')
            for k, v in (S.get('fa') or {}).items()}


def _vis(S):
    return {n.val for n in (S.get('vis') or [])}


CONFIG = dict(
    num=1516, title='移动N叉树的子树', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='父亲表 + 最近公共祖先 · 分情况改孩子列表',
    tags=['链表树与回溯', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def moveSubTree(self, root, p, q):

        p_root = Node()
        p_root.children.append(root)

        fa = {}
        fa[root] = p_root

        queue = [root]
        head, tail = 0, 1
        while head < tail:
            now = queue[head]
            head += 1
            for child in now.children:
                fa[child] = now
                queue.append(child)
                tail += 1
        
        if fa[p] == q:
            return p_root.children[0]
        
        now = p
        vis = set()
        while now != p_root:
            vis.add(now)
            now = fa[now]
        
        now = q
        while now:
            if now in vis:
                break
            now = fa[now]

        if now == p:
            fa[q].children.remove(q)
            pos = fa[p].children.index(p)
            fa[p].children[pos] = q
        else:
            fa[p].children.remove(p)
        
        q.children.append(p)
        return p_root.children[0]
''',
    setup=SETUP,
    call='Solution().moveSubTree(root, p, q)',
    expect='1(5(2(4)) 3)',
    result_fn=_ser,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var=_fa, label='fa：节点 → 父亲', h=140, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='set', var=_vis, label='vis（p 到根路径上的节点）', h=90, fmt=lambda x: str(x)),
    ],
    watch=[('now', lambda S: getattr(S.get('now'), 'val', None), 'yellow'),
           ('p', lambda S: S['p'].val, 'orange'), ('q', lambda S: S['q'].val, 'pink')],
    skip=['head, tail = 0, 1', 'fa = {}', 'vis = set()'],
    captions={
        'p_root = Node()': '加一个==假根==：根也能有「父亲」，p、q 就总有父亲',
        'p_root.children.append(root)': '真正的根挂在假根下面',
        'fa[root] = p_root': '`fa` 记录每个节点的父亲，根的父亲是假根',
        'queue = [root]': 'BFS 求所有节点的父亲，从根开始',
        'while head < tail': lambda S, B, r: (f'`head = {S.head} < tail = {S.tail}`：还有节点没展开' if S.head < S.tail else 'BFS 结束：所有节点的父亲都记下了'),
        'now = queue[head]': '取出 `now = {now.val}`',
        'head += 1': '`head` 后移（出队）',
        'for child in now.children': lambda S, B, r: (f'`{S.now.val}` 没有孩子' if not S.now.children else ('孩子都记完了' if getattr(B._inner.get('child'), 'val', None) == S.child.val and getattr(B._inner.get('now'), 'val', None) == S.now.val else f'取孩子 `{S.child.val}`')),
        'fa[child] = now': '`{child.val}` 的父亲是 `{now.val}`',
        'queue.append(child)': '孩子入队',
        'tail += 1': '`tail = {tail}`',
        'if fa[p] == q': lambda S, B, r: ('`q` 已经是 `p` 的父亲 → 什么都不用改' if S.fa[S.p] is S.q else f'`p` 的父亲是 `{S.fa[S.p].val}`，不是 `q`（{S.q.val}）→ 需要真正移动'),
        'return p_root.children[0]': '返回假根的孩子，就是（可能已经换掉的）真正的根',
        'now = p': '从 `p` 开始往上走，记下路径',
        'while now != p_root': lambda S, B, r: ('走到假根了 → 路径收集完' if S.now is S.p_root else f'`now = {S.now.val}` 还不是假根，继续往上'),
        'vis.add(now)': '`{now.val}` 加入 `vis`',
        'now = fa[now]': lambda S, B, r: ('`now` 走到父亲：假根（到顶了）' if S.now.val is None else f'`now` 走到父亲 `{S.now.val}`'),
        'now = q': '再从 `q` 往上走，第一个落在 `vis` 里的就是==最近公共祖先==',
        'while now:': lambda S, B, r: (f'`now = {S.now.val}`，继续' if S.now else '走过头了'),
        'if now in vis': lambda S, B, r: (f'`{S.now.val}` 在 `vis` 里 → 它就是 p 和 q 的最近公共祖先' if S.now in S.vis else f'`{S.now.val}` 不在 `vis` 里，继续往上'),
        'break': '找到最近公共祖先 `{now.val}`',
        'if now == p': lambda S, B, r: ('LCA 就是 `p`：`q` 在 `p` 的子树里（情况一）：`q` 顶替 `p` 的位置，`p` 再挂到 `q` 下面' if S.now is S.p else 'LCA 不是 `p`：`q` 不在 `p` 的子树里，直接把 `p` 摘下来挂到 `q` 下'),
        'fa[q].children.remove(q)': '先把 `q` 从原来的父亲 `{fa[q].val}` 的孩子里摘掉',
        'pos = fa[p].children.index(p)': '`p` 在父亲孩子列表中的下标 `{pos}`',
        'fa[p].children[pos] = q': '`q` 顶替 `p` 的位置（保持顺序）',
        'fa[p].children.remove(p)': '把 `p` 从原父亲的孩子里摘掉',
        'q.children.append(p)': '`p` 追加到 `q` 孩子列表的末尾：`{[c.val for c in q.children]}`',
    },
    cards=dict(
        one_liner='先求每个点的父亲和 p、q 的最近公共祖先，再按三种情况改孩子列表',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `p` 为根的子树移到 `q` 下，作为 `q` 的==最后一个孩子==，返回新树的根',
                 '情况一：`q` 在 `p` 的子树里 → `q` 顶替 `p` 的位置，再把 `p` 接到 `q` 下',
                 '情况二、三：`q` 本来就是 `p` 的父亲（不变）；其余 → 摘下 `p` 接到 `q` 下',
                 '本视频：树 `1(2(4 5) 3)`，`p = 2`，`q = 5`（情况一）'],
        quote='第一种情况要求的是先找出p在其父亲节点的孩子列表中的下标位置，然后将这个位置的节点替换成q，然后再将p加入到q孩子列表的末尾。',
        quote_src='—— yiduobo 题解原文',
        idea=['BFS 求 `fa`；p 往上走到根，路径存进 `vis`',
              'q 往上走，第一个在 `vis` 里的节点就是最近公共祖先',
              'LCA 是 `p` ⇔ `q` 在 `p` 子树里 → 先让 `q` 顶替 `p`，避免成环',
              '根没有父亲：加一个假根 `p_root`，最后返回它的孩子'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`q` 在 `p` 子树里时，要先摘 `q`、用 `q` 替换 `p`，再把 `p` 挂到 `q` 下',
                 '易错：`p`、`q` 都可能是根，所以用假根统一处理',
                 '`fa[p] == q` 时树已经满足要求，直接返回',
                 '原文为 Python 2 风格，这里只删去了 Node 定义说明；Node 放在 setup 中'],
    ),
)
