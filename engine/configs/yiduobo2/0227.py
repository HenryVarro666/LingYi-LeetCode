EXPR = '19-5/2*3'


def _terms(S):
    if 'stack' not in S:
        return '把算式看成若干项的加和：`19`、`-5/2*3`'
    st = S['stack']
    items = ' + '.join(f'({v})' if v < 0 else str(v) for v in st) if st else '空'
    return f"栈里的项：{items}；正在读的数 `now = {S.get('now', 0)}`，它前面的符号 `sign = '{S.get('sign', '+')}'`"


def _op_cap(S, B, ret):
    c, i = S.char, S.index
    if c in '+-*/':
        return f"读到运算符 `'{c}'`：数字 `{S.now}` 读完了 → 按它==前面==的 `sign = '{S.sign}'` 处理"
    if i == len(S.s) - 1:
        return f"已经是最后一个字符：最后一个数字 `{S.now}` 也要按 `sign = '{S.sign}'` 处理"
    return f"`'{c}'` 后面可能还有数字，继续读"


def _sign_cap(op, yes):
    def f(S, B, ret):
        if S.sign == op:
            return yes
        return f"`sign = '{S.sign}'`，不是 `{op}`"
    return f


def _neg_cap(S, B, ret):
    if S.x < 0:
        return f'`x = {S.x} < 0`：Python 的 `//` 是==向下取整==，负数要先取反再除，才能向零取整'
    return f'`x = {S.x} ≥ 0`：直接整除'


def _ret_cap(S, B, ret):
    st = S.stack
    expr = ' + '.join(f'({v})' if v < 0 else str(v) for v in st)
    return f'把栈中各项加起来：`{expr} = {ret}`'


CONFIG = dict(
    num=227, title='基本计算器 II', difficulty='Medium', category='栈',
    author='yiduobo', technique='栈 · 乘除先算，加减入栈',
    tags=['热题173'],
    code='''
class Solution(object):
    def calculate(self, s):
        stack = []
        sign = '+'
        now = 0
        for index, char in enumerate(s):
            if char.isdigit():
                now = now * 10 + int(char)
            if char in '+-*/' or index == len(s) - 1:
                if sign == '+':
                    stack.append(now)
                elif sign == '-':
                    stack.append(-now)
                elif sign == '*':
                    stack.append(stack.pop() * now)
                elif sign == '/':
                    x = stack.pop()
                    if x < 0:
                        stack.append(-(-x // now))
                    else:
                        stack.append(x // now)

                sign = char
                now = 0

        return sum(stack)
''',
    call=f'Solution().calculate({EXPR!r})',
    expect=13,
    skip=['for index, char', 'if char.isdigit()', 24],
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符 char）', cell=84, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('index') else None,
             dim=lambda S, i, v: S.get('index') is not None and i < S['index']),
        dict(type='text', h=90, fn=_terms, size=25, lines=2),
        dict(type='stack', var='stack', label='stack（待加和的各项）', h=130, font=30),
    ],
    watch=[('char', 'char', 'blue'), ('now', 'now', 'yellow'), ('sign', 'sign', 'orange'), ('x', 'x', 'pink'),
           ('stack', 'stack', 'green')],
    captions={
        'stack = []': '栈存放==待加和的各项==：乘除先算好再放进去',
        "sign = '+'": '`sign`：当前数字==前面==的运算符，开头视为 `+`',
        5: '`now`：正在读的数字',
        'now = now * 10': lambda S, B, ret: f"读到数字 `'{S.char}'`：`now = {B.now}×10 + {S.char} = {S.now}`",
        "if char in '+-*/'": _op_cap,
        "if sign == '+'": _sign_cap('+', '`sign` 是 `+` → `now` 原样入栈'),
        'stack.append(now)': '入栈 `{now}`',
        "elif sign == '-'": _sign_cap('-', '`sign` 是 `-` → 看成==负数==入栈：减法变成加一个负数'),
        'stack.append(-now)': '入栈 `{-now}`',
        "elif sign == '*'": _sign_cap('*', '`sign` 是 `*` → ==乘法优先==：被乘数一定在栈顶'),
        'stack.append(stack.pop() * now)': lambda S, B, ret: f'弹出栈顶 `{B.stack[-1]}`，`{B.stack[-1]} × {S.now} = {S.stack[-1]}` 再入栈',
        "elif sign == '/'": _sign_cap('/', '`sign` 是 `/` → ==除法优先==：被除数在栈顶'),
        'x = stack.pop()': '弹出被除数 `x = {x}`（除数是 `now = {now}`，别搞反）',
        'if x < 0': _neg_cap,
        'stack.append(-(-x // now))': lambda S, B, ret: (f'`-({-S.x} // {S.now}) = {S.stack[-1]}` 入栈'
                                                       f'（直接 `{S.x} // {S.now}` 会得到 `{S.x // S.now}`，错）'),
        'stack.append(x // now)': '`{x} // {now} = {stack[-1]}` 入栈',
        'sign = char': lambda S, B, ret: (f"记下新符号 `sign = '{S.sign}'`，留给下一个数字；`now` 清零"
                                          if S.index < len(S.s) - 1 else '已经处理完最后一个数字（这里的 `sign`、`now` 不会再用到）'),
        'return sum(stack)': _ret_cap,
    },
    cards=dict(
        one_liner='乘除先算：加减号把数连符号入栈，乘除号弹出栈顶算完再入栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你字符串表达式 `s`（非负整数和 `+ - * /`，可能有空格，没有括号），计算它的值',
                 '整数除法==向零截断==',
                 '示例：`"3+2*2"` → `7`；`" 3/2 "` → `1`；`" 3+5 / 2 "` → `5`',
                 '本视频：`"19-5/2*3"` → `19 - 2×3 = 13`'],
        quote='考虑到乘法与除法需要优先计算，那么被乘数与被除数，以及在乘法和除法之前的算式结果就需要保存起来……因此，==栈是一个很好地选择，因为取被乘数与被除数都是取最近的那个==，正好是后进先出。',
        quote_src='—— yiduobo 题解原文',
        idea=['把整个式子看成若干个整数、乘法算式、除法算式的==加和==；减法看成负数',
              '遇到运算符时，式子一定是 `sign X char`：按 X ==前面==的 `sign` 处理 X',
              '`+`/`-`：X 带符号入栈；`*`/`/`：弹出栈顶和 X 算完再入栈；最后求和'],
        result='运行结束，返回 `13`：栈里是 `19` 和 `-6`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（还删去了 docstring）',
                 '易错：Python 的 `//` 向下取整，`-5 // 2 = -3`；负数先取反再除才是向零截断',
                 '最后一个数字后面没有运算符，要用 `index == len(s) - 1` 触发处理',
                 '同类：224 基本计算器（带括号）'],
    ),
)
