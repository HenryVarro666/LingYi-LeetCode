CONFIG = dict(
    num=772, title='基本计算器 III', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='数值栈 + 运算符栈',
    tags=['常用数据结构', '栈'],
    code='''
class Solution(object):
    def calculate(self, s):

        num_stack = []
        op_stack = []
        n = len(s)
        p = 0

        def calc(x, y, op):
            if op == '+':
                return x + y
            elif op == '-':
                return x - y
            elif op == '*':
                return x * y
            else:
                print(x, y)
                if x < 0:
                    if y < 0:
                        return x // y
                    else:
                        return -(-x // y)
                elif y < 0:
                    return -(x // -y)
                else:
                    return x // y

        while p < n:
            if '0' <= s[p] <= '9':
                now = 0
                while p < n and '0' <= s[p] <= '9':
                    now = now * 10 + int(s[p])
                    p += 1
                num_stack.append(now)

            elif s[p] == '+' or s[p] == '-':
                while op_stack and op_stack[-1] != '(' and op_stack[-1] != ')':
                    y, x = num_stack.pop(), num_stack.pop()
                    op = op_stack.pop()
                    num_stack.append(calc(x, y, op))
                
                op_stack.append(s[p])
                p += 1
            
            elif s[p] == '*' or s[p] == '/':
                while op_stack and (op_stack[-1] == '*' or op_stack[-1] == '/'):
                    y, x = num_stack.pop(), num_stack.pop()
                    op = op_stack.pop()
                    num_stack.append(calc(x, y, op))
                
                op_stack.append(s[p])
                p += 1
            
            elif s[p] == '(':
                op_stack.append(s[p])
                p += 1
            else:
                while op_stack[-1] != '(':
                    y, x = num_stack.pop(), num_stack.pop()
                    op = op_stack.pop()
                    num_stack.append(calc(x, y, op))
                op_stack.pop()
                p += 1

        while op_stack:
            y, x = num_stack.pop(), num_stack.pop()
            op = op_stack.pop()
            num_stack.append(calc(x, y, op))
        
        return num_stack[-1]
''',
    call='Solution().calculate("2*(3+4)-6/2")',
    expect=11,
    views=[
        dict(type='string', var='s', label='表达式 s（蓝箭头 = 当前字符 p）', cell=64, h=200, pointers={'p': 'blue'},
             dim=lambda S, i, v: i < S['p']),
        dict(type='stack', var='num_stack', label='num_stack（数值栈，栈顶在右）', h=120, font=30),
        dict(type='stack', var='op_stack', label='op_stack（运算符栈，栈顶在右）', h=120, font=30),
    ],
    watch=[('p', 'p', 'blue'), ('num_stack', 'num_stack', 'green'), ('op_stack', 'op_stack', 'pink')],
    skip=['n = len(s)', 'now = 0', 'y, x = num_stack.pop()', 'op = op_stack.pop()', 'print(x, y)', 'p += 1', 'while p < n:',
          "if op == '+'", "elif op == '-'", "elif op == '*'", 'if x < 0', 'if y < 0', 'elif y < 0'],
    captions={
        'num_stack = []': '两个栈：==数值栈==放操作数，==运算符栈==放还不能算的运算符',
        'p = 0': '`p` 从左往右扫描表达式',
        "while p < n and": lambda S, B, r: (f'`s[{S.p}] = "{S.s[S.p]}"` 还是数字 → 继续拼' if S.p < S.n and '0' <= S.s[S.p] <= '9'
                                            else '数字到此结束（遇到非数字或表达式末尾）'),
        "if '0' <= s[p] <= '9'": lambda S, B, r: (f'`s[{S.p}] = "{S.s[S.p]}"` 是数字 → 向右读完整个多位数' if '0' <= S.s[S.p] <= '9'
                                                   else f'`s[{S.p}] = "{S.s[S.p]}"` 不是数字 → 看是不是运算符或括号'),
        'now = now * 10': '`now = {now}`：把这一位拼进多位数',
        'num_stack.append(now)': '数字读完，`{now}` 入数值栈：`{num_stack}`',
        "elif s[p] == '+'": lambda S, B, r: (f'`s[{S.p}] = "{S.s[S.p]}"` 是 `+` / `-` → 优先级最低，栈里除左括号外的运算都能先算了'
                                              if S.s[S.p] in '+-' else f'`"{S.s[S.p]}"` 不是加减 → 看乘除'),
        "while op_stack and op_stack[-1] != '('": lambda S, B, r: (
            f'栈顶运算符 `{S.op_stack[-1]}` 不是括号 → ==先把它算掉==，再处理新的加减号' if S.op_stack and S.op_stack[-1] not in '()'
            else '栈空或栈顶是 `(` → 不能越过括号往下算，停'),
        "elif s[p] == '*'": lambda S, B, r: (f'`s[{S.p}] = "{S.s[S.p]}"` 是 `*` / `/`' if S.s[S.p] in '*/' else f'`"{S.s[S.p]}"` 不是乘除 → 看括号'),
        "while op_stack and (op_stack[-1] == '*'": lambda S, B, r: (
            f'栈顶 `{S.op_stack[-1]}` 也是乘除，优先级相同 → ==先算栈顶=='
            if S.op_stack and S.op_stack[-1] in '*/' else '栈顶不是乘除（空、加减或括号）→ 新的乘除可以压着它，先不算'),
        'return x + y': '加法：`{x} + {y}` = =={ret}==',
        'return x - y': '减法：`{x} - {y}` = =={ret}==（x 是先入栈的左操作数）',
        'return x * y': '乘法：`{x} * {y}` = =={ret}==',
        'return x // y': '除法：`{x} // {y}` = =={ret}==（原文分情况处理负数，向 0 截断）',
        'num_stack.append(calc': lambda S, B, r: f'弹出栈顶两个数 `{S.x}`、`{S.y}` 和运算符 `{S.op}`，调用 `calc` 算 `{S.x} {S.op} {S.y}`',
        'op_stack.append(s[p])': '新运算符 `{s[p]}` 入栈：`{op_stack}`（还缺右操作数，不能算）',
        "elif s[p] == '('": lambda S, B, r: (f'`s[{S.p}]` 是 `(`' if S.s[S.p] == '(' else f'`s[{S.p}]` 只剩 `)`'),
        'while op_stack[-1] != ': lambda S, B, r: (
            f'遇到 `)`：一路算到栈顶是 `(` 为止，现在栈顶 `{S.op_stack[-1]}`' + ('，还要算' if S.op_stack[-1] != '(' else ' → 括号内算完')),
        'op_stack.pop()': '弹出 `(`，括号内的值已留在数值栈顶',
        'while op_stack:': lambda S, B, r: (f'扫完后栈里还剩 `{S.op_stack}` → 继续从栈顶往下算' if S.op_stack else '运算符栈空了，数值栈只剩一个数'),
        'return num_stack[-1]': '数值栈唯一的数就是答案 =={ret}==',
    },
    max_steps=110,

    cards=dict(
        one_liner='两个栈：数字进数值栈，运算符等到优先级明确后才算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给含 `+ - * /` 和括号的表达式字符串，求值',
                 '整数除法向 0 截断；表达式合法，无空格',
                 '本视频：`"2*(3+4)-6/2"` → `11`'],
        quote='对于一个新到来的运算符，其可能确立了栈顶运算符的优先级以及运算对象，因此就可以将栈顶运算符未完成的运算给完成掉。',
        quote_src='—— yiduobo 题解原文',
        idea=['运算符暂不算，原因：右操作数未知，或优先级未定 → 存进栈',
              '新到 `+ -`：栈里直到 `(` 为止的运算全算掉；新到 `* /`：只算栈顶的 `* /`',
              '`(` 直接入栈；`)` 一路算到 `(` 并弹掉；最后清空栈'],
        result='表达式求值完成 `2*7 − 3 = 11` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：多位数要连续读完；`)` 到来时必须算到 `(` 才停',
                 '易错：`*` `/` 只能算栈顶的 `*` `/`，不能越过 `+ -`',
                 '原文为 Python 2 写法，`print x, y` 已改为 `print(x, y)`，整数除法 `/` 已改为 `//`',
                 '同类题：224、227 基本计算器；1597 用同一套栈法建表达式树'],
    ),
)
