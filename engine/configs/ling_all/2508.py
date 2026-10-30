def _third(S):
    g, x, y = S.get('g'), S.get('x'), S.get('y')
    if S.get('odd') is None or g is None or x is None or y is None or x not in g[y]:
        return None
    for i in range(1, S['n'] + 1):
        if i != x and i != y and x not in g[i] and y not in g[i]:
            return i
    return None


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    n = S['n']
    g = S.get('g') or {}
    odd = S.get('odd')
    x, y = (S.get('x'), S.get('y')) if S.get('odd') is not None else (None, None)
    i = _third(S) if S.get('_line') in (12, 14) else None
    cv.text((x0 + 18, y0 + 4), '图（橙 = 度数为奇数的点，粉框 = x、y，黄框 = 正在试的第三个点 i）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 14
    R = min((x1 - x0) / 2 - 90, (y1 - y0) / 2 - 62)
    pos = {}
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        pos[k + 1] = (cx + R * math.cos(a), cy + R * math.sin(a))
    for a, b in S['edges']:
        hot = x is not None and y is not None and {a, b} == {x, y}
        cv.line([pos[a], pos[b]], T['pink'] if hot else T['border'], 6 if hot else 3)
    if x is not None and y is not None and i is not None and i in pos:
        for t in (x, y):
            cv.dashed(pos[i], pos[t], T['yellow'], 3)
    for v in range(1, n + 1):
        X, Y = pos[v]
        d = len(g.get(v, ())) if odd is not None else 0
        isodd = odd is not None and v in odd
        fill = T['orange'] if isodd else T['panel2']
        if v == x or v == y:
            cv.rect((X - 38, Y - 38, X + 38, Y + 38), outline=T['pink'], width=5, r=38)
        elif v == i:
            cv.rect((X - 38, Y - 38, X + 38, Y + 38), outline=T['yellow'], width=5, r=38)
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=fill, outline=T['border'], width=2, r=30)
        cv.text((X, Y), v, 30, T['bg'] if isodd else T['text'], anchor='mm', bold=True)
        if odd is not None:
            cv.text((X, Y + 52), f'度 {d}', 20, T['orange'] if isodd else T['dim'], anchor='mm', bold=True)


def _odd_txt(S):
    odd = S.get('odd')
    if odd is None:
        return ''
    m = len(odd)
    tail = {0: '已经全是偶数', 2: '一条边修两个点', 4: '两条边刚好配对'}.get(m, '两条边最多改 4 个点 → 不可能')
    return f'奇数度的点 `odd = {odd}`，`m = {m}`：=={tail}=='


CONFIG = dict(
    num=2508, title='添加边使所有节点度数都为偶数', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='按奇点个数分类讨论',
    tags=['灵神题单', '难度分 2060'],
    code='''
class Solution:
    def isPossible(self, n: int, edges: List[List[int]]) -> bool:
        g = defaultdict(set)
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        odd = [i for i, nb in g.items() if len(nb) % 2]
        m = len(odd)
        if m == 0: return True
        if m == 2:
            x, y = odd
            return x not in g[y] or any(
                i != x and i != y and x not in g[i] and y not in g[i]
                for i in range(1, n + 1))
        if m == 4:
            a, b, c, d = odd
            return b not in g[a] and d not in g[c] or \\
                   c not in g[a] and d not in g[b] or \\
                   d not in g[a] and c not in g[b]
        return False
''',
    call='Solution().isPossible(5, [[1,2],[3,4],[4,5],[5,3]])',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_odd_txt, h=70, size=28),
    ],
    watch=[('m', 'm', 'orange'), ('x', 'x', 'pink'), ('y', 'y', 'pink'), ('i', 'i', 'yellow')],
    captions={
        'g = defaultdict(set)': '`g[x]` = 点 x 的邻居集合，用集合方便查「有没有边」',
        'g[x].add(y)': '无向边 `{x}`-`{y}`：两个点互相加入对方的邻居',
        'odd = [': '找出度数为奇数的点：`odd = {odd}`，共 `{len(odd)}` 个',
        'm = len(odd)': '`m = {m}`：一条新边最多改变 2 个点的奇偶，所以 ==m 只可能是 0、2、4==',
        'if m == 0': lambda S, B, r: ('`m = 0`：本来就全是偶数 → `True`' if S.m == 0 else f'`m = {S.m}` 不是 0，往下看'),
        'if m == 2': lambda S, B, r: ('`m = 2`：只有两个奇点，连起来就行；但要先看它们之间==已经有边==没有' if S.m == 2 else f'`m = {S.m}` 不是 2，往下看'),
        'x, y = odd': '两个奇点：`x = {x}`，`y = {y}`',
        'return x not in g[y]': lambda S, B, r: (
            f'`{S.x}` 和 `{S.y}` 之间没有边 → 直接连上 → `True`' if S.x not in S.g[S.y] else
            f'找到 `i = {_third(S)}`：它与 `{S.x}`、`{S.y}` 都没有边 → 连 `{_third(S)}-{S.x}`、`{_third(S)}-{S.y}`，三点度数都变偶 → ==`{r}`==' if r else
            f'`{S.x}` 和 `{S.y}` 之间已有边（不能重边）→ 只能找第三个点 i，分别连 `i-{S.x}` 和 `i-{S.y}`'),
        14: lambda S, B, r: f'枚举 `i = 1..n`：`i` 不能是 x、y 自己，且要与 `{S.x}`、`{S.y}` 都没有边；`i = {_third(S)}` 满足（偶数度 +2 仍是偶数）',
        'i != x and i != y': lambda S, B, r: (
            f'枚举 `i = 1..n`：`i` 不能是 x、y 自己（`1`、`2` 跳过），且要与 `{S.x}`、`{S.y}` 都没有边；`i = {_third(S)}` 满足（它的度数是偶数，+2 仍是偶数）'),
        'if m == 4': '`m = 4`：四个奇点只能两两配对，共 3 种配法',
        'a, b, c, d = odd': '四个奇点 `a,b,c,d = {a},{b},{c},{d}`',
        'return b not in g[a]': '三种配对 `(a-b, c-d)`、`(a-c, b-d)`、`(a-d, b-c)`，任一种两条边都不存在即可 → `{ret}`',
        'return False': '`m = {m}`：奇点太多，两条边修不完 → `False`',
    },
    max_steps=80,
    cards=dict(
        one_liner='数奇点：0、2、4 个才有救，再分类找可连的边',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['无向图 `n` 个点，至多添加 2 条边（不能重边、自环）',
                 '能否让==所有点的度数都变成偶数==，返回 `True/False`',
                 '本视频示例：`n=5, edges=[[1,2],[3,4],[4,5],[5,3]]` → `True`'],
        quote='把度数为奇数的节点记到 odd 中，记 m 为 odd 的长度，分类讨论：如果 m=0，那么已经符合要求。如果 m=2 ……如果 x 和 y 之间有边，那么枚举 [1,n] 的所有不为 x 和 y 的点 i',
        quote_src='—— 灵茶山艾府题解',
        idea=['每加一条边，两个端点的奇偶都翻转：==奇点个数最多减少 2==，两条边最多处理 4 个奇点',
              '`m=2`：x、y 连边；若已有边，找一个偶点 i 同时连 x 和 y（i 度数 +2 仍为偶）',
              '`m=4`：两两配对，3 种配法逐一检查边是否已存在'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：`m=2` 且 x、y 已有边时，第三个点 i 要同时与 x、y 都没有边',
                 '奇数个奇点不会出现（握手定理），所以只需讨论 0/2/4',
                 '本例走的是 `m=2` 且已有边的分支；`m=4`、`m>4` 的分支见代码',
                 '同类：欧拉路径中的奇点配对、构造题的分类讨论'],
    ),
)
