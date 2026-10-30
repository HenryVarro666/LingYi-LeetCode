_NAME = {'a': 'add', 's': 'sub', 'm': 'mul', 'd': 'div'}
_SYM = {'a': '+', 's': '-', 'm': '×', 'd': '//'}


def _top(S):
    e = S.get('expression')
    if e is None or 'p' not in S or 'stack' not in S:
        return '用栈存「待运算的运算符」和「还没有 b 的 a」'
    p = S['p']
    ln = S.get('_line')
    if ln in range(14, 25) and 'x' in S and 'o' in S:
        return f"弹出 `{S['x']}`（a）和 `{_NAME[S['o']]}`，算 `a {_SYM[S['o']]} b`，此时 b = `{S['y']}`"
    if p < len(e):
        return f"栈 `{S['stack']}`"
    return f"表达式扫完，栈里剩 `{S['stack']}`"


def _col(S, i, v):
    if 'p' not in S or 'expression' not in S:
        return None
    p = S['p']
    if ln_in_num(S) and 'q' in S and p <= i < S['q']:
        return 'green'
    if i == p:
        return 'blue'
    return None


def ln_in_num(S):
    return 'y' in S and S.get('_line') in range(10, 29)


CONFIG = dict(
    num=3749, title='计算有效表达式', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈 · 运算符先入栈，凑齐 a、b 再算',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def evaluateExpression(self, expression):
        
        stack = []
        p = 0
        op = set(['a', 's', 'm', 'd'])
        while p < len(expression):
            if '0' <= expression[p] <= '9' or expression[p] == '-':
                q = p + 1
                while q < len(expression) and '0' <= expression[q] <= '9':
                    q += 1
                y = int(expression[p: q])
                while stack and stack[-1] not in op:
                    x = stack.pop()
                    o = stack.pop()
                    if o == 'a':
                        x += y
                    elif o == 's':
                        x -= y
                    elif o == 'm':
                        x *= y
                    else:
                        x //= y
                    y = x
                
                stack.append(y)
                p = q + 1

            elif expression[p] == ')' or expression[p] == ',':
                p += 1
            else:
                stack.append(expression[p])
                p += 4
        
        return stack[-1]
''',
    call='Solution().evaluateExpression("add(2,mul(3,sub(7,4)))")',
    expect=11,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='string', var='expression', label='expression（蓝 = 当前下标 p，绿 = 正在读的整数）', cell=44,
             pointers={'p': 'blue'}, color=_col, dim=lambda S, i, v: 'p' in S and i < S['p'], h=200),
        dict(type='stack', var='stack', label='stack（栈顶在右：运算符字母 或 已求出的整数）', fmt=lambda x: str(x), h=200, font=34),
    ],
    max_steps=95,
    watch=[('p', 'p', 'blue'), ('y', 'y', 'green'), ('x', 'x', 'yellow'), ('o', 'o', 'orange')],
    captions={
        'stack = []': '栈里要放两种东西：==运算符==（a/s/m/d）和==已经算好的数==',
        'p = 0': '`p` 从头向后扫',
        'op = set': '`op` 是四个运算符首字母：add / sub / mul / div',
        'while p < len': lambda S, B, r: (f"`p = {S.p}`，`expression[{S.p}] = '{S.expression[S.p]}'`" if S.p < len(S.expression) else '`p` 走到末尾，扫描结束'),
        "if '0' <= expression[p] <= '9' or": lambda S, B, r: ("是数字（或负号）→ 一个整数的开头" if S.expression[S.p].isdigit() or S.expression[S.p] == '-' else f"`'{S.expression[S.p]}'` 不是数字也不是负号"),
        'q = p + 1': '`q` 从 `p+1` 往右找这个整数的结尾',
        'while q < len': lambda S, B, r: (f"`expression[{S.q}] = '{S.expression[S.q]}'` 是数字 → 整数还没结束" if S.q < len(S.expression) and S.expression[S.q].isdigit() else '整数到此结束'),
        'q += 1': '`q` → {q}',
        'y = int(': '整数是 `expression[{p}:{q}]` → `y = {y}`',
        'while stack and stack[-1] not in op': lambda S, B, r: (f"栈顶 `{S.stack[-1]}` 不是运算符，是 a → a、b 凑齐了，可以算" if S.stack and not isinstance(S.stack[-1], str) else ('栈空或栈顶是运算符 → b 还不能算，先把 y 压栈' if True else '')),
        'x = stack.pop()': '弹出栈顶：`x` = a = `{x}`',
        'o = stack.pop()': '再弹出：`o = {o!r}` 是这对 a、b 的运算符',
        "if o == 'a'": lambda S, B, r: f"运算符是 `{S.o}`（{_NAME[S.o]}）",
        "x += y": '`a + b`：x → `{x}`',
        "x -= y": '`a - b`：x → `{x}`（顺序是 a 在前）',
        "x *= y": '`a × b`：x → `{x}`',
        "x //= y": '`a // b`：x → `{x}`（整除）',
        'y = x': '运算结果当作新的 `y = {y}`，==继续看更外层==能不能算（嵌套）',
        'stack.append(y)': lambda S, B, r: f'`{S.y}` 压栈：它是别人的 a，或者是最终答案 → 栈 `{S.stack}`',
        'p = q + 1': '`p` 跳到数字后面，顺便跳过一个 `,` 或 `)` → `p = {p}`',
        "expression[p] == ')' or": lambda S, B, r: ('是 `)` 或 `,` → 只是分隔符' if S.expression[S.p] in '),' else '是运算符开头 → 入栈'),
        'p += 1': '分隔符直接跳过，`p` → {p}',
        'stack.append(expression[p])': lambda S, B, r: f"`'{S.expression[S.p]}'` 是运算符 {_NAME[S.expression[S.p]]} → 压栈等它的 a、b",
        'p += 4': '运算符名字 3 个字母再加 `(`，共跳 4 位 → `p = {p}`',
        'return stack[-1]': '栈里只剩最终结果：`{stack[-1]}`',
    },
    cards=dict(
        one_liner='运算符先压栈，数字一出现就尽量往外归并',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['表达式要么是整数，要么是 `op(a, b)`，`op` 为 `add/sub/mul/div`（整除）',
                 '`a`、`b` 本身也是有效表达式，可以嵌套',
                 '本视频：`add(2,mul(3,sub(7,4)))` → `11`'],
        quote='于是只需使用一个变量p，从头开始向后移动，在这个过程中使用栈来记录待运算的运算符以及还没有确定对应的b的a。',
        quote_src='—— yiduobo 题解原文',
        idea=['遇到运算符字母就压栈，`p` 跳 4 位越过 `add(`',
              '读到整数 `y`：栈顶若是数 `x`，说明 `x` 是 a、`y` 是 b，弹出 `x` 和运算符算一次',
              '算出的结果又是新的 `y`，循环检查更外层，直到栈顶是运算符或栈空'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`sub` 是 `a - b`，弹出的 `x` 是 a，`y` 是 b，顺序别反',
                 '易错：负数以 `-` 开头，要和数字一起读',
                 '易错：算完一对后必须继续循环，嵌套的外层可能也凑齐了',
                 '原文用 `//` 做整除，已是 Python 3 写法，无修改'],
    ),
)
