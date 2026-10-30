def _inf(x):
    return '∞' if x == inf else str(x)


OPS = 'push(-2) → push(0) → push(-3) → getMin() → pop() → top() → getMin()'

CONFIG = dict(
    num=155, title='最小栈', difficulty='Medium', category='栈',
    author='灵茶山艾府', technique='栈中额外保存前缀最小值',
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
ms.push(-2); ms.push(0); ms.push(-3)
a = ms.getMin(); ms.pop(); b = ms.top()
[a, b, ms.getMin()]''',
    expect=[-3, 0, -2],
    views=[
        dict(type='text', fn=lambda S: f'操作序列：`{OPS}`', size=24, h=90, lines=2),
        dict(type='stack', var='self.st', label='st：每项是 (val, 前缀最小值)',
             fmt=lambda x: f'({x[0]}, {_inf(x[1])})', h=130),
        dict(type='table', var=lambda S: [[x[0] for x in S['self.st']], [x[1] for x in S['self.st']]],
             label='把栈“摊开”看：min[i] = min(min[i-1], val[i])', rows=lambda S: ['val', 'min'],
             cols=lambda S: ['哨兵'] + [str(i) for i in range(len(S['self.st']) - 1)],
             color=lambda S, i, j, v: ('purple' if j == len(S['self.st']) - 1 else None), cell=90, h=280),
        dict(type='text', fn=lambda S: f"top() 读栈顶 val：`{S['self.st'][-1][0]}`　　getMin() 读栈顶 min：=={_inf(S['self.st'][-1][1])}==", size=28),
    ],
    watch=[('val', 'val', 'blue'), ('top()', 'self.st[-1][0]'), ('getMin()', 'self.st[-1][1]', 'green')],
    captions={
        'self.st = [(0, inf)]': '初始化：栈底放哨兵 `(0, ∞)`，它的前缀最小值 ==∞== 充当 `preMin[-1]`，push 时不用特判空栈',
        'self.st.append((val': lambda S, B, ret: (
            f"`push({S.val})`：新的前缀最小值 = `min({_inf(B['self.st'][-1][1])}, {S.val})` = =={S['self.st'][-1][1]}==，"
            f"连同 val 一起入栈"),
        'self.st.pop()': lambda S, B, ret: (
            f"`pop()`：弹出 `({B['self.st'][-1][0]}, {B['self.st'][-1][1]})`，它保存的最小值也一起走了，"
            f"新栈顶的 preMin = =={_inf(S['self.st'][-1][1])}== 自动就是剩下元素的最小值"),
        'return self.st[-1][0]': '`top()`：栈顶 pair 的第 0 项 → 返回 =={ret}==',
        'return self.st[-1][1]': '`getMin()`：栈顶 pair 里存的前缀最小值 → 返回 =={ret}==，==O(1)==',
    },
    cards=dict(
        one_liner='把栈看成数组，入栈时顺手记下前缀最小值',
        complexity='所有操作 `O(1)`，空间 `O(q)`',
        problem=['设计一个栈，支持 `push / pop / top`，并能 ==O(1)== 取到最小元素 `getMin`',
                 '示例：`push(-2), push(0), push(-3)` 后 `getMin() = -3`',
                 '`pop()` 后 `top() = 0`，`getMin() = -2`'],
        quote='把 nums 视作栈，本题相当于在 nums 的末尾==动态地添加/删除元素==。栈中除了保存添加的元素，还保存前缀最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['引入：前缀最小值 `preMin[i] = min(preMin[i-1], nums[i])`',
              '栈只在末尾增删 → 每个位置的前缀最小值==永远不变==，可以和元素一起存',
              '栈底放 `∞` 哨兵当 `preMin[-1]`，省掉空栈特判'],
        result='返回 `[getMin, top, getMin]` = `[-3, 0, -2]` ✓',
        after=[dict(heading='进阶：栈里只能存整数？', lines=[
            '方法二：栈中保存 `val - 之前的最小值`（差值），另用变量 `mn` 维护最小值',
            '`push`：先入栈 `val - mn`，再 `mn = min(mn, val)`',
            '`pop`：`mn -= min(栈顶, 0)`；`top`：`mn + max(栈顶, 0)`',
            '栈顶为负说明 val 就是当时的最小值，用差值即可还原上一个最小值'])],
        summary=['所有操作 `O(1)`（push 均摊），空间 `O(q)`，`q` 为 push 次数',
                 '只存一个全局最小值不行：==pop 掉最小值后无法恢复==',
                 '哨兵 `(0, ∞)`：第一个 push 时 `min(∞, val) = val`',
                 '题目保证 `pop/top/getMin` 都在非空栈上调用，哨兵不会被弹出'],
    ),
)
