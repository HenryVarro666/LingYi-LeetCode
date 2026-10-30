
def _term(c, pw):
    s = ''.join(f"·{v}^{p}" if p > 1 else f"·{v}" for v, p in sorted(pw.items()))
    if not pw:
        return f"{c}"
    return (f"{c}" if c != 1 else '') + (s[1:] if c == 1 else s)


def _poly(p):
    if isinstance(p, str):
        return f"`{p}`"
    if not p:
        return '0'
    out = ' + '.join(_term(c, pw) for c, pw in p).replace('+ -', '− ')
    return '(' + out + ')'


def _seq(items):
    return '　'.join(_poly(x) for x in items)


def _t_parts(S):
    pl = S.get('part_list')
    if pl is None:
        return '还没有切分：part_list 为空'
    return 'part_list：' + (_seq(pl) if pl else '（空）')


def _t_stack(S):
    st = S.get('stack')
    if st is None or 'part_list' not in S:
        return ''
    return '栈 stack：' + ('　'.join(_poly(x) for x in st) if st else '（空）')


def _t_key(S):
    kd = S.get('key_dict')
    if kd is None or S.get('_line', 0) < 56:
        return ''
    if not kd:
        return '合并字典 key_dict：（空）'
    return '合并字典 key_dict：' + '　'.join(f"{k or '常数'}→=={v}==" if v else f"{k or '常数'}→{v}" for k, v in kd.items())


def _t_expr(S):
    e = S.get('expression')
    if e is None:
        return ''
    return f"当前解析的表达式 `{e}`"


CONFIG = dict(
    num=770, title='基本计算器 IV', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='递归解析 · 栈处理乘法 · 字典合并同类项',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def basicCalculatorIV(self, expression, evalvars, evalints):
        var_dict = {}
        for var, value in zip(evalvars, evalints):
            var_dict[var] = value

        parse_list = self.parse(expression, var_dict)
        res_list = []
        for index in range(len(parse_list)):
            c, power_dict = parse_list[index]
            if c != 0:
                exp = '*'.join(['*'.join([char] * power_dict[char]) for char in sorted(power_dict.keys())])
                d = sum(power_dict.values())
                if d > 0:
                    res_exp = str(c) + '*' + exp
                else:
                    res_exp = str(c)
                res_list.append([-d, c, exp, res_exp])

        return [x[-1] for x in sorted(res_list, key=lambda d:(d[0], d[2]))]

    def parse(self, expression, var_dict):
        if expression.find(' ') == -1:
            if expression[0] in ('+', '-', '*'):
                return expression[0]
            if expression[0] == '(':
                expression = expression[1 : len(expression) - 1]
            if expression in var_dict:
                return [[var_dict[expression], {}]]
            elif expression[0] >= '0' and expression[0] <= '9':
                return [[int(expression), {}]]
            else:
                return [[1, {expression : 1}]]

        part_list = []
        cnt = 0
        start_pos = 0
        now = 0
        while now < len(expression):
            char = expression[now]
            if char == '(':
                cnt += 1
            elif char == ')':
                cnt -= 1
            elif char == ' ' and cnt == 0:
                if expression[now - 1] == ')':
                    part_list.append(self.parse(expression[start_pos + 1 : now - 1], var_dict))
                else:
                    part_list.append(self.parse(expression[start_pos : now], var_dict))
                start_pos = now + 1

            now += 1

        if expression[-1] == ')':
            part_list.append(self.parse(expression[start_pos + 1 : len(expression) - 1], var_dict))
        else:
            part_list.append(self.parse(expression[start_pos : len(expression)], var_dict))
        stack = [part_list[0]]
        for index in range(1, len(part_list), 2):
            operator = part_list[index]
            now = part_list[index + 1]
            if operator == '+':
                stack.append(now)
            elif operator == '-':
                stack.append([[c * -1, power_dict] for c, power_dict in now])
            else:
                last = stack.pop()
                tmp = []
                for c1, power_dict1 in last:
                    for c2, power_dict2 in now:
                        tmp_dict = {}
                        for char, power in power_dict1.items():
                            tmp_dict[char] = power
                        for char, power in power_dict2.items():
                            tmp_dict[char] = tmp_dict.get(char, 0) + power
                        tmp.append([c1 * c2, tmp_dict.copy()])

                stack.append(tmp)
                
        key_dict = {}
        for parts in stack:
            for c, var_dict in parts:
                var_key = '*'.join([key + '^' + str(var_dict.get(key)) for key in sorted(var_dict.keys())])
                key_dict[var_key] = key_dict.get(var_key, 0) + c

        res_list = []
        for key, c in key_dict.items():
            if c == 0:
                continue
            res_list.append([c, {}])
            if key != '':
                for char_power in key.split('*'):
                    char, power = char_power.split('^')
                    res_list[-1][1][char] = int(power)
        
        return res_list
''',
    call='Solution().basicCalculatorIV("(a + 2) * a", [], [])',
    expect=['1*a*a', '2*a'],
    views=[
        dict(type='text', fn=_t_expr, size=26, h=60),
        dict(type='calls', h=210, hide=('expression', 'evalvars', 'evalints')),
        dict(type='text', fn=_t_parts, size=26, h=60),
        dict(type='text', fn=_t_stack, size=26, h=60),
        dict(type='text', fn=_t_key, size=26, h=60),
    ],
    watch=[('cnt', 'cnt', 'yellow'), ('start_pos', 'start_pos', 'blue')],
    max_steps=130,
    skip=["now = 0", "cnt = 0", "start_pos = 0", "while now < len(expression)", "char = expression[now]",
          "if char == '('", "elif char == ')'", "elif char == ' ' and cnt == 0", "cnt += 1", "cnt -= 1", "now += 1",
          "expression[0] == '('", "expression = expression[1 :",
          "now = part_list", "res_list.append([c, {}])", "if key != ''", "for char_power in", "char, power =", "res_list[-1][1][char]", "for c1, power_dict1", "for c2, power_dict2", "tmp = []", "start_pos = now + 1", "if expression[-1] == ')'", "if expression[now - 1] == ')'", "for index in range(len(parse_list))", "res_list.append([-d", "operator = part_list", "if expression[0] in", "if expression in var_dict", "elif expression[0] >=", "for parts in stack", "res_list = []", "exp = ", "d = sum", "if d > 0", "c, power_dict = parse_list", "if c != 0", "tmp_dict = {}", "tmp_dict[char] =", "for char, power in power_dict", "tmp_dict.copy()"],
    captions={
        'var_dict = {}': '`var_dict`：把 evalvars 和 evalints 配成「变量 → 值」的字典，这里没有已知变量',
        'parse_list = self.parse': '先把整个表达式交给 `parse`，得到一个多项式：每项 `[系数, {变量: 幂次}]`',
        'expression.find': lambda S, B, r: (f"`{S.expression}` 里没有空格 → 是一个整体：常量、变量或运算符" if S.expression.find(' ') == -1
                                           else f"`{S.expression}` 里有空格 → 要先切成「段 + 运算符」再递归"),
        'part_list = []': '准备切分：括号外（`cnt = 0`）的空格才是分隔符。`part_list` 依次放 part、运算符、part……',
        "expression[now - 1] == ')'": lambda S, B, r: (f"到了一个括号外的空格，前一个字符是 `)` → 这一段是 `(…)`，递归时要==剥掉两侧括号==" if S.expression[S.now - 1] == ')'
                                                    else "到了一个括号外的空格，这一段是普通的变量/数字/运算符"),
        'part_list.append(self.parse(expression[start_pos + 1 : now - 1]': '递归解析括号里的内容 `{expression}`',
        'part_list.append(self.parse(expression[start_pos : now]': '递归解析这一段 `{expression}`',
        'start_pos = now + 1': '下一段从空格之后开始：`start_pos = {start_pos}`',
        "if expression[-1] == ')'": '最后一段后面没有空格，循环里切不出来，要在循环外单独处理',
        'part_list.append(self.parse(expression[start_pos + 1 : len(expression) - 1]': '最后一段是括号：剥括号后递归 `{expression}`',
        'part_list.append(self.parse(expression[start_pos : len(expression)]': '最后一段：递归解析 `{expression}`',
        "expression[0] in ('+', '-', '*')": lambda S, B, r: (f"`{S.expression}` 是运算符 → 原样返回" if S.expression[0] in '+-*' else f"`{S.expression}` 不是运算符"),
        "return expression[0]": '运算符直接返回，留给上层去处理',
        'if expression in var_dict': lambda S, B, r: (f"`{S.expression}` 是已赋值的变量 → 换成数值" if S.expression in S.var_dict else f"`{S.expression}` 不在 `var_dict` 里，不是已知变量"),
        'elif expression[0] >=': lambda S, B, r: (f"`{S.expression}` 以数字开头 → 是常量" if S.expression[0].isdigit() else f"`{S.expression}` 不是数字 → 它是未知变量"),
        'return [[int(expression), {}]]': '常量：系数就是这个数，没有变量 → `[{int(expression)}, {{}}]`',
        'return [[1, {expression : 1}]]': '变量：系数 1，幂次 1 → `[1, {{{expression!r}: 1}}]`',
        'stack = [part_list[0]]': '用栈算加减乘：先把 part_0 压进去，后面每次读「运算符 + part」',
        'for index in range(1, len(part_list), 2)': lambda S, B, r: ('part_list 是 part、运算符、part……交替排列，每次跳 2 个读一对' if 'index' not in B or B.index != S.index else '这一轮合并完了'),
        'operator = part_list[index]': '这一对的运算符是 `{operator}`',
        "if operator == '+'": lambda S, B, r: ("加号 → 新 part 直接压栈，最后一起合并" if S.operator == '+' else f"`{S.operator}` 不是加号"),
        'stack.append(now)': '加号：直接把 part 压栈',
        "elif operator == '-'": lambda S, B, r: ("减号 → 把 part 里每一项的系数取反再压栈" if S.operator == '-' else "不是减号，只剩乘号"),
        'stack.append([[c * -1': '减号：系数取反后压栈（这样最后统一相加就是减）',
        'last = stack.pop()': '乘号：乘法优先，把栈顶 `last` 弹出，要和新 part 逐项两两相乘',
        'for c1, power_dict1 in last': '取 last 里的一项 `[{c1}, {power_dict1}]`',
        'for c2, power_dict2 in now': '再取 part 里的一项 `[{c2}, {power_dict2}]`',
        'tmp.append([c1 * c2': '两项相乘：系数 `{c1} × {c2}` = =={c1 * c2}==，幂次相加 → `{tmp_dict}`',
        'stack.append(tmp)': '乘完的结果 `tmp` 压回栈（展开后项数是两边项数的乘积）',
        'key_dict = {}': '栈里剩下的各项要合并同类项：把幂次字典转成字符串当 key',
        'for parts in stack': lambda S, B, r: f"处理栈里的第 {S.stack.index(S.parts) + 1 if S.parts in S.stack else '?'} 个多项式",
        'for c, var_dict in parts': '取出一项：系数 `{c}`，幂次 `{var_dict}`',
        'var_key = ': '幂次字典变成字符串 key：`{var_key!r}`（空串代表常数项）',
        'key_dict[var_key] = ': '同 key 的系数相加：`key_dict[{var_key!r}]` = =={key_dict[var_key]}==',
        'res_list = []': '把 `key_dict` 还原成 `[系数, {变量: 幂次}]`',
        'if c == 0': lambda S, B, r: (f"系数为 0（`{S.key!r}` 抵消了）→ 这一项丢掉" if S.c == 0 else f"系数 `{S.c}` ≠ 0 → 保留"),
        'res_list.append([c, {}])': '新增一项，系数 `{c}`',
        'return res_list': '返回合并后的多项式',
        'for index in range(len(parse_list))': '解析完了，下面把每一项按题目格式输出',
        'c, power_dict = parse_list[index]': '取第 `{index}` 项：系数 `{c}`，幂次 `{power_dict}`',
        'if c != 0': '系数非零才输出',
        "exp = '*'.join": '变量按字母序展开，每个变量重复「幂次」遍：`exp = {exp!r}`',
        'd = sum(power_dict.values())': '`d` 是这一项的总次数 = {d}，排序时「次数大的在前」',
        'if d > 0': lambda S, B, r: ('有变量 → 格式 `系数*变量*…`' if S.d > 0 else '常数项 → 只输出系数'),
        'res_list.append([-d': '存 `[-次数, 系数, 变量串, 文本]`，用 `-d` 让次数大的排前面',
        'return [x[-1]': lambda S, B, r: f'按（次数降序，字典序）排序后输出：`{ret}`',
    },
    cards=dict(
        one_liner='递归切段，栈里先乘后加，字典合并同类项',
        complexity='时间取决于展开后的项数，最坏指数级；空间同阶',
        problem=['给定含 `+ - *`、括号、变量的表达式，以及 `evalvars`/`evalints`（已知变量的值），要把它展开化简',
                 '输出项按「次数降序、同次数字典序」排列，如 `["-1*a","14"]`，系数为 0 的项不输出',
                 '本视频：`"(a + 2) * a"`，无已知变量 → `["1*a*a","2*a"]`'],
        quote='这里的难写并不是指的算法难写，而是构造题目要求的数据结构有点复杂。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `[系数, {变量: 幂次}]` 表示一项，多项式就是项的列表',
              '空格（括号外）把表达式切成 part 和运算符，每个 part 递归求解；括号段先剥括号',
              '栈里：加号直接压，减号取反再压，乘号弹出栈顶与新 part 两两相乘',
              '最后把幂次字典转成字符串当 key，系数相加，抵消为 0 的项丢掉'],
        summary=['递归只在括号和空格处分段；叶子是常量、变量或运算符',
                 '易错：乘法要先于加减，所以乘号当场弹栈计算，加减只压栈',
                 '易错：括号段递归时要剥掉两侧括号；最后一段不以空格结尾，要循环外再处理一次',
                 '易错：相乘后要合并同类项，否则 `(a+2)*(a-2)` 会残留多个同类项，必须按幂次合并系数；系数合并成 0 的项要丢掉',
                 '原文已是 Python 3 可运行的写法（`items()` 等），没有修改；输出为 `["1*a*a","2*a"]`'],
    ),
)
