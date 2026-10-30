SETUP = '''
root = Tr([1, 2, 3, 4, 5, None, 7])
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


def _nm(x):
    if x is None:
        return 'None'
    if not hasattr(x, 'left'):
        return 'dummy'
    return x.val


def _level(S, x):
    if x is None or not hasattr(x, 'left') or S.get('root') is None:
        return None
    return _nodes(S['root'])[1].get(x._uid)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '二叉树 + next 指针（绿弧 = 已连好的 next，黄 = 这一步新连的）', 22, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    order, depth = _nodes(root)
    xi = {n._uid: i for i, n in enumerate(order)}
    D = max(depth.values()) + 1
    pad = 170
    sp = min(140, (x1 - x0 - pad - 40) / len(order))
    dy = min(150, (y1 - y0 - 110) / D)
    R = 30
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
    dummy = S.get('dummy')
    if dummy is not None:
        dn = getattr(dummy, 'next', None)
        lv = depth.get(dn._uid) if dn is not None and dn._uid in xi else ((cl + 1) if cl is not None else None)
        if lv is not None and lv < D + 1:
            DX, DY = x0 + 80, y0 + 90 + lv * dy
            isn = S.get('nxt') is dummy or (S.get('nxt') is not None and not hasattr(S.get('nxt'), 'left'))
            cv.rect((DX - 52, DY - 24, DX + 52, DY + 24), fill=T['pink'] if isn else (52, 46, 70), r=10,
                    outline=T['border'], width=2)
            cv.text((DX, DY), 'dummy', 20, T['bg'] if isn else T['text'], anchor='mm', bold=True)
            if isn:
                cv.text((DX, DY + 28), 'nxt', 19, T['pink'], anchor='mt', bold=True)
            if dn is not None and dn._uid in xi:
                X2, Y2 = P(dn)
                ch = B.get('dummy') is None or getattr(B['dummy'], 'next', None) is None
                c = T['yellow'] if ch else T['cyan']
                cv.arrow((DX + 54, DY), (X2 - R - 4, Y2), c, 4 if ch else 3, 12)
    hit = {}
    for name, c in (('cur', 'blue'), ('nxt', 'pink')):
        v = S.get(name)
        if v is not None and hasattr(v, 'left') and v._uid in xi:
            hit.setdefault(v._uid, []).append((name, T[c]))
    for n in order:
        X, Y = P(n)
        hs = hit.get(n._uid, [])
        fill = hs[0][1] if hs else T['panel2']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), n.val, 26, T['bg'] if hs else T['text'], anchor='mm', bold=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X + R + 4, Y + 8 + r * 22), name, 20, cc, anchor='lt', bold=True)


def _w4(S, B, ret):
    if S.cur is None:
        return '下一层链表为空 → 所有层都连好了，结束'
    lv = _level(S, S.cur)
    if lv == 0:
        return '第 0 层只有 `root`：它本身就是一条（长度为 1 的）链表'
    return f'第 {lv} 层已经连成链表，表头 `{S.cur.val}` → 用它来连第 {lv + 1} 层'


def _w6(S, B, ret):
    if S.cur is None:
        return '当前层的链表走完了'
    return f'遍历当前层的链表：`cur = {S.cur.val}`，看它的儿子'


def _ifc(side):
    def f(S, B, ret):
        ch = getattr(S.cur, side)
        word = '左' if side == 'left' else '右'
        if ch is None:
            return f'`{S.cur.val}` 没有{word}儿子 → 跳过'
        return f'`{S.cur.val}` 有{word}儿子 `{ch.val}` → 接到下一层链表的末尾'
    return f


def _link(side):
    def f(S, B, ret):
        ch = getattr(S.cur, side)
        if not hasattr(B.nxt, 'left'):
            return f'`dummy.next = {ch.val}`：`{ch.val}` 成为下一层的==第一个节点==（哨兵省去了判空）'
        return f'下一层的相邻节点连起来：`{B.nxt.val}.next = {ch.val}`'
    return f


CONFIG = dict(
    num=117, title='填充每个节点的下一个右侧节点指针 II', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='BFS + 链表 · 哨兵节点 · O(1) 空间',
    tags=['面试经典150'],
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
    expect=[1, '#', 2, 3, '#', 4, 5, 7, '#'],
    views=[
        dict(type='text', size=26, fn=lambda S: '一边沿 next 遍历==当前层==，一边把==下一层==连成链表'),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('cur', lambda S: _nm(S['cur']), 'blue'), ('nxt', lambda S: _nm(S['nxt']), 'pink'),
           ('dummy.next', lambda S: _nm(S['dummy'].next), 'cyan')],
    captions={
        'cur = root': '`cur = root`：从第一层开始',
        4: _w4,
        'nxt = dummy = Node()': '新建==哨兵== `dummy`（下一层“第一个节点之前的节点”），`nxt` 指向下一层链表的末尾',
        6: _w6,
        7: _ifc('left'),
        'nxt.next = cur.left': _link('left'),
        'nxt = cur.left': '`nxt` 移到下一层链表的新末尾 `{nxt.val}`',
        10: _ifc('right'),
        'nxt.next = cur.right': _link('right'),
        'nxt = cur.right': '`nxt` 移到下一层链表的新末尾 `{nxt.val}`',
        'cur = cur.next': lambda S, B, r: (f'沿上一轮连好的 `{B.cur.val}.next` 走到 `{S.cur.val}`' if S.cur
                                           else f'`{B.cur.val}.next` 为空：当前层到头了'),
        'cur = dummy.next': lambda S, B, r: (f'`dummy.next = {S.cur.val}` 就是下一层链表的头节点 → 进入下一层' if S.cur
                                             else '`dummy.next` 为空：下一层没有节点了'),
        'return root': '每一层都用 next 连成了链表，返回 `root`',
    },
    cards=dict(
        one_liner='当前层已是链表：沿着它走，顺手把下一层也连成链表',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给每个节点的 `next` 指针指向==同一层右侧==的下一个节点，没有则为 `NULL`',
                 '和 116 题不同：这棵树==不一定是完美二叉树==',
                 '示例：`[1,2,3,4,5,null,7]` → `[1,#,2,3,#,4,5,7,#]`'],
        quote='既然每一层都连接成一个链表了，那么知道链表头，就能访问这一层的所有节点。所以在 BFS 的时候，==可以一边遍历当前层的节点，一边把下一层的节点连接起来==。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['不用队列：当前层靠 `next` 遍历，下一层只需记住链表头',
              '用==哨兵节点== `dummy` 表示“第一个节点之前的节点”，接儿子时不用判断是不是第一个',
              '`dummy.next` 就是下一层的头，进入下一轮循环'],
        summary=['时间 `O(n)`，空间 `O(1)`：满足进阶要求',
                 '易错：每层都要==新建==哨兵，`cur = dummy.next` 才是下一层的头',
                 '题解的另两种写法：DFS + `pre[depth]` 数组；普通 BFS 每层 `pairwise` 连接',
                 '同类：116. 填充每个节点的下一个右侧节点指针、102. 二叉树的层序遍历'],
    ),
)
