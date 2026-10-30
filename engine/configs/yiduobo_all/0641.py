CODE = '''
class ListNode(object):

    def __init__(self, value):
        self.value = value
        self.left = self.right = None

class MyCircularDeque(object):

    def __init__(self, k):
        self.k = k
        self.l = 0
        self.head = ListNode(-1)
        self.tail = ListNode(-1)
        self.head.right = self.tail
        self.tail.left = self.head

    def insertFront(self, value):
        if self.l == self.k:
            return False

        self.l += 1
        node = ListNode(value)
        self.head.right.left = node
        node.right = self.head.right
        self.head.right = node
        node.left = self.head
        return True

    def insertLast(self, value):
        if self.l == self.k:
            return False

        self.l += 1
        node = ListNode(value)
        self.tail.left.right = node
        node.left = self.tail.left
        self.tail.left = node
        node.right = self.tail
        return True

    def deleteFront(self):
        if self.l == 0:
            return False

        self.l -= 1
        tmp = self.head.right
        self.head.right = tmp.right
        tmp.right.left = self.head
        del tmp
        return True

    def deleteLast(self):
        if self.l == 0:
            return False

        self.l -= 1
        tmp = self.tail.left
        self.tail.left = tmp.left
        tmp.left.right = self.tail
        del tmp
        return True

    def getFront(self):
        return self.head.right.value

    def getRear(self):
        return self.tail.left.value

    def isEmpty(self):
        return self.l == 0

    def isFull(self):
        return self.l == self.k
'''

_LINES = CODE.strip('\n').split('\n')


def _ln(sub, nth=0):
    return [i + 1 for i, s in enumerate(_LINES) if sub in s][nth]


_DEFS = [(i + 1, s.split('def ')[1].split('(')[0]) for i, s in enumerate(_LINES) if s.strip().startswith('def ')]
PTRS = {'node': 'pink', 'tmp': 'orange'}


def _method(S):
    ln = S.get('_line')
    return [nm for i, nm in _DEFS if i < ln][-1] if ln else ''


def _nm(S, n):
    if n is None:
        return None
    if n is S.get('self.head'):
        return 'head'
    if n is S.get('self.tail'):
        return 'tail'
    return str(n.value)


def _layout(S):
    """按 right 从 head 走，再按 left 从 tail 往回走补上漏掉的节点；都走不到的是悬空节点"""
    order, seen = [], set()
    x = S.get('self.head')
    while x is not None and id(x) not in seen and len(order) < 10:
        order.append(x)
        seen.add(id(x))
        x = x.right
    tail = S.get('self.tail')
    if tail is not None and id(tail) not in seen:
        order.append(tail)
        seen.add(id(tail))
    prev, x = tail, getattr(tail, 'left', None)
    while x is not None and len(order) < 12:
        if id(x) not in seen:
            order.insert(order.index(prev), x)
            seen.add(id(x))
        prev, x = x, x.left
        if prev is S.get('self.head'):
            break
    det = []
    for name in PTRS:
        v = S.get(name)
        if v is not None and hasattr(v, 'right') and id(v) not in seen:
            seen.add(id(v))
            det.append(v)
    return order, det


def _links(S):
    order, det = _layout(S)
    return {_nm(S, n): (_nm(S, n.right), _nm(S, n.left)) for n in order + det}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '双向链表（上方箭头 = right，下方箭头 = left；黄 = 这一步改的）', 24, T['muted'], bold=True)
    if S.get('self.head') is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    k, l = S.get('self.k'), S.get('self.l', 0)
    cv.text((x1 - 20, y0 + 44), f'l = {l} / k = {k}', 24, T['green'] if l < k else T['red'], anchor='ra', bold=True, mono=True)
    order, det = _layout(S)
    bl = _links(B) if B.get('self.head') is not None else {}
    gap = min(200, (x1 - x0 - 140) / max(4, len(order)))
    nw, nh = 100, 58
    Y = y0 + 200
    P = {}
    for i, n in enumerate(order):
        P[id(n)] = (x0 + 70 + nw / 2 + i * gap, Y)
    for n in det:
        anchors = [P[id(t)][0] for t in (n.left, n.right) if t is not None and id(t) in P]
        anchors += [P[id(m)][0] for m in order if m.left is n or m.right is n]
        X = sum(anchors) / len(anchors) if anchors else x0 + 70 + nw / 2 + len(order) * gap
        P[id(n)] = (X, Y + 170)

    def style(n, which):
        old = bl.get(_nm(S, n))
        new = _nm(S, getattr(n, which))
        if old is None:
            ch = bool(bl) and new is not None
        else:
            ch = old[0 if which == 'right' else 1] != new
        return (T['yellow'], 4) if ch else (T['muted'], 3)

    for i, n in enumerate(order):
        X, _ = P[id(n)]
        for which in ('right', 'left'):
            t = getattr(n, which)
            if t is None or id(t) not in P:
                continue
            c, w = style(n, which)
            X2, Y2 = P[id(t)]
            sg = 1 if which == 'right' else -1
            lane = -11 if which == 'right' else 11
            if Y2 == Y and 0 <= i + sg < len(order) and t is order[i + sg]:
                cv.arrow((X + sg * (nw / 2 + 2), Y + lane), (X2 - sg * (nw / 2 + 3), Y + lane), c, w, 11)
            elif Y2 == Y:
                if which == 'right':
                    cv.arc_arrow((X + nw * 0.25, Y - nh / 2 - 2), (X2 - nw * 0.25, Y - nh / 2 - 4), 84, c, w, 11)
                else:
                    cv.arc_arrow((X - nw * 0.25, Y + nh / 2 + 2), (X2 + nw * 0.25, Y + nh / 2 + 4), -48, c, w, 11)
            else:
                cv.dashed((X + sg * nw * 0.2, Y + nh / 2), (X2 - sg * nw * 0.2, Y2 - nh / 2), c, w)
    for n in det:
        X, Yd = P[id(n)]
        for which, sg in (('right', 1), ('left', -1)):
            t = getattr(n, which)
            if t is not None and id(t) in P:
                c, w = style(n, which)
                X2, Y2 = P[id(t)]
                p0 = (X + sg * nw * 0.3, Yd - nh / 2)
                p1 = (X2 - sg * nw * 0.1, Y2 + nh / 2 + 4)
                cv.dashed(p0, p1, c, w)
                cv.tri_up(p1[0], p1[1], 8, c)
                cv.text((p0[0] + (p1[0] - p0[0]) * 0.3 + sg * 10, p0[1] + (p1[1] - p0[1]) * 0.3), which, 17, c,
                        anchor='lm' if sg > 0 else 'rm')
    hit = {}
    for name, c in PTRS.items():
        v = S.get(name)
        if v is not None and id(v) in P:
            hit.setdefault(id(v), []).append((name, T[c]))
    for n in order + det:
        X, Yn = P[id(n)]
        nm = _nm(S, n)
        sent = nm in ('head', 'tail')
        hs = hit.get(id(n), [])
        fill = hs[0][1] if hs else ((52, 46, 70) if sent else T['panel2'])
        cv.rect((X - nw / 2, Yn - nh / 2, X + nw / 2, Yn + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
        cv.text((X, Yn - (8 if sent else 0)), nm, 22 if sent else 28, T['bg'] if hs else T['text'], anchor='mm', bold=True)
        if sent:
            cv.text((X, Yn + 15), 'value=-1', 15, T['purple'], anchor='mm', mono=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X, Yn - nh / 2 - 6 - r * 24), name, 20, cc, anchor='mb', bold=True)
    real = [n for n in order if _nm(S, n) not in ('head', 'tail')]
    if det:
        return
    if real and S['self.head'].right is real[0]:
        cv.text((P[id(real[0])][0], Y + nh / 2 + 66), '队首', 19, T['blue'], anchor='mt', bold=True)
    if real and S['self.tail'].left is real[-1]:
        cv.text((P[id(real[-1])][0], Y + nh / 2 + (90 if len(real) == 1 else 66)), '队尾', 19, T['pink'], anchor='mt', bold=True)


def _op(S):
    m = _method(S)
    if not m:
        return ''
    if m == '__init__':
        return f'正在执行：`MyCircularDeque({S.get("k", "")})`'
    return f'正在执行：`{m}({S["value"] if "value" in S else ""})`'


def _guard_ins(S, B, ret):
    l, k = S['self.l'], S['self.k']
    return (f'==' + _method(S) + f'({S.value})==：`l = {l}`，`k = {k}` → ' + ('已满，不能再插入' if l == k else '还有空位'))


def _guard_del(S, B, ret):
    l = S['self.l']
    return f'==' + _method(S) + f'()==：`l = {l}` → ' + ('队列为空，没有节点可删' if l == 0 else '有节点可删')


def _old(B, end, pre, post=''):
    n = B['self.head'].right if end == 'front' else B['self.tail'].left
    nm = _nm(B, n)
    if nm in ('head', 'tail'):
        who = f'`{"head.right" if end == "front" else "tail.left"}`（队列为空，就是哨兵 `{nm}`）'
    else:
        who = f'原{"队首" if end == "front" else "队尾"} `{nm}`'
    return pre + who + post


def _get(end):
    def f(S, B, ret):
        if S['self.l'] == 0:
            side = '`head.right` 就是 `tail`' if end == 'front' else '`tail.left` 就是 `head`'
            return f'==get{"Front" if end == "front" else "Rear"}()==：队列为空，{side}，哨兵的值是 `-1` → ==直接返回 -1=='
        return ('==getFront()==：队首 = `head.right`' if end == 'front' else '==getRear()==：队尾 = `tail.left`') + f' → 返回 =={ret}=='
    return f


CONFIG = dict(
    num=641, title='设计循环双端队列', difficulty='Medium', category='设计',
    author='yiduobo', technique='双向链表 + 头尾哨兵',
    tags=['labuladong', '灵神核心路线'],
    code=CODE,
    call='''d = MyCircularDeque(2)
[d.insertLast(1), d.insertFront(2), d.isFull(), d.insertFront(3), d.getRear(), d.deleteFront(), d.deleteLast(), d.getFront()]''',
    expect=[True, True, True, False, 1, True, True, -1],
    views=[
        dict(type='text', fn=_op, size=28, h=60),
        dict(type='custom', draw=_draw, h=440),
    ],
    watch=[('l', 'self.l', 'green'), ('k', 'self.k'), ('value', 'value')],
    skip=['self.value = value', 'self.left = self.right = None'],
    captions={
        'self.k = k': '`MyCircularDeque({self.k})`：容量 `k = {self.k}`',
        'self.l = 0': '`l` 记录当前元素个数',
        'self.head = ListNode(-1)': '哨兵 `head`：它的 `right` 永远是==队首==',
        'self.tail = ListNode(-1)': '哨兵 `tail`：它的 `left` 永远是==队尾==；两个哨兵的值都是 `-1`',
        'self.head.right = self.tail': '空队列：`head.right = tail`',
        'self.tail.left = self.head': '`tail.left = head`：两个哨兵互相指着',
        _ln('if self.l == self.k', 0): _guard_ins,
        _ln('if self.l == self.k', 1): _guard_ins,
        _ln('if self.l == 0', 0): _guard_del,
        _ln('if self.l == 0', 1): _guard_del,
        'return False': lambda S, B, ret: ('插入失败 → 返回 `False`' if 'value' in S else '删除失败 → 返回 `False`'),
        'self.l += 1': '元素个数 `l` → `{self.l}`',
        'node = ListNode(value)': '新建节点 `{value}`',
        'self.head.right.left = node': lambda S, B, ret: _old(B, 'front', '① ', ' 的 `left` 指向新节点'),
        'node.right = self.head.right': lambda S, B, ret: _old(B, 'front', '② `node.right` = '),
        'self.head.right = node': '③ `head.right = node`：新节点成为==队首==',
        'node.left = self.head': '④ `node.left = head`：头部插入完成',
        'self.tail.left.right = node': lambda S, B, ret: _old(B, 'rear', '① ', ' 的 `right` 指向新节点'),
        'node.left = self.tail.left': lambda S, B, ret: _old(B, 'rear', '② `node.left` = '),
        'self.tail.left = node': '③ `tail.left = node`：新节点成为==队尾==',
        'node.right = self.tail': '④ `node.right = tail`：尾部插入完成',
        'return True': '操作成功 → 返回 `True`',
        'self.l -= 1': '元素个数 `l` → `{self.l}`',
        'tmp = self.head.right': '`tmp` = 队首节点 `{tmp.value}`',
        'self.head.right = tmp.right': lambda S, B, ret: f'① `head.right` 跳过 `tmp`，直接指向 `{_nm(S, S["self.head"].right)}`',
        'tmp.right.left = self.head': lambda S, B, ret: f'② `{_nm(S, S.tmp.right)}.left` 指回 `head`：`tmp` 被摘下',
        'tmp = self.tail.left': '`tmp` = 队尾节点 `{tmp.value}`',
        'self.tail.left = tmp.left': lambda S, B, ret: f'① `tail.left` 跳过 `tmp`，直接指向 `{_nm(S, S["self.tail"].left)}`',
        'tmp.left.right = self.tail': lambda S, B, ret: f'② `{_nm(S, S.tmp.left)}.right` 指回 `tail`：`tmp` 被摘下',
        'del tmp': '`del tmp`：删除摘下的节点',
        'return self.head.right.value': _get('front'),
        'return self.tail.left.value': _get('rear'),
        'return self.l == 0': '==isEmpty()==：`l = {self.l}` → 返回 `{ret}`',
        'return self.l == self.k': '==isFull()==：`l = {self.l}`，`k = {self.k}` → 返回 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='操作只发生在两头：双向链表 + head / tail 两个哨兵',
        complexity='每个操作 `O(1)`，空间 `O(k)`',
        problem=['设计容量为 `k` 的双端队列：`insertFront` / `insertLast` 两头插入',
                 '`deleteFront` / `deleteLast` 两头删除，成功返回 `True`，否则 `False`',
                 '`getFront` / `getRear` 取两头元素（空时返回 `-1`），`isEmpty` / `isFull`',
                 '本视频：`k = 2`，尾插 1、头插 2 → 满了 → 删两头 → `getFront()` 得 `-1`'],
        quote='注意到这里所有的操作都跟队列头部或者队列尾部相关，那么只需要队列可以两头扩展或者删除就可以达成题目要求了，于是我们可以==使用双向链表来实现==。',
        quote_src='—— yiduobo 题解原文',
        idea=['维护 `head` 和 `tail`：`head` 的下一个是队首，`tail` 的上一个是队尾',
              '头部操作只涉及 `head` 和 `head.right`；尾部操作只涉及 `tail` 和 `tail.left`',
              '插入前判断是否已满，删除前判断是否有节点'],
        summary=['每个操作 `O(1)`：只改常数个指针',
                 '哨兵的值是 `-1`：队列为空时 `getFront` / `getRear` 自然返回 `-1`',
                 '插入时先把新节点和邻居连好，再改哨兵指针，避免丢掉原来的邻居',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
