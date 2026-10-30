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


def _merged(S):
    # 新链表中已经确定的部分：从 dummy.next 走到 cur 为止
    d, cur = S.get('dummy'), S.get('cur')
    out, x = [], getattr(d, 'next', None)
    while x is not None and len(out) < 12:
        out.append(str(x.val))
        if x is cur:
            break
        x = x.next
    return ' → '.join(out) if out else '空'


CONFIG = dict(
    num=21, title='合并两个有序链表', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='哨兵节点 + 迭代尾插',
    code='''
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 用哨兵节点简化代码逻辑
        while list1 and list2:
            if list1.val < list2.val:
                cur.next = list1  # 把 list1 加到新链表中
                list1 = list1.next
            else:  # 注：相等的情况加哪个节点都是可以的
                cur.next = list2  # 把 list2 加到新链表中
                list2 = list2.next
            cur = cur.next
        cur.next = list1 or list2  # 拼接剩余链表
        return dummy.next
''',
    setup='''
import tracer
a, b = L([1, 2, 4]), L([1, 3, 4])
for i, nd in enumerate(tracer.Lnodes(a)): tracer._origin[nd._uid] = (0, i + 1)
for i, nd in enumerate(tracer.Lnodes(b)): tracer._origin[nd._uid] = (2, i + 1)
''',
    call='Solution().mergeTwoLists(a, b)',
    expect=[1, 1, 2, 3, 4, 4],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: f"已合并：=={_merged(S)}==　（`cur` 是新链表的末尾）" if 'dummy' in S else '', size=26),
        dict(type='custom', h=520, draw=_ll({'cur': 'yellow', 'list1': 'blue', 'list2': 'pink', 'dummy': 'purple'},
                                             title='上：list1　下：list2　左：哨兵 dummy', place=lambda k, base: (1, 0))),
    ],
    watch=[('list1', 'list1', 'blue'), ('list2', 'list2', 'pink'), ('cur', 'cur', 'yellow')],
    captions={
        'cur = dummy = ListNode()': '创建==哨兵节点== `dummy`（新链表头节点的前一个节点），`cur` 指向新链表的末尾',
        'while list1 and list2': lambda S, B, r: ('两个链表都还有节点 → 比较当前节点' if S.list1 and S.list2 else
                                                  f'`{"list1" if S.list1 is None else "list2"}` 空了 → 结束循环'),
        'if list1.val < list2.val': lambda S, B, r: (f'`{S.list1.val} < {S.list2.val}` → list1 的更小，取 list1'
                                                     if S.list1.val < S.list2.val else
                                                     f'`{S.list1.val} < {S.list2.val}` 不成立 → 取 list2'
                                                     + ('（==相等时加哪个节点都可以==）' if S.list1.val == S.list2.val else '')),
        'cur.next = list1  #': lambda S, B, r: f'把 list1 的节点 `{S.cur.next.val}` 接到新链表末尾（尾插）' + (
            '：它本来就接在 `cur` 后面，指针不变' if B.cur.next is not None and B.cur.next._uid == S.cur.next._uid else ''),
        'list1 = list1.next': lambda S, B, r: f'`list1` 后移 → `{_v(S.list1)}`',
        'cur.next = list2  #': lambda S, B, r: f'把 list2 的节点 `{S.cur.next.val}` 接到新链表末尾（尾插）' + (
            '：它本来就接在 `cur` 后面，指针不变' if B.cur.next is not None and B.cur.next._uid == S.cur.next._uid else ''),
        'list2 = list2.next': lambda S, B, r: f'`list2` 后移 → `{_v(S.list2)}`',
        'cur = cur.next': lambda S, B, r: f'`cur` 移到新链表的末尾 `{S.cur.val}`',
        'cur.next = list1 or list2': lambda S, B, r: f'拼接剩余链表：`list1 or list2` 就是没空的那条，直接接上 `{_v(S.cur.next)}`',
        'return dummy.next': lambda S, B, r: '返回 `dummy.next`（哨兵的下一个才是真正的头）→ ==' + ' → '.join(map(str, list_vals(r))) + '==',
    },
    cards=dict(
        one_liner='用哨兵节点当新链表的头，每次把较小的节点尾插到新链表末尾',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['将两个==升序==链表合并为一个新的升序链表并返回',
                 '新链表由两个链表的所有节点拼接而成',
                 '示例：`[1,2,4]` 和 `[1,3,4]` → `[1,1,2,3,4,4]`'],
        quote='创建一个哨兵节点，作为合并后的新链表头节点的前一个节点。这样可以==避免单独处理头节点==，也无需特判链表为空的情况，从而简化代码。',
        quote_src='—— 灵茶山艾府题解（方法一：迭代）',
        idea=['比较两个链表的当前节点，==较小的接到新链表末尾==，然后后移',
              '两个节点值一样时，加谁都一样，不妨规定加 `list2`',
              '循环结束后，其中一个链表可能还有剩余，整段接到末尾'],
        summary=['时间 `O(n+m)`，空间 `O(1)`：只改指针，不新建节点（除了哨兵）',
                 '返回 `dummy.next`，不是 `dummy`',
                 '`cur.next = list1 or list2`：剩下的本身有序，整段接上即可',
                 '灵神的另一种写法：递归（头插法），空间 `O(n+m)`'],
    ),
)
