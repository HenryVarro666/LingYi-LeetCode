N0 = 130
LAYER_COL = ['blue', 'pink', 'purple', 'cyan']


def _v5(x):
    c = 0
    while x % 5 == 0:
        x //= 5
        c += 1
    return c


_KMAP = {}
for _k in range(8):
    _KMAP.setdefault(N0 // 5 ** _k, _k)


def _state(S):
    """(已计入的层数, 刚算出的层 or None)"""
    line = S.get('_line')
    n = S.get('n')
    if line in (None, 3) or n is None:
        return 0, None
    k = _KMAP.get(n, 0)
    if line == 6:
        return k - 1, k
    if line == 8:
        return 9, None
    return k, None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    done, cur = _state(S)
    xs = list(range(5, N0 + 1, 5))
    cv.text((x0 + 18, y0 + 4), f'[1,{N0}] 中 5 的倍数：每个方块 = 一个质因子 5（第 k 层 = 能被 5^k 整除）', 22, T['muted'], bold=True)
    cw = (x1 - x0 - 40) / len(xs)
    sq = min(cw - 6, 46)
    base = y1 - 110
    for idx, x in enumerate(xs):
        X = x0 + 20 + idx * cw + cw / 2
        for k in range(1, _v5(x) + 1):
            Y = base - k * (sq + 6)
            if k <= done:
                fill, out = T[LAYER_COL[k - 1]], None
            elif cur == k:
                fill, out = T['yellow'], None
            else:
                fill, out = T['panel2'], T['border']
            cv.rect((X - sq / 2, Y, X + sq / 2, Y + sq), fill=fill, outline=out, width=1, r=6)
        cv.text((X, base + 6), x, 15 if x >= 100 else 17, T['muted'], anchor='mt', mono=True)
    if 'ans' in S:
        cv.text(((x0 + x1) / 2, base + 50), f"已计入的方块数 = ans = {S['ans']}", 26, T['green'], anchor='mt', bold=True)
    # 每层计数
    ly = y0 + 46
    lx = x0 + 24
    for k in range(1, 4):
        c = N0 // 5 ** k
        on = k <= done or cur == k
        col = T[LAYER_COL[k - 1]] if k <= done else (T['yellow'] if cur == k else T['dim'])
        s = f'第{k}层：floor({N0}/{5 ** k}) = {c} 个'
        cv.rect((lx, ly, lx + 16, ly + 16), fill=col, r=3)
        cv.text((lx + 24, ly + 8), s, 21, T['text'] if on else T['dim'], anchor='lm', bold=on)
        lx += cv.tlen(s, 21, bold=True) + 60


def _chain(S):
    n = S.get('n')
    if n is None:
        return ''
    seq = []
    v = N0
    while True:
        seq.append(v)
        if v == n or v == 0:
            break
        v //= 5
    s = ' → '.join(str(x) for x in seq[:-1])
    s = (s + ' → ' if s else '') + f'=={seq[-1]}=='
    return f'n 的变化：{s}'


def _cap_div(S, B, ret):
    k = _KMAP.get(S.n, 0)
    if S.n == 0:
        return f'`n = floor({B.n} / 5) = 0`：已经没有 `5^{k}` 的倍数了'
    return f'`n = floor({B.n} / 5) = {S.n}`，它等于 `floor({N0} / 5^{k})`：有 =={S.n}== 个数是 `5^{k}` 的倍数'


def _cap_add(S, B, ret):
    k = _KMAP.get(S.n, 0)
    if S.n == 0:
        return f'`ans += 0`，不变'
    if k == 1:
        return f'5 的倍数各贡献 1 个 5：`ans = {B.ans} + {S.n}` = =={S.ans}=='
    return f'`5^{k}` 的倍数==再各多贡献== 1 个 5（第 {k} 层方块）：`ans = {B.ans} + {S.n}` = =={S.ans}=='


CONFIG = dict(
    num=172, title='阶乘后的零', difficulty='Medium', category='数学',
    author='灵茶山艾府', technique='数质因子 5 · 下取整恒等式',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution:
    def trailingZeroes(self, n: int) -> int:
        ans = 0
        while n:
            # 循环 k 次后，n 变成了 floor(n/5^k)
            n //= 5
            ans += n
        return ans
''',
    call=f'Solution().trailingZeroes({N0})',
    expect=32,
    views=[
        dict(type='text', fn=_chain, h=60),
        dict(type='custom', draw=_draw, h=540),
    ],
    watch=[('n', 'n', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 数 `{n}!` 里有多少个==质因子 5==（5 比 2 少，配对成 10 的个数就是它）',
        'while n': lambda S, B, ret: (f'`n = {S.n}` ≠ 0 → 继续除以 5' if S.n else '`n = 0`：再除下去全是 0 → 结束'),
        'n //= 5': _cap_div,
        'ans += n': _cap_add,
        'return ans': f'`{N0}!` 末尾有 =={{ret}}== 个 0：`26 + 5 + 1`',
    },
    cards=dict(
        one_liner='尾零个数 = 质因子 5 的个数 = n/5 + n/25 + n/125 + …（下取整）',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给定整数 `n`，返回 `n!` 结果中==尾随零==的数量',
                 '示例：`n = 5` → `5! = 120` → `1`；`n = 3` → `3! = 6` → `0`',
                 '进阶：能做到==对数时间==吗？',
                 f'本视频：`n = {N0}` → `32`'],
        quote='一般地，n! 的尾零个数，取决于 n! 可以==分解出多少个 10==。……由于 p 越大，上式越小，所以 n! 中的质因子 5 的个数比 2 少。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`10 = 2 × 5`：尾零个数 = 因子 2、5 个数的较小值 = 因子 5 的个数',
              '恰好被 `5^k` 整除的数有 `floor(n/5^k) − floor(n/5^(k+1))` 个，各含 `k` 个 5',
              '加权求和化简为 `floor(n/5) + floor(n/25) + floor(n/125) + …`',
              '恒等式 `floor(n/5^k) = floor(floor(n/5^(k-1)) / 5)` → 反复 `n //= 5` 再累加'],
        result=f'`ans = 26 + 5 + 1 = 32`：`{N0}!` 末尾有 32 个 0',
        after=[dict(heading='为什么可以反复 n //= 5', lines=[
            f'`floor({N0}/25)` = `floor(floor({N0}/5) / 5)` = `floor(26/5)` = `5`',
            '下取整恒等式：每轮把上一轮的 `n` ==再除以 5== 即可',
            '不用算 `5^k`：既省事，也不会因为 `5^k` 太大而溢出',
        ])],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：别真的算 `n!`，`10^4!` 是天文数字',
                 '易错：25、125 这类数含多个 5，只算 `n // 5` 会少算',
                 '质因子 2 一定比 5 多：同一公式 `p` 越大结果越小',
                 '相似题：793. 阶乘函数后 K 个零'],
    ),
)
