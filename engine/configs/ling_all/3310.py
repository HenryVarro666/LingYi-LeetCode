def _graph(cv, box, T, title, POS, EDGES, fill, label=None, ecol=None, elab=None, directed=False, ring=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 21, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 120, y1 - y0 - 110
    P = {k: (x0 + 60 + Wd * a, y0 + 66 + Hd * b) for k, (a, b) in POS.items()}
    R = 30
    for e in EDGES:
        a, b = e[0], e[1]
        col, wd = ecol(e) if ecol else (T['border'], 4)
        (ax, ay), (bx, by) = P[a], P[b]
        if directed:
            d = max(1.0, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5)
            ux, uy = (bx - ax) / d, (by - ay) / d
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 3), by - uy * (R + 3)), col, wd, head=16)
        else:
            cv.line([P[a], P[b]], col, wd)
        if elab:
            mx, my = (ax + bx) / 2, (ay + by) / 2
            s = elab(e)
            cv.rect((mx - 22, my - 16, mx + 22, my + 16), fill=T['bg'], r=8)
            cv.text((mx, my), s, 22, col, anchor='mm', bold=True)
    for k, (px, py) in P.items():
        f = fill(k)
        cv.rect((px - R, py - R, px + R, py + R), fill=f or T['panel2'], outline=T['border'], r=R)
        cv.text((px, py), k if label is None else label(k), 32, T['bg'] if f else T['muted'], anchor='mm', bold=True)
        if ring is not None and ring == k:
            cv.rect((px - R - 10, py - R - 10, px + R + 10, py + R + 10), outline=T['text'], width=5, r=R + 10)


SUS = {1, 2, 3}
POS = {0: (0.05, 0.15), 4: (0.28, 0.15), 5: (0.51, 0.15), 1: (0.76, 0.10), 2: (0.94, 0.85), 3: (0.58, 0.85)}
EDGES = [(1, 2), (2, 3), (3, 1), (0, 4), (4, 5)]


def _draw(cv, S, B, box, T):
    sus = S.get('suspicious')
    sus = set(sus) if sus is not None else set()
    inner = S.get('_inner') or {}
    cur = inner.get('x') if ('y' in inner and 'x' in inner and S.get('_line', 0) in (10, 11, 12, 13)) or S.get('_line', 0) == 10 else None
    done = S.get('_line', 0) >= 17
    _graph(cv, box, T, '方法调用图（箭头 a→b 表示 a 调用 b；红 = 可疑方法，白环 = DFS 正在访问）', POS, EDGES,
           lambda k: T['red'] if k in sus else None, directed=True, ring=cur,
           ecol=lambda e: ((T['red'], 5) if e[0] in sus and e[1] in sus else (T['border'], 4)))


CONFIG = dict(
    num=3310, title='移除可疑的方法', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='DFS 标记可疑方法 + 查入边', tags=['灵神题单·图论算法', '难度分 1711'],
    code='''
class Solution:
    def remainingMethods(self, n: int, k: int, invocations: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for x, y in invocations:
            g[x].append(y)

        # 收集所有可疑方法
        suspicious = set()
        def dfs(x: int) -> None:
            suspicious.add(x)
            for y in g[x]:
                if y not in suspicious:  # 避免无限递归
                    dfs(y)
        dfs(k)

        # 检查是否有【非可疑方法】->【可疑方法】的边
        for x, y in invocations:
            if x not in suspicious and y in suspicious:
                # 无法移除可疑方法
                return list(range(n))

        # 移除所有可疑方法
        return list(set(range(n)) - suspicious)
''',
    call='Solution().remainingMethods(6, 1, [[1,2],[2,3],[3,1],[0,4],[4,5]])',
    expect=[0, 4, 5],
    result_fn=sorted,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='set', var='suspicious', label='suspicious（可疑方法集合）', fmt=lambda x: str(x), h=100),
        dict(type='calls', h=190),
    ],
    watch=['x', ('k', 'k', 'red')],
    captions={
        'g[x].append(y)': '`{x}` 调用 `{y}`：有向边 `{x}→{y}`',
        'suspicious = set()': '`suspicious` 收集所有可疑方法',
        'suspicious.add(x)': '`{x}` 是可疑方法（`k` 或被它直接/间接调用）→ 加入集合',
        'if y not in suspicious': lambda S, B, r: (f'`{S.y}` 还不在集合里 → 继续 DFS' if S.y not in S.suspicious else f'`{S.y}` 已经是可疑方法 → 不再递归，==避免环上无限递归=='),
        'dfs(y)': '递归进入 `{y}`',
        'dfs(k)': '从有 bug 的方法 `k = {k}` 出发 DFS，沿着调用边标记所有可疑方法',
        'if x not in suspicious and y in suspicious': lambda S, B, r: (
            f'边 `{S.x}→{S.y}`：' + ('==正常方法调用了可疑方法==，删不掉！' if (S.x not in S.suspicious and S.y in S.suspicious) else '不是「正常 → 可疑」，没问题')),
        'return list(range(n))': '有正常方法依赖可疑方法 → 一个都不能删，返回全部方法',
        'return list(set(range(n)) - suspicious)': '没有正常方法调用可疑方法 → 全部可疑方法删掉，剩下 ==`{ret}`==',
    },
    max_steps=120,
    cards=dict(
        one_liner='从 k 出发 DFS 标出可疑方法，再查有没有正常方法调用它们',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`invocations[i] = [a, b]` 表示方法 a 调用了方法 b，方法 `k` 有 bug',
                 '`k` 和它直接或间接调用的方法都是==可疑方法==，要全部移除',
                 '若有可疑方法被外面的正常方法调用，则谁都不能删，返回全部',
                 '本例：`n=6, k=1` → `[0,4,5]`'],
        quote='从 k 开始 DFS 图，标记所有可能有 bug 的方法（节点）。遍历 invocations，如果存在从「非可疑方法」到「可疑方法」的边，则删除后无法编译，返回数组 [0,1,2,...,n-1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一步：DFS 求出 `k` 能到达的所有节点 = 可疑集合',
              '第二步：枚举每条边，「非可疑 → 可疑」就说明删不掉',
              '图中可能有环，只 DFS 没访问过的点'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '易错：判断的是==非可疑 → 可疑==这个方向，反过来（可疑调用正常）不影响删除',
                 '环：`if y not in suspicious` 防止无限递归',
                 '题解另有「数组」写法（`is_suspicious` 布尔数组），思路相同',
                 '返回 `list(set(...))` 的顺序不重要，题目允许任意顺序'],
    ),
)
