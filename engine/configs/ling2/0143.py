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


def _ll(ptrs, title='链表', place=None, deco=None, ghost_dim=True):
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
            lc, lw = (T['yellow'], 4) if ch else ((T['dim'], 2) if u in ghost and ghost_dim else (T['muted'], 3))
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
            if '.' in name:  # 'func.var'：只取某个函数栈帧里的变量（避免内层同名参数抢走标签）
                fn, var = name.split('.', 1)
                v = next((fr['locals'].get(var) for fr in (st.get('_frames') or []) if fr['name'] == fn), None)
            else:
                var, v = name, S.get(name)
            if isinstance(v, ListNode):
                hit.setdefault(v._uid, []).append((var, T[cc]))
        for u, nd in alln.items():
            X, Y = xy(u)
            hs = hit.get(u, [])
            bn = bnodes.get(u)
            vch = bn is not None and bn.val != nd.val
            gh = u in ghost and ghost_dim  # ghost_dim=False：没有变量指向但仍在链表里的节点照常画
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


def _v(x):
    return '∅' if x is None else str(x.val)


def _chain(node, limit=8):
    vals = list_vals(node)[:limit]
    return ' → '.join(map(str, vals)) if vals else '空'


def _info(S):
    if 'head2' in S and S['_line'] >= 23:
        return f"③ 合并：`head` 链 {_chain(S['head'])}　　`head2` 链 =={_chain(S['head2'])}=="
    if 'pre' in S or 'cur' in S:
        return f"② 反转后半段：`pre` = =={_chain(S.get('pre'))}=="
    if 'slow' in S:
        return '① 快慢指针找中间节点：`slow` 走 1 步，`fast` 走 2 步'
    return '① 找中间节点　② 反转后半段　③ 两条链交替合并'


CONFIG = dict(
    num=143, title='重排链表', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='876 找中点 + 206 反转 + 交替合并',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    # 876. 链表的中间结点
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    # 206. 反转链表
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre

    def reorderList(self, head: Optional[ListNode]) -> None:
        mid = self.middleNode(head)
        head2 = self.reverseList(mid)
        while head2.next:
            nxt = head.next
            nxt2 = head2.next
            head.next = head2
            head2.next = nxt
            head = nxt
            head2 = nxt2
''',
    call='''h = L([1, 2, 3, 4, 5, 6])
Solution().reorderList(h)
list_vals(h)''',
    expect=[1, 6, 2, 5, 3, 4],
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=430, draw=_ll({'reorderList.head': 'orange', 'head2': 'cyan', 'mid': 'purple',
                                              'slow': 'blue', 'fast': 'pink', 'pre': 'pink', 'cur': 'blue',
                                              'nxt': 'green', 'nxt2': 'yellow'},
                                             title='链表（黄色箭头 = 这一步刚改的 next）', ghost_dim=False)),
        dict(type='calls', h=150),
    ],
    watch=['slow', 'fast', ('pre', 'pre', 'pink'), ('cur', 'cur', 'blue'), ('head2', 'head2', 'cyan'),
           ('nxt', 'nxt', 'green'), ('nxt2', 'nxt2', 'yellow')],
    captions={
        'mid = self.middleNode': '① 先找==中间节点==（876 题）',
        'slow = fast = head': '快慢指针都从头节点出发',
        'while fast and fast.next': lambda S, B, r: ('`fast` 还能走两步 → 继续' if S.fast and S.fast.next else
                                                     f'`fast` 走到空了（偶数个节点）→ `slow = {_v(S.slow)}` 是==正中间偏右=='
                                                     if S.fast is None else
                                                     f'`fast` 是最后一个节点（奇数个）→ `slow = {_v(S.slow)}` 是正中间'),
        'slow = slow.next': lambda S, B, r: f'`slow` 走 1 步 → `{_v(S.slow)}`',
        'fast = fast.next.next': lambda S, B, r: f'`fast` 走 2 步 → `{_v(S.fast)}`',
        'return slow': '返回中间节点 `{ret.val}`：从它到末尾是==后半段==',
        'head2 = self.reverseList': '② 把后半段反转（206 题），反转后从 `head2` 能==从右往左==访问',
        'pre, cur = None, head': '`pre = None`，`cur` 从中间节点 `{cur.val}` 出发',
        'while cur': lambda S, B, r: ('`cur` 不为空 → 继续头插' if S.cur else '`cur` 为空 → 后半段反转完毕'),
        'nxt = cur.next': lambda S, B, r: f'记住下一个 `nxt = {_v(S.nxt)}`',
        'nxt = head.next': '先存 `nxt = head.next = {nxt.val}`',
        'cur.next = pre': lambda S, B, r: (f'`{S.cur.val}.next = None`：中间节点变成末尾，==前半段指向它的边还在=='
                                           if S.pre is None else f'`{S.cur.val}.next` 指向 `{S.pre.val}`'),
        'pre = cur': lambda S, B, r: f'`pre` → `{S.pre.val}`',
        'cur = nxt': lambda S, B, r: f'`cur` → `{_v(S.cur)}`',
        'return pre': lambda S, B, r: f'返回 `{r.val}`：`head2` 链 = =={_chain(r)}==',
        'while head2.next': lambda S, B, r: (
            f'`head2.next = {_v(S.head2.next)}` 不为空 → 继续合并' if S.head2.next else
            f'`head2.next` 为空 → 停！两条链都包含 `{S.head2.val}`，==写成 while head2 会让它指向自己=='),
        'nxt2 = head2.next': '再存 `nxt2 = head2.next = {nxt2.val}`：两个 next 都要改，先都存好',
        'head.next = head2': '`{head.val}.next` → `{head2.val}`：前半段的节点后面接一个后半段的节点',
        'head2.next = nxt': '`{head2.val}.next` → `{nxt.val}`：再接回前半段的下一个',
        'head = nxt': '`head` 前进到 `{head.val}`',
        'head2 = nxt2': '`head2` 前进到 `{head2.val}`',
    },
    cards=dict(
        one_liner='找中间节点，反转后半段，再把两条链交替合并',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['单链表 `L0 → L1 → … → Ln` 重排为 `L0 → Ln → L1 → Ln-1 → L2 → …`',
                 '==不能只改节点的值==，要实际交换节点',
                 '示例：`[1,2,3,4]` → `[1,4,2,3]`；`[1,2,3,4,5]` → `[1,5,2,4,3]`'],
        quote='两个链表分别为 head=[1,2,3] 和 head2=[4,3]。==注意它俩都包含节点 3==……如果写成 while head2，会导致最后一轮循环中 3 指向它自己。',
        quote_src='—— 灵茶山艾府题解（答疑：为什么是 while head2.next）',
        idea=['拼两道前置题：876 找中间节点（偶数个取==正中间偏右==）+ 206 反转',
              '反转后：`head` 链 = 前半段 + 中间节点，`head2` 链 = 末尾 → … → 中间节点',
              '每轮先存两个 next，再交叉连接：`head → head2 → 原 head.next`'],
        result='重排为 `[1,6,2,5,3,4]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`；直接修改原链表，没有返回值',
                 '循环条件是 `while head2.next`，==不是 while head2==（两条链共享中间节点）',
                 '合并时先存 `nxt`、`nxt2` 再改指针，否则会丢节点',
                 '最相似的题：234 回文链表（同样是找中点 + 反转后半段）'],
    ),
)
