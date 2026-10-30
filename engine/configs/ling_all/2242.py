_SC = [5, 2, 9, 8, 4]
_POS = {0: (0.08, 0.55), 1: (0.33, 0.0), 2: (0.5, 0.6), 3: (0.92, 0.15), 4: (0.85, 1.0)}
_E = [(0, 1), (1, 2), (2, 3), (0, 2), (2, 4)]


def _gdraw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '黄 = 正中间的边 x-y　粉 = a（x 的邻居）　青 = b（y 的邻居）　节点下方 = 分数', 21, T['muted'], bold=True)
    W, Hh = x1 - x0 - 140, y1 - y0 - 190
    pt = {k: (x0 + 70 + p[0] * W, y0 + 70 + p[1] * Hh) for k, p in _POS.items()}
    inn = S.get('_inner', {})
    search = 'ans' in S
    x, y, a, b = (inn.get(k) if search else None for k in 'xyab')
    if search and a is not None and b is None and S.get('_line', 0) < 17:
        b = None
    for u, v in _E:
        hot = search and x is not None and {u, v} == {x, y}
        (ux, uy), (vx, vy) = pt[u], pt[v]
        cv.line([(ux, uy), (vx, vy)], T['yellow'] if hot else T['dim'], 6 if hot else 3)
    # a-x and y-b links
    for p, q, col in ((a, x, 'pink'), (y, b, 'cyan')):
        if search and p is not None and q is not None and p != q:
            cv.line([pt[p], pt[q]], T[col], 5)
    for k, (px, py) in pt.items():
        ol, fill, tc = T['border'], T['panel2'], T['text']
        if search and k in (x, y):
            ol, fill = T['yellow'], T['panel2']
        if search and k == a:
            ol, fill = T['pink'], T['pink']; tc = T['bg']
        if search and k == b and k != a:
            ol, fill = T['cyan'], T['cyan']; tc = T['bg']
        cv.d.ellipse((px - 32, py - 32, px + 32, py + 32), fill=fill, outline=ol, width=5)
        cv.text((px, py), k, 32, tc, anchor='mm', bold=True)
        cv.text((px, py + 50), f'分 {_SC[k]}', 22, T['muted'], anchor='mm')


def _top3(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('g')
    cv.text((x0 + 18, y0 + 2), 'g[i]：与 i 相邻、分数最大的至多 3 个点  (分数, 节点)', 22, T['muted'], bold=True)
    if g is None:
        return
    inn = S.get('_inner', {})
    cur = S.get('i') if 'ans' not in S else None
    hx, hy = (inn.get('x'), inn.get('y')) if 'ans' in S else (None, None)
    rh = min(44, (y1 - y0 - 40) / max(1, len(g)))
    for i, vs in enumerate(g):
        yy = y0 + 40 + i * rh
        hot = i == cur or i in (hx, hy)
        if hot:
            cv.rect((x0 + 10, yy, x1 - 10, yy + rh - 4), fill=T['panel2'], r=8)
        cv.text((x0 + 24, yy + rh / 2 - 2), f'g[{i}]', 26, T['yellow'] if hot else T['text'], anchor='lm', bold=True, mono=True)
        cv.text((x0 + 120, yy + rh / 2 - 2), '  '.join(f'({s},{n})' for s, n in vs), 26, T['text'], anchor='lm', mono=True)


CONFIG = dict(
    num=2242, title='节点序列的最大得分', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举中间的边 + 每点保留前三大邻居',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构', '难度分 2304'],
    code='''
class Solution:
    def maximumScore(self, scores: List[int], edges: List[List[int]]) -> int:
        g = [[] for _ in range(len(scores))]
        for x, y in edges:
            g[x].append((scores[y], y))
            g[y].append((scores[x], x))
        for i, vs in enumerate(g):
            if len(vs) > 3: 
                g[i] = nlargest(3, vs)

        # 下面这一段可以简写成一行，为了可读性这里就不写了
        ans = -1
        for x, y in edges:
            for score_a, a in g[x]:
                for score_b, b in g[y]:
                    if y != a != b != x:
                        ans = max(ans, score_a + scores[x] + scores[y] + score_b)
        return ans
''',
    call='Solution().maximumScore([5, 2, 9, 8, 4], [[0, 1], [1, 2], [2, 3], [0, 2], [2, 4]])',
    expect=24,
    views=[
        dict(type='custom', draw=_gdraw, h=330),
        dict(type='custom', draw=_top3, h=260),
    ],
    watch=[('x-y', lambda S: f"{S['_inner']['x']}-{S['_inner']['y']}" if 'ans' in S and 'x' in S['_inner'] else None, 'yellow'),
           ('a', lambda S: S['_inner'].get('a') if 'ans' in S else None, 'pink'),
           ('b', lambda S: S['_inner'].get('b') if 'ans' in S else None, 'cyan'),
           ('ans', 'ans', 'green')],
    skip=['g = [[] for', 'for x, y, in edges', 'g[y].append', 'for i, vs in enumerate', 'for x, y in edges', 'for score_a, a in g[x]', 'for score_b, b in g[y]'],
    captions={
        'g[x].append': '无向边 `{x}-{y}`：互相登记为邻居，同时记下==邻居的分数==：`g[{x}]` 加 `({scores[y]}, {y})`，`g[{y}]` 加 `({scores[x]}, {x})`',
        'if len(vs) > 3': lambda S, B, r: (f'`g[{S.i}]` 有 `{len(S.vs)}` 个邻居 > 3 → 只保留分数最大的 3 个' if len(S.vs) > 3
                                           else f'`g[{S.i}]` 邻居不超过 3 个，全留'),
        'nlargest': '`g[{i}]` = 前三大：`{g[i]}`。==只要 3 个就够==：a 只需躲开 y 和 b',
        'ans = -1': '`ans = -1`：找不到长度 4 的序列就返回 -1',
        'if y != a != b != x': lambda S, B, r: (
            f'中间边 `{S.x}-{S.y}`，两端接 a=`{S.a}`、b=`{S.b}` → `{S.a}-{S.x}-{S.y}-{S.b}`：' + ('四个点互不相同 → 合法' if S.y != S.a != S.b != S.x else
             ('a 就是 y，重复 → 跳过' if S.a == S.y else 'a 和 b 是同一个点，重复 → 跳过' if S.a == S.b else 'b 就是 x，重复 → 跳过'))),
        'ans = max': '`{score_a} + {scores[x]} + {scores[y]} + {score_b}` = {score_a + scores[x] + scores[y] + score_b} → `ans = max({B.ans}, ..) = {ans}`',
        'return ans': lambda S, B, r: f'枚举结束，最大得分 =={r}==',
    },
    max_steps=64,
    cards=dict(
        one_liner='枚举正中间的边，两端各接一个最大的邻居',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['无向图，每个点有分数；找长度为 4 的节点序列 `a-x-y-b`，相邻点有边、点互不相同',
                 '返回序列分数和的最大值，找不到返回 `-1`',
                 '示例：`scores=[5,2,9,8,4]`，5 条边 → `24`'],
        quote='枚举中间的点是最方便的……设序列为 a-x-y-b，枚举 edges 中的每条边，作为序列正中间的那条边，即 x-y。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举中间的边 `x-y`，两端的 a、b 各取邻居里分数最大的',
              'a 要和 `y`、`b` 都不同 → 每个点只需保留==前三大==邻居，a 必在其中',
              '预处理用 `nlargest(3, ...)` 把邻居裁到 3 个，枚举量只有 `m × 3 × 3`'],
        result='最大得分 24（序列 0-1-2-3 之类）',
        summary=['时间 `O(n+m)`（`nlargest` 对固定的 3 近似线性），空间 `O(n+m)`',
                 '`y != a != b != x` 是链式比较，等价于 a≠y、a≠b、b≠x（a≠x、b≠y 由邻居关系自动成立）',
                 '邻居里存 `(分数, 节点)` 元组，nlargest 才能按分数取最大',
                 '没有合法序列时 ans 保持 -1',
                 '同类题：Codeforces 666B（World Tour）'],
    ),
)
