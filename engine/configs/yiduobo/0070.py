_B = [[0, 1], [1, 1]]


def _mul(x, y):
    return [[sum(x[i][k] * y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


_POW = {1: _B}
for _k in range(2, 12):
    _POW[_k] = _mul(_POW[_k - 1], _B)


def _which_pow(m):
    for k, p in _POW.items():
        if m == p:
            return f'b^{k}'
    return None


def _sup(k):
    return f'^{k}'


def _changed_cell(S, B, name):
    m, bm = S.get(name), B.get(name)
    if not (isinstance(m, list) and isinstance(bm, list)):
        return None
    for r in range(2):
        for c in range(2):
            try:
                if m[r][c] != bm[r][c]:
                    return r, c
            except Exception:
                return None
    return None


def _draw_mat(cv, T, x, y, cell, name, m, bm, row_hl=None, col_hl=None, title=None):
    cv.text((x + cell, y), title or name, 24, T['muted'], anchor='mb', bold=True)
    if m is None:
        cv.text((x + cell, y + cell), '（未创建）', 22, T['dim'], anchor='mm')
        return
    for r in range(2):
        for c in range(2):
            X, Y = x + c * cell, y + 10 + r * cell
            fill = T['panel2']
            if row_hl is not None and r == row_hl:
                fill = T['blue']
            if col_hl is not None and c == col_hl:
                fill = T['pink'] if fill == T['panel2'] else T['purple']
            changed = False
            try:
                changed = bm is not None and bm[r][c] != m[r][c]
            except Exception:
                changed = True
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=8,
                    outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
            cv.text((X + cell / 2, Y + cell / 2), m[r][c], 30, T['bg'] if fill != T['panel2'] else T['text'],
                    anchor='mm', bold=True)
    tag = _which_pow(m)
    cv.text((x + cell, y + 10 + 2 * cell + 8), f'= {tag}' if tag else '计算中…', 22,
            T['green'] if tag else T['dim'], anchor='mt', bold=True)


def _mats(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cell = 76
    y = y0 + 40
    if 'base_b' in S:
        names = [('base_b', 'base_b'), ('tmp', 'tmp'), ('res', 'res')]
        rc_res = _changed_cell(S, B, 'res')
        rc_tmp = _changed_cell(S, B, 'tmp') if 'res' in S else None
        hl = {}
        if rc_res and 'res' in B:
            hl['tmp'] = rc_res  # res[r][c] = tmp 第 r 行 · tmp 第 c 列
        if rc_tmp:
            hl['res_row'] = rc_tmp[0]
            hl['base_col'] = rc_tmp[1]
    else:
        names = [('b', 'b'), ('final_b', 'final_b')]
        hl = {}
    gap = (x1 - x0 - 40) / len(names)
    for k, (var, title) in enumerate(names):
        x = x0 + 20 + k * gap + (gap - 2 * cell) / 2
        row_hl = col_hl = None
        if var == 'tmp' and 'tmp' in hl:
            row_hl, col_hl = hl['tmp']
        if var == 'res' and 'res_row' in hl:
            row_hl = hl['res_row']
        if var == 'base_b' and 'base_col' in hl:
            col_hl = hl['base_col']
        _draw_mat(cv, T, x, y, cell, var, S.get(var), B.get(var), row_hl, col_hl, title)
    if hl:
        y2 = y + 10 + 2 * cell + 80
        x = x0 + 30
        for c, t in [('blue', '蓝 = 取这一行'), ('pink', '粉 = 取这一列'), ('purple', '紫 = 行列交叉')]:
            cv.rect((x, y2 - 11, x + 22, y2 + 11), fill=T[c], r=5)
            cv.text((x + 32, y2), t, 22, T['muted'], anchor='lm')
            x += 32 + cv.tlen(t, 22) + 36
    if 'base_b' not in S and 'a' in S:
        cv.text((x0 + 30, y1 - 44), f"a = [f(1), f(2)] = {S['a']}", 26, T['cyan'], anchor='lm', bold=True, mono=True)


def _goal(S):
    if 'base_b' in S:
        n = S['n']
        if n == 1:
            return '`fast_pow(b, 1)`：==递归到底==，`b¹` 就是 b 本身'
        s = f"`fast_pow(b, {n})`：求 `b{_sup(n)}` = `b{_sup(n // 2)}` × `b{_sup(n // 2)}`"
        return s + (' × `b`（==n 是奇数==）' if n % 2 else '（n 是偶数）')
    if 'final_b' in S:
        return f"`[f(1), f(2)] × b{_sup(S['n'] - 2)}` = `[f({S['n'] - 1}), f({S['n']})]`，取第 2 项"
    return '`[f(k-1), f(k)] × b` = `[f(k), f(k+1)]`：==每乘一次 b，往前走一阶=='


def _cap_res(r, c):
    def cap(S, B, ret):
        t = S.tmp
        val = S.res[r][c]
        return (f'`res[{r}][{c}]` = tmp 第 {r} 行 · tmp 第 {c} 列 = '
                f'`{t[r][0]}×{t[0][c]} + {t[r][1]}×{t[1][c]}` = =={val}==')
    return cap


def _cap_tmp(r, c):
    def cap(S, B, ret):
        m, b = S.res, S.base_b
        val = S.tmp[r][c]
        return (f'复用 tmp 存 `res × b`：res 第 {r} 行 · b 第 {c} 列 = '
                f'`{m[r][0]}×{b[0][c]} + {m[r][1]}×{b[1][c]}` = =={val}==')
    return cap


CONFIG = dict(
    num=70, title='爬楼梯', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='斐波那契 + 矩阵快速幂',
    code='''
class Solution(object):
    def climbStairs(self, n):
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            b = [[0, 1], [1, 1]]
            final_b = self.fast_pow(b, n - 2)
            a = [1, 2]
            return a[0] * final_b[0][1] + a[1] * final_b[1][1]

    def fast_pow(self, base_b, n):
        if n == 1:
            return [base_b[0][:], base_b[1][:]]

        tmp = self.fast_pow(base_b, n // 2)

        res = [[0, 0], [0, 0]]

        res[0][0] = tmp[0][0] * tmp[0][0] + tmp[0][1] * tmp[1][0]
        res[0][1] = tmp[0][0] * tmp[0][1] + tmp[0][1] * tmp[1][1]
        res[1][0] = tmp[1][0] * tmp[0][0] + tmp[1][1] * tmp[1][0]
        res[1][1] = tmp[1][0] * tmp[0][1] + tmp[1][1] * tmp[1][1]

        if n % 2 == 0:
            return res

        tmp[0][0] = res[0][0] * base_b[0][0] + res[0][1] * base_b[1][0]
        tmp[0][1] = res[0][0] * base_b[0][1] + res[0][1] * base_b[1][1]
        tmp[1][0] = res[1][0] * base_b[0][0] + res[1][1] * base_b[1][0]
        tmp[1][1] = res[1][0] * base_b[0][1] + res[1][1] * base_b[1][1]
        return tmp
''',
    call='Solution().climbStairs(7)',
    expect=21,
    views=[
        dict(type='text', fn=_goal, h=60),
        dict(type='custom', draw=_mats, h=330),
        dict(type='calls', h=200),
    ],
    watch=[('n', 'n', 'orange'), ('n // 2', lambda S: S['n'] // 2 if 'base_b' in S else None, 'cyan')],
    skip=['elif n == 2'],
    captions={
        3: '`n = {n}`：不是边界 `f[1] = 1`、`f[2] = 2`，走矩阵快速幂',
        'b = [[0, 1], [1, 1]]': '乘数矩阵 `b`：由 `[f(k-1), f(k)] × b = [f(k), f(k+1)]` ==逐项比对解出来==',
        'final_b = self': '从 `[f(1), f(2)]` 走到 `f({B.n})` 要乘 `n-2 = {B.n-2}` 次 b → ==结合律==：先算 `b^{B.n-2}`',
        14: lambda S, B, ret: ('`n = 1`：递归到底' if S.n == 1 else f'`n = {S.n}` 不是 1，继续折半'),
        'return [base_b': '返回 b 的==拷贝==（`[:]`）：后面会原地改写 tmp，不拷贝会把 b 改坏',
        'tmp = self.fast_pow': '先递归求 `b^{B.n // 2}`（`{B.n} // 2 = {B.n // 2}`；原文 `n / 2` 是 Python 2 整除）',
        'res = [[0, 0]': '递归返回：`tmp = b^{n // 2}`；新开 `res` 存 `tmp × tmp`',
        'res[0][0] =': _cap_res(0, 0),
        'res[0][1] =': _cap_res(0, 1),
        'res[1][0] =': _cap_res(1, 0),
        'res[1][1] =': _cap_res(1, 1),
        'if n % 2 == 0': lambda S, B, ret: (f'`n = {S.n}` 是偶数：`b^{S.n} = (b^{S.n // 2})²` 就是 res' if S.n % 2 == 0
                                            else f'`n = {S.n}` 是奇数：`(b^{S.n // 2})²` 只到 `b^{S.n - 1}`，==还差一个 b=='),
        'return res': '返回 `res = b^{n}`',
        'tmp[0][0] =': _cap_tmp(0, 0),
        'tmp[0][1] =': _cap_tmp(0, 1),
        'tmp[1][0] =': _cap_tmp(1, 0),
        'tmp[1][1] =': _cap_tmp(1, 1),
        'return tmp': '返回 `tmp = b^{n}`',
        'a = [1, 2]': '递归全部返回：`final_b = b^{n-2}`；起始矩阵 `a = [f(1), f(2)] = [1, 2]`',
        'return a[0]': '`a × final_b` 的第 2 项 = `1×{final_b[0][1]} + 2×{final_b[1][1]}` = =={ret}== = `f({n})`',
    },
    cards=dict(
        one_liner='发现是斐波那契数列，构造 2×2 矩阵，用快速幂把 O(n) 压到 O(log n)',
        complexity='时间 `O(log n)`，空间 `O(log n)`（递归栈）',
        problem=['每次可以爬 `1` 或 `2` 个台阶，爬到第 `n` 阶有多少种不同方法？',
                 '示例：`n = 3` → `3`（1+1+1、1+2、2+1）',
                 '演示：`n = 7` → `21`'],
        before=[dict(heading='yiduobo 的推导：构造乘数矩阵 b', chapter='② 思路', lines=[
            '`f[i]` = 走到第 i 阶的走法：`f[i] = f[i-1] + f[i-2]`，`f[1]=1`，`f[2]=2`',
            '==这就是斐波那契数列== → 可以用矩阵快速幂',
            '设 `a = [f[k-1], f[k]]`（1×2），目标 `c = [f[k], f[k+1]]`（1×2）',
            '1×2 乘出 1×2 → b 必是 2×2；按乘法定义逐项比对，解得 `b = [[0,1],[1,1]]`',
        ])],
        quote='可以发现这个过程中一共执行了n - 2次矩阵乘法，而==矩阵乘法是满足结合律的==，于是也可以变成a * (b^3)来计算。',
        quote_src='—— yiduobo 题解（n = 5 的例子）',
        idea=['`[1,2]·b = [2,3]`，再 `·b = [3,5]`，再 `·b = [5,8]`：每乘一次 b 走一阶',
              '结合律：先算 `b^(n-2)`，最后和 `a = [1, 2]` 乘一次',
              '`b^n` 照搬第 50 题快速幂：`b^n = (b^(n//2))²`，==n 为奇数再乘一个 b=='],
        summary=['时间 `O(m³ log n)`，m = 2 → `O(log n)`；递归栈 `O(log n)`',
                 '原文为 Python 2 写法：`n / 2` 已改为 `n // 2`，并删去 docstring',
                 '`n == 1` 返回 ==b 的拷贝==：奇数层会原地改写 `tmp`',
                 'n ≤ 2 要特判；奇数次幂别忘了再乘一次 b',
                 '作者原话：n 不大时这样做性能并不突出，但矩阵快速幂常用于优化 DP'],
    ),
)
