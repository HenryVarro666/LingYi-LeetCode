SETUP = '''
root = Tr([1, 2, 3, 4, 5, 6, 7])
def _init(n):
    if n:
        n.next = None
        _init(n.left)
        _init(n.right)
_init(root)
'''


def _ser(root):
    """按层检查 next 指针，输出 LeetCode 的序列化格式"""
    out, level = [], [root] if root else []
    while level:
        for i, n in enumerate(level):
            want = level[i + 1] if i + 1 < len(level) else None
            out.append(n.val if getattr(n, 'next', None) is want else 'X')
        out.append('#')
        level = [c for n in level for c in (n.left, n.right) if c]
    return out


def _nodes(root):
    order, depth = [], {}

    def ino(n, d):
        if n is None:
            return
        ino(n.left, d + 1)
        order.append(n)
        depth[n._uid] = d
        ino(n.right, d + 1)
    ino(root, 0)
    return order, depth


def _v(x):
    return None if x is None else x.val


def _level(S, x):
    if x is None or S.get('root') is None:
        return None
    return _nodes(S['root'])[1].get(x._uid)


PTRS = (('now', 'blue'),)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '完美二叉树 + next 指针（绿弧 = 已连好，黄 = 这一步新连的）', 22, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    order, depth = _nodes(root)
    xi = {n._uid: i for i, n in enumerate(order)}
    D = max(depth.values()) + 1
    pad = 60
    sp = min(130, (x1 - x0 - pad - 40) / len(order))
    dy = min(150, (y1 - y0 - 110) / D)
    R = 28
    sx = x0 + pad + ((x1 - x0 - pad - 40) - sp * len(order)) / 2 + sp / 2

    def P(n):
        return sx + xi[n._uid] * sp, y0 + 90 + depth[n._uid] * dy

    cl = _level(S, S['_inner'].get('now'))
    for lv, (txt, c) in ((cl, ('p 层', 'blue')), ((cl + 1) if cl is not None else None, ('孩子层', 'pink'))):
        if lv is not None and lv < D:
            Y = y0 + 90 + lv * dy
            cv.rect((x0 + 14, Y - R - 10, x1 - 14, Y + R + 10), fill=T[c], alpha=22, r=12)
            cv.text((x0 + 22, Y - R - 6), txt, 18, T[c], anchor='la', bold=True)
    for n in order:
        X, Y = P(n)
        for ch in (n.left, n.right):
            if ch is not None:
                X2, Y2 = P(ch)
                cv.line([(X, Y), (X2, Y2)], T['border'], 3)
    bnext = {}
    if B.get('root') is not None:
        for n in _nodes(B['root'])[0]:
            nx = getattr(n, 'next', None)
            bnext[n._uid] = nx._uid if nx is not None else None
    for n in order:
        nx = getattr(n, 'next', None)
        if nx is None or nx._uid not in xi:
            continue
        (X, Y), (X2, Y2) = P(n), P(nx)
        ch = bnext.get(n._uid, -1) != nx._uid
        c = T['yellow'] if ch else T['green']
        cv.arc_arrow((X + R * 0.6, Y - R * 0.8), (X2 - R * 0.6, Y2 - R * 0.8), 30, c, 5 if ch else 3, 13)
    hit = {}
    for name, c in PTRS:
        v = S['_inner'].get(name)
        if v is not None and getattr(v, '_uid', None) in xi:
            hit.setdefault(v._uid, []).append((name, T[c]))
    for n in order:
        X, Y = P(n)
        hs = hit.get(n._uid, [])
        fill = hs[0][1] if hs else T['panel2']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), n.val, 26, T['bg'] if hs else T['text'], anchor='mm', bold=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X + R + 4, Y + 4 + r * 22), name, 19, cc, anchor='lt', bold=True)


def _ifl(S, B, ret):
    n = S.now
    if n.left is None:
        return f'`{n.val}` 没有孩子（叶子层）→ 什么也不用做，返回'
    return f'`{n.val}` 有孩子（完美二叉树必定左右都有）→ 给两个孩子连 next'


def _ifn(S, B, ret):
    n = S.now
    if n.next is None:
        return f'`{n.val}.next` 为空：`{n.val}` 是这一层最右边 → 右孩子 `{n.right.val}` 的 next 保持为空'
    return f'`{n.val}.next = {n.next.val}` 存在（上一层递归已经连好）'


CONFIG = dict(
    num=116, title='填充每个节点的下一个右侧节点指针', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='先序递归 · 父节点连孩子',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def connect(self, root):

        if not root:
            return root
        self.dfs(root)
        return root

    def dfs(self, now):
        if now.left:
            now.left.next = now.right
            if now.next:
                now.right.next = now.next.left
            self.dfs(now.left)
            self.dfs(now.right)
''',
    setup=SETUP,
    call='Solution().connect(root)',
    result_fn=_ser,
    expect=[1, '#', 2, 3, '#', 4, 5, 6, 7, '#'],
    views=[
        dict(type='text', size=26, fn=lambda S: '`p.left.next = p.right`，`p.right.next = p.next.left`'),
        dict(type='custom', draw=_draw, h=410),
        dict(type='calls', h=200),
    ],
    watch=[('now', lambda S: _v(S['_inner'].get('now')), 'blue'),
           ('now.next', lambda S: _v(getattr(S['_inner'].get('now'), 'next', None)), 'green')],
    captions={
        'if not root': '树非空',
        'self.dfs(root)': '从根开始递归：处理到节点 p 时，==p 自己的 next 已经连好了==',
        'if now.left': _ifl,
        'now.left.next = now.right': '同一个父亲：左孩子 `{now.left.val}` 的 next ==一定是右孩子== `{now.right.val}`',
        'if now.next': _ifn,
        'now.right.next = now.next.left': '右孩子 `{now.right.val}` 的 next 是 ==p.next 的左孩子== `{now.next.left.val}`',
        'self.dfs(now.left)': lambda S, B, r: f'`{B.now.val}` 的两个孩子连好了 → 递归左孩子 `{S.now.val}`',
        'self.dfs(now.right)': lambda S, B, r: f'`{B.now.val}` 的左子树处理完 → 递归右孩子 `{S.now.val}`',
        7: '所有 next 都连好了，返回 `root`',
    },
    cards=dict(
        one_liner='站在父亲 p 上连孩子：左连右，右连 p.next 的左',
        complexity='时间 `O(n)`，空间 `O(log n)`（递归栈）',
        problem=['给定一棵==完美二叉树==，让每个节点的 `next` 指向同一层右侧的下一个节点',
                 '每层最右边的节点 `next` 为 `NULL`',
                 '示例：`[1,2,3,4,5,6,7]` → `[1,#,2,3,#,4,5,6,7,#]`'],
        quote='若p有左孩子，那么p的左孩子的next一定是指向p的右孩子的，于是有==p.left.next = p.right==。另外，对于p的右孩子，可以发现其一定是指向了p的next的左孩子的，于是有==p.right.next = p.next.left==。',
        quote_src='—— yiduobo 题解原文',
        idea=['先序递归：先处理 p，再递归左右孩子',
              '处理 p 时它的 next 已由父亲连好，所以能用 `p.next.left`',
              '完美二叉树保证：有左孩子就有右孩子，`p.next` 也一定有孩子'],
        summary=['时间 `O(n)`：每个节点处理一次；递归栈 `O(log n)`',
                 '顺序很重要：必须先连好 p 这一层，再递归下去',
                 '只适用于完美二叉树；117 题孩子可能缺失，要换成逐层维护 next_tail',
                 '对比灵神：灵神用哨兵逐层把下一层连成链表，`O(1)` 空间且也能解 117',
                 '原文为 Python 2 风格，只删去了 Node 定义说明和类型文档字符串'],
    ),
)
