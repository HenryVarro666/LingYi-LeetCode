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


CODE = '''
class Solution(object):
    def findProductsOfElements(self, queries):

        f = [0]
        g = [1]
        for index in range(1, 5):
            f.append(f[-1] * 2 + (index << index))
            g.append(g[-1] * 2 + (1 << index))
        
        def calc(v):
            pos = []
            s = 0
            res = 0
            for index in range(4, 0, -1):
                low_cnt = (len(pos) << index) + g[index - 1]
                low_s = (s << index) + f[index - 1]
                if low_cnt < v:
                    res += low_s
                    v -= low_cnt
                    pos.append(index)
                    s += index

            if v > len(pos):
                res += s
                v -= len(pos) + 1
            if v > 0:
                res += sum(pos[-v:])

            return res

        def quick_pow(p, mod):
            if p == 0:
                return 1 % mod
            if p == 1:
                return 2 % mod
            
            x = quick_pow(p // 2, mod)
            x = x * x % mod
            if p & 1:
                x = x * 2 % mod
            return x

        return [quick_pow(calc(y + 1) - calc(x), mod) for x, y, mod in queries]
'''
_LINES = CODE.strip('\n').split('\n')
L_TAIL = _LINES.index('                v -= len(pos) + 1') + 1
L_SUM = _LINES.index('                res += sum(pos[-v:])') + 1
BANDS = [('yellow', 1), ('cyan', 2), ('pink', 3)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    N = 22
    chips = _chips(N)
    if 'pos' not in S:
        _chip_row(cv, box, T, N, 0, 0, y0 + 110, 'arr = big_nums 取 log2（每组 = 整数 x 的强数组）')
        return
    pos, g, f = S['pos'], S['g'], S['f']
    line = S.get('_line', 0)
    base = sum((j << idx) + g[idx - 1] for j, idx in enumerate(pos))
    mid = base + (len(pos) + 1 if line >= L_TAIL else 0)
    top = mid + (S['v'] if line >= L_SUM else 0)
    sx, cell = _chip_row(cv, box, T, N, base, max(mid, top), y0 + 110,
                         'arr（每组 = 整数 x 的强数组）；绿 = 已跳过的前缀，黄/橙 = 尾部补上的')
    first = {}
    for k, (x, e) in enumerate(chips):
        first.setdefault(x, k)
    yb = y0 + 110 + cell + 60
    for col, idx in BANDS:
        a, b = first.get(1 << idx), first.get((1 << (idx + 1)))
        if a is None:
            continue
        b = N if b is None else b
        X0, X1 = sx + a * cell, sx + b * cell
        cv.rect((X0 + 3, yb, X1 - 3, yb + 34), fill=T[col], alpha=90, r=8)
        cv.text(((X0 + X1) / 2, yb + 17), f'斜盖 {idx}', 20, T['text'], anchor='mm', bold=True)
    yt = yb + 100
    cv.text((x0 + 20, yt - 36), '斜盖 i = 整数 2^i .. 2^(i+1)−1 对应的那一片，长度 2^i', 22, T['muted'], anchor='lm', bold=True)
    cv.text((x0 + 20, yt), f'g = {g}   （g[i] = 前 2^(i+1)−1 个整数共多少项）', 22, T['muted'], anchor='lm', mono=True)
    cv.text((x0 + 20, yt + 36), f'f = {f}   （f[i] = 这些项的数值之和）', 22, T['muted'], anchor='lm', mono=True)
    if 'index' in S and 'low_cnt' in S and line >= L_LOW and line < L_TAIL - 1:
        cv.text((x0 + 20, yt + 90), f"index = {S['index']}：low_cnt = {S['low_cnt']}，v = {S['v']}"
                + ('  → v 在斜盖下方' if S['low_cnt'] < S['v'] else '  → v 还在上半部分'), 26, T['text'], anchor='lm', bold=True)
    cv.text((x0 + 20, yt + 140), f"pos = {pos}   s = {S['s']}   res = {S['res']}", 26, T['cyan'], anchor='lm', bold=True, mono=True)


L_LOW = _LINES.index('                low_cnt = (len(pos) << index) + g[index - 1]') + 1


def _txt(S):
    if 'v' not in S:
        return '把乘积变成 arr 的前缀和：`calc(to+1) − calc(from)`，再快速幂'
    return f'`calc(v)`：求 arr 前 `v` 个数之和；现在 `v = {S["v"]}`'


CONFIG = dict(
    num=3145, title='大数组元素的乘积', difficulty='Hard', category='位运算',
    author='yiduobo', technique='斜盖递推 f/g + 前缀和 + 快速幂',
    tags=['灵神题单·位运算', '难度分 2859'],
    code=CODE,
    call='Solution().findProductsOfElements([[1, 9, 1000]])',
    expect=[512],
    views=[
        dict(type='text', h=60, size=28, fn=_txt),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('v', 'v', 'pink'), ('pos', 'pos', 'cyan'), ('s', 's', 'blue'), ('res', 'res', 'green')],
    skip=['for index in range(4, 0, -1)', 'low_cnt = (len(pos)', 'f = [0]', 'g = [1]', 'for index in range(1, 5)', 'f.append', 'g.append', 'pos = []', 's = 0', 'res = 0',
          'low_s = (s << index)', 'v -= low_cnt', 'pos.append(index)', 's += index', 'if p == 0', 'return 1 % mod',
          'if p == 1', 'return 2 % mod', 'x = x * x % mod', 'if p & 1', 'x = x * 2 % mod'],
    captions={
        'def calc': '',
        'if low_cnt < v': lambda S, B, r: (f'斜盖 {S.index}：上方 `low_cnt = {S.low_cnt}` < `v = {S.v}` → ==v 在它之下==：跳过上半部分，`res` 加 `low_s = {S.low_s}`'
                                           if S.low_cnt < S.v else f'斜盖 {S.index}：上方 `low_cnt = {S.low_cnt}` ≥ `v = {S.v}` → v 还在上半部分'),
        'res += low_s': '`res = {res}`（上半部分的数值和累加进来）',
        'if v > len(pos)': lambda S, B, r: (f'剩下 `v = {S.v}` > `len(pos) = {len(S.pos)}` → 落在 0 所在那一行之后，补上外层斜盖整行 `s = {S.s}`' if S.v > len(S.pos)
                                              else f'剩下 `v = {S.v}` ≤ `len(pos) = {len(S.pos)}` → 还没走完一整行，不用补'),
        'res += s': '补整行：`res = {res}`',
        'v -= len(pos) + 1': '跳过上一行和 0 所在这一行：`v = {v}`',
        'if v > 0': lambda S, B, r: (f'还剩 `v = {S.v}` 项 → 它们就是外层斜盖（pos）的最后 {S.v} 项' if S.v > 0 else '正好走完，没有剩余'),
        'res += sum(pos[-v:])': '加上 `pos` 的后 `{v}` 项：`res = {res}`',
        'return res': '前缀和 `calc = {res}`',
        'return [quick_pow': '幂次 = `calc(y+1) − calc(x)`，再 `quick_pow` 算 `2^幂次 % mod`',
        'x = quick_pow(p // 2, mod)': lambda S, B, r: f'`2^{S.p} = (2^{S.p // 2})^2` ' + ('`× 2`' if S.p & 1 else '') + '：折半递归',
        'return x': '返回 `{x}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='把 arr 切成「斜盖」，用 f/g 递推出前缀和',
        complexity='时间 `O(q log r)`，空间 `O(log r)`',
        problem=['`big_nums` 由 1,2,3,… 的强数组（二进制各个 1 对应的 2 的幂）依次拼成',
                 '查询 `[from, to, mod]`：求 `big_nums[from..to]` 的乘积 `% mod`，下标最大 `10^15`',
                 '演示：`[1, 9, 1000]` → 乘积 `2^9 % 1000 = 512`'],
        quote='可以发现，当1首次出现时，可以写成一个斜盖，盖住之前出现的1；当2首次出现时，可以写成一个斜盖盖住上面出现过的0和1……其中数值index对应的斜盖长度恰好为2^index。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘积取 log2 → 前缀和，下标范围大，只能找规律',
              '按「整数第一次出现」把 arr 分成斜盖，用 `f[i] = 2f[i−1] + i·2^i`、`g[i] = 2g[i−1] + 2^i` 递推项数和数值和',
              '从大到小判断 `v` 落在哪个斜盖下，落进去就跳过上半部分，并把这个 index 记进 `pos`'],
        summary=['时间 `O(q log r)`，空间 `O(log r)`',
                 '判断要带上外层斜盖：`low_cnt = g[index−1] + len(pos)·2^index`',
                 '循环后可能刚好落在外层斜盖上：`v > len(pos)` 补一整行，再加 `pos` 的最后 `v` 项',
                 '为了演示，把预处理和循环范围 `range(1, 46)` / `range(45, 0, -1)` 改成 `range(1, 5)` / `range(4, 0, -1)`（演示查询下标只到 10）；原文代码在 Python 3 下无需其他改动（整除已是 `//`）'],
    ),
)
