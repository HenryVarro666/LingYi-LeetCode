MOD = 10 ** 9 + 7


def _mat(cv, T, x, y, M, color, label, cw=105, ch=62):
    cv.text((x, y), label, 22, T['muted'], bold=True)
    y += 36
    for r, row in enumerate(M):
        for c, v in enumerate(row):
            X, Y = x + c * (cw + 8), y + r * (ch + 8)
            cv.rect((X, Y, X + cw, Y + ch), fill=color, r=10)
            cv.text((X + cw / 2, Y + ch / 2), v, 28, T['bg'], anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 20, y0 + 6), '红黄红 x 种，红黄绿 y 种：新增一行 x\' = 3x + 2y，y\' = 2x + 2y', 24, T['text'], bold=True)
    if 'base' not in S:
        return
    _mat(cv, T, x0 + 40, y0 + 70, S['base'], T['blue'], 'base')
    X = x0 + 40
    if S.get('tmp') is not None and 'n' in S:
        _mat(cv, T, x0 + 340, y0 + 70, S['tmp'], T['yellow'], 'tmp（一半次幂）')
    if S.get('res') is not None and 'tmp' in S:
        _mat(cv, T, x0 + 640, y0 + 70, S['res'], T['green'], 'res = tmp × tmp')
    if 'n' in S and 'tmp' not in S:
        cv.text((x0 + 340, y0 + 110), f"当前要算 base 的 {S['n']} 次方", 26, T['text'])
    cv.text((x0 + 20, y1 - 40), '元素都对 10^9+7 取模；最后 4 个元素之和 × 6 就是答案', 22, T['muted'])


CONFIG = dict(
    num=1411, title='给 N x 3 网格图涂色的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='利用对称性 · 两类状态递推 + 矩阵快速幂',
    tags=['灵神题单', '难度分 1845'],
    code='''
class Solution(object):
    def numOfWays(self, n):

        if n == 1:
            return 12

        mod = 10 ** 9 + 7
        base = [[3, 2], [2, 2]]
        final = self.quick_pow(n - 1, base, mod)
        return ((final[0][0] + final[0][1] + final[1][0] + final[1][1]) % mod * 6) % mod

    def quick_pow(self, n, base, mod):
        if n == 1:
            return base[:]
        
        tmp = self.quick_pow(n // 2, base, mod)
        res = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    res[i][j] += tmp[i][k] * tmp[k][j]
                    res[i][j] %= mod
        
        if n % 2 == 0:
            return res
        
        tmp = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    tmp[i][j] += res[i][k] * base[k][j]
                    tmp[i][j] %= mod
        
        return tmp
''',
    call='Solution().numOfWays(7)',
    expect=106494,
    skip=['mod = 10', 'for i in range(2)', 'for j in range(2)', 'for k in range(2)', 'res[i][j] +=', 'res[i][j] %=', 'tmp[i][j] +=', 'tmp[i][j] %='],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=200),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        4: '`n = {n}`：不是 1，继续（`n = 1` 单独返回 12，其余走 `base^(n-1)`）',
        13: lambda S, B, r: (f'`n = {S.n}`：只需 1 次方 → 直接返回 `base`' if S.n == 1 else f'`n = {S.n}`：不是 1，先算一半次幂'),
        'return 12': '一行三格有 12 种涂法，`n = 1` 直接返回 `12`',
        'base = [[3, 2]': '转移矩阵：`[x, y] × [[3,2],[2,2]]` 得到下一行的 `[x\', y\']`',
        'final = self.quick_pow': '`final = base^(n-1)`：第一行有 `x = y = 1`（各记一个代表），要乘 `n-1 = {B.n - 1}` 次矩阵',
        'return base[:]': '递归到底：`1` 次方就是 `base` 本身（复制一份）',
        'tmp = self.quick_pow': '先递归算 `base^({B.n // 2})`（`n // 2`，原文是 Python 2 的 `n / 2`）',
        'res = [[0, 0], [0, 0]]': '准备结果矩阵，下面做 `tmp × tmp`（2×2 三重循环，每个元素取模）',
        'if n % 2 == 0': '`res = tmp × tmp` = `base^{(n // 2) * 2}`；`n = {n}` ==偶数==就返回它，==奇数==还要再乘一个 `base`',
        'tmp = [[0, 0]': 'n 是奇数：`base^n = base^(n-1) × base`，再算一次矩阵乘法（`res × base`）',
        'return tmp': '奇数次幂：返回 `res × base`',
        'return res': '偶数次幂：返回 `tmp × tmp`',
        'return ((final': '四个元素之和 = 两类状态数目之和；再 ×6（6 种颜色排列）= =={ret}=='
    },
    cards=dict(
        one_liner='利用颜色对称，只数两类形状：ABA 和 ABC',
        complexity='时间 `O(log n)`，空间 `O(log n)`（递归栈）',
        problem=['`n × 3` 网格，每格涂红/黄/绿，相邻格子颜色不同，求方案数（对 `10^9+7` 取模）',
                 '`n = 1` → `12`；`n = 2` → `54`；`n = 3` → `246`',
                 '本视频：`n = 7` → `106494`'],
        quote='三种颜色是完全等价的，因此我们可以只考虑以某种颜色开头的所有方案数，在这里我们只考虑最左侧是红色的这四种情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['一行只有两类形状：A-B-A（如红黄红）和 A-B-C（如红黄绿）',
              'A-B-A 能接 3 个 A-B-A、2 个 A-B-C；A-B-C 能接 2 个 A-B-A、2 个 A-B-C',
              '于是 `x\' = 3x + 2y`，`y\' = 2x + 2y`，对应矩阵 `[[3,2],[2,2]]`，用快速幂',
              '最后把 `[1, 1]` 乘上去，各元素求和，再乘 6（颜色排列）'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '`n = 1` 要单独返回 12，因为后面是 `base^(n-1)`，`n - 1 = 0` 次方递归不到',
                 '原文为 Python 2 写法，`quick_pow` 里的整数除法 `n / 2` 已改为 `n // 2`',
                 '对比灵神：灵神用 Berlekamp-Massey 找出 `f[i] = 5f[i-1] − 2f[i-2]`；yiduobo 靠对称性手推两类状态'],
    ),
)
