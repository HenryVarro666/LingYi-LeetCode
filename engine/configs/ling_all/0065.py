def _phase(S, B=None):
    if 'i' not in S:
        return '把字符串拆成：符号 | 指数前 | 指数符号 | 指数后'
    s, i = S['s'], S['i']
    ln = S.get('_line')
    hd, hg = S.get('has_dot'), S.get('has_digit')
    if hd is None:
        return f"当前下标 `i = {i}`，先看有没有开头的正负号"
    return f"小数点 {'有' if hd else '无'}　数字 {'有' if hg else '无'}　`i = {i}`" + (f"　当前字符 `{s[i]}`" if i < len(s) else '　已扫到末尾')


def _col(S, i, v):
    if 'i' not in S:
        return None
    k = S['i']
    if i == k:
        return 'blue'
    if i < k:
        return 'green' if v.isdigit() else 'yellow'
    return None


CONFIG = dict(
    num=65, title='有效数字', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='分段扫描 · 先指数前再指数后',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution:
    def isNumber(self, s: str) -> bool:
        n = len(s)

        # 正负号
        i = 0
        if s[i] in "+-":
            i += 1

        # 指数符号之前，至多一个小数点，其余必须全是数字
        has_dot = has_digit = False
        while i < n and s[i] not in "eE":
            if s[i] == '.':
                if has_dot:  # 不能有两个小数点
                    return False
                has_dot = True
            elif '0' <= s[i] <= '9':
                has_digit = True
            else:
                return False
            i += 1

        # 必须有数字
        if not has_digit:
            return False

        # 指数符号之后，必须是整数
        if i < n and s[i] in "eE":
            i += 1

            # 正负号
            if i < n and s[i] in "+-":
                i += 1

            # 必须有数字
            if i == n:
                return False

            # 剩下的必须全是数字
            while i < n and '0' <= s[i] <= '9':
                i += 1

        # 如果 i < n 说明有非法字符，不是有效数字
        return i == n
''',
    call='Solution().isNumber("-1.5e+3")',
    expect=True,
    views=[
        dict(type='text', fn=_phase, size=26, h=80),
        dict(type='string', var='s', label='s（蓝 = 当前位置，绿 = 数字，黄 = 符号/小数点/e）', cell=100,
             pointers={'i': 'blue'}, color=_col, h=300),
    ],
    watch=[('i', 'i', 'blue'), ('has_dot', 'has_dot', 'yellow'), ('has_digit', 'has_digit', 'green'), ('n', 'n')],
    captions={
        'n = len(s)': '`n = {n}`，下面用下标 `i` 从左到右扫一遍',
        'if s[i] in "+-"': lambda S, B, r: (f"`s[0] = '{S.s[0]}'` 是正负号 → 跳过它" if S.s[0] in '+-' else f"`s[0] = '{S.s[0]}'` 不是正负号，不用跳"),
        'i = 0': '`i` 从 0 开始',
        'has_dot = has_digit': '指数符号前要记两件事：==有没有小数点==、==有没有数字==，都还没见到',
        'while i < n and s[i] not in': lambda S, B, r: (f"`i = {S.i}`，`s[{S.i}] = '{S.s[S.i]}'` 不是 e/E → 还在指数符号之前" if S.i < len(S.s) and S.s[S.i] not in 'eE'
                                                          else f'`i = {S.i}`：到了末尾或指数符号，指数前的部分扫完'),
        "if s[i] == '.'": lambda S, B, r: (f"`'{S.s[S.i]}'` 是小数点 → 检查是不是第二个" if S.s[S.i] == '.' else f"`'{S.s[S.i]}'` 不是小数点"),
        'if has_dot': lambda S, B, r: ('`has_dot = True`：已经有小数点，这是第二个 → ==返回 False==' if S.has_dot else '`has_dot = False`：这是第一个小数点，允许'),
        'has_dot = True': '记下：已经出现过小数点',
        "elif '0' <= s[i] <= '9'": lambda S, B, r: (f"`'{S.s[S.i]}'` 是数字 → 记下==有数字==" if '0' <= S.s[S.i] <= '9' else f"`'{S.s[S.i]}'` 既不是点也不是数字 → 非法字符"),
        'has_digit = True': '记下：至少有一个数字（`.` 或 `+` 单独出现不算数）',
        'i += 1\n': '`i` → {i}',
        'if not has_digit': lambda S, B, r: ('指数前一个数字都没有（如 `"."`、`"e3"`）→ `False`' if not S.has_digit else '指数前有数字，继续看指数部分'),
        'if i < n and s[i] in "eE"': lambda S, B, r: (f"`s[{S.i}] = '{S.s[S.i]}'` 是指数符号 → 后面必须是整数" if S.i < len(S.s) and S.s[S.i] in 'eE' else '没有指数部分'),
        'if i < n and s[i] in "+-"': lambda S, B, r: ('指数符号后也可以有一个正负号 → 跳过' if S.i < len(S.s) and S.s[S.i] in '+-' else '指数后没有正负号'),
        'if i == n': '`i = {i}`，`n = {n}`：指数符号（和符号）后面==必须还有数字==，没有就 `False`',
        'while i < n and \'0\' <= s[i] <= \'9\'': '指数后剩下的必须全是数字，一路向右走',
        'return i == n': lambda S, B, r: f'`i = {S.i}`，`n = {S.n}`：==扫完了整个字符串== → `{S.i == S.n}`',
    },
    cards=dict(
        one_liner='先看指数符号之前，再看之后，各自检查规则',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['判断字符串 `s` 是不是有效数字：整数或小数，后面可跟 `e/E` 加整数的指数',
                 '例如 `"2"`、`"-.9"`、`"4."`、`"53.5e93"` 合法；`"e"`、`"."`、`"99e2.5"`、`"--6"` 不合法',
                 '本视频：`"-1.5e+3"` → `true`'],
        quote='本题相当于实现半个 atof 函数（把字符串转成浮点数）。说「半个」是因为本题只需判断字符串是否合法。',
        quote_src='—— 灵茶山艾府题解',
        idea=['去掉开头正负号后，指数前：至多一个小数点、至少一个数字、不能有别的字符',
              '指数后：去掉正负号，至少一个数字，其余只能是数字',
              '最后 `i == n` 说明整串都被合法地消耗掉了'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`"."`、`"+"` 没有数字；`"4."`、`".5"` 却合法，所以只看 `has_digit`',
                 '易错：`"1e"`、`"1e+"` 指数后没有数字，靠 `i == n` 判断',
                 '相似题：8. 字符串转换整数 (atoi)'],
    ),
)
