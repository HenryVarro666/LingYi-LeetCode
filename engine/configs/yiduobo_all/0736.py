def _parts_txt(S):
    if 'exp' not in S:
        return ''
    p = S.get('parts')
    s = f"当前表达式 `{S['exp']}`"
    if p is not None and S.get('_line', 0) >= 22:
        s += f"　分块 `{p}`"
    return s


CONFIG = dict(
    num=736, title='Lisp 语法解析', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='递归 · 括号匹配分块 · 复制变量表',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def evaluate(self, expression):

        return self.parse(expression, {})

    def parse(self, exp, value_dict):
        if exp[0] == '(':
            exp = exp[1:-1]
        
        if (exp[0] >= '0' and exp[0] <= '9') or exp[0] =='-':
            return int(exp)
        
        parts = []
        last_pos = 0
        cnt = 0
        for index, char in enumerate(exp):
            if exp[index] == '(':
                cnt += 1
            elif exp[index] == ')':
                cnt -= 1
            elif exp[index] == ' ' and cnt == 0:
                parts.append(exp[last_pos:index])
                last_pos = index + 1
        
        parts.append(exp[last_pos:index + 1])

        tmp_value_dict = value_dict.copy()
        if len(parts) == 1:
            return tmp_value_dict[parts[0]]
        elif parts[0] == 'add':
            v1 = self.parse(parts[1], tmp_value_dict)
            v2 = self.parse(parts[2], tmp_value_dict)
            return v1 + v2
        elif parts[0] == 'mult':
            v1 = self.parse(parts[1], tmp_value_dict)
            v2 = self.parse(parts[2], tmp_value_dict)
            return v1 * v2
        else:
            for index in range(1, len(parts) - 1, 2):
                tmp_value_dict[parts[index]] = self.parse(parts[index + 1], tmp_value_dict)
            return self.parse(parts[-1], tmp_value_dict)
''',
    call='Solution().evaluate("(let x 2 (add x (let x 3 x)))")',
    expect=5,
    views=[
        dict(type='text', fn=_parts_txt, size=26, h=90),
        dict(type='array', var='parts', label='parts（括号外的空格把表达式切成块）', cell=100, h=190,
             color=lambda S, i, v: None),
        dict(type='map', var='tmp_value_dict', label='tmp_value_dict（这一层的变量表，子块继承、不回写）', fmt=lambda k, v: f'{k} = {v}', h=110, font=32),
        dict(type='calls', h=180, hide=('value_dict',)),
    ],
    watch=[('cnt', 'cnt', 'yellow'), ('v1', 'v1', 'blue'), ('v2', 'v2', 'pink')],
    skip=[7, 13, 14, 16, 17, 18, 19, 20, 21, 23],
    max_steps=110,
    captions={
        4: '先解析整个表达式，变量表从空字典 `{}` 开始',
        7: lambda S, B, r: (f"`exp = {S.exp!r}` 以 `(` 开头 → 去掉头尾括号" if S.exp[0] == '(' else f"`exp = {S.exp!r}` 不以括号开头，不用去"),
        8: '去掉头尾括号：`exp = {exp!r}`',
        10: lambda S, B, r: (f"`exp = {S.exp!r}` 以数字或负号开头 → ==整串就是一个整数==" if (S.exp[0].isdigit() or S.exp[0] == '-')
                             else f"`exp = {S.exp!r}` 不是数字 → 要分块"),
        11: '整串是数字，直接 `int(exp)` 返回：=={ret}==',
        13: '`parts` 存分出来的块',
        14: '`last_pos` 记当前块的起点',
        15: '准备分块：`parts` 存块，`last_pos` 是块起点，`cnt` 记==没匹配的左括号数==（遇 `(` 加一，遇 `)` 减一）',
        22: '扫到括号外的空格（`cnt = 0`）→ ==切出一块== `{parts[-1]!r}`',
        25: '最后一块后面没有空格，补上：`parts = {parts}`',
        27: '==复制==一份变量表：子块里的改动不能影响父块',
        28: lambda S, B, r: ('只有一块 → 是变量名，直接查表' if len(S.parts) == 1 else f"`parts` 有 {len(S.parts)} 块，看第一块 `{S.parts[0]}`"),
        29: '变量 `{parts[0]}` 的值：=={ret}==',
        30: lambda S, B, r: ('第一块是 `add` → 两个操作数相加' if S.parts[0] == 'add' else '第一块不是 `add`'),
        31: '递归算第一个操作数 `{parts[1]}` = =={v1}==',
        32: '递归算第二个操作数 `{parts[2]}` = =={v2}==',
        33: '`add`：`{v1} + {v2}` = =={ret}==',
        34: lambda S, B, r: ('第一块是 `mult` → 两个操作数相乘' if S.parts[0] == 'mult' else '第一块不是 `mult` → 一定是 `let`'),
        35: '递归算第一个操作数 `{parts[1]}` = =={v1}==',
        36: '递归算第二个操作数 `{parts[2]}` = =={v2}==',
        37: '`mult`：`{v1} * {v2}` = =={ret}==',
        39: '`let`：`parts[1:-1]` 两块一组「变量名 + 表达式」，逐组赋值',
        40: '递归算 `{parts[index + 1]}` 的值，再存给变量 `{parts[index]}`',
        41: '最后一块 `{parts[-1]}` 是返回表达式，带着新变量表 `{tmp_value_dict}` 递归',
    },
    cards=dict(
        one_liner='按括号外的空格分块，看第一块决定 add / mult / let',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['Lisp 风格表达式：`(add a b)`、`(mult a b)`、`(let v1 e1 v2 e2 ... expr)`，变量有作用域',
                 '求表达式的整数值；`let` 里的变量只在该括号内有效，内层可以遮盖外层同名变量',
                 '本视频：`"(let x 2 (add x (let x 3 x)))"` → `5`'],
        quote='每个子块都会继承父块的变量值，但是在子块内部如果变量值产生的变化并不会反馈回父块，于是每次递归求解时，都需要先copy一遍变量表',
        quote_src='—— yiduobo 题解原文',
        idea=['去掉头尾括号；数字直接转 `int`',
              '用 `cnt` 数未匹配的 `(`：括号外的空格才切块，得到 `parts`',
              '一块 = 变量查表；`add`/`mult` 递归算两块；`let` 两个一组赋值，最后递归算最后一块'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`：每层递归都要复制变量表、切分字符串',
                 '易错：必须 `copy()` 变量表，否则内层的 `x = 3` 会污染外层的 `x = 2`',
                 '括号外的空格才能切块，括号内的空格属于子表达式',
                 '`let` 的最后一块才是返回值，前面的是「变量名、表达式」成对出现'],
    ),
)
