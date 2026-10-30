def _strong(x):
    return [b for b in range(20) if x >> b & 1]


def _chips(N=22):
    out = []
    x = 1
    while len(out) < N:
        for e in _strong(x):
            out.append((x, e))
        x += 1
    return out[:N]


def _ones(n):
    return sum(bin(x).count('1') for x in range(n))


def _chip_row(cv, box, T, N, green, yellow, y, title):
    x0, y0, x1, y1 = box
    chips = _chips(N)
    cell = min(54, (x1 - x0 - 40) / N)
    sx = x0 + 20
    cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
    starts = {}
    for k, (x, e) in enumerate(chips):
        starts.setdefault(x, []).append(k)
    for x, ks in starts.items():
        a, b = sx + ks[0] * cell, sx + (ks[-1] + 1) * cell
        cv.line([(a + 3, y - 14), (b - 3, y - 14)], T['dim'], 3)
        cv.text(((a + b) / 2, y - 22), str(x), 20, T['muted'], anchor='mb', bold=True, mono=True)
    for k, (x, e) in enumerate(chips):
        X = sx + k * cell
        if k < green:
            fill, tc = T['green'], T['bg']
        elif k < yellow:
            fill, tc = T['yellow'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((X + 3, y, X + cell - 3, y + cell - 6), fill=fill, r=8, outline=T['border'])
        cv.text((X + cell / 2, y + (cell - 6) / 2), str(e), 26, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, y + cell + 2), str(k), 16, T['dim'], anchor='mt', mono=True)
    return sx, cell


def _norig(S):
    n = S['n']
    taken = S['cnt1'] - bin(n).count('1')
    if taken == 1:
        pos = sum(b for b in range(20) if n >> b & 1)
        return n | (1 << (S['sum_i'] - pos))
    return n


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S or 'cnt1' not in S:
        _chip_row(cv, box, T, 22, 0, 0, y0 + 90, 'big_nums 的幂次数组（每组 = 整数 x 的强数组）')
        return
    no = _norig(S)
    base = _ones(no)
    left_phase = '_' in S or S.get('_line') == LEFT_LINE
    taken = (S['cnt1'] - bin(S['n']).count('1')) if left_phase else 0
    sx, cell = _chip_row(cv, box, T, 22, base, base + taken + (1 if S.get('_line') in (LEFT_LINE + 1, LEFT_LINE + 2, LEFT_LINE + 3) else 0) if left_phase else base,
                         y0 + 90, '大数组的幂次（每组 = 整数 x 的强数组）；绿 = 已被试填的整数覆盖，黄 = 由 n 的低位补的')
    # n 的二进制
    yb = y0 + 90 + cell + 70
    cv.text((x0 + 20, yb + 24), 'n 的二进制', 24, T['muted'], anchor='lm', bold=True)
    n = S['n']
    cur_i = S.get('i') if not left_phase else None
    for j, b in enumerate(range(4, -1, -1)):
        X = x0 + 220 + j * 78
        on = n >> b & 1
        trial = cur_i == b
        cv.rect((X, yb, X + 66, yb + 52), fill=T['blue'] if on else T['panel2'], r=8,
                outline=T['yellow'] if trial else T['border'], width=5 if trial else 1)
        cv.text((X + 33, yb + 26), str(on), 30, T['bg'] if on else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + 33, yb + 58), f'2^{b}={1 << b}', 18, T['yellow'] if trial else T['dim'], anchor='mt', mono=True)
    cv.text((x0 + 220 + 5 * 78 + 14, yb + 26), f'n = {n}', 30, T['text'], anchor='lm', bold=True, mono=True)
    msg = f'覆盖了 ones(n) = {base} 个幂次'
    if left_phase:
        msg += f'，再用 n 的最低位补 {taken} 个'
    cv.text((x0 + 20, yb + 110), msg, 26, T['green'], anchor='lm', bold=True)
    if not left_phase and 'c' in S and 'i' in S and S.get('_line', 0) >= LEFT_LINE - 9 - 1 or (not left_phase and 'c' in S and 'i' in S):
        ok = S['c'] <= S['k'] if S.get('_line') == LEFT_LINE - 8 else None
        cv.text((x0 + 20, yb + 160), f"试填第 {S['i']} 位：新增 c = {S['c']} 个幂次；可用 k = {S['k']}", 26, T['text'], anchor='lm', bold=True)
    cv.text((x0 + 20, yb + 210), f"已覆盖部分的幂次之和 res = {S['res']}", 26, T['cyan'], anchor='lm', bold=True)


def _txt(S):
    if 'k' not in S:
        return '把「乘积」变成「幂次之和」，再用前缀和 `sum_e(to+1) − sum_e(from)`'
    return f'`sum_e(k)`：前 `k` 个幂次的和；剩余要凑的幂次个数 `k = {S["k"]}`'


CODE = '''
class Solution:
    def findProductsOfElements(self, queries: List[List[int]]) -> List[int]:
        def sum_e(k: int) -> int:
            res = n = cnt1 = sum_i = 0
            for i in range((k + 1).bit_length() - 1, -1, -1):
                c = (cnt1 << i) + (i << i >> 1)  # 新增的幂次个数
                if c <= k:
                    k -= c
                    res += (sum_i << i) + ((i * (i - 1) // 2) << i >> 1)
                    sum_i += i  # 之前填的 1 的幂次之和
                    cnt1 += 1  # 之前填的 1 的个数
                    n |= 1 << i  # 填 1
            # 剩余的 k 个幂次，由 n 的低 k 个 1 补充
            for _ in range(k):
                lb = n & -n
                res += lb.bit_length() - 1
                n ^= lb  # 去掉最低位的 1（置为 0）
            return res
        return [pow(2, sum_e(r + 1) - sum_e(l), mod) for l, r, mod in queries]
'''
LEFT_LINE = CODE.strip('\n').split('\n').index('            for _ in range(k):') + 1


CONFIG = dict(
    num=3145, title='大数组元素的乘积', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='试填法 + 前缀和 + 快速幂',
    tags=['灵神题单·位运算', '难度分 2859'],
    code=CODE,
    call='Solution().findProductsOfElements([[1, 9, 1000]])',
    expect=[512],
    views=[
        dict(type='text', h=60, size=28, fn=_txt),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('i', 'i', 'yellow'), ('k', 'k', 'pink'), ('c', 'c', 'cyan'),
           ('n', 'n', 'blue'), ('res', 'res', 'green')],
    skip=['res = n = cnt1 = sum_i = 0', 'lb = n & -n', 'sum_i += i', 'cnt1 += 1', 'return pow'],
    captions={
        'for i in range((k + 1)': lambda S, B, r: ('每一位都试过了，得到 `n = {}`'.format(S.n) if B.get('i') == S.get('i') and 'i' in B else '从高位到低位试填 `n`：这一位填 1，`ones(n)` 还 ≤ k 吗？'),
        'c = (cnt1 << i)': lambda S, B, r: f'填第 {S.i} 位新增的幂次个数：之前 {S.cnt1} 个 1 × `2^{S.i}` + 低位自己的 = ==`{S.c}`==',
        'if c <= k': lambda S, B, r: (f'`c = {S.c} ≤ k = {S.k}` → ==可以填 1==' if S.c <= S.k else f'`c = {S.c} > k = {S.k}` → 填不了，这一位是 0'),
        'k -= c': '这些幂次用掉：剩余 `k = {k}`',
        'res += (sum_i << i)': '幂次和增加 = 已填位的幂次和 × `2^i` + `sumE(2^i)`：`res = {res}`',
        'n |= 1 << i': '`n` 的第 {i} 位填 1 → `n = {n}`（{n:b}）',
        'for _ in range(k)': lambda S, B, r: (f'填完 `n = {S.n}`，还差 `k = {S.k}` 个幂次：由 `n` 的最低位补' if '_' not in B else '补完了，不再循环'),
        'res += lb.bit_length()': '最低位 `{lb}` 的幂次是 `{lb.bit_length() - 1}`，加进去：`res = {res}`',
        'n ^= lb': '去掉这个最低位：`n = {n}`',
        'return res': '前缀的幂次之和 `{res}`',
        'return [pow': '`pow(2, sum_e(r+1) − sum_e(l), mod)`：两个前缀的幂次和相减，再快速幂',
    },
    max_steps=130,
    cards=dict(
        one_liner='乘积变幂次之和，再用试填法数出前 k 个幂次',
        complexity='时间 `O(q log r)`，空间 `O(1)`',
        problem=['`big_nums` = 把 1,2,3,… 各自的==强数组==（二进制每个 1 对应的 2 的幂）依次拼接',
                 '多个查询 `[from, to, mod]`：求 `big_nums[from..to]` 的乘积 `% mod`，下标可达 `10^15`',
                 '演示：`[1, 9, 1000]` → `big_nums[1..9]` 的乘积 = `2^9 = 512`'],
        quote='由于要计算的是 bigNums 数组的元素乘积，而这些元素都是 2 的幂，所以先计算出幂次之和。……根据前缀和的思想，计算从 from 到 to 的幂次之和，等于「前 to+1 个幂次之和」减去「前 from 个幂次之和」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['元素全是 2 的幂 → 先求==幂次之和==，最后一次快速幂',
              '前 `k` 个幂次来自哪些整数？找最大的 `n` 使 `ones(n) ≤ k`：==试填法==，高位到低位逐位试 1',
              '不够的几个幂次，由 `n` 自己的低位补上'],
        summary=['时间 `O(q log r)`，空间 `O(1)`',
                 '`ones(2^i) = i·2^(i-1)`，`sumE(2^i) = i(i-1)/2 · 2^(i-1)`，代码用 `<< i >> 1` 避免 `i=0` 特判',
                 '试填时增量 = 之前填的 1 的个数 × `2^i` + 低位自己的贡献',
                 '剩余的 `k` 个幂次由 `n` 的低 `k` 个 1 补充（`n & -n` 取最低位）'],
    ),
)
