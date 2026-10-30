NUMS = (8, 10, -4, 1)
W = 6  # 显示的二进制位数


def _bits(cv, T, x, y, val, cell, color, label, sub):
    cv.text((x - 30, y + cell / 2), label, 26, T['text'], anchor='rm', bold=True, mono=True)
    cv.text((x - 30, y + cell / 2 + 30), sub, 20, T['dim'], anchor='rm', mono=True)
    s = format(val, f'0{W}b')
    for i, ch in enumerate(s):
        X = x + i * cell
        one = ch == '1'
        cv.rect((X + 4, y + 4, X + cell - 4, y + cell - 4), fill=T[color] if one else T['panel2'], r=8,
                outline=T['border'], width=1)
        cv.text((X + cell / 2, y + cell / 2), ch, 32, T['bg'] if one else T['dim'], anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'n & (n − 1)：去掉 n 二进制的最低位 1，剩下是否为 0？', 24, T['muted'], bold=True)
    n = S.get('n')
    if n is None:
        return
    cell = 78
    x = x0 + 300
    if n <= 0:
        cv.text((x0 + 60, y0 + 110), f'n = {n} ≤ 0', 40, T['red'], bold=True, mono=True)
        cv.text((x0 + 60, y0 + 180), '不可能是 2 的幂（2^x 总是正数）', 28, T['text'], bold=True)
        cv.text((x0 + 60, y0 + 230), '先用 if 特判掉，直接返回 False', 24, T['muted'])
        if n == 0:
            cv.text((x0 + 60, y0 + 310), '注意：0 & (0 − 1) = 0 & (−1) = 0', 26, T['orange'], bold=True, mono=True)
            cv.text((x0 + 60, y0 + 352), '如果漏掉 n > 0，0 会被误判成 2 的幂！', 26, T['orange'], bold=True)
        return
    for i in range(W):
        cv.text((x + i * cell + cell / 2, y0 + 50), f'2^{W - 1 - i}', 18, T['dim'], anchor='mm', mono=True)
    _bits(cv, T, x, y0 + 75, n, cell, 'blue', f'n = {n}', '')
    _bits(cv, T, x, y0 + 175, n - 1, cell, 'purple', f'n − 1 = {n - 1}', '')
    cv.line([(x - 10, y0 + 268), (x + W * cell + 10, y0 + 268)], T['border'], 3)
    r = n & (n - 1)
    _bits(cv, T, x, y0 + 285, r, cell, 'red' if r else 'green', f'n & (n−1) = {r}', '')
    msg = (f'去掉最低位的 1 之后 ==什么都不剩== → 原来只有一个 1 → 是 2 的幂' if r == 0
           else f'去掉最低位的 1 之后还剩 `{r}` → 原来不止一个 1 → 不是 2 的幂')
    cv.rich(x0 + 30, y0 + 395, msg, x1 - x0 - 60, size=25, accent=T['orange'], max_lines=2)


CONFIG = dict(
    num=231, title='2 的幂', difficulty='Easy', category='技巧',
    author='yiduobo', technique='位运算 · 去掉最低位的 1',
    tags=['List.md'],
    code='''
class Solution(object):
    def isPowerOfTwo(self, n):
        if n <= 0:
            return False

        return n & (n - 1) == 0
''',
    call=f'''s = Solution()
[s.isPowerOfTwo(x) for x in {NUMS}]''',
    expect=[True, False, False, True],
    views=[
        dict(type='custom', draw=_draw, h=500),
        dict(type='text', h=60, size=26, fn=lambda S: f'依次测试 `n = {", ".join(map(str, NUMS))}`'),
    ],
    watch=[('n', 'n', 'blue'), ('n - 1', 'n - 1', 'purple'), ('n & (n - 1)', 'n & (n - 1)')],
    captions={
        'if n <= 0': lambda S, B, ret: (f'`n = {S.n} ≤ 0`：2 的幂一定是正数 → 不可能' if S.n <= 0
                                        else f'测试 `n = {S.n}`：大于 0，看它的二进制'),
        'return False': '返回 `False`',
        'return n & (n - 1) == 0': lambda S, B, ret: (
            f'`{S.n} & {S.n - 1} = {S.n & (S.n - 1)}`：' + ('去掉最低位的 1 后为 0 → ==只有一个 1==，返回 `True`' if ret
                                                          else f'去掉最低位的 1 后还剩 `{S.n & (S.n - 1)}` → 返回 `False`')),
    },
    cards=dict(
        one_liner='2 的幂只有一个 1：去掉最低位的 1 就变成 0',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给你整数 `n`（可能为负数或 0），判断它是不是 2 的幂',
                 '即是否存在整数 `x` 使 `n == 2^x`',
                 '示例：`1` → `true`，`16` → `true`，`3` → `false`',
                 f'本视频依次测试 `{", ".join(map(str, NUMS))}`'],
        quote='可以不断模2来判断，不过这样做的时间复杂度是O(logn)，有更好的做法。注意到2的幂在二进制表示下一定是1000....000的形式，于是我们可以通过n &= n - 1去除掉最低位的1，然后判断n是否等于0。',
        quote_src='—— yiduobo 题解',
        idea=['朴素：不断除以 2 看余数，`O(log n)`',
              '`n - 1` 把最低位的 1 变成 0、它右边的 0 全变成 1，所以 `n & (n - 1)` ==恰好去掉最低位的 1==',
              '去掉之后为 0 ⇔ 原来只有一个 1 ⇔ 是 2 的幂；`n ≤ 0` 先特判'],
        result='四个测试：`[True, False, False, True]` ✓',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：`n ≤ 0` 必须先特判，`0 & (−1) = 0` 会被误判',
                 '`n & (n − 1)` 去最低位 1、`n & −n` 取最低位 1，是两个常用位运算技巧',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神把特判和位运算合成一行 `n > 0 and …`'],
    ),
)
