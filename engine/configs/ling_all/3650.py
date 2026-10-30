import math as _m


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title, directed=True):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 30
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 70 + R, y1 - R - 34
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v, w in edges:
        c, wd = ecol(u, v)
        (ax, ay), (bx, by) = P[u], P[v]
        dd = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / dd, (by - ay) / dd
        if directed:
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 2), by - uy * (R + 2)), c, wd, 16)
        else:
            cv.line([(ax + ux * R, ay + uy * R), (bx - ux * R, by - uy * R)], c, wd)
        mx, my = (ax + bx) / 2 - uy * 20, (ay + by) / 2 + ux * 20
        cv.rect((mx - 17, my - 15, mx + 17, my + 15), fill=T['bg'], r=6)
        cv.text((mx, my), w, 22, c if c != T['dim'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u, (px, py) in pos.items():
        px, py = P[u]
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is not None:
            if py < (Tp + Bt) / 2 - 5:
                cv.text((px, py - R - 4), s, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            else:
                cv.text((px, py + R + 4), s, 20, T['yellow'], anchor='mt', bold=True, mono=True)

N = 5
EDGES = [(0, 1, 3), (3, 1, 1), (2, 3, 4), (0, 2, 2), (3, 4, 2)]
POS = {0: (0.02, 0.5), 1: (0.36, 0.04), 2: (0.36, 0.96), 3: (0.68, 0.5), 4: (0.98, 0.5)}

CODE = '''
class Solution:
    def minCost(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]  # 邻接表
        for x, y, wt in edges:
            g[x].append((y, wt))
            g[y].append((x, wt * 2))

        dis = [inf] * n
        dis[0] = 0  # 起点到自己的距离是 0
        h = [(0, 0)]  # 堆中保存 (起点到节点 x 的最短路长度，节点 x)

        while h:
            dis_x, x = heappop(h)
            if dis_x > dis[x]:  # x 之前出堆过
                continue
            if x == n - 1:  # 到达终点
                return dis_x
            for y, wt in g[x]:
                new_dis_y = dis_x + wt
                if new_dis_y < dis[y]:
                    dis[y] = new_dis_y  # 更新 x 的邻居的最短路
                    # 懒更新堆：只插入数据，不更新堆中数据
                    # 相同节点可能有多个不同的 new_dis_y，除了最小的 new_dis_y，其余值都会触发上面的 continue
                    heappush(h, (new_dis_y, y))

        return -1
'''
_L = CODE.strip('\n').split('\n')
FOR_LINE = next(i + 1 for i, l in enumerate(_L) if 'for y, wt in g[x]' in l)


def _inf(v):
    return '∞' if v == _m.inf else v


def _fwd(x, y, wt):
    return any(e[0] == x and e[1] == y and e[2] == wt for e in EDGES)


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    line = S.get('_line')
    x = S.get('x') if 'dis_x' in S else None
    dx = S.get('dis_x')
    y = S.get('y') if line in range(FOR_LINE, FOR_LINE + 7) and 'y' in S else None
    wt = S.get('wt')

    def ncol(u):
        if dis is None or dis[u] == _m.inf:
            return T['panel2']
        if u == x:
            return T['blue']
        if dx is not None and dis[u] < dx:
            return T['green']
        return T['orange']

    def nsub(u):
        return None if dis is None else f'dis={_inf(dis[u])}'

    def ecol(u, v):
        if y is not None and ((u == x and v == y and _fwd(x, y, wt)) or (v == x and u == y and not _fwd(x, y, wt))):
            return T['yellow'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol, '有向图（蓝 = 刚出堆，绿 = 已确定，橙 = 暂定；黄边 = 正在走的边）')


def _text(S, B):
    line = S.get('_line')
    if 'new_dis_y' in S and line in range(FOR_LINE + 1, FOR_LINE + 4):
        x, y, wt = S['x'], S['y'], S['wt']
        how = '正着走原边' if _fwd(x, y, wt) else f'反转原边 `{y} → {x}`，成本翻倍'
        return f"`{x} → {y}`：{how}，边权 `{wt}`，总计 `{S['new_dis_y']}`"
    if 'dis_x' in S:
        return f"刚出堆：`dis_x = {S['dis_x']}`，`x = {S['x']}`"
    return '每条边建两份：正向 `w`，反向 `2w`'


def _skip(S, B, r):
    if S.dis_x > S.dis[S.x]:
        return f'`{S.dis_x} > dis[{S.x}] = {S.dis[S.x]}`：==x 之前出堆过==，旧记录'
    return f'`{S.dis_x} == dis[{S.x}]`：首次出堆，最短路已定'


def _for(S, B, r):
    if 'y' in B and (B.x, B.y, B.wt) == (S.x, S.y, S.wt):
        return f'`{S.x}` 的边都看完了'
    how = '原边' if _fwd(S.x, S.y, S.wt) else '==反转边（成本 2w）=='
    return f'看 `{S.x} → {S.y}`：{how}，边权 `{S.wt}`'


def _cmp(S, B, r):
    if S.new_dis_y < S.dis[S.y]:
        return f'`{S.new_dis_y} < dis[{S.y}] = {_inf(S.dis[S.y])}`：==更短=='
    return f'`{S.new_dis_y} >= dis[{S.y}] = {S.dis[S.y]}`：不更短，不更新'


CONFIG = dict(
    num=3650, title='边反转的最小路径总成本', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='反向边权设为 2w 的 Dijkstra',
    tags=['灵神题单·图论算法', '难度分 1854'],
    code=CODE,
    call=f'Solution().minCost({N}, {[list(e) for e in EDGES]})',
    expect=7,
    skip=['for x, y, wt in edges', 'g[x].append', 'g[y].append', 'dis = [inf]', 'dis[0] = 0'],
    max_steps=80,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=370),
        dict(type='array', var=lambda S: [_inf(v) for v in S['dis']] if 'dis' in S else None, label='dis[i]：0 到 i 的最小成本', h=150, cell=90,
             color=lambda S, i, v: 'blue' if 'x' in S and 'dis_x' in S and i == S['x'] else None),
        dict(type='heap', var='h', label='h（最小堆，元素 = (成本, 节点)）', h=130, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('dis_x', 'dis_x', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('wt', 'wt'), ('new_dis_y', 'new_dis_y', 'orange')],
    captions={
        'g = [[] for': '邻接表 `g[x]` 存 `(终点, 边权)`',
        'dis = [inf] * n': '`dis[i]`：从 0 出发到 i 的最小成本，先设为 ∞',
        'dis[0] = 0': '起点到自己 `0`',
        'h = [(0, 0)]': '堆里放 `(0, 0)`',
        'while h': lambda S, B, r: '堆非空，继续' if S.h else '堆空了，终点没到过',
        'dis_x, x = heappop': '弹出堆顶 `({dis_x}, {x})`：成本最小的节点',
        'if dis_x > dis[x]': _skip,
        'continue': '过时记录，邻居早被更小的值更新过 → ==跳过==',
        'if x == n - 1': lambda S, B, r: (f'`x = {S.x}` 是终点：==首次出堆，成本 {S.dis_x} 就是最小总成本==' if S.x == S.n - 1 else f'`x = {S.x}` 不是终点 `{S.n - 1}`，继续扩展'),
        'return dis_x': '返回终点的最小成本 `{dis_x}`',
        'for y, wt in g[x]': _for,
        'new_dis_y = dis_x + wt': '`{dis_x} + {wt}` = =={new_dis_y}==',
        'if new_dis_y < dis[y]': _cmp,
        'dis[y] = new_dis_y': '更新邻居：`dis[{y}]` = =={dis[y]}==',
        'heappush(h,': '`({new_dis_y}, {y})` 入堆：==只插入不修改旧值==（懒更新）',
        'return -1': '堆空了还没到终点：返回 `-1`',
    },
    cards=dict(
        one_liner='「最多用一次开关」是障眼法：反向边直接建成 2w 就行',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['有向带权图，到达节点 `u` 时可以把一条入边 `v → u` 反转，立即穿过，成本 `2w`',
                 '每个节点的开关最多用一次；求 `0` 到 `n-1` 的最小总成本',
                 '本视频：5 个点，最优走法 `0→1`，反转 `3→1`，再 `3→4`，总成本 `7`'],
        quote='根据 Dijkstra 算法，同一个节点我们只会访问一次，所以「最多可使用一次开关」这个约束是多余的，我们只需把反向边的边权设置为 2w 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['Dijkstra 里每个节点只会被确定一次，所以最优路径不会重复用同一个开关',
              '对每条边 `x → y, w` 再加一条 `y → x, 2w`',
              '之后就是普通最短路：出堆时遇到 `n-1` 直接返回'],
        summary=['时间 `O(n + m log m)`，空间 `O(n + m)`',
                 '易错：反向边权是 `2 * wt`，不是 `wt`',
                 '懒更新堆：同一节点可多次入堆，靠 `dis_x > dis[x]` 过滤旧记录',
                 '到达终点出堆时立即返回；堆空仍没到终点则返回 `-1`'],
    ),
)
