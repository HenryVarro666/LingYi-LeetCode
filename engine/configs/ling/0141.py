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


def _gap(S):
    # 两人都在环里时，兔子还要追几步才能追上乌龟：(乌龟位置 − 兔子位置) mod 环长
    nodes = _tr.Lnodes(S.get('head'))
    if not nodes or nodes[-1].next is None or 'slow' not in S:
        return None
    start = next(i for i, nd in enumerate(nodes) if nd is nodes[-1].next)
    idx = {id(nd): i for i, nd in enumerate(nodes)}
    i, j = idx.get(id(S['slow'])), idx.get(id(S['fast']))
    if i is None or j is None or i < start or j < start:
        return None
    return (i - j) % (len(nodes) - start)


def _info(S):
    d = _gap(S)
    if d is None:
        return '乌龟 `slow` 每次走 1 步，兔子 `fast` 每次走 2 步'
    if d == 0:
        return '兔子和乌龟在==同一个节点==：追上了！'
    return f'两人都在环里：兔子还差 =={d}== 步追上乌龟（相对速度 1，每轮缩短 1）'


CONFIG = dict(
    num=141, title='环形链表', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='快慢指针（龟兔赛跑）',
    code='''
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head  # 乌龟和兔子同时从起点出发
        while fast and fast.next:
            slow = slow.next  # 乌龟走一步
            fast = fast.next.next  # 兔子走两步
            if fast is slow:  # 兔子追上乌龟（套圈），说明有环
                return True
        return False  # 访问到了链表末尾，无环
''',
    call='Solution().hasCycle(L([3, 2, 0, -4], 1))',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=27),
        dict(type='custom', h=480, draw=_ll({'slow': 'green', 'fast': 'pink'},
                                             title='链表：尾节点 -4 指回下标 1（有环）')),
    ],
    watch=[('slow（乌龟）', 'slow', 'green'), ('fast（兔子）', 'fast', 'pink'), ('兔子还差几步', _gap)],
    captions={
        'slow = fast = head': '乌龟 `slow` 和兔子 `fast` 同时从起点 `3` 出发',
        'while fast and fast.next': lambda S, B, r: (
            ('兔子还能跑两步 → 继续。==不用判断 slow==：乌龟走的都是兔子走过的路' if S.slow is S.head
             else '兔子还能跑两步 → 继续') if S.fast and S.fast.next else '兔子跑到了链表末尾 → 无环'),
        'slow = slow.next': lambda S, B, r: f'乌龟走一步 → `{S.slow.val}`',
        'fast = fast.next.next': lambda S, B, r: f'兔子走两步 → `{S.fast.val}`' + (
            f'（相对乌龟近了 1 步，还差 {_gap(S)} 步）' if _gap(S) and _gap(B) is not None else ''),
        'if fast is slow': lambda S, B, r: ('`fast is slow`：兔子追上乌龟（套圈）→ ==说明有环==' if S.fast is S.slow else
                                            f'兔子在 `{S.fast.val}`、乌龟在 `{S.slow.val}`，不是同一个节点 → 继续'),
        'return True': '返回 `True`',
    },
    cards=dict(
        one_liner='兔子每次两步、乌龟每次一步：有环的话兔子一定会追上乌龟',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你链表的头节点 `head`，判断链表中==是否有环==',
                 '示例：`head = [3,2,0,-4]`，`pos = 1`（尾节点连到下标 1）→ `true`',
                 '`pos` 只是评测用来建环，==不会作为参数传入=='],
        quote='如果有环的话，那么兔子和乌龟都会进入环中。这时用「相对速度」思考，==乌龟不动，兔子相对乌龟每次只走一步==，这样就可以看出兔子一定会和乌龟相遇了。',
        quote_src='—— 灵茶山艾府题解 · 答疑',
        idea=['无环：兔子先跑到终点，`fast` 或 `fast.next` 变成空',
              '有环：两人最终都进环，变成兔子在后面追乌龟',
              '兔子不会「跳过」乌龟：距离每轮只缩短 1，一定会减到 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '比较的是==节点地址== `fast is slow`，不是 `val`',
                 '`while` 只判断 `fast`：快人先去探路，慢人走的都是快人走过的路',
                 '进阶：返回入环口，见 142. 环形链表 II'],
    ),
)
