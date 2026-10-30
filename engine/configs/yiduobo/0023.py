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
    author='yiduobo', technique='小根堆 K 路归并',
    code="""
from queue import PriorityQueue

class Solution(object):
    def mergeKLists(self, lists):
        head = ListNode(0)
        now = head

        heap = PriorityQueue()
        for l in lists:
            if l is not None:
                heap.put((l.val, l))

        while not heap.empty():
            min_val, min_node = heap.get()
            now.next = min_node
            if min_node.next:
                heap.put((min_node.next.val, min_node.next))
            min_node.next = None
            now = min_node

        return head.next
""",
    # setup 只为可视化：PriorityQueue 内含线程锁、无法深拷贝，快照时改为拷贝它内部的堆数组 .queue（不影响算法）
    setup="""
import queue, copy
queue.PriorityQueue.__deepcopy__ = lambda self, memo: copy.deepcopy(self.queue, memo)
""",
    call='Solution().mergeKLists([L([1,4,5]), L([2,6]), L([3])])',
    expect=[1, 2, 3, 4, 5, 6],
    result_fn=list_vals,
    views=[
        dict(type='heap', var='heap', label='小根堆 heap（元素是 (val, node)，这里只写 val）', fmt=lambda x: str(x[0]), h=110),
        dict(type='custom', draw=_kv({'min_node': 'pink', 'now': 'blue', 'head': 'cyan'}, 'head', 'now',
                                     'lists：还没取出的节点留在原位；取出的节点接到最下面的答案链表'), h=520),
    ],
    watch=['min_val', ('min_node', 'min_node', 'pink'), ('now', 'now', 'blue')],
    captions={
        'from queue import PriorityQueue': '导入优先队列（小根堆）',
        'head = ListNode(0)': '假表头 `head`：答案链表挂在它后面',
        'now = head': '`now` 指向答案链表的末尾',
        'heap = PriorityQueue()': '小根堆：堆顶永远是最小的元素，取最小 `O(1)`，插入/删除 `O(log K)`',
        'for l in lists': lambda S, B, ret: ('看第 {} 条链表的头部'.format([x._uid for x in S.lists].index(S.l._uid) + 1)
                                             if 'l' not in B or S.l._uid != B.l._uid else '所有链表的头部都处理完了'),
        'if l is not None': lambda S, B, ret: '头部 `{}` 非空'.format(B.l.val) if B.l is not None else '空链表，跳过',
        'heap.put((l.val, l))': '堆中存放这 K 个链表的头部：放入 `({l.val}, 节点)`',
        'while not heap.empty()': lambda S, B, ret: '堆不空 → 取出最小的' if B.heap else '堆空了 → 没有节点了，结束',
        'min_val, min_node = heap.get()': '从堆中取出最小的节点 `{min_val}`：它一定是剩下所有节点中最小的',
        'now.next = min_node': '将其加入答案：接在 `now` 后面',
        'if min_node.next': lambda S, B, ret: ('它所在链表还有下一个节点 `{}`'.format(B.min_node.next.val) if B.min_node.next
                                               else '它是所在链表的最后一个'),
        'heap.put((min_node.next.val, min_node.next))': '将其所在链表的下一个节点 `{min_node.next.val}` 加入堆',
        'min_node.next = None': lambda S, B, ret: ('`min_node.next = None`：和原链表断开（下一个已经在堆里了）' if B.min_node.next
                                                   else '`min_node.next` 本来就是空，置空不影响'),
        'now = min_node': '`now` 移到答案末尾 `{now.val}`',
        'return head.next': '返回 `head.next`',
    },
    cards=dict(
        one_liner='堆里放 K 个链表的头部：取出最小的接到答案，再补进它的下一个',
        complexity='时间 `O(n log K)`，空间 `O(K)`（`n` 个节点，`K` 条链表）',
        problem=['给 `K` 条==升序==链表，合并成一条升序链表',
                 '示例（演示用无重复值的小例子）：`[[1,4,5],[2,6],[3]]` → `[1,2,3,4,5,6]`'],
        quote='K路的归并我们可以维护一个小根堆，堆中存放这K个链表的头部。接下来我们从堆中取出最小的节点，将其加入答案……并将其所在链表的下一个节点加入到堆当中。',
        quote_src='—— yiduobo 题解',
        idea=['小根堆：任意节点 `p` 都比左右儿子小 ⇒ ==堆顶就是最小==',
              '每次取出的都是当前剩下节点中最小的 ⇒ 合并结果有序',
              '`n` 个节点各做一次插入 + 删除，每次 `O(log K)` ⇒ `O(n log K)`'],
        summary=['时间 `O(n log K)`，空间 `O(K)`',
                 '取出后 `min_node.next = None`，答案链表不会残留旧指针',
                 '原文为 Python 2 写法：`from Queue` 已改为 `from queue`，并删掉文档字符串',
                 'Python 3 中 `val` 相同会比较 `ListNode` 而报错：可存 `(val, i, node)`'],
    ),
)
