def _frac(S):
    if 'frac_list' not in S:
        return ''
    fl = S['frac_list']
    parts = ' ， '.join(f'`{x}/{y}`' for x, y in fl)
    s = f'已拆出：{parts}' if fl else '还没拆出分数'
    if 'nowx' in S and 'index' in S:
        s += f"\n通分累加：`{S['nowx']}/{S['nowy']}`"
    return s


CONFIG = dict(
    num=592, title='分数加减运算', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='拆分数 + 通分累加 + gcd 约分',
    code='''
class Solution(object):
    def fractionAddition(self, expression):
        flag = 1
        pos = 0
        if expression[0] == '-':
            flag = -1
            pos = 1

        frac_list = []
        x = 0
        y = 0
        num_flag = True
        while pos < len(expression):
            if expression[pos] == '+'  or expression[pos] == '-':
                frac_list.append([x * flag, y])
                if expression[pos] == '+':
                    flag = 1
                else:
                    flag = -1
                num_flag = True
                x = y = 0
            elif expression[pos] == '/':
                num_flag = False
            elif num_flag:
                x = x * 10 + int(expression[pos])
            else:
                y = y * 10 + int(expression[pos])

            pos += 1
        frac_list.append([x * flag, y])

        nowx, nowy = frac_list[0]
        for index in range(1, len(frac_list)):
            x, y = frac_list[index]
            nowx = nowx * y + nowy * x
            nowy *= y

        flag = 1
        if nowx < 0:
            flag = -1
            nowx = -nowx
        tmpx = nowx
        tmpy = nowy
        while tmpx:
            tmp = tmpy % tmpx
            tmpy = tmpx
            tmpx = tmp
        return '%d/%d' % (flag * nowx // tmpy, nowy // tmpy)
''',
    call='Solution().fractionAddition("1/2+1/6")',
    expect="2/3",
    views=[
        dict(type='string', var='expression', label='expression（pos 逐字符扫描）', cell=70, pointers={'pos': 'blue'}, h=170),
        dict(type='text', fn=_frac, size=28, h=130),
    ],
    max_steps=90,
    watch=[('pos', 'pos', 'blue'), ('flag', 'flag'), ('x', 'x', 'cyan'), ('y', 'y', 'pink'),
           ('nowx', 'nowx', 'green'), ('nowy', 'nowy', 'green')],
    captions={
        "expression[0] == '-'": '第一个分数是正数时 `+` 被省略；这里是 `{expression[0]!r}`，不是负号，`flag` 保持 1',
        'frac_list = []': '`frac_list` 存拆出来的 `[分子, 分母]`，减号一律看成“负的分子”',
        'num_flag = True': '`num_flag` 为真表示正在读分子，遇到 `/` 后改读分母',
        'while pos < len': lambda S, B, r: (f'扫描到 `expression[{S.pos}] = {S.expression[S.pos]!r}`' if S.pos < len(S.expression)
                                             else '扫描完了，最后一个分数还没入表'),
        "== '+'  or": lambda S, B, r: (f"`{S.expression[S.pos]!r}` 是符号 → 前一个分数结束" if S.expression[S.pos] in '+-'
                                       else f"`{S.expression[S.pos]!r}` 不是符号，继续判断"),
        'frac_list.append([x * flag, y])': '分数 `{x * flag}/{y}` 入表（符号乘进分子）',
        "if expression[pos] == '+':": '后一个分数的符号：`+` 记 1，`-` 记 -1',
        3: '`flag` 记符号：1 为正，-1 为负，先假设第一个分数为正',
        17: '`flag = 1`，下一个分数为正',
        19: '`flag = -1`，下一个分数为负',
        38: '`flag = 1`：结果符号先记为正，下面若分子为负再改',
        'x = y = 0': '`x`、`y` 清零，准备读下一个分数',
        'num_flag = False': '`num_flag = False`：接下来读分母',
        "== '/'": lambda S, B, r: ('遇到 `/`：分子读完了，后面读分母' if S.expression[S.pos] == '/' else f"`{S.expression[S.pos]!r}` 也不是 `/`，是数位"),
        'elif num_flag': '`num_flag = {num_flag}` → 当前在读 =={"分子" if num_flag else "分母"}==',
        'x = x * 10': '`x` 累加数位 → `{x}`',
        'y = y * 10': '`y` 累加数位 → `{y}`',
        'nowx, nowy = frac_list[0]': '先取第一个分数 `{nowx}/{nowy}` 作为累计值',
        'x, y = frac_list[index]': '取下一个分数 `{x}/{y}`',
        'nowx = nowx * y': '通分：分子 `{B.nowx}×{y} + {B.nowy}×{x}` = =={nowx}==',
        'nowy *= y': '分母 `{B.nowy}×{y}` = =={nowy}==（`a/b + c/d = (a·d + b·c)/(b·d)`）',
        'if nowx < 0': lambda S, B, r: ('分子为负，先记下符号、取绝对值，方便求 gcd' if S.nowx < 0
                                        else '分子非负，直接求 gcd'),
        'while tmpx': lambda S, B, r: (f'辗转相除：`tmpx = {S.tmpx}`，`tmpy = {S.tmpy}`，`tmpx ≠ 0` 继续' if S.tmpx
                                       else f'`tmpx = 0`，此时 `tmpy = {S.tmpy}` 就是 ==最大公约数=='),
        'tmp = tmpy % tmpx': '`tmp = {tmpy} % {tmpx}` = {tmp}',
        'tmpy = tmpx': '`tmpy` ← 上一轮的 `tmpx` = {tmpy}',
        'tmpx = tmp': '`tmpx` ← 余数 {tmpx}',
        'return': '分子分母同除 gcd `{tmpy}` → `{ret}`',
    },
    cards=dict(
        one_liner='先拆成分数，再暴力通分累加，最后用 gcd 约分',
        complexity='时间 `O(n·L)`（n 个分数，gcd 对数级），空间 `O(n)`',
        problem=['给字符串 `expression`，由 `±分子/分母` 组成，返回最简分数结果',
                 '整数结果要写成 `x/1`；分子分母范围 `[1,10]`，至多 10 个分数',
                 '本视频：`"1/2+1/6"` → `"2/3"`'],
        quote='这里我们将减号统一视为加号，例如对于a/b - c/d，我们看做a/b + (-c)/d',
        quote_src='—— yiduobo 题解原文',
        idea=['数据很小，直接暴力通分：`a/b + c/d = (a·d + b·c)/(b·d)`',
              '一趟扫描，按 `+`/`-` 切开，遇到 `/` 切换读分子/分母；符号乘进分子',
              '累加完后求分子分母的 gcd，同除即得最简分数'],
        summary=['原文为 Python 2 写法，最后一行 `/` 是整数除法，已改为 `//`，并删去了类型说明文档字符串',
                 '时间 `O(n)` 次通分，分母最多 10^10，不会溢出 Python 整数',
                 '易错：首个分数无符号；负数要先取绝对值再求 gcd，符号单独乘回去',
                 '分子为 0 时 `while tmpx` 不进循环，gcd = 分母，结果为 `0/1`',
                 '对比灵神：灵神用有理数类自动约分，这里手写通分与 gcd'],
    ),
)
