NUMS = (678, 38, 18, 0)


def _chain(n):
    out = [n]
    while n >= 10:
        n = sum(int(c) for c in str(n))
        out.append(n)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'num' not in S:
        return
    n = S['num']
    ch = _chain(n)
    cv.text((x0 + 18, y0 + 4), '反复把各位相加（暴力过程，只用来对照）', 22, T['muted'], bold=True)
    X, Y = x0 + 40, y0 + 60
    for k, v in enumerate(ch):
        txt = str(v)
        w = max(90, cv.tlen(txt, 40, True, True) + 40)
        last = k == len(ch) - 1
        cv.rect((X, Y, X + w, Y + 76), fill=T['green'] if last else T['panel2'], r=12, outline=T['border'])
        cv.text((X + w / 2, Y + 38), txt, 40, T['bg'] if last else T['text'], anchor='mm', bold=True, mono=True)
        if not last:
            nxt = ch[k + 1]
            digits = ' + '.join(str(v))
            cv.text((X + w + 70, Y - 4), digits, 20, T['muted'], anchor='mb', mono=True)
            cv.arrow((X + w + 12, Y + 38), (X + w + 128, Y + 38), T['muted'], 3, 12)
            d = v - nxt
            cv.text((X + w + 70, Y + 64), f'−{d}', 22, T['orange'], anchor='mt', bold=True, mono=True)
            cv.text((X + w + 70, Y + 92), f'= 9×{d // 9}', 20, T['orange'], anchor='mt', mono=True)
        X += w + (140 if not last else 0)
    Y2 = y0 + 230
    if n > 0:
        cv.text((x0 + 40, Y2), '每一步减少的都是 9 的倍数 → 只看结果，就是从 num 开始不断减 9：', 24, T['text'])
        m = n % 9
        r = (n - 1) % 9 + 1
        tail = f'num mod 9 = {m}' + ('，但 num > 0 是 9 的倍数，结果是 9 而不是 0' if m == 0 else '')
        cv.text((x0 + 40, Y2 + 44), tail, 26, T['yellow'], bold=True)
        cv.text((x0 + 40, Y2 + 96), f'(num − 1) mod 9 + 1 = ({n} − 1) mod 9 + 1 = {r}', 30, T['green'], bold=True, mono=True)
    else:
        cv.text((x0 + 40, Y2), 'num = 0：Python 中 (0 − 1) % 9 = 8，公式会算出 9 → 必须特判', 26, T['yellow'], bold=True)
    cur = NUMS.index(n)
    Y3 = y1 - 70
    cv.text((x0 + 18, Y3 - 40), '本视频的输入（依次调用）', 22, T['muted'], bold=True)
    X = x0 + 40
    for k, v in enumerate(NUMS):
        r = (v - 1) % 9 + 1 if v else 0
        txt = f'{v} → {r}' if k <= cur else f'{v} → ?'
        w = cv.tlen(txt, 26, True, True) + 36
        cv.rect((X, Y3, X + w, Y3 + 50), fill=T['blue'] if k == cur else T['panel2'], r=10, outline=T['border'])
        cv.text((X + w / 2, Y3 + 25), txt, 26, T['bg'] if k == cur else (T['text'] if k < cur else T['dim']),
                anchor='mm', bold=True, mono=True)
        X += w + 16


CONFIG = dict(
    num=258, title='各位相加', difficulty='Easy', category='数学',
    author='灵茶山艾府', technique='O(1) 公式：(num − 1) mod 9 + 1',
    tags=['List.md'],
    code='''
class Solution:
    def addDigits(self, num: int) -> int:
        return (num - 1) % 9 + 1 if num else 0
''',
    call=f'[Solution().addDigits(x) for x in {NUMS}]',
    expect=[3, 2, 9, 0],
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('num', 'num', 'blue'), ('num % 9', 'num % 9', 'orange')],
    captions={
        'return (num - 1)': lambda S, B, ret: (
            f'`num = {S.num}`：`({S.num} − 1) % 9 + 1` = =={ret}==' + ('（是 9 的倍数 → 9，不是 0）' if S.num % 9 == 0 else '')
            if S.num else '`num = 0` → 走 `else`，直接返回 ==0=='),
    },
    cards=dict(
        one_liner='每次各位相加都减少 9 的倍数，所以答案就是 num 模 9（0 变 9）',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定非负整数 `num`，反复把各位数字相加，直到结果只有一位，返回它',
                 '示例：`38 → 3 + 8 = 11 → 1 + 1 = 2`，返回 `2`；`num = 0` → `0`',
                 '进阶：不用循环或递归，`O(1)` 时间解决',
                 f'本视频依次计算 `{list(NUMS)}`'],
        before=[dict(heading='从 678 到 21，减少了多少？', chapter='② 思路', lines=[
            '`678 → 6 + 7 + 8 = 21 → 2 + 1 = 3`',
            '`678 − 21 = (600 − 6) + (70 − 7) + (8 − 8)`',
            '`= 6 × 99 + 7 × 9`：==99 和 9 都是 9 的倍数==',
            '从 21 到 3 也一样，减少量也是 9 的倍数',
        ])],
        quote='由于减少量总是 9 的倍数，只看结果的话，相当于从 678 开始，不断地减 9，直到减成个位数（小于 10 的数）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不断减 9 直到小于 9，得到的就是 `num mod 9`',
              '特殊情况：`num > 0` 且是 9 的倍数，最终会减成 ==9== 而不是 0',
              '整合成一个公式：`(num − 1) mod 9 + 1`；Python 里 `-1 % 9 = 8`，`num = 0` 要特判'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '结论：答案 = `0`（num = 0）/ `9`（9 的倍数）/ `num mod 9`（其余）',
                 '易错：Python 的 `%` 结果非负，`(0 − 1) % 9 = 8`，所以 `num = 0` 必须单独返回 0',
                 '这个结果在数学上叫「数根」，`n ≡ 各位数字之和 (mod 9)`'],
    ),
)
