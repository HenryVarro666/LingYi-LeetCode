def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    cv.text((x0 + 18, y0 + 4), f'三个候选：lower / same / upper，各自与 n = {n} 比差值', 24, T['muted'], bold=True)
    I = S['_inner']
    rows = [('lower', 'first_part − 1', I.get('lower'), T['blue']),
            ('same', 'first_part 不变', I.get('same'), T['yellow']),
            ('upper', 'first_part + 1', I.get('upper'), T['pink'])]
    y = y0 + 64
    rh = 96
    ln = S['_line']
    for name, desc, v, c in rows:
        cv.rect((x0 + 20, y, x1 - 20, y + rh - 10), fill=(36, 42, 52), r=10, outline=c if v is not None else None, width=3)
        cv.text((x0 + 44, y + (rh - 10) / 2 - 16), name, 30, c, anchor='lm', bold=True, mono=True)
        cv.text((x0 + 44, y + (rh - 10) / 2 + 22), desc, 21, T['muted'], anchor='lm')
        if v is None:
            cv.text((x0 + 330, y + (rh - 10) / 2), '尚未算出', 24, T['dim'], anchor='lm')
        else:
            d = abs(int(v) - int(n))
            cv.text((x0 + 330, y + (rh - 10) / 2), v, 36, T['text'], anchor='lm', mono=True, bold=True)
            cv.text((x0 + 650, y + (rh - 10) / 2), f'差 {d}' if d else '差 0（就是 n，要舍去）', 26, T['pink'] if not d else T['cyan'], anchor='lm', bold=True)
        y += rh
    if ln >= 27 and 'same_diff' in I:
        cv.text((x0 + 24, y + 10), '比较差值：lower_diff <= upper_diff 时选 lower 或 same，否则选 upper 或 same', 22, T['orange'], bold=True)
        cv.text((x0 + 24, y + 48), f"same_diff = {I['same_diff']}，lower_diff = {I.get('lower_diff', '?')}，upper_diff = {I.get('upper_diff', '?')}", 24, T['text'], mono=True)


CONFIG = dict(
    num=564, title='寻找最近的回文数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='前半部分 −1 / 不变 / +1',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def nearestPalindromic(self, n):

        l = len(n)

        first_part = n[:(l + 1) // 2]
        if l % 2 == 1:
            same = first_part + first_part[::-1][1:]
        else:
            same = first_part + first_part[::-1]

        upper_part = str(int(first_part) + 1)
        if len(first_part) < len(upper_part):
            upper = '1' + '0' * (l - 1) + '1'
        else:
            if l % 2 == 1:
                upper = upper_part + upper_part[::-1][1:]
            else:
                upper = upper_part + upper_part[::-1]
        
        lower_part = str(int(first_part) - 1)
        if first_part == '1' or len(first_part) > len(lower_part):
            lower = '9' * (l - 1)
            if not lower:
                lower = '0'
        else:
            if l % 2 == 1:
                lower = lower_part + lower_part[::-1][1:]
            else:
                lower = lower_part + lower_part[::-1]

        same_diff = abs(int(same) - int(n))
        lower_diff = int(n) - int(lower)
        upper_diff = int(upper) - int(n)
        if lower_diff <= upper_diff:
            if same_diff == 0 or same_diff >= lower_diff:
                return lower
            else:
                return same
        else:
            if same_diff == 0 or same_diff > upper_diff:
                return upper
            else:
                return same
''',
    call='Solution().nearestPalindromic("1000")',
    expect='999',
    views=[
        dict(type='string', var='n', h=170,
             color=lambda S, i, v: 'cyan' if 'l' in S and i < (S['l'] + 1) // 2 else None),
        dict(type='custom', draw=_draw, h=470),
    ],
    watch=[('l', 'l', 'cyan'), ('first_part', 'first_part', 'orange'), ('same', 'same', 'yellow'), ('upper', 'upper', 'pink'), ('lower', 'lower', 'blue')],
    captions={
        'l = len(n)': '`n = {n}`，位数 `l = {l}`',
        'first_part = ': '前半部分 `first_part = {first_part}`（位数为奇数时包含中间那位）：==调前半、后半跟着镜像==，因为高位的代价更大',
        'if l % 2 == 1:': lambda S, B, r: (f'`l = {S.l}` 是奇数：镜像时要去掉中间那位' if S.l % 2 else f'`l = {S.l}` 是偶数：整段前半直接镜像'),
        'same = first_part + first_part[::-1][1:]': '`same` = 前半 `{first_part}` + 反转去掉中间位 = =={same}==',
        'same = first_part + first_part[::-1]': '`same` = 前半 `{first_part}` + 反转 = =={same}==：前半不变的回文数',
        'upper_part = ': '`first_part + 1` = `{upper_part}`',
        'if len(first_part) < len(upper_part)': lambda S, B, r: (f'`{S.first_part}` 加 1 变成 `{S.upper_part}`，多出一位 → 特殊情况（`99…9`）' if len(S.first_part) < len(S.upper_part) else f'`{S.upper_part}` 没有进位变长，正常镜像'),
        'upper = \'1\'': '特殊情况：候选是 `1` + `0` × {l - 1} + `1` = =={upper}==',
        'upper = upper_part + upper_part[::-1][1:]': '`upper` = `{upper_part}` + 反转去掉中间位 = =={upper}==',
        'upper = upper_part + upper_part[::-1]': '`upper` = `{upper_part}` + 反转 = =={upper}==',
        'lower_part = ': '`first_part - 1` = `{lower_part}`',
        'if first_part == \'1\'': lambda S, B, r: (f'`first_part = {S.first_part}` 减 1 少了一位（`100…0` 减 1）→ 特殊情况：候选是 `99…9`' if (S.first_part == '1' or len(S.first_part) > len(S.lower_part)) else '减 1 没有退位变短，正常镜像'),
        'lower = \'9\'': '特殊情况：`lower` = `9` × {l - 1} = =={lower}==',
        'if not lower': lambda S, B, r: ('`l = 1` 时 `9 × 0` 是空串 → 改成 `0`' if not S.lower else f'`lower = {S.lower}` 非空，保持不变'),
        'lower = lower_part + lower_part[::-1][1:]': '`lower` = `{lower_part}` + 反转去掉中间位 = =={lower}==',
        'lower = lower_part + lower_part[::-1]': '`lower` = `{lower_part}` + 反转 = =={lower}==',
        'same_diff = abs': '`same` 与 `n` 的差 = =={same_diff}==（为 0 说明 `same` 就是 `n`，要舍去）',
        'lower_diff = int': '`lower` 比 `n` 小 =={lower_diff}==',
        'upper_diff = int': '`upper` 比 `n` 大 =={upper_diff}==',
        'if lower_diff <= upper_diff': lambda S, B, r: (f'`{S.lower_diff} <= {S.upper_diff}`：lower 更近（相等取小的 lower）→ 在 lower 与 same 之间选' if S.lower_diff <= S.upper_diff else f'`{S.lower_diff} > {S.upper_diff}`：upper 更近 → 在 upper 与 same 之间选'),
        'if same_diff == 0 or same_diff >= lower_diff': lambda S, B, r: (f'`same_diff = {S.same_diff}`：same 不合法或不比 lower 更近 → 选 lower' if (S.same_diff == 0 or S.same_diff >= S.lower_diff) else f'`same_diff = {S.same_diff} < lower_diff`：same 更近 → 选 same'),
        'if same_diff == 0 or same_diff > upper_diff': lambda S, B, r: (f'`same_diff = {S.same_diff}`：same 不合法或比 upper 更远 → 选 upper' if (S.same_diff == 0 or S.same_diff > S.upper_diff) else '`same` 不比 upper 远 → 选 same'),
        'return lower': '返回 `lower` = =={lower}==',
        'return same': '返回 `same` = =={same}==',
        'return upper': '返回 `upper` = =={upper}==',
    },
    cards=dict(
        one_liner='调前半部分让后半镜像：只看前半 −1 / 不变 / +1',
        complexity='时间 `O(L)`，空间 `O(L)`（L 为位数）',
        problem=['给数字字符串 `n`，返回最近的回文整数，不含自身；同样近取小',
                 '示例：`"123"` → `"121"`；`"1"` → `"0"`',
                 '本视频：`"1000"` → `"999"`（特殊情况）'],
        quote='应该调整前半部分让后半部分来适配，因为变动低位数字的代价比变动高位数字的代价要大。',
        quote_src='—— yiduobo 题解原文',
        idea=['把 `n` 分成前半 `first_part` 和后半，只改前半，后半跟着镜像',
              '候选只有三个：前半 `+1`、`不变`、`-1`',
              '三个特殊情况：加 1 进位变长、减 1 退位变短、`same` 恰好等于 `n`'],
        summary=['时间 `O(L)`，空间 `O(L)`',
                 '原文为 Python 2 写法，`n[:(l + 1) / 2]` 的整数除法已改为 `//`',
                 '`same_diff == 0` 要舍去：`n` 本身是回文时不能选自己',
                 '对比灵神：灵神把两个边界当作额外候选，循环里统一处理；yiduobo 在 upper/lower 里分情况特判'],
    ),
)
