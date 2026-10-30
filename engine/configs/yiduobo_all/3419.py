N = 4
EDGES = [[1, 0, 1], [2, 0, 3], [3, 1, 2], [2, 3, 1]]
POS = {0: (0.92, 0.50), 1: (0.60, 0.14), 3: (0.25, 0.14), 2: (0.25, 0.86)}


def _live(S):
    return 'mid' in S and S.get('_line', 0) >= 15


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '原图（箭头 = 原方向；灰暗 = 权重 > mid 的边；绿 = 本轮 BFS 访问到，蓝 = 当前出队）', 20, T['muted'], bold=True)
    W, H = x1 - x0 - 120, y1 - y0 - 100
    ox, oy = x0 + 60, y0 + 56

    def P(k):
        return ox + POS[k][0] * W, oy + POS[k][1] * H

    line = S.get('_line', 0)
    live = _live(S)
    bfs = live and line >= 24 and 'vis' in S
    vis = S['vis'] if bfs else set()
    cur = S.get('x') if bfs and line >= 25 and S.get('head', 0) > 0 else None
    hot = None
    if line in (28, 29, 30) and 'y' in S and 'x' in S:
        hot = (S['y'], S['x'])
    build = live and 15 <= line <= 19
    R = 30
    for a, b, w in EDGES:
        (ax, ay), (bx, by) = P(a), P(b)
        dx, dy = bx - ax, by - ay
        L = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / L, dy / L
        p0 = (ax + ux * R, ay + uy * R)
        p1 = (bx - ux * (R + 4), by - uy * (R + 4))
        off = live and w > S['mid']
        c = T['border']
        wd = 3
        if hot == (a, b):
            c, wd = T['pink'], 6
        elif live and not off:
            c = T['muted']
        if build and S.get('x') == a and S.get('y') == b and 'w' in S:
            c, wd = T['yellow'], 6
        cv.arrow(p0, p1, c, width=wd, head=14)
        mx, my = (p0[0] + p1[0]) / 2 - uy * 18, (p0[1] + p1[1]) / 2 + ux * 18
        cv.text((mx, my), w, 22, T['dim'] if off else (T['pink'] if hot == (a, b) else T['yellow']), anchor='mm', bold=True)
    for k in range(N):
        X, Y = P(k)
        fill = T['green'] if k in vis else T['panel2']
        cv.rect((X - R, Y - R, X + R, Y + R), fill=fill, r=R, outline=T['border'])
        if cur == k:
            cv.rect((X - R - 5, Y - R - 5, X + R + 5, Y + R + 5), outline=T['blue'], width=5, r=R + 5)
        cv.text((X, Y), k, 28, T['bg'] if k in vis else T['text'], anchor='mm', bold=True)


def _info(S):
    if 'left' not in S or S['left'] is None or S.get('right') is None:
        return ''
    t = f'二分边权上限：`[{S["left"]}, {S["right"]}]`'
    if _live(S):
        t += f'，当前 `mid = {S["mid"]}`：只用权重 `<= {S["mid"]}` 的边'
    return t


CONFIG = dict(
    num=3419, title='图的最大边权的最小值', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 + 反向建图 BFS',
    tags=['难度分 2243'],
    code='''
class Solution(object):
    def minMaxWeight(self, n, edges, threshold):

        left, right = None, None
        for x, y, w in edges:
            if left is None or w < left:
                left = w
            if right is None or w > right:
                right = w

        right += 1
        ma = right
        while left < right:
            mid = (left + right) // 2
            g = [set() for x in range(n)]
            for x, y, w in edges:
                if w > mid:
                    continue
                g[y].add(x)

            q = [0]
            head, tail = 0, 1
            vis = set([0])
            while head < tail:
                x = q[head]
                head += 1
                for y in g[x]:
                    if y not in vis:
                        q.append(y)
                        vis.add(y)
                        tail += 1

            if tail == n:
                right = mid
            else:
                left = mid + 1

        if left == ma:
            return -1
        return left
''',
    call=f'Solution().minMaxWeight({N}, {EDGES}, 1)',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_info, h=56),
        dict(type='array', var=lambda S: S['q'] if 'q' in S and S['_line'] >= 21 else None,
             label='q（BFS 队列；暗 = 已出队，head 指向下一个）', cell=76, h=170, pointers={'head': 'blue'},
             dim=lambda S, i, v: i < S.get('head', 0)),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('head', 'head'), ('tail', 'tail'), ('n', 'n')],
    skip=['for x, y, w in edges', 'if left is None', 'if right is None', 'continue', 'head, tail = 0, 1',
          'head += 1', 'tail += 1', 'for y in g[x]', 'q.append', 'ma = right', 'vis = set([0])'],
    captions={
        'left, right = None, None': '`left`、`right` 先设成空，下面扫一遍边权求最小、最大',
        'left = w': '边权最小值：`left = {w}`',
        'right = w': '边权最大值：`right = {w}`',
        'right += 1': '`right` 再加 1 = `{right}`：答案若落在上限 `{right}` 就说明连不通，要返回 `-1`',
        'while left < right': lambda S, B, r: (f'`left = {B.left} < right = {B.right}`：还没锁定，继续二分' if B.left < B.right
                                               else f'`left == right = {B.left}`：二分结束'),
        'mid = (left + right)': '猜最大边权 `mid = ({left} + {right}) // 2 = {mid}`',
        'g = [set()': '本轮重建==反向图==：只放权重 `<= mid` 的边',
        'if w > mid': lambda S, B, r: (f'边 `{S.x}→{S.y}`，权 `{S.w}` > `mid = {S.mid}` → 不能用，跳过' if S.w > S.mid
                                       else f'边 `{S.x}→{S.y}`，权 `{S.w}` <= `mid = {S.mid}` → 可以用'),
        'g[y].add(x)': '反向存边：`g[{y}]` 里加 `{x}`（从 {y} 能走到 {x}）',
        'q = [0]': '从 0 开始 BFS：能走到几个点？',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：队列不空，继续' if B.head < B.tail
                                              else f'`head == tail = {B.tail}`：BFS 结束，一共走到 `{B.tail}` 个点'),
        'x = q[head]': '出队节点 `{x}`，看反向图里它能走到的点 `g[{x}] = {sorted(g[x])}`',
        'if y not in vis': lambda S, B, r: (f'`{S.y}` 没访问过 → ==入队==' if S.y not in B.vis
                                            else f'`{S.y}` 访问过，跳过'),
        'vis.add(y)': '`{y}` 入队并标记访问，`tail = {tail + 1}`',
        'if tail == n': lambda S, B, r: (f'`tail = {S.tail} == n = {S.n}`：所有点都能到 0 → `mid = {S.mid}` ==可行==' if S.tail == S.n
                                         else f'`tail = {S.tail} < n = {S.n}`：有点到不了 0 → `mid = {S.mid}` ==太小=='),
        'right = mid': '可行 → 答案 <= mid：`right = {right}`',
        'left = mid + 1': '不可行 → 答案 > mid：`left = {left}`',
        'if left == ma': lambda S, B, r: (f'`left = {S.left}` 等于上限 `{S.ma}`：最大的边都不够，连不通' if S.left == S.ma
                                          else f'`left = {S.left}` < 上限 `{S.ma}`：真的找到了可行边权'),
        'return left': '答案 =={left}==',
    },
    max_steps=130,
    cards=dict(
        one_liner='二分最大边权 mid，用 <= mid 的边反向 BFS，看能否走遍所有点',
        complexity='时间 `O(m log U)`，空间 `O(n + m)`',
        problem=['有向带权图，删掉一些边，使所有点都能到达 0',
                 '剩余边的==最大边权尽量小==，每个点出边至多 `threshold` 条',
                 '无解返回 `-1`；本视频：`n = 4`，4 条边 → `2`'],
        quote='最终bfs路径上的每个节点的入度都为1，反过来说在正向图上的出度均为1，必然小于等于threshold，因此实际上完全无需考虑出度这个条件。',
        quote_src='—— yiduobo 题解原文',
        idea=['最大值最小 → ==二分答案==：边权上限越大越容易连通',
              '把权重 `<= mid` 的边==反向==，从 0 做 BFS，走到 `n` 个点就可行',
              '上限设成「最大边权 + 1」：落在这个值就说明无解'],
        summary=['时间 `O(m log U)`，空间 `O(n + m)`',
                 '判定里不用管 `threshold`：BFS 树中每个点只用一条出边',
                 '二分上限是最大边权 + 1，最后 `left == ma` 才返回 `-1`',
                 '原文为 Python 2 风格（继承 object），代码未改',
                 '对比灵神：灵神用 DFS/Dijkstra，并先判断边数 `< n-1`'],
    ),
)
