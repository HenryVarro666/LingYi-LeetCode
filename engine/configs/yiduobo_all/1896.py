EXPR = '1&(0|1)'

SETUP = '''
class Expr(str):
    """str 的子类：for 循环取字符时记下当前下标 pos，仅供动画画指针用"""
    pos = -1
    def __iter__(self):
        import sys
        for k, c in enumerate(str.__iter__(self)):
            if sys._getframe(1).f_code.co_name == 'minOperationsToFlip':   # 画图时遍历它不算
                self.pos = k
            yield c
'''


def _pos(S):
    e = S.get('expression')
    return getattr(e, 'pos', -1) if e is not None else -1


def _show(S):
    ln = S.get('_line', 0)
    if 'f_zero' in S and 17 <= ln <= 31:
        t = f"前一个 `(f0, f1) = ({S['f_zero']}, {S['f_one']})`，后一个 `(s0, s1) = ({S['s_zero']}, {S['s_one']})`"
        if ln >= 21:
            t += f"\n保持原运算符：`or → ({S.get('or_zero', '?')}, {S.get('or_one', '?')})`，`and → ({S.get('and_zero', '?')}, {S.get('and_one', '?')})`"
        return t
    return '每个子表达式用二元组 `(变成0的最少操作数, 变成1的最少操作数)` 表示'


CONFIG = dict(
    num=1896, title='反转表达式值的最少操作次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='双栈 + 二元组 DP，一趟扫描',
    tags=['动态规划', '常用数据结构'],
    setup=SETUP,
    code='''
class Solution(object):
    def minOperationsToFlip(self, expression):

        stack_op = []
        stack_res = []
        for char in expression:
            if char == '0' or char == '1' or char == ')':
                if char == '0':
                    stack_res.append([0, 1])
                elif char == '1':
                    stack_res.append([1, 0])
                else:
                    stack_op.pop()
                
                while stack_op and stack_op[-1] != '(':
                    f_zero, f_one = stack_res.pop()
                    s_zero, s_one = stack_res.pop()
                    or_zero = f_zero + s_zero
                    or_one = min(f_zero + s_one, f_one + s_zero, f_one + s_one)
                    and_zero = min(f_zero + s_one, f_one + s_zero, f_zero + s_zero)
                    and_one = f_one + s_one

                    if stack_op[-1] == '|':
                        and_zero += 1
                        and_one += 1
                    else:
                        or_zero += 1
                        or_one += 1

                    stack_res.append([min(or_zero, and_zero), min(or_one, and_one)])
                    stack_op.pop()
            
            else:
                stack_op.append(char)

        return max(stack_res[0][0], stack_res[0][1])
''',
    call=f'Solution().minOperationsToFlip(Expr({EXPR!r}))',
    expect=1,
    views=[
        dict(type='string', var='expression', label='expression（蓝 = 当前字符）', cell=90,
             pointers={'expression.pos': 'blue'}, pointer_labels={'expression.pos': 'char'},
             dim=lambda S, i, v: i < _pos(S), color=lambda S, i, v: 'blue' if i == _pos(S) else None, h=210),
        dict(type='stack', var='stack_op', label='stack_op（符号栈）', h=120, font=30),
        dict(type='stack', var='stack_res', label='stack_res（二元组栈：变0 / 变1 的最少操作数）', h=130, font=30,
             fmt=lambda x: f'({x[0]},{x[1]})'),
        dict(type='text', fn=_show, size=26, h=120),
    ],
    watch=[('char', 'char', 'blue'), ('f', '(f_zero, f_one)', 'cyan'), ('s', '(s_zero, s_one)', 'pink')],
    captions={
        'stack_op = []': '符号栈：放 `&`、`|`、`(`',
        'stack_res = []': '结果栈：每项是二元组 `(变成0的最少操作数, 变成1的最少操作数)`',
        'for char in expression': lambda S, B, r: ('字符都读完了' if B.get('char') == S.char == EXPR[-1] else f'读入字符 `{S.char}`'),
        "if char == '0' or": lambda S, B, r: ('数字或右括号 → ==立刻能算的时候就算==（从左到右、无优先级）'
                                                if S.char in '01)' else f'`{S.char}` 是运算符或左括号 → 只入符号栈'),
        "if char == '0'": lambda S, B, r: f"`char == '0'`：{'是' if S.char == '0' else '不是'}",
        'stack_res.append([0, 1])': '数字 0：变 0 要 0 次，变 1 要 1 次 → 二元组 `(0, 1)`',
        'stack_res.append([1, 0])': '数字 1：变 0 要 1 次，变 1 要 0 次 → 二元组 `(1, 0)`',
        'stack_op.pop()': lambda S, B, r: ('右括号：弹出匹配的 `(`，括号里的结果已在结果栈顶' if S.get('_line') == 13
                                            else f'这一对已算完，弹出符号 `{B.stack_op[-1]}`'),
        'while stack_op': lambda S, B, r: ('符号栈顶是运算符 → 前后两个子表达式可以合并了'
                                            if S.stack_op and S.stack_op[-1] != '(' else '栈空或栈顶是 `(`：括号挡住，不能再往前合并'),
        'f_zero, f_one = stack_res.pop()': '后进的二元组 `f = ({f_zero}, {f_one})`',
        's_zero, s_one = stack_res.pop()': '先进的二元组 `s = ({s_zero}, {s_one})`',
        'or_zero = ': '若是 `|` 且要结果 0：两边都得 0 → `or_zero = f0 + s0 = {or_zero}`',
        'or_one = ': '`|` 要结果 1：一边为 1 即可，取三种里最小 → `or_one = {or_one}`',
        'and_zero = ': '`&` 要结果 0：一边为 0 即可，取三种里最小 → `and_zero = {and_zero}`',
        'and_one = ': '`&` 要结果 1：两边都得 1 → `and_one = f1 + s1 = {and_one}`',
        "if stack_op[-1] == '|'": lambda S, B, r: (f"当前运算符是 `{S.stack_op[-1]}`：{'它是 |，要改成 & 就得多花 1 次' if S.stack_op[-1] == '|' else '它是 &，要改成 | 就得多花 1 次'}"),
        'and_zero += 1': '原运算符是 `|`，换成 `&` 要 +1：`and_zero = {and_zero}`',
        'and_one += 1': '同上，`and_one` +1',
        'or_zero += 1': '原运算符是 `&`，换成 `|` 要 +1：`or_zero = {or_zero}`',
        'or_one += 1': '同上，`or_one` +1',
        'stack_res.append([min(or_zero': '不换/换运算符取最小 → 合并后的二元组 `{stack_res[-1]}`',
        'stack_op.append(char)': '运算符或左括号 `{char}` 入符号栈',
        'return max': lambda S, B, r: f'栈里只剩一个二元组 `{S.stack_res[0]}`：原值那一侧是 0 次，另一侧较大值就是翻转所需 =={r}=='
    },
    cards=dict(
        one_liner='把每段子表达式压成二元组：变0、变1各要多少次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['表达式含 `0 1 & | ( )`，`&` 和 `|` 没有优先级，从左到右算',
                 '一次操作：翻转一个数字，或把 `&` 和 `|` 互换',
                 '求让表达式结果翻转的最少操作次数',
                 '本视频：`1&(0|1)`，值为 1，要变成 0'],
        quote='由于这里的中间结果只可能是0或者1，那么就可以使用二元组(zero, one)来表示将当前子表达式的值变为0和1所需的最少操作数。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文先说 `O(n^2)`：先求值、再拆最上层表达式，括号会让拆解白费',
              '改成边扫边合并：数字入栈，`(0,1)` 或 `(1,0)`',
              '遇到数字或 `)` 就和前一个合并：不换运算符用原值，换运算符 `+1`',
              '括号用 `(` 挡住向前合并，保证了优先级'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文已是 Python 3 可运行的写法，代码未改动',
                 '无优先级：第二个数一出现就立刻和第一个合并 → 自然从左到右',
                 '最终答案取二元组较大者：原值那一侧一定是 0',
                 '这里用 str 子类在 setup 里记录下标仅为画指针，算法代码未改'],
    ),
)
