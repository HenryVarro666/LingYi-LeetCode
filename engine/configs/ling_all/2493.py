_POS = {0: (0.08, 0.1), 1: (0.4, 0.1), 2: (0.72, 0.1), 3: (0.08, 0.9), 4: (0.4, 0.9)}
_E = [(0, 1), (1, 2), (3, 4)]


def _gdraw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '填充 = 黑白染色（蓝 / 粉）　黄圈 = 本轮 BFS 已访问　橙环 = 当前层　绿环 = 下一层', 21, T['muted'], bold=True)
    W, Hh = x1 - x0 - 300, y1 - y0 - 150
    pt = {k: (x0 + 90 + p[0] * W, y0 + 80 + p[1] * Hh) for k, p in _POS.items()}
    inn = S.get('_inner', {})
    color = S.get('color')
    tm, clock = S.get('time'), S.get('clock', 0)
    tmp, q = inn.get('tmp') or [], inn.get('q') or []
    for u, v in _E:
        cv.line([pt[u], pt[v]], T['dim'], 4)
    for k, (px, py) in pt.items():
        fill, tc = T['panel2'], T['text']
        if color is not None and color[k] == 1:
            fill, tc = T['blue'], T['bg']
        elif color is not None and color[k] == -1:
            fill, tc = T['pink'], T['bg']
        ol, w = T['border'], 3
        if tm is not None and clock and tm[k] == clock:
            ol, w = T['yellow'], 5
        if k in tmp:
            ol, w = T['orange'], 7
        elif k in q and 'q' in inn and 'tmp' in inn:
            ol, w = T['green'], 7
        cv.d.ellipse((px - 32, py - 32, px + 32, py + 32), fill=fill, outline=ol, width=w)
        cv.text((px, py), k + 1, 32, tc, anchor='mm', bold=True)


def _info(S):
    inn = S.get('_inner', {})
    if 'depth' in inn:
        return f"BFS 起点 `{inn.get('start', '?') + 1 if isinstance(inn.get('start'), int) else '?'}`，已走 ==`{inn['depth']}`== 层；累计答案 `{S.get('ans', 0)}`"
    return f"累计答案 `ans = {S.get('ans', 0)}`（每个连通块的最大深度相加）"


CONFIG = dict(
    num=2493, title='将节点分成尽可能多的组', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='二分图判定 + 枚举起点 BFS 求最大深度',
    tags=['灵神题单·图论算法', '难度分 2415'],
    code='''
class Solution:
    def magnificentSets(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x - 1].append(y - 1)
            g[y - 1].append(x - 1)

        time = [0] * n  # 充当 vis 数组的作用（避免在 BFS 内部重复创建 vis 数组）
        clock = 0
        def bfs(start: int) -> int:  # 返回从 start 出发的最大深度
            depth = 0
            nonlocal clock
            clock += 1
            time[start] = clock
            q = [start]
            while q:
                tmp = q
                q = []
                for x in tmp:
                    for y in g[x]:
                        if time[y] != clock:  # 没有在同一次 BFS 中访问过
                            time[y] = clock
                            q.append(y)
                depth += 1
            return depth

        color = [0] * n
        def is_bipartite(x: int, c: int) -> bool:  # 二分图判定，原理见视频讲解
            nodes.append(x)
            color[x] = c
            for y in g[x]:
                if color[y] == c or color[y] == 0 and not is_bipartite(y, -c):
                    return False
            return True

        ans = 0
        for i, c in enumerate(color):
            if c: continue
            nodes = []
            if not is_bipartite(i, 1): return -1  # 如果不是二分图（有奇环），则无法分组
            # 否则一定可以分组
            ans += max(bfs(x) for x in nodes)  # 枚举连通块的每个点，作为起点 BFS，求最大深度
        return ans
''',
    call='Solution().magnificentSets(5, [[1, 2], [2, 3], [4, 5]])',
    expect=5,
    views=[
        dict(type='custom', draw=_gdraw, h=400),
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='array', var='time', label='time[i] == clock 表示本轮 BFS 访问过', cell=70, h=130,
             color=lambda S, i, v: 'yellow' if v and v == S.get('clock') else None),
        dict(type='calls', h=130),
    ],
    watch=[('clock', 'clock', 'yellow'), ('ans', 'ans', 'green'), ('depth', lambda S: S['_inner'].get('depth'), 'orange')],
    skip=['g = [[] for', 'for x, y in edges', 'g[y - 1].append', 'for x in tmp', 'for y in g[x]', 'while q', 'for i, c in enumerate',
          'if c: continue', 'nonlocal clock', 'time[y] = clock', 'time[start] = clock', 'q = []', 'tmp = q', 'color = [0]', 'ans = 0', 'depth = 0'],
    captions={
        'g[x - 1].append': '边 `{x}-{y}`（题目编号从 1 开始，这里转成从 0 开始）：双向登记邻居',
        'time = [0] * n': '`time[i]` 记录 i 最近一次被哪一轮 BFS 访问；==用轮次号代替每次新建 vis 数组==',
        'clock += 1': '新开一轮 BFS：`clock = {clock}`，起点 `{start + 1}` 标记为本轮已访问',
        'q = [start]': '第一层只有起点：`q = [{start + 1}]`',
        'if time[y] != clock': lambda S, B, r: (
            f'邻居 `{S.y + 1}`：`time[{S.y}] = {S.time[S.y]}`，本轮号 `{S.clock}` → ' +
            ('==没访问过==，标记为本轮已访问并放进下一层' if S.time[S.y] != S.clock else '本轮已访问，跳过（不会走回头路）')),
        'q.append(y)': '`{y + 1}` 进入下一层：`q` = `{[v + 1 for v in q]}`',
        'depth += 1': '这一层处理完 → 层数 `depth` = =={depth}==',
        'return depth': lambda S, B, r: f'BFS 结束：从 `{S.start + 1}` 出发最多 =={r}== 层 = 最大组数',
        'nodes.append(x)': '记下连通块里的点 `{x + 1}`，后面逐个当 BFS 起点',
        'color[x] = c': '给 `{x + 1}` 染色 `{c}`',
        'if color[y] == c': lambda S, B, r: (
            f'邻居 `{S.y + 1}` 颜色 `{S.color[S.y]}` 和 `{S.x + 1}` 的 `{S.c}` ' +
            ('相同 → ==奇环==，不是二分图' if S.color[S.y] == S.c else
             ('还没染色 → 递归染成相反色 `{}`'.format(-S.c) if S.color[S.y] == 0 else '不同，没问题'))),
        'return False': '发现冲突 → 无法分组',
        'return True': '`{x + 1}` 的邻居全部染色无冲突 → True',
        'nodes = []': lambda S, B, r: (f'新连通块，从 `{S.i + 1}` 开始；上一块的最大深度已加进 `ans = {S.ans}`' if S.ans else f'第一个连通块，从 `{S.i + 1}` 开始'),
        'if not is_bipartite': '调用 `is_bipartite({B.i + 1}, 1)`：DFS 黑白染色判二分图，同时收集连通块里的点',
        'ans += max': '是二分图 → 一定能分组。把连通块 `{[v + 1 for v in B.nodes]}` 里每个点都当起点跑一遍 BFS，取最大深度加进 `ans`',
        'return ans': '所有连通块的最大深度之和 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='同组 = 同一层：先判二分图，再枚举起点取最大深度',
        complexity='时间 `O(nm)`，空间 `O(n+m)`',
        problem=['`n` 个点（编号 1..n）的无向图，可能不连通；把点分到编号 1..m 的组里',
                 '每条边两端所在组的编号必须恰好差 `1`；求最大的 `m`，不可能则返回 `-1`',
                 '示例（改小）：`n=5`，边 `[[1,2],[2,3],[4,5]]` → `5`'],
        quote='|y-x|=1 这个要求，其实就是 BFS 这张图，让同一层的节点分到同一个编号。……每个连通块的最大深度相加，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`|y-x|=1` ⇔ 按 BFS 层数分组；枚举每个点当起点，取最大层数',
              '图中有奇环就不可能：用 DFS 黑白染色判二分图，冲突返回 `-1`',
              '不同连通块互不影响，各块最大深度==相加=='],
        result='两个连通块：3 层 + 2 层 = 5 组',
        summary=['时间 `O(nm)`，空间 `O(n+m)`',
                 '`time` 数组 + `clock` 轮次号，免得每次 BFS 新建 `vis`',
                 '先判二分图：有奇环直接返回 -1',
                 '起点要枚举连通块内==每个点==，不同起点深度不同',
                 '同类题：785. 判断二分图'],
    ),
)
