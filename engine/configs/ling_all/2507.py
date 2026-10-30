CHAIN = [15, 8, 6, 5]


def _factors(n):
    r, i = [], 2
    while i * i <= n:
        while n % i == 0:
            r.append(i)
            n //= i
        i += 1
    if n > 1:
        r.append(n)
    return r


def _found(facs, s):
    c = 0
    for k, f in enumerate(facs):
        if c == s:
            return k
        c += f
    return len(facs) if c == s else 0


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S or 's' not in S:
        return
    n, s = S['n'], S['s']
    k = CHAIN.index(n) if n in CHAIN else 0
    cv.text((x0 + 18, y0 + 4), 'n 的变化链（每轮：n → 它的质因数之和）', 24, T['muted'], bold=True)
    cw, gap = 120, 70
    tot = len(CHAIN) * cw + (len(CHAIN) - 1) * gap
    sx = x0 + ((x1 - x0) - tot) / 2
    y = y0 + 60
    for j, v in enumerate(CHAIN):
        X = sx + j * (cw + gap)
        if j <= k:
            cur = j == k
            cv.rect((X, y, X + cw, y + 80), fill=T['blue'] if cur else T['panel2'], outline=T['border'], r=14)
            cv.text((X + cw / 2, y + 40), v, 40, T['bg'] if cur else T['muted'], anchor='mm', bold=True)
        else:
            cv.rect((X, y, X + cw, y + 80), outline=T['border'], r=14)
            cv.text((X + cw / 2, y + 40), '?', 36, T['dim'], anchor='mm', bold=True)
        if j < len(CHAIN) - 1:
            cv.arrow((X + cw + 8, y + 40), (X + cw + gap - 8, y + 40), T['dim'], 3)
    facs = _factors(n)
    fd = _found(facs, s)
    y2 = y + 170
    cv.text((x0 + 18, y2 - 50), f'n = {n} 的质因数（绿 = 已加进 s）', 24, T['muted'], bold=True)
    tw = 90
    tot2 = len(facs) * tw + (len(facs) - 1) * 24
    sx2 = x0 + ((x1 - x0) - tot2) / 2
    for j, f in enumerate(facs):
        X = sx2 + j * (tw + 24)
        got = j < fd
        cv.rect((X, y2, X + tw, y2 + 80), fill=T['green'] if got else None, outline=T['border'], r=14)
        cv.text((X + tw / 2, y2 + 40), f, 38, T['bg'] if got else T['dim'], anchor='mm', bold=True)
    done = ' + '.join(str(f) for f in facs[:fd]) or '0'
    cv.text(((x0 + x1) / 2, y2 + 130), f's = {done} = {s}' if fd > 1 else f's = {s}', 36, T['green'], anchor='mm', bold=True)


CONFIG = dict(
    num=2507, title='使用质因数之和替换后可以取到的最小值', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='分解质因数 · 循环到不动点',
    tags=['灵神题单·数学算法', '难度分 1500'],
    code='''
class Solution:
    def smallestValue(self, n: int) -> int:
        while True:
            x, s, i = n, 0, 2
            while i * i <= x:
                while x % i == 0:
                    s += i
                    x //= i
                i += 1
            if x > 1: s += x
            if s == n: return n
            n = s
''',
    call='Solution().smallestValue(15)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"试除数 `i = {S['i']}`，剩余 `x = {S['x']}`" if 'i' in S else '', size=28, h=60),
        dict(type='custom', draw=_draw, h=470),
    ],
    watch=[('n', 'n', 'blue'), 'x', ('i', 'i', 'pink'), ('s', 's', 'green')],
    captions={
        'x, s, i = n': '新一轮：拿 `x = {x}` 做分解（保住 `n` 用来对比），`s` 累加质因数，试除数 `i` 从 2 起',
        'while i * i <= x': lambda S, B, r: (f'`i*i = {S.i * S.i} <= x = {S.x}`，还可能有因数 `{S.i}` 或更大 → 继续试除' if S.i * S.i <= S.x
                                              else f'`i*i = {S.i * S.i} > x = {S.x}`：剩下的 x 不会再有 ≤ 根号 x 的因数 → 停止试除'),
        'while x % i == 0': lambda S, B, r: (f'`{S.x} % {S.i} == 0`：`{S.i}` 整除 x，是一个质因数' if S.x % S.i == 0
                                              else f'`{S.x} % {S.i} != 0`：`{S.i}` 除尽了（或根本不是因数）→ 换下一个 `i`'),
        's += i': '`i = {i}` 一定是质数（更小的因子已除尽），重复的因子要算多次：`s` → =={s}==',
        'x //= i': '除掉一个 `{i}`：`x` → {x}，下一行看还能不能再除',
        'i += 1': '`i` → {i}',
        'if x > 1': lambda S, B, r: (f'`x = {S.x} > 1`：剩下的是一个大质数（比根号大的至多一个）→ 加进 `s`' if S.x > 1
                                      else '`x = 1`：已经分解干净，没有剩余的大质因数'),
        'if s == n': lambda S, B, r: (f'`s = {S.s} == n = {S.n}`：再替换也不变（n 是质数）→ 返回 =={S.n}==' if S.s == S.n
                                       else f'`s = {S.s} != n = {S.n}`：n 还能变，继续下一轮'),
        'n = s': '把 `n` 换成质因数之和：`n` → =={n}==，回到 while True',
    },
    cards=dict(
        one_liner='不断把 n 换成质因数之和，直到它不再变化',
        complexity='时间 `O(√n)`，空间 `O(1)`',
        problem=['把 `n` 换成它的质因数之和（重复的质因数算多次），一直重复',
                 '求 `n` 能取到的最小值',
                 '示例：`15 → 8 → 6 → 5`，返回 `5`；`3` 本身是质数，返回 `3`'],
        quote='不断循环，计算 n 的质因数之和 s。如果 s=n 说明无法再继续减小 n 了，返回 n；否则更新 n 为 s，继续循环。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每轮都做一次试除法分解质因数，小因子先除尽，保证拿到的都是质数',
              '合数的质因数之和严格小于它，所以 n 越换越小，停在 `s == n`（质数）',
              '剩下的 `x > 1` 是一个比 √x 大的质数，别忘了补进 s'],
        summary=['时间 `O(√n)`：最坏每轮 n 约减半，根号和是等比级数',
                 '易错点：重复的质因数要算多次（8 → 2+2+2）',
                 '易错点：循环结束后 `x > 1` 的剩余部分要加进 `s`',
                 '同类题：2521 数组乘积中的不同质因数数目（同样的分解模板）'],
    ),
)
