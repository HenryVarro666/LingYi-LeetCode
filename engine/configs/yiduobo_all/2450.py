def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s, k = S['s'], S['k']
    n = len(s)
    w = n - k + 1
    cell = min(80, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    cv.text((x0 + 18, y0 + 4), f's = {s}，k = {k}：长为 k 的窗口共 n−k+1 = {w} 个', 24, T['muted'], bold=True)
    ys = y0 + 44
    ch = cell * 0.85
    for i, c in enumerate(s):
        X = sx + i * cell
        cv.rect((X + 3, ys, X + cell - 3, ys + ch), fill=T['panel2'], outline=T['border'], r=8)
        cv.text((X + cell / 2, ys + ch / 2), c, 34, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 6), i, 16, T['dim'], anchor='mt', mono=True)
    cols = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']
    yb = ys + ch + 30
    for a in range(w):
        c = T[cols[a % len(cols)]]
        Y = yb + a * 42
        cv.rect((sx + a * cell + 3, Y, sx + (a + k) * cell - 3, Y + 32), fill=c, alpha=150, r=8)
        cv.text((sx + a * cell + (k * cell) / 2, Y + 16), f'窗口 {a}：翻 / 不翻', 20, T['text'], anchor='mm', bold=True)
    yt = yb + w * 42 + 10
    cv.text((x0 + 30, yt), f'每个窗口 2 种选择，彼此不能替代 → 2^{w} = {2 ** w} 种', 28, T['green'], bold=True)


def _t(S):
    inner = S.get('_inner', {})
    if 'x' in inner:
        r = inner.get('res')
        return f"`pow2({inner['x']})`" + (f"：`res = {r}`" if r is not None else '：还在往下拆 x')
    return ''


CONFIG = dict(
    num=2450, title='应用操作后不同二进制字符串的数量', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='窗口计数 · 递归快速幂',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def countDistinctStrings(self, s, k):

        mod = 10 ** 9 + 7

        def pow2(x):
            if x == 0:
                return 1
            if x == 1:
                return 2
            
            res = pow2(x // 2)
            res *= res
            res %= mod
            if x % 2 == 1:
                res += res
                if res >= mod:
                    res -= mod
            
            return res
        
        return pow2(len(s) - k + 1)
''',
    call='Solution().countDistinctStrings("10010", 3)',
    expect=8,
    views=[
        dict(type='custom', draw=_draw, h=340),
        dict(type='text', fn=_t, size=30, h=70),
        dict(type='calls', h=200, hide=('s', 'k')),
    ],
    watch=['mod', ('x', "x", 'blue'), ('res', 'res', 'green')],
    captions={
        'mod = ': '答案取模：`mod = 10^9 + 7`',
        'if x == 0': lambda S, B, r: (f'`x = {S.x}`：0 个窗口，只有原串 1 种 → 返回 1' if S.x == 0 else f'`x = {S.x} != 0`，继续'),
        'if x == 1': lambda S, B, r: (f'`x = 1`：1 个窗口，翻或不翻 → 返回 2' if S.x == 1 else f'`x = {S.x} != 1`，继续往下拆'),
        'return 1': '`2^0 = 1`',
        'return 2': '`2^1 = 2`，递归出口',
        'res = pow2(x // 2)': '先算一半：进入 `pow2({B.x // 2})`',
        'res *= res': '半个指数的结果平方：`res = res × res = {res}`',
        'res %= mod': '取模 `res = {res}`',
        'if x % 2 == 1': lambda S, B, r: (f'`x = {S.x}` 是奇数：平方后还差一个 2' if S.x % 2 == 1 else f'`x = {S.x}` 是偶数：平方正好，不用补'),
        'res += res': '`res + res` 就是再乘 2：`res = {res}`',
        'if res >= mod': lambda S, B, r: ('`res >= mod`，减一次 mod' if S.res >= S.mod else f'`res = {S.res} < mod`：不用减'),
        'return res': '这一层返回 `2^{x} = {res}`',
        'return pow2(len': '共 `len(s) - k + 1 = {len(s) - k + 1}` 个窗口，要算 `2^{len(s) - k + 1}`：调用 `pow2({len(s) - k + 1})`',
    },
    cards=dict(
        one_liner='n−k+1 个长度为 k 的窗口，各自翻或不翻，答案 2^(n−k+1)',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['二进制字符串 `s` 和整数 `k`，可对任意长为 `k` 的子串做==整体翻转==，次数不限',
                 '求能得到多少种不同的字符串，对 `10^9+7` 取模',
                 '示例：`s = "1001", k = 3` → `4`；本视频 `s = "10010", k = 3` → `8`'],
        quote='对于每个子串，都有翻转和不翻转两种可行的操作，另一方面，不可能通过其他子串的翻转来达成某个特定子串的翻转，因此这里就一共有2^(n - k + 1)种可行的方案。',
        quote_src='—— yiduobo 题解原文',
        idea=['长为 `n` 的串有 `n−k+1` 个长为 `k` 的窗口',
              '每个窗口 ==翻 / 不翻== 两种，且不能被别的窗口的翻转代替',
              '答案就是 `2^(n−k+1)`；指数可大，用递归快速幂 `pow2`'],
        summary=['时间 `O(log n)`，递归深度约 `log n`',
                 '窗口数是 `n−k+1`，不是 `n−k`',
                 '`x` 为奇数时平方后 `res += res`（相当于再乘 2），要记得判断是否 `>= mod`',
                 '原文为 Python 2 写法，`/` 为整数除法，已改为 `//`',
                 '题目原题面库里没有：按题意（翻转任意长 k 的子串，数不同结果）演示'],
    ),
)
