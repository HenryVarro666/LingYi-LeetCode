L_DEC, L_CNT, L_SUB, L_MUL, L_LEN, L_X, L_TAIL, L_RET = 3, 6, 8, 9, 10, 13, 16, 17


def _sub(S):
    """已经从 n 里减掉的位数（不含开头的 -1）"""
    length, cnt, line = S['length'], S['cnt'], S.get('_line')
    sub = sum(9 * 10 ** (l - 1) * l for l in range(1, length))
    if line == L_SUB:
        sub += cnt * length
    elif line == L_MUL:
        sub += cnt // 10 * length
    return sub


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S:
        return
    line = S.get('_line')
    if 'cnt' not in S:
        n0 = S['n'] + 1
        cv.text((x0 + 18, y0 + 4), f'序列 1 2 3 … 9 10 11 …：求第 {n0} 位数字', 23, T['muted'], bold=True)
        cv.rich(x0 + 30, y0 + 70, f'`n -= 1` → `{S["n"]}`：改成==从 0 开始==数，后面的除法、取模更顺', x1 - x0 - 60, size=28)
        return
    sub = _sub(S)
    n0 = S['n'] + sub + 1
    cv.text((x0 + 18, y0 + 4), f'求第 {n0} 位数字（从 0 开始是第 {n0 - 1} 位）', 23, T['muted'], bold=True)
    y = y0 + 50
    length, cnt = S['length'], S['cnt']
    if line == L_MUL:
        length_done = length
    elif line == L_SUB:
        length_done = length
    else:
        length_done = length - 1
    for l in range(1, 5):
        c = 9 * 10 ** (l - 1)
        Y = y + (l - 1) * 74
        done = l <= length_done
        cur = (l == length and not done)
        fill = (30, 70, 45) if done else ((70, 60, 25) if cur else T['panel2'])
        cv.rect((x0 + 30, Y, x1 - 30, Y + 62), fill=fill, r=10, outline=T['yellow'] if cur else T['border'],
                width=3 if cur else 1)
        lo, hi = 10 ** (l - 1), 10 ** l - 1
        cv.text((x0 + 50, Y + 31), f'{l} 位数', 26, T['green'] if done else (T['yellow'] if cur else T['muted']),
                anchor='lm', bold=True)
        cv.text((x0 + 170, Y + 31), f'{lo}~{hi}：{c} 个 × {l} = {c * l} 位', 24, T['text'] if (done or cur) else T['dim'],
                anchor='lm', mono=True)
        tag = '跳过 ✓' if done else (('答案在这里' if cnt * length > S['n'] else '比较 cnt·length 和 n') if cur else '')
        if tag:
            cv.text((x1 - 50, Y + 31), tag, 24, T['green'] if done else T['yellow'], anchor='rm', bold=True)
    y += 4 * 74 + 10
    if line in (L_SUB, L_MUL):
        cv.rich(x0 + 30, y, f'减掉 {length} 位数这一组后，还要往后数 `n = {S["n"]}` 位', x1 - x0 - 60, size=26)
    else:
        cv.rich(x0 + 30, y, f'剩下 `n = {S["n"]}`：去长为 `length = {length}` 的数里，数第 `{S["n"]}` 位（从 0 数）',
                x1 - x0 - 60, size=26)
    y += 56
    if 'x' in S:
        xv = S['x']
        k = S['n'] % length
        cv.rich(x0 + 30, y, f'第 `{S["n"]} // {length} = {S["n"] // length}` 个 {length} 位数：`x = {cnt // 9} + {S["n"] // length} = {xv}`',
                x1 - x0 - 60, size=26)
        y += 56
        s = str(xv)
        cw = 70
        sx = x0 + 60
        for i, ch in enumerate(s):
            X = sx + i * cw
            hit = i == k
            cv.rect((X, y, X + cw - 8, y + 66), fill=T['yellow'] if hit else T['panel2'], r=10, outline=T['border'])
            cv.text((X + (cw - 8) / 2, y + 33), ch, 34, T['bg'] if hit else T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + (cw - 8) / 2, y + 72), i, 18, T['dim'], anchor='mt', mono=True)
        cv.text((sx + len(s) * cw + 16, y + 33), f'← 从高到低第 n % length = {k} 个', 24, T['yellow'], anchor='lm')


CONFIG = dict(
    num=400, title='第 N 位数字', difficulty='Medium', category='数学',
    author='灵茶山艾府', technique='按位数分组 · 逐组减去',
    tags=['字节30天'],
    code='''
class Solution:
    def findNthDigit(self, n: int) -> int:
        n -= 1  # n 改成从 0 开始，方便计算

        # 十进制长为 length 的正整数有 cnt = 9 * 10**(length-1) 个
        cnt, length = 9, 1
        while cnt * length <= n:
            n -= cnt * length  # 这里减小了 n
            cnt *= 10
            length += 1

        # 答案在正整数 x 中
        x = cnt // 9 + n // length

        # 计算 x 从高到低第 n%length（从 0 开始）个数字
        tail = 10 ** (length - n % length - 1)
        return x // tail % 10
''',
    call='[Solution().findNthDigit(11), Solution().findNthDigit(195)]',
    expect=[0, 1],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('n', 'n', 'yellow'), ('cnt', 'cnt'), ('length', 'length', 'cyan'), ('cnt*length', 'cnt * length'),
           ('x', 'x', 'green'), ('tail', 'tail')],
    captions={
        'n -= 1': '`n` 改成从 0 开始：`n = {n}`',
        'cnt, length = 9, 1': '1 位数有 `cnt = 9` 个；一般地，长为 length 的数有 `9 · 10^(length−1)` 个',
        'while cnt * length': lambda S, B, ret: (
            f'长为 {B.length} 的数一共 `{B.cnt} × {B.length} = {B.cnt * B.length}` 位 `≤ n = {B.n}` → ==答案不在这一组==，整组跳过'
            if B.cnt * B.length <= B.n else
            f'`{B.cnt} × {B.length} = {B.cnt * B.length} > n = {B.n}` → ==答案就在长为 {B.length} 的数里=='),
        'n -= cnt * length': '减去这一组的位数：`n = {B.n} − {cnt * length} = {n}`',
        'cnt *= 10': '下一组的个数 ×10：`cnt = {cnt}`',
        'length += 1': '长度 +1：`length = {length}`',
        'x = cnt // 9': '每个数占 `{length}` 位 → 答案在第 `n // length = {n // length}` 个 {length} 位数里：`x = {cnt // 9} + {n // length} = {x}`',
        'tail = 10': '要的是 x 从高到低第 `n % length = {n % length}` 位 → 去掉后面 `{length - n % length - 1}` 位：`tail = {tail}`',
        'return x // tail': '`{x} // {tail} % 10` = =={ret}==',
    },
    cards=dict(
        one_liner='按位数分组，整组整组地跳过，最后定位到某个数的某一位',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['在无限序列 `1 2 3 4 5 6 7 8 9 10 11 …` 中，找第 `n` 位上的数字',
                 '示例：`n = 3` → `3`；`n = 11` → `0`（是 10 的 `0`）',
                 '本视频：`n = 11` 和 `n = 195`'],
        quote='十进制长为 length 的正整数，最高位不能填 0，有 9 种填法，其余 length−1 位有 10 种填法。根据乘法原理，十进制长为 length 的正整数个数为 ==cnt = 9·10^(length−1)==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长为 length 的数共 `cnt · length` 位：只要 `≤ n`，就整组减掉',
              '`n` 先减 1 改成从 0 开始：第 `n // length` 个数 `x = 10^(length−1) + n // length`',
              '答案是 x 从高到低第 `n % length` 位：`x // 10^(length − n%length − 1) % 10`'],
        result='`n = 11` → `0`，`n = 195` → `1` ✓',
        summary=['时间 `O(log n)`：每组长度 +1，最多十来组',
                 '易错：一开始 `n -= 1`，否则 `n // length` 和 `n % length` 都要 ±1',
                 '`cnt // 9 = 10^(length−1)` 就是这一组的第一个数',
                 '相似题：4022. 无限字符串里第 K 个数字'],
    ),
)
