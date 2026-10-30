def _lru_view(start, sentinels, ptrs, title, note):
    """146 专用：从哨兵出发沿 next 走一圈，按顺序画成一行；上车道 = next，下车道 = prev；
    不在环上的节点（刚抽出 / 还没插入）画在上方；和相邻关系对不上的指针画成弧线；本步改动的指针标黄。"""
    def ident(S, n):
        for name, tag in sentinels.items():
            if n is S.get(name):
                return tag
        return getattr(n, 'key', None)

    def layout(S):
        st = S.get(start)
        if st is None:
            return None, [], []
        ring, x = [st], getattr(st, 'next', None)
        while x is not None and x is not st and len(ring) < 10:
            ring.append(x)
            x = getattr(x, 'next', None)
        seen = {id(n) for n in ring}
        det = []
        cands = list(ptrs) + [k for k in S if k.endswith('key_to_node') or k == 'self.cache']
        for name in cands:
            v = S.get(name)
            vs = list(v.values()) if isinstance(v, dict) else [v]
            for n in vs:
                if n is not None and hasattr(n, 'key') and id(n) not in seen:
                    seen.add(id(n))
                    det.append(n)
        return st, ring, det

    def links(S):
        st, ring, det = layout(S)
        out = {}
        for n in ring + det:
            out[ident(S, n)] = (ident(S, getattr(n, 'next', None)) if getattr(n, 'next', None) is not None else None,
                                ident(S, getattr(n, 'prev', None)) if getattr(n, 'prev', None) is not None else None)
        return out

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        st, ring, det = layout(S)
        if st is None:
            cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
            return
        bl = links(B)
        gap = min(190, (x1 - x0 - 120) / max(1, len(ring)))
        nw, nh = min(104, gap * 0.62), 50
        Y = y0 + 240
        P = {}
        for i, n in enumerate(ring):
            P[id(n)] = (x0 + 70 + nw / 2 + i * gap, Y)
        for k, n in enumerate(det):
            pv, nx = getattr(n, 'prev', None), getattr(n, 'next', None)
            if pv is not None and nx is not None and id(pv) in P and id(nx) in P:
                X = (P[id(pv)][0] + P[id(nx)][0]) / 2
            else:
                X = x0 + 70 + nw / 2 + (len(ring) - 0.3 + k) * gap
            P[id(n)] = (min(X, x1 - nw / 2 - 20), Y - 112)

        def changed(n, which):
            old = bl.get(ident(S, n))
            if old is None:
                return False
            tgt = getattr(n, which, None)
            return old[0 if which == 'next' else 1] != (ident(S, tgt) if tgt is not None else None)

        def col(n, which):
            return (T['yellow'], 4) if changed(n, which) else (T['muted'], 3)

        L = len(ring)
        for i, n in enumerate(ring):
            X, _ = P[id(n)]
            nx, pv = getattr(n, 'next', None), getattr(n, 'prev', None)
            # next：相邻画上车道直箭头；最后一个指回哨兵画下方弧线
            if i + 1 < L:
                c, w = col(n, 'next')
                cv.arrow((X + nw / 2 + 2, Y - 9), (P[id(ring[i + 1])][0] - nw / 2 - 3, Y - 9), c, w, 11)
            elif nx is not None and id(nx) in P and nx is not n:
                c, w = col(n, 'next')
                X2, Y2 = P[id(nx)]
                if Y2 == Y:
                    cv.arc_arrow((X + nw * 0.2, Y + nh / 2 + 2), (X2 + nw * 0.2, Y2 + nh / 2 + 4), -(44 + 4 * L), c, w, 11)
                    cv.text(((X + X2) / 2 + nw * 0.2, Y + nh / 2 + 24 + 2 * L), 'next', 17, c, anchor='mt')
                else:
                    cv.dashed((X, Y - nh / 2), (X2, Y2 + nh / 2), c, 2)
            # prev：和左邻一致画下车道直箭头；哨兵的 prev 指向最后一个画更深的下方弧线；其余对不上的画上方弧线
            if pv is None or pv is n:
                continue
            c, w = col(n, 'prev')
            if i >= 1 and pv is ring[i - 1]:
                cv.arrow((X - nw / 2 - 2, Y + 9), (P[id(pv)][0] + nw / 2 + 3, Y + 9), c, w, 11)
            elif id(pv) in P:
                X2, Y2 = P[id(pv)]
                if Y2 == Y and i == 0:
                    cv.arc_arrow((X - nw * 0.2, Y + nh / 2 + 2), (X2 - nw * 0.2, Y2 + nh / 2 + 4), -(96 + 4 * L), c, w, 11)
                    cv.text(((X + X2) / 2 - nw * 0.2, Y + nh / 2 + 50 + 2 * L), 'prev', 17, c, anchor='mt')
                elif Y2 == Y:
                    cv.arc_arrow((X - nw * 0.25, Y - nh / 2 - 2), (X2 + nw * 0.25, Y2 - nh / 2 - 4), 34 + 6 * abs(i), c, w, 11)
                else:
                    cv.dashed((X - nw * 0.3, Y - nh / 2), (X2 + nw * 0.3, Y2 + nh / 2), c, 2)
        if len(ring) == 1 and getattr(st, 'next', None) is st:
            cv.text((P[id(st)][0] + nw / 2 + 10, Y), '↺ prev、next 都指向自己', 20, T['dim'], anchor='lm')
        for n in det:  # 不在环上的节点：用虚线画出它的 prev / next（从靠近目标的一侧出发）
            X, Yd = P[id(n)]
            for which in ('prev', 'next'):
                tgt = getattr(n, which, None)
                if tgt is not None and id(tgt) in P:
                    X2, Y2 = P[id(tgt)]
                    sg = 1 if X2 > X + 1 else (-1 if X2 < X - 1 else (1 if which == 'next' else -1))
                    c, w = col(n, which)
                    p0 = (X + sg * nw * 0.3, Yd + nh / 2)
                    p1 = (X2 - sg * nw * 0.15, Y2 - nh / 2 - 2)
                    cv.dashed(p0, p1, c, 3 if c == T['yellow'] else 2)
                    mx, my = p0[0] + (p1[0] - p0[0]) * 0.4, p0[1] + (p1[1] - p0[1]) * 0.4
                    cv.text((mx + sg * 10, my), which, 17, c, anchor='lm' if sg > 0 else 'rm')
        hit = {}
        for name, c in ptrs.items():
            v = S.get(name)
            if v is not None and id(v) in P:
                hit.setdefault(id(v), []).append((name, T[c]))
        for n in ring + det:
            X, Yn = P[id(n)]
            hs = hit.get(id(n), [])
            tag = ident(S, n)
            sent = tag in sentinels.values()
            fill = hs[0][1] if hs else ((52, 46, 70) if sent else T['panel2'])
            cv.rect((X - nw / 2, Yn - nh / 2, X + nw / 2, Yn + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
            if sent:
                txt = tag
            else:
                txt = f"{n.key}:{getattr(n, 'value', getattr(n, 'val', '?'))}"
            cv.text((X, Yn), txt, 22, T['bg'] if hs else T['text'], anchor='mm', bold=True, mono=not sent)
            for i, (name, cc) in enumerate(hs):
                cv.text((X, Yn - nh / 2 - 4 - i * 22), name, 19, cc, anchor='mb', bold=True)
        if L > 1:
            cv.text((x0 + 18, Y + nh / 2 + 86 + 4 * L), note, 18, T['dim'], anchor='lt')
    return draw


def _nm(S, n):
    if n is S.get('self.head'):
        return 'head'
    if n is S.get('self.tail'):
        return 'tail'
    return f'{n.key}:{n.val}' if n is not None else 'None'


CONFIG = dict(
    num=146, title='LRU 缓存', difficulty='Medium', category='链表',
    author='yiduobo', technique='dict + 双向链表（假头 + 假尾）',
    code="""
class ListNode(object):

    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.cache = {}
        self.head = ListNode()
        self.tail = ListNode()
        self.head.prev = self.tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.tail.next = self.head

    def remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_tail(self, node):
        self.tail.prev.next = node
        node.prev = self.tail.prev
        self.tail.prev = node
        node.next = self.tail

    def get(self, key):
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.remove_node(node)
        self.move_tail(node)
        return node.val

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self.remove_node(node)
        else:
            if self.size == self.capacity:
                node = self.head.next
                self.remove_node(node)
                self.cache.pop(node.key)
                node.key = key
                node.val = value
            else:
                node = ListNode(key, value)
                self.cache[key] = node
                self.size += 1

            self.cache[key] = node

        self.move_tail(node)
""",
    call="""c = LRUCache(2)
c.put(1, 1)
c.put(2, 2)
c.get(1)
c.put(3, 3)
c.get(2)""",
    expect=-1,
    views=[
        dict(type='custom', draw=_lru_view('self.head', {'self.head': 'head', 'self.tail': 'tail'}, {'node': 'pink'},
                                           '双向链表（上车道 next、下车道 prev；黄色 = 这一步改的）',
                                           '从左到右：head → 最久未使用 → … → 最近使用 → tail → 回到 head'), h=380),
        dict(type='map', var='self.cache', label='cache（key → 节点）', fmt=lambda k, v: f'{k} → {v.key}:{v.val}', h=95),
        dict(type='calls', label='正在执行', h=155),
    ],
    watch=['key', 'value', ('size', 'self.size'), ('capacity', 'self.capacity')],
    skip=['self.key = key', 'self.val = val', 'self.prev = None', 'self.next = None'],
    captions={
        'self.capacity = capacity': '`LRUCache({capacity})`：容量 `{capacity}`',
        'self.size = 0': '`size` 记录当前有几个 key',
        'self.cache = {}': 'key-value 的存取用 dict：`key` → 链表节点',
        'self.head = ListNode()': '假头 `head`：它的 `next` 是最久未使用的节点',
        'self.tail = ListNode()': '假尾 `tail`：它的 `prev` 是最近使用的节点',
        'self.head.prev = self.tail': '首尾相连成环：有了假头假尾，就==不需要判断 now 是否存在 prev 与 next== 了',
        'self.head.next = self.tail': '`head.next = tail`（空链表）',
        'self.tail.prev = self.head': '`tail.prev = head`',
        'self.tail.next = self.head': '`tail.next = head`',
        'if key not in self.cache': lambda S, B, ret: ('get({})：不在 cache 里 → 返回 -1'.format(S.key) if S.key not in B['self.cache']
                                                       else '==get({})==：命中 → 先删除，再插到链表尾部'.format(S.key)),
        'return -1': '返回 `-1`',
        36: 'dict 直接找到节点 `{node.key}:{node.val}`',
        37: '先把它从链表中删去',
        38: '再插入到链表的尾部（最近使用）',
        'return node.val': '返回 `{ret}`',
        'if key in self.cache': lambda S, B, ret: ('==put({}, {})==：已存在 → 更新 value，删掉后再插到尾部'.format(S.key, S.value) if S.key in B['self.cache']
                                                   else '==put({}, {})==：不存在'.format(S.key, S.value)),
        43: '找到旧节点',
        44: '更新 value = {value}',
        45: '从链表中删去',
        'if self.size == self.capacity': lambda S, B, ret: ('满了（`size` = {}）→ 删去链表的头部元素（最久未使用）'.format(B['self.size'])
                                                            if B['self.size'] == B['self.capacity'] else
                                                            '没满（`size` = {} < {}）→ 新建节点'.format(B['self.size'], B['self.capacity'])),
        'node = self.head.next': '`head.next` = `{node.key}:{node.val}`：最久未使用的就是它',
        49: '把它从链表中删去（节点对象还在内存里）',
        'self.cache.pop(node.key)': '从 dict 中删掉旧 key',
        'node.key = key': '==直接复用这个节点==：设置新的 key = {key}',
        52: '…和新的 value = {value}',
        'node = ListNode(key, value)': '新建节点 `{key}:{value}`',
        55: '记入 cache',
        'self.size += 1': '`size` = {self.size}',
        58: '`cache[{key}]` 指向这个节点',
        60: '最后都插入到链表的尾部（最近使用）',
        'node.prev.next = node.next': lambda S, B, ret: '删除节点只需两步 ①：`{}.next` 跳过它，指向 `{}`'.format(_nm(S, S.node.prev), _nm(S, S.node.next)),
        'node.next.prev = node.prev': lambda S, B, ret: '②：`{}.prev` 指回 `{}`；节点本身还没从内存删去'.format(_nm(S, S.node.next), _nm(S, S.node.prev)),
        'self.tail.prev.next = node': lambda S, B, ret: '插到尾部 ①：原来的最后一个 `{}` 的 `next` 指向 `node`'.format(_nm(S, S['self.tail'].prev)),
        'node.prev = self.tail.prev': lambda S, B, ret: '`node.prev` = `{}`'.format(_nm(S, S.node.prev)),
        'self.tail.prev = node': '`tail.prev = node`：它成为最近使用的',
        'node.next = self.tail': '`node.next = tail`：插入完成',
    },
    cards=dict(
        one_liner='dict 负责 O(1) 存取，双向链表负责 O(1) 找出最久未使用的 key',
        complexity='`get` / `put` 都是 `O(1)`，空间 `O(capacity)`',
        problem=['实现 `LRUCache(capacity)`、`get(key)`、`put(key, value)`',
                 '`get` 不存在返回 `-1`；`put` 超过容量时==逐出最久未使用==的 key',
                 '两个操作都要 `O(1)`'],
        quote='另一种思路就是维护一个队列，将新来的放在队列的尾部，同时将队列的头部踢出去。但是，遇到cache命中的情况，需要将队列中的某个值移动到队列的尾部，这种时候就需要链表的帮助了。',
        quote_src='—— yiduobo 题解',
        idea=['时间戳方案：要比较找最老的，做不到 `O(1)`',
              '队列：新来的放尾部、踢掉头部；命中时要把中间的移到尾部 ⇒ ==双向链表==',
              '删除 `now`：`now.prev.next = now.next`，`now.next.prev = now.prev`'],
        summary=['`get`、`put` 均 `O(1)`；链表头部 = 最久未使用，尾部 = 最近使用',
                 '假头 `head` + 假尾 `tail` 首尾相连，增删都不用判空',
                 '满了时==复用被淘汰的节点==：`pop` 旧 key，改 `key/val` 后插到尾部',
                 '原文为 Python 2 写法：仅删掉了 `"""type"""` 文档字符串和模板注释，逻辑未改'],
    ),
)
