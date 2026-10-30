A, B_ = '456', '77'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '竖式加法：从低位（右）到高位（左）', 22, T['muted'], bold=True)
    n = max(len(A), len(B_)) + 1
    cell = 92
    right = x0 + (x1 - x0) / 2 + n * cell / 2
    rows = {'carry': y0 + 56, 'a': y0 + 110, 'b': y0 + 190, 'r': y0 + 300}
    idx = S.get('index')
    res = S.get('res')
    done = S['_line'] >= 21   # 循环结束之后

    def X(i):  # 第 i 位（从低位数起）的格子左边
        return right - (i + 1) * cell

    if idx is not None and not done:
        cv.rect((X(idx) + 4, rows['carry'] - 6, X(idx) + cell - 4, rows['r'] + 70), fill=T['panel2'], outline=T['yellow'], width=3, r=12)
    for s, key in ((A, 'a'), (B_, 'b')):
        L = len(s)
        for i in range(L):
            used = idx is not None and (i < idx or (i == idx and S['_line'] >= 9 and (key == 'a' or S['_line'] >= 11)))
            cv.text((X(i) + cell / 2, rows[key] + 30), s[L - 1 - i], 48, T['text'] if not used or i == idx else T['muted'],
                    anchor='mm', mono=True, bold=True)
    cv.text((X(n - 1) + cell / 2, rows['b'] + 30), '+', 44, T['muted'], anchor='mm', bold=True)
    cv.line([(X(n - 1) + 10, rows['b'] + 76), (right - 6, rows['b'] + 76)], T['muted'], 3)
    if res is not None:
        for i, d in enumerate(res):
            cv.text((X(i) + cell / 2, rows['r'] + 30), d, 48, T['green'], anchor='mm', mono=True, bold=True)
    x = S.get('x')
    k = None
    if x == 1 and idx is not None:
        if S['_line'] == 16:
            k = idx + 1                      # 刚产生进位：写在下一位上方
        elif S['_line'] in (9, 10) and not done:
            k = idx                          # 新的一位：上一位的进位
        elif S['_line'] in (21, 22):
            k = idx + 1
    if k is not None:
        cv.text((X(k) + cell / 2, rows['carry'] + 22), '+1', 28, T['orange'], anchor='mm', bold=True)
    cv.text((x0 + 30, rows['a'] + 30), 'num1', 22, T['muted'], anchor='lm')
    cv.text((x0 + 30, rows['b'] + 30), 'num2', 22, T['muted'], anchor='lm')
    cv.text((x0 + 30, rows['r'] + 30), 'res', 22, T['muted'], anchor='lm')
    cv.text((x0 + 30, rows['carry'] + 22), '进位 x', 22, T['orange'], anchor='lm')


def _for(S, B, ret):
    if 'index' in B and B.index == S.index:
        return '所有位都加完了'
    i = S.index
    return f'第 `index = {i}` 位（从低位数起），当前 `x = {S.x}`（上一位的进位）'


def _if1(S, B, ret):
    if S.index < S.l1:
        return f'`num1` 还有第 {S.index} 位：`num1[{S.l1 - S.index - 1}] = {A[S.l1 - S.index - 1]}`'
    return f'`num1` 只有 {S.l1} 位，这一位当 0'


def _if2(S, B, ret):
    if S.index < S.l2:
        return f'`num2` 还有第 {S.index} 位：`num2[{S.l2 - S.index - 1}] = {B_[S.l2 - S.index - 1]}`'
    return f'`num2` 只有 {S.l2} 位，这一位当 0'


def _ge(S, B, ret):
    if S.x >= 10:
        return f'`x = {S.x}` ≥ 10 → ==要进位=='
    return f'`x = {S.x}` < 10 → 不进位'


CONFIG = dict(
    num=415, title='字符串相加', difficulty='Easy', category='数学',
    author='yiduobo', technique='高精度加法 · 逐位相加维护进位',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def addStrings(self, num1, num2):

        l1 = len(num1)
        l2 = len(num2)

        x = 0
        res = []
        for index in range(max(l1, l2)):
            if index < l1:
                x += int(num1[l1 - index - 1])
            if index < l2:
                x += int(num2[l2 - index - 1])
            if x >= 10:
                res.append(x - 10)
                x = 1
            else:
                res.append(x)
                x = 0

        if x:
            res.append(x)

        res.reverse()
        return ''.join([str(x) for x in res])
''',
    call=f'Solution().addStrings({A!r}, {B_!r})',
    expect='533',
    skip=['l1 = len', 'l2 = len'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='res', label='res（低位在前，最后再反转）', cell=80, h=150),
    ],
    watch=[('index', 'index', 'yellow'), ('x', 'x', 'orange'), ('l1', 'l1'), ('l2', 'l2')],
    captions={
        7: '`x` 是当前位的和（含上一位进位），一开始为 0',
        'res = []': '`res` 从低位到高位存结果的每一位',
        'for index in range': _for,
        'if index < l1': _if1,
        'x += int(num1': '`x` += `{int(num1[l1 - index - 1])}` → {x}',
        'if index < l2': _if2,
        'x += int(num2': '`x` += `{int(num2[l2 - index - 1])}` → {x}',
        'if x >= 10': _ge,
        'res.append(x - 10)': '这一位写 `{B.x} − 10 = {res[-1]}`',
        'x = 1': '进位 `x = 1`，带到下一位',
        18: '这一位写 `{res[-1]}`',
        19: '没有进位，`x = 0`',
        'if x:': lambda S, B, ret: ('最高位还有进位 → 结果多一位' if S.x else '最高位没有进位，不用补'),
        'res.append(x)': '补上最高位 `{x}`',
        'res.reverse()': '`res` 是低位在前，反转成高位在前：`{res}`',
        'return': '拼成字符串：=={ret!r}==',
    },
    cards=dict(
        one_liner='从低位到高位逐位相加，注意维护进位',
        complexity='时间 `O(max(l1, l2))`，空间 `O(max(l1, l2))`',
        problem=['给两个字符串形式的非负整数 `num1`、`num2`，返回它们的和（也用字符串表示）',
                 '==不能==用大整数库，也不能直接把输入转成整数',
                 '示例：`"11" + "123"` → `"134"`；`"456" + "77"` → `"533"`'],
        quote='经典的==高精度加法==问题，从低到高位逐位执行加法即可。过程中需要注意==维护进位==的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `index` 位（从低位数起）是 `num[l - index - 1]`，位数不够就当 0',
              '`x` = 两个数这一位之和 + 上一位进位；`x ≥ 10` 写 `x − 10` 并进位 1',
              '循环结束后若还有进位，补一个最高位；最后反转拼接'],
        result='`"456" + "77" = "533"` ✓',
        summary=['时间、空间都是 `O(max(l1, l2))`',
                 '易错：循环结束后别忘了最后的进位（如 `"9" + "1" = "10"`）',
                 '`res` 低位在前，返回前要 `reverse`',
                 '原文为 Python 2 风格，只删去了文档字符串',
                 '同类：2 题两数相加（链表）、43 题字符串相乘'],
    ),
)
