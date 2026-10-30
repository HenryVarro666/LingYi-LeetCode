NS = [9, 0, 243, 15, -27, 3]
BIG = 1162261467  # int 范围内最大的 3 的幂


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    cv.text((x0 + 18, y0 + 4), '1162261467 的全部正约数（只有 3^0 … 3^19 这 20 个）', 24, T['muted'], bold=True)
    cw, chh, per = 190, 50, 5
    sx = x0 + (x1 - x0 - cw * per) / 2
    for k in range(20):
        r, c = divmod(k, per)
        X, Y = sx + c * cw, y0 + 44 + r * (chh + 8)
        v = 3 ** k
        hit = v == n
        cv.rect((X + 4, Y, X + cw - 4, Y + chh), fill=T['green'] if hit else T['panel2'], r=10,
                outline=T['border'], width=1)
        cv.text((X + 14, Y + chh / 2), f'3^{k}', 18, T['bg'] if hit else T['muted'], anchor='lm', bold=True)
        cv.text((X + cw - 14, Y + chh / 2), str(v), 18 if v < 10 ** 8 else 16, T['bg'] if hit else T['text'],
                anchor='rm', mono=True)
    if n is None:
        return
    y = y0 + 290
    if n <= 0:
        cv.text((x0 + 40, y), f'n = {n}：不满足 n > 0', 36, T['red'], bold=True, mono=True)
        cv.text((x0 + 40, y + 60), '括号里的 (n > 0) 为 False → 后半句不再计算', 26, T['text'])
    else:
        q, r = divmod(BIG, n)
        cv.text((x0 + 40, y), f'1162261467 ÷ {n} = {q} … {r}', 34, T['green'] if r == 0 else T['red'],
                bold=True, mono=True)
        cv.text((x0 + 40, y + 60), f'{n} 是 1162261467 的约数 → 是 3 的幂' if r == 0
                else f'余数不为 0 → {n} 不是约数 → 不是 3 的幂', 26, T['green'] if r == 0 else T['red'], bold=True)
    done = NS[:NS.index(n) + 1] if n in NS else []
    cv.text((x0 + 18, y1 - 110), '已测试', 22, T['muted'], bold=True)
    X = x0 + 40
    for v in done:
        ok = v > 0 and BIG % v == 0
        w = max(cv.tlen(str(v), 24, mono=True), cv.tlen('False', 20)) + 30
        cv.rect((X, y1 - 76, X + w, y1 - 6), fill=T['panel2'], r=10, outline=T['yellow'] if v == n else T['border'],
                width=3 if v == n else 1)
        cv.text((X + w / 2, y1 - 58), str(v), 24, T['text'], anchor='mm', mono=True, bold=True)
        cv.text((X + w / 2, y1 - 26), str(ok), 20, T['green'] if ok else T['red'], anchor='mm', bold=True)
        X += w + 12


def _cap(S, B, ret):
    n = S.n
    if n <= 0:
        return f'`n = {n}`：`(n > 0)` 不成立 → 直接返回 `False`，后面的取模不会执行'
    q, r = divmod(BIG, n)
    if r == 0:
        return f'`1162261467 = {n} × {q}`：`{n}` ==是约数== → `True`'
    return f'`1162261467 % {n} = {r}`：`{n}` 不是约数（含 3 以外的因子）→ `False`'


CONFIG = dict(
    num=326, title='3 的幂', difficulty='Easy', category='数学',
    author='yiduobo', technique='取巧：判断 n 是不是 1162261467 的约数',
    tags=['List.md'],
    code='''
class Solution(object):
    def isPowerOfThree(self, n):
        return (n > 0) and (1162261467 % n == 0)
''',
    call=f'''s = Solution()
[s.isPowerOfThree(x) for x in {NS}]''',
    expect=[True, False, True, False, False, True],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return (n > 0)': _cap,
    },
    cards=dict(
        one_liner='int 里最大的 3 的幂是 1162261467，3 的幂都是它的约数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定一个整数 `n`，判断它是否是 3 的幂次方：存在整数 `x` 使 `n == 3^x`',
                 '示例：`27` → `true`，`0` → `false`，`9` → `true`，`45` → `false`',
                 '`n` 在 32 位有符号整数范围内'],
        quote='考虑int范围内3的幂次最大为1162261467，那么==如果n大于0，且n是1162261467的约数，那么n就是3的幂==。',
        quote_src='—— yiduobo 题解（原文：“我在这里使用的是取巧的做法”）',
        idea=['`1162261467 = 3^19`，它的质因子只有 3',
              '所以它的约数恰好就是 `3^0, 3^1, …, 3^19`——int 范围内全部的 3 的幂',
              '一行判断：`(n > 0) and (1162261467 % n == 0)`'],
        result='6 个测试：`[True, False, True, False, False, True]` ✓',
        summary=['时间、空间 `O(1)`，没有循环也没有递归（题目的进阶要求）',
                 '`(n > 0)` 写在前面：负数和 0 直接排除，也避免了 `% 0` 报错',
                 '只适用于==质数==的幂；判断 4 的幂之类要换别的办法',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
