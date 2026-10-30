_DATES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_AA, _LA, _AB, _LB = '10-01', '10-31', '10-15', '11-05'


def _g(s):
    return sum(_DATES[:int(s[:2]) - 1]) + int(s[3:])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a1, a2, b1, b2 = _g(_AA), _g(_LA), _g(_AB), _g(_LB)
    cv.text((x0 + 18, y0 + 4), '两个区间画在“第几天”的数轴上（蓝 = Alice，粉 = Bob，黄框 = 交集）', 22, T['muted'], bold=True)
    lo, hi = a1 - 2, b2 + 2
    W = x1 - x0 - 170
    sx = x0 + 130
    sc = W / (hi - lo + 1)
    al, bo = S.get('alice'), S.get('bob')
    rows = [('Alice', a1, a2, T['blue'], y0 + 80, al), ('Bob', b1, b2, T['pink'], y0 + 180, bo)]
    for name, l, r, c, y, ready in rows:
        cv.text((x0 + 20, y + 28), name, 26, c, anchor='lm', bold=True)
        if ready:
            cv.rect((sx, y + 26, sx + W, y + 30), fill=T['border'], r=2)
            cv.rect((sx + (l - lo) * sc, y, sx + (r - lo + 1) * sc, y + 56), fill=c, alpha=200, r=10)
            cv.text((sx + (l - lo) * sc, y - 6), f'{l}', 22, c, anchor='lb', bold=True)
            cv.text((sx + (r - lo + 1) * sc, y - 6), f'{r}', 22, c, anchor='rb', bold=True)
        else:
            cv.text((sx + 10, y + 28), '（还没换算成第几天）', 22, T['dim'], anchor='lm')
    if al and bo:
        L, R = max(al[0], bo[0]), min(al[1], bo[1])
        if R >= L:
            cv.rect((sx + (L - lo) * sc - 3, y0 + 78, sx + (R - lo + 1) * sc + 3, y0 + 250), outline=T['yellow'], width=5, r=12)
            cv.text((sx + (L - lo) * sc, y0 + 262), f'max(左端点) = {L}', 24, T['yellow'], anchor='lt', bold=True)
            cv.text((sx + (R - lo + 1) * sc, y0 + 296), f'min(右端点) = {R}', 24, T['yellow'], anchor='rt', bold=True)
            cv.text((x0 + 20, y0 + 350), f'交集天数 = {R} − {L} + 1 = {R - L + 1}', 30, T['green'], bold=True)
        else:
            cv.text((x0 + 20, y0 + 320), '两个区间没有交集', 30, T['red'], bold=True)


CONFIG = dict(
    num=2409, title='统计共同度过的日子数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='月日转第几天 · 区间交集',
    tags=[],
    code='''
class Solution(object):
    def countDaysTogether(self, arriveAlice, leaveAlice, arriveBob, leaveBob):

        dates = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        s = [0]
        for d in dates[:11]:
            s.append(s[-1] + d)
        
        def get_date(date_s):
            m, d = date_s.split('-')
            return s[int(m) - 1] + int(d)

        alice = [get_date(arriveAlice), get_date(leaveAlice)]
        bob = [get_date(arriveBob), get_date(leaveBob)]

        if alice[1] < bob[0] or bob[1] < alice[0]:
            return 0
        else:
            return min(alice[1], bob[1]) - max(alice[0], bob[0]) + 1
''',
    call=f'Solution().countDaysTogether({_AA!r}, {_LA!r}, {_AB!r}, {_LB!r})',
    expect=17,
    views=[
        dict(type='array', var='s', label='s：每个月开始前已过的天数（前缀和）', cell=80, h=150, index=False,
             color=lambda S, i, v: 'blue' if 'm' in S and i == int(S['m']) - 1 else None),
        dict(type='custom', draw=_draw, h=380),
    ],
    watch=[('m', 'm', 'blue'), ('d', 'd'), ('alice', 'alice', 'blue'), ('bob', 'bob', 'pink')],
    captions={
        'dates = [': '每个月的天数（平年）',
        's = [0]': '`s` 是前缀和：`s[k]` = 前 `k` 个月一共多少天',
        'for d in dates[:11]': lambda S, B, ret: (f'第 {len(S.s)} 个月有 `{S.d}` 天（只遍历前 11 个月，12 月的天数用不上）' if S.d == _DATES[len(S.s) - 1] else '前 11 个月都加完了'),
        's.append': '`s` 追加 `{s[-1]}`：前 `{len(s) - 1}` 个月共 `{s[-1]}` 天',
        'm, d = date_s.split': '`{date_s!r}` 拆成月 `m = {m}`、日 `d = {d}`',
        'return s[int(m) - 1] + int(d)': '前 `{int(m) - 1}` 个月共 `{s[int(m) - 1]}` 天，再加 `{int(d)}` 号 → 第 =={ret}== 天',
        'alice = [': lambda S, B, ret: ('先把 Alice 的到达日、离开日各换算成第几天' if 'alice' not in S else f'`alice` = [到达日, 离开日] = `{S.alice}`'),
        'bob = [': lambda S, B, ret: ('再换算 Bob 的到达日、离开日' if 'bob' not in S else f'`bob` = [到达日, 离开日] = `{S.bob}`'),
        'if alice[1] < bob[0]': lambda S, B, ret: (
            f'有一方的离开日早于另一方的到达日吗？`{S.alice[1]} < {S.bob[0]}` 或 `{S.bob[1]} < {S.alice[0]}`：都不成立 → ==有交集=='
            if not (S.alice[1] < S.bob[0] or S.bob[1] < S.alice[0])
            else '一方的离开日早于另一方的到达日 → 没有交集'),
        'return 0': '没有交集，返回 `0`',
        'return min(alice[1]': '交集 = [较大的左端点, 较小的右端点]：`min({alice[1]}, {bob[1]}) − max({alice[0]}, {bob[0]}) + 1` = `{min(alice[1], bob[1])} − {max(alice[0], bob[0])} + 1` = =={ret}==',
    },
    skip=['m, d = date_s.split'],
    cards=dict(
        one_liner='先排除不相交，再取左端点较大者、右端点较小者',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给出 Alice、Bob 在罗马的两段日期（闭区间，`"MM-DD"`，平年），求同时在罗马的天数',
                 '示例：`08-15~08-18` 与 `08-16~08-19` → `3`',
                 '本视频：`10-01~10-31` 与 `10-15~11-05` → `17`'],
        quote='题目本质上是给出两个区间，求这两个区间交集的长度。不过在这里给出的区间是月-日这种形式的，使用起来不太方便，需要先将其转化为一年中的第几天。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用月份天数的前缀和 `s` 把 `"MM-DD"` 变成第几天',
              '先排除不相交：一个区间的右端 `<` 另一个区间的左端',
              '相交时：左边界取两个左端点的较大值，右边界取两个右端点的较小值'],
        summary=['时间、空间均为 `O(1)`',
                 '闭区间的天数要 `+1`',
                 '`s[int(m) - 1]` 是前 `m-1` 个月的总天数，别写成 `s[int(m)]`',
                 '对比灵神：灵神不单独判断不相交，直接和 `0` 取 `max`'],
    ),
)
