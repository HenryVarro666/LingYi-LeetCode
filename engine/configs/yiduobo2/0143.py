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
    ln = S['_line']
    if ln >= 27:
        return f"③ 合并：从 head 出发 = =={_chain(S['head'])}=="
    if ln >= 17:
        return f"② 翻转后半段：`pre` = =={_chain(S.get('pre'))}=="
    if ln >= 9:
        return '① 快慢指针==从假头 p_head 出发==：`slow` 走 1 步，`fast` 走 2 步'
    return '① 找后半段　② 翻转后半段　③ 前后两半交替合并'


def _split_cap(S, B, ret):
    if B.fast.next:
        return f'`fast.next` 存在 → ==链表长度为奇数==，最中间的节点划在前半部分 → `slow` 要再后移一位'
    return '`fast.next` 为空 → 长度为偶数，`slow` 就是前半部分的末尾'


CONFIG = dict(
    num=143, title='重排链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='快慢指针（假头）+ 翻转 + 合并',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def reorderList(self, head):
        if not head or not head.next:
            return

        p_head = ListNode()
        p_head.next = head

        fast = slow = p_head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        if fast.next:
            slow = slow.next

        pre = slow.next
        now = pre.next
        while now:
            tmp = now.next
            now.next = pre
            pre = now
            now = tmp
        slow.next.next = None
        slow.next = None

        now = head
        while pre:
            next1 = now.next
            now.next = pre
            next2 = pre.next
            pre.next = next1
            now = next1
            pre = next2
''',
    # setup 只做布局：把运行中创建的第一个节点（假头 p_head）放在第 0 行最左边，原链表整体右移一格
    setup="""
import tracer, itertools
h = L([1, 2, 3, 4, 5])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
""",
    call='''Solution().reorderList(h)
list_vals(h)''',
    expect=[1, 5, 2, 4, 3],
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=520, draw=_ll({'head': 'orange', 'p_head': 'cyan', 'slow': 'blue', 'fast': 'pink',
                                              'pre': 'purple', 'now': 'green', 'tmp': 'yellow', 'next1': 'yellow',
                                              'next2': 'red'},
                                             title='链表（黄色箭头 = 这一步刚改的 next）')),
    ],
    watch=[('slow', 'slow', 'blue'), ('fast', 'fast', 'pink'), ('pre', 'pre', 'purple'), ('now', 'now', 'green'),
           ('next1', 'next1', 'yellow'), ('next2', 'next2', 'red')],
    captions={
        'if not head or not head.next': '空链表或只有一个节点 → 不用动；这里有 `5` 个节点，继续',
        'p_head = ListNode()': '快慢指针需要先设置==假头 p_head==，才能正确定位前后两半的分界点',
        'p_head.next = head': '假头接在 head 前面',
        'fast = slow = p_head': '`fast` 与 `slow` 同时从 `p_head` 开始往后走',
        'while fast.next and fast.next.next': lambda S, B, r: (
            '`fast` 还能走两步 → 继续' if S.fast.next and S.fast.next.next else
            f'`fast` 走不了两步了：`slow = {_v(S.slow)}`，`fast = {_v(S.fast)}`'),
        11: lambda S, B, r: f'`slow` 走 1 步 → `{_v(S.slow)}`',
        'fast = fast.next.next': lambda S, B, r: f'`fast` 走 2 步 → `{_v(S.fast)}`',
        'if fast.next': _split_cap,
        15: '`slow = {slow.val}`：前半部分到它为止',
        'pre = slow.next': '后半部分从 `slow.next = {pre.val}` 开始翻转：`pre = {pre.val}`',
        'now = pre.next': '`now = pre.next = {now.val}`：从后半部分的第 2 个节点开始反转 next',
        'while now:': lambda S, B, r: ('`now` 不为空 → 继续翻转' if S.now else '`now` 为空 → 翻转完成，`pre` 是原链表的末尾'),
        'tmp = now.next': lambda S, B, r: f'先存 `tmp = {_v(S.tmp)}`',
        21: lambda S, B, r: f'`{S.now.val}.next` 反过来指向 `{S.pre.val}`',
        22: '`pre` → `{pre.val}`',
        23: lambda S, B, r: f'`now` → `{_v(S.now)}`',
        'slow.next.next = None': lambda S, B, r: (f'后半部分原来的头 `{S.slow.next.val}` 现在是末尾，'
                                                  f'它的 next 还指着 `{_v(B.slow.next.next)}`（==互相指向==）→ 断开'),
        'slow.next = None': '`slow.next = None`：==把前后两半彻底断开==',
        'now = head': lambda S, B, r: f'③ 合并：`now` 从 `head` 出发；后半部分从 `pre = {S.pre.val}` 出发',
        'while pre:': lambda S, B, r: ('`pre` 不为空 → 继续合并' if S.pre else '`pre` 为空 → 后半部分接完了，结束'),
        'next1 = now.next': lambda S, B, r: f'存前半部分的下一个 `next1 = {_v(S.next1)}`',
        30: lambda S, B, r: f'`{S.now.val}.next` → `{S.pre.val}`：前半部分的节点后接一个后半部分的节点',
        'next2 = pre.next': lambda S, B, r: f'存后半部分的下一个 `next2 = {_v(S.next2)}`',
        'pre.next = next1': lambda S, B, r: f'`{S.pre.val}.next` → `{_v(S.next1)}`：再接回前半部分',
        'now = next1': lambda S, B, r: f'`now` → `{_v(S.now)}`',
        'pre = next2': lambda S, B, r: f'`pre` → `{_v(S.pre)}`',
    },
    cards=dict(
        one_liner='链表题中的缝合怪：找后半段、翻转、合并',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['单链表 `L0 → L1 → … → Ln` 重排为 `L0 → Ln → L1 → Ln-1 → L2 → …`',
                 '==不能只改节点的值==，要实际交换节点',
                 '示例：`[1,2,3,4,5]` → `[1,5,2,4,3]`'],
        quote='快慢指针需要先设置假头p_head，然后fast与slow同时从p_head开始往后走……当链表长度为奇数时，==最中间的节点是划在前半部分的==，因此要将此时的slow往后移动一位。',
        quote_src='—— yiduobo 题解',
        idea=['三段 while：==找后半段、翻转、合并==',
              '从假头出发，`slow` 停在前半部分末尾（奇数时再后移一位）',
              '翻转后半部分后==把两半彻底断开==，再交替合并直到后半部分用完'],
        result='重排为 `[1,5,2,4,3]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`；原地修改，没有返回值',
                 '翻转后要 `slow.next.next = None` 和 `slow.next = None`，否则会成环',
                 '原文还提到 dfs 解法：递归到末尾，回溯时把 head 与 tail 接到答案后面',
                 '对比灵神：灵神不断开两半，靠 `while head2.next` 停在共享的中间节点',
                 '原文为 Python 2 风格：删去 docstring 和节点定义注释，代码未改'],
    ),
)
