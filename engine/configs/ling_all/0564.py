def _cands(n):
    m = len(n)
    left = int(n[:(m + 1) // 2])
    out = [('长 m-1 的最大回文', 10 ** (m - 1) - 1)]
    out.append(('长 m+1 的最小回文', 10 ** m + 1))
    for d, name in ((-1, 'left-1'), (0, 'left'), (1, 'left+1')):
        s = str(left + d)
        out.append((f'{name} = {left + d}', int(s + s[::-1][m % 2:])))
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    num = int(n)
    cv.text((x0 + 18, y0 + 4), f'5 个候选回文数，取离 num = {num} 最近、且不等于自身的那个', 24, T['muted'], bold=True)
    cur = S['_inner'].get('pal') if S['_inner'].get('pal') is not None else None
    ans = S.get('ans')
    if ans and ans[0] == float('inf'):
        ans = None
    y = y0 + 60
    rh = 70
    for k, (name, v) in enumerate(_cands(n)):
        diff = abs(v - num)
        is_cur = cur == v and S['_line'] in (7, 8, 9, 10)
        is_best = ans is not None and ans[1] == v
        fill = T['green'] if is_best else (T['panel'] if 'panel' in T else (40, 46, 56))
        cv.rect((x0 + 20, y, x1 - 20, y + rh - 8), fill=(36, 42, 52), r=10,
                outline=T['yellow'] if is_cur else (T['green'] if is_best else None), width=4 if (is_cur or is_best) else 1)
        cv.text((x0 + 40, y + (rh - 8) / 2), name, 24, T['muted'], anchor='lm')
        cv.text((x0 + 380, y + (rh - 8) / 2), v, 30, T['text'], anchor='lm', mono=True, bold=True)
        cv.text((x0 + 620, y + (rh - 8) / 2), f'差 {diff}' if diff else '差 0（=num，不能选）', 24,
                T['green'] if is_best else (T['pink'] if not diff else T['cyan']), anchor='lm', bold=True)
        y += rh
    cv.text((x0 + 24, y + 20), 'left 只能在 left−1、left、left+1 里选：其余回文数一定更远', 22, T['orange'], bold=True)


CONFIG = dict(
    num=564, title='寻找最近的回文数', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='枚举左半 ±1 + 两个边界',
    tags=['灵神题单·数学算法'],
    code='''
class Solution:
    def nearestPalindromic(self, n: str) -> str:
        num = int(n)
        ans = (inf, 0)

        def update(pal: int) -> None:
            diff = abs(pal - num)
            if diff > 0:
                nonlocal ans
                ans = min(ans, (diff, pal))

        m = len(n)  # num 的十进制长度
        update(10 ** (m - 1) - 1)  # 十进制长为 m-1 的最大回文数
        update(10 ** m + 1)  # 十进制长为 m+1 的最小回文数

        left = int(n[:(m + 1) // 2])
        # 枚举十进制长为 m 的邻近回文数
        for l in range(left - 1, left + 2):
            s = str(l)
            update(int(s + s[::-1][m % 2:]))

        return str(ans[1])
''',
    call='Solution().nearestPalindromic("123")',
    expect='121',
    views=[
        dict(type='string', var='n', pointers={}, h=170,
             color=lambda S, i, v: 'orange' if 'left' in S and i < (len(S['n']) + 1) // 2 else None),
        dict(type='custom', draw=_draw, h=470),
    ],
    watch=[('num', 'num', 'blue'), ('m', 'm', 'cyan'), ('left', 'left', 'orange'), ('pal', 'pal', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'num = int(n)': '`num = {num}`：后面要和它比差值',
        'ans = (inf, 0)': '`ans = (差值, 回文数)`，初始差值无穷大：用元组 `min` 同时满足==最近==和==相同取小==',
        'diff = abs': '候选 `{pal}` 与 `{num}` 差 =={diff}==',
        'if diff > 0': lambda S, B, r: (f'`diff = {S.diff} > 0`：不是 `n` 自身，可以参选' if S.diff > 0 else '`diff = 0`：就是 `n` 自己，题目不允许 → ==跳过=='),
        'ans = min(': lambda S, B, r: (f'`{S.ans}` 比原来 `{B.ans}` 更近（或同样近但更小）→ ==更新答案==' if S.ans != B.ans else f'没有 `{S.ans}` 更近，答案不变'),
        'm = len(n)': '`m = {m}`：`n` 的位数，决定回文数的长度',
        'update(10 ** (m - 1)': '边界 1：`n = 1000` 这类 → 答案可能是少一位的 `99…9`，候选 `{10 ** (m - 1) - 1}`',
        'update(10 ** m': '边界 2：`n = 999` 这类 → 答案可能是多一位的 `10…01`，候选 `{10 ** m + 1}`',
        'left = int': '左半（奇数位含中心）`left = {left}`：连续回文数的左半边也是连续整数',
        'for l in range': lambda S, B, r: (f'枚举 `left - 1, left, left + 1`：`l = {S.l}`' if S.l != B.get('l') else '三个左半边都试过了，循环结束'),
        's = str(l)': '`l = {l}` 的字符串 `{s}`',
        'update(int(s +': '`{s}` + 反转（`m` 为奇数先去掉中间位）→ 回文数 =={s + s[::-1][m % 2:]}==',
        'return str': '答案 `{ans[1]}`（差值 {ans[0]}）',
    },
    cards=dict(
        one_liner='最近回文数的左半边只可能是 left−1、left、left+1',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['给数字字符串 `n`，返回最近的回文整数，不含自身；同样近返回较小的',
                 '`n` 最长 18 位，不能直接枚举',
                 '示例：`"123"` → `"121"`；`"1"` → `"0"`'],
        quote='设 `n` 的左半（奇数长度时包含中心）为 left。一般地，最近回文数的左半只会在 left-1, left, left+1 中，其余回文数一定比这三个更远。',
        quote_src='—— 灵茶山艾府题解',
        idea=['连续的回文数，左半边是连续整数，所以只看左半边附近',
              '再补两个边界：少一位的 `99…9`，多一位的 `10…01`',
              '共 5 个候选，用元组 `(差值, 回文数)` 取 `min`：差值小优先，相同取小'],
        summary=['时间 `O(log n)`，空间 `O(log n)`（位数 m）',
                 '易错点：不能选 `n` 自己，所以 `update` 里要判 `diff > 0`',
                 '`n = 999` → `1001`，`n = 101` → `99`，靠两个边界候选处理',
                 '`s[::-1][m % 2:]`：奇数位时去掉中间那位，避免重复'],
    ),
)
