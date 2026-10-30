OPS = ["5", "2", "C", "D", "+"]   # 示例 1
IDX = 'ops.index(op)'


def _idx(S):
    return S['ops'].index(S['op']) if 'op' in S else -1


def cap_branch(word, hit):
    def f(S, B, ret):
        op = S.op
        if op == hit:
            return f'`op = "{op}"` ==是== `{word}`'
        return f'`"{op}"` 不是 `{word}`'
    return f


def recent(S):
    st = S.get('stack')
    if st is None:
        return '特殊操作只和==最近一两次得分==有关 → 栈'
    if not st:
        return '栈空'
    if len(st) == 1:
        return f'最近一次得分 `stack[-1] = {st[-1]}`'
    return f'最近两次得分 `stack[-2] = {st[-2]}`，`stack[-1] = {st[-1]}`'


CONFIG = dict(
    num=682, title='棒球比赛', difficulty='Easy', category='栈',
    author='yiduobo', technique='栈维护得分序列，操作栈顶',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def calPoints(self, ops):
        stack = []
        for op in ops:
            if op == 'C':
                stack.pop()
            elif op == 'D':
                stack.append(stack[-1] * 2)
            elif op == '+':
                stack.append(stack[-1] + stack[-2])
            else:
                stack.append(int(op))

        return sum(stack)
''',
    call=f'Solution().calPoints({OPS!r})',
    expect=30,
    views=[
        dict(type='array', var='ops', label='ops（记录操作）', cell=110,
             pointers={IDX: 'blue'}, pointer_labels={IDX: 'op'},
             dim=lambda S, i, v: 'op' in S and i < _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='stack', var='stack', label='stack（得分序列，栈顶在右）', h=160, font=32),
        dict(type='text', fn=recent, size=28, h=100),
    ],
    watch=[('op', 'op', 'blue'), ('stack', 'stack', 'green')],
    captions={
        'stack = []': '用栈维护==得分序列==：特殊操作都只看栈顶',
        'for op in ops': lambda S, B, ret: (f'下一条操作：`"{S.op}"`'
                                            if 'op' not in B or B.op != S.op else '操作全部记录完'),
        "if op == 'C'": cap_branch('"C"', 'C'),
        'stack.pop()': '`"C"`：前一次得分 `{B.stack[-1]}` 无效 → ==弹出栈顶==，它从此不参与后面的计算',
        "elif op == 'D'": cap_branch('"D"', 'D'),
        'stack.append(stack[-1] * 2)': '`"D"`：栈顶 `{B.stack[-1]}` × 2 = =={stack[-1]}== 入栈',
        "elif op == '+'": cap_branch('"+"', '+'),
        'stack.append(stack[-1] + stack[-2])': '`"+"`：栈顶两个数 `{B.stack[-1]} + {B.stack[-2]}` = =={stack[-1]}== 入栈',
        'stack.append(int(op))': '不是特殊操作 → 是整数：`int("{op}") = {stack[-1]}` 入栈',
        'return sum(stack)': '栈里剩下的就是所有有效得分：`sum = {ret}`',
    },
    cards=dict(
        one_liner='特殊操作只看最近一两次得分 → 用栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['按顺序记录 `ops`：整数 `x` 表示本回合得 `x` 分',
                 '`"+"` 前两次得分之和，`"D"` 前一次得分的两倍，`"C"` 前一次得分作废',
                 '返回所有有效得分的总和',
                 '示例：`["5","2","C","D","+"]` → `[5,10,15]` → `30`'],
        quote='注意到题目中的所有特殊操作都跟最近的一次或者两次得分有关，因此很自然就想到使用栈来维护得分的序列，而特殊操作则通过操作栈顶元素来完成。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`"C"` 删最近一次 → `pop`；`"D"`、`"+"` 读最近一两次 → `stack[-1]`、`stack[-2]`',
              '只和==最近==的元素打交道，后进先出 → 栈',
              '最后栈里剩下的都是有效得分，求和即可'],
        result='栈 `[5, 10, 15]`，返回 `30` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先判断 `"C"`/`"D"`/`"+"`，其余都当整数：`"-2"` 这类负数也能被 `int` 正确解析',
                 '易错：`"C"` 后，`"D"` 要用==被删之前的那一项==，栈会自动帮你回到它',
                 '原文为 Python 2 风格（类型写在文档字符串里），已删去文档字符串，代码未改'],
    ),
)
