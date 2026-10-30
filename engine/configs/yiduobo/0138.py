import tracer as _tr


def _collect(S):
    nodes = {}

    def walk(v, d=0):
        if d > 30 or not isinstance(v, Node) or v._uid in nodes:
            return
        nodes[v._uid] = v
        walk(v.next, d + 1)
        walk(v.random, d + 1)
    for v in S.values():
        walk(v)
    return nodes


def _rl_view(ptrs, title, n):
    """138 专用：原链表在上排，拷贝节点在下排（正好在原节点正下方）；
    next 用灰色实线箭头，random 用紫色弧线（上排画在上方，下排画在下方）；本步改动的指针标黄。"""
    def place(S):
        nodes = _collect(S)
        org = _tr._origin
        pos = {u: org[u] for u in nodes if u in org}
        new = sorted(u for u in nodes if u not in org)
        for k, u in enumerate(new):
            pos[u] = (1, k + 1) if k < n else (1, 0)  # 第 n+1 个新节点是 dummy，放在下排最左
        return nodes, pos

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        nodes, pos = place(S)
        bnodes = _collect(B)
        gap = min(200, (x1 - x0 - 100) / (n + 1))
        nw, nh = min(70, gap * 0.5), 50
        rowy = [y0 + 175, y0 + 175 + min(190, (y1 - y0 - 330))]

        def xy(u):
            r, c = pos[u]
            return x0 + 50 + c * gap + nw / 2, rowy[r]

        def changed(u, attr):
            b = bnodes.get(u)
            return b is not None and getattr(getattr(b, attr), '_uid', None) != getattr(getattr(nodes[u], attr), '_uid', None)

        for u, nd in nodes.items():
            X, Y = xy(u)
            r, c = pos[u]
            for attr in ('next', 'random'):
                tg = getattr(nd, attr)
                ch = changed(u, attr)
                if tg is None:
                    if attr == 'next':
                        cv.text((X + nw / 2 + 6, Y), '∅', 22, T['yellow'] if ch else T['dim'], anchor='lm')
                    continue
                if tg._uid not in pos:
                    continue
                X2, Y2 = xy(tg._uid)
                r2, c2 = pos[tg._uid]
                if attr == 'random':
                    color, w = (T['yellow'], 3) if ch else (T['purple'], 2)
                    up = r == 0
                    sgn = 1 if c2 >= c else -1
                    p0 = (X + sgn * nw * 0.22, Y + (-nh / 2 if up else nh / 2))
                    p1 = (X2 - sgn * nw * 0.22, Y2 + (-nh / 2 - 3 if up else nh / 2 + 3))
                    lift = 34 + 12 * abs(c2 - c)
                    cv.arc_arrow(p0, p1, lift if up else -lift, color, w, 10)
                    continue
                color, w = (T['yellow'], 4) if ch else (T['muted'], 3)
                if r2 == r and c2 == c + 1:
                    cv.arrow((X + nw / 2 + 2, Y), (X2 - nw / 2 - 3, Y2), color, w, 12)
                elif r2 == r:
                    cv.arc_arrow((X, Y + nh / 2), (X2, Y2 + nh / 2 + 3), -(30 + 10 * abs(c2 - c)), color, w, 12)
                else:
                    down = r2 > r
                    s = 0 if c2 == c else (1 if c2 > c else -1)
                    p0 = (X + s * nw * 0.28, Y + (nh / 2 if down else -nh / 2))
                    p1 = (X2 - s * nw * 0.28, Y2 + (-nh / 2 - 3 if down else nh / 2 + 3))
                    cv.arrow(p0, p1, color, w, 12)
        hit = {}
        for name, c in (ptrs(S) if callable(ptrs) else ptrs).items():
            v = S.get(name)
            if isinstance(v, Node) and v._uid in pos:
                hit.setdefault(v._uid, []).append((name, T[c]))
        for u, nd in nodes.items():
            X, Y = xy(u)
            hs = hit.get(u, [])
            copy = pos[u][0] == 1
            fill = hs[0][1] if hs else ((40, 62, 58) if copy else T['panel2'])
            cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10,
                    outline=T['cyan'] if copy else T['border'], width=2)
            cv.text((X, Y), nd.val, 23, T['bg'] if hs else T['text'], anchor='mm', bold=True)
            for i, (name, cc) in enumerate(hs):
                if pos[u][1] == 0:  # 最左列：写在节点上方
                    cv.text((X, Y - nh / 2 - 4 - i * 24), name, 20, cc, anchor='mb', bold=True)
                else:  # 其余：写在节点左上方，避开中线上的箭头
                    cv.text((X - nw / 2 - 4, Y - 6 - i * 24), name, 20, cc, anchor='rb', bold=True)
        cv.text((x0 + 18, rowy[0] - nh / 2 - 92), '上排：原链表', 20, T['dim'])
        cv.text((x0 + 18, rowy[1] + nh / 2 + 70), '下排：新建的拷贝节点（青色边框）', 20, T['dim'])
        cv.text((x1 - 20, rowy[1] + nh / 2 + 70), '紫色弧线 = random', 20, T['purple'], anchor='ra')
    return draw


def _enc(head):
    out, x = [], head
    while x is not None and len(out) < 50:
        out.append(x)
        x = x.next
    idx = {id(v): i for i, v in enumerate(out)}
    return [[v.val, idx.get(id(v.random)) if v.random is not None else None] for v in out]


def _all_new(head):
    x = head
    while x is not None:
        if x._uid in _tr._origin:
            return False
        x = x.next
    return True


def _progress(S):
    nodes = _collect(S)
    N, R = 3, 2  # 本例：3 个节点，其中 2 个 random 非空
    copies = [v for u, v in nodes.items() if u not in _tr._origin]
    nr = sum(1 for v in copies if v.random is not None)
    s = f'已复制 =={len(copies)}==/{N} 个　·　p′ 的 random 已连 =={nr}==/{R}'
    if S.get('res') is not None:
        k, x = 0, S['res']
        while x is not None and x._uid not in _tr._origin and k < 20:
            k, x = k + 1, x.next
        j, x = 0, S.get('head')
        while x is not None and x._uid in _tr._origin and j < 20:
            j, x = j + 1, x.next
        s += f'　·　新链 =={k}==/{N}，原链 =={j}==/{N}'
    return s


CONFIG = dict(
    num=138, title='随机链表的复制', difficulty='Medium', category='链表',
    author='yiduobo', technique='p′ 接在 p 后面 + 拆分还原',
    code="""
class Solution(object):
    def copyRandomList(self, head):
        if not head:
            return head

        now = head
        while now:
            copy_now = Node(now.val)
            copy_now.next = now.next
            now.next = copy_now
            now = copy_now.next

        now = head
        while now:
            if now.random is not None:
                now.next.random = now.random.next
            now = now.next.next

        old_head = head
        res = new_head = head.next
        while old_head:
            old_head.next = new_head.next
            old_head = old_head.next
            if old_head:
                new_head.next = old_head.next
                new_head = new_head.next

        return res
""",
    # setup：手动建 3 个 Node 并接好 random（7→11，13→7，11→空）；_origin 只用于布局（原节点放上排）
    setup="""
import tracer
_vals, _rnd = [7, 13, 11], [2, 0, None]
_ns = [Node(v) for v in _vals]
for _i in range(len(_ns) - 1):
    _ns[_i].next = _ns[_i + 1]
for _i, _r in enumerate(_rnd):
    if _r is not None:
        _ns[_i].random = _ns[_r]
for _i, _nd in enumerate(_ns):
    tracer._origin[_nd._uid] = (0, _i + 1)
head = _ns[0]
""",
    call='Solution().copyRandomList(head)',
    expect=[[7, 2], [13, 0], [11, None]],
    result_fn=_enc,
    check=_all_new,
    views=[
        dict(type='text', fn=_progress),
        dict(type='custom', draw=_rl_view(lambda S: {'now': 'blue', 'copy_now': 'green'} if 'old_head' not in S else
                                          {'old_head': 'purple', 'new_head': 'pink', 'res': 'cyan'},
                                          '上排 p，下排 p′（灰色 = next，紫色 = random，黄色 = 这一步改的）', 3), h=560),
    ],
    watch=[('now', 'now', 'blue'), ('copy_now', 'copy_now', 'green'), ('old_head', 'old_head', 'purple'), ('new_head', 'new_head', 'pink')],
    captions={
        'if not head': lambda S, B, ret: '`head` 非空 → 不用特判' if B.head else '空链表直接返回',
        6: '第一段 while：对每个节点 `p` 复制出 `p′`',
        'copy_now = Node(now.val)': '复制节点 `{now.val}′`（先只有值）',
        'copy_now.next = now.next': lambda S, B, ret: '`{}′.next` = `p` 原来的下一个（{}）'.format(
            S.now.val, S.copy_now.next.val if S.copy_now.next else 'None'),
        'now.next = copy_now': '`p.next = p′`：把 `{now.val}′` 接在 `{now.val}` 的后面',
        'now = copy_now.next': lambda S, B, ret: '`now` 跳到下一个原节点 {}'.format(S.now.val if S.now else 'None（复制完毕）'),
        'while now:': lambda S, B, ret: '`now` = {} → 处理它'.format(B.now.val) if B.now else '`now` 为空 → 这一段结束',
        13: '第二段 while：设置 random 指针',
        'if now.random is not None': lambda S, B, ret: ('`p` = {} 的 random 是 `q` = {}'.format(B.now.val, B.now.random.val) if B.now.random
                                                        else '`p` = {} 的 random 为空，跳过'.format(B.now.val)),
        'now.next.random = now.random.next': '`p′.random = q′`，而 `q′` 就是 `q.next`：`{now.val}′ → {now.random.val}′`',
        'now = now.next.next': lambda S, B, ret: '跳过 `p′`，到下一个原节点 {}'.format(S.now.val if S.now else 'None'),
        'old_head = head': '第三段 while：逐个断开 `p` 与 `p′`，回到原先的连接方式',
        'res = new_head = head.next': '`res` 记下拷贝链表的头 `{res.val}′`',
        'while old_head': lambda S, B, ret: '`old_head` = {} → 拆开这一对'.format(B.old_head.val) if B.old_head else '原链表走完了',
        'old_head.next = new_head.next': lambda S, B, ret: '原节点 `{}` 的 next 改回 `{}`（恢复原链表）'.format(
            S.old_head.val, S.old_head.next.val if S.old_head.next else 'None'),
        'old_head = old_head.next': lambda S, B, ret: '`old_head` → {}'.format(S.old_head.val if S.old_head else 'None'),
        'if old_head:': lambda S, B, ret: '后面还有原节点 → 拷贝也要接到下一个拷贝' if B.old_head else '后面没有了：最后一个 `p′.next` 本来就是空',
        'new_head.next = old_head.next': '`{new_head.val}′.next = {new_head.next.val}′`：拷贝之间连起来',
        'new_head = new_head.next': '`new_head` → `{new_head.val}′`',
        'return res': '返回拷贝链表的头 `res`',
    },
    cards=dict(
        one_liner='把 p′ 接在 p 后面：q′ 就是 q.next，random 一步就能连上',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['链表每个节点多一个 `random` 指针，可指向任意节点或空',
                 '构造它的==深拷贝==：新节点的 `next`、`random` 都只能指向新节点',
                 '本例：`[[7,2],[13,0],[11,null]]`（`[val, random 下标]`）'],
        quote="我在这里的做法是对于每个节点p，复制节点p'接在p的后面。设p的random为q，那么我们需要将p'的random指向到q'。由于q'为q的next……",
        quote_src='—— yiduobo 题解',
        idea=['第一段：每个 `p` 后面插入 `p′`，链表变成 `p → p′ → …`',
              "第二段：`p.random = q` ⇒ `p′.random = q′ = q.next`",
              '第三段：逐个断开 `p` 与 `p′`，==原链表恢复原样==，拷贝链表单独成链'],
        summary=['三段 while：复制 → 连 random → 拆分；时间 `O(n)`，空间 `O(1)`',
                 'random 要等所有 `p′` 都插好后再连：`q′` 可能在 `p′` 后面才创建',
                 '拆分时==同时恢复原链表==：`old_head.next = new_head.next`',
                 '原文为 Python 2 写法：仅删掉了 `"""type"""` 文档字符串，逻辑未改'],
    ),
)
