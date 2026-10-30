GRAPH = [[1, 1, 0, 1, 0, 0],
         [1, 1, 1, 0, 0, 0],
         [0, 1, 1, 0, 0, 1],
         [1, 0, 0, 1, 1, 0],
         [0, 0, 0, 1, 1, 0],
         [0, 0, 1, 0, 0, 1]]
INITIAL = [1, 5]
N = 6


def _pos(box):
    import math
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 36
    R = min((x1 - x0) / 2 - 90, (y1 - y0) / 2 - 70)
    return [(cx + R * math.cos(-math.pi / 2 + 2 * math.pi * k / N), cy + R * math.sin(-math.pi / 2 + 2 * math.pi * k / N)) for k in range(N)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '网络（红 = initial，绿 = 已访问，蓝环 = 当前点）', 20, T['muted'], bold=True)
    P = _pos(box)
    g = GRAPH
    for i in range(N):
        for j in range(i + 1, N):
            if g[i][j]:
                cv.line([P[i], P[j]], T['border'], 4)
    vis = S.get('vis')
    st = S.get('st') or set()
    inner = S.get('_inner', {})
    cur = inner.get('x') if 'x' in inner and S.get('_line', 0) >= 6 else None
    for k in range(N):
        x, y = P[k]
        r = 30
        if k in st:
            fill = T['red']
        elif vis and vis[k]:
            fill = T['green']
        else:
            fill = T['panel2']
        cv.rect((x - r, y - r, x + r, y + r), fill=fill, outline=T['muted'], width=2, r=r)
        cv.text((x, y), k, 32, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        if cur == k:
            cv.rect((x - r - 7, y - r - 7, x + r + 7, y + r + 7), outline=T['blue'], width=5, r=r + 7)
    if 'node_id' in S and 'size' in S:
        nid = S['node_id']
        desc = '还没遇到 initial 中的点' if nid == -1 else ('遇到 ≥ 2 个不同的 initial 点：删谁都救不了' if nid == -2 else f'只遇到 initial 中的点 {nid}')
        cv.text((x0 + 18, y0 + 34), f"本块：size = {S['size']}　node_id = {nid}（{desc}）", 24, T['yellow'], anchor='la', bold=True)


CONFIG = dict(
    num=928, title='尽量减少恶意软件的传播 II', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='逆向思维 · 绕开 initial 的 DFS',
    tags=['灵神题单·图论算法', '难度分 1985'],
    code='''
class Solution:
    def minMalwareSpread(self, graph: List[List[int]], initial: List[int]) -> int:
        st = set(initial)
        vis = [False] * len(graph)
        def dfs(x: int) -> None:
            vis[x] = True
            nonlocal node_id, size
            size += 1
            for y, conn in enumerate(graph[x]):
                if conn == 0:
                    continue
                if y in st:
                    # 按照 924 题的状态机更新 node_id
                    # 注意避免重复统计，例如上图中的 0 有两条不同路径可以遇到 1
                    if node_id != -2 and node_id != y:
                        node_id = y if node_id == -1 else -2
                elif not vis[y]:
                    dfs(y)

        cnt = Counter()
        for i, seen in enumerate(vis):
            if seen or i in st:
                continue
            node_id = -1
            size = 0
            dfs(i)
            if node_id >= 0:  # 只找到一个在 initial 中的节点
                # 删除节点 node_id 可以让 size 个点不被感染
                cnt[node_id] += size

        # size 取反计算最大值，相同最大值取 node_id 最小值
        return min((-size, node_id) for node_id, size in cnt.items())[1] if cnt else min(initial)
''',
    call=f'Solution().minMalwareSpread({GRAPH!r}, {INITIAL!r})',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='map', var='cnt', label='cnt（initial 点 → 删它能救的点数）', fmt=lambda k, v: f'{k}: {v}', h=140, font=28),
        dict(type='calls', h=200),
    ],
    watch=[('i', 'i', 'blue'), ('node_id', 'node_id', 'orange'), ('size', 'size', 'yellow'), ('st', 'st', 'red')],
    skip=['nonlocal', 'for y, conn', 'if conn == 0', 'continue', 'vis = [False]'],
    captions={
        'st = set(initial)': '`st`：被感染的初始点集合 `{st}`，DFS 时要避开它们',
        'cnt = Counter()': '`cnt[x]`：删掉 initial 中的点 `x` 能让多少点免受感染',
        'for i, seen in enumerate(vis)': lambda S, B, ret: (f'看点 `{S.i}`' if 'i' not in B or S.i != B.i else '所有点看完了'),
        'if seen or i in st': lambda S, B, ret: (f'点 `{S.i}` 已访问过或是 initial 点 → 跳过' if S.seen or S.i in S.st else f'点 `{S.i}` 是普通点且没访问过 → 从它出发 DFS'),
        'node_id = -1': '`node_id = -1`：这个块里还没遇到 initial 的点',
        'size = 0': '`size = 0`：块内普通点个数清零',
        'dfs(i)': '从 `{i}` 出发 DFS：只走普通点，数 `size`，遇到 initial 点就更新 `node_id`',
        'vis[x] = True': '访问点 `{x}`',
        'size += 1': '块大小 `size = {size}`',
        'if y in st': lambda S, B, ret: (f'邻居 `{S.y}` 在 initial 中：不进去，只记录是谁' if S.y in S.st else f'邻居 `{S.y}` 是普通点'),
        'if node_id != -2': lambda S, B, ret: (f'`node_id = {S.node_id}`，邻居 `{S.y}`：{"新遇到的 initial 点，要更新" if S.node_id != -2 and S.node_id != S.y else "已经记录过，不用重复统计"}'),
        'node_id = y if': lambda S, B, ret: (f'第一次遇到 initial 点 `{S.y}` → `node_id = {S.node_id}`' if S.node_id >= 0
                                             else f'又遇到另一个 initial 点 → `node_id = -2`：删谁都救不了这个块'),
        'elif not vis[y]': lambda S, B, ret: (f'邻居 `{S.y}` 没访问过 → 继续 DFS' if not S.vis[S.y] else f'邻居 `{S.y}` 已访问过'),
        'dfs(y)': '往普通邻居 `{y}` 继续走',
        'if node_id >= 0': lambda S, B, ret: (f'`node_id = {S.node_id} ≥ 0`：整块只被点 `{S.node_id}` 感染到，删掉它就能救 `{S.size}` 个点' if S.node_id >= 0
                                              else '`node_id = -2`：有多个 initial 点能感染这块，删谁都没用'),
        'cnt[node_id] += size': '`cnt[{node_id}] += {size}` → `{dict(cnt)}`',
        'return min': '救得最多的是 `{ret}`（并列取编号小的）',
    },
    max_steps=100,
    cards=dict(
        one_liner='反着想：从普通点 DFS，看谁是唯一能感染它的 initial 点',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['无向图用邻接矩阵给出，`initial` 中的点最初被感染，感染会沿边扩散',
                 '只能从 `initial` 里删一个点（连同它的边），使最终感染点数最少',
                 '本视频：6 个点，`initial = [1,5]` → 删 `1`'],
        quote='逆向思维，从不在 initial 中的点 v 出发 DFS，在不经过 initial 中的节点的前提下，看看 v 是只能被一个点感染到，还是能被多个点感染到。如果 v 只能被点 x 感染到，那么在本次 DFS 过程中访问到的其它节点，也只能被点 x 感染到。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从普通点出发 DFS，不进入 initial 点，只记录碰到了哪个',
              '`node_id` 是状态机：-1 没碰到，≥ 0 唯一的点，-2 碰到多个',
              '块内只碰到唯一的 `x`：删 `x` 就能救 `size` 个点，累加到 `cnt[x]`'],
        summary=['时间 `O(n^2)`（遍历邻接矩阵），比暴力 `O(m n^2)` 快',
                 '`node_id != y` 的判断避免同一个 initial 点被重复统计',
                 '`cnt` 为空说明谁都救不了普通点 → 返回 `min(initial)`',
                 '最后 `(-size, node_id)` 取最小：救得多优先，并列取编号小',
                 '前置题：924，思路相同的状态机'],
    ),
)
