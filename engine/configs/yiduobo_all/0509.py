def _mat(cv, T, x, y, cs, name, M, hi_cells=(), hi_row=None, hi_col=None, color=None):
    cv.text((x + cs, y - 6), name, 20, T['muted'], anchor='mb', bold=True)
    for i in range(2):
        for j in range(2):
            X, Y = x + j * cs, y + i * cs
            on = (i, j) in hi_cells
            line = (hi_row == i) or (hi_col == j)
            fill = T['yellow'] if on else (T[color] if color and M is not None else T['panel2'])
            cv.rect((X + 3, Y + 3, X + cs - 3, Y + cs - 3), fill=fill, r=8,
                    outline=T['blue'] if line else T['border'], width=4 if line else 1)
            if M is not None:
                cv.text((X + cs / 2, Y + cs / 2), M[i][j], 30, T['bg'] if (on or color) else T['text'], anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S.get('_inner', {})
    if 'base' not in inner:
        cv.text((x0 + 20, y0 + 10), '`X = [[0,1],[1,1]]`：`[f(k-2), f(k-1)] × X = [f(k-1), f(k)]`', 24, T['muted'])
        return
    line = S.get('_line')
    i, j, k = inner.get('i'), inner.get('j'), inner.get('k')
    tmp, ret, new_ret, base = inner.get('tmp'), inner.get('ret'), inner.get('new_ret'), inner['base']
    cs = 78
    gap = (x1 - x0 - 40 - 4 * 2 * cs) / 3
    xs = [x0 + 20 + t * (2 * cs + gap) for t in range(4)]
    y = y0 + 50
    in_sq = line == 22  # ret[i][j] += tmp[i][k] * tmp[k][j]
    in_odd = line == 29  # new_ret[i][j] += ret[i][k] * base[k][j]
    _mat(cv, T, xs[0], y, cs, 'base = X', base, hi_col=j if in_odd else None, color='purple')
    _mat(cv, T, xs[1], y, cs, f'tmp = X^{inner["n"] // 2}', tmp,
         hi_row=i if in_sq else None, hi_col=j if in_sq else None, color='cyan' if tmp is not None else None)
    _mat(cv, T, xs[2], y, cs, 'ret = tmp × tmp', ret,
         hi_cells=[(i, j)] if in_sq else [], hi_row=i if in_odd else None)
    _mat(cv, T, xs[3], y, cs, 'new_ret = ret × base', new_ret, hi_cells=[(i, j)] if in_odd else [])
    if in_sq and k is not None:
        txt = f'ret[{i}][{j}] += tmp[{i}][{k}] × tmp[{k}][{j}] = {tmp[i][k]} × {tmp[k][j]}'
    elif in_odd and k is not None:
        txt = f'new_ret[{i}][{j}] += ret[{i}][{k}] × base[{k}][{j}] = {ret[i][k]} × {base[k][j]}'
    else:
        txt = f'当前这一层：n = {inner["n"]}，X^n = (X^(n//2))² ' + ('× X（n 是奇数）' if inner['n'] % 2 else '（n 是偶数）')
    cv.text((x0 + 20, y + 2 * cs + 30), txt, 24, T['text'], mono=True)


def _sq(S, B, ret):
    i, j, k = S.i, S.j, S.k
    t = S.tmp
    if k == 0:
        return f'`ret[{i}][{j}]` = 第 {i} 行 · 第 {j} 列：先加 `{t[i][0]} × {t[0][j]}`'
    return f'再加 `{t[i][1]} × {t[1][j]}` → `ret[{i}][{j}]` = =={S.ret[i][j]}=='


def _od(S, B, ret):
    i, j, k = S.i, S.j, S.k
    r, b = S.ret, S.base
    if k == 0:
        return f'`new_ret[{i}][{j}]`：先加 `{r[i][0]} × {b[0][j]}`'
    return f'再加 `{r[i][1]} × {b[1][j]}` → `new_ret[{i}][{j}]` = =={S.new_ret[i][j]}=='


CONFIG = dict(
    num=509, title='斐波那契数', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='矩阵乘法 + 递归快速幂',
    tags=['labuladong', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def fib(self, N):
        if N == 0:
            return 0
        if N == 1:
            return 1

        k = N - 1
        tmp_X = self.quick_pow([[0, 1], [1, 1]], k)

        return tmp_X[1][1]

    def quick_pow(self, base, n):
        if n == 1:
            return base

        tmp = self.quick_pow(base, n // 2)
        ret = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    ret[i][j] += tmp[i][k] * tmp[k][j]

        if n % 2 == 1:
            new_ret = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        new_ret[i][j] += ret[i][k] * base[k][j]
            return new_ret

        return ret
''',
    call='Solution().fib(6)',
    expect=8,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=200, hide=('base',)),
    ],
    watch=[('n', lambda S: S['_inner'].get('n'), 'blue'), ('k', 'k'), ('tmp_X', 'tmp_X', 'green')],
    skip=['for i in range(2)', 'for j in range(2)', 'for k in range(2)'],
    captions={
        'if N == 0': '`N = {N}`，不是 0',
        'if N == 1': '也不是 1 → 用矩阵快速幂',
        'k = N - 1': '从 `A[1] = [f(0), f(1)]` 出发，要乘 `k = N - 1 = {k}` 次 `X`',
        'tmp_X = self.quick_pow': lambda S, B, ret: (f'乘法满足==结合律==：先算 `X^{B.k}`（快速幂）' if 'tmp_X' not in S
                                                      else f'`X^{S.k} = {S.tmp_X}`'),
        'if n == 1': lambda S, B, ret: ('`n == 1`：`X^1` 就是 `base`，递归到底' if S.n == 1
                                        else f'`n = {S.n}`：先算 `X^{S.n // 2}`，再平方'),
        'return base': '返回 `X^1 = {base}`',
        'tmp = self.quick_pow': lambda S, B, ret: f'递归：`quick_pow(base, {B.n} // 2 = {B.n // 2})`',
        'new_ret = [[0, 0], [0, 0]]': '`new_ret = ret × base`',
        'ret = [[0, 0], [0, 0]]': lambda S, B, ret: f'拿到 `tmp = X^{S.n // 2} = {S.tmp}`，下面算 `ret = tmp × tmp = X^{S.n // 2 * 2}`',
        'ret[i][j] += tmp[i][k]': _sq,
        'if n % 2 == 1': lambda S, B, ret: (f'`n = {S.n}` 是奇数：`X^{S.n // 2 * 2}` 还差一个 `X` → 再乘一次 `base`'
                                            if S.n % 2 else f'`n = {S.n}` 是偶数：`ret` 就是 `X^{S.n}`'),
        'new_ret[i][j] += ret[i][k]': _od,
        'return new_ret': '返回 `X^{n} = {new_ret}`',
        '        return ret': '返回 `X^{n} = {ret}`',
        'return tmp_X[1][1]': '`A[1][0][0] = f(0) = 0`，所以答案就是 `X^k` 的==右下角== = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='构造 X 使 [f(k-2), f(k-1)] × X = [f(k-1), f(k)]，再对 X 快速幂',
        complexity='时间 `O(log N)`，空间 `O(log N)`（递归）',
        problem=['`F(0) = 0`，`F(1) = 1`，`F(n) = F(n-1) + F(n-2)`，给定 `n` 求 `F(n)`',
                 '示例：`n = 4` → `3`',
                 '本视频：`N = 6` → `8`'],
        quote='矩阵乘法是==满足结合律==的……后面这一堆X可以先计算好……可以视为X的幂，那么就可以使用快速幂来进行优化，这里的时间复杂度为O(logN)。',
        quote_src='—— yiduobo 题解原文',
        idea=['设行向量 `A[k-1] = [f(k-2), f(k-1)]`，按矩阵乘法定义列方程',
              '解出 `X = [[0,1],[1,1]]`，于是 `A[N] = A[1] × X^(N-1)`',
              '`X^n = (X^(n//2))²`，`n` 为奇数时再乘一个 `X`：递归 `O(log N)` 层'],
        summary=['时间 `O(log N)`，每层做 1~2 次 2×2 矩阵乘法',
                 '`A[1] = [0, 1]`，乘完只剩 `X^k` 的第二行 → 答案取==右下角== `[1][1]`',
                 '`N = 0`、`N = 1` 要单独返回：`quick_pow` 要求 `n ≥ 1`',
                 '原文为 Python 2 写法，整数除法 `n / 2` 已改为 `n // 2`，并删去多余空行',
                 '对比灵神：灵神用列向量和 `[[1,1],[1,0]]`、迭代快速幂；这里是行向量 + 递归'],
    ),
)
