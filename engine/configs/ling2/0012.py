_R = (
    ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"),  # 个位
    ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"),  # 十位
    ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"),  # 百位
    ("", "M", "MM", "MMM"),  # 千位
)
_NAMES = ('个位', '十位', '百位', '千位')
_EXPR = ('num % 10', 'num // 10 % 10', 'num // 100 % 10', 'num // 1000')
_COL = ('blue', 'green', 'purple', 'orange')


def _digits(num):
    return (num % 10, num // 10 % 10, num // 100 % 10, num // 1000)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    num = S.get('num')
    cv.text((x0 + 18, y0 + 4), 'R[p][d]：第 p 位（0=个位 … 3=千位）数字为 d 时的罗马数字', 23, T['muted'], bold=True)
    hx = 70
    cell = min(64, (x1 - x0 - 40 - hx) / 10)
    sx = x0 + 20 + hx + ((x1 - x0 - 40 - hx) - cell * 10) / 2
    sy = y0 + 70
    rh = 52
    for d in range(10):
        cv.text((sx + d * cell + cell / 2, sy - 8), d, 20, T['muted'], anchor='mb', mono=True)
    dg = _digits(num) if isinstance(num, int) else None
    for vis, p in enumerate((3, 2, 1, 0)):
        Y = sy + vis * rh
        c = T[_COL[p]]
        cv.text((sx - 12, Y + rh / 2 - 3), f'R[{p}]', 20, c, anchor='rm', mono=True, bold=True)
        for d in range(10):
            X = sx + d * cell
            if d >= len(_R[p]):
                continue
            hit = dg is not None and dg[p] == d
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + rh - 8), fill=c if hit else T['panel2'], r=6,
                    outline=T['yellow'] if hit else T['border'], width=3 if hit else 1)
            s = _R[p][d] or '""'
            fs = 20 if len(s) <= 3 else 17
            cv.text((X + cell / 2, Y + (rh - 6) / 2), s, fs, T['bg'] if hit else (T['dim'] if not _R[p][d] else T['text']),
                    anchor='mm', mono=True, bold=True)
    if dg is None:
        return
    y = sy + 4 * rh + 26
    cv.line([(x0 + 20, y - 10), (x1 - 20, y - 10)], T['border'], 2)
    cv.text((x0 + 24, y + 6), f'num = {num}  拆成四个数位：', 24, T['text'], bold=True)
    y += 50
    for vis, p in enumerate((3, 2, 1, 0)):
        c = T[_COL[p]]
        cv.text((x0 + 30, y), f'{_NAMES[p]}', 22, c, bold=True)
        cv.text((x0 + 100, y), f'{_EXPR[p]} = {dg[p]}', 22, T['text'], mono=True)
        cv.text((x0 + 390, y), '→', 22, T['muted'])
        s = _R[p][dg[p]]
        cv.text((x0 + 430, y), f'R[{p}][{dg[p]}] = "{s}"', 22, c, mono=True, bold=True)
        y += 36
    y += 10
    ans = ''.join(_R[p][dg[p]] for p in (3, 2, 1, 0))
    parts = ' + '.join(f'"{_R[p][dg[p]]}"' for p in (3, 2, 1, 0))
    cv.rich(x0 + 24, y, f'{parts} = =={ans}==', x1 - x0 - 48, size=26)


def _cap(S, B, ret):
    num = S.num
    dg = _digits(num)
    parts = '、'.join(f'{_NAMES[p]} `{dg[p]}`→`{_R[p][dg[p]] or "空"}`' for p in (3, 2, 1, 0))
    return f'`num = {num}`：{parts}，拼起来 =={ret}=='


CONFIG = dict(
    num=12, title='整数转罗马数字', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='按数位查表',
    tags=['字节30天', '面试经典150'],
    code='''
R = (
    ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"),  # 个位
    ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"),  # 十位
    ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"),  # 百位
    ("", "M", "MM", "MMM"),  # 千位
)

class Solution:
    def intToRoman(self, num: int) -> str:
        return R[3][num // 1000] + R[2][num // 100 % 10] + R[1][num // 10 % 10] + R[0][num % 10]
''',
    call='[Solution().intToRoman(x) for x in (3749, 58, 1994)]',
    expect=['MMMDCCXLIX', 'LVIII', 'MCMXCIV'],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('num', 'num', 'yellow'), ('千位', 'num // 1000', 'orange'), ('百位', 'num // 100 % 10', 'purple'),
           ('十位', 'num // 10 % 10', 'green'), ('个位', 'num % 10', 'blue')],
    captions={
        'return R[3]': _cap,
    },
    cards=dict(
        one_liner='每一位的写法互不影响：拆出千百十个位，各查一次表',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把整数 `num`（`1 ≤ num ≤ 3999`）转成罗马数字',
                 '符号：`I=1 V=5 X=10 L=50 C=100 D=500 M=1000`；4、9 开头用==减法形式==（`IV IX XL XC CD CM`）',
                 '示例：`3749` → `"MMMDCCXLIX"`；`58` → `"LVIII"`；`1994` → `"MCMXCIV"`'],
        quote='把 num 拆分成==千位数、百位数、十位数和个位数==，分别用罗马数字表示。用字符串数组存储罗马数字，用数位当作数组下标，取出对应的罗马数字，拼接起来。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`3749` = `3000 + 700 + 40 + 9` → `MMM` + `DCC` + `XL` + `IX`',
              '每个数位只有 10 种情况，==提前把 4 张表打好==：`R[0]` 个位 … `R[3]` 千位',
              '数位公式：千位 `num // 1000`，百位 `num // 100 % 10`，十位 `num // 10 % 10`，个位 `num % 10`'],
        result='三个示例全部正确：`MMMDCCXLIX`、`LVIII`、`MCMXCIV` ✓',
        after=[dict(heading='为什么表里是这些字符串？', lines=[
            '1~3：重复一的符号（`I II III`）；4：减法 `IV`',
            '5~8：五的符号再补一（`V VI VII VIII`）；9：减法 `IX`',
            '十位、百位把 `I V X` 换成 `X L C`、`C D M`，规律完全一样',
            '千位最多 3（`num ≤ 3999`），所以 `R[3]` 只有 4 项'])],
        summary=['时间、空间都是 `O(1)`：只查 4 次表',
                 '表的第 0 项是空串 `""`：数位为 0 时什么都不拼（如 `58` 的千位、百位）',
                 '拼接顺序是==千 → 百 → 十 → 个==，高位在前',
                 '同类题：13. 罗马数字转整数（反过来：小符号在大符号左边就减）'],
    ),
)
