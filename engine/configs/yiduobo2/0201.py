def _row(cv, T, x, y, val, nb, cell, label, lab_color, colors=None, note=None):
    cv.text((x - 16, y + cell / 2), label, 24, lab_color, anchor='rm', mono=True, bold=True)
    s = format(val, f'0{nb}b')
    for k, ch in enumerate(s):
        X = x + k * cell
        c = (colors or {}).get(k)
        cv.rect((X + 2, y + 2, X + cell - 2, y + cell - 4), fill=c or T['panel2'], r=6, outline=T['border'])
        cv.text((X + cell / 2, y + cell / 2 - 1), ch, 26, T['bg'] if c else T['text'], anchor='mm', mono=True, bold=True)
    cv.text((x + nb * cell + 16, y + cell / 2), note or f'= {val}', 22, T['muted'], anchor='lm', mono=True)


def _lcp(a, b, nb):
    sa, sb = format(a, f'0{nb}b'), format(b, f'0{nb}b')
    k = 0
    while k < nb and sa[k] == sb[k]:
        k += 1
    return k


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'm' not in S:
        return
    m, n = S['m'], S['n']
    nb = 6
    cell = 50
    x = x0 + 220
    y = y0 + 30
    cv.text((x0 + 18, y0 + 4), '每次去掉 n 最低位的 1，直到 n ≤ m', 23, T['muted'], bold=True)
    y += 30
    k = _lcp(m, n, nb)
    green = {i: (30, 110, 60) for i in range(k)}
    _row(cv, T, x, y, m, nb, cell, 'm', T['blue'], colors=dict(green) if n <= m else None)
    y += cell + 10
    bn = B.get('n')
    line = S.get('_line')
    if line == 4 and isinstance(bn, int) and bn != n:
        low = (bn & -bn).bit_length() - 1
        pos = nb - 1 - low
        _row(cv, T, x, y, bn, nb, cell, 'n（之前）', T['muted'], colors={pos: T['red']},
             note=f'= {bn}，最低位的 1 在这')
        y += cell + 10
        _row(cv, T, x, y, bn - 1, nb, cell, 'n - 1', T['muted'], note=f'= {bn - 1}（最低位 1 变 0，后面变 1）')
        y += cell + 10
    cols = {}
    if n <= m:
        cols = dict(green)
    _row(cv, T, x, y, n, nb, cell, 'n', T['pink'], colors=cols)
    y += cell + 30
    if n <= m:
        cv.line([(x0 + 20, y - 12), (x1 - 20, y - 12)], T['border'], 2)
        cv.rich(x0 + 30, y, f'`n` 变成 ==公共前缀 XX + 全 0==，`m` 是 XX + YY', x1 - x0 - 60, size=26)
        y += 50
        cv.rich(x0 + 30, y, f'`m & n` 只留下 XX：`{m:06b} & {n:06b}` = =={m & n}==', x1 - x0 - 60, size=26)
    else:
        cv.rich(x0 + 30, y, f'`m = {m} < n = {n}`：n 的低位还和 m 不同 → 继续去掉最低位的 1', x1 - x0 - 60, size=26)


CONFIG = dict(
    num=201, title='数字范围按位与', difficulty='Medium', category='技巧',
    author='yiduobo', technique='n &= n - 1 去掉最低位的 1',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def rangeBitwiseAnd(self, m, n):
        while m < n:
            n &= n - 1

        return m & n
''',
    call='[Solution().rangeBitwiseAnd(50, 54), Solution().rangeBitwiseAnd(5, 7)]',
    expect=[48, 4],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('m', 'm', 'blue'), ('n', 'n', 'pink'), ('m (二进制)', "format(m, '06b')", 'blue'),
           ('n (二进制)', "format(n, '06b')", 'pink')],
    captions={
        'while m < n': lambda S, B, ret: (f'`m = {B.m} < n = {B.n}`：n 比 m 大，二者的低位还不一样 → 继续'
                                          if B.m < B.n else
                                          f'`n = {B.n} ≤ m = {B.m}`：n 已经缩到 m 以下 → 停'),
        'n &= n - 1': lambda S, B, ret: (f'`n & (n - 1)` ==去掉 n 最低位的 1==：`{B.n:06b}` → `{S.n:06b}`'
                                         f'（{B.n} → {S.n}）'),
        'return m & n': lambda S, B, ret: (f'此时 n 是「公共前缀 + 全 0」，`m & n = {S.m:06b} & {S.n:06b}` → 返回 =={ret}=='),
    },
    cards=dict(
        one_liner='连续区间的按位与 = m 和 n 的最长公共前缀',
        complexity='时间 `O(log n)`（最多 31 次），空间 `O(1)`',
        problem=['给你 `m ≤ n`（原题叫 `left`、`right`），返回 `[m, n]` 内==所有数字按位与==的结果',
                 '示例：`5, 7` → `4`（`101 & 110 & 111 = 100`）',
                 '本视频：`50, 54` → `48`，再跑一遍 `5, 7`'],
        quote='题目要求m到n的按位与，实际上就是求==m到n在二进制表示下的最长公共前缀==。……我在这里的做法是==不断去除n的最低位1，直到n小于等于m==。',
        quote_src='—— yiduobo 题解原文',
        idea=['m 到 n 是连续的 → 区间内所有数的公共前缀 = m 和 n 的公共前缀',
              '`n &= n - 1` 每次去掉 n 最低位的 1；当 `n ≤ m` 时 n 变成 `XX…X000…0`',
              '而 m 是 `XX…XYYY…Y`，二者 XX 部分相同 → 最后 `m & n` 取出 XX'],
        result='`[50, 54]` → `48`，`[5, 7]` → `4` ✓',
        summary=['时间 `O(log n)`：每次至少去掉一个 1；空间 `O(1)`',
                 '为什么停在 `n ≤ m`？再去掉的就是 m 和 n 不同的那些低位',
                 '另一种做法：m、n 同时右移直到相等，记下位数再左移回去',
                 '对比灵神：灵神用 `(left ^ right).bit_length()` 一步算出要清零的长度，`O(1)`',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码未改'],
    ),
)
