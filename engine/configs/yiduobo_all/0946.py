PUSHED = [1, 2, 3, 4, 5]
POPPED = [4, 5, 3, 2, 1]


def _pp(S):
    return S.get('pop_pos', -1) if 'pop_pos' in S else -1


def _tip(S):
    if 'pop_pos' not in S or 'stack' not in S:
        return '用一个栈模拟：先入后出'
    n = len(S['popped'])
    if S['pop_pos'] >= n:
        return '出栈序列全部对上了 → ==返回 True=='
    x = S['popped'][S['pop_pos']]
    top = S['stack'][-1] if S['stack'] else '空'
    return f'这次要出栈的是 ==`{x}`==，当前栈顶是 `{top}`' + ('，对上了' if top == x else '，还没对上')


def _pc(S, i, v):
    if 'pop_pos' in S and i == S['pop_pos']:
        return 'pink'
    return None


def _uc(S, i, v):
    if 'push_pos' in S and i == S['push_pos']:
        return 'blue'
    return None


CONFIG = dict(
    num=946, title='验证栈序列', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='用栈直接模拟入栈出栈',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def validateStackSequences(self, pushed, popped):

        n = len(pushed)
        push_pos = pop_pos = 0
        stack = []
        while pop_pos < n:
            while push_pos < n and (not stack or stack[-1] != popped[pop_pos]):
                stack.append(pushed[push_pos])
                push_pos += 1
            
            if not stack or stack[-1] != popped[pop_pos]:
                return False
            
            stack.pop()
            pop_pos += 1
        
        return True
''',
    call=f'Solution().validateStackSequences({PUSHED}, {POPPED})',
    expect=True,
    views=[
        dict(type='array', var='pushed', label='pushed（入栈序列，蓝箭头 = 下一个要入栈）', cell=90, h=200,
             pointers={'push_pos': 'blue'},
             dim=lambda S, i, v: 'push_pos' in S and i < S['push_pos'],
             color=_uc),
        dict(type='array', var='popped', label='popped（出栈序列，粉箭头 = 当前要出栈）', cell=90, h=200,
             pointers={'pop_pos': 'pink'},
             dim=lambda S, i, v: 'pop_pos' in S and i < S['pop_pos'],
             color=_pc),
        dict(type='stack', var='stack', label='stack（栈顶在右）', h=140, font=32),
        dict(type='text', fn=_tip, size=28, h=80),
    ],
    watch=[('push_pos', 'push_pos', 'blue'), ('pop_pos', 'pop_pos', 'pink'), ('stack', 'stack', 'green')],
    captions={
        'n = len(pushed)': '两个序列一样长，`n = {n}`',
        'push_pos = pop_pos = 0': '两个指针：`push_pos` 管下一个==入栈==的数，`pop_pos` 管当前要==出栈==的数',
        'stack = []': '空栈，用来模拟入栈出栈',
        'while pop_pos < n': lambda S, B, r: (f'`pop_pos = {S.pop_pos} < {S.n}`：还有数要出栈，继续'
                                              if S.pop_pos < S.n else f'`pop_pos = {S.pop_pos}`：出栈序列都对上了，结束'),
        'while push_pos < n and': lambda S, B, r: (
            f'要出栈 `{S.popped[S.pop_pos]}`，栈顶 `{S.stack[-1] if S.stack else "空"}`'
            + ('（栈是空的）' if not S.stack else '')
            + (f' → 要出的数还没在栈顶，==继续入栈=='
               if S.push_pos < S.n and (not S.stack or S.stack[-1] != S.popped[S.pop_pos])
               else (' → 栈顶正好是它，停止入栈' if S.stack and S.stack[-1] == S.popped[S.pop_pos]
                     else ' → 入栈序列已经用完'))),
        'stack.append(pushed[push_pos])': '`{pushed[push_pos]}` 入栈，栈变成 `{stack}`',
        'push_pos += 1': '`push_pos` 后移到 `{push_pos}`',
        'if not stack or stack[-1] != popped[pop_pos]': lambda S, B, r: (
            f'栈顶 `{S.stack[-1]}` ≠ 要出栈的 `{S.popped[S.pop_pos]}`，入栈序列又用完了 → ==不可能达成，返回 False=='
            if (not S.stack or S.stack[-1] != S.popped[S.pop_pos])
            else f'栈顶 `{S.stack[-1]}` 正好是要出栈的 `{S.popped[S.pop_pos]}` → 可以弹出'),
        'stack.pop()': '栈顶 `{B.stack[-1]}` 出栈，栈变成 `{stack}`',
        'pop_pos += 1': '处理出栈序列的下一个：`pop_pos = {pop_pos}`',
        'return False': '无法达成，返回 `False`',
        'return True': '整个出栈序列都顺利对上，返回 ==True==',
    },
    cards=dict(
        one_liner='要出栈的数必须恰好在栈顶：不在就继续入栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给两个互不相同的整数序列 `pushed`、`popped`',
                 '问：能否对一个空栈按 `pushed` 顺序入栈、穿插出栈，得到 `popped`',
                 '示例：`[1,2,3,4,5]`、`[4,5,3,2,1]` → `true`；`[4,3,5,1,2]` → `false`'],
        quote='对于当前应该出栈的元素而言，其必须恰好是栈顶的元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历出栈序列，当前要出栈的数 `x` 必须在栈顶',
              '栈顶不是 `x` 就把入栈序列的下一个数压进去，直到栈顶是 `x` 或入栈序列用完',
              '栈顶是 `x` 就弹出，看下一个；否则说明无法达成，返回 `False`'],
        result='出栈序列全部匹配，返回 `True` ✓',
        summary=['时间 `O(n)`：每个数最多入栈一次、出栈一次；空间 `O(n)`',
                 '内层循环有两个停止条件：入栈序列用完，或栈顶正好是目标数',
                 '易错：栈为空时不能直接访问 `stack[-1]`，条件里要先判 `not stack`',
                 '原文是 Python 2 风格的类定义，在 Python 3 下无需改动，直接运行'],
    ),
)
