PTRS = {'now': 'blue', 'node': 'pink', 'tmp': 'orange'}


def _name(S, n):
    if n is None:
        return None
    if n is S.get('self.head'):
        return 'head'
    if n is S.get('self.tail'):
        return 'tail'
    return str(n.val)


def _layout(S):
    head = S.get('self.head')
    if head is None:
        return [], []
    ring, x, seen = [], head, set()
    while x is not None and id(x) not in seen and len(ring) < 10:
        ring.append(x)
        seen.add(id(x))
        if x is S.get('self.tail'):
            break
        x = x.next
    det = []
    for name in PTRS:
        v = S.get(name)
        if v is not None and hasattr(v, 'prev') and id(v) not in seen:
            seen.add(id(v))
            det.append(v)
    return ring, det


def _links(S):
    ring, det = _layout(S)
    return {_name(S, n): (_name(S, n.next), _name(S, n.prev)) for n in ring + det}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '双向链表（上方箭头 = next，下方箭头 = prev，黄 = 这一步改的）', 24, T['muted'], bold=True)
    ring, det = _layout(S)
    if not ring:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    bl = _links(B) if B.get('self.head') is not None else {}
    L = len(ring)
    gap = min(200, (x1 - x0 - 100) / max(1, L))
    nw, nh = min(100, gap * 0.56), 52
    Y = y0 + 230
    P = {}
    for i, n in enumerate(ring):
        P[id(n)] = (x0 + 50 + nw / 2 + i * gap, Y)
    for k, n in enumerate(det):
        pv, nx = n.prev, n.next
        if pv is not None and nx is not None and id(pv) in P and id(nx) in P:
            X = (P[id(pv)][0] + P[id(nx)][0]) / 2
        elif nx is not None and id(nx) in P:
            X = P[id(nx)][0] - gap / 2
        elif pv is not None and id(pv) in P:
            X = P[id(pv)][0] + gap / 2
        else:
            X = x0 + 50 + nw / 2 + (L - 0.5 + k) * gap
        P[id(n)] = (min(max(X, x0 + 60), x1 - nw / 2 - 20), Y - 120)

    def changed(n, which):
        old = bl.get(_name(S, n))
        if old is None:
            return bool(bl) and getattr(n, which) is not None
        return old[0 if which == 'next' else 1] != _name(S, getattr(n, which))

    def style(n, which):
        return (T['yellow'], 4) if changed(n, which) else (T['muted'], 3)

    for i, n in enumerate(ring):
        X, _ = P[id(n)]
        if n.next is not None and i + 1 < L and n.next is ring[i + 1]:
            c, w = style(n, 'next')
            cv.arrow((X + nw / 2 + 2, Y - 10), (P[id(ring[i + 1])][0] - nw / 2 - 3, Y - 10), c, w, 11)
        elif n.next is not None and id(n.next) in P:
            c, w = style(n, 'next')
            X2, Y2 = P[id(n.next)]
            cv.dashed((X + nw * 0.25, Y - nh / 2), (X2 + nw * 0.1, Y2 + nh / 2), c, w)
            cv.text(((X + X2) / 2 + 12, (Y + Y2) / 2 + 6), 'next', 17, c, anchor='lm')
        if n.prev is not None and i >= 1 and n.prev is ring[i - 1]:
            c, w = style(n, 'prev')
            cv.arrow((X - nw / 2 - 2, Y + 10), (P[id(ring[i - 1])][0] + nw / 2 + 3, Y + 10), c, w, 11)
        elif n.prev is not None and id(n.prev) in P:
            c, w = style(n, 'prev')
            X2, Y2 = P[id(n.prev)]
            if Y2 == Y:
                cv.arc_arrow((X - nw * 0.2, Y + nh / 2 + 2), (X2 + nw * 0.2, Y2 + nh / 2 + 2), -50, c, w, 11)
            else:
                cv.dashed((X - nw * 0.25, Y - nh / 2), (X2 - nw * 0.1, Y2 + nh / 2), c, w)
                cv.text(((X + X2) / 2 - 12, (Y + Y2) / 2 + 6), 'prev', 17, c, anchor='rm')
    for n in det:
        X, Yd = P[id(n)]
        for which, sg in (('next', 1), ('prev', -1)):
            t = getattr(n, which)
            if t is not None and id(t) in P:
                c, w = style(n, which)
                X2, Y2 = P[id(t)]
                cv.dashed((X + sg * nw * 0.3, Yd + nh / 2), (X2 - sg * nw * 0.2, Y2 - nh / 2 - 2), c, w)
                cv.text((X + sg * nw * 0.3 + (X2 - X) * 0.35 + sg * 8, Yd + nh / 2 + 22), which, 17, c,
                        anchor='lm' if sg > 0 else 'rm')
    hit = {}
    for name, c in PTRS.items():
        v = S.get(name)
        if v is not None and id(v) in P:
            hit.setdefault(id(v), []).append((name, T[c]))
    for n in ring + det:
        X, Yn = P[id(n)]
        nm = _name(S, n)
        sent = nm in ('head', 'tail')
        hs = hit.get(id(n), [])
        fill = hs[0][1] if hs else ((52, 46, 70) if sent else T['panel2'])
        cv.rect((X - nw / 2, Yn - nh / 2, X + nw / 2, Yn + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
        cv.text((X, Yn), nm, 24 if not sent else 21, T['bg'] if hs else T['text'], anchor='mm', bold=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X, Yn - nh / 2 - 4 - r * 22), name, 19, cc, anchor='mb', bold=True)
    # 下标
    for i, n in enumerate(ring[1:-1]):
        X, _ = P[id(n)]
        cv.text((X, Y + nh / 2 + 34), f'[{i}]', 18, T['dim'], anchor='mt', mono=True)


_OP = {'op': ''}


def _op(name, text):
    def f(S, B, ret):
        _OP['op'] = name
        return text(S) if callable(text) else text
    return f


def _ret_now(S, B, ret):
    s = f'第 `{S.k}` 个节点是 `{ret.val}`'
    if _OP['op'] == 'get':
        s += f' → `get` 返回 =={ret.val}=='
    elif _OP['op'] == 'add':
        s += f' → 新节点要插到它前面'
    elif _OP['op'] == 'del':
        s += ' → 要删除的就是它'
    return s


def _find_cap(S, B, ret):
    k, ln = S.k, S['self.length']
    if k + 1 < ln - k:
        return f'从 head 走 `k+1 = {k + 1}` 步 < 从 tail 走 `length-k = {ln - k}` 步 → ==从 head 出发=='
    return f'从 head 走 `{k + 1}` 步 ≥ 从 tail 走 `length-k = {ln - k}` 步 → ==从 tail 往回走=='


CODE = '''
class Node(object):

    def __init__(self, val=0):
        self.val = val
        self.next = None
        self.prev = None

class MyLinkedList(object):

    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.length = 0

    def findIndex(self, k):
        if k + 1 < self.length - k:
            now = self.head
            for index in range(k + 1):
                now = now.next
        else:
            now = self.tail
            for index in range(self.length - k):
                now = now.prev

        return now

    def get(self, index):
        if index < 0 or index >= self.length:
            return -1

        return self.findIndex(index).val

    def addAtHead(self, val):
        node = Node(val)
        node.next = self.head.next
        self.head.next.prev = node
        node.prev = self.head
        self.head.next = node
        self.length += 1

    def addAtTail(self, val):
        node = Node(val)
        node.prev = self.tail.prev
        self.tail.prev.next = node
        node.next = self.tail
        self.tail.prev = node
        self.length += 1

    def addAtIndex(self, index, val):
        if index < 0:
            self.addAtHead(val)
        elif index == self.length:
            self.addAtTail(val)
        elif index > self.length:
            return
        else:
            tmp = self.findIndex(index)
            node = Node(val)
            tmp.prev.next = node
            node.prev = tmp.prev
            tmp.prev = node
            node.next = tmp
            self.length += 1

    def deleteAtIndex(self, index):
        if index >= 0 and index < self.length:
            tmp = self.findIndex(index)
            tmp.prev.next = tmp.next
            tmp.next.prev = tmp.prev
            del tmp
            self.length -= 1
'''

CONFIG = dict(
    num=707, title='设计链表', difficulty='Medium', category='设计',
    author='yiduobo', technique='双向链表 + 假头假尾',
    tags=['字节30天'],
    code=CODE,
    call='''obj = MyLinkedList()
obj.addAtHead(1)
obj.addAtTail(3)
obj.addAtIndex(1, 2)
r1 = obj.get(1)
obj.deleteAtIndex(1)
r2 = obj.get(1)
[r1, r2]''',
    expect=[2, 3],
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', label='正在执行的操作', hide=(), h=130),
    ],
    watch=[('length', 'self.length', 'green'), ('index', 'index'), ('k', 'k'), ('val', 'val')],
    skip=['self.val = val', 'self.next = None', 'self.prev = None'],
    captions={
        'self.head = Node()': '`MyLinkedList()`：建一个假头 `head`',
        'self.tail = Node()': '再建一个假尾 `tail`：头尾插入都不用判空',
        'self.head.next = self.tail': '初始状态下二者互联：`head.next = tail`',
        'self.tail.prev = self.head': '`tail.prev = head`',
        'self.length = 0': '`length` 记录真实节点个数',
        'if k + 1 < self.length - k': _find_cap,
        'now = self.head': '`now` 从 `head` 出发',
        'for index in range(k + 1)': lambda S, B, ret: ('往后走' if S.get('index') != B.get('index') or 'index' not in B else f'走完 `{S.k + 1}` 步'),
        'now = now.next': '`now` → `{now.val}`',
        'now = self.tail': '`now` 从 `tail` 出发',
        'for index in range(self.length - k)': lambda S, B, ret: ('往前走' if S.get('index') != B.get('index') or 'index' not in B else f'走完 `{S["self.length"] - S.k}` 步'),
        'now = now.prev': '`now` → `{now.val}`',
        'return now': _ret_now,
        'if index < 0 or index >= self.length': _op('get', lambda S: (f'`get({S.index})`：下标合法（0 ≤ {S.index} < {S["self.length"]}）' if 0 <= S.index < S['self.length'] else f'`get({S.index})`：下标非法 → -1')),
        'return self.findIndex(index).val': lambda S, B, ret: (f'找到第 `{S.index}` 个节点 → 返回 =={ret}==' if ret is not None else '先找到第 `{}` 个节点'.format(S.index)),
        'node = Node(val)': lambda S, B, ret: (_OP.update(op='') or f'新建节点 `{S.val}`'),
        'node.next = self.head.next': '头插：插到 `head` 与 `head.next` 之间 ① `node.next = head.next`',
        'self.head.next.prev = node': '② 原来的第一个节点的 `prev` 指向 `node`',
        'node.prev = self.head': '③ `node.prev = head`',
        'self.head.next = node': '④ `head.next = node`，插入完成',
        'self.length += 1': '`length` = {self.length}',
        'node.prev = self.tail.prev': '尾插：插到 `tail.prev` 与 `tail` 之间 ① `node.prev = tail.prev`',
        'self.tail.prev.next = node': '② 原来的最后一个节点的 `next` 指向 `node`',
        'node.next = self.tail': '③ `node.next = tail`',
        'self.tail.prev = node': '④ `tail.prev = node`，插入完成',
        'if index < 0:': _op('add', lambda S: f'`addAtIndex({S.index}, {S.val})`：`index` 不是负数'),
        'elif index == self.length': lambda S, B, ret: (f'`index = {S.index}` == length → 等价于尾插' if S.index == S['self.length'] else f'`index = {S.index}` ≠ length `{S["self.length"]}`'),
        'elif index > self.length': '`index` 没有越界 → 插到第 `{index}` 个节点前面',
        'tmp = self.findIndex(index)': lambda S, B, ret: (f'先找到第 `{S.index}` 个节点 `tmp = {S.tmp.val}`' if S.get('tmp') is not None else f'先找到第 `{S.index}` 个节点'),
        'tmp.prev.next = node': lambda S, B, ret: (f'① `tmp.prev`（`{S.tmp.prev.val}`）的 `next` 指向 `node`' if S.get('node') is not None and S.node.prev is None
                                                   else f'删除 ①：`{S.tmp.prev.val if S.tmp.prev is not S["self.head"] else "head"}.next` 跳过 `tmp`'),
        'node.prev = tmp.prev': '② `node.prev = tmp.prev`',
        'tmp.prev = node': '③ `tmp.prev = node`',
        'node.next = tmp': '④ `node.next = tmp`，插入完成',
        'if index >= 0 and index < self.length': _op('del', lambda S: f'`deleteAtIndex({S.index})`：下标合法'),
        'tmp.prev.next = tmp.next': lambda S, B, ret: '删除 ①：`tmp.prev.next = tmp.next`，前一个节点跳过 `{}`'.format(S.tmp.val),
        'tmp.next.prev = tmp.prev': '删除 ②：`tmp.next.prev = tmp.prev`，后一个节点也跳过它',
        'del tmp': '`del tmp`：只是删掉局部变量名，节点已经不在链表里了',
        'self.length -= 1': '`length` = {self.length}',
    },
    max_steps=80,
    cards=dict(
        one_liner='维护假头 head 和假尾 tail，增删都插在两个已有节点之间',
        complexity='`get`/`addAtIndex`/`deleteAtIndex` `O(min(k, n−k))`，头尾插入 `O(1)`',
        problem=['设计链表：`get(index)`、`addAtHead(val)`、`addAtTail(val)`',
                 '`addAtIndex(index, val)`：插到第 index 个节点之前（index == 长度时插到末尾）',
                 '`deleteAtIndex(index)`：下标有效才删除；`get` 无效时返回 -1',
                 '示例：头插 1、尾插 3、在 1 处插 2 → `get(1) = 2`；删掉下标 1 → `get(1) = 3`'],
        quote='因此==可以维护head节点和tail节点，初始状态下二者互联==。当要在头部插入时，就将新节点插入到head与head.next之间；当要在尾部插入时，则是插入到tail与tail.prev之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['双向链表 + 假头假尾：每个真实节点前后都有节点，不用判空',
              '`findIndex(k)`：看从 head 还是从 tail 走更近',
              '插入：改 4 个指针；删除：改 2 个指针'],
        summary=['头尾插入 `O(1)`；按下标操作最多走 `n/2` 步',
                 '插入的 4 步顺序要保证==不丢失原来的邻居==（先连新节点，再改旧节点）',
                 '`addAtIndex` 中 `index == length` 等价于尾插，`index > length` 不插',
                 '原文为 Python 2 风格：删去了文档字符串和末尾模板注释，代码未改'],
    ),
)
