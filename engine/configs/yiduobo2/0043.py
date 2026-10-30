MUL_LINES = range(11, 20)   # 乘法双重循环所在的代码行
OUT_LINES = (30, 31, 32, 34, 36)   # 从高位往低位拼答案


def _top(res):
    return max([p for p in range(len(res)) if res[p] != 0], default=0)


def _draw(cv, S, B, box, T):
    """竖式：每一列是 10 的同一次方，res[k] 画在第 k 列（高位在左）"""
    x0, y0, x1, y1 = box
    num1, num2 = S.get('num1'), S.get('num2')
    if num1 is None:
        return
    m, n = len(num1), len(num2)
    C = m + n
    cell = 96
    xr = (x0 + x1) / 2 + C * cell / 2 + 40

    def X(p):  # 第 p 次方那一列的左边界
        return xr - (p + 1) * cell

    ln = S.get('_line', 0)
    mul = ln in MUL_LINES and 'j' in S and 'ypos' in S
    cv.text((x0 + 18, y0 + 4), '竖式（每列是 10 的同一次方；res[k] 存 10^k 位）', 24, T['muted'], bold=True)
    rows = [('num1', y0 + 52), ('× num2', y0 + 142), ('res', y0 + 262)]
    for name, y in rows:
        cv.text((X(C - 1) - 30, y + 40), name, 28, T['muted'], anchor='rm', bold=True)
    # num1 / num2
    for row, (s, cur, c) in enumerate(((num1, S.get('i'), 'blue'), (num2, S.get('j'), 'pink'))):
        y = rows[row][1]
        L = len(s)
        for idx, ch in enumerate(s):
            p = L - 1 - idx
            hit = mul and idx == cur
            cv.rect((X(p) + 6, y, X(p) + cell - 6, y + 80), fill=T[c] if hit else T['panel2'], r=10,
                    outline=T['border'], width=1)
            cv.text((X(p) + cell / 2, y + 40), ch, 40, T['bg'] if hit else T['text'], anchor='mm', bold=True)
            cv.text((X(p) + cell - 10, y + 76), f'[{idx}]', 16, T['bg'] if hit else T['dim'], anchor='rb', mono=True)
    cv.line([(X(C - 1) - 10, y0 + 240), (xr + 10, y0 + 240)], T['muted'], 3)
    res = S.get('res')
    if res is None:
        return
    bres = B.get('res')
    k = S['xpos'] + S['ypos'] if mul else None
    out = ln in OUT_LINES and 'index' in S
    idx = S.get('index')
    top = _top(res)
    y = rows[2][1]
    for p, v in enumerate(res):
        fill, tc = T['panel2'], T['text']
        if mul and p == k:
            fill, tc = T['yellow'], T['bg']
        elif mul and ln == 18 and p == k + 1:
            fill, tc = T['orange'], T['bg']
        elif out:
            read = p > idx or (p == idx and ln in (34, 36))
            if p > top and p >= idx:
                fill, tc = (40, 45, 53), T['dim']
            elif read:
                fill, tc = T['green'], T['bg']
        changed = bres is not None and len(bres) == len(res) and bres[p] != v
        cv.rect((X(p) + 6, y, X(p) + cell - 6, y + 80), fill=fill, r=10,
                outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
        cv.text((X(p) + cell / 2, y + 40), v, 40, tc, anchor='mm', bold=True)
        cv.text((X(p) + cell / 2, y + 88), f'10^{p}', 18, T['dim'], anchor='mt', mono=True)
    if out and idx is not None and 0 <= idx < C:
        Xc = X(idx) + cell / 2
        cv.tri_up(Xc, y + 118, 11, T['green'])
        cv.text((Xc, y + 134), 'index', 22, T['green'], anchor='mt', bold=True)


def _formula(S):
    ln = S.get('_line', 0)
    if ln in MUL_LINES and 'j' in S and 'ypos' in S:
        i, j, k = S['i'], S['j'], S['xpos'] + S['ypos']
        return (f"`num1[{i}]` 在 10^{S['xpos']} 位，`num2[{j}]` 在 10^{S['ypos']} 位 "
                f"→ 乘积加到 ==10^{k} 位：res[{k}]==")
    if 'res' in S and ln >= 22:
        return '从最高位往下读，==跳过开头的 0=='
    return ''


def _for_i(S, B, ret):
    if S.get('i') is not None and S.get('i') != B.get('i') or 'i' not in B:
        return f"外层取 `num1[{S.i}] = {S.num1[S.i]}`：从右数第 `xpos = {S.xpos}` 位"
    return 'num1 的每一位都乘完了'


def _for_j(S, B, ret):
    if 'j' not in B or S.j != B.j:
        return f"内层取 `num2[{S.j}] = {S.num2[S.j]}`（第 `ypos = {S.ypos}` 位）：`{S.num1[S.i]}×{S.num2[S.j]}` 属于 10^{S.xpos + S.ypos} 位"
    return f"num2 的每一位都乘过 `num1[{S.i}]` 了"


def _if_zero(S, B, ret):
    k = B['index']
    if B['res'][k] == 0 and B['zero_flag']:
        return f"`res[{k}] = 0` 且还在开头 → ==前导零，不能输出=="
    if B['res'][k] == 0:
        return f"`res[{k}] = 0`，但前面已经输出过数字 → ==中间的 0 要保留=="
    return f"`res[{k}] = {B['res'][k]}` 不是 0 → 输出它"


CONFIG = dict(
    num=43, title='字符串相乘', difficulty='Medium', category='数学',
    author='yiduobo', technique='高精度乘法 · 竖式逐位相乘',
    tags=['热题173'],
    code='''
class Solution(object):
    def multiply(self, num1, num2):
        if num1 == '0' or num2 == '0':
            return '0'

        m = len(num1)
        n = len(num2)
        res = [0] * (m + n)

        xpos = 0
        for i in range(m - 1, -1, -1):
            x = int(num1[i])
            ypos = 0
            for j in range(n - 1, -1, -1):
                y = int(num2[j])
                tmp = res[xpos + ypos] + x * y
                res[xpos + ypos] = tmp % 10
                res[xpos + ypos + 1] += tmp // 10
                ypos += 1
            xpos += 1

        tmp = 0
        for index in range(xpos + ypos):
            res[index] += tmp
            tmp = res[index] // 10
            res[index] %= 10

        zero_flag = True
        res_str = ''
        for index in range(xpos + ypos - 1, -1, -1):
            if res[index] == 0 and zero_flag:
                continue
            zero_flag = False
            res_str += str(res[index])

        return res_str
''',
    call="Solution().multiply('12', '34')",
    expect='408',
    skip=['m = len', 'n = len', 'x = int', 'ypos = 0', 'y = int', 'ypos += 1', 'xpos += 1',
          23, 24, 25, 26, 'zero_flag = False'],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=_formula, h=60, size=26),
        dict(type='string', var='res_str', label='res_str（答案字符串）', cell=80, h=130),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('xpos', 'xpos'), ('ypos', 'ypos'), ('tmp', 'tmp', 'yellow'),
           ('zero_flag', 'zero_flag')],
    captions={
        "if num1 == '0'": "特判乘数为 `'0'`：否则结果全是 0，后面去前导零会把它们==全删光，得到空串==",
        'res = [0] * (m + n)': '`m` 位 × `n` 位最多 `m + n = {m + n}` 位 → `res` 开 `{m + n}` 格，==低位在前==',
        'xpos = 0': '`xpos`：当前 num1 的这一位是从右数第几位（10 的几次方）',
        'for i in range': _for_i,
        'for j in range': _for_j,
        'tmp = res[xpos + ypos] + x * y': '`tmp = res[{xpos + ypos}] + {x}×{y} = {B.res[xpos + ypos]} + {x * y}` = =={tmp}==',
        'res[xpos + ypos] = tmp % 10': '本位只留个位：`res[{xpos + ypos}] = {tmp} % 10 = {res[xpos + ypos]}`',
        'res[xpos + ypos + 1] += tmp // 10': lambda S, B, r: (
            f'十位进到高一位：`res[{S.xpos + S.ypos + 1}] += {S.tmp} // 10` → =={S.res[S.xpos + S.ypos + 1]}=='
            if S.tmp >= 10 else f'`{S.tmp} < 10`，没有进位：`res[{S.xpos + S.ypos + 1}] += 0`'),
        'tmp = 0': '再从低位到高位统一进位一遍（保险起见；本例每位都已 `< 10`，这一趟略过）',
        'zero_flag = True': '`zero_flag = True`：从最高位往下读，开头的 0 都是前导零',
        "res_str = ''": '`res_str` 收集答案',
        'for index in range(xpos + ypos - 1': lambda S, B, r: (
            '所有位读完' if B.get('index') == 0 else f'从高位往低位：读 `res[{S.index}]`（10^{S.index} 位）'),
        'if res[index] == 0 and zero_flag': _if_zero,
        'continue': '跳过这个前导零',
        'res_str += str(res[index])': '`zero_flag` 置为 False，拼上 `{res[index]}` → `res_str = "{res_str}"`',
        'return res_str': '`12 × 34 = {ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='像竖式一样一位一位乘：第 i 位 × 第 j 位 落在第 i+j 位',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['给两个用字符串表示的非负整数 `num1`、`num2`，返回它们的==乘积==（也是字符串）',
                 '==不能==用大整数库，也不能直接把输入转成整数',
                 '示例：`"2" × "3"` → `"6"`；`"123" × "456"` → `"56088"`',
                 '本视频：`"12" × "34"` → `"408"`'],
        quote='经典的高精度乘法问题，==朴素的做法是一位一位乘，然后再加起来==，平方的复杂度。',
        quote_src='—— yiduobo 题解',
        idea=['`res[k]` 存答案的 10^k 位：num1 第 `xpos` 位 × num2 第 `ypos` 位 → 加到 `res[xpos+ypos]`',
              '加完只留个位，十位进到 `res[xpos+ypos+1]`',
              '最后从高位往低位读，用 `zero_flag` 跳过==前导零=='],
        after=[dict(heading='进阶：FFT', lines=[
            '原文还提到：把 n 位数看成 `x = 10` 时的 n−1 次多项式',
            '多项式 → 点值表示 → 点值相乘 → 转回多项式',
            '取复数单位根时转换只要 `O(n log n)`（FFT）',
            '原文：==由于具体实现非常复杂，这里最后还是选择了朴素的做法=='])],
        summary=['时间 `O(mn)`：两重循环逐位相乘；`res` 长度 `m + n` 一定够用',
                 '易错：乘积为 0 要特判，否则去前导零后得到空串',
                 '易错：只跳过==开头==的 0，中间的 0（如 4==0==8）要保留',
                 '原文为 Python 2 写法：`tmp / 10` 和 `res[index] / 10` 已改为 `//` 整除，并删去 docstring'],
    ),
)
