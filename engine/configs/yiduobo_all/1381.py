def _real(S):
    """栈中每个元素“实际应有的值” = 原值 + 之后所有 add_list[j]（j >= i）之和"""
    st, ad = S.get('self.stack'), S.get('self.add_list')
    if st is None or ad is None:
        return None
    return [v + sum(ad[i:]) for i, v in enumerate(st)]


def _tip(S):
    st = S.get('self.stack')
    if st is None:
        return '栈 + 延迟更新：`increment` 只记账，不真的去改栈底元素'
    ln = S.get('_line')
    if ln in (19, 20, 21):
        return '`pop` 时才兑现：把栈顶的欠账结清，剩下的账传给下一个位置'
    if not st:
        return '栈是空的'
    real = _real(S)
    return f'栈里每个元素实际该是 `{real}`（原值 + 它名下的所有延迟增量）'


CONFIG = dict(
    num=1381, title='设计一个支持增量操作的栈', difficulty='Medium', category='设计',
    author='yiduobo', technique='栈 + 延迟更新 add_list',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class CustomStack(object):

    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.stack = []
        self.add_list = [0] * maxSize

    def push(self, x):
        if len(self.stack) < self.maxSize:
            self.stack.append(x)

    def pop(self):
        l = len(self.stack) - 1
        if l < 0:
            return -1

        delta = self.add_list[l]
        if l > 0:
            self.add_list[l - 1] += delta
        self.add_list[l] = 0
        return self.stack.pop() + delta

    def increment(self, k, val):
        if k > len(self.stack):
            k = len(self.stack)
        if k > 0:
            self.add_list[k - 1] += val
''',
    call='''c = CustomStack(3)
out = []
c.push(1)
c.push(2)
out.append(c.pop())
c.push(2)
c.push(3)
c.push(4)
c.increment(5, 100)
c.increment(2, 100)
out.append(c.pop())
out.append(c.pop())
out.append(c.pop())
out.append(c.pop())
out''',
    expect=[2, 103, 202, 201, -1],
    views=[
        dict(type='array', var='self.stack', label='stack（下标 0 是栈底，栈顶在右）', cell=100, h=225, min_slots=3,
             pointers={'l if l >= 0 else None': 'pink'}, pointer_labels={'l if l >= 0 else None': 'l 栈顶'}),
        dict(type='array', var='self.add_list', label='add_list[i]：栈底 i+1 个元素还欠的增量（黄框 = 刚改动）',
             cell=100, h=215,
             pointers={'k - 1 if k > 0 else None': 'blue', 'l if l >= 0 else None': 'pink'},
             pointer_labels={'k - 1 if k > 0 else None': 'k-1 记账', 'l if l >= 0 else None': 'l 取账'}),
        dict(type='text', fn=_tip, size=26, h=100, lines=2),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=[('l', 'l', 'pink'), ('delta', 'delta', 'yellow'), ('k', 'k', 'blue'), ('val', 'val', 'blue')],
    max_steps=110,
    captions={
        'self.maxSize = maxSize': '`CustomStack({maxSize})`：最多放 `{maxSize}` 个数',
        'self.stack = []': '`stack`：存放真正的数',
        'self.add_list = [0] * maxSize': '`add_list` 是==欠账本==：`add_list[i]` 表示栈底 `i + 1` 个元素还要各加多少，开始都是 0',
        'if len(self.stack) < self.maxSize': lambda S, B, r: (
            f'`push({S.x})`：栈里 `{len(S["self.stack"])}` 个 < `maxSize = {S["self.maxSize"]}`，可以放'
            if len(S['self.stack']) < S['self.maxSize']
            else f'`push({S.x})`：栈里已有 `{len(S["self.stack"])}` 个，==满了，直接忽略=='),
        'self.stack.append(x)': '`{x}` 入栈。==push 不碰 add_list==，欠账本保持原样',
        'l = len(self.stack) - 1': '`pop()`：先看栈顶下标 `l = {l}`（栈空时是 -1）',
        'if l < 0': lambda S, B, r: ('`l = -1`：栈是空的' if S.l < 0 else f'`l = {S.l}` ≥ 0：栈不空，继续'),
        'return -1': '空栈直接返回 `-1`',
        'delta = self.add_list[l]': '查账本：`delta = add_list[{l}] = {delta}`，栈顶这个元素该加上它',
        'if l > 0': lambda S, B, r: (
            f'下面还有 `{S.l}` 个元素，它们也欠着这笔账，要传下去'
            if S.l > 0 else '栈顶就是栈底，下面没人了，不用再传'),
        'self.add_list[l - 1] += delta': lambda S, B, r: (
            '`delta = 0`，没有账要传，`add_list[{}]` 不变'.format(S.l - 1) if S.delta == 0 else
            f'==账往下传==：`add_list[{S.l - 1}] += {S.delta}` → `{S["self.add_list"][S.l - 1]}`。下面的元素没出栈前，这笔账还得算上它们'),
        'self.add_list[l] = 0': '`add_list[{l}]` 的账已兑现，清零',
        'return self.stack.pop() + delta': '弹出栈顶（原值 `{ret - delta}`），加上欠账 `{delta}` → 返回 =={ret}==',
        'if k > len(self.stack)': lambda S, B, r: (
            f'`increment({S.k}, {S.val})`：`k = {S.k}` 比栈里的 `{len(S["self.stack"])}` 个还多 → 最多只能加到栈顶'
            if S.k > len(S['self.stack']) else
            f'`increment({S.k}, {S.val})`：`k = {S.k}` ≤ 栈里的 `{len(S["self.stack"])}` 个，不用截断'),
        'k = len(self.stack)': '`k` 改成栈里的元素个数 `{k}`',
        'if k > 0': lambda S, B, r: ('`k > 0`：有元素要加' if S.k > 0 else '栈是空的，没有元素可加，什么也不做'),
        'self.add_list[k - 1] += val': '==延迟更新==：不去改栈底 `{k}` 个元素，只在 `add_list[{k - 1}]` 记账 `+{val}` → `{self.add_list[k - 1]}`，`O(1)`',
    },
    cards=dict(
        one_liner='increment 只记账，等 pop 到那个元素时再兑现',
        complexity='每个操作 `O(1)`，空间 `O(maxSize)`',
        problem=['设计栈 `CustomStack(maxSize)`：`push`、`pop`，栈满时 `push` 无效，栈空时 `pop` 返回 `-1`',
                 '`increment(k, val)`：给栈底的前 `k` 个元素都加上 `val`',
                 '朴素做法每次都老老实实加，时间太高',
                 '本视频：`maxSize = 3`，操作后 `pop` 依次返回 `[2, 103, 202, 201, -1]`'],
        quote='注意到栈先进后出的特性，我们可以利用延迟更新来做这个inc。',
        quote_src='—— yiduobo 题解原文',
        idea=['`increment` 时只在 `add_list[k - 1]` 上记 `+val`，表示栈底 `k` 个元素之后都要加',
              '`pop` 时取 `delta = add_list[l]` 加到栈顶，并把账传给 `add_list[l - 1]`',
              '栈底 `l - 1` 个元素出栈前，第 `l` 个必先出栈 → 在它出栈时传账，正确性有保证'],
        result='`pop` 依次返回 `[2, 103, 202, 201, -1]` ✓',
        summary=['`push`、`pop`、`increment` 全是 `O(1)`，空间 `O(maxSize)`',
                 '`k` 超过栈内元素个数时要先截成 `len(stack)`',
                 '易错：`pop` 取走账以后要清零，同时把账传给下一个位置（`l > 0` 时）',
                 '原文为 Python 2 风格，代码无需改动；这里只是把示例操作串成一段可运行的调用'],
    ),
)
