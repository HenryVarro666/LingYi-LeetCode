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


PTRS = (('cur', 'blue'), ('nxt', 'pink'))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '完美二叉树 + next 指针（绿弧 = 已连好，黄 = 这一步新连的）', 22, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    order, depth = _nodes(root)
    xi = {n._uid: i for i, n in enumerate(order)}
    D = max(depth.values()) + 1
    pad = 150
    sp = min(130, (x1 - x0 - pad - 40) / len(order))
    dy = min(150, (y1 - y0 - 110) / D)
    R = 28
    sx = x0 + pad + ((x1 - x0 - pad - 40) - sp * len(order)) / 2 + sp / 2

    def P(n):
        return sx + xi[n._uid] * sp, y0 + 90 + depth[n._uid] * dy

    cl = _level(S, S.get('cur'))
    for lv, (txt, c) in ((cl, ('当前层', 'blue')), ((cl + 1) if cl is not None else None, ('下一层', 'pink'))):
        if lv is not None and lv < D:
            Y = y0 + 90 + lv * dy
            cv.rect((x0 + 14, Y - R - 10, x1 - 14, Y + R + 10), fill=T[c], alpha=22, r=12)
            cv.text((x1 - 22, Y - R - 6), txt, 18, T[c], anchor='ra', bold=True)
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
    # 哨兵 dummy：画在下一层最左边
    dm = S.get('dummy')
    dl = _level(S, dm.next) if dm is not None and dm.next is not None else ((cl + 1) if cl is not None else None)
    if dm is not None and dl is not None and dl < D:
        Y = y0 + 90 + dl * dy
        bx = x0 + 30
        hit = S.get('nxt') is not None and getattr(S['nxt'], '_uid', None) == dm._uid
        cv.rect((bx, Y - 22, bx + 84, Y + 22), fill=T['pink'] if hit else T['panel2'], outline=T['border'], width=2, r=8)
        cv.text((bx + 42, Y), 'dummy', 19, T['bg'] if hit else T['muted'], anchor='mm', bold=True)
        if hit:
            cv.text((bx + 42, Y + 26), 'nxt', 19, T['pink'], anchor='mt', bold=True)
        if dm.next is not None and dm.next._uid in xi:
            X2, Y2 = P(dm.next)
            cv.arrow((bx + 86, Y), (X2 - R - 4, Y2), T['cyan'], 3, 12)
    hit = {}
    for name, c in PTRS:
        v = S.get(name)
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


def _nv(x):
    return 'dummy' if x is not None and not hasattr(x, 'left') else _v(x)


def _ifc(side):
    word = '左' if side == 'left' else '右'

    def f(S, B, ret):
        ch = getattr(S.cur, side)
        if ch is None:
            return f'`{S.cur.val}` 没有{word}儿子 → 跳过'
        return f'`{S.cur.val}` 有{word}儿子 `{ch.val}` → 把它接到下一层链表末尾'
    return f


def _link(side):
    def f(S, B, ret):
        ch = getattr(S.cur, side)
        return f'`{_nv(B.nxt)}.next = {ch.val}`：==下一层的相邻节点连起来=='
    return f


def _w(S, B, ret):
    if S.cur is None:
        return '`cur` 为空：没有下一层了 → 结束'
    lv = _level(S, S.cur)
    return f'第 {lv} 层的 next 已经连好，它就是一条链表 → 遍历它，同时连好第 {lv + 1} 层'


CONFIG = dict(
    num=116, title='填充每个节点的下一个右侧节点指针', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='BFS + 链表 · 哨兵节点',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def connect(self, root: 'Node') -> 'Node':
        cur = root
        while cur:
            nxt = dummy = Node()  # 下一层的链表
            while cur:  # 遍历当前层的链表
                if cur.left:
                    nxt.next = cur.left  # 下一层的相邻节点连起来
                    nxt = cur.left
                if cur.right:
                    nxt.next = cur.right  # 下一层的相邻节点连起来
                    nxt = cur.right
                cur = cur.next  # 当前层链表的下一个节点
            cur = dummy.next  # 下一层链表的头节点
        return root
''',
    setup=SETUP,
    call='Solution().connect(root)',
    result_fn=_ser,
    expect=[1, '#', 2, 3, '#', 4, 5, 6, 7, '#'],
    views=[
        dict(type='text', size=26, fn=lambda S: '遍历==当前层==的链表，同时把==下一层==连成链表'),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('cur', lambda S: _v(S['cur']), 'blue'), ('nxt', lambda S: _nv(S['nxt']), 'pink'),
           ('dummy.next', lambda S: _v(S['dummy'].next) if S.get('dummy') is not None else None, 'cyan')],
    captions={
        'cur = root': '`cur = root`：第 0 层只有根节点，它自己就是一条链表',
        4: _w,
        'nxt = dummy = Node()': '新建哨兵 `dummy` 作为下一层链表的头前节点，`nxt` 指向链表末尾',
        6: lambda S, B, r: (f'处理当前层的节点 `cur = {S.cur.val}`' if S.cur else '当前层遍历完了'),
        7: _ifc('left'),
        'nxt.next = cur.left': _link('left'),
        'nxt = cur.left': '`nxt` 移到链表新末尾 `{nxt.val}`',
        10: _ifc('right'),
        'nxt.next = cur.right': _link('right'),
        'nxt = cur.right': '`nxt` 移到链表新末尾 `{nxt.val}`',
        'cur = cur.next': lambda S, B, r: (f'沿着已连好的 `{B.cur.val}.next` 走到 `{S.cur.val}`' if S.cur
                                           else f'`{B.cur.val}.next` 为空：当前层走完了'),
        'cur = dummy.next': lambda S, B, r: (f'`dummy.next = {S.cur.val}` 是下一层的头 → 进入下一层' if S.cur
                                             else '`dummy.next` 为空：下一层没有节点'),
        'return root': '每一层都连成了链表，返回 `root`',
    },
    cards=dict(
        one_liner='把每一层看成链表：遍历这一层，顺手把下一层连起来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定一棵==完美二叉树==，让每个节点的 `next` 指向同一层右侧的下一个节点',
                 '每层最右边的节点 `next` 为 `NULL`；进阶：只用常量额外空间',
                 '示例：`[1,2,3,4,5,6,7]` → `[1,#,2,3,#,4,5,6,7,#]`'],
        quote='既然每一层都连接成一个链表了，那么知道链表头，就能访问这一层的所有节点。所以在 BFS 的时候，可以==一边遍历当前层的节点，一边把下一层的节点连接起来==。',
        quote_src='—— 灵茶山艾府题解 · 方法三',
        idea=['当前层已连成链表，用 `cur = cur.next` 遍历它，不需要队列',
              '下一层用==哨兵 `dummy`== 起头，`nxt` 指向末尾，儿子依次接上去',
              '这一层走完，`dummy.next` 就是下一层的头'],
        summary=['时间 `O(n)`，空间 `O(1)`：只用了几个指针',
                 '哨兵节点省去了「下一层第一个节点」的特判',
                 '这段代码不依赖完美二叉树，原样可解 117 题',
                 '方法一 DFS 用 `pre[depth]` 记每层上一个节点；方法二 BFS 用 `pairwise` 连同层节点'],
    ),
)
