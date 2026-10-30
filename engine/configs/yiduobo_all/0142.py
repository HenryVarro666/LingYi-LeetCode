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


K, LOOP = 4, 3  # 本例：从 head 走 k = 4 步到入环点（值 5），环长 l = 3（5 → 6 → 7 → 5）
M = 6           # 第一次相遇时 slow 走了 m = 6 步


def _pos(t):
    # 从 head 出发走 t 步后所在的下标
    return t if t < K else K + (t - K) % LOOP


def _idx(S, name):
    # 节点在输入链表中的下标（建表时记录在 tracer._origin 里）
    nd = S.get(name)
    return _tr._origin[nd._uid][1] if nd is not None and nd._uid in _tr._origin else None


def _t1(S):
    # 第一阶段：slow 走了 t 步、fast 走了 2t 步
    i, j = _idx(S, 'slow'), _idx(S, 'fast')
    if i is None or j is None:
        return None
    return next((t for t in range(M + 1) if _pos(t) == i and _pos(2 * t) == j), None)


def _info(S):
    if 'slow' not in S:
        return f'本例：从 head 走 `k = {K}` 步到入环点，环长 `l = {LOOP}`'
    if S.get('_line', 0) < 17:
        t = _t1(S)
        if t is None:
            return ''
        extra = f'，在环里已走 `{t - K}` 步' if t > K else ''
        return f'① `slow` 已走 =={t}== 步{extra}　`fast` 已走 =={2 * t}== 步'
    s = _idx(S, 'fast')
    return (f'② `m = {M}`，`m % l = 0`　`fast` 从 head 已走 =={s}== 步，'
            f'`slow` 在环里共走了 `{M - K} + {s} = {M - K + s}` 步（目标 `m = {M}`）')


def _deco(cv, S, nodes, xy, T):
    inv = {c: u for u, (r, c) in _tr._origin.items()}
    if inv.get(K) in nodes:
        X, Y = xy(inv[K])
        cv.text((X, Y + 66), '入环点', 22, T['yellow'], anchor='mt', bold=True)
    if inv.get(0) in nodes and inv.get(K) in nodes:
        Xa, Y = xy(inv[0])
        Xb, _ = xy(inv[K])
        cv.text(((Xa + Xb) / 2, Y + 66), f'环外 k = {K} 步', 22, T['muted'], anchor='mt')
    last = max(inv)
    if inv.get(last) in nodes and inv.get(K) in nodes:
        Xa, Y = xy(inv[K])
        Xb, _ = xy(inv[last])
        cv.text(((Xa + Xb) / 2, Y + 112), f'环长 l = {LOOP}', 22, T['muted'], anchor='mt')


def _meet(S, B, r):
    if S.fast is S.slow:
        return f'`fast == slow`：在 `{S.slow.val}` 相遇 → 有环。此时 `m = {M}`，`(2m − k) − (m − k) = m` 是 `l` 的倍数'
    i, j = _idx(S, 'slow'), _idx(S, 'fast')
    if i >= K and j >= K:
        return f'`fast` 在 `{S.fast.val}`、`slow` 在 `{S.slow.val}`：都在环里，每次距离缩短 1，还差 {(i - j) % LOOP}'
    return f'`fast` 在 `{S.fast.val}`、`slow` 在 `{S.slow.val}`，还没相遇'


def _back(S, B, r):
    if S.fast is S.slow:
        return f'`fast == slow`：都走了 `k = {K}` 步，在==入环点== `{S.fast.val}` 相遇'
    s = _idx(S, 'fast')
    if s == 0:
        return '`fast != slow` → 两个指针每次==同时走一步=='
    return f'`fast != slow`（已走 {s} 步，还差 {K - s} 步）→ 继续'


def _slow2(S, B, r):
    s = _idx(S, 'fast')
    msg = f'`slow` 在环里走一步 → `{S.slow.val}`'
    if _idx(S, 'slow') == K and s < K:
        msg += f'（==路过入环点==，但 fast 还没到：k > l 时 slow 要多绕圈）'
    return msg


CONFIG = dict(
    num=142, title='环形链表 II', difficulty='Medium', category='链表',
    author='yiduobo', technique='快慢指针 · m % l = 0 推导入环点',
    tags=['labuladong', '灵神突击'],
    code='''
class Solution(object):
    def detectCycle(self, head):

        if not head:
            return None

        fast = slow = head

        while True:
            if not fast or not fast.next:
                return None
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                break

        fast = head

        while fast != slow:
            fast = fast.next
            slow = slow.next

        return fast
''',
    call='Solution().detectCycle(L([1, 2, 3, 4, 5, 6, 7], 4))',
    result_fn=lambda node: node.val,
    expect=5,
    views=[
        dict(type='text', fn=_info, size=26, h=110),
        dict(type='custom', h=480, draw=_ll({'fast': 'pink', 'slow': 'green'},
                                             title='链表：尾节点 7 指回下标 4（入环点是 5）', deco=_deco)),
    ],
    watch=[('fast', 'fast', 'pink'), ('slow', 'slow', 'green')],
    skip=['while True'],
    captions={
        'if not head': '空链表直接返回 None',
        'fast = slow = head': '`fast` 每次走两步，`slow` 每次走一步，都从 head 出发',
        'if not fast or not fast.next': lambda S, B, r: (
            ('`fast` 还能走两步 → 继续（无环的话 fast 会先走到结尾）' if S.slow is S.head else '`fast` 还能走两步 → 继续')
            if S.fast and S.fast.next
            else '`fast` 走到了结尾 → 无环'),
        'fast = fast.next.next': lambda S, B, r: f'`fast` 走两步 → `{S.fast.val}`',
        21: _slow2,
        'slow = slow.next': lambda S, B, r: f'`slow` 走一步 → `{S.slow.val}`',
        'if fast == slow': _meet,
        'break': '相遇，跳出第一个循环；接下来找入环点',
        'fast = head': '`slow` 在环外走了 `k`、环内走了 `m − k`；再走 `k` 步凑满 `m` 步就回到入环点 → 让 `fast` ==回到 head==',
        'while fast != slow': _back,
        'fast = fast.next': lambda S, B, r: f'`fast` 从 head 往后走一步 → `{S.fast.val}`',
        'return fast': lambda S, B, r: f'返回入环点 `{r.val}`',
    },
    cards=dict(
        one_liner='相遇时 slow 走的步数 m 是环长的倍数：fast 回到 head，两人同速再走 k 步就在入环点碰头',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定链表头节点 `head`，返回链表==开始入环的第一个节点==；无环返回 `null`',
                 '`pos` 只用来建环，不作为参数；==不允许修改==链表',
                 '示例：`[3,2,0,-4]`，`pos = 1` → 返回下标 1 的节点',
                 '本视频：`[1..7]`，尾节点连到下标 4 → 返回值为 `5` 的节点'],
        quote='不妨设相遇时fast走了m * 2步，slow走了m步。设入环需要从head往后走k步，环的长度为l，那么就有：((m * 2 - k) - (m - k)) % l = 0 ……化简后可以得到==m % l = 0==',
        quote_src='—— yiduobo 题解',
        idea=['`m*2 − k`、`m − k` 是 fast、slow 在环里的步数；相遇 ⇒ 差是 `l` 的倍数 ⇒ `m % l = 0`',
              '从入环点走 `m` 步一定回到入环点；slow 已在环内走了 `m − k`，==再走 k 步==就回来了',
              '从 head 走 `k` 步也到入环点 → fast 回到 head，两人同速走，相遇处就是答案'],
        result='返回入环点 `5`：fast 走了 4 步，slow 在环里绕了一圈多',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`k` 可能比环长大：第二段里 slow 会多次经过入环点（本例 k = 4 > l = 3）',
                 '`fast == slow` 比较的是同一个节点对象，不是值',
                 '141 只需第一个 `while`：`return None` 是无环，`break` 是有环',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动'],
    ),
)
