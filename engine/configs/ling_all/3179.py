N, K = 4, 3
_rows = [[1] * N]
for _ in range(K):
    _p, _r = 0, []
    for _x in _rows[-1]:
        _p += _x
        _r.append(_p)
    _rows.append(_r)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '每秒后的数组（从左下往右上看斜线，就是杨辉三角）', 24, T['muted'], bold=True)
    cw, ch = 110, min(64, (y1 - y0 - 110) / (K + 1))
    sx, sy = x0 + 110, y0 + 60
    for t, row in enumerate(_rows):
        y = sy + t * ch
        cv.text((sx - 20, y + ch / 2), f'{t} 秒', 24, T['dim'], anchor='rm', bold=True)
        for j, v in enumerate(row):
            last = (t == K and j == N - 1)
            diag = (t + j == K + N - 1)
            col = T['yellow'] if last else (T['cyan'] if diag else (60, 66, 76))
            cv.rect((sx + j * cw, y + 4, sx + j * cw + cw - 8, y + ch - 4), fill=col, r=8)
            cv.text((sx + j * cw + (cw - 8) / 2, y + ch / 2), v, 30, T['bg'] if (last or diag) else T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=3179, title='K 秒后第 N 个元素的值', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='杨辉三角 · 组合数',
    tags=['灵神题单', '组合数学'],
    code='''
class Solution:
    def valueAfterKSeconds(self, n: int, k: int) -> int:
        return comb(n + k - 1, k) % 1_000_000_007
''',
    setup='from math import comb',
    call=f'Solution().valueAfterKSeconds({N}, {K})',
    expect=20,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=lambda S: (f"`n = {S['n']}, k = {S['k']}`：`C(n+k−1, k) = C({S['n']+S['k']-1}, {S['k']})` = =={comb(S['n']+S['k']-1, S['k'])}==" if 'n' in S else ''), h=90),
    ],
    watch=['n', 'k'],
    captions={
        'return comb': lambda S, B, r: f'斜线是杨辉三角：答案是第 `n+k−1 = {S.n+S.k-1}` 行的第 `k = {S.k}` 个数，`C({S.n+S.k-1}, {S.k})` = =={r}==',
    },
    cards=dict(
        one_liner='把脑袋往左斜 45°：每条斜线就是杨辉三角',
        complexity='时间 `O(1)`，空间 `O(1)`（预处理不计）',
        problem=['长度为 `n` 的数组，初始全是 1；每秒同时把每个元素变成「前面所有元素 + 自己」',
                 '求 `k` 秒后 `a[n-1]`，对 `10^9 + 7` 取模',
                 '示例：`n = 4, k = 5` → `56`；本视频：`n = 4, k = 3` → `20`'],
        quote='把脑袋往左斜 45°，看示例 1，你发现了什么？……这是杨辉三角。我们相当于计算的是杨辉三角第 n+k 排的第 n 个数，即 C(n+k-1,n-1) = C(n+k-1, k)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['示例的数字从左下往右上读，每条斜线 `[1,3,3,1]` 都是杨辉三角的一行',
              '所以 `a[n-1]` 就是 `C(n+k−1, k)`',
              '预处理阶乘和逆元（费马小定理）可以 `O(1)` 算组合数；Python 直接 `comb`'],
        summary=['时间 `O(1)`，空间 `O(1)`（预处理阶乘及逆元的开销不计）',
                 '`C(n+k−1, k) = C(n+k−1, n−1)`，选哪个都行',
                 '`comb` 是 Python 3.8+ 的 `math.comb`，大整数精度无忧，最后再取模',
                 '本题 `n, k ≤ 1000` 也可以 `O(nk)` DP：`f[i][j] = f[i][j−1] + f[i−1][j]`'],
    ),
)
