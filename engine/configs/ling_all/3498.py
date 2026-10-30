def _prods(S):
    s = S['s']
    return [(ord('{') - ord(c)) * i for i, c in enumerate(s, 1)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    n = len(s)
    cv.text((x0 + 18, y0 + 4), '每个字母：反转值 × 位置（反转值 = ord("{") − ord(c)）', 24, T['muted'], bold=True)
    cell = min(130, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    top = y0 + 70
    tot = 0
    for i, c in enumerate(s, 1):
        X = sx + (i - 1) * cell
        rv = ord('{') - ord(c)
        p = rv * i
        tot += p
        cv.rect((X + 4, top, X + cell - 4, top + 70), fill=T['blue'], r=8)
        cv.text((X + cell / 2, top + 35), c, 40, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, top + 84), f'位置 {i}', 22, T['dim'], anchor='mt')
        cv.text((X + cell / 2, top + 120), f'反转值 {rv}', 24, T['cyan'], anchor='mt', bold=True)
        cv.text((X + cell / 2, top + 160), f'× {i}', 24, T['muted'], anchor='mt')
        cv.text((X + cell / 2, top + 200), f'= {p}', 30, T['green'], anchor='mt', bold=True)
    cv.text((x0 + 20, top + 270), '累加：' + ' + '.join(str(p) for p in _prods(S)) + f' = {tot}', 30, T['yellow'], bold=True)


CONFIG = dict(
    num=3498, title='字符串的反转度', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='一行 sum + enumerate',
    tags=[],
    code='''
class Solution:
    def reverseDegree(self, s: str) -> int:
        return sum((ord('{') - ord(c)) * i for i, c in enumerate(s, 1))  # 下标从 1 开始
''',
    call='Solution().reverseDegree("zaza")',
    expect=160,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('s', 's')],
    captions={
        'return sum': lambda S, B, ret: f'逐个字母：`ord("{{") - ord(c)` 是反转值（`{{` 是 `z` 的下一个字符），乘以从 1 开始的下标，全部求和 = =={ret}==',
    },
    cards=dict(
        after=[dict(heading='再看示例 "abc"', lines=[
            '`a`：`26 × 1 = 26`；`b`：`25 × 2 = 50`；`c`：`24 × 3 = 72`',
            '`26 + 50 + 72 = 148`，和题目示例一致',
            '越靠后的字母乘的位置越大，所以顺序也会影响结果'])],
        one_liner='用 z 的下一个字符 { 减去 c，就是反转后的字母值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母在反转字母表里的位置：`a = 26, b = 25, ..., z = 1`',
                 '反转度 = 每个字符「反转位置 × 字符串位置（从 1 开始）」之和',
                 '示例：`"abc"` → `26 + 50 + 72 = 148`；本视频演示 `"zaza"` → `160`'],
        quote='用 z 的下一个字符 { 减去 s[i]，就是字母反转后的值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['ASCII 里 `{` 紧挨在 `z` 后面：`ord("{") - ord("z") = 1`，`ord("{") - ord("a") = 26`',
              '不用建反转表，一次减法就得到反转值',
              '`enumerate(s, 1)` 让下标直接从 1 开始，再配合 `sum` 一行写完'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：下标从 1 开始，所以 `enumerate(s, 1)`，不是默认的 0',
                 '易错：反转值是 `ord("{") - ord(c)`，写成 `ord("z") - ord(c)` 会少 1',
                 '同类技巧：字母和数字互转时，用 ASCII 差值代替查表'],
    ),
)
