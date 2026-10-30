def _text(S):
    if 'x' not in S:
        return '最终构造：==一堆 0…01、一堆 1…10、再加一个 1…11=='
    ln = S.get('_line')
    if ln is not None and ln >= 22:
        return '`quickPow`：指数折半，`base^p = (base^(p//2))² ×（p 为奇数再乘 base）`'
    if 'res2' in S:
        return f'`res1 × res2` = `{S["res1"]} × {S["res2"]}`（取模前乘积 `(2^p−1)·(2^p−2)^(2^(p−1)−1)`）'
    if 'e' in S and ln is not None and ln >= 10:
        return f'指数 `e = 2^(p−1) − 1` 对 `mod−1` 取模（费马小定理）：当前 `e = {S["e"]}`'
    return f'`x = 2^p mod 10^9+7 = {S["x"]}`，`res1 = x − 1`（就是 `2^p − 1`）'


def _bits(v, p):
    return format(v, '0%db' % p)


P = 3   # 示例 p（递归里的 p 是 quickPow 自己的参数，所以这里固定）


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = P
    N = (1 << p) - 1
    m = (1 << (p - 1)) - 1
    cv.text((x0 + 18, y0 + 2), f'最终数组（共 {N} 个数，p = {p}）', 22, T['muted'], bold=True)
    rows = [(_bits(1, p), m, T['cyan'], f'{m} 个 {_bits(1, p)}（= 1）'),
            (_bits(N - 1, p), m, T['orange'], f'{m} 个 {_bits(N - 1, p)}（= {N - 1}）'),
            (_bits(N, p), 1, T['yellow'], f'1 个 {_bits(N, p)}（= {N}）')]
    cell = min(110, (x1 - x0 - 60) / max(m, 1) - 10)
    y = y0 + 34
    for bits, cnt, col, label in rows:
        cv.text((x0 + 24, y - 6), label, 20, col, bold=True)
        for i in range(cnt):
            X = x0 + 24 + i * (cell + 10)
            cv.rect((X, y + 30, X + cell, y + 66), fill=col, r=8, alpha=235)
            cv.text((X + cell / 2, y + 48), bits, 22, T['bg'], anchor='mm', bold=True, mono=True)
        y += 78


CONFIG = dict(
    num=1969, title='数组元素的最小非零乘积', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按位归属推导 + 费马降幂 + 三次快速幂',
    tags=['难度分 1967'],
    code='''
class Solution(object):
    def minNonZeroProduct(self, p):

        mod = 10 ** 9 + 7
        x = self.quickPow(2, p, mod)
        res1 = x - 1
        if res1 < 0:
            res1 += mod
        
        e = self.quickPow(2, p - 1, mod - 1)
        e -= 1
        if e < 0:
            e += mod - 1
        
        x -= 2
        if x < 0:
            x += mod
        res2 = self.quickPow(x, e, mod)

        return res1 * res2 % mod
    
    def quickPow(self, base, p, mod):
        if p == 0:
            return 1
        elif p == 1:
            return base
        
        res = self.quickPow(base, p // 2, mod)
        res = res * res % mod
        if p % 2 == 1:
            res = res * base % mod
        
        return res
''',
    call='Solution().minNonZeroProduct(3)',
    expect=1512,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='custom', draw=_draw, h=300),
        dict(type='calls', h=260, hide=()),
    ],
    watch=['p', 'x', 'res1', 'e', 'res2', ('mod', 'mod', 'blue')],
    captions={
        'x = self.quickPow(2, p, mod)': '`x = 2^p mod 10^9+7`：用快速幂求，`x = {x}`',
        'res1 = x - 1': '`res1 = x − 1 = 2^p − 1` = =={res1}==，就是落单的那个全 1 数',
        'e = self.quickPow': '指数 `2^(p−1) − 1` 太大：`mod` 是质数，==费马小定理==说 `x^(mod−1) ≡ 1`，指数可以先对 `mod−1` 取模，先求 `2^(p−1) mod (mod−1)` = {e}',
        'e -= 1': '指数 `2^(p−1)−1` 太大：`mod` 是质数，==费马小定理== `x^(mod−1) ≡ 1`，指数可先对 `mod−1` 取模；这里 `2^(p−1)` 取模得 {B.e}，再减 1 → `e = {e}`',
        'x -= 2': '底数 `2^p − 2`：`x = {x}`',
        'res2 = self.quickPow(x, e, mod)': '`res2 = (2^p−2)^e mod 10^9+7` = =={res2}==（第三次快速幂）',
        'return res1': '`res1 × res2 % mod` = `{res1} × {res2}` → =={ret}==',
        'if p == 0': '`p = {p}`：快速幂的递归边界检查',
        'elif p == 1': lambda S, B, r: (f'`p = 1`：递归到底，直接返回 `base = {S.base}`' if S.p == 1 else f'`p = {S.p}`：还没到底，继续折半'),
        'res = self.quickPow': '把指数折半：`p // 2 = {p // 2}`，先求 `base^({p // 2})` = =={res}==',
        'res = res * res': '平方：`base^({p//2})` 的平方 = =={res}==',
        'res = res * base': '指数是奇数，多乘一个 `base` → =={res}==',
        'return res': '这层返回 `{res}`',
    },
    cards=dict(
        one_liner='最小的构造是 2^(p−1)−1 个 0…01 和 1…10，加一个 1…11',
        complexity='时间 `O(p)`，空间 `O(p)`（递归栈）',
        problem=['数组含 `[1, 2^p−1]` 的所有整数，可交换两数相同位置的二进制位',
                 '求能得到的最小非零乘积，对 `10^9+7` 取余',
                 '示例：`p = 3` → `1512`'],
        quote='最终的构造结果就是 2^(p - 1) - 1个00...0001，2^(p - 1) - 1个11...1110，以及一个11...1111。',
        quote_src='—— yiduobo 题解原文',
        idea=['每一位上 1 的个数比 0 多一个；某位只有一个数是 0 时，这个 `2^k` 给较小的那个数更小',
              '结果：乘积 `(2^p−2)^(2^(p−1)−1) × (2^p−1)`',
              '三次快速幂：底数 `2^p`、指数先对 `mod−1` 取模（费马小定理）、最后 `x^e`'],
        summary=['时间 `O(p)`，空间 `O(p)`（递归栈）',
                 '易错点：指数 `2^(p−1)−1` 要对 `mod−1` 而不是 `mod` 取模',
                 '易错点：减法后可能为负，要补 `mod`（或 `mod−1`）',
                 '原文为 Python 2 写法，`quickPow` 里的 `p / 2` 已改为 `p // 2`',
                 '对比灵神：灵神用 `pow` + 全 1 指数去掉了降幂这一步'],
    ),
)
