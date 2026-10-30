PTS = [[2, 2], [-1, -2], [-4, 4], [-3, 1], [3, -3]]
LAB = 'abdca'
LC = {'a': 'pink', 'b': 'blue', 'c': 'green', 'd': 'purple'}


def _plot(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    R = 5
    side = min(x1 - x0 - 60, y1 - y0 - 40)
    cx, cy = (x0 + x1) / 2 - 150, (y0 + y1) / 2
    u = side / (2 * R)
    P = lambda x, y: (cx + x * u, cy - y * u)
    for k in range(-R + 1, R):
        cv.line([P(k, -R + 0.5), P(k, R - 0.5)], T['border'] if k else T['dim'], 1 if k else 2)
        cv.line([P(-R + 0.5, k), P(R - 0.5, k)], T['border'] if k else T['dim'], 1 if k else 2)
    rank, p, q = S.get('rank'), S.get('p'), S.get('q')
    vis = S.get('vis', set())
    done = set(rank[:max(p, q if q is not None else 0)]) if rank is not None and p is not None else set()
    cur = rank[q] if rank is not None and q is not None and q < len(rank) and S['_line'] in (11, 12, 13, 14) else None
    if rank is not None and p is not None and p < len(rank):
        h = S['dis'][rank[p]]
        (ax, ay), (bx, by) = P(-h, h), P(h, -h)
        cv.rect((ax, ay, bx + 1, by + 1), fill=T['yellow'], alpha=30)
        for p0, p1 in (((ax, ay), (bx, ay)), ((bx, ay), (bx, by)), ((bx, by), (ax, by)), ((ax, by), (ax, ay))):
            cv.dashed(p0, p1, T['yellow'], 3)
        cv.text((bx + 6, ay - 4), f'半边长 {h}', 20, T['yellow'], anchor='lb', bold=True)
    for i, ((x, y), c) in enumerate(zip(PTS, LAB)):
        X, Y = P(x, y)
        col = T[LC[c]]
        if i == cur:
            cv.rect((X - 26, Y - 26, X + 26, Y + 26), outline=T['yellow'], width=5, r=26)
        alpha = 255 if (i in done or i == cur or rank is None) else 120
        cv.rect((X - 18, Y - 18, X + 18, Y + 18), fill=col, r=18, alpha=alpha)
        cv.text((X, Y), c, 24, T['bg'], anchor='mm', bold=True)
        cv.text((X + 24, Y - 22), f'dis={max(abs(x), abs(y))}', 20, T['muted'], anchor='lm', mono=True)
    lx = cx + R * u + 30
    cv.text((lx, y0 + 30), '点 (x, y) 在正方形内', 22, T['muted'], bold=True)
    cv.text((lx, y0 + 60), '⇔ 半边长 ≥ max(|x|, |y|)', 22, T['text'])
    cv.text((lx, y0 + 110), '黄框：当前这一组距离', 22, T['yellow'], bold=True)
    cv.text((lx, y0 + 140), '对应的正方形', 22, T['yellow'], bold=True)


def _order(S):
    if 'rank' not in S:
        return []
    return [f"{S['s'][i]}·{S['dis'][i]}" for i in S['rank']]


def _ocol(S, i, v):
    p, q = S.get('p'), S.get('q')
    if p is None:
        return None
    if i < p:
        return 'green'
    if q is not None and p <= i < q:
        return 'cyan'
    return None


def _inner(S, B, ret):
    if S.q >= len(S.rank):
        return '`q` 走到末尾，这一组结束'
    a, b = S.dis[S.rank[S.p]], S.dis[S.rank[S.q]]
    if a == b:
        return f'`dis[rank[q]] = {b}` 与本组距离 `{a}` 相同：==半边长一到，同组的点一起进来=='
    return f'`dis[rank[q]] = {b} ≠ {a}`：下一组距离更大，本组结束'


def _dup(S, B, ret):
    c = S.s[S.rank[S.q]]
    if c in S.vis:
        return f'标签 `{c!r}` 已在 `vis` 中：框住这一组就==出现重复标签=='
    return f'标签 `{c!r}` 还没出现过'


CONFIG = dict(
    num=3143, title='正方形中的最多点数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='按距离排序 · 枚举前缀',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1697'],
    code='''
class Solution(object):
    def maxPointsInsideSquare(self, points, s):

        dis = [max(abs(x), abs(y)) for x, y in points]

        rank = sorted(range(len(points)), key=lambda d:dis[d])
        p = 0
        vis = set()
        while p < len(rank):
            q = p
            while q < len(rank) and dis[rank[p]] == dis[rank[q]]:
                if s[rank[q]] in vis:
                    return p
                vis.add(s[rank[q]])
                q += 1
            
            p = q
        
        return p
''',
    call=f'Solution().maxPointsInsideSquare({PTS}, {LAB!r})',
    expect=2,
    views=[
        dict(type='custom', draw=_plot, h=420),
        dict(type='array', var=_order, label='按 dis 排序后的点（标签·距离；绿 = 已放入，青 = 本组已检查）',
             cell=110, h=170, color=_ocol, pointers={'p': 'blue', 'q': 'pink'}),
        dict(type='set', var='vis', label='vis：已放入的标签', fmt=lambda x: repr(x), h=100),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink')],
    captions={
        'dis = [': '每个点的 `dis = max(|x|, |y|)`：半边长至少为它才能框住该点 → `dis = {dis}`',
        'rank = sorted': '按 `dis` 从小到大排序：合法正方形里的点==必然是排序后的一个前缀==',
        'p = 0': '`p`：前缀长度，也就是目前已放进正方形的点数',
        'vis = set()': '`vis` 记录前缀中出现过的标签',
        'while p < len(rank)': lambda S, B, r: (f'还有点没放：从 `p = {S.p}` 开始取下一组' if S.p < len(S.rank) else '全部点都放进来了'),
        'q = p': '`q = p = {q}`：同一距离的点必须==整组==一起加入',
        'while q < len(rank) and': _inner,
        'if s[rank[q]] in vis': _dup,
        'return p': '这一组放不进来 → 最多只能放前 `p` 个点：=={ret}==',
        'vis.add': '`vis` 加入标签 `{s[rank[q]]!r}`',
        'q += 1': '`q` → {q}',
        'p = q': '整组合法：前缀扩展到 `p = {p}`',
    },
    cards=dict(
        one_liner='按 max(|x|,|y|) 排序，答案一定是一个前缀；同距离的点整组判断',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['平面上若干点，`s[i]` 是第 `i` 个点的标签',
                 '中心在原点、边平行坐标轴的正方形内（含边界）==不能有同标签的两点==，求最多包含几个点',
                 '示例：`[[2,2],[-1,-2],[-4,4],[-3,1],[3,-3]], "abdca"` → `2`'],
        quote='当正方形边长的一半大于等于max(abs(x), abs(y))时，就说明(x, y)处于正方形中……合法的正方形中包含的点==必然是排序后点的一个前缀==。',
        quote_src='—— yiduobo 题解原文',
        idea=['正方形越大，框住的点只多不少：按距离排序后，框住的是一个前缀',
              '距离相同的点会被==同时框进来==，所以按组扩展前缀',
              '组内一出现重复标签，就返回这一组之前的点数 `p`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：同一距离要整组加入，不能逐点返回 `q`',
                 '返回的是 `p`（组起点），不是 `q`',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神维护「次小距离的最小值」`min2`，`O(n)` 一次遍历'],
    ),
)
