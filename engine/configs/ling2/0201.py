def _bits_row(cv, T, x, y, val, nb, cell, prefix_len, label, lab_color, hi_low=None, bold_prefix=True, note=None):
    cv.text((x - 16, y + cell / 2), label, 22, lab_color, anchor='rm', mono=True, bold=True)
    s = format(val, f'0{nb}b')
    for k, ch in enumerate(s):
        X = x + k * cell
        in_prefix = prefix_len is not None and k < prefix_len
        fill = T['panel2']
        tc = T['text']
        if in_prefix and bold_prefix:
            fill = (30, 70, 45)
            tc = T['green']
        elif hi_low is not None and not in_prefix:
            fill = hi_low
            tc = T['bg']
        cv.rect((X + 2, y + 2, X + cell - 2, y + cell - 4), fill=fill, r=6, outline=T['border'])
        cv.text((X + cell / 2, y + cell / 2 - 1), ch, 24, tc, anchor='mm', mono=True, bold=True)
    cv.text((x + nb * cell + 16, y + cell / 2), note or f'= {val}', 22, T['muted'], anchor='lm', mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'left' not in S:
        return
    L, R = S['left'], S['right']
    nb = max(3, R.bit_length())
    m = S.get('m')
    line = S.get('_line')
    cell = 44
    x = x0 + 230
    y = y0 + 20
    cv.text((x0 + 18, y0 + 4), f'[{L}, {R}] 中所有数的二进制（绿 = 公共前缀）', 23, T['muted'], bold=True)
    y += 34
    plen = nb - m if m is not None else None
    for v in range(L, R + 1):
        lab = 'left' if v == L else ('right' if v == R else '')
        c = T['blue'] if v == L else (T['pink'] if v == R else T['muted'])
        _bits_row(cv, T, x, y, v, nb, cell, plen, lab, c)
        y += cell + 2
        if y > y0 + 300:
            break
    if m is None:
        return
    y += 14
    cv.line([(x0 + 20, y - 6), (x1 - 20, y - 6)], T['border'], 2)
    y += 8
    xr = L ^ R
    _bits_row(cv, T, x, y, xr, nb, cell, None, 'left ^ right', T['yellow'])
    first = nb - xr.bit_length()
    if 0 <= first < nb:
        X = x + first * cell
        cv.rect((X, y, X + cell, y + cell - 2), outline=T['yellow'], width=3, r=6)
    cv.text((x0 + 30, y + cell + 14), f'XOR 的最高位 1 = 第一个不同的位置 → 长度 m = {m}，后 {m} 位要置 0', 22, T['yellow'])
    y += cell + 54
    if line == 4:
        mask = ~((1 << m) - 1) & ((1 << nb) - 1)
        _bits_row(cv, T, x, y, mask, nb, cell, None, '~((1<<m)-1)', T['cyan'], note=f'高位全 1，低 {m} 位是 0')
        y += cell + 4
        _bits_row(cv, T, x, y, L & mask, nb, cell, nb - m, 'left & 它', T['green'], hi_low=None)
        y += cell + 6
        cv.rich(x0 + 30, y + 4, f'答案 = 公共前缀，后 {m} 位补 0 = =={L & mask}==', x1 - x0 - 60, size=26)


CONFIG = dict(
    num=201, title='数字范围按位与', difficulty='Medium', category='技巧',
    author='灵茶山艾府', technique='位运算 · 公共前缀 O(1)',
    tags=['面试经典150'],
    code='''
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        m = (left ^ right).bit_length()
        return left & ~((1 << m) - 1)
''',
    call='[Solution().rangeBitwiseAnd(50, 54), Solution().rangeBitwiseAnd(5, 7)]',
    expect=[48, 4],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('left ^ right', 'left ^ right', 'yellow'),
           ('m', 'm', 'cyan')],
    captions={
        'm = (left ^ right)': lambda S, B, ret: (
            f'`{S.left} ^ {S.right} = {S.left ^ S.right:b}`：XOR 里最高位的 1 就是==从左往右第一个不同的位置==，'
            f'它的长度 `m = {S.m}`'),
        'return left &': lambda S, B, ret: (
            f'`(1 << {S.m}) - 1` 是低 {S.m} 位全 1，取反后与 `left` → ==去掉低 {S.m} 位==，'
            f'只留公共前缀：返回 =={ret}=='),
    },
    cards=dict(
        one_liner='区间内所有数的 AND = left 和 right 的公共前缀，后面补 0',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你 `left ≤ right`，返回区间 `[left, right]` 内==所有数字按位与==的结果',
                 '示例：`left = 5, right = 7` → `4`（`101 & 110 & 111 = 100`）',
                 '数据范围：`0 ≤ left ≤ right ≤ 2^31 − 1`，不能逐个与'],
        before=[dict(heading='举例：left = 110010，right = 110110', lines=[
            '区间里的数：`110010` `110011` `110100` `110101` `110110`',
            '公共前缀都是 `110`',
            '后三位：既有 `110011` 又有 `110100` → 每一位都出现过 0 → ==AND 一定是 0==',
            '所以答案是 `110000`：把 left 的后三位置 0'])],
        quote='注意 110==0==10 和 110==1==10 画下划线的地方，这是它们俩从左往右看，首次不同的位置。这可以通过计算 left 和 right 的 ==XOR== 得到，即 100。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`m = (left ^ right).bit_length()`：需要置 0 的长度',
              '低 `m` 位组成的集合是 `2^m − 1`，用 `& ~(2^m − 1)` 把它们去掉',
              '答案 `left & ~((1 << m) - 1)`，一步算完'],
        result='`[50, 54]` → `48`，`[5, 7]` → `4` ✓',
        summary=['时间、空间 `O(1)`：只用了 XOR、`bit_length` 和掩码',
                 '为什么低位全是 0？区间必含 `前缀0111…` 和 `前缀1000…`，低位每一位都出现过 0',
                 '`left == right` 时 `m = 0`，掩码是全 1，直接返回 left',
                 '思考题：区间 OR 见 CF1981B，区间 XOR 见 1486'],
    ),
)
