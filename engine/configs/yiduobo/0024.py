import tracer as _tr


def _ll_view(ptrs, title='链表', hide=(), new_row=None):
    """自绘单链表：节点按输入位置固定不动；相邻的正向 next 画直箭头，
    其余（跨越 / 反向）画在节点下方的弧线；指针名写在节点上方；本步改动的 next 标黄。"""
    def collect(S):
        nodes = {}

        def walk(v, d=0):
            if isinstance(v, (list, tuple)) and d < 2:
                for y in v:
                    walk(y, d + 1)
            while isinstance(v, (ListNode, Node)) and v._uid not in nodes:
                nodes[v._uid] = v
                v = v.next
        for k, v in S.items():
            if k not in hide:
                walk(v)
        return nodes

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        nodes, bnodes = collect(S), collect(B)
        org = _tr._origin
        base = max([r for r, c in org.values()] + [-1]) + 1
        pos = {u: org[u] for u in nodes if u in org}
        for k, u in enumerate(sorted(u for u in nodes if u not in org)):
            pos[u] = new_row(k, base) if new_row else (base, k)
        allp = list(org.values()) + list(pos.values())
        R = max(r for r, c in allp) + 1
        C = max(c for r, c in allp) + 1
        gap = min(150, (x1 - x0 - 100) / C)
        nw, nh = min(74, gap * 0.56), 50
        top = y0 + 112
        rowh = min(170, (y1 - top - nh - 50) / max(1, R - 1)) if R > 1 else 0
        top += max(0, ((y1 - y0) - (112 + nh + 140 + (R - 1) * rowh)) / 2)

        def xy(u):
            r, c = pos[u]
            return x0 + 50 + c * gap + nw / 2, top + nh / 2 + r * rowh

        links = {}
        for u, nd in nodes.items():
            if nd.next is not None and nd.next._uid in pos:
                links[pos[u]] = pos[nd.next._uid]
        for u, nd in nodes.items():
            X, Y = xy(u)
            r, c = pos[u]
            nx = nd.next
            bn = bnodes.get(u)
            ch = bn is not None and getattr(bn.next, '_uid', None) != getattr(nx, '_uid', None)
            lc, lw = (T['yellow'], 4) if ch else (T['muted'], 3)
            if nx is None:
                busy = links.get((r, c + 1)) == (r, c)  # 右边邻居有箭头指回来，∅ 挪到上方
                cv.text((X + nw / 2 + 8, Y - (22 if busy else 0)), '∅', 24, T['yellow'] if ch else T['dim'], anchor='lm')
                continue
            if nx._uid not in pos:
                continue
            X2, Y2 = xy(nx._uid)
            r2, c2 = pos[nx._uid]
            both = links.get((r2, c2)) == (r, c)
            if r2 == r and c2 == c + 1:
                dy = -9 if both else 0
                cv.arrow((X + nw / 2 + 2, Y + dy), (X2 - nw / 2 - 3, Y2 + dy), lc, lw, 12)
            elif r2 == r and c2 == c - 1:
                dy = 9 if both else 0
                cv.arrow((X - nw / 2 - 2, Y + dy), (X2 + nw / 2 + 3, Y2 + dy), lc, lw, 12)
            elif r2 == r:
                fwd = c2 > c
                s = nw * 0.2
                p0 = (X + (s if fwd else -s), Y + nh / 2 + 2)
                p1 = (X2 - (s if fwd else -s), Y2 + nh / 2 + 4)
                cv.arc_arrow(p0, p1, -(26 + 15 * abs(c2 - c) + (0 if fwd else 14)), lc, lw, 12)
            else:
                down = r2 > r
                p0 = (X, Y + (nh / 2 if down else -nh / 2))
                p1 = (X2, Y2 - (nh / 2 + 3 if down else -nh / 2 - 3))
                cv.arrow(p0, p1, lc, lw, 12)
        hit = {}
        for k, (name, c) in enumerate(ptrs.items()):
            v = S.get(name.split('.')[0])
            for a in name.split('.')[1:]:
                v = getattr(v, a, None)
            if isinstance(v, (ListNode, Node)) and v._uid in pos:
                hit.setdefault(v._uid, []).append((name, T[c]))
        for u, nd in nodes.items():
            X, Y = xy(u)
            hs = hit.get(u, [])
            fill = hs[0][1] if hs else T['panel2']
            cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
            cv.text((X, Y), nd.val, 25, T['bg'] if hs else T['text'], anchor='mm', bold=True)
            for i, (name, cc) in enumerate(hs):
                cv.text((X, Y - nh / 2 - 6 - i * 25), name, 21, cc, anchor='mb', bold=True)
        nones = [n for n in ptrs if n in S and S[n] is None]
        if nones:
            cv.text((x1 - 20, y0 + 6), '  '.join(f'{n}=None' for n in nones), 20, T['muted'], anchor='ra', mono=True)
    return draw


def _links(S):
    parts = []
    for name in ('now', 'tmp'):
        v = S.get(name)
        if v is None:
            continue
        chain, x, k = [f'{name}({v.val})'], v.next, 0
        while x is not None and k < 3:
            chain.append(str(x.val))
            x, k = x.next, k + 1
        chain.append('∅' if x is None else '…')
        parts.append(' → '.join(chain))
    return ('链接情况：' + '　|　'.join(parts)) if parts else ''


CONFIG = dict(
    num=24, title='两两交换链表中的节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='假表头 + 按顺序改指针',
    code="""
class Solution(object):
    def swapPairs(self, head):
        new_head = ListNode(0)
        new_head.next = head

        now = new_head

        while now.next and now.next.next:
            tmp = now.next.next
            now.next.next = tmp.next
            tmp.next = now.next
            now.next = tmp
            now = tmp.next

        return new_head.next
""",
    # setup 只做布局：把运行中创建的第一个节点（假表头）放在第 0 行最左边，原链表整体右移一格
    setup="""
import tracer, itertools
head = L([1,2,3,4])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
""",
    call='Solution().swapPairs(head)',
    expect=[2, 1, 4, 3],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_links),
        dict(type='custom', draw=_ll_view({'now': 'purple', 'tmp': 'pink', 'now.next': 'blue', 'new_head': 'cyan'},
                                          title='链表（最左边是假表头 new_head；黄色 = 这一步改的指针）'), h=420),
    ],
    watch=[('now', 'now', 'purple'), ('tmp', 'tmp', 'pink'), ('now.next', 'now.next')],
    captions={
        'new_head = ListNode(0)': '加一个假表头 `new_head`：充当最开始的 `now`',
        'new_head.next = head': '假表头接在原链表前面',
        'now = new_head': '`now` 站在要交换的一对==前面==：`now → node1 → node2 → right`',
        'while now.next and now.next.next': lambda S, B, ret: ('`now` 后面还有两个节点（`{}`、`{}`）→ 交换它们'.format(B.now.next.val, B.now.next.next.val)
                                                               if B.now.next and B.now.next.next else
                                                               '`now` 后面不足两个节点 → 结束'),
        'tmp = now.next.next': '① 记下 node2 为 `tmp`（=`{tmp.val}`）：现在能直接访问的只有 `now` 和 `tmp`',
        'now.next.next = tmp.next': lambda S, B, ret: '② node1 指向 right：`now.next.next = tmp.next` → `{} → {}`'.format(
            S.now.next.val, S.now.next.next.val if S.now.next.next else '∅'),
        'tmp.next = now.next': '③ `tmp` 指向 node1：`{tmp.val} → {tmp.next.val}`（node1 仍是 `now.next`，还能找到）',
        'now.next = tmp': '④ 最后才改 `now.next = tmp`：`now → {tmp.val} → {tmp.next.val}`，这一对交换完成',
        'now = tmp.next': '⑤ 跳到 node1（`tmp.next`，=`{now.val}`），继续处理后面的节点',
        'return new_head.next': '返回 `new_head.next`',
    },
    cards=dict(
        one_liner='先改后面、再改前面：靠前的 next 一改，后面的节点就找不到了',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两两交换相邻节点，返回新的头节点',
                 '==不能改节点的值==，只能改指针',
                 '示例：`[1,2,3,4]` → `[2,1,4,3]`'],
        quote='一旦靠前的节点产生变动，那么就无法根据next找到后面的节点了……因此在交换的时候必须要注意顺序，并利用临时节点储存信息。',
        quote_src='—— yiduobo 题解',
        idea=['`now → node1 → node2 → right`：只用 `now` 和 `tmp` 两个变量',
              '顺序：存 `tmp`，node1 接 right，`tmp` 接 node1，==最后才改== `now.next`',
              '交换后 node1 在后面，`now` 跳到它，继续下一对'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：先改 `now.next` 会丢掉 node1；每一步都要确认“还能找到谁”',
                 '假表头 `new_head` 充当第一个 `now`，返回 `new_head.next`',
                 '原文为 Python 2 写法：仅删掉了 `"""type"""` 文档字符串，逻辑未改'],
    ),
)
