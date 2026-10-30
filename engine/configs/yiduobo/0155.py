OPS = 'push(-2) → push(0) → push(-3) → getMin() → pop() → top() → getMin()'


def _push_if(S, B, ret):
    ms = B['self.min_stack']
    x = S.x
    if not ms:
        return f'`push({x})`：min_stack 为空 → `{x}` 就是当前最小值'
    if ms[-1] > x:
        return f'`push({x})`：`{x}` 比旧最小值 `{ms[-1]}` 还小 → ==最小值更新为 {x}=='
    return f'`push({x})`：`{x}` 不比旧最小值 `{ms[-1]}` 小 → 最小值不变'


CONFIG = dict(
    num=155, title='最小栈', difficulty='Medium', category='栈',
    author='yiduobo', technique='辅助栈 min_stack',
    code='''
class MinStack(object):

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x):
        if not self.min_stack or self.min_stack[-1] > x:
            self.min_stack.append(x)
        else:
            self.min_stack.append(self.min_stack[-1])
        self.stack.append(x)

    def pop(self):
        self.min_stack.pop()
        return self.stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]
''',
    call='''ms = MinStack()
ms.push(-2); ms.push(0); ms.push(-3)
a = ms.getMin(); ms.pop(); b = ms.top()
[a, b, ms.getMin()]''',
    expect=[-3, 0, -2],
    views=[
        dict(type='text', fn=lambda S: f'操作序列：`{OPS}`', size=24, h=90, lines=2),
        dict(type='stack', var='self.stack', label='stack（数据栈）', h=140),
        dict(type='stack', var='self.min_stack', label='min_stack（每个数入栈时的最小值）', h=140),
        dict(type='text', fn=lambda S: '两个栈==一样高==：min_stack[i] = stack[0..i] 的最小值', size=26),
        dict(type='text', fn=lambda S: (f"当前最小值 = min_stack 栈顶 = =={S['self.min_stack'][-1]}=="
                                        if S.get('self.min_stack') else '两个栈都为空'), size=28),
    ],
    watch=[('x', 'x', 'blue'), ('len(stack)', 'len(self.stack)'), ('len(min_stack)', 'len(self.min_stack)', 'green')],
    captions={
        'self.stack = []': '数据栈 `stack`：按常规方式存所有数',
        'self.min_stack = []': '辅助栈 `min_stack`：记录==每个数入栈时==的最小值',
        'if not self.min_stack': _push_if,
        'self.min_stack.append(x)': 'min_stack 压入新的最小值 `{x}`',
        'self.min_stack.append(self.min_stack[-1])': '最小值没变，min_stack 再压一份旧最小值 `{self.min_stack[-1]}`，保持两栈等高',
        'self.stack.append(x)': '`{x}` 压入数据栈',
        'self.min_stack.pop()': lambda S, B, ret: (
            f"`pop()`：min_stack 顶 `{B['self.min_stack'][-1]}` 跟着一起弹出 → 最小值==自动回到== "
            f"`{S['self.min_stack'][-1]}`"),
        'return self.stack.pop()': '数据栈弹出 `{ret}`',
        'return self.stack[-1]': '`top()`：数据栈栈顶 → 返回 =={ret}==',
        'return self.min_stack[-1]': '`getMin()`：直接看 min_stack 栈顶 → 返回 =={ret}==，==O(1)==',
    },
    cards=dict(
        one_liner='再开一个栈，记录每个数入栈时的最小值',
        complexity='所有操作 `O(1)`，空间 `O(n)`',
        problem=['设计一个栈，支持 `push / pop / top`，并能 ==O(1)== 取到最小元素 `getMin`',
                 '示例：`push(-2), push(0), push(-3)` 后 `getMin() = -3`',
                 '`pop()` 后 `top() = 0`，`getMin() = -2`'],
        quote='一个自然的想法是使用一个变量维护当前栈的最小值……但是这样做有一个问题，==当栈pop掉最小值时，这个最小值无法更新==。',
        quote_src='—— yiduobo 题解',
        idea=['于是维护住==每个数入栈时的最小值==：另开一个栈 `min_stack`',
              '`push` 时把当前最小值压入 `min_stack`',
              '`pop` 时 `min_stack` 的栈顶也一起弹掉，最小值自动回退'],
        result='返回 `[getMin, top, getMin]` = `[-3, 0, -2]` ✓',
        summary=['所有操作 `O(1)`，空间 `O(n)`（多一个等高的辅助栈）',
                 '关键：两栈==同进同出==，`min_stack[i]` 是前 `i+1` 个数的最小值',
                 '易错：只用一个变量记最小值，pop 掉最小值后就恢复不了',
                 '原文为 Python 2 写法：删去了文档字符串和 LeetCode 模板注释，逻辑未改'],
    ),
)
