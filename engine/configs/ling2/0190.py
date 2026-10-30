N = 43261596
MASKS = [0x55555555, 0x33333333, 0x0f0f0f0f, 0x00ff00ff, 0x0000ffff]
MASK_NAMES = ['m0 = 0x55555555', 'm1 = 0x33333333', 'm2 = 0x0f0f0f0f', 'm3 = 0x00ff00ff', 'm4 = 0x0000ffff']
STEP_NAME = ['交换相邻位（块长 1）', '两个两个交换（块长 2）', '四个四个交换（块长 4）', '八个八个交换（块长 8）', '交换高低 16 位（块长 16）']
BYTE_COL = ['blue', 'pink', 'green', 'orange']


def _row(cv, T, x, y, cell, val, level, label, dim_zero=False, mask=False):
    cv.text((x, y), label, 22, T['muted'], bold=True)
    y += 32
    for d in range(32):
        b = 31 - d                      # 第 d 个格子是第 b 位
        bit = val >> b & 1
        X = x + d * cell
        if mask:
            fill = T['yellow'] if bit else T['panel2']
            tc = T['bg'] if bit else T['dim']
        else:
            ob = b ^ ((1 << level) - 1)  # 这一位最初来自第 ob 位
            fill = T[BYTE_COL[ob // 8]]
            fill = fill if bit else tuple(int(c * 0.35 + 22 * 0.65) for c in fill)
            tc = T['bg'] if bit else T['text']
        cv.rect((X + 1, y, X + cell - 1, y + 40), fill=fill, r=4)
        cv.text((X + cell / 2, y + 20), bit, 20, tc, anchor='mm', bold=True, mono=True)
    return y + 40


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ln = S.get('_line')
    if ln not in (8, 9, 10, 11, 12):
        return
    k = ln - 8
    before = B['n']
    after = S['n'] if ln < 12 else (before >> 16 | (before & MASKS[4]) << 16)
    cell = (x1 - x0 - 40) / 32
    x = x0 + 20
    cv.text((x, y0 + 4), f'第 {k + 1} 层：{STEP_NAME[k]}', 26, T['text'], bold=True)
    y = _row(cv, T, x, y0 + 52, cell, before, k, f'执行前 n = {before}（颜色 = 这一位原来在哪个字节）')
    # 交换的块：每 2*bs 位一组，组内左右两块互换
    bs = 1 << k
    for g in range(0, 32, 2 * bs):
        gx0, gx1 = x + g * cell + 3, x + (g + 2 * bs) * cell - 3
        mid = x + (g + bs) * cell
        cv.line([(gx0, y + 8), (gx0, y + 14), (gx1, y + 14), (gx1, y + 8)], T['muted'], 2)
        if bs >= 2:
            cv.line([(mid, y + 4), (mid, y + 18)], T['muted'], 2)
    y = _row(cv, T, x, y + 28, cell, MASKS[k], 0, f'掩码 {MASK_NAMES[k]}（黄 = 1）', mask=True)
    y = _row(cv, T, x, y + 22, cell, after, k + 1, f'执行后 n = {after}' + ('（这就是答案）' if ln == 12 else ''))
    yy = y + 22
    cv.rich(x, yy, f'`n>>{bs} & m` 把每组的高块挪到低块，`(n & m)<<{bs}` 把低块挪到高块，`|` 合并', x1 - x0 - 40, size=24)
    cx = x
    for i, c in enumerate(BYTE_COL):
        cv.rect((cx, yy + 62, cx + 26, yy + 86), fill=T[c], r=4)
        cv.text((cx + 34, yy + 74), f'原 bit {i * 8}–{i * 8 + 7}', 20, T['muted'], anchor='lm')
        cx += 200
    _row(cv, T, x, yy + 110, cell, N, 0, f'对照：原始输入 n = {N}（5 层之后，每个颜色块整体倒到了对称位置）')


CONFIG = dict(
    num=190, title='颠倒二进制位', difficulty='Easy', category='技巧',
    author='灵茶山艾府', technique='位运算分治 · O(1)',
    tags=['面试经典150'],
    code='''
m0 = 0x55555555  # 01010101 ...
m1 = 0x33333333  # 00110011 ...
m2 = 0x0f0f0f0f  # 00001111 ...
m3 = 0x00ff00ff  # 00000000111111110000000011111111
m4 = 0x0000ffff  # 00000000000000001111111111111111
class Solution:
    def reverseBits(self, n: int) -> int:
        n = n>>1&m0 | (n&m0)<<1  # 交换相邻位
        n = n>>2&m1 | (n&m1)<<2  # 两个两个交换
        n = n>>4&m2 | (n&m2)<<4  # 四个四个交换
        n = n>>8&m3 | (n&m3)<<8  # 八个八个交换
        return n>>16 | (n&m4)<<16  # 交换高低 16 位
''',
    call=f'Solution().reverseBits({N})',
    expect=964176192,
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('n', 'n', 'blue')],
    captions={
        'n = n>>1&m0': '==交换相邻位==：`m0 = 0101…` 选出偶数位；奇数位右移 1、偶数位左移 1，`|` 合并 → `{n}`',
        'n = n>>2&m1': '==两个两个交换==：`m1 = 0011…` 选出每 4 位的低 2 位，高低两块互换 → `{n}`',
        'n = n>>4&m2': '==四个四个交换==：`m2 = 00001111…`，每个字节的高低 4 位互换 → `{n}`',
        'n = n>>8&m3': '==八个八个交换==：`m3 = 0x00ff00ff`，每 16 位里的两个字节互换 → `{n}`',
        'return n>>16': '最后==交换高低 16 位==：`n>>16` 取高半，`(n&m4)<<16` 把低半搬上去 → =={ret}==',
    },
    cards=dict(
        one_liner='分治反转：相邻位、两两、四四、八八、高低 16 位依次交换',
        complexity='时间 `O(log W)` = `O(1)`，`W = 32`；空间 `O(1)`',
        problem=['颠倒给定的 32 位整数的二进制位',
                 '`43261596` = `00000010100101000001111010011100`',
                 '→ `964176192` = `00111001011110000010100101000000`'],
        before=[dict(heading='分治：以 8 位 12345678 为例', lines=[
            '反转 `12345678` = 反转左半 `1234 → 4321`，反转右半 `5678 → 8765`，再==交换两半==',
            '去掉「递」只看「归」（自底向上）：`12345678`',
            '两两交换 → `21436587`；两个两个交换 → `43218765`；四个四个交换 → `87654321`',
            '32 位整数再多两层：八个八个交换，最后交换高低 16 位'])],
        quote='利用位运算「并行计算」的特点，我们可以高效地实现上述过程。去掉递归的「递」，直接看「归」的过程（自底向上）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一层的所有交换==同时完成==：用掩码分离 → 移位 → 合并',
              '`n>>1 & m0`：奇数位挪到偶数位；`(n & m0) << 1`：偶数位挪到奇数位',
              '5 层就把 32 位完全倒过来，计算量和输入无关'],
        result='`43261596` → `964176192` ✓ 只用了 5 行位运算',
        summary=['时间 `O(log W)`，`W = 32`：输入是 0 还是 `2³¹ − 2` 计算量都一样',
                 '掩码：`0x55…`=0101，`0x33…`=0011，`0x0f…`=00001111，`0x00ff00ff`，`0x0000ffff`',
                 '易错：先移位再与掩码，`n>>1&m0` 等价于 `(n >> 1) & m0`（移位优先级更高）',
                 '库函数替代：`int(f\'{n:032b}\'[::-1], 2)`（字符串反转）'],
    ),
)
