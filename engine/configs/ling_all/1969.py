def _bin(v, p):
    return format(v, '0%db' % p)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = S['p']
    N = (1 << p) - 1
    half = 1 << (p - 1)
    k = S.get('k')
    cv.text((x0 + 18, y0 + 4), f'nums = 1 ~ 2^p−1 = 1 ~ {N}（青 = 小于 2^(p−1)，橙 = 其余，黄 = 全 1 的 {N}）', 22, T['muted'], bold=True)
    cell = min(112, (x1 - x0 - 40) / N)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * N) / 2
    ys = y0 + 56
    for v in range(1, N + 1):
        X = sx + (v - 1) * cell
        col = T['yellow'] if v == N else (T['cyan'] if v < half else T['orange'])
        cv.rect((X + 4, ys, X + cell - 4, ys + 92), fill=col, alpha=60 if k is not None and v != N else 255, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + 30), v, 32, T['text'] if k is not None and v != N else T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ys + 68), _bin(v, p), 22, T['muted'] if k is not None and v != N else T['bg'], anchor='mm', mono=True)
    if k is None:
        cv.text(((x0 + x1) / 2, ys + 200), '交换后会变成什么样？每个数对里把 1 都集中到一个数上', 28, T['muted'], anchor='mm')
        return
    pairs = half - 1
    cv.text((x0 + 18, ys + 130), f'配对：和为 {N} 的两个数，二进制互补（一个是 0，另一个必是 1）→ 全部交换到一边', 22, T['muted'], bold=True)
    pw = min(300, (x1 - x0 - 40) / max(pairs, 1) - 16)
    py = ys + 160
    tot = (pw + 16) * pairs - 16
    px0 = (x0 + x1) / 2 - tot / 2
    for i in range(1, pairs + 1):
        a, b = i, N - i
        X = px0 + (i - 1) * (pw + 16)
        cv.rect((X, py, X + pw, py + 250), fill=T['panel2'], r=14, outline=T['border'])
        cv.text((X + pw / 2, py + 32), f'{b} + {a} = {N}', 26, T['text'], anchor='mm', bold=True)
        cv.text((X + pw / 2, py + 78), f'{_bin(b, p)}  {_bin(a, p)}', 26, T['muted'], anchor='mm', mono=True)
        cv.arrow((X + pw / 2, py + 100), (X + pw / 2, py + 138), T['green'])
        cv.text((X + pw / 2, py + 170), f'{_bin(N - 1, p)}  {_bin(1, p)}', 26, T['green'], anchor='mm', mono=True, bold=True)
        cv.text((X + pw / 2, py + 218), f'乘积 {N - 1} × 1 = {N - 1}', 26, T['green'], anchor='mm', bold=True)
    cv.text(((x0 + x1) / 2, py + 285), f'{pairs} 对各乘 {N - 1}，再乘落单的 {N}：`{N} × {N - 1}^{pairs}`'.replace('`', ''), 30, T['yellow'], anchor='mm', bold=True)
    if 'MOD' in S and S.get('_line') == 5:
        val = N * (N - 1) ** pairs
        cv.text(((x0 + x1) / 2, py + 330), f'= {val}（取模前）', 28, T['text'], anchor='mm', bold=True)


def _text(S):
    if 'k' not in S:
        return '交换位只会让两数乘积变小：==把 1 集中到一个数，另一个只剩最低位 1=='
    k = S['k']
    return f'`k = 2^p − 1 = {k}`，最小乘积 = `k × (k−1)^(k>>1)` = `{k} × {k - 1}^{k >> 1}`'


CONFIG = dict(
    num=1969, title='数组元素的最小非零乘积', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='数对构造 + 快速幂',
    tags=['难度分 1967'],
    code='''
class Solution:
    def minNonZeroProduct(self, p: int) -> int:
        MOD = 1_000_000_007
        k = (1 << p) - 1
        return k * pow(k - 1, k >> 1, MOD) % MOD
''',
    call='Solution().minNonZeroProduct(3)',
    expect=1512,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=['p', 'k', ('MOD', 'MOD', 'blue')],
    captions={
        'MOD =': '答案要对 `10^9 + 7` 取余',
        'k = (1 << p) - 1': '`k = 2^p − 1 = {k}`：数组里最大的数，二进制全是 1',
        'return k *': '最小乘积 = `{k}` × `{k-1}^{k>>1}`，指数 `k>>1 = 2^(p−1)−1 = {k>>1}` 就是数对个数 → 取余后 =={ret}==',
    },
    cards=dict(
        one_liner='把每对互补的数交换成 2^p−2 和 1，乘积最小',
        complexity='时间 `O(p)`，空间 `O(1)`',
        problem=['数组含 `[1, 2^p−1]` 里的所有整数，可以交换任意两数的同一位',
                 '求能得到的最小非零乘积，对 `10^9+7` 取余',
                 '示例：`p = 3` → `1512`'],
        quote='例如 x=1000, y=0111，如果把 y 中最低位以外的 1 全部给 x，那么 x\'=1110, y\'=0001，这样两数乘积最小且非零。',
        quote_src='—— 灵茶山艾府题解',
        before=[dict(heading='为什么交换变小', lines=['交换 x 的 0 位与 y 的 1 位（位值 `2^k`）',
                                                    '乘积从 `x·y\'+x·2^k` 变成 `x·y\'+y\'·2^k`',
                                                    '只要 `x > y\'` 就变小 → 把 y 的 1 不断给 x，直到 y 只剩 1'])],
        idea=['按 `2^(p−1)` 分成 A、B 两组：除 `2^p−1` 外，B 里每个数和 A 里一个数和为 `2^p−1`',
              '每对互补，可以完美交换成 `2^p−2` 和 `1`，一共 `2^(p−1)−1` 对',
              '最小乘积 `(2^p−1)·(2^p−2)^(2^(p−1)−1)`，幂用快速幂'],
        summary=['时间 `O(p)`，空间 `O(1)`',
                 '`2^(p−1)−1` 的二进制全是 1，所以等于 `k >> 1`',
                 '易错点：要用取模前的大小比较来构造，取模只能最后做（用 `pow` 带模）',
                 '易错点：`p = 1` 时 `k = 1`，`pow(0, 0, MOD) = 1`，答案 1'],
    ),
)
