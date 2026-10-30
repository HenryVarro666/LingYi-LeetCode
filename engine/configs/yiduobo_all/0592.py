def _fl(S):
    if 'frac_list' not in S:
        return ''
    fs = ' ， '.join(f"{a}/{b}" for a, b in S['frac_list'])
    cur = f"　正在读：分子 `{S['x']}` 分母 `{S['y']}`" if 'x' in S and 'y' in S and 'nowx' not in S else ''
    return f"`frac_list` = ==[{fs}]=={cur}"


def _sum(S):
    if 'nowx' not in S:
        return ''
    return f"当前结果 `{S['nowx']}/{S['nowy']}`"


CONFIG = dict(
    num=592, title='分数加减运算', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='拆分数 · 通分累加 · gcd 约分',
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
    call="Solution().fractionAddition('1/3-1/2')",
    expect='-1/6',
    views=[
        dict(type='string', var='expression', pointers={'pos': 'blue'}, h=170),
        dict(type='text', fn=_fl, h=100),
        dict(type='text', fn=_sum, h=60),
    ],
    watch=[('pos', 'pos', 'blue'), ('flag', 'flag', 'orange'), 'x', 'y', ('nowx', 'nowx', 'green'), ('nowy', 'nowy', 'green')],
    captions={
        15: lambda S, B, r: f"`expression[{S.pos}] = '{S.expression[S.pos]}'`：" + ("遇到符号 → ==上一个分数读完了==" if S.expression[S.pos] in '+-' else "不是 `+` `-`，是数字或 `/`"),
        17: '这个符号是 `{expression[pos]}`，决定下一个分数的正负',
        23: lambda S, B, r: f"`expression[{S.pos}] = '{S.expression[S.pos]}'`：" + ("是 `/` → 分子读完，转去读分母" if S.expression[S.pos] == '/' else "不是 `/`，是数字"),
        'frac_list.append([x * flag': '把读完的分数连同符号存起来：`[{x*flag}, {y}]` → `{frac_list}`',
        24: '`num_flag = False`：后面的数字都是分母',
        'x = x * 10': '读分子：`x = {B.x}*10 + {expression[pos]}` = =={x}==（多位数逐位累加）',
        'y = y * 10': '读分母：`y = {B.y}*10 + {expression[pos]}` = =={y}==',
        4: '先假设第一个分数为正：`flag = 1`',
        18: '符号为 `+` → `flag = 1`',
        20: '符号为 `-` → `flag = -1`，减号当作「加负分子」',
        39: '最终结果先按正数处理：`flag = 1`',
        41: '结果为负 → `flag = -1`，后面对绝对值求 gcd',
        'num_flag = True': '新分数开始，先读分子',
        'x = y = 0': '`x、y` 清零，准备读下一个分数',
        'nowx, nowy = frac_list[0]': '以第一个分数 `{nowx}/{nowy}` 为起点',
        'nowx = nowx * y': '通分相加：`a/b + c/d = (a*d + b*c)/(b*d)` → 分子 `{B.nowx}*{y} + {B.nowy}*{x}` = =={nowx}==',
        'nowy *= y': '分母 `{B.nowy} * {y}` = =={nowy}==，当前结果 `{nowx}/{nowy}`',
        'if nowx < 0': '`nowx = {nowx}`：{"为负 → 记下符号，取绝对值求 gcd" if nowx < 0 else "非负，直接求 gcd"}',
        'tmp = tmpy % tmpx': '辗转相除：`{tmpy} % {B.tmpx}` = {tmp}',
        'while tmpx': lambda S, B, r: f'`tmpx = {S.tmpx}`：' + ('不为 0，继续辗转相除' if S.tmpx else '为 0，==gcd 就是 tmpy=={}'.format(S.tmpy)),
        'return': '约分：分子分母同除 gcd `{tmpy}` → =={ret}==（符号 `flag` 补回去）',
    },
    max_steps=110,
    cards=dict(
        one_liner='负号当作「加负分子」，通分累加后用 gcd 约分',
        complexity='时间 `O(n·log)`，空间 `O(n)`（n 为分数个数）',
        problem=['字符串形如 `-1/2+1/2+1/3`，做分数加减，返回最简分数',
                 '整数结果要写成分母为 1，如 `0/1`',
                 '示例：`1/3-1/2` → `-1/6`'],
        quote='这里我们将减号统一视为加号，例如对于a/b - c/d，我们看做a/b + (-c)/d',
        quote_src='—— yiduobo 题解原文',
        idea=['数据范围很小，直接暴力通分：`a/b + c/d = (a*d + b*c)/(b*d)`',
              '先扫描字符串，按 `+`/`-` 切出每个分数，`/` 切出分子分母',
              '累加完最后用最大公约数约分，负号单独处理'],
        summary=['时间 `O(n)` 次通分 + 一次 gcd，空间 `O(n)`',
                 '易错：第一个分数没有符号；最后一个分数循环结束后要补加入',
                 '分子可能为负，gcd 前先取绝对值再补符号',
                 '原文为 Python 2 写法，最后返回里的整数除法 `/` 已改为 `//`'],
    ),
)
