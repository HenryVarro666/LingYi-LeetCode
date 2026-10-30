NS = [27, 45, 1, 0, 6561, 18]
BIG = 1162261467  # 3^19


def _fac(n):
    """质因数分解 → [(p, e), ...]"""
    out, p = [], 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            out.append((p, e))
        p += 1
    if n > 1:
        out.append((n, 1))
    return out


def _fac_str(n):
    return ' × '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in _fac(n)) or '1'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    cv.text((x0 + 18, y0 + 4), '3 的幂（int 范围内一共 20 个，最大是 3^19 = 1162261467）', 24, T['muted'], bold=True)
    cw, chh = 96, 74
    sx = x0 + (x1 - x0 - cw * 10) / 2
    for k in range(20):
        r, c = divmod(k, 10)
        X, Y = sx + c * cw, y0 + 50 + r * (chh + 16)
        v = 3 ** k
        hit = v == n
        cv.rect((X + 4, Y, X + cw - 4, Y + chh), fill=T['green'] if hit else T['panel2'], r=10,
                outline=T['yellow'] if k == 19 else T['border'], width=3 if k == 19 else 1)
        cv.text((X + cw / 2, Y + 22), f'3^{k}', 20, T['bg'] if hit else T['muted'], anchor='mm', bold=True)
        s = str(v)
        cv.text((X + cw / 2, Y + 52), s, 18 if len(s) <= 5 else (15 if len(s) <= 7 else 13),
                T['bg'] if hit else T['text'], anchor='mm', mono=True)
    if n is None:
        return
    # 底部：已经测过的 n
    done = NS[:NS.index(n) + 1] if n in NS else []
    cv.text((x0 + 18, y1 - 110), '已测试', 22, T['muted'], bold=True)
    X = x0 + 40
    for v in done:
        ok = v > 0 and BIG % v == 0
        w = max(cv.tlen(str(v), 24, mono=True), cv.tlen('False', 20)) + 30
        cv.rect((X, y1 - 76, X + w, y1 - 6), fill=T['panel2'], r=10, outline=T['yellow'] if v == n else T['border'],
                width=3 if v == n else 1)
        cv.text((X + w / 2, y1 - 58), str(v), 24, T['text'], anchor='mm', mono=True, bold=True)
        cv.text((X + w / 2, y1 - 26), str(ok), 20, T['green'] if ok else T['red'], anchor='mm', bold=True)
        X += w + 12
    y = y0 + 260
    if n <= 0:
        cv.text((x0 + 40, y), f'n = {n} ≤ 0', 40, T['red'], bold=True)
        cv.text((x0 + 40, y + 70), '3 的幂一定大于 0 → 直接 False（and 短路，不会算 % 0）', 26, T['text'])
        return
    cv.text((x0 + 40, y), f'n = {n} = {_fac_str(n)}', 38, T['text'], bold=True, mono=True)
    only3 = all(p == 3 for p, _ in _fac(n))
    cv.text((x0 + 40, y + 62), '只含质因子 3' if only3 else '含有不是 3 的质因子 → 不可能整除 3^19',
            26, T['green'] if only3 else T['red'], bold=True)
    r = BIG % n
    cv.text((x0 + 40, y + 120), f'1162261467 % {n} = {r}', 36, T['green'] if r == 0 else T['red'], bold=True, mono=True)


def _cap(S, B, ret):
    n = S.n
    if n <= 0:
        return f'`n = {n}` 不大于 0 → ==and 短路==，后面的 `% n` 根本不会执行（避免除以 0）→ `False`'
    r = BIG % n
    f = _fac_str(n)
    if r == 0:
        k = next(k for k in range(20) if 3 ** k == n)
        return f'`{n} = 3^{k}` 是 `3^19` 的因子：`1162261467 % {n} = 0` → ==True=='
    return f'`{n} = {f}` 含其他质因子：`1162261467 % {n} = {r}` ≠ 0 → ==False=='


CONFIG = dict(
    num=326, title='3 的幂', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='O(1) 数学：看 n 是不是 3^19 的因子',
    tags=['List.md'],
    code='''
class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        return n > 0 and 1162261467 % n == 0
''',
    call=f'''s = Solution()
[s.isPowerOfThree(x) for x in {NS}]''',
    expect=[True, False, True, False, True, False],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return n > 0': _cap,
    },
    cards=dict(
        one_liner='在 int 范围内，n 是 3 的幂 ⇔ n > 0 且 n 整除 3^19',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定一个整数 `n`，判断它是否是 3 的幂次方：存在整数 `x` 使 `n == 3^x`',
                 '示例：`27` → `true`，`0` → `false`，`9` → `true`，`45` → `false`',
                 '范围：`-2^31 <= n <= 2^31 - 1`；进阶：不用循环或递归'],
        before=[dict(heading='3^19 是怎么来的', lines=[
            '3 的幂一定 `> 0`；`n ≤ 0` 直接排除',
            '在本题数据范围下，最大的 3 的幂是 `3^19 = 1162261467`',
            '怎么算？写个循环，找最大的满足 `3^i ≤ 2^31 - 1` 的 `i`'])],
        quote='由于==任何 3 的幂都是 3^19 的因子==，所以 3^19 mod n = 0。……如果 n 不是 3 的幂，那么 ==n 必然有不等于 3 的质因子==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n = 3^k`（`k ≤ 19`）：`3^19 = n × 3^(19−k)`，整除',
              '`n` 不是 3 的幂：它有别的质因子，而 `3^19` 只含质因子 3，不可能整除',
              '所以：当且仅当 `n > 0` 且 `1162261467 % n == 0` 时为 True'],
        result='6 个测试：`[True, False, True, False, True, False]` ✓',
        summary=['时间、空间都是 `O(1)`：一次比较 + 一次取模',
                 '易错：`n > 0` 必须写在前面，靠 `and` 短路避免 `% 0`',
                 '这个技巧只对==质数==的幂成立（比如 4 的幂就不能这样判）',
                 '朴素做法：不断除以 3 直到不能整除，看是否剩 1，`O(log n)`'],
    ),
)
