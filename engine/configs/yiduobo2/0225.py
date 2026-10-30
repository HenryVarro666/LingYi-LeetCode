OPS = 'push(1) → push(2) → push(3) → top() → pop() → top() → empty()'


def _while(S, B, ret):
    if B.size > 1:
        return f'`size = {B.size} > 1`：新元素前面还有 `{B.size - 1}` 个旧元素 → 继续把队首挪到队尾'
    return f'`size = {B.size}`：新元素 `{S.x}` 已经==转到了队首== → 旋转结束'


def _rot(S, B, ret):
    v = B['self.q'][0]
    return f'队首 `{v}` 出队，再从队尾入队：`q = {S["self.q"]}`'


def _rotating(S):
    q = S.get('self.q')
    return 'x' in S and bool(q) and q[0] != S['x']


def _state(S):
    q = S.get('self.q')
    if not q:
        return '队列为空 = 栈为空'
    if _rotating(S):
        return f"旋转中：新元素 `{S['x']}` 还没到队首，暂时不是合法的栈"
    return f"栈顶 = 队首 = =={q[0]}==，栈里共 `{len(q)}` 个数"


CONFIG = dict(
    num=225, title='用队列实现栈', difficulty='Easy', category='设计',
    author='yiduobo', technique='单队列 · push 时旋转，新元素转到队首',
    tags=['热题173'],
    code='''
class MyStack(object):

    def __init__(self):
        self.q = []

    def push(self, x):
        self.q.append(x)
        size = len(self.q)
        while size > 1:
            self.q.append(self.q.pop(0))
            size -= 1

    def pop(self):
        return self.q.pop(0)

    def top(self):
        return self.q[0]

    def empty(self):
        return len(self.q) == 0
''',
    call='''ms = MyStack()
ms.push(1); ms.push(2); ms.push(3)
a = ms.top(); b = ms.pop()
[a, b, ms.top(), ms.empty()]''',
    expect=[3, 3, 2, False],
    views=[
        dict(type='text', fn=lambda S: f'操作序列：`{OPS}`', size=24, h=90, lines=2),
        dict(type='queue', var='self.q', label='q（只用队列操作：队尾进、队首出）', h=150, font=32),
        dict(type='array', var='self.q', label='同一个 q 当栈看：队首 = 栈顶（旋转途中变暗）', cell=90, index=False,
             dim=lambda S, i, v: _rotating(S),
             color=lambda S, i, v: 'purple' if i == 0 else None),
        dict(type='text', fn=_state, size=28),
    ],
    watch=[('x', 'x', 'blue'), ('size', 'size', 'pink'), ('len(q)', 'len(self.q)', 'green')],
    captions={
        'self.q = []': '只用一个队列 `q`：约定==队首就是栈顶==',
        'self.q.append(x)': '`push({x})`：先把新元素放到队尾 → `q = {self.q}`',
        'size = len(self.q)': lambda S, B, ret: (f'`size = {S.size}`：新元素前面有 `{S.size - 1}` 个旧元素，要把它们依次挪到后面'
                                                 if S.size > 1 else '`size = 1`：队列里只有它自己，不用旋转'),
        'while size > 1': _while,
        'self.q.append(self.q.pop(0))': _rot,
        'size -= 1': '还剩 `size = {size}`',
        'return self.q.pop(0)': '`pop()`：队首就是最后进来的数 → 弹出 =={ret}==',
        'return self.q[0]': '`top()`：看队首 → =={ret}==',
        'return len(self.q) == 0': '`empty()`：队列还有 `{len(self.q)}` 个数 → `{ret}`',
    },
    skip=[],
    cards=dict(
        one_liner='push 时把前面的旧元素依次挪到队尾，让新元素站到队首',
        complexity='`push` 为 `O(n)`，`pop / top / empty` 为 `O(1)`',
        problem=['只用==队列==的标准操作（队尾入、队首出、看队首、求大小、判空），实现一个后进先出的栈',
                 '支持 `push(x)`、`pop()`、`top()`、`empty()`',
                 '示例：`push(1), push(2), top() → 2, pop() → 2, empty() → false`'],
        quote='由于队列是先进先出的，因此如果要用队列模拟栈，那么==要把晚进来的数据放在队列的头部==，才能达成栈后进先出的效果。',
        quote_src='—— yiduobo 知乎题解',
        idea=['新元素先加入队尾', '再从头开始把前面的元素依次弹出、加入队尾，==直到新元素成为队首==',
              '于是队列从头到尾 = 栈从顶到底，`pop / top` 直接访问队首'],
        result='返回 `[3, 3, 2, False]`：`top()=3`，`pop()=3`，之后栈顶是 `2`，栈非空 ✓',
        summary=['`push` 要转 `n-1` 次，`O(n)`；其余操作 `O(1)`',
                 '关键：每次 push 后都保持「队首 = 栈顶」，所以只需旋转==新元素前面的== `size-1` 个数',
                 '原文用列表当队列，`pop(0)` 是 `O(n)`；换成 `deque.popleft()` 才是 `O(1)`',
                 '原文为 Python 2 风格：删去了文档字符串和 LeetCode 模板注释，逻辑未改'],
    ),
)
