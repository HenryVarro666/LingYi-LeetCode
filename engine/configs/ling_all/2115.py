import math as _m


def _gdraw(cv, box, T, pos, edges, state, sub=None, hot=None, title='', R=30, fs=26):
    """有向图：pos={名字:(fx,fy)}，edges=[(a,b)]，state={名字:颜色名或None}，sub={名字:下方小字}，hot=高亮边 (a,b)"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    half = {k: max(R, (cv.tlen(k, fs, bold=True) + 30) / 2) for k in pos}
    mx = max(half.values())
    w, h = x1 - x0 - 2 * mx - 40, y1 - y0 - 2 * R - 100
    P = {k: (x0 + 20 + mx + fx * w, y0 + 50 + R + fy * h) for k, (fx, fy) in pos.items()}

    def edge_pt(k, ux, uy, pad):
        a, b = half[k] + pad, R + pad
        t = 1 / _m.sqrt((ux / a) ** 2 + (uy / b) ** 2)
        return t

    for a, b in edges:
        if a not in P or b not in P:
            continue
        (ax, ay), (bx, by) = P[a], P[b]
        d = _m.hypot(bx - ax, by - ay) or 1
        ux, uy = (bx - ax) / d, (by - ay) / d
        ta, tb = edge_pt(a, ux, uy, 3), edge_pt(b, ux, uy, 6)
        on = hot is not None and (a, b) == tuple(hot)
        cv.arrow((ax + ux * ta, ay + uy * ta), (bx - ux * tb, by - uy * tb),
                 T['yellow'] if on else T['dim'], width=6 if on else 3, head=16 if on else 13)
    for k, (cx, cy) in P.items():
        c = state.get(k)
        fill = T[c] if c else T['panel2']
        cv.rect((cx - half[k], cy - R, cx + half[k], cy + R), fill=fill, outline=T['border'], width=3, r=R)
        cv.text((cx, cy), k, fs, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if sub and sub.get(k) not in (None, ''):
            cv.text((cx, cy + R + 6), sub[k], 22, T['muted'], anchor='mt', bold=True)


SUP = ['yeast', 'flour', 'meat']
REC = ['bread', 'sandwich', 'pizza']
ING = [['yeast', 'flour'], ['bread', 'meat'], ['cheese', 'bread']]
POS = {'yeast': (0.0, 0.05), 'flour': (0.0, 0.3), 'meat': (0.0, 0.62), 'cheese': (0.0, 0.95),
       'bread': (0.38, 0.2), 'sandwich': (0.8, 0.45), 'pizza': (0.8, 0.95)}
EDGES = [(s, r) for r, ing in zip(REC, ING) for s in ing]
ORDER = SUP + ['bread', 'sandwich']   # 入队（= 出队）顺序


def _cur(S):
    """刚被 popleft 出来的原材料；还没开始出队时为 None"""
    if 'q' not in S or 'ans' not in S:
        return None
    ever = len(SUP) + len(S['ans'])
    r = S.get('r')
    if r is not None and r in S['q'] and r not in S['ans']:
        ever += 1          # q.append(r) 已执行、ans.append(r) 还没执行
    k = ever - len(S['q']) - 1
    return ORDER[k] if 0 <= k < len(ORDER) else None


def _draw(cv, S, B, box, T):
    q, ans, deg = S.get('q'), S.get('ans'), S.get('deg')
    cur = _cur(S) if 12 <= S.get('_line', 0) <= 16 else None
    st, sub = {}, {}
    for k in POS:
        if k in SUP:
            st[k] = 'blue'
        if q is not None and k in q:
            st[k] = 'cyan'
        if ans is not None and k in ans:
            st[k] = 'green'
        if k == cur:
            st[k] = 'yellow'
        if k in REC and deg is not None and k in deg:
            sub[k] = f'还缺 {deg[k]}'
            if k in (ans or []):
                sub[k] = ''
    hot = None
    if cur is not None and S.get('r') is not None and (cur, S['r']) in EDGES:
        hot = (cur, S['r'])
    _gdraw(cv, box, T, POS, EDGES, st, sub, hot, '蓝 原有材料 · 青 在队列 · 黄 刚出队 · 绿 能做出', R=34)


CONFIG = dict(
    num=2115, title='从给定原材料中找到所有可以做出的菜', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='拓扑排序 · 初始原材料当队列',
    tags=['灵神题单', '图论算法', '难度分 1679'],
    code='''
class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        g = defaultdict(list)
        deg = {}
        for r, ing in zip(recipes, ingredients):
            for s in ing:
                g[s].append(r)  # 从这道菜的原材料向这道菜连边
            deg[r] = len(ing)
        ans = []
        q = deque(supplies)  # 拓扑排序（用初始原材料当队列）
        while q:
            for r in g[q.popleft()]:
                deg[r] -= 1
                if deg[r] == 0:  # 这道菜的所有原材料我们都有
                    q.append(r)
                    ans.append(r)
        return ans
''',
    call="Solution().findAllRecipes(['bread','sandwich','pizza'], [['yeast','flour'],['bread','meat'],['cheese','bread']], ['yeast','flour','meat'])",
    expect=['bread', 'sandwich'],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='queue', var='q', label='q（待处理的原材料 / 已做出的菜）', h=130),
        dict(type='map', var='deg', label='deg（每道菜还缺几种原材料）', h=200),
    ],
    watch=[('ans', 'ans', 'green'), ('r', 'r', 'yellow')],
    skip=['deg = {}', 'ans = []'],
    captions={
        'g = defaultdict': '`g[s]`：原材料 `s` 被哪些菜用到（图的邻接表）',
        'for r, ing in zip': lambda S, B, r_: ('三道菜都连好边了' if B.get('r') == S.r and 'deg' in B and S.r in B.deg
                                               else f'看菜 `{S.r}`，它需要 `{S.ing}`'),
        'g[s].append': '`{s}` → `{r}` 连边：`g[{s!r}]` = {g[s]}',
        'deg[r] = len(ing)': '`{r}` 一共需要 `{deg[r]}` 种原材料 → 入度 `deg[{r!r}] = {deg[r]}`',
        'q = deque': '把 `supplies` 直接当队列初值：这些原材料==随时能用==（入度为 0）',
        'while q': lambda S, B, r: (f'队列里还有 `{len(S.q)}` 个，继续' if S.q else '队列空了：再也没有新东西可用 → 结束'),
        'for r in g[q.popleft()]': lambda S, B, r_: (
            f'`{_cur(S)}` 出队，用到它的菜：`{S.g[_cur(S)]}`' if len(S.q) < len(B.q)
            else ('用到它的菜都处理完了，回到 while' if B.get('r') == S.r else f'下一道用到它的菜：`{S.r}`')),
        'deg[r] -= 1': lambda S, B, r_: f'`{_cur(S)}` 用掉了：`{S.r}` 还缺 `{S.deg[S.r]}` 种原材料',
        'if deg[r] == 0': lambda S, B, r_: (f'`deg[{S.r!r}] = 0`：原材料凑齐了 → ==这道菜能做=='  if S.deg[S.r] == 0
                                            else f'`deg[{S.r!r}] = {S.deg[S.r]}` > 0：还缺原材料，先等着'),
        'q.append(r)': '`{r}` 也能当别的菜的原材料 → 入队',
        'ans.append(r)': '记入答案：`ans` = {ans}',
        'return ans': '队列空了，能做的菜 `{ans}`；`pizza` 缺 `cheese`，`deg` 永远到不了 0',
    },
    cards=dict(
        one_liner='原材料入队，用掉就减一，缺口归零的菜也入队',
        complexity='时间 `O(L)`（L 为所有原材料数之和），空间 `O(L)`',
        problem=['`recipes[i]` 需要 `ingredients[i]` 里的全部原材料；菜也可以当别的菜的原料',
                 '`supplies` 里的原材料无限多，返回所有能做出的菜',
                 '本视频：3 道菜，`pizza` 缺 `cheese` → `[bread, sandwich]`'],
        quote='直接用输入的 supplies 当作队列的初始元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['原材料 → 菜连有向边，`deg[菜]` = 还缺几种原材料',
              '初始 `supplies` 都能用，直接当拓扑排序的起点队列',
              '出队一个，所有用它的菜 `deg` 减一；==减到 0 就能做==，入队并记入答案'],
        summary=['时间、空间都是 `O(L)`，`L` 是 `ingredients` 总长度加 `supplies` 长度',
                 '`deg` 只记菜，不记原材料：队列里的原材料天然入度为 0',
                 '成环（互相依赖）的菜 `deg` 永远减不到 0，自然不会进答案',
                 '同类题：210 课程表 II、310 最小高度树'],
    ),
)
