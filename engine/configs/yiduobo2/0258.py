NUMS = (38, 0, 99, 12345)
_REM = {x % 9 if x % 9 else 9: x for x in NUMS if x}  # remainder (0 shown as 9) -> original; inputs chosen to be unique


def _orig(S, B):
    ln = S.get('_line')
    if 'num' not in S:
        return None
    if ln in (3, 4):
        return S['num']
    if ln == 6:
        return B['num']
    r = S['num']
    return _REM.get(r if r else 9)


def _chain(n):
    out = [n]
    while n >= 10:
        n = sum(int(c) for c in str(n))
        out.append(n)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n0 = _orig(S, B)
    if n0 is None:
        return
    ch = _chain(n0)
    cv.text((x0 + 18, y0 + 4), f'num0 = {n0}：每轮迭代 num(t+1) = num(t) − 9 × m(t+1)', 24, T['muted'], bold=True)
    X, Y = x0 + 40, y0 + 64
    for k, v in enumerate(ch):
        txt = str(v)
        w = max(90, cv.tlen(txt, 36, True, True) + 40)
        last = k == len(ch) - 1
        cv.rect((X, Y, X + w, Y + 70), fill=T['cyan'] if last else T['panel2'], r=12, outline=T['border'])
        cv.text((X + w / 2, Y + 35), txt, 36, T['bg'] if last else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + w / 2, Y + 78), f'num{k}', 20, T['muted'], anchor='mt', mono=True)
        if not last:
            m = (v - ch[k + 1]) // 9
            cv.arrow((X + w + 10, Y + 35), (X + w + 120, Y + 35), T['muted'], 3, 12)
            cv.text((X + w + 65, Y + 26), f'− 9×{m}', 22, T['orange'], anchor='mb', bold=True, mono=True)
        X += w + (130 if not last else 0)
    ln = S.get('_line')
    Y2 = y0 + 210
    if n0 == 0:
        cv.text((x0 + 40, Y2), 'num0 = 0：已经是一位数，直接返回 0', 28, T['yellow'], bold=True)
    else:
        total = (n0 - ch[-1]) // 9
        cv.text((x0 + 40, Y2), f'numk = num0 − 9 × n = {n0} − 9 × {total} = {ch[-1]}', 30, T['text'], bold=True, mono=True)
        cv.text((x0 + 40, Y2 + 50), '→ numk 就是 num0 除以 9 的余数（余数为 0 时是 9）', 26, T['muted'])
        if ln is not None and ln >= 6:
            r = n0 % 9
            msg = f'{n0} % 9 = {r}' + ('  → 余数 0 且 num0 ≠ 0，答案是 9' if r == 0 else '')
            cv.text((x0 + 40, Y2 + 100), msg, 30, T['yellow'], bold=True, mono=True)
    cur = NUMS.index(n0)
    Y3 = y1 - 70
    cv.text((x0 + 18, Y3 - 40), '本视频的输入（依次调用）', 22, T['muted'], bold=True)
    X = x0 + 40
    for k, v in enumerate(NUMS):
        r = (v - 1) % 9 + 1 if v else 0
        txt = f'{v} → {r}' if k < cur or (k == cur and ln in (4, 9)) else f'{v} → ?'
        w = cv.tlen(txt, 26, True, True) + 36
        cv.rect((X, Y3, X + w, Y3 + 50), fill=T['blue'] if k == cur else T['panel2'], r=10, outline=T['border'])
        cv.text((X + w / 2, Y3 + 25), txt, 26, T['bg'] if k == cur else (T['text'] if k < cur else T['dim']),
                anchor='mm', bold=True, mono=True)
        X += w + 16


CONFIG = dict(
    num=258, title='各位相加', difficulty='Easy', category='数学',
    author='yiduobo', technique='每轮减少 9 的倍数 → 直接模 9',
    tags=['List.md'],
    code='''
class Solution(object):
    def addDigits(self, num):
        if num == 0:
            return num

        num %= 9
        if num == 0:
            num = 9
        return num
''',
    call=f'[Solution().addDigits(x) for x in {NUMS}]',
    expect=[2, 0, 9, 6],
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('num', 'num', 'blue')],
    captions={
        3: lambda S, B, ret: ('`num == 0` → 本身就是一位数' if S.num == 0 else f'新的输入 `num = {S.num}`，不为 0'),
        4: '直接返回 =={ret}==',
        'num %= 9': '`num %= 9`：`{B.num} % 9` = =={num}==（每轮减少的都是 9 的倍数）',
        7: lambda S, B, ret: ('余数为 0 但 num0 ≠ 0 → 最终会停在 ==9==，不是 0' if S.num == 0 else f'余数 `{S.num}` 不为 0，它就是答案'),
        'num = 9': '`num = 9`',
        9: '返回 =={ret}==',
    },
    cards=dict(
        one_liner='每轮各位相加都减少 9 的倍数，最后剩下的就是模 9 的余数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给定非负整数 `num`，反复把各位数字相加，直到结果只有一位，返回它',
                 '示例：`38 → 11 → 2`，返回 `2`',
                 f'本视频依次计算 `{list(NUMS)}`'],
        quote='继续迭代直到numk在0到9之间，此时numk就是最终的答案，那么numk = num0 - 9 * m1 - 9 * m2 - ... - 9 * mk = num0 - 9 * n，于是就可以直接对num0模9，余数就是numk了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num0 = 10^(L−1)·a[L−1] + … + 10·a[1] + a[0]`',
              '各位相加后 `num1 = a[L−1] + … + a[0] = num0 − 9·m1`（因为 `10^k − 1` 是 9 的倍数）',
              '一直迭代：`numk = num0 − 9·n` → 对 `num0` 模 9 即可',
              '余数为 0 时：`num0 = 0` 答案 0，否则答案 9'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '两个特判：`num == 0` 直接返回；模 9 余 0 的正数返回 9',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神把两种情况合并成一个公式 `(num − 1) % 9 + 1`（`num = 0` 仍需特判）'],
    ),
)
