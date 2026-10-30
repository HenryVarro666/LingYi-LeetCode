def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S.get('s')
    if not isinstance(s, str):
        return
    cv.text((x0 + 18, y0 + 4), f's = "{s}"（蓝 = 1，灰 = 0）', 26, T['muted'], bold=True)
    n = len(s)
    cell = min(110, (x1 - x0 - 80) / max(n, 1))
    sx = x0 + (x1 - x0 - cell * n) / 2
    y = y0 + 56
    for i, ch in enumerate(s):
        X = sx + i * cell
        one = ch == '1'
        cv.rect((X + 6, y, X + cell - 6, y + 96), fill=T['blue'] if one else T['panel2'], r=12)
        cv.text((X + cell / 2, y + 48), ch, 44, T['bg'] if one else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, y + 104), i, 18, T['dim'], anchor='mt', mono=True)
    # 所有相邻两位
    y2 = y + 160
    cv.text((x0 + 18, y2), '逐个检查相邻两位，找 "01"（0 的后面紧跟着 1）：', 24, T['muted'], bold=True)
    y3 = y2 + 50
    hit = None
    for i in range(n - 1):
        pair = s[i:i + 2]
        X = sx + i * cell + cell / 2
        bad = pair == '01'
        if bad and hit is None:
            hit = i
        c = T['red'] if bad else T['border']
        cv.rect((X - cell / 2 + 10, y3 + (i % 2) * 70, X + cell / 2 + cell - 10, y3 + (i % 2) * 70 + 56),
                outline=c, width=4 if bad else 2, r=10, fill=(70, 30, 30) if bad else None)
        cv.text((X + cell / 2, y3 + (i % 2) * 70 + 28), pair, 30, T['red'] if bad else T['muted'], anchor='mm', bold=True, mono=True)
    if n == 1:
        cv.text((sx, y3 + 20), '只有一位，没有相邻的两位', 26, T['muted'])
    y4 = y3 + 170
    if hit is not None:
        cv.rich(x0 + 24, y4, f'下标 `{hit}` 开始出现 ==01==：0 后面还有 1 → 至少两段 1 → `False`', x1 - x0 - 48, size=28,
                accent=T['red'])
    else:
        cv.rich(x0 + 24, y4, '没有 ==01==：形如 `11…100…0`，只有一段 1 → `True`', x1 - x0 - 48, size=28, accent=T['green'])


CONFIG = dict(
    num=1784, title='检查二进制字符串字段', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='找子串 "01"',
    tags=['字节30天'],
    code='''
class Solution:
    def checkOnesSegment(self, s: str) -> bool:
        return "01" not in s
''',
    call='''Solution().checkOnesSegment("1001")
Solution().checkOnesSegment("1")
Solution().checkOnesSegment("1100")''',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', fn=lambda S: '依次运行三个输入：`"1001"` → `"1"` → `"1100"`', size=24),
    ],
    watch=[('s', 's', 'blue')],
    captions={
        'return "01" not in s': lambda S, B, ret: (
            f'`"01"` 不在 `"{S.s}"` 中 → 只有一段连续的 1 → `True`' + ('（只有一个 1 也算一段）' if S.s.count('1') == 1 else '')
            if ret else f'`"01"` 出现在 `"{S.s}"` 的下标 `{S.s.find("01")}` → ==0 的后面还有 1==，至少两段 → `False`'),
    },
    cards=dict(
        one_liner='不含前导零时，出现 "01" 就说明有第二段 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，==不含前导零==（`s[0]` 一定是 `1`）',
                 '如果 s 包含==零个或一个==由连续 `1` 组成的字段，返回 `true`，否则 `false`',
                 '示例：`"1001"` → `false`（两段 1）；`"110"` → `true`'],
        before=[dict(heading='只含一段 1 的 s 长什么样？', lines=[
            '因为不含前导零，第一段 1 一定==从开头开始==',
            '情况一：s 全是 1，例如 `111`',
            '情况二：一段 1 加一段 0，例如 `11…100…0`',
            '有多段 1 时，比如 `1001`：==0 的后面还有 1=='])],
        quote='如果 s 包含多段连续的 1，比如示例 1 的 s = 1001，在 0 的后面还有 1。所以检查 s 是否包含 01 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['出现 `01` ⇔ 某个 0 后面又出现了 1 ⇔ 至少两段 1',
              '没有 `01` ⇔ 形如 `11…100…0` 或全是 1 ⇔ 只有一段',
              '注：只有一个 1 也算一段连续的 1'],
        result='`"1001"` → False，`"1"` → True，`"1100"` → True ✓',
        summary=['时间 `O(n)`，空间 `O(1)`；代码只有一行：`return "01" not in s`',
                 '关键前提：==不含前导零==，否则 `"01"` 本身只有一段，却会被判 false',
                 '只有一个 1 也算一段：`"1"`、`"10"` 都返回 true',
                 '对比 yiduobo：用指针先跳过开头的 1，再跳过 0，看能不能走到末尾'],
    ),
)
