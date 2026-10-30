D = ["acd", "bed", "accd"]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    d = S['demand']
    cv.text((x0 + 18, y0 + 4), 'demand：每天需要的展台（Counter = 多重集）', 24, T['muted'], bold=True)
    cs = [Counter(s) for s in d]
    u = cs[0]
    for c in cs[1:]:
        u = u | c
    done = '_ret' in S or S.get('_line') is None
    y = y0 + 60
    for i, (s, c) in enumerate(zip(d, cs)):
        cv.text((x0 + 30, y), f'第 {i} 天  "{s}"', 28, T['text'], mono=True)
        cv.text((x0 + 330, y), '→  ' + '  '.join(f'{k}×{v}' for k, v in sorted(c.items())), 28, T['cyan'], mono=True)
        y += 56
    y += 20
    cv.line([(x0 + 20, y), (x1 - 20, y)], T['border'], 2)
    y += 24
    cv.text((x0 + 30, y), '按位取最大 |', 28, T['yellow'], bold=True)
    cv.text((x0 + 330, y), '→  ' + '  '.join(f'{k}×{v}' for k, v in sorted(u.items())), 28, T['yellow'], mono=True)
    y += 64
    cv.text((x0 + 30, y), 'sum(values) =', 28, T['green'], bold=True)
    cv.text((x0 + 330, y), '→  ' + ' + '.join(str(v) for k, v in sorted(u.items())) + f' = {sum(u.values())}', 28, T['green'], mono=True)


CONFIG = dict(
    num='LCP 66', title='最小展台数量', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='Counter 并集（多重集取最大）',
    code='''
class Solution:
    def minNumBooths(self, demand: List[str]) -> int:
        return sum(reduce(or_, map(Counter, demand)).values())
''',
    setup='from operator import or_',
    call=f'Solution().minNumBooths({D!r})',
    expect=6,
    views=[dict(type='custom', draw=_draw, h=420)],
    watch=[],
    captions={
        'return sum': '`map(Counter, demand)` 把每天变成多重集；`reduce(or_, …)` 逐个取并集（每种展台取最大次数）；`sum(...values())` 加起来 → =={ret}==',
    },
    cards=dict(
        one_liner='展台可跨天复用：每种取单天最大值，再求和',
        complexity='时间 `O(L)`，空间 `O(|Σ|)`（L 为字符总数）',
        problem=['`demand[i]` 是第 i 天要用的展台类型（字符）',
                 '展台可以在不同天重复使用，求最少准备几个',
                 '示例：`["acd","bed","accd"]` → `6`（`abccde`）'],
        quote='`Counter` 本质上表示的是一个多重集，直接用 `|` 就可以计算并集了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每种展台需要的数量 = ==各天需求的最大值==',
              '多重集的并集正好是「每个元素取最大次数」',
              '`reduce(or_, ...)` 把所有天的 Counter 依次并起来，再求和'],
        before=[dict(heading='先看一个小例子', lines=['`Counter("acd") | Counter("accd")`', '= `{a:1, c:2, d:1}`：==每个字母取较大的次数==', '这正是「两天需求合并后至少要备多少」'])],
        after=[dict(heading='展开写就是', lines=['`need = Counter()`，对每天的 `c`：`need |= Counter(c)`', '最后 `sum(need.values())`', '`reduce(or_, …)` 只是把这个循环压成一行']) ],
        summary=['时间 `O(L)`，空间 `O(|Σ|)`',
                 '注意是并集 `|`（取最大），不是加法 `+`（会把各天加起来）',
                 '`or_` 来自 `operator`，`reduce` 来自 `functools`',
                 '一行写完，对应 yiduobo 的手写循环取最大'],
    ),
)
