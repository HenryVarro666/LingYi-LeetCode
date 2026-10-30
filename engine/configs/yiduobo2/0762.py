L0, R0 = 6, 10
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19}
W = R0.bit_length()

CODE = '''
class Solution(object):
    def countPrimeSetBits(self, L, R):

        res = 0
        for now in range(L, R + 1):
            cnt = 0
            while now:
                now &= now - 1
                cnt += 1
            if cnt in [2, 3, 5, 7, 11, 13, 17, 19]:
                res += 1

        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _src(S):
    ln = S.get('_line', 0)
    return _LINES[ln - 1] if 0 < ln <= len(_LINES) else ''


def _clear(x, k):
    for _ in range(k):
        x &= x - 1
    return x


def _P(x):
    """[L0, x) 中满足条件的个数"""
    return sum(1 for v in range(L0, x) if bin(v).count('1') in PRIMES)


def _cur(S):
    """当前正在处理的原始整数（now 会被改掉，所以从 now/cnt/res 反推）"""
    if 'now' not in S or 'res' not in S:
        return None
    src = _src(S)
    if 'for now in' in src:
        return S['now'] if S['now'] != 0 else None   # 循环结束时 now 停在 0
    if 'cnt' not in S:
        return None
    k = S['cnt'] + (1 if 'now &=' in src else 0)
    t = S['res'] - (1 if 'res += 1' in src else 0)
    c = [x for x in range(L0, R0 + 1) if _clear(x, k) == S['now'] and _P(x) == t]
    return c[0] if c else None


def _bits(cv, T, X, y, val, cell, hl=None, gone=None, size=26):
    s = format(val, f'0{W}b')
    for j, ch in enumerate(s):
        pos = W - 1 - j
        fill = T['panel2']
        col = T['text'] if ch == '1' else T['dim']
        out = None
        if pos == hl:
            fill, col, out = T['yellow'], T['bg'], T['yellow']
        if pos == gone:
            out = T['red']
            col = T['red']
        cv.rect((X + j * cell + 2, y, X + (j + 1) * cell - 2, y + cell - 4), fill=fill, outline=out, width=3, r=6)
        cv.text((X + j * cell + cell / 2, y + (cell - 4) / 2), ch, size, col, anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '枚举 [L, R] 的每个数，数二进制里有几个 1（黄框 = 当前数）', 24, T['muted'], bold=True)
    cur = _cur(S)
    alldone = cur is None and 'now' in S
    src = _src(S)
    judged = 'if cnt in' in src or 'res += 1' in src
    rh = 56
    for idx, x in enumerate(range(L0, R0 + 1)):
        y = y0 + 48 + idx * rh
        is_cur = x == cur
        done = alldone or (cur is not None and x < cur)
        if is_cur:
            cv.rect((x0 + 20, y - 2, x1 - 20, y + rh - 8), fill=T['panel2'], outline=T['yellow'], width=2, r=8)
        bright = is_cur or done
        cv.text((x0 + 70, y + (rh - 10) / 2), x, 28, T['text'] if bright else T['muted'], anchor='mm', bold=True)
        bs = format(x, f'0{W}b')
        for j, ch in enumerate(bs):
            cv.text((x0 + 140 + j * 34, y + (rh - 10) / 2), ch, 26,
                    (T['blue'] if ch == '1' else T['dim']) if bright else T['dim'], anchor='mm', bold=True, mono=True)
        c = bin(x).count('1')
        if done or (is_cur and judged):
            ok = c in PRIMES
            cv.text((x0 + 330, y + (rh - 10) / 2), f'{c} 个 1', 26, T['text'], anchor='lm', bold=True)
            cv.text((x0 + 470, y + (rh - 10) / 2), '质数 ✓ 计入' if ok else '不是质数', 26,
                    T['green'] if ok else T['red'], anchor='lm', bold=True)
        elif is_cur:
            cv.text((x0 + 330, y + (rh - 10) / 2), f"已数到 {S.get('cnt', 0)} 个 1 …", 26, T['yellow'], anchor='lm', bold=True)
    # now 的二进制
    yb = y0 + 48 + 5 * rh + 24
    cv.line([(x0 + 20, yb - 12), (x1 - 20, yb - 12)], T['border'], 2)
    if cur is None or 'now' not in S:
        cv.text((x0 + 30, yb + 30), 'n & (n − 1) 会抹掉 n 最低位的 1', 26, T['muted'], anchor='lm')
        return
    now = S['now']
    cell = 64
    gone = None
    if 'now &=' in src and 'now' in B:
        gone = (B['now'] & -B['now']).bit_length() - 1
    hl = (now & -now).bit_length() - 1 if now and gone is None else None
    cv.text((x0 + 30, yb + 28), 'now =', 30, T['muted'], anchor='lm', bold=True)
    _bits(cv, T, x0 + 130, yb, now, cell, hl=hl, gone=gone, size=30)
    note = ('红框：刚被抹掉的 1' if gone is not None else
            ('黄格：最低位的 1，下一步被抹掉' if now else 'now = 0：1 已全部抹掉'))
    cv.text((x0 + 130 + W * cell + 24, yb + 28), note, 24, T['red'] if gone is not None else T['yellow'], anchor='lm', bold=True)


def _for_cap(S, B, ret):
    if S['now'] == 0:
        return '`[L, R]` 全部枚举完毕'
    return f"取下一个数 `now = {S['now']}`，二进制 `{S['now']:b}`"


def _while_cap(S, B, ret):
    if S['now']:
        return f"`now = {S['now']:b}` 非 0，还有 1"
    return f"`now` 变成 0：1 已全部抹掉，一共 `cnt = {S['cnt']}` 个"


def _if_cap(S, B, ret):
    c = S['cnt']
    if c in PRIMES:
        if S['res'] == 0:
            return f'`cnt = {c}` 是质数 → 计入答案（`2^20 > 10^6`，只需判断 19 以内的质数）'
        return f'`cnt = {c}` 是质数 → 计入'
    return f'`cnt = {c}` 不在质数表里 → 不计入（注意 ==1 不是质数==）'


CONFIG = dict(
    num=762, title='二进制表示中质数个计算置位', difficulty='Easy', category='技巧',
    author='yiduobo', technique='暴力枚举 · n &= n − 1 数 1',
    tags=['字节3个月', '字节6个月'],
    code=CODE,
    call=f'Solution().countPrimeSetBits({L0}, {R0})',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('now', 'now', 'blue'), ('now(二进制)', lambda S: format(S['now'], 'b'), 'yellow'),
           ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计满足条件的整数个数；区间最多 `10^4` 个数，==直接逐个枚举==',
        'for now in range': _for_cap,
        'cnt = 0': '`cnt`：`now` 的二进制里 1 的个数',
        'while now': _while_cap,
        'now &= now - 1': lambda S, B, r: (f"`{B['now']:b} & {B['now'] - 1:b}` = `{S['now']:b}`："
                                           f"`now − 1` 把最低位的 1 变 0、右边变 1，与运算后==最低位的 1 被抹掉=="
                                           if B['now'] == L0 else
                                           f"`{B['now']:b} & {B['now'] - 1:b}` = `{S['now']:b}`，抹掉最低位的 1"),
        'cnt += 1': '抹掉一个 1 → `cnt = {cnt}`',
        'if cnt in': _if_cap,
        'res += 1': '`res` → {res}',
        'return res': '`[{L}, {R}]` 中共有 `{res}` 个数的置位数是质数',
    },
    max_steps=70,
    cards=dict(
        one_liner='逐个枚举，用 `n &= n − 1` 数出二进制里 1 的个数',
        complexity='时间 `O((R − L)·log R)`，空间 `O(1)`',
        problem=['统计 `[L, R]` 中二进制里 1 的个数为==质数==的整数个数',
                 '例：`21 = 10101` 有 3 个 1，3 是质数',
                 '示例：`L = 6, R = 10` → `4`（6、7、9、10）'],
        quote='注意到这里最多也就一百万个数，因此我在这里选择直接遍历每个数，分解其二进制表示中的每一位然后进行统计。'
              '由于2的20次方为1048576，因此我们最大只需要考虑到19个1的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据范围只有 `10^6`，区间长度 `≤ 10^4` → 直接暴力枚举',
              '`now &= now − 1` 每次抹掉最低位的 1，循环次数 = 1 的个数',
              '`2^20 > 10^6` → 至多 19 个 1，只需查 `[2,3,5,…,19]`'],
        summary=['时间 `O((R − L)·log R)`，空间 `O(1)`',
                 '`n & (n − 1)`：抹掉最低位的 1，比逐位 `>> 1` 循环次数更少',
                 '易错：==1 不是质数==；`range(L, R + 1)` 要包含右端点',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：数位 DP / 组合数学可做到 `O(log² R)`，与区间长度无关'],
    ),
)
