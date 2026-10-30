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


def _v(x):
    return None if x is None else x.val


def _level(S, x):
    if x is None or S.get('root') is None:
        return None
    return _nodes(S['root'])[1].get(x._uid)


PTRS = (('now', 'blue'), ('next_head', 'cyan'), ('next_tail', 'pink'))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '二叉树 + next 指针（绿弧 = 已连好的 next，黄 = 这一步新连的）', 22, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    order, depth = _nodes(root)
    xi = {n._uid: i for i, n in enumerate(order)}
    D = max(depth.values()) + 1
    pad = 60
    sp = min(150, (x1 - x0 - pad - 60) / len(order))
    dy = min(150, (y1 - y0 - 110) / D)
    R = 30
    sx = x0 + pad + ((x1 - x0 - pad - 60) - sp * len(order)) / 2 + sp / 2

    def P(n):
        return sx + xi[n._uid] * sp, y0 + 90 + depth[n._uid] * dy

    cl = _level(S, S.get('now'))
    for lv, (txt, c) in ((cl, ('这一层', 'blue')), ((cl + 1) if cl is not None else None, ('下一层', 'pink'))):
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
    hit = {}
    for name, c in PTRS:
        v = S.get(name)
        if v is not None and v._uid in xi:
            hit.setdefault(v._uid, []).append((name, T[c]))
    for n in order:
        X, Y = P(n)
        hs = hit.get(n._uid, [])
        fill = hs[0][1] if hs else T['panel2']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), n.val, 26, T['bg'] if hs else T['text'], anchor='mm', bold=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X + R + 4, Y + 4 + r * 22), name, 19, cc, anchor='lt', bold=True)


def _w4(S, B, ret):
    if S.now is None:
        return '`next_head` 为空：下一层没有节点 → 结束'
    lv = _level(S, S.now)
    if lv == 0:
        return '一层一层往下做：第 0 层只有 `root`'
    return f'第 {lv} 层的 next 已经建好 → 用它来构建第 {lv + 1} 层的 next'


def _w7(S, B, ret):
    if S.now is None:
        return '这一层走完了'
    return f'处理这一层的节点 `now = {S.now.val}`，检查它的左右孩子'


def _ifc(side):
    def f(S, B, ret):
        ch = getattr(S.now, side)
        word = '左' if side == 'left' else '右'
        if ch is None:
            return f'`{S.now.val}` 没有{word}孩子 → 跳过'
        return f'`{S.now.val}` 有{word}孩子 `{ch.val}`'
    return f


def _ifh(side):
    def f(S, B, ret):
        ch = getattr(S.now, side)
        if not S.next_head:
            return f'`next_head` 还是空的 → `{ch.val}` 是下一层的==第一个节点=='
        return f'`next_head` 已经有了 → `{ch.val}` 要接在 `next_tail = {S.next_tail.val}` 后面'
    return f


def _link(side):
    def f(S, B, ret):
        ch = getattr(S.now, side)
        return f'处理到 `{ch.val}` 时才能确定：已处理过的最后一个节点 `{S.next_tail.val}` 的 ==next 是 {ch.val}=='
    return f


CONFIG = dict(
    num=117, title='填充每个节点的下一个右侧节点指针 II', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='逐层构建 · 维护 next_head / next_tail',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def connect(self, root):
        now = root
        while now:
            next_head = None
            next_tail = None
            while now:
                if now.left:
                    if not next_head:
                        next_head = now.left
                    else:
                        next_tail.next = now.left
                    next_tail = now.left
                if now.right:
                    if not next_head:
                        next_head = now.right
                    else:
                        next_tail.next = now.right
                    next_tail = now.right
                now = now.next

            now = next_head

        return root
''',
    setup=SETUP,
    call='Solution().connect(root)',
    result_fn=_ser,
    expect=[1, '#', 2, 3, '#', 4, 5, 7, '#'],
    views=[
        dict(type='text', size=26, fn=lambda S: '利用==这一层==的 next 遍历，同时构建==下一层==的 next'),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('now', lambda S: _v(S['now']), 'blue'), ('next_head', lambda S: _v(S['next_head']), 'cyan'),
           ('next_tail', lambda S: _v(S['next_tail']), 'pink')],
    captions={
        'now = root': '`now = root`：从第一层开始',
        4: _w4,
        'next_head = None': '`next_head`：下一层的第一个节点，先置空',
        'next_tail = None': '`next_tail`：下一层==已经处理过的最后一个节点==，先置空',
        7: _w7,
        8: _ifc('left'),
        9: _ifh('left'),
        'next_head = now.left': '记下下一层的第一个节点 `next_head = {next_head.val}`',
        'next_tail.next = now.left': _link('left'),
        'next_tail = now.left': '`next_tail` 更新为 `{next_tail.val}`',
        14: _ifc('right'),
        15: _ifh('right'),
        'next_head = now.right': '记下下一层的第一个节点 `next_head = {next_head.val}`',
        'next_tail.next = now.right': _link('right'),
        'next_tail = now.right': '`next_tail` 更新为 `{next_tail.val}`',
        'now = now.next': lambda S, B, r: (f'沿着已建好的 `{B.now.val}.next` 走到 `{S.now.val}`' if S.now
                                           else f'`{B.now.val}.next` 为空：这一层到头了'),
        'now = next_head': lambda S, B, r: (f'从 `next_head = {S.now.val}` 开始处理下一行' if S.now
                                            else '`next_head` 为空：没有下一行了'),
        'return root': '每一层的 next 都建好了，返回 `root`',
    },
    cards=dict(
        one_liner='用这一层的 next 遍历，维护下一层的头和尾来连 next',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给每个节点的 `next` 指针指向==同一层右侧==的下一个节点，没有则为 `NULL`',
                 '和 116 题不同：左右子树==不一定存在==',
                 '示例：`[1,2,3,4,5,null,7]` → `[1,#,2,3,#,4,5,7,#]`'],
        quote='只有当我们处理到3的右孩子7时，才能确定同一层已经处理过的最后一个节点5的next是7。……我们需要==维护好下一个层已经处理过的最后一个节点next_tail==。',
        quote_src='—— yiduobo 题解原文',
        idea=['116 题可以直接写“a 的 next 是 b”，这里 b 不一定存在',
              '改成：处理到节点 a 时，才把 `next_tail.next` 指向 a，再更新 `next_tail`',
              '还要记下一层的第一个节点 `next_head`，这一层做完从它开始下一行'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：第一个孩子没有前驱，要用 `if not next_head` 特判（灵神用哨兵节点省掉了这个判断）',
                 '每层开始时 `next_head`、`next_tail` 都要重置为 `None`',
                 '原文为 Python 2 写法：只删去了 Node 定义说明和类型文档字符串'],
    ),
)
