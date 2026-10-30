import math


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S['graph']
    n = len(g)
    cv.text((x0 + 18, y0 + 4), '图（蓝 = state 里已访问，黄圈 = 当前所在 x，粉 = 要走向的 next）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 24
    R = min(x1 - x0, y1 - y0) * 0.34
    pos = []
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        pos.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    for u in range(n):
        for v in g[u]:
            if u < v:
                cv.line([pos[u], pos[v]], T['border'], 4)
    state = S.get('state', 0) if 'state' in S else 0
    xx = S.get('x') if 'state' in S else None
    nx = S.get('next') if 'next_state' in S else None
    for k in range(n):
        px, py = pos[k]
        vis = (state >> k) & 1
        if nx == k:
            cv.rect((px - 40, py - 40, px + 40, py + 40), outline=T['pink'], width=5, r=40)
        if xx == k:
            cv.rect((px - 35, py - 35, px + 35, py + 35), outline=T['yellow'], width=5, r=35)
        cv.rect((px - 28, py - 28, px + 28, py + 28), fill=T['blue'] if vis else T['panel2'], r=28, outline=T['border'])
        cv.text((px, py), k, 30, T['bg'] if vis else T['muted'], anchor='mm', bold=True)
    if 'state' in S:
        cv.text((x0 + 18, y1 - 34), f"state = {format(state, '0%db' % n)}（低位 = 点 0）  目标 {format((1 << n) - 1, 'b')}", 24, T['text'], bold=True, mono=True)


CONFIG = dict(
    num=847, title='访问所有节点的最短路径', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='状态压缩 + 多源 BFS',
    tags=['灵神题单', '图论算法'],
    code='''
class Solution(object):
    def shortestPathLength(self, graph):

        n = len(graph)
        f = [[None] * n for _ in range(1 << n)]
        q = []
        for i in range(n):
            f[1 << i][i] = 0
            q.append([1 << i, i])
        
        l = 0
        r = len(q)
        while l < r:
            for index in range(l, r):
                state, x = q[index]
                for next in graph[x]:
                    next_state = state | (1 << next)
                    if f[next_state][next] is None:
                        f[next_state][next] = f[state][x] + 1
                        q.append([next_state, next])
                        if next_state == (1 << n) - 1:
                            return f[next_state][next]
            
            l, r = r, len(q)

        return 0
''',
    call='Solution().shortestPathLength([[1],[0,2],[1]])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: [f"{format(a, '0%db' % len(S['graph']))}@{b}" for a, b in S['q']] if 'q' in S else [], label='BFS 队列 q：[state, x]', cell=110, h=150),
        dict(type='text', fn=lambda S: (f"f[{format(S['state'], '0%db' % len(S['graph']))}][{S['x']}] = {S['f'][S['state']][S['x']]}" if 'state' in S and 'x' in S else ''), size=26, h=60),
    ],
    watch=['l', 'r', 'state', 'x', 'next'],
    skip=['n = len', 'q = []', 'for i in range', 'l = 0', 'r = len(q)', 'state, x = q[index]', 'for index in range'],
    max_steps=90,
    captions={
        'f = [[None]': '`f[state][x]`：已访问集合为 `state`、停在 `x` 的最少步数；`None` 表示还没到过',
        'f[1 << i][i] = 0': '多源起点：从点 `{i}` 出发，`state` 只含自己，步数 0',
        'q.append([1 << i, i])': '起点 `{i}` 入队',
        'while l < r': lambda S, B, r: f'队列里 `q[{S.l}:{S.r}]` 是同一步数的一层，继续展开',
        'for next in graph[x]': '从 `x = {x}` 走到邻居 `next = {next}`，步数 +1',
        'next_state = ': '访问 `{next}`：`state | (1 << {next})` = `{format(next_state, "b")}`',
        'if f[next_state][next] is None': lambda S, B, r: (f'`({format(S.next_state, "b")}, {S.next})` 没到过 → 第一次到达就是最短（BFS 按层推进）' if S.f[S.next_state][S.next] is None else f'`({format(S.next_state, "b")}, {S.next})` 已到过 → 更晚到达没意义，丢弃'),
        'f[next_state][next] = f[state][x] + 1': '记录 `f[...] = {B.f[state][x]} + 1 = {f[next_state][next]}`',
        'q.append([next_state, next])': '新状态入队，下一层再展开',
        'if next_state == (1 << n) - 1': lambda S, B, r: ('所有点都访问过 → 立刻返回当前步数' if S.next_state == (1 << len(S.graph)) - 1 else f'`{format(S.next_state, "b")}` 还没覆盖全部点，继续'),
        'l, r = r, len(q)': '这一层处理完：下一层 = 刚入队的 `q[{l}:{r}]`',
        'return f[next_state][next]': '首次覆盖全部点：最短路径长度 =={f[next_state][next]}==',
    },
    cards=dict(
        one_liner='状态 = (访问过哪些点, 停在哪个点)，所有边长 1 → BFS',
        complexity='时间 `O(2^n · n · deg)`，空间 `O(2^n · n)`',
        problem=['无向连通图，`n` 个点，可以从任意点出发，可重复经过点和边',
                 '求访问==所有节点==的最短路径长度',
                 '示例：`[[1,2,3],[0],[0],[0]]` → `4`；本视频：`[[1],[0,2],[1]]` → `2`'],
        quote='设f[state][x]表示当前已经访问过了state这些点，最后处于x这一点上所需的最少步数。',
        quote_src='—— yiduobo 题解原文',
        idea=['点数很少，用二进制 `state` 记录访问过的点，走到邻居 `state | (1 << next)`',
              '所有边长为 1，从每个点同时出发做 BFS，第一次让 `state` 全 1 就是答案',
              '`f[state][x]` 既当访问标记，也记录步数'],
        summary=['时间 `O(2^n · n · deg)`，空间 `O(2^n · n)`',
                 '要把 n 个点都当起点入队，不是只从 0 出发',
                 '同一个 `(state, x)` 只入队一次，所以点和边可以重复经过',
                 '原文已是 Python 3 可运行写法，逐字照搬；变量名 `next` 覆盖了内置函数，但这里不影响'],
    ),
)
