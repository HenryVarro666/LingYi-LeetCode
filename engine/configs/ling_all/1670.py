def _qs(S):
    """返回 (left 列表, right 列表)：优先取当前栈帧里的 self，其次取外层变量 q"""
    o = S.get('self')
    if o is None:
        o = S.get('q')
    if o is None or not hasattr(o, 'left'):
        return None, None
    return list(o.left), list(o.right)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L, R = _qs(S)
    if L is None:
        cv.text((x0 + 18, y0 + 4), '队列尚未创建', 24, T['muted'], bold=True)
        return
    Lb, Rb = _qs(B)
    cv.text((x0 + 18, y0 + 4), '整个队列 = left + right（保证 len(right) − len(left) 为 0 或 1）', 24, T['muted'], bold=True)
    n = len(L) + len(R)
    cell = 84
    gap = 56
    total = n * cell + gap
    sx = x0 + max(20, ((x1 - x0) - total) / 2)
    Y = y0 + 150
    old = set(Lb or []) | set(Rb or [])
    x = sx
    for name, arr, col in (('left', L, 'blue'), ('right', R, 'pink')):
        w = max(len(arr), 1) * cell
        cv.text((x + w / 2 if arr else x + cell / 2, Y - 62), f'{name}（{len(arr)}）', 22, T[col], anchor='mm', bold=True)
        if not arr:
            cv.rect((x + 4, Y - 32, x + cell - 4, Y + 32), fill=None, outline=T['border'], width=2, r=8)
            cv.text((x + cell / 2, Y), '空', 22, T['dim'], anchor='mm')
            x += cell
        for v in arr:
            fill = T['yellow'] if v not in old else T['panel2']
            cv.rect((x + 4, Y - 32, x + cell - 4, Y + 32), fill=fill, r=8, outline=T['border'], width=2)
            cv.text((x + cell / 2, Y), v, 28, T['bg'] if v not in old else T['text'], anchor='mm', bold=True, mono=True)
            x += cell
        if name == 'left':
            cv.line([(x + gap / 2, Y - 50), (x + gap / 2, Y + 50)], T['purple'], 4)
            cv.text((x + gap / 2, Y + 74), '中点', 20, T['purple'], anchor='mm', bold=True)
            x += gap
    if L or R:
        full = L + R
        mid = full[(len(full) - 1) // 2]
        cv.text((x0 + 18, Y + 120), '完整队列：' + ' → '.join(map(str, full)) + f'　（正中间 = {mid}）', 24, T['text'])
    else:
        cv.text((x0 + 18, Y + 120), '完整队列：空', 24, T['text'])


CONFIG = dict(
    num=1670, title='设计前中后队列', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='两个双端队列 · 平衡长度',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1610'],
    code='''
class FrontMiddleBackQueue:
    __slots__ = 'left', 'right'

    def __init__(self):
        self.left = deque()
        self.right = deque()

    # 调整长度，保证 0 <= len(right) - len(left) <= 1
    # 从而保证可以在正中间插入删除元素
    def balance(self):
        if len(self.left) > len(self.right):
            self.right.appendleft(self.left.pop())
        elif len(self.right) > len(self.left) + 1:
            self.left.append(self.right.popleft())

    def pushFront(self, val: int) -> None:
        self.left.appendleft(val)
        self.balance()

    def pushMiddle(self, val: int) -> None:
        if len(self.left) < len(self.right):
            self.left.append(val)
        else:
            self.right.appendleft(val)

    def pushBack(self, val: int) -> None:
        self.right.append(val)
        self.balance()

    def popFront(self) -> int:
        if not self.right:  # 整个队列为空
            return -1
        val = self.left.popleft() if self.left else self.right.popleft()
        self.balance()
        return val

    def popMiddle(self) -> int:
        if not self.right:  # 整个队列为空
            return -1
        if len(self.left) == len(self.right):
            return self.left.pop()
        return self.right.popleft()

    def popBack(self) -> int:
        if not self.right:  # 整个队列为空
            return -1
        val = self.right.pop()
        self.balance()
        return val
''',
    call='''q = FrontMiddleBackQueue()
res = [q.pushFront(1), q.pushBack(2), q.pushMiddle(3), q.pushMiddle(4), q.popFront(), q.popMiddle(), q.popMiddle(), q.popBack(), q.popFront()]
res''',
    expect=[None, None, None, None, 1, 3, 4, 2, -1],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=['val', ('left 长度', 'len(self.left)', 'blue'), ('right 长度', 'len(self.right)', 'pink')],
    captions={
        'self.left = deque()': '`left` 存队列的前半段，`right` 存后半段',
        'self.right = deque()': '约定：`right` 比 `left` 长 0 或 1，所以==正中间就在两段的交界处==',
        'if len(self.left) > len(self.right)': lambda S, B, r: ('`left` 比 `right` 长 → 把 `left` 末尾挪给 `right` 头部' if len(S.self.left) > len(S.self.right) else '`left` 没有超长'),
        'self.right.appendleft(self.left.pop())': '`left` 末尾 → `right` 头部：中点向左移一格',
        'elif len(self.right) > len(self.left) + 1': lambda S, B, r: ('`right` 多出 2 个以上 → 把 `right` 头部挪给 `left` 末尾' if len(S.self.right) > len(S.self.left) + 1 else '长度差合法，不用调整'),
        'self.left.append(self.right.popleft())': '`right` 头部 → `left` 末尾：中点向右移一格',
        'self.left.appendleft(val)': '`pushFront({val})`：加到 `left` 最前面',
        'self.balance()': '操作完调整长度，保持 0 <= len(right) − len(left) <= 1',
        'if len(self.left) < len(self.right)': lambda S, B, r: ('`left` 比 `right` 短 → 新元素加到 `left` 末尾（正好在中间）' if len(S.self.left) < len(S.self.right) else '两段一样长 → 新元素加到 `right` 头部（中间靠前的位置）'),
        'self.left.append(val)': '`pushMiddle({val})`：加到 `left` 末尾',
        'self.right.appendleft(val)': '`pushMiddle({val})`：加到 `right` 头部',
        'self.right.append(val)': '`pushBack({val})`：加到 `right` 最后面',
        'if not self.right': lambda S, B, r: ('`right` 为空 → 整个队列为空，返回 `-1`' if not S.self.right else '队列非空，可以弹出'),
        'val = self.left.popleft() if self.left': '`popFront`：`left` 不空弹它的头，否则（队列只有 1 个）弹 `right` 的头：弹出 `{val}`',
        'if len(self.left) == len(self.right)': lambda S, B, r: ('两段一样长 → 中间元素是 `left` 末尾（靠前的那个）' if len(S.self.left) == len(S.self.right) else '`right` 多一个 → 中间元素就是 `right` 头部'),
        'return self.left.pop()': '`popMiddle`：弹出 `left` 末尾 `{ret}`',
        'return self.right.popleft()': '`popMiddle`：弹出 `right` 头部 `{ret}`',
        'val = self.right.pop()': '`popBack`：弹出 `right` 末尾 `{val}`',
        'return val': '返回 `{val}`',
        'return -1': '队列为空 → 返回 `-1`',
    },
    cards=dict(
        one_liner='把队列劈成两半，中点永远在两段交界处',
        complexity='所有操作均为 `O(1)`，空间 `O(q)`',
        problem=['设计队列，支持在==前、中、后==三个位置 push 和 pop',
                 '有两个中间位置时选靠前的；队列为空时 pop 返回 `-1`',
                 '示例：`pushFront(1)`、`pushBack(2)`、`pushMiddle(3)`、`pushMiddle(4)`，再依次 pop 前、中、中、后、前 → `1, 3, 4, 2, -1`'],
        quote='调整长度，保证 0 <= len(right) - len(left) <= 1，从而保证可以在正中间插入删除元素。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['两个 `deque`：`left` 放前半，`right` 放后半，==right 不比 left 短，最多长 1==',
              '前、后操作后调用 `balance`，把一个元素从长的一段挪到另一段',
              '中间插入 / 弹出直接对 `left` 末尾或 `right` 头部操作，不会破坏平衡约束'],
        summary=['所有操作 `O(1)`，空间 `O(q)`',
                 '易错：队列为空判断用 `not self.right`——`right` 为空则 `left` 一定也空',
                 '`popFront` 在只剩一个元素时 `left` 为空，要弹 `right` 头部',
                 '`pushMiddle` 不用调用 `balance`：它本身就是按约束放的'],
    ),
)
