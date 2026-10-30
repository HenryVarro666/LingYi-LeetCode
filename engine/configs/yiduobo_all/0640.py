def _state(S):
    if 'char' in S and 'flag' in S and S.get('_line') is not None and 's' in S:
        t = '正在读字符 `' + str(S['char']) + '`'
        now = S['now']
        t += f"　数字缓存 `now = {now}`　符号 `flag = {'+' if S['flag'] == 1 else '-'}`"
        return t
    return ''


def _acc(S):
    if 'char' in S and 'a' in S and 's' in S:
        return f"已累计：`a = {S['a']}`（x 的系数）　`b = {S['b']}`（常数）"
    return ''


def _eq(S):
    if 'a1' in S and 'a2' in S:
        return f"`{S['a1']}x + ({S['b1']})` = `{S['a2']}x + ({S['b2']})`　→　`({S['a1']}−{S['a2']})x = {S['b2']}−({S['b1']})`"
    if 'a1' in S:
        return f"左边：`{S['a1']}x + ({S['b1']})`"
    return '把方程拆成「系数 × x + 常数」两边'


CONFIG = dict(
    num=640, title='求解方程', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='分别统计系数与常数',
    tags=[],
    code='''
class Solution(object):
    def solveEquation(self, equation):

        left, right = equation.split('=')
        a1, b1 = self.get_para(left)
        a2, b2 = self.get_para(right)

        if a1 == a2:
            if b1 == b2:
                return 'Infinite solutions'
            else:
                return 'No solution'
        else:
            return 'x=%d' % ((b2 - b1) // (a1 - a2))

    def get_para(self, s):
        flag = 1
        now = None
        a = b = 0
        x_flag = False
        for char in s:
            if char == '+' or char == '-':
                if now is not None:
                    if x_flag:
                        a += now * flag
                    else:
                        b += now * flag
                
                if char == '+':
                    flag = 1
                else:
                    flag = -1

                x_flag = False
                now = None

            elif char == 'x':
                x_flag = True
                if now is None:
                    now = 1
            
            elif now is None:
                now = int(char)
            else:
                now = now * 10 + int(char)

        if x_flag:
            a += now * flag
        else:
            b += now * flag
        return a, b
''',
    call="Solution().solveEquation('x+5-3+x=6+x-2')",
    expect='x=2',
    views=[
        dict(type='string', var=lambda S: S.get('s', S.get('equation', '')), label='正在解析的字符串', cell=70, h=170),
        dict(type='text', fn=_state, size=26, h=70),
        dict(type='text', fn=_acc, size=26, h=70),
        dict(type='text', fn=_eq, size=28, h=90),
    ],
    watch=['a', 'b', 'now', ('flag', 'flag', 'blue'), 'x_flag'],
    skip=['flag = 1', 'a = b = 0', 'x_flag = False'],
    max_steps=110,
    captions={
        'left, right = equation.split': '按 `=` 拆成两边：左 `{left}`，右 `{right}`',
        'a1, b1 = self.get_para(left)': '`get_para` 返回（x 的系数, 常数）：左边 `a1 = {a1}`，`b1 = {b1}`',
        'a2, b2 = self.get_para(right)': '右边同样统计：`a2 = {a2}`，`b2 = {b2}`',
        'if a1 == a2': lambda S, B, r: ('两边 x 系数相同 `{} = {}`：x 要么任意、要么无解，要看常数'.format(S.a1, S.a2) if S.a1 == S.a2
                                         else '系数不同 `{} ≠ {}`：有唯一解'.format(S.a1, S.a2)),
        'if b1 == b2': '常数也相同 `{b1} = {b2}`：恒等式 → ==无穷多解==' ,
        "return 'Infinite": '返回 `Infinite solutions`',
        "return 'No solution'": '常数不同：x 项抵消后 `{b1} = {b2}` 不成立 → 无解',
        "return 'x=%d'": '移项：`x = (b2 − b1) // (a1 − a2) = ({b2} − {b1}) // ({a1} − {a2})` = =={ret}==',
        'flag = 1': '`flag`：当前项的符号，开头默认为正',
        'a = b = 0': '`a` 累计 x 的系数，`b` 累计常数',
        'for char in s': '读入下一个字符 `{char}`',
        "if char == '+' or char == '-'": lambda S, B, r: ('`{}` 是符号：上一项读完了，要结算'.format(S.char) if S.char in '+-' else '`{}` 不是符号'.format(S.char)),
        'if now is not None': lambda S, B, r: ('上一项有内容 `now = {}`，结算它'.format(S.now) if S.now is not None else '符号前没有项（开头的符号），不用结算'),
        'if x_flag': lambda S, B, r: ('这一项带 x → 计入系数 `a`' if S.x_flag else '这一项不带 x → 计入常数 `b`'),
        'a += now * flag': '`a += {now} × {flag}` → ==a 变为 {a}==',
        'b += now * flag': '`b += {now} × {flag}` → ==b 变为 {b}==',
        "if char == '+'": lambda S, B, r: ('`+` → 下一项为正' if S.char == '+' else '`-` → 下一项为负'),
        'flag = -1': '下一项符号为负：`flag = -1`',
        'x_flag = False': '新的一项开始，`x_flag` 复位',
        'now = None': lambda S, B, r: '新的一项开始，数字缓存清空' if 'char' in S else '`now` 缓存正在读的数字；`None` 表示还没读到数',
        "elif char == 'x'": lambda S, B, r: ('`x`：这一项带 x' if S.char == 'x' else '`{}` 不是 x，是数字'.format(S.char)),
        'x_flag = True': '标记这一项含 x：`x_flag = True`',
        39: lambda S, B, r: ('单独的 `x` 没有系数，等价于 `1x`：`now = 1`' if S.now is None else '`x` 前已有系数 `{}`'.format(S.now)),
        42: lambda S, B, r: ('数字的第一位：直接记下' if S.now is None else '之前已有数字 `{}`，要接着拼'.format(S.now)),
        'now = int(char)': '数字的第一位：`now = {now}`',
        'now = now * 10': '多位数：`now = now × 10 + {char}` = {now}',
        'return a, b': '一边读完：`(a, b) = ({a}, {b})`，即 `{a}x + ({b})`',
    },
    cards=dict(
        one_liner='方程两边各拆成「系数 × x + 常数」，再一次除法解出 x',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个只含 `+`、`-`、`x`、整数和 `=` 的一次方程，求 `x`',
                 '解唯一：`x=值`；恒成立：`Infinite solutions`；矛盾：`No solution`',
                 '示例：`x+5-3+x=6+x-2` → `x=2`'],
        quote='分别统计出等号两边的常数项之和以及系数之和。若两边的系数相等，那么根据常数是否相等确定是无穷解还是无解，若系数不相等，则直接除法求解即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐字符扫描：数字拼进 `now`，遇到 `+` / `-` 才把上一项结算',
              '带 `x` 的项加到系数 `a`，否则加到常数 `b`；符号由 `flag` 决定',
              '两边得到 `a1x+b1 = a2x+b2`，移项后 `x = (b2−b1)/(a1−a2)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：单独的 `x` 系数是 1；末尾最后一项要在循环结束后再结算',
                 '易错：系数相同时，常数相同是无穷解，不同是无解',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
