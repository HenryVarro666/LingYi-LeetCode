CONFIG = dict(
    num=726, title='原子的数量', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='栈 + 表达式解析（Go 原文转写）',
    tags=['灵神题单', '常用数据结构'],
    code='''
def isDigit(b: str) -> bool:
    return '0' <= b and b <= '9'

def isLower(b: str) -> bool:
    return 'a' <= b and b <= 'z'

class Solution:
    def countOfAtoms(self, s: str) -> str:
        ans = ''
        stack = [defaultdict(int)]
        i, n = 0, len(s)
        def parseNum() -> int:
            nonlocal i
            v = 0
            if i == n or not isDigit(s[i]):
                return 1
            while i < n and isDigit(s[i]):
                v = v * 10 + int(s[i])
                i += 1
            return v
        while i < n:
            if s[i] == '(':
                stack.append(defaultdict(int))
                i += 1
            elif s[i] == ')':
                mp = stack.pop()
                i += 1
                v = parseNum()
                for k, c in mp.items():
                    stack[-1][k] += c * v
            else:
                st = i
                i += 1
                while i < n and isLower(s[i]):
                    i += 1
                name = s[st:i]
                stack[-1][name] += parseNum()
        mp = stack[0]
        ss = []
        for k in mp:
            ss.append(k)
        ss.sort()
        for k in ss:
            ans += k
            v = mp[k]
            if v > 1:
                ans += str(v)
        return ans
''',
    call='Solution().countOfAtoms("Mg(OH)2")',
    expect='H2MgO2',
    skip=[2, 5],
    max_steps=100,
    views=[
        dict(type='text', fn=lambda S: (f"`i = {S['i']}`：正在看 `{S['s'][S['i']]}`" if 'i' in S and 's' in S and 0 <= S['i'] < len(S['s']) and isinstance(S['s'], str) else '栈顶的 map 记录当前括号层里各原子的数量')),
        dict(type='string', var='s', label='化学式 s', pointers={'i': 'blue', 'st': 'pink'}, h=210, cell=84),
        dict(type='stack', var='stack', label='stack：每层括号一个 map（栈底在左）', h=260, fmt=lambda d: str(dict(d)) if d else '{}'),
    ],
    watch=[('i', 'i', 'blue'), ('st', 'st', 'pink'), 'name', 'v', ('ans', 'ans', 'green')],
    captions={
        'stack = [defaultdict': '栈里先放一个空 map，装最外层的原子数量',
        'i, n = 0': '`i` 是扫描位置，`n = {n}`',
        'def parseNum': '`parseNum`：读取原子或右括号后面的数字，没有数字就是 `1`',
        'if i == n or not isDigit': lambda S, B, r: ('后面没有数字 → 数量默认是 `1`' if S['i'] == S['n'] or not isDigit(S['s'][S['i']]) else f"`{S['s'][S['i']]}` 是数字 → 开始读数"),
        'v = v * 10': '`v = v * 10 + {s[i]}` → `{v}`：多位数逐位累加',
        'while i < n and isDigit': lambda S, B, r: (f"`{S['s'][S['i']]}` 还是数字，继续读" if S['i'] < S['n'] and isDigit(S['s'][S['i']]) else '数字读完了'),
        'return 1': '没有数字，数量是 `1` → 回到上一行累加：栈顶 = `{dict(stack[-1])}`' if False else '没有数字，数量是 `1`',
        'return v': '数字是 `{v}`',
        'while i < n:': lambda S, B, r: (f"`i = {S['i']} < {S['n']}`，继续扫描" if S['i'] < S['n'] else f"`i = {S['i']} = n`：全部扫完，栈里只剩最外层 map"),
        "if s[i] == '('": lambda S, B, r: f"当前字符 `{S['s'][S['i']]}`" + ('，是左括号 → 新开一层' if S['s'][S['i']] == '(' else '，不是左括号'),
        'stack.append(defaultdict': '遇到 `(`：压入一个新的空 map，括号里的原子先记在这层',
        "elif s[i] == ')'": lambda S, B, r: f"当前字符 `{S['s'][S['i']]}`" + ('，是右括号 → 这一层结束' if S['s'][S['i']] == ')' else '，是原子名的开头 → 走 else'),
        'mp = stack.pop()': '右括号：弹出栈顶 map `{dict(mp)}`，等读完后面的数字再乘上去',
        'v = parseNum()': '括号后面的倍数 `v = {v}`',
        'for k, c in mp.items()': lambda S, B, r: ('括号里的原子都合并完了' if 'k' in B and B['k'] == S['k'] else f"括号里的每个原子 `{S['k']}` 数量 `{S['c']}`，都要乘以 `{S['v']}`"),
        'stack[-1][k] += c * v': '合并到外一层：`{k}` += `{c} × {v}`，现在栈顶 = `{dict(stack[-1])}`',
        'st = i': '原子名从 `{st}` 开始，大写字母后面可能跟小写字母',
        'while i < n and isLower': lambda S, B, r: (f"`{S['s'][S['i']]}` 是小写字母 → 还是同一个原子名" if S['i'] < S['n'] and isLower(S['s'][S['i']]) else '原子名结束了'),
        'name = s[st:i]': '原子名 `{name}`',
        'stack[-1][name] += parseNum()': '读 `{name}` 后面的数字（`parseNum()`），加到栈顶 map 里',
        'mp = stack[0]': '最外层 map：`{dict(mp)}`',
        'ss.sort()': '题目要求按字典序输出：`{ss}`',
        'ans += k': '先写原子名：`ans = {ans}`',
        'if v > 1': '数量 `{v}`，只有大于 1 才写数字',
        'ans += str(v)': '写上数量：`ans = {ans}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='每层括号一个 map，遇到右括号弹栈再乘倍数合并',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['化学式里原子 = 大写字母 + 若干小写字母，后面可跟数量；括号后也可跟倍数',
                 '统计每种原子的数量，按字典序输出，数量为 1 不写',
                 '示例：`Mg(OH)2` → `H2MgO2`'],
        quote='理解清楚题意就能一遍过',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['栈里存每层括号的 `map[原子] → 数量`，一开始只有最外层',
              '`(`：压入新 map；`)`：弹出 map，读后面的数字 `v`，每个数量乘 `v` 并入新栈顶',
              '原子：大写字母 + 小写字母得到名字，数量加上后面的数字（没有就是 1）'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；`for s, c := range mp` 里的 `s` 会遮住外层字符串，Python 里没有块作用域，改名为 `k` 避免覆盖',
                 '`map` → `defaultdict(int)`；`parseNum` 用 `nonlocal i` 共享扫描位置',
                 '时间 `O(n^2)`（嵌套括号层层合并），空间 `O(n)`',
                 '易错：数字可能多位；`)` 后的数字要在弹栈之后立刻读；数量为 1 不写数字',
                 '同类题：224 基本计算器、394 字符串解码'],
    ),
)
