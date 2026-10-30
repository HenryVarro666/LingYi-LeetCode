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


CONFIG = dict(
    num=206, title='反转链表', difficulty='Easy', category='链表',
    author='yiduobo', technique='递归 · 先反转后面再接上自己',
    code='''
class Solution(object):
    def reverseList(self, head):
        if not head:
            return head
        return self.dfs(head)

    def dfs(self, now):
        if not now.next:
            return now

        new_head = self.dfs(now.next)
        now.next.next = now
        now.next = None
        return new_head
''',
    call='Solution().reverseList(L([1, 2, 3, 4, 5]))',
    expect=[5, 4, 3, 2, 1],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: (f"已反转部分（从 `new_head` 出发）：=={_chain(S['new_head'])}=="
                                        if S.get('new_head') else '「递」：先一路走到最后一个节点')),
        dict(type='custom', h=330, draw=_ll({'now': 'blue', 'new_head': 'pink'},
                                             title='链表（黄色 = 这一步刚改的 next）')),
        dict(type='calls', h=230),
    ],
    watch=[('now', 'now', 'blue'), ('new_head', 'new_head', 'pink')],
    captions={
        'if not head': '先特判：空链表直接返回',
        'return self.dfs': '链表非空 → 交给 `dfs(head)` 去反转',
        'if not now.next': lambda S, B, r: (f'`now = {S.now.val}` 没有 next → 它是==最后一个节点==' if S.now.next is None
                                            else f'`now = {S.now.val}` 还有 next → 先反转它后面的部分'),
        'return now': lambda S, B, r: f'最后一个节点 `{r.val}` 就是反转后的==新表头==，直接返回',
        'new_head = self.dfs': lambda S, B, r: f'递归反转 `{B.now.next.val}` 及之后的部分：进入 `dfs({B.now.next.val})`',
        'now.next.next = now': lambda S, B, r: (f'「归」：后面已反转成 {_chain(B.new_head)}，`now.next`（{S.now.next.val}）正是它的==尾部==；'
                                                f'`{S.now.next.val}.next = now`，把 `{S.now.val}` 接到尾部'),
        'now.next = None': lambda S, B, r: (f'`{S.now.val}.next = None`：`{S.now.val}` 成为新的尾部。'
                                            + (f'==不断开的话 {S.now.val} 和 {B.now.next.val} 互相指向，成环=='
                                               if S.new_head.next is S.now else f'反转部分：=={_chain(S.new_head)}==')),
        'return new_head': lambda S, B, r: f'新表头始终是 `{r.val}`，原样往上一层返回',
    },
    cards=dict(
        one_liner='先递归反转 now 后面的部分，再把 now 接到它的尾巴上',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['给你单链表的头节点 `head`，反转链表，返回反转后的链表',
                 '示例：`[1,2,3,4,5]` → `[5,4,3,2,1]`',
                 '节点数 `[0, 5000]`，链表可能为空'],
        quote='先递归反转now.next以及之后的部分……此时==now.next就是反转的链表的尾部==，因此将now.next.next指向now……然后将now.next指向null即可。',
        quote_src='—— yiduobo 题解',
        idea=['边界：`now` 没有 next，说明是最后一个节点，它就是新表头',
              '否则先反转 `now.next` 之后的部分，拿到 `new_head`',
              '`now.next` 成了尾部：`now.next.next = now` 接上，再断开 `now.next`'],
        summary=['时间 `O(n)`，空间 `O(n)`：递归深度等于链表长度',
                 '易错：忘了 `now.next = None` → 最后两个节点互相指向，==成环==',
                 '`new_head` 只在最深一层产生，之后每层原样返回',
                 '原文 `class Solution(object)` 在 Python 3 可直接运行，只删了文档字符串',
                 '作者说以前都写迭代版，这里特意用递归；迭代头插法见灵神的视频'],
    ),
)
