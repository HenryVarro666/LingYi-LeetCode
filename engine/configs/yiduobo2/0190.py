N = 44


def _bits_row(cv, T, x, y, cell, val, label, hi=None, hi_col=None, base_col=None):
    cv.text((x, y), label, 22, T['muted'], bold=True)
    y += 32
    for d in range(32):
        b = 31 - d
        bit = val >> b & 1
        X = x + d * cell
        if hi is not None and b == hi:
            fill, tc = hi_col, T['bg']
        elif bit:
            fill, tc = base_col, T['bg']
        else:
            fill, tc = T['panel2'], T['dim']
        cv.rect((X + 1, y, X + cell - 1, y + 42), fill=fill, r=4)
        cv.text((X + cell / 2, y + 21), bit, 20, tc, anchor='mm', bold=True, mono=True)
        if b % 8 == 0 and b:
            cv.line([(X + cell, y - 4), (X + cell, y + 46)], T['border'], 2)
    return y + 42


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S:
        return
    ln = S.get('_line')
    cell = (x1 - x0 - 40) / 32
    x = x0 + 20
    n_now = B['n'] if ln == 9 else S['n']
    k = S.get('k')
    take = ln in (8, 9) and n_now
    yn = _bits_row(cv, T, x, y0 + 10, cell, n_now, f'n = {n_now}（黄 = 最低位 n & 1，下一个要搬走的）',
                   hi=0 if take else None, hi_col=T['yellow'], base_col=T['blue'])
    res = S.get('res', 0)
    hk = B.get('k') if ln == 9 else k
    yr = _bits_row(cv, T, x, yn + 110, cell, res, f'res = {res}（绿 = 已放好的 1，粉 = 第 k 位）',
                   hi=hk if (hk is not None and 0 <= hk <= 31) else None, hi_col=T['pink'], base_col=T['green'])
    if k is not None and 0 <= k <= 31:
        X = x + (31 - k) * cell + cell / 2
        cv.tri_up(X, yr + 8, 9, T['pink'])
        cv.text((X, yr + 24), f'k={k}', 20, T['pink'], anchor='mt', bold=True)
    if ln == 9:
        kb = B['k']
        a = (x + 31 * cell + cell / 2, yn + 4)
        b = (x + (31 - kb) * cell + cell / 2, yn + 140)
        cv.arc_arrow(a, b, 30, T['yellow'], 4)
        cv.text((x, yr + 70), f'第 0 位的 {B["n"] & 1} → 左移 {kb} 位 → 放到 res 的第 {kb} 位', 24, T['yellow'], bold=True)
    tgt = int(f'{N:032b}'[::-1], 2)
    y2 = _bits_row(cv, T, x, yr + 120, cell, N, f'对照：原始输入 n = {N}', base_col=T['dim'])
    _bits_row(cv, T, x, y2 + 16, cell, tgt, f'目标：完全倒过来 = {tgt}', base_col=T['dim'])


CONFIG = dict(
    num=190, title='颠倒二进制位', difficulty='Easy', category='技巧',
    author='yiduobo', technique='逐位取出 · 左移 k 位',
    tags=['面试经典150'],
    code='''
class Solution:
    # @param n, an integer
    # @return an integer
    def reverseBits(self, n):
        res = 0
        k = 31

        while n:
            res += (n & 1) << k
            n >>= 1
            k -= 1

        return res
''',
    call=f'Solution().reverseBits({N})',
    expect=872415232,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 存答案，从 0 开始',
        'k = 31': '`k = 31`：从后往前取出的第一位（最低位）要放到==第 31 位==',
        'while n': lambda S, B, ret: (f'`n = {B.n}`（二进制 `{B.n:b}`）不为 0 → 继续取最低位' if B.n
                                      else '`n == 0`：剩下的高位全是 0，搬过去也是 0 → ==提前结束=='),
        'res += (n & 1) << k': '`n & 1 = {B.n & 1}` 取出最后一位，左移 `{k}` 位加到 res 上 → `res = {res}`',
        'n >>= 1': '`n` 右移一位，扔掉刚取走的最低位 → `{n:b}`',
        'k -= 1': lambda S, B, ret: (f'`k = {S.k}`：倒数第二位左移 30 位，以此类推' if S.k == 30 else f'`k` → `{S.k}`'),
        'return res': '把每一位左移后加起来就是答案 → =={ret}==',
    },
    cards=dict(
        one_liner='从后往前逐位取出 n 的每一位，第 i 个取出的放到第 31−i 位',
        complexity='时间 `O(log n)`（至多 32 次），空间 `O(1)`',
        problem=['颠倒给定的 32 位整数的二进制位',
                 '示例：`43261596` → `964176192`',
                 '本视频：`44`（二进制 `101100`）→ `872415232`（`001101` 后面跟 26 个 0）'],
        quote='通过这两种运算的配合从后往前依次取出n的每一位，然后对于最后一位，需要将其左移31位，对于倒数第二位，则是左移30位，以此类推。',
        quote_src='—— yiduobo 题解',
        idea=['`n & 1` 取 n 二进制的最后一位，`n >> 1` 让 n 右移一位',
              '第 1 个取出的位左移 31，第 2 个左移 30……用 `k` 记录左移多少',
              '把每一位左移后的结果加起来就是答案'],
        result='`n = 44` 的 6 位全部搬完：`res = 872415232` ✓',
        summary=['时间 `O(log n)`：循环次数 = n 的二进制长度，最多 32 次',
                 '`while n` 可以提前结束：n 变成 0 后剩下的位都是 0',
                 '对比灵神：逐位搬运要循环；灵神分治只需 5 次位运算',
                 '原文代码在 Python 3 下可直接运行，未做修改（保留了 LeetCode 旧模板的 @param 注释）'],
    ),
)
