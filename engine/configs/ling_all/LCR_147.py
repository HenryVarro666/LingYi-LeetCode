def _fmt(x):
    v, m = x
    if m == float('inf'):
        return '哨兵 ∞'
    return f'{v} | min {m}'


def _txt(S):
    st = S.get('self.st')
    if not st or len(st) < 2:
        return '栈里每个元素是一对 `(值, 到此为止的最小值)`'
    return f'栈顶 `{st[-1][0]}`，当前最小值 =={st[-1][1]}==：直接读栈顶的第二个数'


CONFIG = dict(
    num='LCR 147', title='最小栈', difficulty='Easy', category='设计',
    author='灵茶山艾府', technique='栈里存 (值, 前缀最小值) · 栈底哨兵',
    tags=[],
    code='''
class MinStack:
    def __init__(self):
        # 这里的 0 写成任意数都可以，反正用不到
        self.st = [(0, inf)]  # 栈底哨兵

    def push(self, val: int) -> None:
        self.st.append((val, min(self.st[-1][1], val)))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        return self.st[-1][1]
''',
    call='''ms = MinStack()
res = []
ms.push(-2)
ms.push(0)
ms.push(-3)
res.append(ms.getMin())
ms.pop()
res.append(ms.top())
res.append(ms.getMin())
res''',
    expect=[-3, 0, -2],
    views=[
        dict(type='stack', var='self.st', label='self.st（值 | 到这里为止的最小值）', fmt=_fmt, h=330),
        dict(type='text', h=70, size=30, fn=_txt),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=['val', ('栈大小', 'len(self.st) - 1'), ('res', 'res', 'green')],
    skip=['# 这里的 0'],
    captions={
        'self.st = [(0, inf)]': '栈底放哨兵 `(0, inf)`：`inf` 当作「空栈的最小值」，以后 `push` 不用特判空栈',
        'self.st.append': lambda S, B, ret: (f'`push({S.val})`：新的最小值 = `min({B["self.st"][-1][1]}, {S.val})` = =={S["self.st"][-1][1]}==，'
                                             f'和 `{S.val}` 一起入栈'),
        'self.st.pop()': lambda S, B, ret: f'`pop()`：弹出栈顶 `{B["self.st"][-1]}`，==最小值跟着一起回退==，不用重新计算',
        'return self.st[-1][0]': '`top()`：栈顶的第一个数 → `{ret}`',
        'return self.st[-1][1]': '`getMin()`：栈顶的第二个数就是当前栈的最小值 → ==`{ret}`==，`O(1)`',
    },
    cards=dict(
        one_liner='每个元素顺手记下「到我为止的最小值」，弹出时它自然回退',
        complexity='所有操作 `O(1)`，空间 `O(q)`',
        problem=['设计栈，支持 `push`、`pop`、`top`，并能 `O(1)` 取出最小元素 `getMin`',
                 '示例：`push(-2), push(0), push(-3)` → `getMin()` = `-3`',
                 '`pop()` 后 `top()` = `0`，`getMin()` = `-2`'],
        quote='栈中除了保存添加的元素，还保存前缀最小值。（栈中保存的是 pair）',
        quote_src='—— 灵茶山艾府题解',
        idea=['引入：数组每个前缀的最小值 `preMin[i] = min(preMin[i-1], nums[i])`',
              '栈就是一个「末尾增删」的数组，所以每个元素带上自己的 `preMin`',
              '栈底放 `inf` 哨兵当 `preMin[-1]`，第一次 `push` 也不用特判'],
        summary=['所有操作 `O(1)`；空间 `O(q)`，`q` 是 `push` 次数',
                 '易错：只存一个全局 `min` 的话，弹出最小值后就不知道新的最小值了',
                 '哨兵的第一个数 `0` 随便写，用不到；题目保证 `pop/top/getMin` 不会在空栈上调用',
                 '变形题：改成队列 / 双端队列再求最小值，见 Codeforces「Minimum Deque」'],
    ),
)
