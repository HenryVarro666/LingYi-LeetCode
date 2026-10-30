S_IN = ' -2147483649'


def _cells(S):
    return [c if c != ' ' else '␣' for c in S['str']] if 'str' in S else None


def _consumed(S):
    """how many characters have been fully processed"""
    idx = S.get('index')
    if idx is None:
        return 0
    return idx + 1 if S.get('_line') in (11, 13, 14, 16, 17, 19, 29) else idx


def _color(S, k, v):
    idx = S.get('index')
    if idx is None:
        return None
    s = S['str']
    if k < _consumed(S):
        if s[k] == ' ':
            return None
        if s[k] in '+-':
            return 'purple'
        return 'green'
    if k == idx and s[k].isdigit() and S.get('x') is not None:
        x, d, ln = S['x'], int(s[k]), S.get('_line')
        over = x > 214748364 or (x == 214748364 and d > 7)
        under = x < -214748364 or (x == -214748364 and d > 8)
        if (ln in (24, 25) and over) or (ln in (26, 27) and under):
            return 'red'
    return None


def _cmp(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    idx, x = S.get('index'), S.get('x')
    if idx is None or x is None:
        return
    s, ln = S['str'], S.get('_line')
    if ln in (13, 14, 16, 17):
        return
    digits = str(abs(x)) if x != 0 else ''
    if ln != 29 and ln != 19:
        if not s[idx].isdigit():
            return
        digits += s[idx]
    flag = S['negative_flag']
    bound = '2147483647' if flag > 0 else '2147483648'
    cv.text((x0 + 18, y0 + 4), '越界检查：把 x 的绝对值拼上新数字，和边界逐位对齐比较', 24, T['muted'], bold=True)
    cell = 62
    right = x1 - 60
    rows = [(f"{'int_max' if flag > 0 else '|int_min|'}", bound), ('|x| 拼上新数字', digits)]
    diff = None
    if len(digits) == 10:
        for k in range(10):
            if digits[k] != bound[k]:
                diff = k
                break
    for r, (name, txt) in enumerate(rows):
        Y = y0 + 50 + r * 76
        cv.text((x0 + 30, Y + 30), name, 26, T['text'], anchor='lm', bold=True)
        for k, ch in enumerate(txt):
            X = right - (len(txt) - k) * cell
            c = T['panel2']
            if r == 1:
                c = T['green']
                if diff is not None and k == diff:
                    c = T['red'] if digits > bound else T['green']
                if k == len(txt) - 1 and ln != 29 and ln != 19:
                    c = c if c == T['red'] else T['yellow']
            cv.rect((X + 3, Y, X + cell - 3, Y + 60), fill=c, r=8)
            cv.text((X + cell / 2, Y + 30), ch, 32, T['bg'] if r == 1 else T['text'], anchor='mm', bold=True, mono=True)
    Y = y0 + 50 + 2 * 76 + 6
    if len(digits) < 10:
        msg = f'只有 {len(digits)} 位，不到 10 位 → ==不可能越界=='
    elif digits > bound:
        msg = f'前 {diff} 位相同，第 {diff + 1} 位 `{digits[diff]} > {bound[diff]}` → ==越界=='
    else:
        msg = '10 位但不超过边界 → 安全'
    cv.rich(x0 + 30, Y, msg, x1 - x0 - 60, size=28, accent=T['orange'])


def _dim(S, k, v):
    idx = S.get('index')
    return idx is not None and k < _consumed(S) and S['str'][k] == ' '


def _guard(S, B):
    x = S.get('x')
    if x is None:
        return '`x is None`：还没遇到第一个有效字符（符号或数字）' if 'negative_flag' in S else ''
    flag = S['negative_flag']
    bound = '214748364' if flag > 0 else '-214748364'
    return f"`x = {x}`　　安全线 `{bound}`：越过它再乘 10 必越界"


def _cap_for(S, B, ret):
    if S.get('index') == B.get('index'):
        return '所有字符扫描完毕'
    i = S.index
    c = S.str[i]
    return f"看 `str[{i}] = '{c}'`" if c != ' ' else f'看 `str[{i}]`：空格'


def _cap_xnone(S, B, ret):
    if S.x is None:
        return '`x is None`：还没开始读数 → 先判断是不是==开头=='
    return f'`x = {S.x}` 已经开始读数 → 走后面的 `else`，只接受数字'


def _cap_over(S, B, ret):
    x, d = S.x, int(S.str[S.index])
    if x > 214748364 or (x == 214748364 and d > 7):
        return f'`x = {x}`，再拼上 `{d}` 会超过 `2147483647` → ==越界=='
    if x >= 0:
        return f'`x = {x}`：`× 10 + {d}` 不会超过 `2147483647`'
    return f'`x = {x}` 是负数，不会超过上界'


def _cap_under(S, B, ret):
    x, d = S.x, int(S.str[S.index])
    if x < -214748364 or (x == -214748364 and d > 8):
        tail = '最后一位 `> 8`' if x == -214748364 else '`x < -214748364`'
        return f'`x = {x}`，{tail}：再拼上 `{d}` 会小于 `-2147483648` → ==越界=='
    if x <= 0:
        return f'`x = {x}`：`× 10 − {d}` 不会小于 `-2147483648`'
    return f'`x = {x}` 是正数，不会低于下界'


CONFIG = dict(
    num=8, title='字符串转换整数 (atoi)', difficulty='Medium', category='字符串',
    author='yiduobo', technique='逐字符扫描 · 拼数前判断越界',
    tags=['热题173'],
    code='''
class Solution(object):
    def myAtoi(self, str):
        int_max = 2147483647
        int_min = -2147483648

        x = None
        negative_flag = 1
        for index in range(len(str)):
            if x is None:
                if str[index] == ' ':
                    continue
                elif str[index] == '-':
                    negative_flag = -1
                    x = 0
                elif str[index] == '+':
                    negative_flag = 1
                    x = 0
                elif str[index] >= '0' and str[index] <= '9':
                    x = negative_flag * int(str[index])
                else:
                    return 0
            else:
                if str[index] >= '0' and str[index] <= '9':
                    if x > 214748364 or (x == 214748364 and int(str[index]) > 7):
                        return int_max
                    elif x < -214748364 or (x == -214748364 and int(str[index]) > 8):
                        return int_min
                    else:
                        x = x * 10 + negative_flag * int(str[index])
                else:
                    break
        if x is None:
            x = 0
        return x
''',
    call=f'Solution().myAtoi({S_IN!r})',
    expect=-2147483648,
    views=[
        dict(type='text', fn=_guard, h=60),
        dict(type='string', var=_cells, label="str（␣ = 空格，紫 = 符号，绿 = 已拼进 x 的数字，红 = 会越界的那一位）",
             cell=80, h=230, pointers={'index': 'blue'}, color=_color, dim=_dim),
        dict(type='text', fn=lambda S: (f"范围：`int_min = {S['int_min']}`　`int_max = {S['int_max']}`" if 'int_min' in S else ''),
             size=26, h=60),
        dict(type='custom', draw=_cmp, h=250),
    ],
    watch=[('index', 'index', 'blue'), ('negative_flag', 'negative_flag', 'purple'), ('x', 'x', 'green')],
    captions={
        'int_max = 2147483647': '32 位整数上界 `int_max = 2^31 − 1`',
        'int_min = -2147483648': '下界 `int_min = −2^31`',
        'x = None': '`x = None` 表示==还没读到有效字符==（和 `x = 0` 区分开）',
        7: '符号默认为正',
        'for index in range': _cap_for,
        9: _cap_xnone,
        "if str[index] == ' '": lambda S, B, ret: ('是空格 → 跳过' if S.str[S.index] == ' ' else '不是空格'),
        'continue': '前导空格直接 `continue`',
        "elif str[index] == '-'": lambda S, B, ret: ('是 `-` → 负数' if S.str[S.index] == '-' else '不是 `-`'),
        'negative_flag = -1': '`negative_flag = -1`：之后每一位都乘上它',
        14: '`x = 0`：==从此开始读数==，后面只接受数字',
        "elif str[index] == '+'": lambda S, B, ret: ('是 `+`' if S.str[S.index] == '+' else '不是 `+`'),
        "elif str[index] >= '0'": lambda S, B, ret: ('是数字 → 直接开始读数' if '0' <= S.str[S.index] <= '9' else '也不是数字'),
        'x = negative_flag * int': '第一个字符就是数字：`x = {negative_flag} × {str[index]} = {x}`',
        'return 0': '第一个有效字符既不是符号也不是数字 → 返回 0',
        "                if str[index] >= '0'": lambda S, B, ret: (f"`'{S.str[S.index]}'` 是数字 → 准备拼到 x 后面"
                                                                   if '0' <= S.str[S.index] <= '9' else f"`'{S.str[S.index]}'` 不是数字 → 停止"),
        'if x > 214748364': _cap_over,
        'return int_max': '返回上界 `int_max = {ret}`',
        'elif x < -214748364': _cap_under,
        'return int_min': '截断：返回下界 `int_min` = =={ret}==',
        'x = x * 10': '`x = {B.x} × 10 + ({negative_flag}) × {str[index]}` = =={x}==',
        'break': '遇到非数字 → 结束扫描',
        32: lambda S, B, ret: ('整串都没有有效字符' if S.x is None else '`x` 不为空'),
        'return x': '返回 `x = {ret}`',
    },
    max_steps=46,
    cards=dict(
        one_liner='逐字符扫描：拼下一位之前先看会不会越界',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把字符串转成 32 位有符号整数：丢弃前导空格，读可选的 `+`/`-`',
                 '再读连续的数字，遇到非数字就停；超出 `[−2^31, 2^31 − 1]` 就截断',
                 '示例：`"   -042"` → `-42`，`"1337c0d3"` → `1337`',
                 '本视频：`" -2147483649"` → 越界，返回 `-2147483648`'],
        quote='扫描str找到非空字符如果不符合要求，就返回0，否则往后按位累加，直到非数字字符出现，同时在累加的过程中需要注意判断是否越界。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x = None` 表示还没开始读数：此时只认空格、符号、数字',
              '开始读数后，`x` 带着符号累加：`x = x × 10 + flag × d`',
              '拼之前判断：`x > 214748364`，或 `x == 214748364` 且 `d > 7` → 上溢',
              '负数同理：`x == -214748364` 且 `d > 8` → 下溢'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '越界判断沿用第 7 题（整数反转）：在 ==乘 10 之前== 和 `int_max // 10` 比较',
                 '上下界不对称：正数最后一位最多 7，负数最多 8',
                 '`x is None` 和 `x == 0` 含义不同：`"-"` 之后没有数字时最后返回 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；参数名 `str` 照原文保留',
                 '对比灵神：灵神只存绝对值，`num > MX` 时提前返回'],
    ),
)
