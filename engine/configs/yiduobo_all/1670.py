def _walk(ll):
    out, n = [], ll.head.next
    while n is not None and n is not ll.tail and len(out) < 12:
        out.append(n.val)
        n = n.next
    return out


def _qs(S):
    l, r = S.get('self.left'), S.get('self.right')
    if l is None or r is None or not hasattr(l, 'head') or not hasattr(r, 'head'):
        return None, None
    return _walk(l), _walk(r)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L, R = _qs(S)
    if L is None:
        cv.text((x0 + 18, y0 + 4), '队列尚未创建', 24, T['muted'], bold=True)
        return
    Lb, Rb = _qs(B)
    cv.text((x0 + 18, y0 + 4), '左右两条双向链表（各带 head / tail 哨兵），保证 left 不长于 right', 24, T['muted'], bold=True)
    old = set(Lb or []) | set(Rb or [])
    cell, gap = 84, 56
    n = len(L) + len(R)
    sx = x0 + max(20, ((x1 - x0) - (n * cell + gap + 4 * 60)) / 2)
    Y = y0 + 150
    x = sx
    for name, arr, col in (('left', L, 'blue'), ('right', R, 'pink')):
        cv.text((x + 28, Y), 'head', 18, T['dim'], anchor='mm', mono=True)
        x += 56
        w = max(len(arr), 1) * cell
        cv.text((x + w / 2, Y - 62), f'{name}（cnt={len(arr)}）', 22, T[col], anchor='mm', bold=True)
        if not arr:
            cv.rect((x + 4, Y - 32, x + cell - 4, Y + 32), fill=None, outline=T['border'], width=2, r=8)
            cv.text((x + cell / 2, Y), '空', 22, T['dim'], anchor='mm')
            x += cell
        for v in arr:
            fill = T['yellow'] if v not in old else T['panel2']
            cv.rect((x + 4, Y - 32, x + cell - 4, Y + 32), fill=fill, r=8, outline=T['border'], width=2)
            cv.text((x + cell / 2, Y), v, 28, T['bg'] if v not in old else T['text'], anchor='mm', bold=True, mono=True)
            x += cell
        cv.text((x + 28, Y), 'tail', 18, T['dim'], anchor='mm', mono=True)
        x += 56
        if name == 'left':
            cv.line([(x + gap / 2, Y - 50), (x + gap / 2, Y + 50)], T['purple'], 4)
            x += gap
    full = L + R
    cv.text((x0 + 18, Y + 110), '完整队列：' + (' → '.join(map(str, full)) if full else '空'), 24, T['text'])
    hand = S.get('node')
    if hand is not None and hasattr(hand, 'val') and hand.val not in L + R and hand.val != 0:
        cv.text((x0 + 18, y0 + 44), f'手里的节点：{hand.val}（刚创建 / 刚摘下，还没挂上去）', 22, T['orange'])



CONFIG = dict(
    num=1670, title='设计前中后队列', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='手写双向链表 · 左右两段',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1610'],
    code='''
class Node(object):

    def __init__(self, val):
        self.next = None
        self.prev = None
        self.val = val

class LinkedList(object):

    def __init__(self):
        self.head = Node(0)
        self.tail = Node(0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cnt = 0
    
    def addHead(self, node):
        self.head.next.prev = node
        node.next = self.head.next
        self.head.next = node
        node.prev = self.head
        self.cnt += 1
    
    def addTail(self, node):
        self.tail.prev.next = node
        node.prev = self.tail.prev
        self.tail.prev = node
        node.next = self.tail
        self.cnt += 1
    
    def removeHead(self):
        if self.cnt > 0:
            node = self.head.next
            self.head.next = node.next
            node.next.prev = self.head
            self.cnt -= 1
            return node
        
        return None
    
    def removeTail(self):
        if self.cnt > 0:
            node = self.tail.prev
            self.tail.prev = node.prev
            node.prev.next = self.tail
            self.cnt -= 1
            return node
        
        return None

class FrontMiddleBackQueue(object):

    def __init__(self):
        self.left = LinkedList()
        self.right = LinkedList()

    def pushFront(self, val):
        node = Node(val)
        self.left.addHead(node)
        if self.left.cnt > self.right.cnt:
            node = self.left.removeTail()
            self.right.addHead(node)

    def pushMiddle(self, val):
        node = Node(val)
        if self.left.cnt < self.right.cnt:
            self.left.addTail(node)
        else:
            self.right.addHead(node)

    def pushBack(self, val):
        node = Node(val)
        self.right.addTail(node)
        if self.right.cnt - self.left.cnt == 2:
            node = self.right.removeHead()
            self.left.addTail(node)

    def popFront(self):
        if self.left.cnt > 0:
            res = self.left.removeHead().val
            if self.right.cnt - self.left.cnt == 2:
               node = self.right.removeHead()
               self.left.addTail(node)
            return res

        elif self.right.cnt > 0:
            return self.right.removeHead().val
        
        else:
            return -1

    def popMiddle(self):
        if self.left.cnt == self.right.cnt:
            if self.left.cnt == 0:
                return -1
            else:
                return self.left.removeTail().val
        
        else:
            return self.right.removeHead().val

    def popBack(self):
        if self.right.cnt == 0:
            return -1
        
        res = self.right.removeTail().val
        if self.right.cnt < self.left.cnt:
            node = self.left.removeTail()
            self.right.addHead(node)
        
        return res
''',
    call='''q = FrontMiddleBackQueue()
res = [q.pushFront(1), q.pushBack(2), q.pushMiddle(3), q.pushMiddle(4), q.popFront(), q.popMiddle(), q.popMiddle(), q.popBack(), q.popFront()]
res''',
    expect=[None, None, None, None, 1, 3, 4, 2, -1],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=[('left.cnt', 'self.left.cnt', 'blue'), ('right.cnt', 'self.right.cnt', 'pink')],
    skip=['self.next = None', 'self.prev = None', 'self.val = val',
          'self.head.next.prev = node', 'node.next = self.head.next', 'self.head.next = node', 'node.prev = self.head',
          'self.tail.prev.next = node', 'node.prev = self.tail.prev', 'self.tail.prev = node', 'node.next = self.tail',
          'node = self.head.next', 'node.next.prev = self.head', 'node = self.tail.prev', 'node.prev.next = self.tail'],
    captions={
        11: '每条链表有两个==哨兵== `head`、`tail`，增删头尾时不用判空',
        12: '另一个哨兵 `tail`',
        13: '`head.next = tail`：两个哨兵先互相连起来',
        14: '`tail.prev = head`：反向也连上，空链表 = 只有两个哨兵',
        15: '`cnt` 记录这条链表有几个节点',
        54: '`left`：前半段，用一条手写双向链表',
        55: '`right`：后半段。约定 `left` 的长度 <= `right` 的长度',
        58: '`pushFront({val})`：先建节点，加到 `left` 头部',
        59: '`left.addHead`：节点挂到 `head` 后面（`prev / next` 四个指针重连）',
        22: '`addHead` 完成：挂到头部，`cnt` → {self.cnt}',
        29: '`addTail` 完成：挂到尾部，`cnt` → {self.cnt}',
        60: lambda S, B, r: ('`left` 变长了（`{} > {}`）→ 违反约定' .format(S.self.left.cnt, S.self.right.cnt) if S.self.left.cnt > S.self.right.cnt else '`left` 没超过 `right`，不用调整'),
        61: '把 `left` 的末尾节点摘下来……',
        62: '……放到 `right` 的头部：中点向左移一格',
        65: '`pushMiddle({val})`：先建节点',
        66: lambda S, B, r: ('`left` 比 `right` 短（`{} < {}`）→ 放到 `left` 末尾，正好是中间'.format(S.self.left.cnt, S.self.right.cnt) if S.self.left.cnt < S.self.right.cnt
                             else '两段一样长（`{} = {}`）→ 放到 `right` 头部，是中间靠前的位置'.format(S.self.left.cnt, S.self.right.cnt)),
        67: '放到 `left` 末尾',
        69: '放到 `right` 头部',
        72: '`pushBack({val})`：先建节点',
        73: '加到 `right` 的尾部',
        74: lambda S, B, r: ('`right` 比 `left` 多了 2 个 → 需要匀一个给 `left`' if S.self.right.cnt - S.self.left.cnt == 2 else '`right` 只多 {} 个，合法'.format(S.self.right.cnt - S.self.left.cnt)),
        75: '把 `right` 的头节点摘下来……',
        76: '……接到 `left` 的末尾：中点向右移一格',
        79: lambda S, B, r: ('`popFront`：`left` 不空 → 队首在 `left` 头部' if S.self.left.cnt > 0 else '`popFront`：`left` 空了'),
        80: '摘下 `left` 的头节点，取出它的值 `res`',
        81: lambda S, B, r: ('弹出后 `right` 比 `left` 多 2 个 → 要匀一个' if S.self.right.cnt - S.self.left.cnt == 2 else '弹出后长度仍合法（`right` 比 `left` 多 {} 个）'.format(S.self.right.cnt - S.self.left.cnt)),
        84: '返回 `{res}`',
        86: lambda S, B, r: ('`left` 空但 `right` 有 1 个 → 队首在 `right` 头部' if S.self.right.cnt > 0 else '两段都空 → 没有可弹的'),
        87: '摘下 `right` 头节点，返回它的值',
        90: '队列为空，返回 `-1`',
        93: lambda S, B, r: ('两段一样长 → 中间元素是 `left` 的末尾（靠前的那个）' if S.self.left.cnt == S.self.right.cnt else '`right` 多一个 → 中间元素是 `right` 的头部'),
        94: lambda S, B, r: ('两段都是空 → 返回 `-1`' if S.self.left.cnt == 0 else '`left` 不空，弹它的末尾'),
        97: '摘下 `left` 末尾节点，返回它的值',
        100: '摘下 `right` 头节点，返回它的值',
        103: lambda S, B, r: ('`right` 空 → 整个队列空，返回 `-1`' if S.self.right.cnt == 0 else '`popBack`：队尾在 `right` 末尾'),
        106: '摘下 `right` 的末尾节点，取出值 `res`',
        107: lambda S, B, r: ('`right` 比 `left` 短了 → 违反约定，要把 `left` 末尾挪过来' if S.self.right.cnt < S.self.left.cnt else '长度仍合法，不用调整'),
        111: '返回 `{res}`',
        32: lambda S, B, r: '`removeHead`：链表不空，摘头节点' if S.self.cnt > 0 else '链表空，返回 `None`',
        42: lambda S, B, r: '`removeTail`：链表不空，摘尾节点' if S.self.cnt > 0 else '链表空，返回 `None`',
        36: '摘下头节点：`cnt` → {self.cnt}',
        46: '摘下尾节点：`cnt` → {self.cnt}',
    },
    cards=dict(
        one_liner='和数据流中位数一样拆两半：两条双向链表，左不长于右',
        complexity='所有操作 `O(1)`，空间 `O(q)`',
        problem=['设计队列，支持在==前、中、后==三个位置 push 和 pop',
                 '有两个中间位置时选靠前的；队列为空时 pop 返回 `-1`',
                 '示例：`pushFront(1)`、`pushBack(2)`、`pushMiddle(3)`、`pushMiddle(4)`，再依次 pop 前、中、中、后、前 → `1, 3, 4, 2, -1`'],
        quote='本题与之前的某一题数据流的中位数很类似，在这里同样是拆成两个部分。对于这两个部分都需要双端的插入和弹出操作，因此可以使用分别维护两个双端队列。',
        quote_src='—— yiduobo 题解原文',
        idea=['和「数据流的中位数」一样拆成左右两段，默认 ==左侧长度 <= 右侧长度==',
              '操作后若左比右长，就把左侧末尾弹出插到右侧头部；中间操作按两段长度决定放哪边',
              '作者没有用现成的 deque，而是手写带哨兵的双向链表：头尾增删都是 `O(1)`'],
        summary=['所有操作 `O(1)`，空间 `O(q)`',
                 '易错：`popFront` 时 `left` 可能为空（只剩一个元素在 `right`）；弹出后 `right` 可能比 `left` 多 2 个，要匀回去',
                 '`pushBack` 后 `right - left == 2` 时，把 `right` 头节点挪到 `left` 末尾',
                 '原文为 Python 2 写法，无除法等需改动，保持不变；对比灵神：直接用 deque，并抽出 `balance` 统一调整'],
    ),
)
