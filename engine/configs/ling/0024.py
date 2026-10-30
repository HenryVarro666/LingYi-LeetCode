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


def _order(S):
    d = S.get('dummy')
    if d is None:
        return ''
    out, x, seen = [], d.next, set()
    while x is not None and id(x) not in seen and len(out) < 12:
        seen.add(id(x)); out.append(str(x.val)); x = x.next
    return '从 `dummy` 往后读：' + ' → '.join(out) + ' → ∅'


CONFIG = dict(
    num=24, title='两两交换链表中的节点', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='迭代 + 哨兵节点',
    code='''
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node0 = dummy = ListNode(next=head)  # 用哨兵节点简化代码逻辑
        node1 = head
        while node1 and node1.next:  # 至少有两个节点
            node2 = node1.next
            node3 = node2.next

            node0.next = node2  # 0 -> 2
            node2.next = node1  # 2 -> 1
            node1.next = node3  # 1 -> 3

            node0 = node1  # 下一轮交换，0 是 1
            node1 = node3  # 下一轮交换，1 是 3
        return dummy.next  # 返回新链表的头节点
''',
    # setup 只做布局：把运行中创建的第一个节点（dummy）放在第 0 行最左边，原链表整体右移一格
    setup='''
import tracer, itertools
head = L([1,2,3,4])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().swapPairs(head)',
    expect=[2, 1, 4, 3],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_order),
        dict(type='custom', draw=_ll_view({'node0': 'purple', 'node1': 'blue', 'node2': 'pink', 'node3': 'green', 'dummy': 'cyan'},
                                          title='链表（节点不动，只改 next；黄色 = 这一步改的指针）'), h=420),
    ],
    watch=[('node0', 'node0', 'purple'), ('node1', 'node1', 'blue'), ('node2', 'node2', 'pink'), ('node3', 'node3', 'green')],
    captions={
        'node0 = dummy': '哨兵 `dummy` 当作第一组的 `node0`：==头节点也会被换走==，有哨兵就不用特判',
        'node1 = head': '`node1` 是这一组的第一个节点',
        'while node1 and node1.next': lambda S, B, ret: ('至少还有两个节点（`{}` 和 `{}`）→ 交换这一对'.format(B.node1.val, B.node1.next.val)
                                                         if B.node1 and B.node1.next else
                                                         '剩下不足两个节点 → 无需交换，循环结束'),
        'node2 = node1.next': '`node2` = `{node2.val}`：这一对的第二个',
        'node3 = node2.next': '先记住 `node3`（下一组的开头）：改完指针后就==找不到它==了',
        'node0.next = node2': '第 1 步 `0 → 2`（这一轮是 `{node0.val} → {node2.val}`）：前驱先连到这一对的第二个',
        'node2.next = node1': '第 2 步 `2 → 1`（`{node2.val} → {node1.val}`）：第二个反过来指向第一个',
        'node1.next = node3': lambda S, B, ret: '第 3 步 `1 → 3`（`{} → {}`）：接上下一组，==这一对交换完成=='.format(
            S.node1.val, S.node3.val if S.node3 else '∅'),
        'node0 = node1': '交换后 `{node1.val}` 在这一对的后面 → 下一轮的 `node0` 就是它',
        'node1 = node3': lambda S, B, ret: '下一轮的 `node1` 是 `node3`（{}）'.format(S.node1.val if S.node1 else 'None'),
        'return dummy.next': '返回 `dummy.next`：新的头节点（原来的第 2 个）',
    },
    cards=dict(
        one_liner='四个指针 node0~node3，按 0→2、2→1、1→3 的顺序改三根 next',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两两交换相邻节点，返回新的头节点',
                 '==不能改节点的值==，只能改指针',
                 '示例：`[1,2,3,4]` → `[2,1,4,3]`'],
        quote='`node0.next = node2  # 0 -> 2`\n`node2.next = node1  # 2 -> 1`\n`node1.next = node3  # 1 -> 3`',
        quote_src='—— 灵茶山艾府题解（迭代写法，配“一张图秒懂”）',
        idea=['一组交换涉及 4 个节点：前驱 `node0`、这一对 `node1`/`node2`、后继 `node3`',
              '先把 `node2`、`node3` 存下来，再改 3 根 `next`，==谁也不会丢==',
              '交换后 `node1` 跑到后面，正好当下一组的 `node0`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '哨兵 `dummy` 让第一组和后面的组写法一样，最后返回 `dummy.next`',
                 '循环条件 `node1 and node1.next`：至少两个节点才交换',
                 '灵神还给了递归写法：先递归交换 `node3` 之后，再 `2 → 1 → 递归结果`，空间 `O(n)`',
                 '思考题：每 `k` 个一组反转 → 25 题'],
    ),
)
