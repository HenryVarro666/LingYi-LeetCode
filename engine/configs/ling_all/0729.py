SETUP = '''
import bisect as _bs


class _TreeNode:  # redblacktree.Node 的最小替代：只有 key / value
    def __init__(self, key, value):
        self.key = key
        self.value = value


class _TreeIterator:  # redblacktree.Iterator 的最小替代：只含 Next / Key
    def __init__(self, tree, node):
        self.tree = tree
        self.node = node

    def next(self):  # 移到 key 更大的下一个节点；没有就返回 False
        ks = self.tree._keys
        i = _bs.bisect_right(ks, self.node.key)
        if i < len(ks):
            self.node = self.tree._nodes[ks[i]]
            return True
        self.node = None
        return False

    def key(self):
        return self.node.key


class RedBlackTree:  # github.com/emirpasic/gods 的 redblacktree.Tree 的最小替代：有序映射，只含 Put / Floor / IteratorAt
    def __init__(self):
        self._keys = []     # 升序的 key
        self._nodes = {}    # key -> 节点

    def put(self, key, value):
        if key in self._nodes:
            self._nodes[key].value = value
        else:
            _bs.insort(self._keys, key)
            self._nodes[key] = _TreeNode(key, value)

    def floor(self, key):  # 返回 (小于等于 key 的最大节点, 是否找到)
        i = _bs.bisect_right(self._keys, key)
        if i == 0:
            return None, False
        return self._nodes[self._keys[i - 1]], True

    def iterator_at(self, node):
        return _TreeIterator(self, node)

    def items(self):
        return [(k, self._nodes[k].value) for k in self._keys]
'''

CALL = """c = MyCalendar()
out = []
out.append(c.book(10, 20))
out.append(c.book(15, 25))
out.append(c.book(20, 30))
out.append(c.book(5, 12))
out.append(c.book(0, 10))
out"""

AX = 30   # 数轴 0..30


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    t = S.get('self.tree') or S.get('t')
    cv.text((x0 + 18, y0 + 4), '红黑树：按 start 排序的有序映射（start → end），这里画成数轴上的区间', 22, T['muted'], bold=True)
    if t is None:
        cv.text((x0 + 18, y0 + 56), '（尚未创建）', 24, T['dim'])
        return
    L, R = x0 + 110, x1 - 44

    def X(v):
        return L + v / AX * (R - L)
    ln = S.get('_line', 0)
    items = [(k, v) for k, v in t.items() if k >= 0]
    fl = S.get('floor')
    it = S.get('it')
    sent_hot = fl is not None and fl.key == -1
    H = y1 - y0
    yq, yt, ya = y0 + H * 0.17, y0 + H * 0.45, y0 + H * 0.72
    bh = 46
    # 新日程
    cv.text((x0 + 18, yq + bh / 2), '新日程', 22, T['muted'], anchor='lm', bold=True)
    if 'start' in S:
        a, b = S['start'], S['end']
        c = T['yellow']
        if ln in (10, 13):
            c = T['red']
        elif ln >= 14:
            c = T['green']
        cv.rect((X(a), yq, X(b), yq + bh), fill=c, r=10)
        cv.text(((X(a) + X(b)) / 2, yq + bh / 2), f'[{a},{b})', 22, T['bg'], anchor='mm', bold=True, mono=True)
        for v in (a, b):
            cv.dashed((X(v), yq + bh), (X(v), ya), T['yellow'], 2)
    # 已预订
    cv.text((x0 + 18, yt + bh / 2), '已预订', 22, T['muted'], anchor='lm', bold=True)
    cv.rect((x0 + 18, yt + bh + 8, x0 + 92, yt + bh + 34), fill=(52, 46, 70), r=8,
            outline=T['blue'] if sent_hot else T['border'], width=4 if sent_hot else 1)
    cv.text((x0 + 55, yt + bh + 21), '哨兵', 18, T['text'], anchor='mm', bold=True)
    sk = None
    if it is not None and getattr(it, 'node', None) is not None and ln >= 12 and (fl is None or it.node.key != fl.key):
        sk = it.node.key
    for k, v in items:
        new = (k, v) == (S.get('start'), S.get('end')) and ln >= 14
        cv.rect((X(k), yt, X(v), yt + bh), fill=T['green'] if new else T['panel2'], r=10,
                outline=T['blue'] if (fl is not None and fl.key == k) else (T['pink'] if sk == k else T['border']),
                width=5 if ((fl is not None and fl.key == k) or sk == k) else 2)
        cv.text(((X(k) + X(v)) / 2, yt + bh / 2), f'[{k},{v})', 22, T['bg'] if new else T['text'], anchor='mm', bold=True, mono=True)
    # 数轴
    cv.line([(L, ya), (R, ya)], T['border'], 2)
    for v in range(0, AX + 1, 5):
        cv.line([(X(v), ya), (X(v), ya + 8)], T['border'], 2)
        cv.text((X(v), ya + 12), str(v), 18, T['dim'], anchor='mt', mono=True)
    cv.text((x0 + 18, y1 - 22), '蓝框 = Floor 找到的左邻日程，粉框 = Next 找到的右邻日程', 20, T['dim'], anchor='lm')


def _info(S):
    if 'start' not in S:
        return ''
    a, b, ln = S['start'], S['end'], S.get('_line', 0)
    if ln in (10, 13):
        return f'预订 `[{a},{b})`：==冲突==，不加入'
    if ln >= 14:
        return f'预订 `[{a},{b})`：左右邻居都不重叠 → ==加入日历=='
    return f'预订 `[{a},{b})`：只要检查==左右两个邻居=='


CONFIG = dict(
    num=729, title='我的日程安排表 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='有序映射（红黑树）· 查左右邻居（Go 原文转写）',
    tags=['labuladong', '灵神题单·常用数据结构'],
    setup=SETUP,
    code='''
class MyCalendar:
    def __init__(self):
        t = RedBlackTree()
        t.put(-1, -1)  # 哨兵
        self.tree = t

    def book(self, start: int, end: int) -> bool:
        floor, _ = self.tree.floor(start)
        if floor.value > start:  # [start,end) 左侧区间的右端点超过了 start
            return False
        it = self.tree.iterator_at(floor)
        if it.next() and it.key() < end:  # [start,end) 右侧区间的左端点小于 end
            return False
        self.tree.put(start, end)  # 可以插入区间 [start,end)
        return True
''',
    call=CALL,
    expect=[True, False, True, False, True],
    views=[
        dict(type='custom', draw=_draw, h=450),
        dict(type='text', fn=_info, size=28, h=90),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'pink'), ('floor.value', 'floor.value', 'orange'),
           ('已预订', 'len(self.tree.items()) - 1', 'green')],
    max_steps=60,
    captions={
        3: '新建一棵红黑树，保存 ==start → end==，按 start 有序',
        4: '先放一个哨兵 `(-1, -1)`：保证任何 `start ≥ 0` 的 `floor` 都能找到节点，不用判空',
        5: '日历 = 这棵树',
        'floor, _ = self.tree.floor(start)': lambda S, B, r: (
            f'==book({S.start}, {S.end})==：`floor({S.start})` 找 start ≤ {S.start} 的最大节点 = ==左邻== '
            + ('（哨兵，左边没有日程）' if S.floor.key == -1 else f'`[{S.floor.key},{S.floor.value})`')),
        'if floor.value > start': lambda S, B, r: (
            f'左邻的右端点 `{S.floor.value}` > `start = {S.start}` → 左邻覆盖了 `start`，==重叠=='
            if S.floor.value > S.start else
            (f'哨兵的 `value = -1` 不会超过 `start = {S.start}` → 左边没问题' if S.floor.key == -1 else
             f'左邻的右端点 `{S.floor.value}` ≤ `start = {S.start}`（半开区间，相接不算重叠）→ 左边没问题')),
        10: '左边冲突，返回 `False`，不加入日历',
        'it = self.tree.iterator_at(floor)': '迭代器停在 `floor` 这个节点上，下一步 `next()` 就是==右邻==',
        'if it.next() and it.key() < end': lambda S, B, r: (
            f'`next()` 没有下一个节点：右边没有日程，不会重叠' if S.it.node is None else
            (f'右邻 `[{S.it.node.key},{S.it.node.value})` 的左端点 `{S.it.node.key}` < `end = {S.end}` → ==重叠=='
             if S.it.node.key < S.end else
             f'右邻 `[{S.it.node.key},{S.it.node.value})` 的左端点 `{S.it.node.key}` ≥ `end = {S.end}` → 右边没问题')),
        13: '右边冲突，返回 `False`，不加入日历',
        'self.tree.put(start, end)': '左右邻居都不冲突 → 插入 `[{start},{end})`',
        'return True': '预订成功，返回 `True`',
    },
    cards=dict(
        one_liner='日程互不重叠 → 新日程只需和左右邻居比',
        complexity='`book`：时间 `O(log n)`（红黑树），空间 `O(n)`',
        problem=['`book(start, end)`：和已有日程不重叠就加入并返回 `True`，否则返回 `False`',
                 '区间是半开的 `[start, end)`，`[10,20)` 与 `[20,30)` 不算重叠',
                 '示例：`book(10,20)`、`book(15,25)`、`book(20,30)` → `True, False, True`',
                 '本视频再加 `book(5,12)`、`book(0,10)` → `False, True`'],
        quote='[start,end) 左侧区间的右端点超过了 start；[start,end) 右侧区间的左端点小于 end。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['已预订的日程互不重叠，所以按 start 排序后，end 也是有序的',
              '新日程 `[start,end)` 只可能和==左邻（start 的前驱）==或==右邻（后继）==重叠',
              '左邻的右端点 `> start` 就重叠；右邻的左端点 `< end` 就重叠；哨兵让 `floor` 永远有值'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；`redblacktree` 是第三方库，视频里在 setup 用有序数组补了同接口的替代（`put` / `floor` / `iterator_at` / `next` / `key`）',
                 '真正的红黑树每次 `floor`、`next`、`put` 都是 `O(log n)`，所以 `book` 是 `O(log n)`',
                 '易错：半开区间，相接（如 `[10,20)` 和 `[20,30)`）不算重叠，所以比较用 `>`、`<` 而不是 `>=`',
                 '易错：只检查左邻、右邻就够了，不必遍历所有日程（暴力写法是 `O(n)`）'],
    ),
)
