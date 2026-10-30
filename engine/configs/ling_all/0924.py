GRAPH = [[1, 1, 0, 0, 0], [1, 1, 1, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]]
POS = {0: (0.04, 0.15), 1: (0.24, 0.85), 2: (0.44, 0.15), 3: (0.72, 0.85), 4: (0.96, 0.15)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('graph')
    if not g or 'vis' not in S:
        return
    st = S['st']
    vis = S['vis']
    inn = S['_inner']
    cur = inn.get('x') if 'y' in inn or 'conn' in inn or 'size' in inn else None
    gw = x1 - x0
    R = 34

    def P(u):
        fx, fy = POS[u]
        return x0 + 60 + fx * (gw - 120), y0 + 90 + fy * (y1 - y0 - 390)

    n = len(g)
    for i in range(n):
        for j in range(i + 1, n):
            if g[i][j]:
                hot = cur in (i, j) and inn.get('y') in (i, j) and inn.get('y') != cur
                cv.line([P(i), P(j)], T['yellow'] if hot else T['muted'], 7 if hot else 3)
    for u in range(n):
        X, Y = P(u)
        seen = vis[u]
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['green'] if seen else T['panel2'],
                     outline=T['yellow'] if u == cur else (T['red'] if u in st else T['border']),
                     width=7 if u == cur else (5 if u in st else 2))
        cv.text((X, Y), u, 30, T['bg'] if seen else T['text'], anchor='mm', bold=True)
        if u in st:
            cv.text((X, Y + R + 12), '感染源', 20, T['red'], anchor='mt', bold=True)
    cv.text((x0 + 20, y0 + 14), '红圈 = 在 initial 中，绿 = 已访问，黄圈 = 当前 x', 20, T['dim'])
    cv.rect((x0 + 20, y1 - 150, x1 - 20, y1 - 14), fill=T['panel2'], r=10)
    nid = S.get('node_id')
    stxt = '（还没找到感染源）' if nid == -1 else ('（连通块里已有 ≥2 个感染源）' if nid == -2 else f'（只有感染源 {nid}）')
    cv.text((x0 + 40, y1 - 132), f"本块状态 node_id = {nid}  {stxt}" if nid is not None else '本块状态：—', 24,
            T['cyan'], bold=True)
    cv.text((x0 + 40, y1 - 94), f"本块大小 size = {S.get('size', '—')}", 24, T['text'])
    cv.text((x0 + 40, y1 - 56), f"当前最优：ans = {S.get('ans', '—')}，max_size = {S.get('max_size', '—')}", 24, T['green'], bold=True)


def _ifd(S, B, ret):
    y = S.y
    if not S.conn:
        return f'`graph[{S.x}][{y}] = 0`：{y} 和 {S.x} 不相连'
    if B.vis[y]:
        return f'`{y}` 和 {S.x} 相连，但已访问过 → 跳过'
    return f'`{y}` 和 {S.x} 相连且没访问过 → 递归进去'


def _upd(S, B, ret):
    if S.node_id < 0:
        return '`node_id = -2`：这个连通块有 ≥2 个感染源，移除谁都救不了 → 不考虑'
    return (f'`node_id = {S.node_id} ≥ 0`：只有一个感染源。大小 `{S.size}` vs 目前最大 `{B.max_size}`'
            + ('，更大 → 更新答案' if S.size > B.max_size else '，不更大 → 不更新'))


CONFIG = dict(
    num=924, title='尽量减少恶意软件的传播', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='DFS 求连通块 · 状态机记感染源',
    tags=['灵神题单', '图论算法', '难度分 1869'],
    code='''
class Solution:
    def minMalwareSpread(self, graph: List[List[int]], initial: List[int]) -> int:
        st = set(initial)
        vis = [False] * len(graph)
        def dfs(x: int) -> None:
            vis[x] = True
            nonlocal node_id, size
            size += 1
            # 按照状态机更新 node_id
            if node_id != -2 and x in st:
                node_id = x if node_id == -1 else -2
            for y, conn in enumerate(graph[x]):
                if conn and not vis[y]:
                    dfs(y)

        ans = -1
        max_size = 0
        for x in initial:
            if vis[x]:
                continue
            node_id = -1
            size = 0
            dfs(x)
            if node_id >= 0 and (size > max_size or size == max_size and node_id < ans):
                ans = node_id
                max_size = size
        return min(initial) if ans < 0 else ans
''',
    call=f'Solution().minMalwareSpread({GRAPH}, [1, 2, 3])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=450),
        dict(type='calls', h=170),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'yellow'), ('node_id', 'node_id', 'cyan'), ('size', 'size', 'blue'),
           ('ans', 'ans', 'green'), ('max_size', 'max_size', 'green')],
    skip=['st = set', 'vis = [False]', 'for y, conn in enumerate', 'ans = -1', 'max_size = 0', 'continue', 'def dfs'],
    max_steps=90,
    captions={
        'vis[x] = True': '访问 `{x}`，标记 `vis[{x}] = True`',
        'size += 1': '连通块里又多了一个点：`size = {size}`',
        10: lambda S, B, ret: (f'`{S.x}` 在 initial 里 → 要更新状态 node_id' if (S.node_id != -2 and S.x in S.st) is True or (B.node_id != -2 and S.x in S.st)
                               else (f'`node_id` 已是 -2，不用再看了' if B.node_id == -2 else f'`{S.x}` 不在 initial 里，状态不变')),
        11: lambda S, B, ret: (f'状态机：遇到第一个感染源 → `node_id = {S.node_id}`' if B.node_id == -1
                               else f'状态机：已有感染源 {B.node_id}，又遇到 {S.x} → `node_id = -2`（≥2 个）'),
        13: _ifd,
        14: '递归访问 `{y}`',
        18: lambda S, B, ret: ('`initial` 里的感染源都看完了' if B.get('x') == S.x and B.get('ans') is not None and S.x == S.initial[-1]
                               else f'`for x in initial`：取感染源 `{S.x}`'),
        19: lambda S, B, ret: (f'`vis[{S.x}] = True`：它所在的连通块已经统计过 → 跳过' if B.vis[S.x]
                               else f'`vis[{S.x}] = False`：新的连通块，开始统计'),
        21: '新连通块：状态机重置 `node_id = -1`（还没见到感染源）',
        22: '`size = 0`：重新数这个连通块的大小',
        23: '从 `{x}` 开始 DFS，把整个连通块走一遍',
        24: _upd,
        25: '`ans = {node_id}`：目前最值得移除的感染源',
        26: '`max_size = {size}`：能救下的连通块大小',
        27: lambda S, B, ret: f'返回 `{ret}`' + ('：没有「只含一个感染源」的块，返回 `min(initial)`' if S.ans < 0 else '：能救下最大连通块的那个感染源'),
    },
    cards=dict(
        one_liner='只含一个感染源的连通块，越大越值得救',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['`graph` 是邻接矩阵，`initial` 是初始被感染的节点，感染会沿边传播',
                 '从 `initial` 中移除一个节点（图不变），使最终感染数最少；并列返回下标最小的',
                 '本视频：5 个点，两个连通块 `{0,1,2}`、`{3,4}`，`initial=[1,2,3]`'],
        quote='如果连通块内至少有两个节点被感染，无论移除哪个节点，仍然会导致连通块的所有节点被感染，M(initial) 不变。所以我们要找的是只包含一个被感染节点的连通块，并且这个连通块越大越好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['移除感染源 x：只有==块里仅有 x 一个感染源==时，整块才被救下，少感染 `size` 个',
              'DFS 一遍连通块，顺便数 size，并用状态机 `node_id` 记感染源：-1 无 → x 唯一 → -2 多个',
              '答案：size 最大的候选；一样大取下标小的；没有候选就返回 `min(initial)`'],
        summary=['时间 `O(n²)`（遍历邻接矩阵），空间 `O(n)`',
                 '==`node_id` 状态机==：-1 没见到，≥0 恰好一个，-2 至少两个',
                 '没有任何可救的连通块时，返回 `min(initial)`（移除谁都一样，取最小）',
                 '`size == max_size and node_id < ans` 处理并列取小',
                 '思考题：移除 2 个或 k 个节点呢？'],
    ),
)
