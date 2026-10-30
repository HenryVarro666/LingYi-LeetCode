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


def _chain(node, limit=8):
    vals = list_vals(node)[:limit]
    return ' → '.join(map(str, vals)) if vals else '空'


def _info(S):
    if 'new_head' not in S:
        return '把第 ==m = 1 到 n = 3== 个节点（1,2,3）反转；==m = 1==：头节点也要动'
    if S['_line'] in (22, 23, 25):
        return f"拼接后从假头出发：=={_chain(S['new_head'].next)}=="
    if 'reverse_head' in S and 'left_tail' in S and S['_line'] >= 13:
        return f"`left_tail = {_v(S['left_tail'])}`（P(m-1)）　`reverse_head`：已翻转部分的头"
    return '先走到 P(m-1)：翻转后它要接到新的区间头上'


def _loop2(S, B, r):
    k = S.n - S.m
    if 'next_node' not in B or S.get('index') != B.get('index'):
        return f'还要翻转 `n - m = {k}` 条 next：第 `{S["index"] + 1}` 条，`now = {_v(S.now)}`'
    return f'`{k}` 条 next 都反转完：`reverse_head = {_v(S.reverse_head)}` 是 Pn，`now = {_v(S.now)}` 是 P(n+1)'


def _flip(S, B, r):
    msg = f'`{S.now.val}.next` 反过来指向 `{S.reverse_head.val}`'
    if S.reverse_head.next is S.now:
        msg += f'：此时 `{S.reverse_head.val}` 和 `{S.now.val}` ==互相指向==（Pm 的 next 还没改，最后再修正）'
    return msg


CONFIG = dict(
    num=92, title='反转链表 II', difficulty='Medium', category='链表',
    author='yiduobo', technique='假头节点 · 一趟扫描逐个反转 next',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def reverseBetween(self, head, m, n):
        if m == n:
            return head

        new_head = ListNode(0)
        new_head.next = head
        now = new_head
        for index in range(m - 1):
            now = now.next
        left_tail = now
        now = now.next
        reverse_head = now
        now = now.next

        for index in range(n - m):
            next_node = now.next
            now.next = reverse_head
            reverse_head = now
            now = next_node

        left_tail.next.next = now
        left_tail.next = reverse_head

        return new_head.next
''',
    # setup 只做布局：把运行中创建的第一个节点（假头 new_head）放在第 0 行最左边，原链表整体右移一格
    setup="""
import tracer, itertools
head = L([1, 2, 3, 4, 5])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
""",
    call='Solution().reverseBetween(head, 1, 3)',
    expect=[3, 2, 1, 4, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=500, draw=_ll({'new_head': 'cyan', 'left_tail': 'purple', 'reverse_head': 'pink',
                                              'now': 'blue', 'next_node': 'green'},
                                             title='链表（黄色箭头 = 这一步刚改的 next）')),
    ],
    watch=[('left_tail', 'left_tail', 'purple'), ('reverse_head', 'reverse_head', 'pink'), ('now', 'now', 'blue'),
           ('next_node', 'next_node', 'green')],
    captions={
        'if m == n': lambda S, B, r: ('`m == n`：只翻转一个节点，无事发生' if S.m == S.n else
                                      f'`m = {S.m} ≠ n = {S.n}`：需要翻转'),
        'new_head = ListNode(0)': '加一个==假头节点==：覆盖住 `m = 1` 的特殊情况（P(m-1) 不存在）',
        'new_head.next = head': '假头接在 head 前面',
        'now = new_head': '`now` 从假头出发，往后走 `m - 1` 步',
        'for index in range(m - 1)': lambda S, B, r: (
            f'走第 `{S.index + 1}` 步' if 'index' in S and S.index != B.get('index') else
            f'`m - 1 = {S.m - 1}` 步走完：`now` 停在 ==P(m-1) = {_v(S.now)}==' + ('（就是假头）' if S.m == 1 else '')),
        10: '`now` → `{now.val}`',
        'left_tail = now': '记下 `left_tail` = P(m-1)：==翻转后的区间要接在它后面==',
        12: '`now` 前进到 Pm = `{now.val}`',
        13: '`reverse_head = {reverse_head.val}`：`now` ==原始的上一个节点==（已翻转部分的头）',
        14: '`now` 前进到 P(m+1) = `{now.val}`：接下来要把它的 next 反过来',
        'for index in range(n - m)': _loop2,
        'next_node = now.next': lambda S, B, r: f'先记下 `next_node = {_v(S.next_node)}`：反转 next 后就==丢失原始的 next== 了',
        'now.next = reverse_head': _flip,
        19: '`reverse_head` → `{reverse_head.val}`',
        'now = next_node': lambda S, B, r: f'`now` → `{_v(S.now)}`',
        'left_tail.next.next = now': lambda S, B, r: (f'`left_tail.next` 仍是 Pm（`{S.left_tail.next.val}`）'
                                                      f'→ 让它指向 P(n+1) = `{_v(S.now)}`，==拆掉互相指向=='),
        'left_tail.next = reverse_head': '`left_tail`（{left_tail.val}）指向 Pn = `{reverse_head.val}`：区间接回来',
        'return new_head.next': lambda S, B, r: f'返回 `new_head.next` → =={_chain(r)}==：==头节点已经变了==',
    },
    cards=dict(
        one_liner='走到 P(m-1)，边扫描边反转 next，最后两次拼接',
        complexity='时间 `O(n)`，空间 `O(1)`，一趟扫描',
        problem=['单链表 `head`，反转从==位置== `m` 到 `n` 的节点（从 1 开始数），返回反转后的链表',
                 '示例：`[1,2,3,4,5], m = 2, n = 4` → `[1,4,3,2,5]`',
                 '本视频：`m = 1, n = 3` → `[3,2,1,4,5]`（头节点也被反转）'],
        quote='此时Pm-1的next任然是Pm，于是只需要==将Pm的next指向Pn+1==，即Pm-1.next.next = Pn+1，然后再将Pm-1的next指向Pn即可。',
        quote_src='—— yiduobo 题解',
        idea=['翻转后：`P(m-1) → Pn → … → Pm → P(n+1)`',
              '假头节点让 `m = 1` 时也有 P(m-1)；`reverse_head` 记 now 原始的上一个节点',
              '先记下 `next_node` 再反转 next，否则丢失下一个要处理的节点'],
        result='返回 `[3,2,1,4,5]` ✓（m = 1，靠假头节点处理）',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环 `n - m` 次反转 `n - m` 条边；Pm 的 next 留到最后修正（中途和 P(m+1) 互指）',
                 '`left_tail.next.next = now` 必须在 `left_tail.next = reverse_head` ==之前==',
                 '对比灵神：灵神循环 `right - left + 1` 次，从 `pre = None` 开始，区间头先指向空',
                 '原文为 Python 2 风格：删去 docstring 和节点定义注释，代码未改'],
    ),
)
