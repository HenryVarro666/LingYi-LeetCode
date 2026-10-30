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


def _ans(S):
    d = S.get('dummy')
    vals = list_vals(d.next) if d is not None else []
    return '[' + ','.join(map(str, vals)) + ']'


def _deco(cv, S, nodes, xy, T):
    inv = {(r, c): u for u, (r, c) in _tr._origin.items()}
    for (r, c), lab in (((0, 1), 'l1'), ((1, 1), 'l2')):
        u = inv.get((r, c))
        if u in nodes:
            X, Y = xy(u)
            cv.text((X - 52, Y), lab, 24, T['muted'], anchor='rm', bold=True)


CONFIG = dict(
    num=2, title='两数相加', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='哨兵节点 + 逐位相加（迭代）',
    code='''
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 哨兵节点
        carry = 0  # 进位值
        while l1 or l2 or carry:  # 有一个不是空节点，或者还有进位，就继续迭代
            s = carry
            if l1:
                s += l1.val  # 节点值和进位加在一起
                l1 = l1.next  # 下一个节点
            if l2:
                s += l2.val  # 节点值和进位加在一起
                l2 = l2.next  # 下一个节点
            cur.next = ListNode(s % 10)  # 每个节点保存一个数位
            carry = s // 10  # 新的进位
            cur = cur.next  # 下一个节点
        return dummy.next  # 哨兵节点的下一个节点就是头节点
''',
    setup='''
import tracer
a, b = L([2, 4, 3]), L([5, 6, 4])
for nd in tracer.Lnodes(a) + tracer.Lnodes(b):
    r, c = tracer._origin[nd._uid]
    tracer._origin[nd._uid] = (r, c + 1)
''',
    call='Solution().addTwoNumbers(a, b)',
    expect=[7, 0, 8],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: f'`342 + 465 = 807`：逆序存放，表头就是个位　　答案：=={_ans(S)}==' if 'dummy' in S else
             '`342 + 465 = 807`：逆序存放，表头就是个位', size=26),
        dict(type='custom', h=520, draw=_ll({'cur': 'yellow', 'l1': 'blue', 'l2': 'pink', 'dummy': 'purple'},
                                             title='上两行：l1、l2（同一列是同一位）　最下行：答案（最左是哨兵）', deco=_deco)),
    ],
    watch=[('carry', 'carry', 'orange'), ('s', 's', 'green')],
    captions={
        'cur = dummy = ListNode()': '创建==哨兵节点== `dummy` 当成初始的「空链表」；`cur` 指向答案的末尾',
        'carry = 0': '进位值 `carry = 0`',
        'while l1 or l2 or carry': lambda S, B, r: (
            ('有一个不是空节点，或者还有进位 → 继续' if (S.l1 or S.l2) else '两个链表都空了，但==还有进位== → 继续')
            if (S.l1 or S.l2 or S.carry) else '两个链表都空了，也没有进位 → 结束'),
        's = carry': lambda S, B, r: f'`s` 先等于上一位的进位 `{S.carry}`',
        'if l1:': lambda S, B, r: f'`l1` 不为空（{S.l1.val}）→ 加上它' if S.l1 else '`l1` 已经空了 → 跳过（相当于加 0）',
        's += l1.val': lambda S, B, r: f'`s += {B.l1.val}` → `s = {S.s}`',
        'l1 = l1.next': lambda S, B, r: f'`l1` 走到下一个节点 → `{_v(S.l1)}`',
        'if l2:': lambda S, B, r: f'`l2` 不为空（{S.l2.val}）→ 加上它' if S.l2 else '`l2` 已经空了 → 跳过（相当于加 0）',
        's += l2.val': lambda S, B, r: f'`s += {B.l2.val}` → `s = {S.s}`',
        'l2 = l2.next': lambda S, B, r: f'`l2` 走到下一个节点 → `{_v(S.l2)}`',
        'cur.next = ListNode': lambda S, B, r: f'每个节点保存一个数位：`s % 10 = {S.s % 10}`，新建节点接到答案末尾',
        'carry = s // 10': lambda S, B, r: f'新的进位：`s // 10 = {S.carry}`' + ('（==产生进位==，下一位要多加 1）' if S.carry else ''),
        'cur = cur.next': lambda S, B, r: f'`cur` 移到答案的末尾 `{S.cur.val}`',
        'return dummy.next': lambda S, B, r: f'哨兵的下一个节点就是头节点 → ==[{",".join(map(str, list_vals(r)))}]==',
    },
    cards=dict(
        one_liner='哨兵节点当空链表，逐位相加：有节点或还有进位就继续',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['两个==非空==链表表示两个非负整数，数字==逆序==存储，每个节点存一位',
                 '把两数相加，以同样的形式返回和的链表',
                 '示例：`[2,4,3]` + `[5,6,4]` → `[7,0,8]`，即 342 + 465 = 807'],
        quote='在第一次循环时，我们无法往一个空节点的末尾添加节点。这里的技巧是，创建一个==哨兵节点==（dummy node），当成初始的「空链表」。',
        quote_src='—— 灵茶山艾府题解（方法二：迭代）',
        idea=['每次把 `l1.val`、`l2.val` 与进位 `carry` 相加得到 `s`',
              '`s % 10` 是当前节点要保存的数位，`s // 10` 是新的进位',
              '循环条件 `l1 or l2 or carry`：有一个不是空节点，==或者还有进位==，就继续'],
        summary=['时间 `O(n)`（n 为较长链表的长度），空间 `O(1)`（不计答案）',
                 '别漏最高位的进位：`[9,9] + [1]` 结果要多出一位 `1`',
                 '最后返回 `dummy.next`，不是 `dummy`',
                 '灵神还给了递归写法：把剩下的计算看成规模更小的子问题'],
    ),
)
