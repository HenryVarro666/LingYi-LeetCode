TOK = ["3", "-7", "*", "2", "/"]
IDX = 'tokens.index(char)'  # 本例 tokens 互不相同，可以直接用 index 找到当前位置


def _idx(S):
    return S['tokens'].index(S['char']) if 'char' in S else -1


def P(v):
    return f'({v})' if v < 0 else str(v)


def show(S):
    ln = S.get('_line')
    if 'char' not in S:
        return '表达式：`3 -7 * 2 /` = `(3 × (-7)) / 2`'
    if ln == 30:
        return f'所有 token 处理完：栈里只剩 `{S["stack"][0]}`'
    c = S['char']
    if c not in '+-*/':
        return f'`"{c}"` 是数字 → `int` 后入栈'
    if ln in (5, 6):
        return f'`{c}` 是运算符 → 弹出栈顶两个数'
    if ln == 7:
        return f'先弹出右操作数 `num2 = {S["num2"]}`'
    if ln in (10, 12, 14, 24, 28):
        return f'结果 `x = {S["x"]}` → 压回栈'
    if c == '/' and 'flag' in S and 16 <= ln <= 22:
        return f'除法拆符号：`flag = {S["flag"]}`，`num1 = {S["num1"]}`，`num2 = {S["num2"]}`（负数变成绝对值）'
    return f'`num1 = {S["num1"]}`（左），`num2 = {S["num2"]}`（右），运算符 `{c}`'


CONFIG = dict(
    num=150, title='逆波兰表达式求值', difficulty='Medium', category='栈',
    author='yiduobo', technique='栈模拟 · 除法单独处理符号',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def evalRPN(self, tokens):
        stack = []

        for char in tokens:
            if char in ['+', '-', '*', '/']:
                num2 = stack.pop()
                num1 = stack.pop()
                if char == '+':
                    x = num1 + num2
                elif char == '-':
                    x = num1 - num2
                elif char == '*':
                    x = num1 * num2
                else:
                    flag = 1
                    if num1 < 0:
                        flag *= -1
                        num1 = -num1
                    if num2 < 0:
                        flag *= -1
                        num2 = -num2

                    x = num1 // num2 * flag
            else:
                x = int(char)

            stack.append(x)

        return stack[0]
''',
    call=f'Solution().evalRPN({TOK!r})',
    expect=-10,
    views=[
        dict(type='array', var='tokens', label='tokens（后缀表达式）', cell=110,
             pointers={IDX: 'blue'}, pointer_labels={IDX: 'char'},
             dim=lambda S, i, v: 'char' in S and i < _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='stack', var='stack', label='栈 stack', h=150, font=30),
        dict(type='text', fn=show, size=28, h=110),
    ],
    watch=[('char', 'char', 'blue'), ('num1', 'num1'), ('num2', 'num2', 'pink'), ('flag', 'flag'), ('x', 'x', 'green')],
    captions={
        'stack = []': '遇到数字入栈，遇到运算符弹出两个数计算',
        "if char in ['+'": lambda S, B, ret: (f'`"{S.char}"` 是运算符 → 取栈顶两个数' if S.char in '+-*/'
                                              else f'`"{S.char}"` 不是运算符 → 是数字'),
        'num2 = stack.pop()': '先弹出的是==右操作数== `num2 = {num2}`',
        'num1 = stack.pop()': '再弹出的是==左操作数== `num1 = {num1}`',
        'x = num1 + num2': lambda S, B, ret: f'`x = {S.num1} + {P(S.num2)} = {S.x}`，算完压回栈',
        'x = num1 - num2': lambda S, B, ret: f'`x = {S.num1} - {P(S.num2)} = {S.x}`，算完压回栈',
        'x = num1 * num2': lambda S, B, ret: f'`x = {S.num1} × {P(S.num2)} = {S.x}`，算完压回栈',
        'flag = 1': '除法：==先把符号单独拿出来==，`flag` 记录结果的正负',
        'if num1 < 0': lambda S, B, ret: (f'被除数 `{S.num1}` 是负数 → 记下符号' if S.num1 < 0 else f'被除数 `{S.num1}` 非负'),
        'flag *= -1': '遇到一个负数，结果符号就翻转一次：`flag = {flag}`',
        'num1 = -num1': '取绝对值：`num1 = {num1}`',
        'if num2 < 0': lambda S, B, ret: (f'除数 `{S.num2}` 是负数 → 记下符号' if S.num2 < 0 else f'除数 `{S.num2}` 非负，符号不变'),
        'num2 = -num2': '取绝对值：`num2 = {num2}`',
        'x = num1 // num2 * flag': ('两个非负数整除，再乘符号：`{num1} // {num2} × ({flag}) = {x}`'
                                   '，==向零取整==；直接 `-21 // 2` 会得到 `-11`'),
        'x = int(char)': '数字：`x = {x}`',
        'stack.append(x)': '`x = {x}` 入栈：`stack = {stack}`',
        'return stack[0]': '表达式合法 → 栈里刚好剩一个数，就是答案 =={ret}==',
    },
    cards=dict(
        one_liner='数字入栈，运算符弹两个数算完再压回；除法先拆符号再整除',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`tokens` 是逆波兰表示法（后缀表达式），算符写在两个操作数后面',
                 '计算表达式的值；整数除法==向零截断==',
                 '示例：`["2","1","+","3","*"]` → `(2 + 1) × 3 = 9`'],
        quote='遇到一个数字则将其入栈，遇到运算符则是将栈顶两个数字弹出，计算出结果之后将结果入栈。如果表达式合法，那么==最后栈中会刚好剩下一个元素==，即最终的答案。',
        quote_src='—— yiduobo 知乎题解',
        idea=['先弹出的是右操作数 `num2`，后弹出的是左操作数 `num1`',
              '原文提醒：碰到负数时整除的==取整方向不同==，需要特殊判断',
              '做法：把两个数都变成非负数整除，最后再乘上符号 `flag`'],
        result='返回 `-10`：`3 × (-7) = -21`，`-21 / 2 = -10.5` 向零取整为 `-10` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`num2` 先出栈，减法和除法别把左右写反',
                 '易错：负数整除要向零取整，Python 的 `//` 是向下取整',
                 '原文为 Python 2 写法：整数除法 `/` 已改为 `//`，并删去了文档字符串',
                 '对比灵神：只弹一个数、直接改栈顶，除法用 `trunc(a / b)`'],
    ),
)
