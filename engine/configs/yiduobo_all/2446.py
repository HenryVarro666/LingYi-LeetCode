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
    author='yiduobo', technique='转成分钟 · 判断起点是否落在对方区间内',
    tags=[],
    code='''
class Solution(object):
    def haveConflict(self, event1, event2):

        start_hour1, start_minute1 = event1[0].split(':')
        end_hour1, end_minute1 = event1[1].split(':')

        start1 = int(start_hour1) * 60 + int(start_minute1)
        end1 = int(end_hour1) * 60 + int(end_minute1)

        start_hour2, start_minute2 = event2[0].split(':')
        end_hour2, end_minute2 = event2[1].split(':')

        start2 = int(start_hour2) * 60 + int(start_minute2)
        end2 = int(end_hour2) * 60 + int(end_minute2)

        return start2 <= start1 <= end2 or start1 <= start2 <= end1
''',
    call='''r1 = Solution().haveConflict(["01:15","02:00"], ["02:00","03:00"])
r2 = Solution().haveConflict(["10:00","11:00"], ["14:00","15:00"])
[r1, r2]''',
    expect=[True, False],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"event1 = [`{S.get('start1', '?')}`, `{S.get('end1', '?')}`] 分钟；event2 = [`{S.get('start2', '?')}`, `{S.get('end2', '?')}`] 分钟" if 'event1' in S else ''), size=26),
    ],
    watch=[('start1', 'start1', 'blue'), ('end1', 'end1', 'blue'), ('start2', 'start2', 'pink'), ('end2', 'end2', 'pink')],
    captions={
        'start_hour1, start_minute1': '把 `event1[0] = "{event1[0]}"` 按冒号拆开：小时 `{start_hour1}`，分钟 `{start_minute1}`',
        'end_hour1, end_minute1': '`event1[1] = "{event1[1]}"` 拆成小时 `{end_hour1}`、分钟 `{end_minute1}`',
        'start1 = ': '转成分钟：`{start_hour1} * 60 + {start_minute1}` = ==`{start1}`==',
        'end1 = ': '`{end_hour1} * 60 + {end_minute1}` = ==`{end1}`==，event1 就是 `[{start1}, {end1}]`',
        'start_hour2, start_minute2': '`event2[0] = "{event2[0]}"` 拆成小时 `{start_hour2}`、分钟 `{start_minute2}`',
        'end_hour2, end_minute2': '`event2[1] = "{event2[1]}"` 拆成小时 `{end_hour2}`、分钟 `{end_minute2}`',
        'start2 = ': '`{start_hour2} * 60 + {start_minute2}` = ==`{start2}`==',
        'end2 = ': '`{end_hour2} * 60 + {end_minute2}` = ==`{end2}`==，event2 就是 `[{start2}, {end2}]`',
        'return start2': lambda S, B, r: (
            f"`start1 = {S.start1}` 在 `[{S.start2}, {S.end2}]` 里吗？{'在' if S.start2 <= S.start1 <= S.end2 else '不在'}；"
            f"`start2 = {S.start2}` 在 `[{S.start1}, {S.end1}]` 里吗？{'在' if S.start1 <= S.start2 <= S.end1 else '不在'} → "
            + ('==有一个起点落在对方区间内：冲突==' if r else '==两个起点都不在对方区间内：不冲突==')),
    },
    cards=dict(
        one_liner='先统一成分钟，再看有没有起点落在对方区间里',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两个闭区间事件，时间是 `HH:MM` 字符串，有公共时刻就算冲突',
                 '示例：`["01:15","02:00"]` 与 `["02:00","03:00"]` → `true`',
                 '本视频再加一个不冲突的：`["10:00","11:00"]` 与 `["14:00","15:00"]` → `false`'],
        quote='先将题目给出的两个时间区间从小时：分钟的表示方法转化为全部由分钟表示，此时问题就变成了给出两个区间，判断二者是否相交。',
        quote_src='—— yiduobo 题解原文',
        idea=['`split(\':\')` 拆出小时和分钟，`小时 * 60 + 分钟` 转成整数',
              '两个区间相交，==必有某个区间的起点落在另一个区间内==',
              '所以只判断 `start2 <= start1 <= end2` 或 `start1 <= start2 <= end1`'],
        result='两个示例依次是 `True, False` ✓',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '闭区间：端点相等也算，必须用 `<=`',
                 '链式比较 `a <= b <= c` 同时检查了两端',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：他直接比较字符串，一行搞定，思路是「不相交只有两种」'],
    ),
)
