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


def _v(x):
    return '∅' if x is None else str(x.val)


def _deco(cv, S, nodes, xy, T):
    for name, lab in (('headA', 'list1'), ('headB', 'list2')):
        v = S.get(name)
        if v is not None:
            X, Y = xy(v._uid)
            cv.text((X - 54, Y), lab, 24, T['muted'], anchor='rm', bold=True)


def _cmp(S, B, r):
    if S.p1 is S.p2:
        return '`p1 == p2`：走到了==同一个节点== → 这就是交点'
    if S.p1.val == S.p2.val:
        return f'值都是 `{S.p1.val}`，但==不是同一个节点==（比较的是节点对象本身）→ 继续'
    return f'`{S.p1.val}` 和 `{S.p2.val}` 不是同一个节点 → 继续'


CONFIG = dict(
    num=160, title='相交链表', difficulty='Easy', category='链表',
    author='yiduobo', technique='长度差对齐 · 三段同步走',
    code='''
class Solution(object):
    def getIntersectionNode(self, headA, headB):
        p1 = headA
        p2 = headB
        while p1 and p2:
            p1 = p1.next
            p2 = p2.next

        if not p1:
            p1 = headB
        else:
            p2 = headA

        while p1 and p2:
            p1 = p1.next
            p2 = p2.next

        if not p1:
            p1 = headB
        else:
            p2 = headA

        while p1 and p2:
            if p1 == p2:
                return p1
            p1 = p1.next
            p2 = p2.next

        return None
''',
    setup='''
import tracer
headA, headB, common = L([5, 6, 1]), L([4, 1]), L([8, 4, 5])
tracer.Lnodes(headA)[-1].next = common
tracer.Lnodes(headB)[-1].next = common
for i, nd in enumerate(tracer.Lnodes(headA)[:3]): tracer._origin[nd._uid] = (0, i)
for i, nd in enumerate(tracer.Lnodes(common)): tracer._origin[nd._uid] = (1, i + 3)
for i, nd in enumerate(tracer.Lnodes(headB)[:2]): tracer._origin[nd._uid] = (2, i + 1)
''',
    call='Solution().getIntersectionNode(headA, headB)',
    result_fn=lambda node: node.val,
    expect=8,
    views=[
        dict(type='text', text='`L1 = 6`，`L2 = 5` → 相交后 `step1 − step2 = L1 − L2 = 1`', size=26),
        dict(type='custom', h=500, draw=_ll({'p1': 'blue', 'p2': 'pink'}, title='list1 比 list2 长 1 个节点', deco=_deco)),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink')],
    captions={
        3: '`p1` 从 list1 的表头出发',
        4: '`p2` 从 list2 的表头出发',
        5: lambda S, B, r: (('① 两个指针同时往后走，直到有一个走到末尾' if S.p1 is S.headA else '① 继续同时走') if S.p1 and S.p2 else
                            ('`p2` 先走到 list2 末尾 → 此时 `p1` 离 list1 末尾==还差 1 步==（`L1 − L2`）' if S.p1
                             else '`p1` 先走到末尾（A 更短，角色互换）')),
        6: lambda S, B, r: f'`p1` → `{_v(S.p1)}`',
        7: lambda S, B, r: f'`p2` → `{_v(S.p2)}`',
        9: lambda S, B, r: (f'谁先走完？`p1` 还在 `{_v(S.p1)}` → 是 `p2` 先走完' if S.p1 else '`p1` 先走完了'),
        12: '② `p2` 换到 ==list1 的表头==，再和 `p1` 同时走',
        14: lambda S, B, r: ('② 同时走：`p1` 走到 list1 末尾之前，`p2` 一直跟着走' if S.p1 and S.p2 else
                             '`p1` 走完 list1 → `p2` 恰好在 list1 中==走了 1 步==（`L1 − L2`）'),
        15: lambda S, B, r: f'`p1` → `{_v(S.p1)}`',
        16: lambda S, B, r: f'`p2` → `{_v(S.p2)}`（在 list1 里）',
        18: lambda S, B, r: ('`p1` 走完了 list1 → 让它去 list2' if not S.p1 else '`p2` 走完了'),
        19: '③ `p1` 从 ==list2 表头== 出发：现在两个指针==离链表末尾一样远==',
        23: '③ 两个指针并排前进，边走边比较',
        24: _cmp,
        25: lambda S, B, r: f'返回交点 `{r.val}`',
        26: lambda S, B, r: f'`p1` → `{_v(S.p1)}`',
        27: lambda S, B, r: f'`p2` → `{_v(S.p2)}`',
    },
    cards=dict(
        one_liner='先让长链表多走 L1 − L2 步，再两条一起走，相遇处就是交点',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['给你两个链表的头节点 `headA`、`headB`，返回==相交的起始节点==；不相交返回 `null`',
                 '示例：A = `[5,6,1,8,4,5]`，B = `[4,1,8,4,5]`，从 `8` 开始相交',
                 '（官方示例 1 交换 A、B，让 list1 更长，正好对上作者的推导）'],
        quote='设相交后需要从list1走step1步，从list2走step2步，那么一定有 `step1 - step2 = L1 - L2`。于是可以先想办法从list1中走L1 - L2步。',
        quote_src='—— yiduobo 题解',
        idea=['证明：相交后还剩 `k` 个节点，`(step1+k) − (step2+k) = L1 − L2`',
              '①② `p2` 先走完 list2，回 list1 表头；`p1` 走完时 `p2` 已走 `L1−L2` 步',
              '③ `p1` 回 list2 表头，两人离末尾一样远，并排走，相遇即交点'],
        summary=['时间 `O(m+n)`，空间 `O(1)`，不用先算长度',
                 '用 `if not p1` 判断谁先走完，所以哪条更长都能处理',
                 '不相交：第三段两人同时走到 `None`，`return None`',
                 '比较的是==节点本身==：值相同的 `1` 不是交点',
                 '原文为 Python 2 风格：只删掉类型注释文档字符串，其余原样'],
    ),
)
