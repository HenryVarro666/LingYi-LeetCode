def _txt(S):
    if 'digits' not in S:
        return ''
    d = S['digits']
    if 'res' in S:
        return f"九进制各位（高位在前）= `{''.join(str(x) for x in d[::-1])}`，按十进制读出来 → res = =={S['res']}=="
    return '`n` 反复 `% 9` 取低位，`// 9` 去掉低位'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '去掉所有含 9 的数后，序列 = 九进制计数（0~8 十个数字里少了 9）', 22, T['muted'], bold=True)
    # 对照表：第 k 个数 -> 九进制写法
    ks = [1, 2, 8, 9, 10, 11, 17, 18, 19]
    cell = min(100, (x1 - x0 - 130) / len(ks))
    sx = x0 + 110
    cv.text((sx - 8, y0 + 70), '第 n 个', 20, T['muted'], anchor='rm')
    cv.text((sx - 8, y0 + 130), '答案', 20, T['muted'], anchor='rm')
    n0 = S.get('n_init')
    for i, k in enumerate(ks):
        ans = int(''.join(str(int(c)) for c in (lambda k: (lambda f: f(f, k))(lambda f, m: '' if m == 0 else f(f, m // 9) + str(m % 9)))(k)))
        X = sx + i * cell
        cv.rect((X + 3, y0 + 46, X + cell - 3, y0 + 92), fill=T['panel2'], r=8)
        cv.text((X + cell / 2, y0 + 69), k, 26, T['text'], anchor='mm', bold=True, mono=True)
        cv.rect((X + 3, y0 + 106, X + cell - 3, y0 + 152), fill=T['panel2'], outline=T['border'], r=8)
        cv.text((X + cell / 2, y0 + 129), ans, 26, T['green'], anchor='mm', bold=True, mono=True)
    cv.text((x0 + 18, y0 + 180), '例：第 9 个数是 `10`（跳过 9），第 18 个是 `20`（跳过 19）'.replace('`', ''), 22, T['dim'])
    if 'digits' in S:
        yy = y0 + 250
        cv.text((x0 + 18, yy), 'digits（低位在前）', 24, T['muted'], bold=True)
        d = S['digits']
        c2 = 90
        for i, v in enumerate(d):
            X = x0 + 40 + i * (c2 + 10)
            cv.rect((X, yy + 44, X + c2, yy + 44 + c2), fill=T['panel2'], outline=T['blue'], width=3, r=10)
            cv.text((X + c2 / 2, yy + 44 + c2 / 2), v, 40, T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + c2 / 2, yy + 44 + c2 + 8), f'9^{i}', 20, T['dim'], anchor='mt', mono=True)
        yy2 = yy + 200
        cv.text((x0 + 18, yy2), f"n = {S['n']}", 36, T['cyan'], bold=True, mono=True)
        if 'res' in S:
            cv.text((x0 + 300, yy2), f"res = {S['res']}", 36, T['green'], bold=True, mono=True)


CONFIG = dict(
    num=660, title='移除 9', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='九进制转换',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def newInteger(self, n):

        digits = []
        while n:
            digits.append(n % 9)
            n //= 9
        
        res = 0
        for digit in digits[::-1]:
            res = res * 10 + digit
        return res
''',
    call='Solution().newInteger(100)',
    expect=121,
    views=[
        dict(type='custom', draw=_draw, h=640),
    ],
    watch=[('n', 'n', 'cyan'), 'digits', 'digit', ('res', 'res', 'green')],
    captions={
        'digits = []': '`digits` 存 9 进制的每一位，先放低位',
        'while n': lambda S, B, r: (f'`n = {S.n}` 还没转完，继续' if S.n else '`n = 0`：所有数位都取完了'),
        'digits.append': '`{B.n} % 9 = {B.n % 9}`：9 进制的最低位 → digits = {digits}',
        'n //= 9': '去掉最低位：`{B.n} // 9` → n = =={n}==',
        'res = 0': '`digits` 是低位在前，要==倒着读==，再按十进制拼成数',
        'for digit in digits[::-1]': lambda S, B, r: ('所有数位都读完了，循环结束' if S.get('digit') == B.get('digit') and 'digit' in B and B.res == S.res and S.res >= 100 else f"取下一位（高位 → 低位）：`digit = {S.digit}`"),
        'res = res * 10': '`res = {B.res}×10 + {digit}` = =={res}==：把 9 进制的数位当十进制数字拼起来',
        'return res': '`100` 的 9 进制是 `121` → 去掉所有含 9 的数后第 100 个数就是 =={res}==',
    },
    cards=dict(
        one_liner='不含 9 的数，就是 9 进制数字',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['把 1, 2, 3, … 中所有==含数字 9==的整数去掉，剩下的序列 1,2,…,8,10,11,…',
                 '给定 `n`，返回新序列的第 `n` 个数（从 1 开始）',
                 '示例：`n = 9` → `10`；本视频：`n = 100` → `121`'],
        quote='本题给出的数字序列实际上就是9进制下的数字序列。因此对于本题，实际上就是问数字n在9进制下的表示，于是直接对n进行进制转换就可以得到最终结果了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想数位 DP 或组合数学：1 到 `10^m` 里含 9 的有 `10^m − 9^m` 个，合法恰好 `9^m` 个',
              '合法数字个数恰是 `9^m`，说明每位只有 9 种选择（0~8）→ 就是==九进制==',
              '所以第 `n` 个数 = `n` 的九进制写法，按十进制读出来'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '`digits` 是低位在前，拼结果必须倒序（`digits[::-1]`）',
                 '原文为 Python 2 写法，整数除法 `n /= 9` 已改为 `n //= 9`（Python 3 的 `/` 会得到小数）',
                 '同类思路：序列缺少某个数字时，把它看成缺一个符号的进制计数'],
    ),
)
