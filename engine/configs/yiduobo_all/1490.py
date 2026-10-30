SETUP = '''
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []
    def __repr__(self):
        return f'Node({self.val})'

root = Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4)])
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
    mid = (y0 + y1) / 2
    root, mp = S['root'], S.get('mapping') or {}
    q, now = S.get('q') or [], S.get('now')
    seen = {id(x) for x in mp}
    _tree(cv, (x0, y0, x1, mid - 6), root, T,
          lambda n: 'yellow' if n is now else ('green' if id(n) in seen else None),
          '原树（绿 = 已经克隆，黄 = now）', R=24)
    cv.line([(x0 + 20, mid), (x1 - 20, mid)], T['border'], 2)
    cl = mp.get(root)
    if cl is not None:
        _tree(cv, (x0, mid + 6, x1, y1), cl, T, lambda n: 'cyan', '克隆出来的新树（mapping[root] 起）', R=24)


def _qv(S):
    return [x.val for x in S['q']] if 'q' in S else []


def _mp(S):
    return {k.val: v.val for k, v in (S.get('mapping') or {}).items()}


CONFIG = dict(
    num=1490, title='克隆N叉树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='BFS · 哈希表建立新旧节点映射',
    tags=['链表树与回溯', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def cloneTree(self, root):

        if not root:
            return None

        mapping = {}
        q = [root]
        mapping[root] = Node(root.val)

        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for child in now.children:
                mapping[child] = Node(child.val)
                mapping[now].children.append(mapping[child])
                q.append(child)
                tail += 1

        return mapping[root]
''',
    setup=SETUP,
    call='Solution().cloneTree(root)',
    expect='1(3(5 6) 2 4)',
    result_fn=_ser,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var=_qv, label='q（数组当队列，head 之前是已处理的）', cell=70, h=150,
             pointers={'head': 'blue', 'tail': 'pink'}),
        dict(type='map', var=_mp, label='mapping：旧节点值 → 新节点值', h=130, fmt=lambda k, v: f'{k} → {v}'),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('now', lambda S: getattr(S.get('now'), 'val', None), 'yellow')],
    skip=['head, tail = 0, 1'],
    captions={
        'if not root': '空树 → 返回 `None`；本例树非空',
        'mapping = {}': '`mapping`：旧节点 → 它的克隆，用来==找到父亲的克隆==',
        'q = [root]': '`q` 当队列做 BFS，从根开始',
        'mapping[root] = Node(root.val)': '先克隆根节点（只复制值，孩子列表是空的）',
        'while head < tail': lambda S, B, r: (f'`head = {S.head} < tail = {S.tail}`：队列里还有没处理的节点' if S.head < S.tail else f'`head = tail = {S.tail}`：队列处理完 → 结束'),
        'now = q[head]': '取出队首 `now = {now.val}`',
        'head += 1': '`head` 后移，相当于出队',
        'for child in now.children': lambda S, B, r: (f'`{S.now.val}` 没有孩子' if not S.now.children else ('孩子都克隆完了' if getattr(B._inner.get('child'), 'val', None) is not None and B._inner['child'].val == S._inner['child'].val else f'取孩子 `{S.child.val}`')),
        'mapping[child] = Node(child.val)': '为孩子 `{child.val}` 新建克隆，记进 `mapping`',
        'mapping[now].children.append': '用映射找到 `{now.val}` 的克隆，把 `{child.val}` 的克隆挂上去——父子关系就复制好了',
        'q.append(child)': '孩子入队，以后再去克隆它的孩子',
        'tail += 1': '队尾 `tail = {tail}`',
        'return mapping[root]': '返回根节点的克隆：整棵新树',
    },
    cards=dict(
        one_liner='用哈希表记住「旧节点 → 新节点」，BFS 时顺手把父子关系搭起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一棵 N 叉树，返回它的==深拷贝==（节点全是新建的）',
                 '`Node` 有 `val` 和 `children` 两个属性',
                 '本视频：`1(3(5 6) 2 4)`，克隆出结构完全相同的新树'],
        quote='与之前的1485题类似，同样是通过哈希表辅助建立父子关系。我在这里依然是采用bfs来进行处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['队列里装旧树节点；每取出一个 `now`，它的克隆已经在 `mapping` 里',
              '对每个孩子：新建克隆 → 挂到 `mapping[now].children` → 孩子入队',
              '用数组 + `head/tail` 当队列，不真正出队'],
        summary=['时间 `O(n)`，空间 `O(n)`（映射 + 队列）',
                 '易错：必须先把根放进 `mapping`，否则第一次 `mapping[now]` 会 KeyError',
                 '易错：只复制 `val`，孩子要靠挂接得到，不能直接引用旧孩子',
                 '换成 DFS 递归同样可行；这里用 BFS 避免递归',
                 '原文为 Python 2 风格，这里只删去了 Node 定义说明；Node 放在 setup 中'],
    ),
)
