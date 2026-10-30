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
    if 'dummy' not in S:
        return '把位置 ==left = 2 到 right = 4== 的节点（2,3,4）反转'
    if S['_line'] in (15, 16, 17):
        return f"拼接：从 dummy 出发 = =={_chain(S['dummy'].next)}=="
    if 'pre' in S:
        cur, pre = S.get('cur'), S.get('pre')
        rest = S['nxt'] if cur is not None and 'nxt' in S and (cur.next is pre or cur is pre) else cur
        return f"`pre` 链（已反转）= =={_chain(pre)}==　　还没处理：{_chain(rest)}"
    return '先让 `p0` 走到位置 `left` 的==上一个==节点'


def _loop1(S, B, r):
    if '_' in S and S['_'] != B.get('_'):
        return f'`p0` 往右走第 `{S["_"] + 1}` 步（共 `left - 1 = {S.left - 1}` 步）'
    return f'`p0` 停在 `{S.p0.val}`：反转区间的==上一个==节点'


def _loop2(S, B, r):
    k = S.right - S.left + 1
    if 'nxt' not in B or S.get('_') != B.get('_'):
        return f'区间共 `right - left + 1 = {k}` 个节点，处理第 `{S["_"] + 1}` 个：`cur = {_v(S.cur)}`'
    return f'{k} 个节点反转完：==pre = {_v(S.pre)} 是区间新头，cur = {_v(S.cur)} 是区间后一个=='


CONFIG = dict(
    num=92, title='反转链表 II', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='哨兵节点 + 206 反转 + 两次拼接',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        p0 = dummy = ListNode(next=head)
        # 把 p0 移到 left 的上一个节点
        for _ in range(left - 1):
            p0 = p0.next
        pre = None
        cur = p0.next
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = pre  # 每次循环只修改一个 next，方便大家理解
            pre = cur
            cur = nxt
        # 见视频
        p0.next.next = cur
        p0.next = pre
        return dummy.next
''',
    # setup 只做布局：把运行中创建的第一个节点（dummy）放在第 0 行最左边，原链表整体右移一格
    setup="""
import tracer, itertools
head = L([1, 2, 3, 4, 5])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
""",
    call='Solution().reverseBetween(head, 2, 4)',
    expect=[1, 4, 3, 2, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=500, draw=_ll({'p0': 'purple', 'dummy': 'cyan', 'pre': 'pink', 'cur': 'blue', 'nxt': 'green'},
                                             title='链表（黄色箭头 = 这一步刚改的 next）')),
    ],
    watch=[('p0', 'p0', 'purple'), ('pre', 'pre', 'pink'), ('cur', 'cur', 'blue'), ('nxt', 'nxt', 'green')],
    captions={
        'p0 = dummy = ListNode': '建==哨兵节点== `dummy` 指向 head：left = 1 时 `p0` 也有上一个节点可停',
        'for _ in range(left - 1)': _loop1,
        'p0 = p0.next': lambda S, B, r: f'`p0` 右移到 `{S.p0.val}`',
        'pre = None': '和 206 题一样反转：`pre = None` 是已反转部分的头',
        'cur = p0.next': '`cur = p0.next = {cur.val}`：区间第一个节点，反转后它会变成区间的==末尾==',
        'for _ in range(right - left + 1)': _loop2,
        'nxt = cur.next': lambda S, B, r: f'先记住 `nxt = {_v(S.nxt)}`：下一步要改 `cur.next`，不记就丢了',
        'cur.next = pre': lambda S, B, r: (f'`{S.cur.val}.next = None`：区间头暂时指向空（==最后再接回去==）' if S.pre is None
                                           else f'`{S.cur.val}.next` 改指 `pre`（{S.pre.val}）：头插到已反转部分'),
        'pre = cur': lambda S, B, r: f'`pre` → `{S.pre.val}`，已反转：=={_chain(S.pre)}==',
        'cur = nxt': lambda S, B, r: f'`cur` → `{_v(S.cur)}`',
        'p0.next.next = cur': lambda S, B, r: (f'`p0.next` 还是原来的区间头 `{S.p0.next.val}`（现在是区间末尾）'
                                               f'→ 让它指向 `cur = {_v(S.cur)}`，==接上右半段=='),
        'p0.next = pre': lambda S, B, r: f'`p0`（{S.p0.val}）指向 `pre = {S.pre.val}`：==接上反转后的区间头==',
        'return dummy.next': lambda S, B, r: f'返回 `dummy.next` → =={_chain(r)}==（不能返回 head：left = 1 时头会变）',
    },
    cards=dict(
        result='返回 `[1,4,3,2,5]` ✓ 与示例答案一致',
        one_liner='p0 停在区间前一个节点，206 反转区间，再把两头接回去',
        complexity='时间 `O(right)`，空间 `O(1)`',
        problem=['单链表 `head`，反转==位置== `left` 到 `right` 的节点（从 1 开始数），返回反转后的链表',
                 '示例：`head = [1,2,3,4,5], left = 2, right = 4` → `[1,4,3,2,5]`',
                 '进阶：一趟扫描完成'],
        quote='⚠注意：left 和 right 是==位置范围==，不是元素值的范围。',
        quote_src='—— 灵茶山艾府题解（详见【基础算法精讲 06】）',
        idea=['区间内照搬 206：循环 `right - left + 1` 次，结束时 ==pre 是区间新头，cur 是区间后一个==',
              '`p0` 是区间前一个节点；`p0.next` 仍指向原区间头（现在是区间末尾）',
              '先 `p0.next.next = cur` 接右边，再 `p0.next = pre` 接左边；==dummy== 处理 left = 1'],
        summary=['时间 `O(right)`，空间 `O(1)`，一趟扫描',
                 '两句拼接==顺序不能反==：先改 `p0.next` 就找不到原区间头了',
                 '哨兵 `dummy`：left = 1 时区间前面也有节点，最后返回 `dummy.next`',
                 '同类：206 反转链表、25 K 个一组翻转链表（循环调用本题的反转）'],
    ),
)
