TOK = ["4", "-13", "5", "/", "+"]
IDX = 'tokens.index(token)'  # 本例 tokens 互不相同，可以直接用 index 找到当前位置


def _idx(S):
    return S['tokens'].index(S['token']) if 'token' in S else -1


def cap_kind(S, B, ret):
    t = S.token
    if len(t) > 1:
        return f'`"{t}"` 长度 > 1 → 是数字（==负数以 `-` 开头==，只看 `isdigit()` 会误判成减号）'
    if t[0].isdigit():
        return f'`"{t}"` 是数字字符 → 是数字'
    return f'`"{t}"` 长度为 1 且不是数字 → 是==运算符=='


def P(v):
    return f'({v})' if v < 0 else str(v)


def cap_div(S, B, ret):
    y, x = B.st[-1], S.x
    return (f'`{y} / {P(x)} = {y / x:g}`，==向零取整== → `{S.st[-1]}`'
            f'（若用 `//` 会向下取整得到 `{y // x}`，错！）')


def show(S):
    k = _idx(S)
    ln = S.get('_line')
    if k < 0:
        return '逆波兰表达式：`4 -13 5 / +` = `4 + (-13 / 5)`'
    t = S['token']
    if len(t) > 1 or t[0].isdigit():
        return f'`"{t}"` 是数字 → 入栈，等待运算符'
    if ln in (4, 5):
        return f'`{t}` 是运算符 → 用栈顶的两个数计算'
    if ln == 9:
        return f'弹出右操作数 `x = {S["x"]}`，左操作数==还留在栈顶== `{S["st"][-1]}`'
    if ln in (10, 12, 14):
        return f'左 `st[-1] = {S["st"][-1]}`，右 `x = {S["x"]}`：看看是哪种运算'
    return f'结果直接写回栈顶 → `st[-1] = {S["st"][-1]}`'


CONFIG = dict(
    num=150, title='逆波兰表达式求值', difficulty='Medium', category='栈',
    author='灵茶山艾府', technique='栈模拟 · 弹一个数，直接改栈顶',
    tags=['面试经典150'],
    setup='from math import trunc',
    code='''
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        st = []
        for token in tokens:
            if len(token) > 1 or token[0].isdigit():  # token 是数字
                st.append(int(token))
                continue

            x = st.pop()
            if token == '+':
                st[-1] += x
            elif token == '-':
                st[-1] -= x
            elif token == '*':
                st[-1] *= x
            else:
                # 题目要求除法向零取整，但 // 是向下取整
                st[-1] = trunc(st[-1] / x)  # 不用浮点数的写法见【Python3 写法二】
        return st[0]
''',
    call=f'Solution().evalRPN({TOK!r})',
    expect=2,
    views=[
        dict(type='array', var='tokens', label='tokens（后缀表达式）', cell=110,
             pointers={IDX: 'blue'}, pointer_labels={IDX: 'token'},
             dim=lambda S, i, v: 'token' in S and i < _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='stack', var='st', label='栈 st', h=150, font=30),
        dict(type='text', fn=show, size=28, h=110),
    ],
    watch=[('token', 'token', 'blue'), ('x', 'x', 'pink'), ('st', 'st', 'green')],
    skip=['continue'],
    captions={
        'st = []': '栈 `st` 存==还没参与运算的数==',
        'if len(token) > 1': cap_kind,
        'st.append(int(token))': '转成整数入栈：`st = {st}`',
        'x = st.pop()': '弹出栈顶 `x = {x}`：==它是运算符右边的数==（减法、除法要分清左右）',
        'st[-1] += x': lambda S, B, ret: f'`{B.st[-1]} + {P(S.x)} = {S.st[-1]}`：不用再弹出左操作数，==直接改栈顶==',
        'st[-1] -= x': '`{B.st[-1]} - {x} = {st[-1]}`：直接改栈顶',
        'st[-1] *= x': '`{B.st[-1]} × {x} = {st[-1]}`：直接改栈顶',
        'st[-1] = trunc': cap_div,
        'return st[0]': '表达式算完，栈里只剩一个数：答案 =={ret}==',
    },
    cards=dict(
        one_liner='数字入栈；遇到运算符，弹出一个数，直接修改栈顶',
        complexity='时间 `O(nL)`（`L ≤ 4` 为 token 长度），空间 `O(n)`',
        problem=['`tokens` 是逆波兰表示法（后缀表达式），算符写在两个操作数后面',
                 '计算表达式的值；整数除法==向零截断==',
                 '示例：`["4","13","5","/","+"]` → `4 + 13 / 5` = `6`；本视频把 13 换成 `-13`'],
        quote='⚠注意：执行减法或者除法运算时，==栈顶数字在运算符右侧==，栈顶下面的数在运算符左侧。代码实现时，可以只出栈一个数，然后==直接修改栈顶==，避免出栈再入栈。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遇到数字入栈；遇到运算符，取出栈顶两个数计算，结果压回栈',
              '优化：只 `pop` 右操作数 `x`，左操作数就是新的栈顶 `st[-1]`，原地更新',
              '判断数字：`len(token) > 1`（多位数或负数）或首字符是数字'],
        result='返回 `2`：`-13 / 5 = -2.6` 向零取整为 `-2`，再 `4 + (-2) = 2` ✓',
        summary=['时间 `O(nL)`，空间 `O(n)`',
                 '易错 1：`"-13"` 以 `-` 开头，不能用 `token[0]` 是否为运算符来判断',
                 '易错 2：Python 的 `//` 向下取整，`-13 // 5 = -3`；题目要的是向零取整 `-2`',
                 '不用浮点数的写法（灵神写法二）：`y // x if y * x >= 0 else -(-y // x)`',
                 '同类：224 基本计算器、227 基本计算器 II（表达式解析）'],
    ),
)
