import sys as _sys
import tracer as _tr


def _up(name, test, depth=16):
    # 取调用栈上层的局部变量（custom 视图只拿到合并后的 S；这里取完整帧列表与全部关键帧）
    f = _sys._getframe(2)
    for _ in range(depth):
        if f is None:
            return None
        v = f.f_locals.get(name)
        if v is not None and test(v):
            return v
        f = f.f_back
    return None


def _reach(frames, S):
    vals = [v for fr in frames for v in fr['locals'].values()] if frames else list(S.values())
    nodes = {}
    for v in vals:
        while isinstance(v, ListNode) and v._uid not in nodes:
            nodes[v._uid] = v
            v = v.next
    return nodes


def _ll(ptrs, title='链表', place=None, deco=None):
    """自绘链表：相邻节点用直箭头（反向链接走下方车道），远距离链接画在节点下方的弧线；
    指针名写在节点上方；这一步改动过的 next 用黄色；已经没有变量指向的节点画成暗色（ghost）。"""
    cache = {}

    def history():
        vid = _up('self', lambda x: hasattr(x, 'keys') and hasattr(x, 'draw_viz'))
        if vid is None:
            return []
        if id(vid) not in cache:
            order, seen = [], set()
            for stt, _, _ in vid.keys:
                S_ = stt.get('_S')
                if S_ is None or id(S_) in seen:
                    continue
                seen.add(id(S_))
                order.append((id(S_), _reach(stt.get('_frames'), S_)))
            cache[id(vid)] = order
        return cache[id(vid)]

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        st = _up('st', lambda x: isinstance(x, dict) and '_S' in x) or {}
        nodes = _reach(st.get('_frames'), S)
        hist = history()
        idx = next((i for i, (k, _) in enumerate(hist) if k == id(S)), None)
        ghost = {}
        if idx is not None:
            for j in range(idx - 1, -1, -1):
                for u, nd in hist[j][1].items():
                    if u not in nodes and u not in ghost:
                        ghost[u] = nd
        bnodes = _reach(None, B)
        if idx:
            for u, nd in hist[idx - 1][1].items():
                bnodes.setdefault(u, nd)
        alln = dict(ghost)
        alln.update(nodes)
        org = _tr._origin
        base = max([r for r, c in org.values()] + [-1]) + 1
        every = set(alln)
        for _, nd in hist:
            every |= set(nd)
        pos = {u: org[u] for u in every if u in org}
        for k, u in enumerate(sorted(u for u in every if u not in org)):
            pos[u] = place(k, base) if place else (base, k)
        allp = list(org.values()) + list(pos.values())
        R = max(r for r, c in allp) + 1
        C = max(c for r, c in allp) + 1
        gap = min(150, (x1 - x0 - 100) / C)
        nw, nh = min(84, gap * 0.58), 60
        top = y0 + 118
        rowh = min(180, (y1 - top - nh - 50) / max(1, R - 1)) if R > 1 else 0
        top = max(top, (y0 + y1) / 2 + 20 - (nh + rowh * (R - 1)) / 2)
        left = x0 + max(50, (x1 - x0 - C * gap) / 2 + (gap - nw) / 2 - 10)

        def xy(u):
            r, c = pos[u]
            return left + c * gap + nw / 2, top + nh / 2 + r * rowh

        fwd, back = set(), set()
        for u, nd in alln.items():
            r, c = pos[u]
            p2 = pos.get(getattr(nd.next, '_uid', None))
            if nd.next is None or p2 == (r, c + 1):
                fwd.add((r, c))
            elif p2 == (r, c - 1):
                back.add((r, c - 1))
        both = fwd & back
        for u, nd in alln.items():
            X, Y = xy(u)
            r, c = pos[u]
            nx = nd.next
            bn = bnodes.get(u)
            ch = bn is not None and getattr(bn.next, '_uid', None) != getattr(nx, '_uid', None)
            lc, lw = (T['yellow'], 4) if ch else ((T['dim'], 2) if u in ghost else (T['muted'], 3))
            if nx is None:
                cv.text((X + nw / 2 + 8, Y - (11 if (r, c) in both else 0)), '∅', 24,
                        T['yellow'] if ch else T['dim'], anchor='lm')
                continue
            if nx._uid not in pos:
                continue
            X2, Y2 = xy(nx._uid)
            r2, c2 = pos[nx._uid]
            if r2 == r and c2 == c + 1:
                d = -11 if (r, c) in both else 0
                cv.arrow((X + nw / 2, Y + d), (X2 - nw / 2 - 2, Y2 + d), lc, lw, 12)
            elif r2 == r and c2 == c - 1:
                d = 11 if (r, c2) in both else 0
                cv.arrow((X - nw / 2, Y + d), (X2 + nw / 2 + 2, Y2 + d), lc, lw, 12)
            elif r2 == r:
                cv.arc_arrow((X, Y + nh / 2), (X2, Y2 + nh / 2 + 2), -(34 + abs(X2 - X) * 0.1), lc, lw, 12)
            else:
                if abs(X2 - X) < 1:  # 竖直箭头往右偏一点，避开节点上方的指针名
                    X, X2 = X + nw * 0.3, X2 + nw * 0.3
                dx, dy = X2 - X, Y2 - Y
                t0 = min((nw / 2) / abs(dx) if dx else 9e9, (nh / 2) / abs(dy) if dy else 9e9)
                t1 = t0 + 4 / math.hypot(dx, dy)
                cv.arrow((X + dx * t0, Y + dy * t0), (X2 - dx * t1, Y2 - dy * t1), lc, lw, 12)
        hit = {}
        for name, cc in ptrs.items():
            v = S.get(name)
            if isinstance(v, ListNode):
                hit.setdefault(v._uid, []).append((name, T[cc]))
        for u, nd in alln.items():
            X, Y = xy(u)
            hs = hit.get(u, [])
            bn = bnodes.get(u)
            vch = bn is not None and bn.val != nd.val
            gh = u in ghost
            fill = hs[0][1] if hs else ((24, 28, 35) if gh else T['panel2'])
            cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10,
                    outline=T['yellow'] if vch else T['border'], width=4 if vch else 2)
            cv.text((X, Y), str(nd.val), 30, T['bg'] if hs else (T['dim'] if gh else T['text']), anchor='mm', bold=True)
            for k, (name, cc) in enumerate(hs):
                cv.text((X, Y - nh / 2 - 6 - k * 26), name, 22, cc, anchor='mb', bold=True)
        if deco:
            deco(cv, S, alln, xy, T)
        nones = [n for n in ptrs if n in S and S[n] is None]
        if nones:
            cv.text((x1 - 20, y0 + 6), '  '.join(f'{n}=None' for n in nones), 20, T['muted'], anchor='ra', mono=True)
    return draw


def _route(S, first, second):
    # 指针的完整路线：first 链表全程 → 空节点 → second 链表全程
    return _tr.Lnodes(S.get(first)) + [None] + _tr.Lnodes(S.get(second))


def _v(x):
    return '∅' if x is None else str(x.val)


def _steps(S):
    # q 先在自己的路线上定位（kq 步）；p 和 q 每轮各走一步，p 已走 kq 或 kq + 1 步（同一轮里 p 先走）
    if 'p' not in S:
        return None
    rp, rq = _route(S, 'headA', 'headB'), _route(S, 'headB', 'headA')
    for kq in range(len(rq)):
        if rq[kq] is S['q']:
            for kp in (kq, kq + 1):
                if kp < len(rp) and rp[kp] is S['p']:
                    return kp, kq
    return None


def _info(S):
    k = _steps(S)
    if k is None:
        return '`p` 的路线：A 全程 → ∅ → B　　`q` 的路线：B 全程 → ∅ → A'
    if S['p'] is S['q']:
        return f'各走了 =={k[0]}== 步：`p` 走 a + c + 1 + b，`q` 走 b + c + 1 + a，都是 2 + 3 + 1 + 3 = =={k[0]}=='
    return f'`p`：A 全程 → ∅ → B（已走 =={k[0]}== 步）　`q`：B 全程 → ∅ → A（已走 =={k[1]}== 步）'


def _deco(cv, S, nodes, xy, T):
    for name, lab in (('headA', 'A'), ('headB', 'B')):
        v = S.get(name)
        if v is not None:
            X, Y = xy(v._uid)
            cv.text((X - 58, Y), lab, 28, T['muted'], anchor='rm', bold=True)
    a = S.get('headA')
    if a is not None and a.next is not None and a.next.next is not None and a.next.next.next is not None:
        X, Y = xy(a.next.next.next._uid)
        cv.text((X, Y + 44), '公共部分（c = 3）', 22, T['muted'], anchor='mt')


CONFIG = dict(
    num='LCR 023', title='相交链表', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='双指针 · 走完自己的路再走对方的路',
    code='''
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        p, q = headA, headB
        while p is not q:
            p = p.next if p else headB
            q = q.next if q else headA
        return p
''',
    setup='''
import tracer
headA, headB, common = L([4, 1]), L([5, 6, 1]), L([8, 4, 5])
tracer.Lnodes(headA)[-1].next = common
tracer.Lnodes(headB)[-1].next = common
for i, nd in enumerate(tracer.Lnodes(headA)[:2]): tracer._origin[nd._uid] = (0, i + 1)
for i, nd in enumerate(tracer.Lnodes(common)): tracer._origin[nd._uid] = (1, i + 3)
for i, nd in enumerate(tracer.Lnodes(headB)[:3]): tracer._origin[nd._uid] = (2, i)
''',
    call='Solution().getIntersectionNode(headA, headB)',
    result_fn=lambda node: node.val,
    expect=8,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=500, draw=_ll({'p': 'blue', 'q': 'pink'}, title='两条链表在 8 处汇合（Y 字形）', deco=_deco)),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink')],
    captions={
        'p, q = headA': '`p` 从 A 的头 `4` 出发，`q` 从 B 的头 `5` 出发',
        'while p is not q': lambda S, B, r: (
            '`p is q`：两个指针指向==同一个节点== → 循环结束' if S.p is S.q else
            (f'`p`、`q` 的值都是 `{S.p.val}`，但==不是同一个节点==（比较的是地址，不是值）→ 继续'
             if S.p is not None and S.q is not None and S.p.val == S.q.val else
             f'`p`（{_v(S.p)}）和 `q`（{_v(S.q)}）不是同一个节点 → 继续走')),
        'p = p.next if p': lambda S, B, r: ('`p` 已在 A 末尾的空节点 → ==换到 B 的头== `headB`' if B.p is None else
                                            (f'`p` 向后走一步 → `{S.p.val}`' if S.p is not None else
                                             '`p` 走完 A，来到空节点（这也算一步）')),
        'q = q.next if q': lambda S, B, r: ('`q` 已在 B 末尾的空节点 → ==换到 A 的头== `headA`' if B.q is None else
                                            (f'`q` 向后走一步 → `{S.q.val}`' if S.q is not None else
                                             '`q` 走完 B，来到空节点（这也算一步）')),
        'return p': lambda S, B, r: f'两人走的总步数相同，==在相交的起始节点相遇==：返回 `{r.val}`',
    },
    cards=dict(
        one_liner='p 走完 A 再走 B，q 走完 B 再走 A，路程一样长，必在交点相遇',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['给你两个链表的头节点 `headA`、`headB`，返回==相交的起始节点==；不相交返回 `null`',
                 '示例：A = `[4,1,8,4,5]`，B = `[5,6,1,8,4,5]`，从 `8` 开始相交',
                 '注意：两条链里的 `1` 值相同，但==不是同一个节点=='],
        quote='每次循环，p 和 q 各向后走一步。如果 p 不是空节点，那么更新 p 为 p.next，==否则更新 p 为 headB==；q 同理（空了就换到 headA）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['A 独有 `a` 个节点、B 独有 `b` 个、公共 `c` 个',
              '`p` 走 `a+c`、再走 `b` 到交点；`q` 走 `b+c`、再走 `a` 到交点',
              '两人路程都是 `a+b+c`（各算上一步空节点），==同时到达交点=='],
        summary=['时间 `O(m+n)`，空间 `O(1)`；==不修改链表结构==',
                 '比较用 `is`（同一个节点），不是比较 `val`',
                 '不相交时：两人都走 `m+n+1` 步后同时变成 `None`，`p is q` 成立，返回 `None`',
                 '空节点也算一步，正是它让两人的步数对齐'],
    ),
)
