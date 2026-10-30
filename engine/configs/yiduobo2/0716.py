CODE = '''
import random

class Node(object):

    def __init__(self, v=(-(10**7) - 1, -1), key=-1, fa=None):
        self.v = v
        self.key = key
        self.fa = fa
        self.left = None
        self.right = None

class Treap(object):

    def __init__(self):
        self.root = Node()
        self.ma = self.root.v

    def leftRotate(self, now):
        fa = now.fa
        fa.right = now.left
        if now.left:
            now.left.fa = fa
        now.left = fa

        g_fa = fa.fa
        if fa == g_fa.left:
            g_fa.left = now
        else:
            g_fa.right = now

        now.fa = g_fa
        fa.fa = now

    def rightRotate(self, now):
        fa = now.fa
        fa.left = now.right
        if now.right:
            now.right.fa = fa
        now.right = fa

        g_fa = fa.fa
        if fa == g_fa.left:
            g_fa.left = now
        else:
            g_fa.right = now

        now.fa = g_fa
        fa.fa = now

    def insert(self, v):
        now = self.root
        while True:
            if v < now.v:
                if now.left:
                    now = now.left
                else:
                    node = Node(v, random.randint(0, 2147483647), now)
                    now.left = node
                    now = node
                    break
            else:
                if now.right:
                    now = now.right
                else:
                    node = Node(v, random.randint(0, 2147483647), now)
                    now.right = node
                    now = node
                    break

        while now.fa.key > now.key:
            if now == now.fa.left:
                self.rightRotate(now)
            else:
                self.leftRotate(now)

        self.findMax()

    def delete(self, v):
        now = self.root
        while now.v != v:
            if v < now.v:
                now = now.left
            else:
                now = now.right

        while now.left and now.right:
            if now.left.key < now.right.key:
                self.rightRotate(now.left)
            else:
                self.leftRotate(now.right)

        fa = now.fa
        if now.left:
            if now == fa.left:
                fa.left = now.left
                now.left.fa = fa
            else:
                fa.right = now.left
                now.left.fa = fa

        elif now.right:
            if now == fa.left:
                fa.left = now.right
                now.right.fa = fa
            else:
                fa.right = now.right
                now.right.fa = fa

        else:
            if now == fa.left:
                fa.left = None
            else:
                fa.right = None

        del(now)
        self.findMax()

    def findMax(self):
        now = self.root
        while now.right:
            now = now.right
        self.ma = now.v

class MaxStack(object):

    def __init__(self):
        self.order = Treap()
        self.value = Treap()
        self.index = 0

    def push(self, x):
        self.order.insert((self.index, x))
        self.value.insert((x, self.index))
        self.index += 1

    def pop(self):
        max_index, v = self.order.ma
        self.order.delete((max_index, v))
        self.value.delete((v, max_index))
        return v

    def top(self):
        _, v = self.order.ma
        return v

    def peekMax(self):
        v, _ = self.value.ma
        return v

    def popMax(self):

        max_v, index = self.value.ma
        self.order.delete((index, max_v))
        self.value.delete((max_v, index))
        return max_v
'''

_LINES = CODE.strip('\n').split('\n')
_MS = next(i for i, l in enumerate(_LINES, 1) if l.startswith('class MaxStack'))


def _ln(sub):
    return next(i for i, l in enumerate(_LINES, 1) if i > _MS and sub in l)


L_FINDMAX = next(i for i, l in enumerate(_LINES, 1) if 'self.ma = now.v' in l)
L_PUSH, L_POP, L_TOP, L_PEEK, L_POPMAX = (_ln('def push'), _ln('def pop(self)'), _ln('def top'),
                                          _ln('def peekMax'), _ln('def popMax'))
OPS = ['push(5)', 'push(1)', 'push(5)', 'top()', 'popMax()', 'top()', 'peekMax()', 'pop()', 'top()']


def _op_name(line):
    for start, name in sorted([(L_POPMAX, 'popMax'), (L_PEEK, 'peekMax'), (L_TOP, 'top'), (L_POP, 'pop'),
                               (L_PUSH, 'push')], reverse=True):
        if line > start:
            return name
    return '__init__'


def _tree_nodes(root):
    """in-order list of (node, depth) under the sentinel root"""
    out = []

    def go(n, d):
        if n is None:
            return
        go(n.left, d + 1)
        out.append((n, d))
        go(n.right, d + 1)
    if root is not None:
        go(root.right, 0)
    return out


def _draw_treap(cv, T, tr, box, title, fmt, note, active=False):
    x0, y0, x1, y1 = box
    if active:
        cv.rect((x0 + 4, y0 + 2, x1 - 4, y1 - 4), outline=T['yellow'], width=3, r=12)
    cv.text((x0 + 14, y0 + 4), title + ('（刚修改）' if active else ''), 23, T['yellow'] if active else T['muted'], bold=True)
    if tr is None:
        cv.text((x0 + 14, y0 + 44), '（尚未创建）', 22, T['dim'])
        return
    nodes = _tree_nodes(tr.root)
    if not nodes:
        cv.text((x0 + 14, y0 + 50), '空树（只有哨兵根）', 22, T['dim'])
    else:
        ma = nodes[-1][0]
        sp = min(110, (x1 - x0 - 40) / len(nodes))
        maxd = max(d for _, d in nodes) + 1
        dy = min(80, (y1 - y0 - 130) / max(1, maxd))
        sx = x0 + 20 + ((x1 - x0 - 40) - sp * len(nodes)) / 2 + sp / 2
        pos = {id(n): (sx + k * sp, y0 + 70 + d * dy) for k, (n, d) in enumerate(nodes)}
        for n, d in nodes:
            X, Y = pos[id(n)]
            for ch in (n.left, n.right):
                if ch is not None and id(ch) in pos:
                    cv.line([(X, Y), pos[id(ch)]], T['border'], 3)
        for n, d in nodes:
            X, Y = pos[id(n)]
            hit = n is ma
            cv.d.ellipse((X - 34, Y - 22, X + 34, Y + 22), fill=T['green'] if hit else T['panel2'],
                         outline=T['green'] if hit else T['border'], width=2)
            cv.text((X, Y), fmt(n.v), 21, T['bg'] if hit else T['text'], anchor='mm', bold=True, mono=True)
        X, Y = pos[id(ma)]
        cv.text((X, Y + 26), '最右 = ma', 18, T['green'], anchor='mt', bold=True)
    cv.rich(x0 + 14, y1 - 48, note(tr), x1 - x0 - 28, size=22)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mid = (x0 + x1) / 2
    order, value = S.get('self.order'), S.get('self.value')
    inner = S.get('self.root') if S.get('_line', 0) == L_FINDMAX else None
    _draw_treap(cv, T, order, (x0, y0, mid - 6, y1), 'order：按 (时间, 值)',
                lambda v: f'{v[0]},{v[1]}',
                lambda tr: (f'`ma = {tr.ma}` → 栈顶 ==`{tr.ma[1]}`==' if tr.ma[0] >= 0 else '`ma` = 哨兵'),
                active=order is not None and inner is order.root)
    _draw_treap(cv, T, value, (mid + 6, y0, x1, y1), 'value：按 (值, 时间)',
                lambda v: f'{v[0]},{v[1]}',
                lambda tr: (f'`ma = {tr.ma}` → 最大值 ==`{tr.ma[0]}`==' if tr.ma[1] >= 0 else '`ma` = 哨兵'),
                active=value is not None and inner is value.root)
    cv.line([(mid, y0 + 10), (mid, y1 - 10)], T['border'], 2)


def _which(S):
    o = S.get('self.order')
    return 'order' if o is not None and S.get('self.root') is o.root else 'value'


def _ops_text(S):
    cur = _op_name(S.get('_line', 0))
    return '操作：`' + ' → '.join(OPS) + f'`；正在执行 =={cur}=='


def _stack_view(S):
    tr = S.get('self.order')
    if tr is None:
        return None
    return [n.v[1] for n, _ in _tree_nodes(tr.root)]


CONFIG = dict(
    num=716, title='最大栈', difficulty='Hard', category='设计',
    author='yiduobo', technique='两棵平衡树（Treap）',
    tags=['字节30天'],
    code=CODE,
    setup='random.seed(2023)',
    call='''ms = MaxStack()
ms.push(5); ms.push(1); ms.push(5)
a = ms.top(); b = ms.popMax(); c = ms.top(); d = ms.peekMax(); e = ms.pop(); f = ms.top()
[a, b, c, d, e, f]''',
    expect=[5, 5, 1, 5, 1, 5],
    skip=[k for k in range(1, _MS + 1) if k != L_FINDMAX],
    views=[
        dict(type='text', fn=_ops_text, size=22, h=80, lines=2),
        dict(type='array', var=_stack_view, label='按时间排好的栈（= order 的中序遍历，最右是栈顶）', h=150, cell=70),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('x', 'x', 'blue'), ('self.index', 'self.index')],
    captions={
        L_FINDMAX: lambda S, B, r: (f'{"删除" if ("max_v" in S or "max_index" in S) else "插入"}完成后，从根一直向右走到底：'
                                    f'`{_which(S)}.ma = {S["self.ma"]}`'),
        'self.order = Treap()': '`order`：按==时间==排序的平衡树，节点值 `(时间戳, x)`',
        'self.value = Treap()': '`value`：按==数值==排序的平衡树，节点值 `(x, 时间戳)`',
        'self.index = 0': '`index` 是时间戳，每 push 一次加 1',
        'self.order.insert((self.index, x))': lambda S, B, r: f'`push({B.x})`：在 order 中插入 `({B["self.index"]}, {B.x})`（插入后从根一直向右走，更新 ma）',
        'self.value.insert((x, self.index))': lambda S, B, r: f'在 value 中插入 `({B.x}, {B["self.index"]})`',
        'self.index += 1': '时间戳 +1 → `{self.index}`',
        'max_index, v = self.order.ma': '`pop()`：栈顶 = order 的最大节点 `order.ma = ({max_index}, {v})`',
        'self.order.delete((max_index, v))': lambda S, B, r: f'从 order 删掉 `({B.max_index}, {B.v})`',
        'self.value.delete((v, max_index))': lambda S, B, r: f'从 value 删掉对应的 `({B.v}, {B.max_index})`：两棵树要同步',
        'return v': lambda S, B, r: f'`{_op_name(S._line)}()` 返回 =={r}==',
        '_, v = self.order.ma': '`top()`：order 里最右的节点就是==最后入栈==的：`order.ma = {self.order.ma}`',
        'v, _ = self.value.ma': '`peekMax()`：value 里最右的节点就是==最大值==：`value.ma = {self.value.ma}`',
        'max_v, index = self.value.ma': '`popMax()`：最大值 = `value.ma = ({max_v}, {index})`（值相同时取时间最大的 = 最靠近栈顶）',
        'self.order.delete((index, max_v))': lambda S, B, r: f'从 order 里删掉 `({B.index}, {B.max_v})`',
        'self.value.delete((max_v, index))': lambda S, B, r: f'从 value 里删掉 `({B.max_v}, {B.index})`',
        'return max_v': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='两棵平衡树：一棵按时间排、一棵按数值排，最大值就是最右节点',
        complexity='`top/peekMax` 为 `O(1)`，其余 `O(log n)`；空间 `O(n)`',
        problem=['设计最大栈：支持 `push(x)`、`pop()`、`top()`、`peekMax()`、`popMax()`',
                 '`popMax()` 删除栈中最大元素；有多个最大值时，只删==最靠近栈顶==的那个',
                 '要求 `top` 为 `O(1)`，其余操作 `O(log n)`',
                 '示例：`push(5), push(1), push(5), top()=5, popMax()=5, top()=1, peekMax()=5, pop()=1, top()=5`'],
        quote='设置两颗平衡二叉树order和value，接下来，对于插入操作，在order中插入值为（timestamp， x）的节点，在value中插入值为（x, timestamp）的节点，同时在插入操作完成后==从根节点出发一直向右侧行走，找出当前树中值最大的节点值ma==。',
        quote_src='—— yiduobo 题解原文',
        idea=['插入和删除都要 `O(log n)` → 只能用==平衡二叉树==（他用的是经典的 treap）',
              '`pop`：通过 `order.ma` 拆出 timestamp 和 x，在两棵树里各删一次；`popMax` 用 `value.ma` 同理',
              '删除可能改变 ma → 删完同样从根一直往右走，重新找最大'],
        summary=['值相同按时间比较：`(x, timestamp)` 最大的就是==最靠近栈顶==的最大值',
                 '树根是哨兵节点 `(-10^7-1, -1)`，key 为 -1，旋转永远转不过它，省去判空',
                 '视频里跳过了 treap 的插入旋转/删除细节（原文也“不展开”），只看两棵树的变化',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；随机优先级固定了种子以便复现',
                 '另一种常见写法：双向链表 + 有序集合（SortedList）'],
    ),
)
