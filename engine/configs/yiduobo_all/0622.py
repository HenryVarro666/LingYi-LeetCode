CODE = '''
class Node(object):

    def __init__(self, val):
        self.val = val
        self.next = None

class MyCircularQueue(object):

    def __init__(self, k):
        self.head = self.tail = None
        self.k = k
        self.cnt = 0

    def enQueue(self, value):
        if self.cnt == self.k:
            return False

        tmp = Node(value)
        if self.cnt == 0:
            self.head = self.tail = tmp
        else:
            self.tail.next = tmp
            self.tail = tmp
        self.cnt += 1
        return True

    def deQueue(self):
        if self.cnt == 0:
            return False

        tmp = self.head

        if self.cnt == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
        self.cnt -= 1
        del tmp
        return True

    def Front(self):
        if self.head:
            return self.head.val
        return -1

    def Rear(self):
        if self.tail:
            return self.tail.val
        return -1

    def isEmpty(self):
        return self.cnt == 0

    def isFull(self):
        return self.cnt == self.k
'''

_LINES = CODE.strip('\n').split('\n')


def _ln(sub, nth=0):
    hits = [i + 1 for i, s in enumerate(_LINES) if sub in s]
    return hits[nth]


ENQ_IF0, DEQ_IF0 = _ln('if self.cnt == 0:', 0), _ln('if self.cnt == 0:', 1)
PTRS = (('self.head', 'head', 'blue'), ('self.tail', 'tail', 'pink'), ('tmp', 'tmp', 'orange'))


def _nm(n):
    return None if n is None else str(n.val)


def _layout(S):
    order, seen, x = [], set(), S.get('self.head')
    while x is not None and id(x) not in seen and len(order) < 8:
        order.append(x)
        seen.add(id(x))
        x = x.next
    det = []
    for name in ('self.tail', 'tmp'):
        v = S.get(name)
        if v is not None and hasattr(v, 'next') and id(v) not in seen:
            seen.add(id(v))
            det.append(v)
    return order, det


def _links(S):
    order, det = _layout(S)
    return {_nm(n): _nm(n.next) for n in order + det}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '单链表（虚线框 = 容量 k 个位置；黄 = 这一步改的）', 24, T['muted'], bold=True)
    k = S.get('self.k')
    if k is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    cnt = S.get('self.cnt', 0)
    cv.text((x1 - 20, y0 + 6), f'cnt = {cnt} / k = {k}', 24, T['green'] if cnt < k else T['red'], anchor='ra', bold=True, mono=True)
    order, det = _layout(S)
    bl = _links(B)
    gap = 190
    nw, nh = 100, 60
    Y = y0 + 210
    sx = x0 + 80 + nw / 2

    def slot(i):
        return sx + i * gap

    for i in range(max(k, len(order))):
        cv.rect((slot(i) - nw / 2 - 10, Y - nh / 2 - 10, slot(i) + nw / 2 + 10, Y + nh / 2 + 10),
                outline=T['border'], width=2, r=12)
        cv.text((slot(i), Y + nh / 2 + 16), f'位置 {i}', 17, T['dim'], anchor='mt')
    P = {}
    for i, n in enumerate(order):
        P[id(n)] = (slot(i), Y)
    for n in det:
        nx = n.next
        X = P[id(nx)][0] if nx is not None and id(nx) in P else slot(len(order) if n is not S.get('tmp') or 'value' in S else 0)
        P[id(n)] = (X, Y + 150)
    for n in order + det:
        X, Yn = P[id(n)]
        ch = bl.get(_nm(n), _nm(n.next)) != _nm(n.next) or (_nm(n) not in bl and n.next is not None)
        c, w = (T['yellow'], 4) if ch else (T['muted'], 3)
        nx = n.next
        if nx is None:
            cv.text((X + nw / 2 + 8, Yn), '∅', 22, T['dim'], anchor='lm')
        elif id(nx) in P:
            X2, Y2 = P[id(nx)]
            if Y2 == Yn:
                cv.arrow((X + nw / 2 + 2, Yn), (X2 - nw / 2 - 3, Y2), c, w, 12)
            else:
                cv.dashed((X + 36, Yn - nh / 2), (X2 + 36, Y2 + nh / 2 + 46), c, w)
                cv.tri_up(X2 + 36, Y2 + nh / 2 + 40, 9, c)
                cv.text((X + 48, (Yn + Y2) / 2 + 20), 'next', 17, c, anchor='lm')
    hit = {}
    for var, lab, col in PTRS:
        v = S.get(var)
        if v is not None and id(v) in P:
            moved = (B.get(var) is None) or _nm(B.get(var)) != _nm(v)
            hit.setdefault(id(v), []).append((lab, T[col], moved))
    for n in order + det:
        X, Yn = P[id(n)]
        hs = hit.get(id(n), [])
        fill = hs[0][1] if hs else T['panel2']
        cv.rect((X - nw / 2, Yn - nh / 2, X + nw / 2, Yn + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
        cv.text((X, Yn), n.val, 28, T['bg'] if hs else T['text'], anchor='mm', bold=True)
        for r, (lab, cc, moved) in enumerate(hs):
            cv.text((X, Yn - nh / 2 - 6 - r * 26), lab, 21,
                    T['yellow'] if moved and lab != 'tmp' else cc, anchor='mb', bold=True)
    nones = [lab for var, lab, _ in PTRS[:2] if S.get(var) is None]
    if nones:
        cv.text((x0 + 18, y0 + 44), '   '.join(f'{lab} = None' for lab in nones), 22, T['muted'], mono=True)


_DEFS = [(i + 1, s.split('def ')[1].split('(')[0]) for i, s in enumerate(_LINES) if s.strip().startswith('def ')]


def _op(S):
    ln = S.get('_line')
    if ln is None:
        return ''
    name = [nm for i, nm in _DEFS if i < ln][-1]
    if name == '__init__':
        return f'正在执行：`MyCircularQueue({S.get("k", "")})`'
    arg = S['value'] if name == 'enQueue' and 'value' in S else ''
    return f'正在执行：`{name}({arg})`'


def _guard_en(S, B, ret):
    full = S['self.cnt'] == S['self.k']
    return (f'==enQueue({S.value})==：`cnt = {S["self.cnt"]}`，`k = {S["self.k"]}` → '
            + ('队列已满' if full else '还有空位'))


def _guard_de(S, B, ret):
    return f'==deQueue()==：`cnt = {S["self.cnt"]}` → ' + ('队列为空' if S['self.cnt'] == 0 else '有元素可删')


CONFIG = dict(
    num=622, title='设计循环队列', difficulty='Medium', category='设计',
    author='yiduobo', technique='单链表维护头尾节点',
    tags=['labuladong', '灵神核心路线'],
    code=CODE,
    call='''q = MyCircularQueue(2)
[q.enQueue(1), q.enQueue(2), q.enQueue(3), q.Front(), q.deQueue(), q.deQueue(), q.Rear(), q.isEmpty()]''',
    expect=[True, True, False, 1, True, True, -1, True],
    views=[
        dict(type='text', fn=_op, size=28, h=60),
        dict(type='custom', draw=_draw, h=380),
    ],
    watch=[('cnt', 'self.cnt', 'green'), ('k', 'self.k'), ('value', 'value')],
    skip=['self.val = val', 'self.next = None'],
    captions={
        _ln('self.head = self.tail = None', 0): '`MyCircularQueue(2)`：一开始头尾节点都为空',
        'self.k = k': '容量 `k = {self.k}`',
        'self.cnt = 0': '`cnt` 记录当前元素个数，用它判断空和满',
        'if self.cnt == self.k': _guard_en,
        'return False': lambda S, B, ret: ('满了，插入失败 → 返回 `False`' if 'value' in S else '空的，没东西可删 → 返回 `False`'),
        'tmp = Node(value)': '新建节点 `{value}`',
        ENQ_IF0: lambda S, B, ret: ('链表为空 → 新节点==既是头也是尾==' if S['self.cnt'] == 0
                                    else '链表不空 → 接在尾节点后面'),
        'self.head = self.tail = tmp': '`head = tail = tmp`',
        'self.tail.next = tmp': '尾节点 `{B["self.tail"].val}` 的 `next` 指向新节点',
        'self.tail = tmp': '`tail` 移到新节点 `{tmp.val}`：==入队在尾部==',
        'self.cnt += 1': '`cnt` → `{self.cnt}`',
        'return True': '操作成功 → 返回 `True`',
        DEQ_IF0: _guard_de,
        'tmp = self.head': '`tmp` 记下要删的头节点 `{tmp.val}`',
        'if self.cnt == 1': lambda S, B, ret: ('只剩一个元素 → 删完后==头尾都要置空==' if S['self.cnt'] == 1
                                               else f'有 `{S["self.cnt"]}` 个元素 → 头节点后移即可'),
        _ln('self.head = self.tail = None', 1): '`head = tail = None`：链表变空',
        'self.head = self.head.next': '`head` 后移到 `{self.head.val}`：==出队在头部==',
        'self.cnt -= 1': '`cnt` → `{self.cnt}`',
        'del tmp': '`del tmp`：删去原先的头节点',
        'if self.head:': lambda S, B, ret: (f'==Front()==：`head` 不为空' if S['self.head'] else '==Front()==：`head` 为空'),
        'return self.head.val': '返回队首 =={ret}==',
        'if self.tail:': lambda S, B, ret: (f'==Rear()==：`tail` 不为空' if S['self.tail'] else '==Rear()==：`tail` 为空 → 队列是空的'),
        'return self.tail.val': '返回队尾 =={ret}==',
        'return -1': '队列为空 → 返回 `-1`',
        'return self.cnt == 0': '==isEmpty()==：`cnt = {self.cnt}` → 返回 `{ret}`',
        'return self.cnt == self.k': '==isFull()==：`cnt = {self.cnt}`，`k = {self.k}` → 返回 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='不必真的「循环」：用单链表维护队首和队尾两个节点',
        complexity='每个操作 `O(1)`，空间 `O(k)`',
        problem=['设计容量为 `k` 的队列：`enQueue` 入队、`deQueue` 出队（成功返回 `True`）',
                 '`Front` / `Rear` 取队首 / 队尾，队列为空时返回 `-1`',
                 '`isEmpty` / `isFull` 判断空 / 满',
                 '本视频：`k = 2`，入队 1、2、3（失败）→ 两次出队 → `Rear()` 返回 `-1`'],
        quote='由于题目没有要求我们展现出“循环”这个性质，因此我们只需要想办法维护住队首和队尾即可，而最简单的做法就是==维护一条单链表的头尾节点==。',
        quote_src='—— yiduobo 题解原文',
        idea=['先进先出：插入看==队尾==，删除看==队首==',
              '插入：链表为空就让头尾都指向新节点，否则接到尾节点后面',
              '删除：只剩一个元素就把头尾都置空，否则头节点后移'],
        summary=['每个操作 `O(1)`；`cnt` 和 `k` 比较判断空 / 满',
                 '易错：删最后一个元素时 `tail` 也要置空，否则 `Rear()` 会返回旧值',
                 '常见的另一种写法：长度为 `k` 的数组 + 头指针，下标对 `k` 取模',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
