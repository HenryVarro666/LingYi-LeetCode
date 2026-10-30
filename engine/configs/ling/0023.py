import tracer as _tr


def _kv(ptrs, dummy, tail, title):
    """23 专用：上面几行是还没合并的原链表（节点留在原位），最下面一行是新链表——
    节点被接到新链表末尾时就“搬”到最下面一行；黄色 = 这一步改的 next，虚线 = 新链表末尾仍连着的旧 next。"""
    def collect(S):
        nodes = {}

        def walk(v, d=0):
            if isinstance(v, (list, tuple)) and d < 2:
                for y in v:
                    walk(y, d + 1)
            while isinstance(v, ListNode) and v._uid not in nodes:
                nodes[v._uid] = v
                v = v.next
        for k, v in S.items():
            if not k.startswith('_'):
                walk(v)
        return nodes

    def chain(S):
        d, t = S.get(dummy), S.get(tail)
        out = []
        if d is None or t is None or t is d:
            return out
        x = d.next
        while x is not None and len(out) < 30:
            out.append(x._uid)
            if x is t:
                break
            x = x.next
        return out

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        nodes, bnodes = collect(S), collect(B)
        org = _tr._origin
        R = max([r for r, c in org.values()] + [0]) + 1
        total = len(org)
        merged = chain(S)
        pos = {u: org[u] for u in nodes if u in org}
        for k, u in enumerate(merged):
            pos[u] = (R, k + 1)
        d = S.get(dummy)
        if d is not None:
            pos[d._uid] = (R, 0)
        gap = min(130, (x1 - x0 - 110) / (total + 1))
        nw, nh = min(64, gap * 0.62), 46
        top = y0 + 84
        rowh = min(120, (y1 - 8 - top - nh - 28) / R)

        def xy(u):
            r, c = pos[u]
            return x0 + 80 + c * gap + nw / 2, top + nh / 2 + r * rowh + (24 if r == R else 0)

        for r in range(R):
            cv.text((x0 + 18, top + nh / 2 + r * rowh), f'[{r}]', 20, T['dim'], anchor='lm', mono=True)
        yR = top + nh / 2 + R * rowh + 24
        yR = top + nh / 2 + R * rowh + 24
        cv.line([(x0 + 18, yR - nh / 2 - 30), (x1 - 18, yR - nh / 2 - 30)], T['border'], 1)
        cv.text((x0 + 14, yR), '新链表', 18, T['muted'], anchor='lm')
        mset = set(merged)
        for u, nd in nodes.items():
            if u not in pos:
                continue
            X, Y = xy(u)
            nx = nd.next
            bn = bnodes.get(u)
            ch = bn is not None and getattr(bn.next, '_uid', None) != getattr(nx, '_uid', None)
            lc, lw = (T['yellow'], 4) if ch else (T['muted'], 3)
            if nx is None:
                if u not in mset or u == merged[-1]:
                    cv.text((X + nw / 2 + 6, Y), '∅', 22, T['yellow'] if ch else T['dim'], anchor='lm')
                continue
            if nx._uid not in pos:
                continue
            X2, Y2 = xy(nx._uid)
            r, c = pos[u]
            r2, c2 = pos[nx._uid]
            if r2 == r and c2 == c + 1:
                cv.arrow((X + nw / 2 + 2, Y), (X2 - nw / 2 - 3, Y2), lc, lw, 11)
            else:  # 新链表末尾的 next 还指着上面某个没合并的节点：写成 “next→v”，并给目标节点画虚线框
                cc = T['yellow'] if ch else T['muted']
                cv.text((X + nw / 2 + 8, Y), f'next→{nx.val}', 19, cc, anchor='lm', mono=True)
                for a, b in (((X2 - nw / 2 - 5, Y2 - nh / 2 - 5), (X2 + nw / 2 + 5, Y2 - nh / 2 - 5)),
                             ((X2 + nw / 2 + 5, Y2 - nh / 2 - 5), (X2 + nw / 2 + 5, Y2 + nh / 2 + 5)),
                             ((X2 + nw / 2 + 5, Y2 + nh / 2 + 5), (X2 - nw / 2 - 5, Y2 + nh / 2 + 5)),
                             ((X2 - nw / 2 - 5, Y2 + nh / 2 + 5), (X2 - nw / 2 - 5, Y2 - nh / 2 - 5))):
                    cv.dashed(a, b, cc, 2, 8, 6)
        hit = {}
        for name, c in ptrs.items():
            v = S.get(name)
            if isinstance(v, ListNode) and v._uid in pos:
                hit.setdefault(v._uid, []).append((name, T[c]))
        for u, nd in nodes.items():
            if u not in pos:
                continue
            X, Y = xy(u)
            hs = hit.get(u, [])
            fill = hs[0][1] if hs else T['panel2']
            cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
            cv.text((X, Y), nd.val, 24, T['bg'] if hs else T['text'], anchor='mm', bold=True)
            for i, (name, cc) in enumerate(hs):
                cv.text((X, Y - nh / 2 - 4 - i * 23), name, 19, cc, anchor='mb', bold=True)
    return draw


CONFIG = dict(
    num=23, title='合并 K 个升序链表', difficulty='Hard', category='链表',
    author='灵茶山艾府', technique='最小堆',
    code="""
# 让堆可以比较节点大小（不改 __lt__ 的写法见 Python3 写法二）
ListNode.__lt__ = lambda a, b: a.val < b.val

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 哨兵节点，作为合并后链表头节点的前一个节点
        h = [head for head in lists if head]  # 把所有非空链表的头节点入堆
        heapify(h)  # 堆化
        while h:  # 循环直到堆为空
            node = heappop(h)  # 剩余节点中的最小节点
            if node.next:  # 下一个节点不为空
                heappush(h, node.next)  # 下一个节点有可能是最小节点，入堆
            cur.next = node  # 把 node 添加到新链表的末尾
            cur = cur.next  # 准备合并下一个节点
        return dummy.next  # 哨兵节点的下一个节点就是新链表的头节点
""",
    call='Solution().mergeKLists([L([1,4,5]), L([1,3,4]), L([2,6])])',
    expect=[1, 1, 2, 3, 4, 4, 5, 6],
    result_fn=list_vals,
    views=[
        dict(type='heap', var='h', label='最小堆 h', fmt=lambda x: str(x.val), h=110),
        dict(type='custom', draw=_kv({'node': 'pink', 'cur': 'blue', 'dummy': 'cyan'}, 'dummy', 'cur',
                                     'lists：还没合并的节点留在原位；合并的节点搬到最下面的新链表'), h=520),
    ],
    watch=[('node', 'node', 'pink'), ('cur', 'cur', 'blue')],
    captions={
        'cur = dummy = ListNode()': '哨兵 `dummy`：合并后链表头节点的前一个；`cur` 指向新链表末尾',
        'h = [head for head': '合并后的第一个节点，==一定是某个链表的头==：把所有非空头节点放进堆',
        'heapify(h)': '堆化：堆顶就是最小的头节点',
        'while h:': lambda S, B, ret: '堆不空 → 继续' if B.h else '堆空了 → 所有节点都已合并',
        'node = heappop(h)': '弹出堆顶 `{node.val}`：它是剩余节点中最小的',
        'if node.next:': lambda S, B, ret: ('`{}` 后面还有 `{}`'.format(B.node.val, B.node.next.val) if B.node.next
                                            else '`{}` 是所在链表的最后一个，没有后继要入堆'.format(B.node.val)),
        'heappush(h, node.next)': '`{node.next.val}` ==有可能是下一个最小节点==，入堆',
        'cur.next = node': '把 `{node.val}` 接到新链表末尾',
        'cur = cur.next': '`cur` 移到新链表末尾 `{cur.val}`',
        'return dummy.next': '返回 `dummy.next`',
    },
    cards=dict(
        one_liner='堆里放“可能是最小”的节点：弹出一个，就把它的 next 补进去',
        complexity='时间 `O(L log m)`，空间 `O(m)`（`m` 条链表，共 `L` 个节点）',
        problem=['给 `m` 条==升序==链表，合并成一条升序链表',
                 '示例：`[[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`'],
        quote='合并后的第一个节点 first，一定是某个链表的头节点……每当我们找到一个节点值最小的节点 x，就把节点 x.next 加入「可能是最小节点」的集合中。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['“可能是最小节点”的集合：每条链表当前最靠前、还没合并的节点',
              '需要：找并移除最小 + 插入 ⇒ ==最小堆==，堆里最多 `m` 个节点',
              '`ListNode.__lt__` 让堆能直接比较节点'],
        summary=['时间 `O(L log m)`，空间 `O(m)`',
                 '哨兵 `dummy` 简化拼接，最后返回 `dummy.next`',
                 'Python 堆要能比较元素：改 `__lt__`，或入堆 `(val, i, node)`（写法二）',
                 '方法二分治：一分为二合并（21 题），同样 `O(L log m)`；迭代版空间 `O(1)`'],
    ),
)
