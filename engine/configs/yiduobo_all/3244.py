def _path(S):
    nxt, n = S['nxt'], S['n']
    p, u = [0], 0
    while u != n - 1 and nxt[u] is not None and len(p) <= n:
        u = nxt[u]
        p.append(u)
    return p


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    qs, n = S['queries'], S['n']
    removed = S.get('removed', set())
    active = 'x' in S and 12 <= S.get('_line', 0) <= 22
    cur = (S['x'], S['y']) if active else None
    ci = qs.index([S['x'], S['y']]) if active else (len(S['res']) - 1 if 'res' in S else 0)
    cv.text((x0 + 18, y0 + 4), '城市（上弧 = 新增道路，蓝 = 当前最短路，灰 = 被跳过）', 22, T['muted'], bold=True)
    sx = x0 + 60
    step = (x1 - x0 - 120) / (n - 1)
    yb = y0 + (y1 - y0) * 0.55
    pos = [sx + i * step for i in range(n)]
    for a, (u, v) in enumerate(qs):
        if a <= ci and (a < ci or cur):
            hot = cur and a == ci
            cv.arc_arrow((pos[u], yb - 24), (pos[v], yb - 24), (v - u) * step * 0.2, T['yellow'] if hot else T['green'], 4 if hot else 3, 13)
    p = _path(S)
    for a, b in zip(p, p[1:]):
        if b - a == 1:
            cv.arrow((pos[a] + 22, yb), (pos[b] - 22, yb), T['blue'], 4, 12)
        else:
            cv.arc_arrow((pos[a], yb + 24), (pos[b], yb + 24), -(b - a) * step * 0.2, T['blue'], 4, 13)
    for i in range(n):
        gone = i in removed
        cv.rect((pos[i] - 22, yb - 22, pos[i] + 22, yb + 22), fill=(40, 46, 56) if gone else T['panel2'], outline=T['border'], r=22)
        cv.text((pos[i], yb), i, 26, T['dim'] if gone else T['text'], anchor='mm', bold=True, mono=True)
    cv.text((x0 + 18, y1 - 78), f"当前最短路径长度 = {len(p) - 1}（经过 {len(p)} 个城市）", 26, T['text'], bold=True)
    if cur:
        cv.text((x0 + 18, y1 - 40), f"正在处理新增道路 {cur[0]} → {cur[1]}", 24, T['yellow'], bold=True)


CONFIG = dict(
    num=3244, title='新增道路查询后的最短距离 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='贪心取最外层 · nxt 跳转 + removed',
    tags=['灵神题单', '常用数据结构', '难度分 2270'],
    code='''
class Solution(object):
    def shortestDistanceAfterQueries(self, n, queries):

        nxt = []
        for index in range(1, n):
            nxt.append(index)
        nxt.append(None)

        removed = set()
        res = [n - 1]

        for x, y in queries:
            res.append(res[-1])
            if x in removed or y in removed:
                continue
            
            now = x
            while nxt[now] < y:
                now = nxt[now]
                res[-1] -= 1
                removed.add(now)
            nxt[x] = y
        
        return res[1:]
''',
    call='Solution().shortestDistanceAfterQueries(7, [[2,5],[3,5],[0,5]])',
    expect=[4, 4, 2],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='nxt', pointers={'now': 'blue', 'x': 'pink'}, label='nxt[i]：从 i 出发最优的下一个城市', h=170),
        dict(type='set', var='removed', label='removed：被跳过的城市', h=90),
        dict(type='array', var='res', label='res（res[0] 是初始长度）', h=120,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    skip=['for index in range(1, n)', 'nxt.append(index)'],
    watch=['x', 'y', 'now', ('res', 'res[-1] if "res" in S else None', 'green')],
    captions={
        'nxt.append(None)': '`nxt[i]` = 从城市 i 出发最优的下一个城市，开始都是 `i+1`；最后一个城市没有下一站，记 `None`',
        'removed = set()': '`removed` 记录被捷径跳过的中继城市，以后它们不会再用到',
        'res = [n - 1]': '还没有新路时，最短路径长度 = `n-1 = {n - 1}`',
        'for x, y in queries': '新增道路 `{x}→{y}`',
        'res.append(res[-1])': '先默认沿用上一轮的答案',
        'if x in removed or y in removed': lambda S, B, r: (f'`x={S.x}` 或 `y={S.y}` 已被跳过 → 这是某条==外层道路==里的内层道路，用外层更优，答案不变'
                                                          if (S.x in S.removed or S.y in S.removed) else f'`x={S.x}`、`y={S.y}` 都没被跳过，是新的最外层道路，需要使用'),
        'continue': '直接进入下一条查询',
        'now = x': '从 `x` 出发，沿 `nxt` 一路走到 `y`',
        'while nxt[now] < y': lambda S, B, r: (f'`nxt[{S.now}] = {S.nxt[S.now]} < y = {S.y}`：下一站还没到 y，中间的城市会被跳过'
                                                if S.nxt[S.now] < S.y else f'`nxt[{S.now}] = {S.nxt[S.now]} >= y = {S.y}`：已经到达 y，结束'),
        'now = nxt[now]': '走到 `{now}`',
        'res[-1] -= 1': '跳过一个中继城市，最短路径少 1 步 → `{res[-1]}`',
        'removed.add(now)': '城市 `{now}` 被跳过：加入 `removed`',
        'nxt[x] = y': '`x` 以后直接走到 `y`：`nxt[{x}] = {y}`',
        'return res[1:]': '去掉初始的 `n-1`，答案 `{res[1:]}`',
    },
    cards=dict(
        one_liner='新增道路只有「互不相关」或「完全包含」，只用最外层的',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['`n` 个城市，初始 `i → i+1` 有单向路；依次新增 `x→y`',
                 '保证任意两条新路不会交叉，每次求 `0` 到 `n-1` 的最短路径长度',
                 '示例：`n=5, queries=[[2,4],[0,2],[0,4]]` → `[3,2,1]`'],
        quote='对于互不相关的路径，自然是全部使用，而对于具有完整包含关系的路径，则应该使用最外层的路径。',
        quote_src='—— yiduobo 题解原文',
        idea=['内层道路要用就必须先走到外层起点、再从外层终点出发，不如直接走外层',
              '`nxt[i]` 记录 i 的下一站；采用外层路径时从 `x` 沿 `nxt` 走到 `y`',
              '路过的城市每跳过一个，最短路径减 1，并记入 `removed`'],
        summary=['时间 `O(n+q)`：每个城市最多被跳过一次',
                 '易错：`x` 或 `y` 已在 `removed` 里，说明这是内层道路，直接沿用上一轮答案',
                 '易错：`res` 以 `n-1` 开头，返回时要 `res[1:]`',
                 '`while nxt[now] < y` 里 `nxt[now]` 不会是 `None`，因为 `now < y <= n-1`',
                 '对比灵神：灵神用并查集合并边；yiduobo 直接沿 `nxt` 走一遍',
                 '原文已是 Python 3 可运行的写法，未做改动；本视频示例 `n=7`，`[[2,5],[3,5],[0,5]]` → `[4,4,2]`'],
    ),
)
