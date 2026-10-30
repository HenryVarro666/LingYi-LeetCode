def _mins(s):
    h, m = s.split(':')
    return int(h) * 60 + int(m)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    e1, e2 = S.get('event1'), S.get('event2')
    if not e1 or not e2:
        return
    a1, b1, a2, b2 = _mins(e1[0]), _mins(e1[1]), _mins(e2[0]), _mins(e2[1])
    lo = min(a1, a2) // 60 * 60
    hi = (max(b1, b2) + 59) // 60 * 60
    if hi - lo < 120:
        hi = lo + 120
    lx, rx = x0 + 60, x1 - 60
    sc = (rx - lx) / (hi - lo)
    X = lambda m: lx + (m - lo) * sc
    base = y0 + 330
    cv.line([(lx, base), (rx, base)], T['border'], 2)
    for t in range(lo, hi + 1, 60):
        cv.line([(X(t), base - 6), (X(t), base + 6)], T['border'], 2)
        cv.text((X(t), base + 14), f'{t // 60:02d}:00', 20, T['dim'], anchor='mt', mono=True)
    for (a, b, y, name, c, ev) in ((a1, b1, y0 + 80, 'event1', T['blue'], e1), (a2, b2, y0 + 190, 'event2', T['pink'], e2)):
        cv.rect((X(a), y, X(b), y + 70), fill=c, r=8, alpha=210)
        cv.text((X(a), y - 8), f'{name}  {ev[0]}–{ev[1]}', 24, c, anchor='lb', bold=True)
    s, e = max(a1, a2), min(b1, b2)
    if s <= e:
        cv.line([(X(s), y0 + 60), (X(s), base)], T['green'], 4)
        cv.line([(X(e), y0 + 60), (X(e), base)], T['green'], 4)
        cv.text(((X(s) + X(e)) / 2, base + 62), f'重叠 {s // 60:02d}:{s % 60:02d}–{e // 60:02d}:{e % 60:02d}', 26, T['green'], anchor='mm', bold=True)
    else:
        cv.text(((rx + lx) / 2, y0 + 20), '两段之间有空隙：没有交集', 26, T['red'], anchor='mm', bold=True)


CONFIG = dict(
    num=2446, title='判断两个事件是否存在冲突', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='区间相交 · 字符串直接比较',
    tags=[],
    code='''
class Solution:
    def haveConflict(self, event1: List[str], event2: List[str]) -> bool:
        return event1[0] <= event2[1] and event1[1] >= event2[0]
''',
    call='''r1 = Solution().haveConflict(["01:15","02:00"], ["02:00","03:00"])
r2 = Solution().haveConflict(["01:00","02:00"], ["01:20","03:00"])
r3 = Solution().haveConflict(["10:00","11:00"], ["14:00","15:00"])
[r1, r2, r3]''',
    expect=[True, True, False],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: (f"`{S['event1'][0]} <= {S['event2'][1]}` 且 `{S['event1'][1]} >= {S['event2'][0]}`" if 'event1' in S else ''), size=28),
    ],
    watch=[('event1', 'event1'), ('event2', 'event2')],
    captions={
        'return event1[0]': lambda S, B, r: (
            f"`event1` 开始 `{S.event1[0]}` {'≤' if S.event1[0] <= S.event2[1] else '>'} `event2` 结束 `{S.event2[1]}`；"
            f"`event1` 结束 `{S.event1[1]}` {'≥' if S.event1[1] >= S.event2[0] else '<'} `event2` 开始 `{S.event2[0]}` → "
            + ('==两个条件都成立：有交集，冲突==' if r else '==有一个不成立：一个事件整个在另一个之前，不冲突==')),
    },
    cards=dict(
        one_liner='不相交只有两种：一个整个在另一个前面',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两个闭区间事件，时间是 `HH:MM` 字符串，有公共时刻就算冲突',
                 '示例：`["01:15","02:00"]` 与 `["02:00","03:00"]` → `true`（2:00 相交）',
                 '`["10:00","11:00"]` 与 `["14:00","15:00"]` → `false`'],
        quote='直接看【周赛 316】第一题，画个图你就明白了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['画图：两个区间相交，等价于 ==event1 开始不晚于 event2 结束==，且 ==event1 结束不早于 event2 开始==',
              '`HH:MM` 位数固定，字符串字典序就等于时间先后，不用转成分钟',
              '一行 `and` 搞定'],
        after=[dict(heading='为什么这样判断', lines=['不冲突 = event1 整个在 event2 前面（`event1[1] < event2[0]`）', '或 event1 整个在 event2 后面（`event1[0] > event2[1]`）', '取反后正好是 `event1[0] <= event2[1] and event1[1] >= event2[0]`'])],
        result='三个示例依次是 `True, True, False` ✓',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '闭区间：碰到端点也算冲突，所以用 `<=` 和 `>=`，不是 `<`、`>`',
                 '字符串可直接比较，前提是都补零成固定 5 位',
                 '相似题：2409. 统计共同度过的日子数'],
    ),
)
