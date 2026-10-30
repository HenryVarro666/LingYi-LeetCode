from itertools import product
from math import comb as _comb

_N, _K = 7, 3
_ALL = [c for c in product(range(1, _N + 1), repeat=_K) if sum(c) == _N]
assert len(_ALL) == _comb(_N - 1, _K - 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    odd = [all(v % 2 for v in c) for c in _ALL]
    cv.text((x0 + 18, y0 + 4), f'和为 {_N}、长为 {_K} 的全部正整数序列（共 {len(_ALL)} 个）', 24, T['muted'], bold=True)
    cols = 5
    cw = (x1 - x0 - 40) / cols
    ch = 64
    for i, c in enumerate(_ALL):
        X = x0 + 20 + (i % cols) * cw
        Y = y0 + 56 + (i // cols) * (ch + 14)
        fill, tc = T['panel2'], T['text']
        outline = T['border']
        if line >= 5 and odd[i]:
            outline = T['pink']
        if line >= 6 and odd[i]:
            fill, tc = (70, 40, 48), T['dim']
        elif line >= 4 and not odd[i]:
            fill, tc = (40, 70, 52), T['green']
        cv.rect((X + 4, Y, X + cw - 4, Y + ch), fill=fill, outline=outline, width=3 if outline == T['pink'] else 1, r=10)
        cv.text((X + cw / 2, Y + ch / 2), ','.join(map(str, c)), 26, tc, anchor='mm', bold=True, mono=True)
        if line >= 6 and odd[i]:
            cv.line([(X + 14, Y + ch / 2), (X + cw - 14, Y + ch / 2)], T['pink'], 3)
    yb = y0 + 56 + 3 * (ch + 14) + 6
    if line >= 4:
        cv.text((x0 + 20, yb), f'隔板法：C({_N - 1}, {_K - 1}) = {len(_ALL)} 个序列', 24, T['text'], bold=True)
    if line >= 5:
        cv.text((x0 + 20, yb + 40), f'粉框 = 三个数全是奇数，乘积为奇数：共 {sum(odd)} 个 = C(({_N}+{_K})/2 − 1, {_K - 1})', 24, T['pink'], bold=True)
    if line >= 6:
        cv.text((x0 + 20, yb + 80), f'绿色 = 至少有一个偶数（乘积为偶数）：{len(_ALL)} − {sum(odd)} = {len(_ALL) - sum(odd)}', 24, T['green'], bold=True)


CONFIG = dict(
    num=4002, title='统计有效序列数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='隔板法 · 总数减全奇数',
    tags=['组合计数', '难度分 1912'],
    setup='''
from math import comb
''',
    code='''
class Solution:
    def countValidSequences(self, n: int, k: int) -> int:
        # 更快的做法见【Python3 预处理】
        ans = comb(n - 1, k - 1)
        if (n + k) % 2 == 0:
            ans -= comb((n + k) // 2 - 1, k - 1)
        return ans % 1_000_000_007
''',
    call=f'Solution().countValidSequences({_N}, {_K})',
    expect=9,
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=lambda S: f"`n + k = {S['n'] + S['k']}`，{'偶数：全奇数序列存在，要减掉' if (S['n'] + S['k']) % 2 == 0 else '奇数：不可能拆成 k 个奇数，什么都不减'}", size=26, h=60),
    ],
    watch=['n', 'k', ('ans', 'ans', 'green')],
    captions={
        'ans = comb': '隔板法：`n` 个球有 `n−1` 个空隙，选 `k−1` 个插隔板：`C({n - 1}, {k - 1})` = =={ans}== 个正整数序列',
        'if (n + k)': lambda S, B, r: (f'`n + k = {S.n + S.k}` 是偶数 → 能拆成 `k` 个正奇数，要把这些全奇（乘积为奇数）的序列减掉' if (S.n + S.k) % 2 == 0 else f'`n + k = {S.n + S.k}` 是奇数 → 拆不成 `k` 个正奇数，不用减'),
        'ans -= comb': '全奇数序列：每个数写成 `2y−1`，`Σy = (n+k)/2 = {(n + k) // 2}`，隔板法 `C({(n + k) // 2 - 1}, {k - 1})` = {__import__("math").comb((n + k) // 2 - 1, k - 1)}；`ans` = {B.ans} − {__import__("math").comb((n + k) // 2 - 1, k - 1)} = =={ans}==',
        'return ans': '返回 `{ans} % (10^9+7)` = =={ret}==',
    },
    cards=dict(
        one_liner='总序列数 − 全是奇数的序列数，两次隔板法',
        complexity='时间 `O(1)`（不计预处理），空间 `O(1)`',
        problem=['求长为 `k`、和为 `n` 的正整数序列中，==乘积为偶数==的个数（模 `10^9+7`）',
                 '`[1,1,2]` 和 `[1,2,1]` 算不同的序列',
                 '示例：`n=5, k=3` → `3`；本视频：`n=7, k=3` → `9`'],
        quote='序列只要有一个偶数，乘积就是偶数。所以只有全为奇数的序列，乘积才不是偶数。减去这种序列的方案数，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['总数：`n` 个球排一行，`n−1` 个空隙插 `k−1` 块隔板，`C(n−1, k−1)`',
              '全奇数：`x_i = 2y_i − 1`，`y_i` 是正整数，`Σy_i = (n+k)/2`',
              '`n+k` 是奇数时拆不出来，方案数 0；偶数时 `C((n+k)/2 − 1, k−1)`'],
        after=[dict(heading='另一种推导（原文「附」）', lines=[
            '先拿出 `k` 个球，剩下 `n−k` 个球分成 `k` 段（可空），每段个数为偶数',
            '两个球一组看成大球，问题变成 `(n−k)/2` 个大球分 `k` 段',
            '再用一次隔板法，得到同一个组合数 `C((n+k)/2 − 1, k−1)`'])],
        summary=['复杂度 `O(1)`（预处理阶乘和逆元 `O(n)`），`n` 大时用预处理版本更快',
                 '`2y−1` 而不是 `2y+1`：这样 `y` 才是正整数，能直接用隔板法',
                 '`n + k` 为奇数时不减；偶数时才减全奇数序列',
                 '最后别忘了 `% (10^9+7)`，减法可能出现负数，Python 取模会自动变回非负'],
    ),
)
