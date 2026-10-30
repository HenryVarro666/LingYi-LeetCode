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
    if n is S.get('self.dummy'):
        return 'dummy'
    return f'{n.key}:{n.value}' if n is not None else 'None'


CONFIG = dict(
    num='面试题 16.25', title='LRU 缓存', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='哈希表 + 双向链表（一个哨兵）',
    code="""
class Node:
    # 提高访问属性的速度，并节省内存
    __slots__ = 'prev', 'next', 'key', 'value'

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.dummy = Node()  # 哨兵节点
        self.dummy.prev = self.dummy
        self.dummy.next = self.dummy
        self.key_to_node = dict()

    def get_node(self, key: int) -> Optional[Node]:
        if key not in self.key_to_node:  # 没有这本书
            return None
        node = self.key_to_node[key]  # 有这本书
        self.remove(node)  # 把这本书抽出来
        self.push_front(node)  # 放在最上面
        return node

    def get(self, key: int) -> int:
        node = self.get_node(key)
        return node.value if node else -1

    def put(self, key: int, value: int) -> None:
        node = self.get_node(key)
        if node:  # 有这本书
            node.value = value  # 更新 value
            return
        self.key_to_node[key] = node = Node(key, value)  # 新书
        self.push_front(node)  # 放在最上面
        if len(self.key_to_node) > self.capacity:  # 书太多了
            back_node = self.dummy.prev
            del self.key_to_node[back_node.key]
            self.remove(back_node)  # 去掉最后一本书

    # 删除一个节点（抽出一本书）
    def remove(self, x: Node) -> None:
        x.prev.next = x.next
        x.next.prev = x.prev

    # 在链表头添加一个节点（把一本书放在最上面）
    def push_front(self, x: Node) -> None:
        x.prev = self.dummy
        x.next = self.dummy.next
        x.prev.next = x
        x.next.prev = x
""",
    call="""c = LRUCache(2)
c.put(1, 1)
c.put(2, 2)
c.get(1)
c.put(3, 3)
c.get(2)""",
    expect=-1,
    views=[
        dict(type='custom', draw=_lru_view('self.dummy', {'self.dummy': 'dummy'},
                                           {'node': 'pink', 'x': 'blue', 'back_node': 'red'},
                                           '书堆（双向循环链表，上车道 next、下车道 prev；黄色 = 这一步改的）',
                                           '从左到右：dummy → 最上面（最近用过）→ … → 最下面（最久没用）→ 回到 dummy'), h=380),
        dict(type='map', var='self.key_to_node', label='key_to_node（key → 书）', fmt=lambda k, v: f'{k} → {v.key}:{v.value}', h=95),
        dict(type='calls', label='正在执行', h=155),
    ],
    watch=['key', 'value', ('书的数量', 'len(self.key_to_node)'), ('capacity', 'self.capacity')],
    skip=['self.key = key', 'self.value = value'],
    captions={
        'self.capacity = capacity': '`LRUCache({capacity})`：最多放 `{capacity}` 本书',
        'self.dummy = Node()': '只用==一个==哨兵 `dummy`',
        'self.dummy.prev = self.dummy': '一开始 `dummy` 的 `prev`、`next` 都指向自己',
        'self.dummy.next = self.dummy': '以后 `dummy.next` 是最上面的书，`dummy.prev` 是最下面的书',
        'self.key_to_node = dict()': '哈希表：`key` → 节点，`O(1)` 找到书',
        26: '==get({key})==：`get_node` 找书，找到就顺便移到最上面',
        30: '==put({key}, {value})==：先用 `get_node` 看看有没有这本书',
        'if key not in self.key_to_node': lambda S, B, ret: ('没有 `{}` 这本书'.format(S.key) if S.key not in B['self.key_to_node']
                                                             else '有 `{}` 这本书'.format(S.key)),
        'return None': '返回 `None`',
        'node = self.key_to_node[key]': '哈希表直接拿到节点 `{node.key}:{node.value}`',
        'self.remove(node)  # 把这本书抽出来': '把这本书==抽出来==',
        22: '再==放到最上面==',
        23: '返回这本书的节点',
        'return node.value if node else -1': lambda S, B, ret: '返回 `{}`'.format(ret) + ('（没找到）' if ret == -1 else ''),
        'if node:': lambda S, B, ret: '有这本书 → 只更新 value' if B.node else '没有这本书 → 新建',
        'node.value = value': '更新 `value` = {value}',
        'self.key_to_node[key] = node = Node(key, value)': '新书 `{key}:{value}`：建节点、记进哈希表',
        35: '新书==放到最上面==',
        'if len(self.key_to_node) > self.capacity': lambda S, B, ret: ('书太多了：{} 本 > `capacity` = {}'.format(len(B['self.key_to_node']), B['self.capacity'])
                                                                       if len(B['self.key_to_node']) > B['self.capacity'] else
                                                                       '{} 本 ≤ `capacity` = {}，不用删'.format(len(B['self.key_to_node']), B['self.capacity'])),
        'back_node = self.dummy.prev': '最下面的书 = `dummy.prev` = `{back_node.key}:{back_node.value}`（最久没用）',
        'del self.key_to_node[back_node.key]': '节点里存了 `key`，才能从哈希表里删掉它（`del [{back_node.key}]`）',
        'self.remove(back_node)': '把最后一本书从链表里去掉',
        'x.prev.next = x.next': lambda S, B, ret: '左边邻居 `{}` 的 `next` 跳过 `x`，直接指向 `{}`'.format(_nm(S, S.x.prev), _nm(S, S.x.next)),
        'x.next.prev = x.prev': lambda S, B, ret: '右边邻居 `{}` 的 `prev` 跳过 `x`，指回 `{}`：`x` ==被抽出=='.format(_nm(S, S.x.next), _nm(S, S.x.prev)),
        'x.prev = self.dummy': '`x.prev = dummy`',
        'x.next = self.dummy.next': lambda S, B, ret: '`x.next` = 原来最上面的书（{}）'.format(_nm(S, S.x.next)),
        'x.prev.next = x': '`dummy.next = x`：`x` 成为最上面的书',
        'x.next.prev = x': lambda S, B, ret: '`{}` 的 `prev` 指回 `x`：插入完成'.format(_nm(S, S.x.next)),
    },
    cards=dict(
        one_liner='一摞书：用到的书抽出来放最上面，书太多就扔掉最下面那本',
        complexity='`get` / `put` 都是 `O(1)`；空间 `O(min(p, capacity))`',
        problem=['实现 `LRUCache(capacity)`、`get(key)`、`put(key, value)`',
                 '`get` 不存在返回 `-1`；`put` 超过容量时==逐出最久未使用==的 key',
                 '两个操作都要 `O(1)`'],
        quote='需要几个哨兵节点？一个就够了。……随着节点的插入，dummy 的 next 指向链表的第一个节点（最上面的书），prev 指向链表的最后一个节点（最下面的书）。',
        quote_src='—— 灵茶山艾府题解答疑',
        idea=['哈希表 `key → 节点`：`O(1)` 找到书；双向链表：`O(1)` 抽出、放顶',
              '`get` 和 `put` 都先 `get_node`：找到就==抽出来放到最上面==',
              '为什么节点要存 `key`？删最下面的书时，要同时删哈希表里的记录'],
        summary=['`get`、`put` 均 `O(1)`：哈希表定位 + 双向链表增删',
                 '只需一个哨兵：`dummy.next` 是最上面，`dummy.prev` 是最下面',
                 '易错：删除时别忘了 `del key_to_node[back_node.key]`',
                 '相似题：460. LFU 缓存（每个频次一条链表）'],
    ),
)
