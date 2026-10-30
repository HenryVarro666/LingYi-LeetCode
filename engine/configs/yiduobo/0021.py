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


def _chain(node):
    vals = list_vals(node)
    return ' → '.join(map(str, vals)) if vals else '空'


def _rest(S):
    # l2 里还没插进来的节点：原来在 l2（第 1 行）且不在假头链上的节点
    inl1 = {nd._uid for nd in _tr.Lnodes(S['head'])}
    pool = {}
    for v in S.values():
        if isinstance(v, ListNode):
            for nd in _tr.Lnodes(v):
                pool[nd._uid] = nd
    rest = sorted((_tr._origin[u][1], nd.val) for u, nd in pool.items()
                  if u in _tr._origin and _tr._origin[u][0] == 1 and u not in inl1)
    return ' → '.join(str(v) for _, v in rest) or '空'


def _info(S):
    if 'head' not in S:
        return ''
    return f"假头之后：=={_chain(S['head'].next)}==　　l2 还没插入的：{_rest(S)}"


CONFIG = dict(
    num=21, title='合并两个有序链表', difficulty='Easy', category='链表',
    author='yiduobo', technique='二路归并 · 把 l2 的节点插进 l1',
    code='''
class Solution(object):
    def mergeTwoLists(self, l1, l2):
        head = ListNode(0)
        head.next = l1

        now = head

        while now.next is not None:
            while l2 is not None and l2.val < now.next.val:
                tmp = l2.next
                l2.next = now.next
                now.next = l2
                now = l2
                l2 = tmp
            now = now.next

        if l2 is not None:
            now.next = l2

        return head.next
''',
    setup='''
import tracer
a, b = L([2, 4]), L([1, 3, 5])
for i, nd in enumerate(tracer.Lnodes(a)): tracer._origin[nd._uid] = (0, 2 * i + 2)
for i, nd in enumerate(tracer.Lnodes(b)): tracer._origin[nd._uid] = (1, 2 * i + 1)
''',
    call='Solution().mergeTwoLists(a, b)',
    expect=[1, 2, 3, 4, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='custom', h=500, draw=_ll({'now': 'yellow', 'l2': 'pink', 'tmp': 'cyan', 'head': 'purple', 'l1': 'blue'},
                                             title='上：l1（最左是假头 head）　下：l2', place=lambda k, base: (0, 0))),
    ],
    watch=[('now', 'now', 'yellow'), ('l2', 'l2', 'pink'), ('tmp', 'tmp', 'cyan')],
    captions={
        3: '加一个==假头== `head`：l2 的节点要插到 l1 头部时，也不用特殊处理',
        4: '`head.next = l1`',
        6: '`now` 从假头出发：每次看 `now.next` 这个 l1 节点前面，要插入哪些 l2 节点',
        8: lambda S, B, r: (f'`now.next = {S.now.next.val}`：处理 l1 的这个节点' if S.now.next is not None
                            else '`now.next` 为空 → l1 的节点都处理完了'),
        9: lambda S, B, r: (f'`{S.l2.val} < {S.now.next.val}` → l2 的这个节点要==插到这个 l1 节点前面=='
                            if S.l2 is not None and S.l2.val < S.now.next.val else
                            ('l2 已经空了' if S.l2 is None else
                             f'`{S.l2.val} < {S.now.next.val}` 不成立 → `{S.now.next.val}` 前面没有要插的了')),
        10: lambda S, B, r: f'先用 `tmp` 记住 l2 的下一个节点 `{_v(S.tmp)}`',
        11: lambda S, B, r: f'`{S.l2.val}.next = now.next`：让 `{S.l2.val}` 指向 `{S.l2.next.val}`',
        12: lambda S, B, r: f'`now.next = l2`：`{S.l2.val}` 插入完成' + (
            '。它插在了 l1 的==最前面==，正是假头派上用场的地方' if S.now is S.head else ''),
        13: lambda S, B, r: f'`now` 移到刚插入的 `{S.now.val}`，它后面还是那个 l1 节点',
        14: lambda S, B, r: f'`l2` 换成之前记下的 `tmp` → `{_v(S.l2)}`',
        15: lambda S, B, r: f'`now` 前进到 l1 的节点 `{S.now.val}`',
        17: lambda S, B, r: (f'l1 处理完了，l2 还剩 `{_chain(S.l2)}`：它们都比 l1 最后一个节点大' if S.l2 is not None
                             else 'l2 没有剩余'),
        18: '把剩下的 l2 ==接在 l1 的屁股上==',
        20: lambda S, B, r: f'返回 `head.next` → =={_chain(r)}==',
    },
    cards=dict(
        one_liner='把 l2 的节点插进 l1：插在第一个比它大的 l1 节点前面',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['将两个==升序==链表合并为一个新的升序链表并返回',
                 '新链表由两个链表的所有节点拼接而成',
                 '示例：`l1 = [2,4]`，`l2 = [1,3,5]` → `[1,2,3,4,5]`'],
        quote='可以想象成对于l1中的每一个节点，找到l2中有哪些节点比这个l1中的节点要小，然后==将这些节点插到l1中节点的前面==，然后依次往后处理l1中的每一个节点即可。',
        quote_src='—— yiduobo 题解',
        idea=['经典的二路归并（归并排序的合并步骤），只不过在链表上做',
              '`now.next` 是当前的 l1 节点：l2 里比它小的，都插到它前面',
              'l1 处理完 l2 还有剩余 → 剩下的都更大，接在 l1 的屁股上'],
        summary=['时间 `O(m+n)`，空间 `O(1)`：每个节点至多遍历一次',
                 '假头处理「插到 l1 头部」的特殊情况，最后返回 `head.next`',
                 '内层用严格小于 `<`：相等时 l2 的节点排在 l1 节点后面',
                 '作者：增加链表头在链表的问题中是非常实用的操作',
                 '原文为 Python 2 风格：只删掉类型注释文档字符串，其余原样'],
    ),
)
