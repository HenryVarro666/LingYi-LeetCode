S_IN = '  -042a1'


def _cells(S):
    return [c if c != ' ' else '␣' for c in S['s']] if 's' in S else None


def _phase(S):
    ln = S.get('_line', 0)
    if ln <= 8:
        return 0
    if ln <= 14:
        return 1
    return 2


def _read_upto(S):
    """characters [0, r) have been consumed (the digit just added on L20/L21 counts too)"""
    i = S.get('i')
    if i is None:
        return 0
    return i + 1 if S.get('_line') in (20, 21, 22) else i


def _color(S, k, v):
    i = S.get('i')
    if i is None:
        return None
    s = S['s']
    if k < _read_upto(S):
        if s[k] == ' ':
            return None
        if s[k] in '+-':
            return 'purple'
        return 'green'
    return None


def _dim(S, k, v):
    i = S.get('i')
    return i is not None and k < i and S['s'][k] == ' '


def _stages(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'i' not in S:
        return
    ph = _phase(S)
    names = ['① 跳过前导空格', '② 处理正负号', '③ 逐位读数字']
    w = (x1 - x0 - 80) / 3
    for k, nm in enumerate(names):
        X = x0 + 30 + k * (w + 10)
        on = k == ph
        done = k < ph
        cv.rect((X, y0 + 10, X + w, y0 + 64), fill=T['blue'] if on else T['panel2'], r=12,
                outline=T['border'], width=1)
        cv.text((X + w / 2, y0 + 37), nm + (' ✓' if done else ''), 26, T['bg'] if on else (T['green'] if done else T['muted']),
                anchor='mm', bold=True)
    if 'num' not in S:
        return
    s = S['s']
    st = 0
    while st < len(s) and s[st] == ' ':
        st += 1
    if st < len(s) and s[st] in '+-':
        st += 1
    r = _read_upto(S)
    hist, num = [], 0
    for c in s[st:r]:
        if '0' <= c <= '9':
            num = num * 10 + int(c)
            hist.append((c, num))
    cv.text((x0 + 30, y0 + 96), 'num 的累加过程（num × 10 + 新数字）', 24, T['muted'], bold=True)
    X, Y = x0 + 30, y0 + 150
    cv.rect((X, Y, X + 70, Y + 56), fill=T['panel2'], r=10)
    cv.text((X + 35, Y + 28), '0', 28, T['text'], anchor='mm', bold=True, mono=True)
    X += 70
    for c, v in hist:
        lab = f'+{c}'
        cv.text((X + 50, Y + 20), lab, 22, T['green'], anchor='mb', bold=True)
        cv.arrow((X + 12, Y + 28), (X + 88, Y + 28), T['muted'], 3, 12)
        X += 100
        txt = str(v)
        tw = max(70, cv.tlen(txt, 28, True, True) + 30)
        cv.rect((X, Y, X + tw, Y + 56), fill=T['green'], r=10)
        cv.text((X + tw / 2, Y + 28), txt, 28, T['bg'], anchor='mm', bold=True, mono=True)
        X += tw
    if S.get('_line') == 25:
        X += 20
        cv.text((X, Y + 28), f"× sign({S['sign']}) = {S['sign'] * S['num']}", 28, T['orange'], anchor='lm', bold=True, mono=True)


def _formula(S, B):
    ln = S.get('_line', 0)
    if ln == 20:
        d = int(S['s'][S['i']])
        return f"`num = {B['num']} × 10 + {d}` = =={S['num']}==　　（MX = `2^31 − 1 = {(1 << 31) - 1}`）"
    if 'num' in S:
        return f"已读入 `num = {S['num']}`，`sign = {S['sign']}`"
    if 'sign' in S:
        return f"符号 `sign = {S['sign']}`"
    if 'i' in S:
        return '第一步：跳过前导空格（灰色 ␣）'
    return ''


def _while_space(S, B, ret):
    i, s, n = B.i, B.s, B.n
    if i < n and s[i] == ' ':
        return f'`s[{i}]` 是空格 → 跳过'
    if i >= n:
        return '`i == n`：字符串已经读完'
    return f"`s[{i}] = '{s[i]}'` 不是空格 → 前导空格跳完了，`i` 停在 {i}"


def _if_sign(S, B, ret):
    i, s, n = B.i, B.s, B.n
    if i < n and s[i] in '+-':
        return f"`s[{i}] = '{s[i]}'` 是正负号 → 记录符号"
    return f'`s[{i}]` 不是正负号 → 默认正数 `sign = 1`'


def _while_digit(S, B, ret):
    i, s, n = B.i, B.s, B.n
    if i < n and '0' <= s[i] <= '9':
        return f"`s[{i}] = '{s[i]}'` 是数字 → 继续读"
    if i >= n:
        return '`i == n`：字符串读完了 → 结束'
    return f"`s[{i}] = '{s[i]}'` ==不是数字== → 读入停止，后面的字符全部忽略"


def _num(S, B, ret):
    d = int(S.s[S.i])
    extra = '：前导零不影响结果' if B.num == 0 and d == 0 else ''
    return f"`num = {B.num} × 10 + {d} = {S.num}`{extra}"


def _inc(S, B, ret):
    ln = S._line
    if ln == 8:
        return f'空格不影响结果，跳过：`i` → {S.i}'
    if ln == 14:
        return f'符号读完，`i` → {S.i}，开始读数字'
    return f'`i` → {S.i}，看下一个字符'


CONFIG = dict(
    num=8, title='字符串转换整数 (atoi)', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='三步走：空格 → 符号 → 数字（提前截断）',
    tags=['热题173'],
    code='''
class Solution:
    def myAtoi(self, s: str) -> int:
        n = len(s)

        # 跳过前导空格
        i = 0
        while i < n and s[i] == ' ':
            i += 1

        # 处理正负号
        sign = 1
        if i < n and s[i] in "+-":
            sign = 1 if s[i] == '+' else -1
            i += 1

        # 处理数字
        MX = (1 << 31) - 1
        num = 0
        while i < n and '0' <= s[i] <= '9':
            num = num * 10 + int(s[i])
            if num > MX:  # 最终答案已确定，提前返回
                return MX if sign > 0 else -(1 << 31)
            i += 1

        return sign * num
''',
    call=f'Solution().myAtoi({S_IN!r})',
    expect=-42,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='string', var=_cells, label="s（␣ = 空格，紫 = 符号，绿 = 已读入的数字）", cell=96, h=230,
             pointers={'i': 'blue'}, color=_color, dim=_dim),
        dict(type='custom', draw=_stages, h=260),
    ],
    watch=[('i', 'i', 'blue'), ('sign', 'sign', 'purple'), ('num', 'num', 'green')],
    captions={
        'n = len(s)': "输入 `s = '{s}'`，长度 `n = {n}`",
        'i = 0': '`i` 从 0 开始扫描：先跳过前导空格',
        "while i < n and s[i] == ' '": _while_space,
        8: _inc,
        14: _inc,
        23: _inc,
        11: '先假设是正数：`sign = 1`',
        "if i < n and s[i] in": _if_sign,
        "sign = 1 if s[i]": "`'{s[i]}'` → `sign = {sign}`",
        'MX = (1 << 31) - 1': '`MX = 2^31 − 1 = {MX}`：超过它就要截断',
        'num = 0': '`num` 从 0 开始累加：==只累加绝对值==，符号最后再乘',
        "while i < n and '0'": _while_digit,
        'num = num * 10': _num,
        'if num > MX': lambda S, B, ret: (f'`{S.num} > MX`：==答案已确定==，提前返回' if S.num > S.MX
                                          else f'`num = {S.num} ≤ MX`，没有越界'),
        'return sign * num': '返回 `sign × num = {sign} × {num}` = =={ret}==',
    },
    skip=[],
    cards=dict(
        one_liner='三步走：跳过空格，读符号，逐位累加数字，超出范围立刻截断',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把字符串 `s` 转成 32 位有符号整数：',
                 '① 丢弃前导空格　② 读 `+`/`-`（没有就是正数）',
                 '③ 跳过前导零读数字，遇到==非数字字符==就停',
                 '④ 超出 `[−2^31, 2^31 − 1]` 就截断到边界',
                 '示例：`"   -042"` → `-42`；本视频：`"  -042a1"` → `-42`'],
        quote='在处理数字的过程中，如果发现 num·10 + d > mx，则可以提前返回答案。如果 sign=1，返回 2^31−1，否则返回 −2^31。',
        quote_src='—— 灵茶山艾府题解 · 四、处理截断',
        idea=['`num` 只存==绝对值==：读字符 `d` 就 `num = num × 10 + d`',
              '读完后乘上 `sign`；中途一旦 `num > MX` 就提前返回边界值',
              '负数时 `num = 2^31` 也会被判为 `> MX`，返回 `−2^31` 恰好正确'],
        after=[dict(heading='截断：为什么能提前返回？', lines=[
            '一旦 `num > MX`，后面不管再读多少位，绝对值只会更大',
            '所以 `sign > 0` 直接返回 `MX`，否则返回 `−2^31`',
            '其它语言只能用 32 位整数时：把 `num·10 + d > MX` 拆成',
            '`num > MX / 10`（下取整）或 `num·10 > MX − d`，避免乘法溢出',
        ])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：每一步都要先判断 `i < n`，空串、全空格都要能处理',
                 '符号只能出现一次，且必须紧跟在空格之后：`"+-12"` → `0`',
                 '遇到非数字立即停止：`"0-1"` → `0`，`"words 987"` → `0`',
                 '同类题：65. 有效数字'],
    ),
)
