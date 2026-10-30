S0 = '11106'
N = len(S0)


def _f_all(s):
    f = [1] + [0] * len(s)
    for i in range(1, len(s) + 1):
        if s[i - 1] != '0':
            f[i] += f[i - 1]
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            f[i] += f[i - 2]
    return f


F = _f_all(S0)   # F[i]：前 i 位的解码方式数（只用来画「已经算过的历史格子」）


def _ended(S, B):
    return S['_line'] == 16 and 'index' in B and B['index'] == S.get('index')


def _pos(S, B):
    """变量 a/b/c 此刻代表 f 的哪一格（f[i] = 前 i 位的解码数）"""
    ln = S['_line']
    out = {}
    if 'index' not in S:
        if 'a' in S:
            out['a'] = 1
        if 'b' in S:
            out['b'] = 2
        if 'c' in S:
            out['c'] = 3
        return out
    if _ended(S, B) or ln == 25:
        return {'a': N - 1, 'b': N}
    k = S['index']
    if ln in (16, 17, 18, 19, 20):
        return {'a': k - 1, 'b': k, 'c': k + 1}
    if ln == 21:
        return {'a': k, 'b': k, 'c': k + 1}
    if ln == 22:
        return {'a': k, 'b': k + 1, 'c': k + 1}
    return {'a': k, 'b': k + 1, 'c': k + 2} if k + 2 <= N else {'a': k, 'b': k + 1}


def _windows(S):
    """(单个数字的下标集合, 两位数的下标集合)"""
    ln = S['_line']
    if ln in (4, 5):
        return {0}, set()
    if ln in (10, 11):
        return {1}, set()
    if ln in (12, 13):
        return set(), {0, 1}
    if ln in (17, 18) and 'index' in S:
        return {S['index']}, set()
    if ln in (19, 20) and 'index' in S:
        return set(), {S['index'] - 1, S['index']}
    return set(), set()


COL = {'a': 'blue', 'b': 'purple', 'c': 'green'}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pos = _pos(S, B)
    one, two = _windows(S)
    cell = min(120, (x1 - x0 - 160) / N)
    sx = x0 + 130
    ys, yf = y0 + 90, y0 + 330
    ch = cell * 0.78
    cv.text((x0 + 18, y0 + 4), 's（蓝 = 单独解码的一位，粉 = 两位一起解码）', 22, T['muted'], bold=True)
    cv.text((sx - 16, ys + ch / 2), 's', 28, T['muted'], anchor='rm', bold=True, mono=True)
    if two:
        a, b = min(two), max(two)
        v = int(S0[a:b + 1])
        ok = 10 <= v <= 26
        cv.rect((sx + a * cell - 2, ys - 8, sx + (b + 1) * cell + 2, ys + ch + 8), outline=T['pink'], width=4, r=14)
        cv.text((sx + (a + b + 1) * cell / 2, ys - 14), f'"{S0[a:b + 1]}" = {v} {"在" if ok else "不在"} 10~26 之间', 22,
                T['pink'] if ok else T['dim'], anchor='mb', bold=True)
    for i, ch_ in enumerate(S0):
        X = sx + i * cell
        if i in one:
            ok = ch_ != '0'
            fill = T['blue'] if ok else (90, 52, 52)
        elif i in two:
            fill = (90, 50, 80)
        else:
            fill = T['panel2']
        cv.rect((X + 6, ys, X + cell - 6, ys + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), ch_, 40, T['bg'] if fill == T['blue'] else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 8), i, 18, T['dim'], anchor='mt', mono=True)
        if i in one:
            cv.text((X + cell / 2, ys - 14), f"'{ch_}' {'可单独解码' if ch_ != '0' else '不能单独解码'}", 20,
                    T['blue'] if ch_ != '0' else T['red'], anchor='mb', bold=True)
    # f 行：f[i] 放在 s[i-1] 正下方（前 i 位）
    cv.text((sx - 16, yf + ch / 2), 'f', 28, T['muted'], anchor='rm', bold=True, mono=True)
    hi = max([p for n, p in pos.items() if n != 'c'] + [0])
    for i in range(1, N + 1):
        X = sx + (i - 1) * cell
        names = sorted(n for n, p in pos.items() if p == i)
        if names:
            nm = names[0]
            val = S[nm]
            fill = T[COL[nm]]
        elif i <= hi:
            val, fill = F[i], (52, 60, 72)
        else:
            val, fill = '?', T['panel2']
        cv.rect((X + 6, yf, X + cell - 6, yf + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, yf + ch / 2), val, 36, T['bg'] if names else (T['muted'] if val != '?' else T['dim']),
                anchor='mm', bold=True)
        cv.text((X + 12, yf + 4), f'f[{i}]', 15, T['bg'] if names else T['dim'], mono=True)
        for r, nm in enumerate(names):
            cv.text((X + cell / 2, yf + ch + 8 + r * 28), nm, 26, T[COL[nm]], anchor='mt', bold=True, mono=True)
    ln = S['_line']
    if 'index' in S and 'c' in pos and ln in (18, 20):
        src = 'b' if ln == 18 else 'a'
        p0 = (sx + (pos[src] - 1) * cell + cell / 2, yf - 6)
        p1 = (sx + (pos['c'] - 1) * cell + cell / 2 - 4, yf - 6)
        mid = cv.arc_arrow(p0, p1, 30 + 20 * (pos['c'] - pos[src]), T['blue'] if src == 'b' else T['pink'], 4, 13)
        cv.text((mid[0], mid[1] - 6), f'c += {src}', 22, T['blue'] if src == 'b' else T['pink'], anchor='mb', bold=True)
    cv.text((x0 + 18, y1 - 40), 'f[i] = 前 i 位的解码方式数；只依赖 f[i-1]、f[i-2] → 用 a、b、c 三个变量滚动', 21, T['muted'])


def _cap_one(S, B, ret):
    k = S.index
    if S.s[k] != '0':
        return f"`s[{k}] = '{S.s[k]}'` 在 1~9：单独解码 → `c += b`（加上前 {k} 位的方案数）"
    return f"`s[{k}] = '0'`：0 不能单独解码"


def _cap_two(S, B, ret):
    k = S.index
    v = int(S.s[k - 1:k + 1])
    if 10 <= v <= 26:
        return f'`s[{k - 1}:{k + 1}] = "{S.s[k - 1:k + 1]}"` = {v} 在 10~26：两位一起解码 → `c += a`（加上前 {k - 1} 位的方案数）'
    return f'`"{S.s[k - 1:k + 1]}"` = {v} 不在 10~26：不能两位一起解码'


def _cap_for(S, B, ret):
    if 'index' in B and B.index == S.index:
        return f'扫描结束：`b` 就是前 {N} 位的方案数'
    return f'算前 `{S.index + 1}` 位：`c` 从 0 开始累加（`a` = 前 {S.index - 1} 位，`b` = 前 {S.index} 位）'


CONFIG = dict(
    num=91, title='解码方法', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP · 三变量滚动',
    tags=['热题173'],
    code='''
class Solution(object):
    def numDecodings(self, s):
        a = 0
        if int(s[0]) >= 1 and int(s[0]) <= 9:
            a = 1
        if len(s) == 1:
            return a

        b = 0
        if int(s[1]) >= 1 and int(s[1]) <= 9:
            b = a
        if int(s[0:2]) >= 10 and int(s[0:2]) <= 26:
            b += 1

        c = 0
        for index in range(2, len(s)):
            if int(s[index]) >= 1 and int(s[index]) <= 9:
                c += b
            if int(s[index - 1 : index + 1]) >= 10 and int(s[index - 1 : index + 1]) <= 26:
                c += a
            a = b
            b = c
            c = 0

        return b
''',
    call=f'Solution().numDecodings("{S0}")',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('index', 'index', 'yellow'), ('a', 'a', 'blue'), ('b', 'b', 'purple'), ('c', 'c', 'green')],
    captions={
        'a = 0': '`a` 先当作 `f[1]`（前 1 位的解码数），初始为 0',
        'if int(s[0])': "边界 `i = 1`：`s[0] = '{s[0]}'` 能否单独解码？",
        'a = 1': '能 → `f[1] = 1`',
        'if len(s) == 1': '长度 `{len(s)}` > 1，继续',
        'b = 0': '`b` 当作 `f[2]`（前 2 位）',
        'if int(s[1])': "边界 `i = 2`：`s[1] = '{s[1]}'` 能单独解码吗？",
        'b = a': '能 → `f[2] += f[1]`，`b = {b}`',
        'if int(s[0:2])': '`"{s[0:2]}"` = {int(s[0:2])} 在 10~26 吗？',
        'b += 1': '在 → 前两位合起来也是一种：`f[2] += 1`（相当于 `f[0] = 1`），`b = {b}`',
        15: '`c` 用来累加新的 `f[i]`',
        'for index in range': _cap_for,
        'if int(s[index]) >= 1': _cap_one,
        'c += b': '`c = {B.c} + b = {B.c} + {b} = {c}`',
        'if int(s[index - 1 : index + 1])': _cap_two,
        'c += a': '`c = {B.c} + a = {B.c} + {a} = {c}`',
        'a = b': '==倒一倒==：`a ← b = {a}`',
        'b = c': '`b ← c = {b}`（新算出的前 {index + 1} 位方案数）',
        23: '`c` 清零，准备下一位',
        'return b': '`b` = 前 {len(s)} 位的解码方式数 = =={ret}==',
    },
    cards=dict(
        one_liner='f[i] = 前 i 位的解码方式数：最后一位单独解码，或最后两位一起解码',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`A→1, B→2, …, Z→26`，给一串数字 `s`，问有多少种解码方式',
                 '`"06"` 不能解成 `F`：==以 0 开头的两位数不合法==，单独的 `0` 也不行',
                 '示例：`"226"` → `3`；本视频：`"11106"` → `2`（`AAJF`、`KJF`）'],
        quote='f[i]表示前i位一共有多少种解码方式……如果s[i - 1]在0到9之间，那么可以将s[i - 1]单独解码，此时 `f[i] += f[i - 1]`。如果s[i - 2]与s[i - 1]组合起来在10到26之间……此时 `f[i] += f[i - 2]`。',
        quote_src='—— yiduobo 题解原文（原文写“0到9”，代码里是 1~9）',
        idea=['看最后一步怎么解码：最后一位单独解码 → 接在前 `i-1` 位后面',
              '最后两位合起来在 10~26 → 接在前 `i-2` 位后面；两种情况相加',
              '只依赖前两项 → 不开数组，`a, b, c` 三个变量「倒一倒」；`i = 1, 2` 单独处理'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`0` 不能单独解码，`"06"` 这种两位数也不行，所以判断区间是 `1~9` 和 `10~26`',
                 '易错：边界 `i = 1、2` 要单独算（原文特别提醒），`b += 1` 相当于 `f[0] = 1`',
                 '原文：转移不确定（取决于字符），所以不能像斐波那契那样用矩阵快速幂加速',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
