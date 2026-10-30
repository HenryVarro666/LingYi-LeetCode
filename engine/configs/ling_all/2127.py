import math as _math


def _gdraw(cv, T, box, title, pos, edges, color_of, sub_of=None, ecolor_of=None, R=26):
    """有向图：pos = [(fx, fy)]（0~1 的相对位置），edges = [(a, b)]"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 100, y1 - y0 - 110
    P = [(x0 + 50 + fx * Wd, y0 + 60 + fy * Hd) for fx, fy in pos]
    es = set(edges)
    for a, b in edges:
        ec = (ecolor_of(a, b) if ecolor_of else None) or 'dim'
        col = T[ec] if isinstance(ec, str) else ec
        (xa, ya), (xb, yb) = P[a], P[b]
        if a == b:
            cv.arc_arrow((xa - 12, ya - R + 2), (xa + 12, ya - R + 2), 46, col, 3, 11)
            continue
        dx, dy = xb - xa, yb - ya
        L = _math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        off = 9 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        cv.arrow((xa + ux * (R + 3) + nx, ya + uy * (R + 3) + ny), (xb - ux * (R + 6) + nx, yb - uy * (R + 6) + ny), col, 3, 12)
    for i, (x, y) in enumerate(P):
        c = color_of(i)
        fill = T[c] if isinstance(c, str) else (c or T['panel2'])
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
        cv.text((x, y), i, 26, T['bg'] if c else T['muted'], anchor='mm', bold=True)
        if sub_of:
            s = sub_of(i)
            if s:
                cv.text((x, y + R + 6), s, 19, T['text'], anchor='mt', mono=True)
    return P


FAV = [1, 0, 0, 2, 1, 6, 7, 5]
_N = len(FAV)


def _ring_set(f):
    r = set()
    for s in range(len(f)):
        x = s
        for _ in range(len(f)):
            x = f[x]
        y = x
        while True:
            r.add(y)
            y = f[y]
            if y == x:
                break
    return r


RING = _ring_set(FAV)
POS = [(0.34, 0.12), (0.52, 0.12), (0.17, 0.12), (0.0, 0.12), (0.52, 0.78), (0.76, 0.78), (0.98, 0.78), (0.87, 0.12)]


def _col(S, i):
    if 'q' not in S:
        return None
    inq = i in S['q']
    if 'max_ring_size' in S:
        if i == S.get('i') and i in RING:
            return 'pink'
        if i in RING:
            return 'green' if S['deg'][i] == 0 else 'cyan'
        return 'orange'
    if inq:
        return 'yellow'
    if i == S.get('x'):
        return 'pink'
    if i == S.get('y'):
        return 'blue'
    if i not in RING and S['deg'][i] == 0:
        return 'orange'
    return None


def _draw(cv, S, B, box, T):
    f = S['favorite']
    _gdraw(cv, T, box, '从 i 向 favorite[i] 连边（黄 = 队列中的叶子，橙 = 已剪掉的树枝，青 = 基环）', POS,
           [(i, f[i]) for i in range(_N)], lambda i: _col(S, i),
           sub_of=(lambda i: f"d={S['max_depth'][i]}") if 'max_depth' in S else None,
           ecolor_of=lambda a, b: 'cyan' if ('max_ring_size' in S and a in RING) else 'dim')


def _cap_pop(S, B, ret):
    return f'弹出 `{S.x}`：没人喜欢它（入度 0）→ 它在==树枝==上，可以剪掉'


def _cap_deg0(S, B, ret):
    if S.deg[S.y] == 0:
        return f'`deg[{S.y}] = 0`：喜欢 `{S.y}` 的人都剪完了 → `{S.y}` 也变成叶子，==入队=='
    return f'`deg[{S.y}] = {S.deg[S.y]}` ≠ 0：还有别人喜欢 `{S.y}`，先不入队（`{S.y}` 在基环上或还有树枝）'


def _cap_skip(S, B, ret):
    if S.d == 0:
        where = '环上的点，前面绕环时已经算过' if S.i in RING else '树枝上的点，早被剪掉'
        return f'`deg[{S.i}] = 0`：{where} → ==跳过=='
    return f'`deg[{S.i}] = {S.d} > 0`：基环上的点，从这里绕环一圈'


def _cap_while(S, B, ret):
    if S.x != S.i:
        return f'`x = {S.x}` 还没回到起点 `{S.i}` → 继续沿着 favorite 走'
    return f'`x` 回到起点 `{S.i}`：环走完了，环长 ==`{S.ring_size}`=='


def _cap_ring2(S, B, ret):
    if S.ring_size == 2:
        return '环长 `== 2`：两人互相喜欢，两侧各能再接一条树枝链 → 走“拼链”分支'
    return f'环长 `{S.ring_size}` > 2：树枝插不进圆桌 → 只能取最大环长'


CONFIG = dict(
    num=2127, title='参加会议的最多员工数', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='基环树 · 拓扑排序剪枝',
    tags=['灵神题单·图论算法', '难度分 2449'],
    code='''
class Solution:
    def maximumInvitations(self, favorite: List[int]) -> int:
        n = len(favorite)
        deg = [0] * n
        for f in favorite:
            deg[f] += 1  # 统计基环树每个节点的入度

        max_depth = [1] * n
        q = deque(i for i, d in enumerate(deg) if d == 0)
        while q:  # 拓扑排序，剪掉图上所有树枝
            x = q.popleft()
            y = favorite[x]  # x 只有一条出边
            max_depth[y] = max_depth[x] + 1
            deg[y] -= 1
            if deg[y] == 0:
                q.append(y)

        max_ring_size = sum_chain_size = 0
        for i, d in enumerate(deg):
            if d == 0: continue

            # 遍历基环上的点
            deg[i] = 0  # 将基环上的点的入度标记为 0，避免重复访问
            ring_size = 1  # 基环长度
            x = favorite[i]
            while x != i:
                deg[x] = 0  # 将基环上的点的入度标记为 0，避免重复访问
                ring_size += 1
                x = favorite[x]

            if ring_size == 2:  # 基环长度为 2
                sum_chain_size += max_depth[i] + max_depth[favorite[i]]  # 累加两条最长链的长度
            else:
                max_ring_size = max(max_ring_size, ring_size)  # 取所有基环长度的最大值
        return max(max_ring_size, sum_chain_size)
''',
    call=f'Solution().maximumInvitations({FAV})',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=270),
        dict(type='queue', var='q', h=110, label='q（待剪的叶子）'),
        dict(type='array', var='deg', h=150, label='deg（入度；基环点最后留下 > 0）',
             pointers={'i': 'pink'}),
        dict(type='array', var='max_depth', h=150, label='max_depth（以 i 结尾的最长链人数）'),
    ],
    watch=['ring_size', ('max_ring_size', 'max_ring_size', 'cyan'), ('sum_chain_size', 'sum_chain_size', 'orange')],
    skip=['n = len(favorite)', 'deg = [0] * n', 'for f in favorite'],
    max_steps=56,
    captions={
        'deg[f] += 1': '`{f}` 被 `favorite` 里的某人喜欢一次 → 入度 `deg[{f}] = {deg[f]}`',
        'max_depth = [1] * n': '`max_depth[i]`：以 `i` 为终点的最长树枝链有几个人，开始每人只有自己，记 1',
        'q = deque': '入度为 0 = 没人喜欢他 = ==树枝的叶子==，先全部入队：`{list(q)}`',
        'x = q.popleft': _cap_pop,
        'y = favorite[x]': '`x = {x}` 只有一条出边，指向 `y = {y}`',
        'max_depth[y] = max_depth[x]': '链延长一人：`max_depth[{y}] = {max_depth[x]} + 1 = {max_depth[y]}`（先弹出的层数浅，后弹出的更深，所以直接赋值就是最大）',
        'deg[y] -= 1': '剪掉 `{x}` 后，`{y}` 少一个喜欢者：`deg[{y}]` → {deg[y]}',
        'if deg[y] == 0': _cap_deg0,
        'max_ring_size = sum_chain_size = 0': '拓扑排序结束：树枝全被剪掉，==入度仍 > 0 的就是基环==。下面逐个环统计',
        'if d == 0: continue': _cap_skip,
        'deg[i] = 0': '把环上的点入度记 0，==避免同一个环重复数==',
        'ring_size = 1': '环长先记 1（`i` 自己）',
        'x = favorite[i]': '`x = favorite[{i}] = {x}`：沿着喜欢的人往前走',
        'while x != i': _cap_while,
        'deg[x] = 0': '`{x}` 在环上 → 入度标 0',
        'ring_size += 1': '环又多一人：`ring_size` = {ring_size}',
        'x = favorite[x]': '`x` 走到 {x}',
        'if ring_size == 2': _cap_ring2,
        'sum_chain_size +=': '两条最长链接在一起：`max_depth[{i}] + max_depth[{favorite[i]}]` = {max_depth[i]} + {max_depth[favorite[i]]}，`sum_chain_size` = =={sum_chain_size}==',
        'max_ring_size = max': '`max_ring_size = max({B.max_ring_size}, {ring_size}) = {max_ring_size}`',
        'return max': '答案 = `max(最大环 {max_ring_size}, 所有 2 环的链之和 {sum_chain_size})` = =={ret}==',
    },
    cards=dict(
        one_liner='内向基环树：拓扑排序剪掉树枝，再分环长 =2 / >2 统计',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`favorite[i]` 是第 `i` 位员工喜欢的人，圆桌上每人必须坐在他喜欢的人旁边',
                 '求圆桌最多能坐多少人',
                 '本视频：`[1,0,0,2,1,6,7,5]` → `5`'],
        quote='每个连通块必定有且仅有一个环，每个点的出度均为 1，这样的有向图又叫做内向基环树……对于多个基环长度等于 2 的基环树，每个基环树所对应的链，都可以拼在其余链的末尾。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从 `i` 向 `favorite[i]` 连边：每块恰一个环 + 若干树枝；树枝上的人插不进长环',
              '环长 `> 2`：答案取最大环长；环长 `== 2`：两侧各接一条最长链，所有这类链能拼成一桌',
              '用拓扑排序剪枝，顺便把最长链长度算进 `max_depth`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '答案是 `max(最大环长, 全部 2 环的链长之和)`，不是只取一种',
                 '`max_depth[y] = max_depth[x] + 1` 直接赋值：FIFO 拓扑序里最后弹出的儿子链最长',
                 '题解还给了另一种写法：拓扑时建反图，再 dfs 找最深的链，思路相同'],
    ),
)
