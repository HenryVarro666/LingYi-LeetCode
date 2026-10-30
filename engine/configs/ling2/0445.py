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


def _ll(ptrs, title='链表', place=None, deco=None, inner=False):
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
            v = (S.get('_inner') or {}).get(name) if inner else S.get(name)
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
        PS = (S.get('_inner') or {}) if inner else S
        nones = [n for n in ptrs if n in PS and PS[n] is None]
        if nones:
            cv.text((x1 - 20, y0 + 6), '  '.join(f'{n}=None' for n in nones), 20, T['muted'], anchor='ra', mono=True)
    return draw


def _chain(node, limit=8):
    out, seen = [], set()
    while node is not None and node._uid not in seen and len(out) < limit:
        seen.add(node._uid)
        out.append(str(node.val))
        node = node.next
    return ' → '.join(out) if out else '空'


def _row(node):
    if node is None:
        return None
    return _tr._origin.get(node._uid, (9, 0))[0]


def _phase(S):
    ln = S.get('_line', 0)
    I = S.get('_inner') or {}
    if 3 <= ln <= 11:
        r = _row(I.get('head'))
        return {0: 1, 1: 2}.get(r, 4)
    if 13 <= ln <= 24:
        return 3
    return {27: 1, 28: 2, 29: 3, 30: 4}.get(ln, 0)


PH = {1: '①反转 l1', 2: '②反转 l2', 3: '③两数相加', 4: '④反转结果'}


def _head(S):
    p = _phase(S)
    steps = '　'.join((f'=={PH[k]}==' if k == p else PH[k]) for k in (1, 2, 3, 4))
    return '`243+564`　' + steps


def _v(x):
    return 'None' if x is None else str(x.val)


def _cap_while_rev(S, B, ret):
    if B.cur is not None:
        return f'`cur = {B.cur.val}` 不为空 → 继续头插'
    return f'`cur` 为空：反转完成，新头是 `{_v(S.pre)}`'


def _cap_rev_next(S, B, ret):
    return (f'头插：`{S.cur.val}.next` 指向 `{_v(S.pre)}`，然后 `pre`、`cur` 各前进一步'
            if B.pre is None and _row(S.cur) == 0 else f'`{S.cur.val}.next = {_v(S.pre)}`')


CONFIG = dict(
    num=445, title='两数相加 II', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='反转链表 + 两数相加（迭代）',
    tags=['热题173'],
    code='''
class Solution:
    # 视频讲解 https://www.bilibili.com/video/BV1sd4y1x7KN/
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre

    def addTwo(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 哨兵节点
        carry = 0  # 进位
        while l1 or l2 or carry:  # 有一个不是空节点，或者还有进位，就继续迭代
            if l1: carry += l1.val  # 节点值和进位加在一起
            if l2: carry += l2.val  # 节点值和进位加在一起
            cur.next = ListNode(carry % 10)  # 每个节点保存一个数位
            carry //= 10  # 新的进位
            cur = cur.next  # 下一个节点
            if l1: l1 = l1.next  # 下一个节点
            if l2: l2 = l2.next  # 下一个节点
        return dummy.next  # 哨兵节点的下一个节点就是头节点

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        l1 = self.reverseList(l1)
        l2 = self.reverseList(l2)  # l1 和 l2 反转后，就变成【2. 两数相加】了
        l3 = self.addTwo(l1, l2)
        return self.reverseList(l3)  # 计算完毕后再反转
''',
    setup='''
import tracer
a, b = L([2, 4, 3]), L([5, 6, 4])
''',
    call='Solution().addTwoNumbers(a, b)',
    expect=[8, 0, 7],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_head, size=24),
        dict(type='custom', h=540, draw=_ll({'pre': 'pink', 'cur': 'blue', 'nxt': 'green', 'head': 'orange',
                                              'l1': 'cyan', 'l2': 'yellow', 'dummy': 'purple', 'l3': 'orange'},
                                             title='第 1 行：l1　第 2 行：l2　第 3 行：新建的和（最左是哨兵）', inner=True)),
    ],
    watch=[('carry', lambda S: S['_inner'].get('carry'), 'orange')],
    skip=['nxt = cur.next', '            pre = cur', 'cur = nxt'],
    captions={
        'l1 = self.reverseList(l1)': '第一步：反转 `l1`，把==个位换到表头==',
        'l2 = self.reverseList(l2)': '第二步：反转 `l2`',
        'l3 = self.addTwo(l1, l2)': 'l1 和 l2 反转后，==就变成【2. 两数相加】了==',
        'return self.reverseList(l3)': '计算完毕后再反转：高位回到表头',
        'pre = None': lambda S, B, ret: f'反转 `{_chain(S.head)}`：`pre = None` 是新链表的头',
        'cur = head': '`cur` 指向第一个还没反转的节点 `{cur.val}`',
        'while cur:': _cap_while_rev,
        'cur.next = pre': _cap_rev_next,
        'return pre': lambda S, B, ret: f'返回新头 `{_v(ret)}`：=={_chain(ret)}==',
        'cur = dummy = ListNode()': '创建==哨兵节点== `dummy`，`cur` 指向答案的末尾',
        'carry = 0': '进位 `carry = 0`',
        'while l1 or l2 or carry': lambda S, B, ret: (
            '有一个不是空节点，或者还有进位 → 继续' if (B.l1 or B.l2 or B.carry) else '都空了，也没有进位 → 结束'),
        'if l1: carry += l1.val': lambda S, B, ret: (f'`carry += {B.l1.val}` → `{S.carry}`' if B.l1 else '`l1` 为空，跳过'),
        'if l2: carry += l2.val': lambda S, B, ret: (f'`carry += {B.l2.val}` → `{S.carry}`' if B.l2 else '`l2` 为空，跳过'),
        'cur.next = ListNode(carry % 10)': '每个节点保存一个数位：`{carry} % 10 = {carry % 10}`',
        'carry //= 10': lambda S, B, ret: f'新的进位 `{B.carry} // 10 = {S.carry}`' + ('（==进位==）' if S.carry else ''),
        'cur = cur.next  # 下一个': '`cur` 移到新节点 `{cur.val}`',
        'if l1: l1 = l1.next': lambda S, B, ret: f'`l1` → `{_v(S.l1)}`',
        'if l2: l2 = l2.next': lambda S, B, ret: f'`l2` → `{_v(S.l2)}`',
        'return dummy.next': lambda S, B, ret: f'哨兵的下一个就是头：=={_chain(ret)}==（个位在前）',
    },
    max_steps=70,
    cards=dict(
        one_liner='反转两条链表，套用第 2 题，再把结果反转回来',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['两个==非空==链表表示两个非负整数，==最高位在表头==，每个节点存一位',
                 '把两数相加，以同样的形式返回和的链表',
                 '示例：`[7,2,4,3] + [5,6,4]` → `[7,8,0,7]`；本视频 `[2,4,3] + [5,6,4]` → `[8,0,7]`'],
        quote='1. 反转链表 l1。2. 反转链表 l2。3. 调用 ==2. 两数相加== 的代码，得到链表 l3。4. 反转链表 l3，返回 l3 作为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['加法要从个位开始，而个位在表尾 → ==先反转==，个位就到了表头',
              '反转用 206 题的头插法，相加用第 2 题的哨兵 + 进位',
              '算出来的和是个位在前，==再反转一次==就是答案'],
        result='运行结束：返回 `[8,0,7]`，即 243 + 564 = 807 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '“反转 + 两数相加”两个模板拼起来就秒杀',
                 '易错：循环条件带上 `carry`，否则 `[5] + [5]` 会丢掉最高位的 1',
                 '方法一是递归写法（空间 `O(n)`）；进阶不许反转时可以用栈'],
    ),
)
