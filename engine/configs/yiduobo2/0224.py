EXPR = '12-(3-1)+4'

# 只用于可视化：让字符串记住 for 循环读到了第几个字符（代码本身不变）
SETUP = '''
class TS(str):
    pos = -1
    def __iter__(self):
        for i, ch in enumerate(str(self)):
            self.pos = i
            yield ch
'''

CODE = '''
class Solution(object):
    def calculate(self, s):
        res = 0
        sign = 1
        now = 0
        stack = []

        for char in s:
            if char == '+':
                res += sign * now
                sign = 1
                now = 0
            elif char == '-':
                res += sign* now
                sign = -1
                now = 0
            elif char.isdigit():
                now = now * 10 + int(char)
            elif char == '(':
                stack.append(res)
                stack.append(sign)
                res = 0
                sign = 1
            elif char == ')':
                res += sign * now
                res *= stack.pop()
                res += stack.pop()
                now = 0

        return res + sign * now
'''
_LINES = CODE.strip('\n').split('\n')


def _lns(sub):
    return [i + 1 for i, s in enumerate(_LINES) if sub in s]


SIGN1 = _lns('sign = 1')          # [初始化, '+' 分支, '(' 分支]
NOW0 = _lns('now = 0')            # [初始化, '+', '-', ')']
ADD = _lns('res += sign')         # ['+', '-', ')']


def _pos(S):
    s = S.get('s')
    p = getattr(s, 'pos', -1)
    return p if isinstance(p, int) and p >= 0 else None


def _depth(S):
    return len(S.get('stack') or []) // 2


def _expr(S):
    if 'res' not in S:
        return '把算式拆成：`res`（已算完的部分）`+ sign × now`（正在读的数）'
    sg = '+' if S['sign'] > 0 else '−'
    d = _depth(S)
    where = f'第 {d} 层括号内' if d else '最外层'
    return f'{where}：`res {sg} now` = `{S["res"]} {sg} {S["now"]}`'


def _stack_fmt(S):
    st = S.get('stack') or []
    out = []
    for k in range(0, len(st) - 1, 2):
        out.append(f'({st[k]}, {st[k + 1]:+d})')
    return out


def _for(S, B, ret):
    p = _pos(S)
    if p is None or S.get('char') == B.get('char') and _pos(B) == p:
        return '字符读完了'
    c = S.char
    kind = '数字' if c.isdigit() else {'+': '加号', '-': '减号', '(': '左括号', ')': '右括号'}[c]
    return f'读入第 `{p}` 个字符 `{c}`（{kind}）'


CONFIG = dict(
    num=224, title='基本计算器', difficulty='Hard', category='栈',
    author='yiduobo', technique='遇到括号就把 res、sign 压栈',
    tags=['字节30天', '热题173', '面试经典150'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().calculate(TS({EXPR!r}))',
    expect=14,
    skip=["if char == '+'", "elif char == '-'", 'elif char.isdigit()', "elif char == '('", "elif char == ')'",
          'stack = []'],
    views=[
        dict(type='text', fn=_expr, h=60),
        dict(type='string', var=lambda S: str(S['s']) if 's' in S else EXPR, label='s（算式，蓝箭头 = 当前字符）',
             cell=80, pointers={_pos: 'blue'}, pointer_labels={_pos: 'char'},
             dim=lambda S, i, v: _pos(S) is not None and i < _pos(S)),
        dict(type='stack', var=_stack_fmt, label='stack：每进一层括号压入 (res, sign)', h=130, font=24),
        dict(type='custom', h=150, draw=lambda cv, S, B, box, T: (
            cv.rich(box[0] + 22, box[1] + 10, '`(`：保存现场 → 压入 `res`、`sign`，括号内从 0 重新算', box[2] - box[0] - 44, size=24, color=T['muted']),
            cv.rich(box[0] + 22, box[1] + 60, '`)`：括号结果 × 弹出的 `sign` + 弹出的 `res`', box[2] - box[0] - 44, size=24, color=T['muted']))),
    ],
    watch=[('char', 'char', 'blue'), ('now', 'now', 'orange'), ('sign', 'sign', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': lambda S, B, ret: ('`res = 0`：当前这一层==已经算完的部分==' if 'sign' not in S
                                      else '括号里==从 0 开始==重新计算：`res = 0`'),
        SIGN1[0]: '`sign = 1`：下一个数字前面的符号（+1 或 −1）',
        NOW0[0]: '`now = 0`：正在读的数字（可能有多位）',
        'for char in s': _for,
        ADD[0]: lambda S, B, ret: (f'遇到 `+`：先把读完的数结算进去：`res += {B.sign} × {B.now}` → {S.res}' if B.now
                                   else f'遇到 `+`：前面是括号，值已并进 `res`，这里 `now = 0`，`res` 仍是 {S.res}'),
        SIGN1[1]: '下一个数的符号变成 `+1`',
        NOW0[1]: '`now` 清零，准备读下一个数',
        ADD[1]: '遇到 `-`：先结算上一个数：`res += {B.sign} × {B.now}` → {res}',
        'sign = -1': '下一个数的符号变成 `−1`',
        NOW0[2]: '`now` 清零，准备读下一个数',
        'now = now * 10 + int(char)': '数字可能有多位：`now = {B.now} × 10 + {char}` = =={now}==',
        'stack.append(res)': '遇到 `(`：把括号外已算好的 `res = {res}` 压栈',
        'stack.append(sign)': '再把括号前的符号 `sign = {sign}` 压栈（==括号整体要乘上它==）',
        SIGN1[2]: '括号内第一个数默认为正：`sign = 1`',
        ADD[2]: '遇到 `)`：先结算括号里最后一个数：`res += {B.sign} × {B.now}` → 括号内结果 =={res}==',
        'res *= stack.pop()': '弹出括号前的符号 `{B.stack[-1]}`：`res = {B.res} × {B.stack[-1]}` = {res}',
        'res += stack.pop()': '弹出括号外的 `res = {B.stack[-1]}` 加回去：`{B.res} + {B.stack[-1]}` = =={res}==',
        NOW0[3]: '括号的值已经并进 `res`，`now` 清零',
        'return res + sign * now': '最后一个数还没结算：`{res} + {sign} × {now}` = =={ret}==',
    },
    cards=dict(
        one_liner='从左往右一趟算；遇到括号就把当前结果和符号压栈，算完括号再弹出来',
        complexity='时间 `O(n)`，空间 `O(n)`（栈深 = 括号层数）',
        problem=['给一个只含 `+ - ( )`、非负整数和空格的算式 `s`，计算它的值（不能用 `eval`）',
                 '`-` 可以作为一元负号，比如 `-(2+3)`',
                 '示例：`"(1+(4+5+2)-3)+(6+8)"` → `23`',
                 '本视频：`"12-(3-1)+4"` → `14`'],
        quote='既然用到了栈，那干脆就全部都丢进去好了，即==碰到括号时将当前的运算结果以及运算符压入栈中==，然后从0开始计算括号中的结果……',
        quote_src='—— yiduobo 题解',
        idea=['没有括号时：维护 `res`、`sign`、`now`，遇到运算符就把 `sign × now` 结算进 `res`',
              '难点是 `A - (B + C - D)`：括号前的减号会让括号里的符号全部取反',
              '`(`：压入 `res`、`sign`，重置；`)`：括号结果 `× sign + res`，省去数符号个数'],
        result='`12 − (3 − 1) + 4 = 12 − 2 + 4 = 14` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`：最坏括号嵌套 `n/2` 层',
                 '易错：遇到运算符 / 右括号 / 结尾时，都要先把 `sign × now` 结算掉',
                 '`stack` 先压 `res` 再压 `sign`，弹出顺序相反：先乘 sign，再加 res',
                 '空格不进任何分支，自动跳过；原文 Python 2 风格，只删去了文档字符串'],
    ),
)
