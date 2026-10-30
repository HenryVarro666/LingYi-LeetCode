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


A, C = 3, 4  # 本例：头节点到入环口 a = 3 步，环长 c = 4


def _pos(t):
    return t if t < A else A + (t - A) % C


def _idx(S, name):
    # 节点在输入链表中的下标（建表时记录在 tracer._origin 里；head 在第二阶段会移动，不能从 head 数）
    nd = S.get(name)
    return _tr._origin[nd._uid][1] if nd is not None and nd._uid in _tr._origin else None


def _phase1(S):
    i, j = _idx(S, 'slow'), _idx(S, 'fast')
    if i is None or j is None or _idx(S, 'head') != 0:
        return None
    return next((t for t in range(A + C) if _pos(t) == i and _pos(2 * t) == j), None)


def _info(S):
    if 'slow' not in S:
        return f'本例：头节点到入环口 `a = {A}` 步，环长 `c = {C}`'
    t = _phase1(S)
    if t is not None:
        if t and S['slow'] is S['fast']:
            return f'相遇：慢指针走了 `b = {t}` 步 `= kc`（`k = 1`），停在入环口后 `kc − a = {t - A}` 步'
        return f'`a = {A}`，`c = {C}`　　慢指针已走 =={t}== 步，快指针已走 =={2 * t}== 步'
    return f'第二阶段：`head` 已走 =={_idx(S, "head")}== 步（目标 `a = {A}`），慢指针在环里同速走'


def _deco(cv, S, nodes, xy, T):
    # 标出入环口、环外段长度和环长
    inv = {c: u for u, (r, c) in _tr._origin.items()}
    if inv.get(3) in nodes:
        X, Y = xy(inv[3])
        cv.text((X, Y + 66), '入环口', 22, T['yellow'], anchor='mt', bold=True)
    if inv.get(0) in nodes and inv.get(3) in nodes:
        Xa, Y = xy(inv[0])
        Xb, _ = xy(inv[3])
        cv.text(((Xa + Xb) / 2, Y + 66), f'环外 `a` = {A} 步'.replace('`', ''), 22, T['muted'], anchor='mt')
    last = max(inv)
    if inv.get(last) in nodes and inv.get(3) in nodes:
        Xa, Y = xy(inv[3])
        Xb, _ = xy(inv[last])
        cv.text(((Xa + Xb) / 2, Y + 112), f'环长 c = {C}', 22, T['muted'], anchor='mt')


CONFIG = dict(
    num=142, title='环形链表 II', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='快慢指针 · Floyd 判圈算法',
    code='''
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if fast is slow:  # 相遇
                while slow is not head:  # 再走 a 步
                    slow = slow.next
                    head = head.next
                return slow
        return None
''',
    call='Solution().detectCycle(L([1, 2, 3, 4, 5, 6, 7], 3))',
    result_fn=lambda node: node.val,
    expect=4,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=480, draw=_ll({'slow': 'green', 'fast': 'pink', 'head': 'orange'},
                                             title='链表：尾节点 7 指回下标 3（入环口是 4）', deco=_deco)),
    ],
    watch=[('slow', 'slow', 'green'), ('fast', 'fast', 'pink'), ('head', 'head', 'orange')],
    captions={
        3: '快慢指针都从头节点出发（和 141 一样）',
        4: lambda S, B, r: ('快指针还能走两步 → 继续' if S.fast and S.fast.next else '快指针走到末尾 → 无环'),
        5: lambda S, B, r: f'慢指针走 1 步 → `{S.slow.val}`',
        6: lambda S, B, r: f'快指针走 2 步 → `{S.fast.val}`',
        7: lambda S, B, r: (f'==相遇==：快指针比慢指针多走了整数圈 → 慢指针走了 `kc` 步，在入环口后 `kc − a = {_idx(S, "slow") - A}` 步'
                            if S.fast is S.slow else f'快指针在 `{S.fast.val}`、慢指针在 `{S.slow.val}`，还没相遇'),
        8: lambda S, B, r: ((f'`slow`（{S.slow.val}）不是 `head`（{S.head.val}）→ 两人同速各走一步。==再走 a 步==就会在入环口碰头'
                             if _idx(S, 'head') == 0 else f'`slow`（{S.slow.val}）还不是 `head`（{S.head.val}）→ 继续')
                            if S.slow is not S.head else f'`slow is head`：两人都走了 `a = {A}` 步，在==入环口== `{S.slow.val}` 相遇'),
        9: lambda S, B, r: f'慢指针从相遇点继续走 → `{S.slow.val}`',
        10: lambda S, B, r: f'`head` 从头节点往后走 → `{S.head.val}`',
        11: lambda S, B, r: f'返回入环口 `{r.val}`',
    },
    cards=dict(
        one_liner='快慢指针相遇后，让慢指针和 head 同速再走 a 步，就在入环口碰头',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定链表的头节点 `head`，返回链表==开始入环的第一个节点==；无环返回 `null`',
                 '示例：`[1,2,3,4,5,6,7]`，尾节点连到下标 3 → 返回值为 `4` 的节点',
                 '==不允许修改==链表'],
        quote='`kc−a` 是从==入环口==开始的步数。由于 `(kc−a) + a = kc`，所以从 `kc−a` 开始，再走 `a` 步，就恰好走了 `k` 圈，回到入环口。',
        quote_src='—— 灵茶山艾府题解 · 注 1',
        idea=['设头节点到入环口要走 `a` 步，环长 `c`；相遇时慢指针走了 `b` 步，快指针走了 `2b` 步',
              '快指针比慢指针多绕了整数圈：`2b − b = kc`，所以 `b = kc`',
              '慢指针已在环里走了 `kc−a` 步，再走 `a` 步回到入环口；`head` 走 `a` 步也到这'],
        summary=['时间 `O(n)`，空间 `O(1)`；这个算法叫 ==Floyd 判圈算法==',
                 '注 2：慢指针走那 `a` 步时，可能会多次经过入环口（环很小时）',
                 '直接复用 `head` 当第二个指针，省一个变量',
                 '比较用 `is`：比的是节点地址，不是 `val`'],
    ),
)
