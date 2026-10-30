X0, N0 = 2.0, 13
NB = N0.bit_length()


def _k(S):
    """已经处理完的低位个数（= 当前正在看的比特位下标）"""
    n = S.get('n')
    if not isinstance(n, int):
        return 0
    return NB - n.bit_length()


def _included(S, j):
    """第 j 位（为 1）对应的 x^(2^j) 是否已经乘进 ans"""
    if not (N0 >> j & 1) or 'ans' not in S:
        return False
    k = _k(S)
    if j < k:
        return True
    if j == k:
        return S['ans'] == X0 ** (N0 & ((2 << k) - 1))
    return False


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'n = {N0} 的二进制：从低位（右）往高位（左）逐位枚举', 24, T['muted'], bold=True)
    k = _k(S)
    colw = min(220, (x1 - x0 - 80) / NB)
    sx = x0 + 40 + ((x1 - x0 - 80) - colw * NB) / 2
    ytop = y0 + 60
    for c in range(NB):
        j = NB - 1 - c                       # 左边是高位
        X = sx + c * colw
        cx = X + colw / 2
        bit = N0 >> j & 1
        cur = j == k and S.get('n', 0) > 0
        done = j < k
        cv.text((cx, ytop), f'第 {j} 位', 22, T['yellow'] if cur else T['muted'], anchor='mt', bold=cur)
        fill = T['panel2']
        if _included(S, j):
            fill = T['green']
        elif done:
            fill = (40, 45, 53)
        cv.rect((cx - 46, ytop + 34, cx + 46, ytop + 120), fill=fill, r=12,
                outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
        cv.text((cx, ytop + 77), bit, 46, T['bg'] if _included(S, j) else (T['dim'] if done else T['text']),
                anchor='mm', bold=True)
        # 权重 x^(2^j)
        w = X0 ** (1 << j)
        wy = ytop + 150
        cv.rect((X + 10, wy, X + colw - 10, wy + 86), fill=T['panel'], r=10,
                outline=T['green'] if _included(S, j) else T['border'], width=3 if _included(S, j) else 1)
        cv.text((cx, wy + 24), f'x^{1 << j}', 26, T['cyan'], anchor='mm', mono=True)
        cv.text((cx, wy + 62), f'{w:g}', 28, T['text'], anchor='mm', bold=True)
        if isinstance(S.get('x'), float) and S['x'] == w:
            cv.tri_up(cx, wy + 100, 11, T['blue'])
            cv.text((cx, wy + 124), '当前 x', 22, T['blue'], anchor='mt', bold=True)
    # 进度箭头：低位在右
    ay = ytop + 300
    cv.arrow((sx + colw * NB - 10, ay), (sx + 10, ay), T['dim'], 3, 14)
    cv.text((sx + colw * NB / 2, ay + 12), '枚举方向：n >>= 1 每次扔掉最低位', 20, T['dim'], anchor='mt')
    # ans 的组成
    parts = [j for j in range(NB) if _included(S, j)]
    fy = ay + 60
    if 'ans' in S:
        if len(parts) == 1:
            cv.rich(x0 + 40, fy, f'ans = =={S["ans"]:g}==', x1 - x0 - 80, size=30)
        elif parts:
            terms = ' × '.join(f'{X0 ** (1 << j):g}' for j in parts)
            cv.rich(x0 + 40, fy, f'ans = {terms} = =={S["ans"]:g}==', x1 - x0 - 80, size=30)
        else:
            cv.rich(x0 + 40, fy, 'ans = `1`（还没有乘进任何一项）', x1 - x0 - 80, size=30)
    ones = [j for j in range(NB - 1, -1, -1) if N0 >> j & 1]
    goal = ' × '.join(f'x^{1 << j}' for j in ones)
    cv.rich(x0 + 40, fy + 56, f'目标：`{N0} = ' + ' + '.join(str(1 << j) for j in ones) + f'`，所以 `x^{N0} = {goal}`',
            x1 - x0 - 80, size=26, color=T['muted'])


def _while(S, B, ret):
    n = B.n
    if n:
        return f'`n = {n}`（二进制 `{n:b}`）≠ 0 → 还有比特位没枚举，看它的最低位'
    return '`n = 0`：所有比特位都枚举完了 → 退出循环'


def _bit(S, B, ret):
    n = B.n
    if n & 1:
        return f'`{n:b}` 的最低位是 ==1== → 当前的 `x = {B.x:g}` 要乘到 `ans` 中'
    return f'`{n:b}` 的最低位是 ==0== → 这一项不要，不乘'


CONFIG = dict(
    num=50, title='Pow(x, n)', difficulty='Medium', category='数学',
    author='灵茶山艾府', technique='快速幂 · 迭代枚举比特位',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def myPow(self, x: float, n: int) -> float:
        ans = 1
        if n < 0:  # x^-n = (1/x)^n
            n = -n
            x = 1 / x
        while n:  # 从低到高枚举 n 的每个比特位
            if n & 1:  # 这个比特位是 1
                ans *= x  # 把 x 乘到 ans 中
            x *= x  # x 自身平方
            n >>= 1  # 继续枚举下一个比特位
        return ans
''',
    call=f'Solution().myPow({X0}, {N0})',
    expect=8192.0,
    views=[
        dict(type='text', fn=lambda S: (f"`n = {S['n']}` = 二进制 `{S['n']:b}`，最低位 `n & 1 = {S['n'] & 1}`"
                                         if S.get('n') else '`n = 0`：比特位全部处理完'), h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('n', 'n'), ('n（二进制）', lambda S: int(f"{S['n']:b}")), ('x', 'x', 'blue'),
           ('ans', 'ans', 'green')],
    captions={
        'ans = 1': '`ans = 1`：乘法的起点，之后把需要的 `x^(2^k)` 逐个乘进来',
        'if n < 0': '`n = {n}` 不是负数，不用转换（负数时利用 `x^-n = (1/x)^n` 转成正数）',
        'while n:': _while,
        'if n & 1': _bit,
        'ans *= x': '`ans = {B.ans:g} × {B.x:g}` = =={ans:g}==',
        'x *= x': lambda S, B, ret: (f'`x` 自身平方：`{B.x:g}² = {S.x:g}`，正好是==下一个比特位的权重=='
                                     if B.n > 1 else f'`x` 自身平方：`{B.x:g}² = {S.x:g}`（已经没有更高的比特位，这次用不上）'),
        'n >>= 1': '`n` 右移一位：`{B.n:b}` → `{n:b}`，扔掉刚处理完的最低位',
        'return ans': '返回 `ans = {ret:g}`，即 `2^13`',
    },
    cards=dict(
        one_liner='把 n 拆成二进制：哪一位是 1，就乘上对应的 x^(2^k)',
        complexity='时间 `O(log|n|)`，空间 `O(1)`',
        problem=['实现 `pow(x, n)`：计算 `x` 的整数 `n` 次幂 `x^n`',
                 '`n` 可以是负数：`x = 2.0, n = -2` → `0.25`',
                 '示例：`x = 2.0, n = 10` → `1024.0`',
                 '本视频：`x = 2.0, n = 13` → `8192.0`'],
        quote='`while n`：从低到高枚举 n 的每个比特位；这个比特位是 1 → ==把 x 乘到 ans 中==；x 自身平方；继续枚举下一个比特位。',
        quote_src='—— 灵茶山艾府题解（方法一：迭代，代码注释）',
        idea=['`13` 的二进制是 `1101`，即 `13 = 8 + 4 + 1`',
              '所以 `x^13 = x^8 × x^4 × x^1`，只需要 `x^1, x^2, x^4, x^8` 这些项',
              '`x` 每轮平方一次，恰好依次得到这些项；比特位为 1 就乘进答案',
              '`n < 0` 时先转换：`x^-n = (1/x)^n`'],
        result='`ans = 2 × 16 × 256 = 8192.0` ✓ 只循环了 4 次（13 的二进制位数）',
        summary=['时间 `O(log|n|)`：循环次数 = `n` 的二进制位数；空间 `O(1)`',
                 '顺序：==先判断最低位、再平方 x、再右移 n==',
                 '易错：其他语言里 `n = -2^31` 取反会溢出 32 位，要先转成 64 位整数',
                 '方法二递归：`x^n = (x^(n/2))^2`，n 为奇数再乘 `x`，空间 `O(log|n|)`'],
    ),
)
