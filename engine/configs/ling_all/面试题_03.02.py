def _fmt(x):
    return f'{x[0]} | min {"∞" if x[1] == inf else x[1]}'


CONFIG = dict(
    num='面试题 03.02', title='栈的最小值', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='栈里额外存前缀最小值', tags=[],
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
        dict(type='stack', var='self.st', label='self.st（每项 = 元素 | 到这一层为止的最小值，栈顶在右）', fmt=_fmt, h=170, font=26),
        dict(type='text', size=28, h=110, fn=lambda S: (
            f"栈顶保存的最小值 = ==当前栈里的最小值== `{S['self.st'][-1][1]}`" if len(S.get('self.st', [])) > 1
            else '栈里只有哨兵 `(0, ∞)`')),
    ],
    watch=[('val', lambda S: S['_inner'].get('val')), ('res', 'res', 'green')],
    captions={
        'self.st = [(0, inf)]': '栈底放一个哨兵 `(0, ∞)`：它的最小值 ∞ 当作 `preMin[-1]`，==空栈也不用特判==',
        'self.st.append((val, min': '压入 `({val}, min(上一层最小值 {B["self.st"][-1][1]}, {val}))`：这一层最小值 = =={self.st[-1][1]}==',
        'self.st.pop()': '弹出栈顶：它保存的最小值跟着一起没了，下面一层的最小值==原封不动== → 现在是 `{self.st[-1][1]}`',
        'return self.st[-1][0]': '`top` 取栈顶的元素值 =={ret}==',
        'return self.st[-1][1]': '`getMin` 直接读栈顶保存的最小值 =={ret}==，不用遍历，==O(1)==',
    },
    max_steps=70,
    cards=dict(
        one_liner='每个元素旁边存一份「到此为止的最小值」，栈顶永远是答案',
        complexity='所有操作 `O(1)`，空间 `O(q)`',
        problem=['设计栈：除了 `push`、`pop`、`top`，还要支持 `getMin`',
                 '所有操作都必须是 ==O(1)==',
                 '示例：`push(-2), push(0), push(-3)` → `getMin()=-3`',
                 '`pop()` 后 `top()=0`，`getMin()=-2`'],
        quote='栈中除了保存添加的元素，还保存前缀最小值。（栈中保存的是 pair）',
        quote_src='—— 灵茶山艾府题解',
        idea=['把栈看成数组，==前缀最小值== `preMin[i] = min(preMin[i-1], nums[i])`',
              '入栈时顺手算好这一层的最小值，出栈时整层丢掉，下面的最小值本来就在',
              '栈底放 `∞` 哨兵，第一次入栈不用判断空栈'],
        result='依次返回 `[-3, 0, -2]` ✓',
        summary=['时间：所有操作 `O(1)`；空间 `O(q)`，`q` 为 push 次数',
                 '易错：不能只存一个全局最小值，pop 掉最小值后就不知道新的最小值了',
                 '哨兵 `(0, inf)` 里的 0 随便写，只有 `inf` 有用',
                 '方法二（进阶）：栈里只存 `val - mn` 的差值，用 mn 还原元素，省掉数对'],
    ),
)
