PF = 17


def _parts(n):
    if n == 1:
        return [1]
    t = n // 3
    r = n % 3
    if r == 1:
        return [3] * (t - 1) + [2, 2]
    if r == 2:
        return [3] * t + [2]
    return [3] * t


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['primeFactors']
    parts = _parts(n)
    cv.text((x0 + 18, y0 + 4), f'把 primeFactors = {n} 拆成若干份，乘积最大（尽量拆 3）', 24, T['muted'], bold=True)
    m = len(parts)
    cell = min(80, (x1 - x0 - 60) / m)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * m) / 2
    y = y0 + 90
    shown = 'base' in S
    for i, v in enumerate(parts):
        X = sx + i * cell
        c = T['blue'] if v == 3 else T['orange']
        cv.rect((X + 4, y, X + cell - 4, y + cell - 8), fill=c if shown else T['panel2'], r=10, outline=T['border'])
        cv.text((X + cell / 2, y + (cell - 8) / 2), v if shown else '?', 34, T['bg'] if shown else T['dim'], anchor='mm', bold=True)
    if shown:
        t = parts.count(3)
        cv.text((x0 + 30, y + cell + 24), f'{t} 个 3（蓝）→ 3^{t}；剩下的橙色部分 → base = {S["base"]}', 24, T['text'], anchor='lm', bold=True)
        cv.text((x0 + 30, y + cell + 66), '余 1：拿回一个 3，拆成 2+2（乘积 4）；余 2：保留 2', 22, T['muted'], anchor='lm')


def _text(S):
    if 'base' not in S:
        return '先看 `primeFactors % 3`：余 0 → base=1，余 1 → p 减 1、base=4，余 2 → base=2'
    n = S['primeFactors']
    p0 = n // 3 - (1 if n % 3 == 1 else 0)
    return f'答案 = `3^p × base` = `3^{p0} × {S["base"]}`，对 `10^9+7` 取模'


CONFIG = dict(
    num=1808, title='好因子的最大数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='拆 3 + 快速幂',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maxNiceDivisors(self, primeFactors):

        if primeFactors == 1:
            return 1

        mod = 10 ** 9 + 7
        p = primeFactors // 3
        if primeFactors % 3 == 1:
            p -= 1
            base = 4
        elif primeFactors % 3 == 2:
            base = 2
        else:
            base = 1

        return self.quickPow(p, mod) * base % mod

    def quickPow(self, p, mod):
        if p == 0:
            return 1
        elif p == 1:
            return 3

        tmp = self.quickPow(p // 2, mod) ** 2 % mod
        if p % 2 == 1:
            tmp = tmp * 3 % mod
        return tmp
''',
    call=f'Solution().maxNiceDivisors({PF})',
    expect=486,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_text, size=24, h=70),
        dict(type='calls', h=230, hide=('mod',)),
    ],
    watch=[('primeFactors', 'primeFactors', 'blue'), ('p', 'p', 'pink'), ('base', 'base', 'orange'), ('tmp', 'tmp', 'green')],
    captions={
        'if primeFactors == 1': lambda S, B, r: ('`primeFactors = 1`：n 本身是质数，答案只能是 1' if S.primeFactors == 1 else f'`primeFactors = {S.primeFactors}` 不是 1，进入一般情况'),
        'mod = 10': '答案很大，要对 `mod = 10^9+7` 取模',
        'p = primeFactors // 3': '先尽量拆 3：`{primeFactors} // 3` = `p` = =={p}==',
        'if primeFactors % 3 == 1': lambda S, B, r: f'`{S.primeFactors} % 3` = {S.primeFactors % 3}' + ('：余 1 → 拿回一个 3，把 3+1 拆成 2+2' if S.primeFactors % 3 == 1 else '，不是 1'),
        'p -= 1': '`p` 减 1 → =={p}==：把一个 3 拿回来',
        'base = 4': '`base = 4`：这个 3 和余下的 1 合成 2+2，乘积是 4',
        'elif primeFactors % 3 == 2': lambda S, B, r: f'`{S.primeFactors} % 3` = {S.primeFactors % 3}' + ('：余 2 → 直接保留这个 2' if S.primeFactors % 3 == 2 else '，不是 2'),
        'base = 2': '`base = 2`：剩下的 2 保留',
        'base = 1': '整除：全是 3，`base = 1`',
        'return self.quickPow': '`3^{p}` 交给快速幂（下面递归二分），再乘 `base = {base}`',
        'if p == 0': lambda S, B, r: f'`p = {S.p}`' + ('：3^0 = 1，递归出口' if S.p == 0 else '，还没到出口'),
        'return 1': '`3^0 = 1`',
        'elif p == 1': lambda S, B, r: f'`p = {S.p}`' + ('：3^1 = 3，递归出口' if S.p == 1 else '，继续二分'),
        'return 3': '`3^1 = 3`',
        'tmp = self.quickPow': lambda S, B, r: f'二分：`3^{S.p}` = (`3^{S.p // 2}`)^2 = ==`{S.tmp}`==（已取模）',
        'if p % 2 == 1': lambda S, B, r: f'下层返回并平方后 `tmp` = {S.tmp} = 3^{S.p // 2 * 2}；`p = {S.p}` 是{"奇" if S.p % 2 else "偶"}数' + ('，还要再乘一个 3' if S.p % 2 else '，不用多乘'),
        'tmp = tmp * 3': '奇数次方多乘一个 3：`tmp` = =={tmp}==',
        'return tmp': '`3^{p}` mod = =={tmp}==，返回上一层',
    },
    cards=dict(
        one_liner='好因子个数 = k 的乘积，转成「拆 3」问题',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['`primeFactors` 是 `n` 的质因数总个数（可重复）',
                 '好因子：能被 `n` 的所有质因数整除的 `n` 的因子',
                 '求 `n` 的好因子最多有几个，对 `10^9+7` 取模',
                 '本视频：`primeFactors = 17` → `486`'],
        quote='问题就转化成了将找出一组k，使得其满足k[0] + k[1] + ... + k[m] <= primeFactors，且k[0] * k[1] * ... * k[m]最大。这就是经典的拆3问题',
        quote_src='—— yiduobo 题解原文',
        idea=['`n = p0^k0 × p1^k1 ×…`，好因子个数 = `k0 × k1 ×…`，而质因数总数 = `k0 + k1 +…`',
              '所以：把 `primeFactors` 拆成若干正整数，乘积最大 → 尽量拆 3',
              '余 1 拿回一个 3 变成 2+2，余 2 保留；`3^p` 用快速幂'],
        summary=['时间 `O(log n)`，空间 `O(log n)`（递归深度）',
                 '`primeFactors = 1` 要单独返回 1',
                 '余 1 时不能留一个 1：`3×1 < 2×2`',
                 '原文为 Python 2 写法，`/` 为整数除法，已改为 `//`，并删去了类型说明文档字符串'],
    ),
)
