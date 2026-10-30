def _lead(s):
    k = 0
    while k < len(s) and s[k] == '1':
        k += 1
    return k


def _color(S, i, v):
    p = S.get('p')
    if p is None:
        return None
    k1 = _lead(S['s'])
    if i < p:
        return 'blue' if i < k1 else 'purple'
    if i == p:
        return 'yellow'
    return None


def _parts(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s, p = S.get('s'), S.get('p')
    if not isinstance(s, str) or p is None:
        return
    n = len(s)
    k1 = _lead(s)
    k2 = k1
    while k2 < n and s[k2] == '0':
        k2 += 1
    ln = S.get('_line')
    cv.text((x0 + 18, y0 + 4), '整串被两个 while 切成三块：', 24, T['muted'], bold=True)
    W = x1 - x0 - 80
    sx = x0 + 40
    unit = W / n
    parts = [(0, k1, '开头连续的 1', T['blue'], ln in (5, 6)),
             (k1, k2, '接着连续的 0', T['purple'], ln in (8, 9)),
             (k2, n, '剩下的（有就说明 0 后面还有 1）', T['red'], ln == 11)]
    y = y0 + 60
    for a, b, name, c, on in parts:
        if b <= a:
            continue
        X0, X1 = sx + a * unit, sx + b * unit
        reached = p >= b or (p > a)
        cv.rect((X0 + 4, y, X1 - 4, y + 64), fill=c if (reached or on) else T['panel2'], outline=c, width=3, r=12)
        cv.text(((X0 + X1) / 2, y + 32), s[a:b], 30, T['bg'] if (reached or on) else c, anchor='mm', bold=True, mono=True)
        cv.text(((X0 + X1) / 2, y + 80), name, 20, c, anchor='mt', bold=True)
    if not (p >= k2 and ln in (8, 11)):
        return
    if k2 == n:
        cv.rich(x0 + 24, y + 130, '没有第三块：p 能走到末尾 → ==只有一段 1==', W, size=26, accent=T['green'])
    else:
        cv.rich(x0 + 24, y + 130, f'第三块从下标 `{k2}` 开始：p 停在这里，`p ≠ n` → ==有两段以上==', W, size=26, accent=T['red'])


def _top(S):
    s, p = S.get('s'), S.get('p')
    if p is None:
        return f'`s = "{s}"`'
    ln = S.get('_line')
    if ln in (5, 6):
        return '第一个 while：跳过开头连续的 ==1=='
    if ln in (8, 9):
        return '第二个 while：跳过接下来连续的 ==0=='
    if ln == 11:
        return f'`p = {p}`，`n = {len(s)}`'
    return f'`s = "{s}"`'


def _w1(S, B, ret):
    p, s, n = B.p, S.s, S.n
    if p < n and s[p] == '1':
        return f"`s[{p}] = '1'` → 还在第一段 1 里，继续往后走"
    if p == n:
        return '`p == n`：走到末尾了，整串都是 1'
    return f"`s[{p}] = '0'` → 第一段 1 结束，`p = {p}` 是==第一个 0=="


def _w2(S, B, ret):
    p, s, n = B.p, S.s, S.n
    if p < n and s[p] == '0':
        return f"`s[{p}] = '0'` → 跳过这个 0"
    if p == n:
        return '`p == n`：走到末尾了，0 的后面没有 1'
    return f"`s[{p}] = '1'` → ==0 的后面又出现了 1==，停下"


CONFIG = dict(
    num=1784, title='检查二进制字符串字段', difficulty='Easy', category='字符串',
    author='yiduobo', technique='指针跳过 1 再跳过 0',
    tags=['字节30天'],
    code='''
class Solution(object):
    def checkOnesSegment(self, s):
        n = len(s)
        p = 0
        while p < n and s[p] == '1':
            p += 1

        while p < n and s[p] == '0':
            p += 1

        return p == n
''',
    call='''Solution().checkOnesSegment("1001")
Solution().checkOnesSegment("110")''',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（蓝 = 跳过的 1，紫 = 跳过的 0，黄 = p 停下的位置）', cell=110, h=240,
             pointers={'p': 'pink'}, color=_color),
        dict(type='custom', draw=_parts, h=230),
        dict(type='text', fn=lambda S: '依次运行两个输入：`"1001"` → False，`"110"` → True', size=24),
    ],
    watch=[('p', 'p', 'pink'), ('n', 'n')],
    captions={
        'n = len(s)': '`n = len(s) = {n}`',
        'p = 0': '指针 `p` 从头开始；题目保证 `s[0] = 1`',
        5: _w1,
        6: '`p` → `{p}`',
        8: _w2,
        9: '`p` → `{p}`',
        'return p == n': lambda S, B, ret: (f'`p == n = {S.n}`：一段 1 加一段 0 就走完了 → `True`' if ret
                                            else f'`p = {S.p} ≠ n = {S.n}`：后面还有第二段 1 → `False`'),
    },
    cards=dict(
        one_liner='找到第一个 0，看它后面还有没有 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，==不含前导零==（`s[0]` 一定是 `1`）',
                 '如果 s 包含==零个或一个==由连续 `1` 组成的字段，返回 `true`，否则 `false`',
                 '示例：`"1001"` → `false`（两段 1）；`"110"` → `true`'],
        quote='题目需要找出字符串中是否有非连续的1，由于字符串默认是从1开始的，那么只需要找到0第一次出现的位置，然后判断这个位置后面是否有1出现即可。',
        quote_src='—— yiduobo 题解',
        idea=['第一个 while：跳过开头连续的 1，停在==第一个 0==',
              '第二个 while：跳过接下来连续的 0',
              '能走到末尾 → 0 的后面没有 1 → 只有一段'],
        result='`"1001"` 停在下标 3 → False；`"110"` 走到末尾 → True ✓',
        summary=['时间 `O(n)`：p 只往后走；空间 `O(1)`',
                 '两个 while 都先判断 `p < n`，再读 `s[p]`（短路防越界）',
                 '对比灵神：灵神一行 `"01" not in s`；本质都是检查「0 后面有没有 1」',
                 '原文为 Python 2 风格，代码未改，仅删去 docstring'],
    ),
)
