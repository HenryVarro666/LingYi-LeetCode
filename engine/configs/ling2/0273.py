NUM = 1012340
ONES = ("", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen")
TENS = ("", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety")
LARGE = ("", "Thousand", "Million", "Billion")


def _groups(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'num' not in S:
        return
    num = S['num']
    cv.text((x0 + 18, y0 + 4), 'num 每 3 位一段（黄 = 当前段 i）', 24, T['muted'], bold=True)
    w = (x1 - x0 - 60) / 4
    cur = S.get('i')
    for k, i in enumerate(range(3, -1, -1)):
        X = x0 + 20 + k * (w + 6)
        x = num // 10 ** (i * 3) % 1000
        on = cur == i and 'x' in S
        done = cur is not None and i > cur
        fill = T['yellow'] if on else T['panel2']
        cv.rect((X, y0 + 44, X + w, y0 + 124), fill=fill, r=12, outline=T['border'])
        tc = T['bg'] if on else (T['dim'] if done else T['text'])
        cv.text((X + w / 2, y0 + 84), f'{x:03d}' if i < 3 or x else '000', 40, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + w / 2, y0 + 136), LARGE[i] or '（空）', 22, T['yellow'] if on else T['muted'], anchor='mt', bold=True)
        cv.text((X + w / 2, y0 + 166), f'i = {i}', 18, T['dim'], anchor='mt', mono=True)


def _words(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ans = S.get('ans')
    cv.text((x0 + 18, y0 + 4), 'ans（虚线 = 空串，最后会被过滤掉）', 24, T['muted'], bold=True)
    if ans is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    old = len(B.get('ans') or [])
    x, y = x0 + 18, y0 + 44
    for k, s in enumerate(ans):
        label = s if s else '""'
        wd = cv.tlen(label, 26, mono=True) + 26
        if x + wd > x1 - 12:
            x, y = x0 + 18, y + 54
        new = k >= old
        if s:
            cv.rect((x, y, x + wd, y + 44), fill=T['green'] if new else T['panel2'], r=10, outline=T['border'])
            cv.text((x + wd / 2, y + 22), label, 26, T['bg'] if new else T['text'], anchor='mm', mono=True, bold=True)
        else:
            cv.rect((x, y, x + wd, y + 44), outline=T['green'] if new else T['dim'], width=2, r=10)
            cv.text((x + wd / 2, y + 22), label, 26, T['dim'], anchor='mm', mono=True)
        x += wd + 10


def _cap_for(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '四段都处理完了'
    if S.i == 0:
        return '最低的一段（`i = 0`），没有大数单位'
    return f'`i = {S.i}`：处理单位为 `{LARGE[S.i]}` 的这一段'


def _cap_x(S, B, ret):
    return f'`x = num // 10**{S.i * 3} % 1000 = {S.x}`：取出这一段（一定 ==小于 1000==）'


def _cap_x0(S, B, ret):
    if S.x == 0:
        return '`x = 0`：这一段全是 0 → ==整段跳过==，连单位都不加'
    return f'`x = {S.x}` 不是 0 → 拼出这一段'


def _cap_ge100(S, B, ret):
    if S.x >= 100:
        return f'`{S.x} ≥ 100`：有百位'
    return f'`{S.x} < 100`：没有百位'


def _cap_lt20(S, B, ret):
    r = S.x % 100
    if r < 20:
        return f'`x % 100 = {r} < 20`：0～19 每个数==都有专门的单词==，不能拆'
    return f'`x % 100 = {r} ≥ 20`：拆成十位 + 个位'


def _cap_one10(S, B, ret):
    d = S.x % 10
    if d == 0:
        return '个位是 0 → `ones[0] = ""`，加入一个==空串=='
    return f'个位 `{d}` → `"{ONES[d]}"`'


def _cap_large(S, B, ret):
    if S.i == 0:
        return '最后一段没有单位：`large_numbers[0] = ""`，加入空串'
    return f'加上大数单位 `"{LARGE[S.i]}"`'


CONFIG = dict(
    num=273, title='整数转换英文表示', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='拆成若干小于 1000 的数',
    tags=['字节30天'],
    code='''
ones = ("", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen")
tens = ("", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety")
large_numbers = ("", "Thousand", "Million", "Billion")

class Solution:
    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"

        ans = []

        # 1_234_567_811
        # One Billion + Two Hundred Thirty Four Million + Five Hundred Sixty Seven Thousand + Eight Hundred Eleven
        # 拆分后，都是小于 1000 的数 + 大数单位（Billion/Million/Thousand/空）
        for i in range(len(large_numbers) - 1, -1, -1):
            x = num // 10 ** (i * 3) % 1000
            if x == 0:
                continue
            # 百位
            if x >= 100:
                ans.append(ones[x // 100])
                ans.append("Hundred")
            # 十位和个位
            if x % 100 < 20:  # 特殊处理小于 20 的数
                ans.append(ones[x % 100])
            else:
                ans.append(tens[x // 10 % 10])
                ans.append(ones[x % 10])
            ans.append(large_numbers[i])  # 大数单位

        return ' '.join(s for s in ans if s)
''',
    call=f'Solution().numberToWords({NUM})',
    expect='One Million Twelve Thousand Three Hundred Forty',
    views=[
        dict(type='text', fn=lambda S: f"`num = {S['num']:,}`" if 'num' in S else '', h=60),
        dict(type='custom', draw=_groups, h=200),
        dict(type='custom', draw=_words, h=190),
        dict(type='text', fn=lambda S: '过滤空串后拼接：==' + ' '.join(w for w in S['ans'] if w) + '=='
             if S.get('ans') else '', h=100, size=26, lines=2),
    ],
    watch=[('i', 'i', 'yellow'), ('x', 'x', 'yellow'), ('len(ans)', 'len(ans)')],
    skip=['continue'],
    captions={
        'if num == 0': '`num = {num:,}` 不为 0（`num = 0` 要特判，返回 `"Zero"`）',
        'ans = []': '`ans` 依次收集单词，最后用空格拼接',
        'for i in range': _cap_for,
        'x = num //': _cap_x,
        'if x == 0': _cap_x0,
        'if x >= 100': _cap_ge100,
        'ans.append(ones[x // 100])': lambda S, B, ret: f'百位 `{S.x // 100}` → `"{ONES[S.x // 100]}"`',
        'ans.append("Hundred")': '再跟一个 `"Hundred"`',
        'if x % 100 < 20': _cap_lt20,
        'ans.append(ones[x % 100])': lambda S, B, ret: f'`ones[{S.x % 100}]` = `"{ONES[S.x % 100]}"`',
        'ans.append(tens[x // 10 % 10])': lambda S, B, ret: f'十位 `{S.x // 10 % 10}` → `"{TENS[S.x // 10 % 10]}"`',
        'ans.append(ones[x % 10])': _cap_one10,
        'ans.append(large_numbers[i])': _cap_large,
        'return': '过滤掉空串，用空格拼接 → =={ret}==',
    },
    cards=dict(
        one_liner='每 3 位一段，每段都是“小于 1000 的数 + 大数单位”',
        complexity='时间 `O(1)`（固定 4 段），空间 `O(1)`',
        problem=['把非负整数 `num`（`≤ 2^31 - 1`）转成英文表示',
                 '示例：`123` → `"One Hundred Twenty Three"`',
                 '`12345` → `"Twelve Thousand Three Hundred Forty Five"`',
                 '演示：`1012340` → `"One Million Twelve Thousand Three Hundred Forty"`'],
        result='运行结束，返回 `"One Million Twelve Thousand Three Hundred Forty"` ✓',
        quote='每一段都是一个==小于 1000 的数 x==，跟着一个大数单位（Billion/Million/Thousand/空）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x = 0`：跳过；`x ≥ 100`：先加百位单词和 `Hundred`',
              '`x % 100 < 20`：直接查 `ones`；否则拆成十位 `tens` + 个位 `ones`',
              '`ones[0]` 和 `large_numbers[0]` 是空串，==最后统一过滤==，省去判断'],
        summary=['时间 `O(1)`：最多 4 段，每段常数个单词',
                 '易错：`num = 0` 要特判返回 `"Zero"`；其他时候 0 不出现在结果里',
                 '易错：`10～19` 不能拆成十位 + 个位',
                 '技巧：先放空串、最后 `join` 时过滤，空格就不会多也不会少',
                 '相似题：12. 整数转罗马数字'],
    ),
)
