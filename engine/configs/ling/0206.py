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


def _chain(node):
    vals = list_vals(node)
    return ' → '.join(map(str, vals)) if vals else '空'


def _rest(S):
    # 原链表里还没插进新链表的部分：cur 已经头插（cur.next 指向 pre 或 pre 已经是 cur）时从 nxt 算起
    cur, pre = S.get('cur'), S.get('pre')
    if cur is not None and 'nxt' in S and (cur.next is pre or cur is pre):
        return _chain(S['nxt'])
    return _chain(cur)


CONFIG = dict(
    num=206, title='反转链表', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='迭代 · 头插法',
    code='''
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = pre  # 把 cur 插在 pre 链表的前面（头插法）
            pre = cur
            cur = nxt
        return pre
''',
    call='Solution().reverseList(L([1, 2, 3, 4, 5]))',
    expect=[5, 4, 3, 2, 1],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: f"新链表 `pre`：=={_chain(S.get('pre'))}==　　原链表还剩：{_rest(S)}" if 'cur' in S else ''),
        dict(type='custom', h=480, draw=_ll({'pre': 'pink', 'cur': 'blue', 'nxt': 'green'},
                                             title='链表（黄色箭头 = 这一步刚改的 next）')),
    ],
    watch=[('pre', 'pre', 'pink'), ('cur', 'cur', 'blue'), ('nxt', 'nxt', 'green')],
    captions={
        'pre = None': '`pre` 表示==新链表==的头节点：一开始新链表是空的，所以 `pre = None`',
        'cur = head': '`cur` 指向原链表中==还没处理==的第一个节点 `{cur.val}`',
        'while cur': lambda S, B, r: (f'`cur = {S.cur.val}` 还没插进新链表 → 继续循环' if S.cur
                                      else '`cur` 为空：所有节点都已插进新链表 → ==循环结束=='),
        'nxt = cur.next': lambda S, B, r: ((f'先用 `nxt` 记住下一个节点 `{S.nxt.val}`：下一步要改 `cur.next`，==不先记下就找不到它了==' if S.pre is None
                                            else f'先存下一个节点：`nxt = {S.nxt.val}`') if S.nxt
                                           else '先存下一个节点：`cur` 已是最后一个，`nxt = None`'),
        'cur.next = pre': lambda S, B, r: (f'头插法：`{S.cur.val}.next` 改为指向新链表的头 `pre`'
                                           + (f'（{S.pre.val}）' if S.pre else '（None，新链表还是空的）')
                                           + f' → =={_chain(S.cur)}=='),
        'pre = cur': lambda S, B, r: (f'`cur` 成了新链表的头 → `pre = {S.pre.val}`。==每轮循环结束，pre 都是最新的新链表=='
                                      if B.pre is None else f'`pre` 移到新的头 `{S.pre.val}`，新链表：=={_chain(S.pre)}=='),
        'cur = nxt': lambda S, B, r: (f'`cur` 走到刚才记下的 `nxt`（{S.cur.val}），处理下一个' if S.cur
                                      else '`cur` 走到 `nxt`，也就是 `None`'),
        'return pre': lambda S, B, r: f'返回新链表的头 `pre` → =={_chain(r)}==',
    },
    cards=dict(
        one_liner='把节点逐个「头插」到一条新链表上，插完就反转了',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你单链表的头节点 `head`，反转链表，返回反转后的链表',
                 '示例：`[1,2,3,4,5]` → `[5,4,3,2,1]`',
                 '节点数 `[0, 5000]`，链表可能为空'],
        quote='创建一个新的空链表，然后用==头插法==依次把节点 1,2,3 插到这个新链表的头部，就得到了链表 3→2→1，这正是反转后的链表。',
        quote_src='—— 灵茶山艾府题解（方法二：迭代）',
        idea=['头插：`node.next = 新链表头`，`node` 就成了新的头',
              '`pre` = 新链表的头，`cur` = 原链表待处理的节点',
              '改 `cur.next` 前先用 `nxt` 存下一个节点，否则原链表断了'],
        summary=['时间 `O(n)`，空间 `O(1)`；空链表时循环不执行，直接返回 `None`',
                 '四行顺序别乱：==先存 nxt，再改指针==，然后 pre、cur 各前进一步',
                 '返回的是 `pre`，不是 `cur`（循环结束时 `cur` 是 `None`）',
                 '灵神的另一种写法：递归（尾插法），先递到末尾再在归的过程中尾插，空间 `O(n)`'],
    ),
)
