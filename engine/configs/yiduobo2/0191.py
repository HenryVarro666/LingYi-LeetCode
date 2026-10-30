N = 0b10110100  # 180
W = 8


def _bits(x):
    return [(x >> (W - 1 - k)) & 1 for k in range(W)]  # 高位在左


def _low(x):
    return (x & -x).bit_length() - 1 if x else -1


def _row(cv, T, x, y, cell, label, val, colors, note=''):
    cv.text((x - 20, y + cell / 2), label, 28, T['muted'], anchor='rm', bold=True, mono=True)
    for k, b in enumerate(_bits(val)):
        pos = W - 1 - k
        c = colors(pos, b)
        X = x + k * cell
        cv.rect((X + 3, y + 3, X + cell - 3, y + cell - 3), fill=T[c] if c else T['panel2'], r=8,
                outline=T['border'], width=1)
        cv.text((X + cell / 2, y + cell / 2), b, 34, T['bg'] if c else (T['text'] if b else T['dim']),
                anchor='mm', bold=True, mono=True)
    cv.text((x + W * cell + 18, y + cell / 2), f'= {val}' + note, 26, T['muted'], anchor='lm', mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S:
        return
    cell = 78
    x = x0 + 230
    cv.text((x0 + 18, y0 + 4), '二进制（高位在左；黄 = 最低位的 1，粉 = 它右边的位）', 24, T['muted'], bold=True)
    for k in range(W):
        cv.text((x + k * cell + cell / 2, y0 + 50), f'2^{W - 1 - k}', 18, T['dim'], anchor='mm', mono=True)
    y = y0 + 72
    if S.get('_line') == 6 and 'n' in B:
        n0 = B['n']
        p = _low(n0)
        _row(cv, T, x, y, cell, 'n', n0,
             lambda pos, b: 'yellow' if pos == p else ('cyan' if pos < p else ('green' if b else None)))
        _row(cv, T, x, y + cell + 24, cell, 'n - 1', n0 - 1,
             lambda pos, b: 'pink' if pos <= p else ('green' if b else None))
        cv.line([(x - 200, y + 2 * cell + 36), (x + W * cell + 160, y + 2 * cell + 36)], T['border'], 2)
        _row(cv, T, x, y + 2 * cell + 48, cell, 'n&(n-1)', S['n'],
             lambda pos, b: None if pos <= p else ('green' if b else None))
        cv.text((x, y + 3 * cell + 62), '左边的 X 部分不变，最低位的 1 及其右边全变成 0', 24, T['yellow'], bold=True)
    else:
        _row(cv, T, x, y, cell, 'n', S['n'], lambda pos, b: 'green' if b else None)
        if S['n']:
            p = _low(S['n'])
            X = x + (W - 1 - p) * cell + cell / 2
            cv.tri_up(X, y + cell + 10, 10, T['yellow'])
            cv.text((X, y + cell + 26), '最低位的 1', 22, T['yellow'], anchor='mt', bold=True)


def _cap_and(S, B, ret):
    p = _low(B.n)
    tail = f'后面 {p} 个 0 变成 1' if p else '后面没有 0'
    return f'`n - 1`：最低位的 1 变成 0，{tail}；与 `n` 相与 → `{B.n} & {B.n - 1} = {S.n}`，==恰好划掉一个 1=='


CONFIG = dict(
    num=191, title='位1的个数', difficulty='Easy', category='技巧',
    author='yiduobo', technique='n &= n - 1 每次划掉最低位的 1',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def hammingWeight(self, n):
        res = 0
        while n:
            res += 1
            n &= n - 1

        return res
''',
    call=f'Solution().hammingWeight({N})',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=lambda S: f"`res = {S['res']}`，`n` 中还有 `{bin(S['n']).count('1')}` 个 1"
             if 'res' in S else '', h=70, size=30),
    ],
    watch=[('n', 'n'), ('bin(n)', 'bin(n)', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`n = {n}`，二进制 `{bin(n)[2:]}`；`res` 统计划掉了几个 1',
        'while n': lambda S, B, ret: (f'`n = {B.n} ≠ 0`：至少还有一位是 1' if B.n else '`n = 0`：所有的 1 都划掉了'),
        'res += 1': '每轮恰好划掉一个 1 → 先计数：`res = {res}`',
        'n &= n - 1': _cap_and,
        'return res': '循环了几轮就有几个 1 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='n &= n - 1 每次划掉最低位的 1，循环几次就有几个 1',
        complexity='时间 `O(1 的个数)`（不超过 32），空间 `O(1)`',
        problem=['给一个正整数 `n`，返回其二进制表示中 ==1 的个数==（汉明重量）',
                 '示例：`n = 11`（`1011`）→ `3`；`n = 128`（`10000000`）→ `1`',
                 '演示：`n = 180`（`10110100`）→ `4`'],
        before=[dict(heading='yiduobo 的推导', lines=[
            '大于 0 的 `n` 一定可以写成 `XXXXXXX 1 000…0`（0 可能一个都没有）',
            '那么 `n - 1` 就是 `XXXXXXX 0 111…1`，`X` 的部分不变',
            '`n &= n - 1` 之后只剩 `XXXXXXX 0 000…0`',
            '→ ==最后一位 1 以及之后的 0 被划掉了==',
        ])],
        quote='依然是可以每次通过n&1取出最后一位……不过这里有一种==更好的写法==……n &= n - 1之后，就只剩下XXXXXXX的部分了，此时已经将==最后一位1以及之后的0划掉了==。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐位检查要循环 32 次；`n &= n - 1` 只循环 ==1 的个数== 次',
              '每轮：`res += 1`，再划掉最低位的 1，直到 `n` 变成 0'],
        summary=['时间 `O(k)`，`k` 为 1 的个数；空间 `O(1)`',
                 '原文：可以起到一定优化效果，但==总体时间复杂度不变==（最坏仍是 32 次）',
                 '`n & (n - 1) == 0` 还能判断 2 的幂（231 题）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
