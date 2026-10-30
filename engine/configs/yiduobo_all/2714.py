EDGES = [[0, 1, 4], [0, 2, 2], [2, 3, 6]]
N, SRC, DST, K = 4, 1, 3, 1
POS = {1: 0, 0: 1, 2: 2, 3: 3}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'原图（起点 {SRC}，终点 {DST}，最多跳 {K} 条边）；节点下方是 dis[节点][层]', 22, T['muted'], bold=True)
    slot = (x1 - x0 - 170) / 3
    cx = lambda v: x0 + 85 + POS[v] * slot
    cy = y0 + 105
    now = S.get('now') if S.get('_line', 0) >= 15 else None
    nxt = S.get('nxt') if S.get('_line', 0) in (21, 24) else None
    for a, b, w in EDGES:
        hot = nxt is not None and now is not None and {a, b} == {now, nxt}
        cv.line([(cx(a), cy), (cx(b), cy)], T['yellow'] if hot else T['border'], 6 if hot else 3)
        cv.text(((cx(a) + cx(b)) / 2, cy - 14), w, 26, T['yellow'] if hot else T['text'], anchor='mb', bold=True)
    dis = S.get('dis')
    for v in range(N):
        c = T['yellow'] if v == now else (T['blue'] if v == nxt else T['panel2'])
        cv.rect((cx(v) - 34, cy - 34, cx(v) + 34, cy + 34), fill=c, outline=T['border'], r=34)
        cv.text((cx(v), cy), v, 32, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True)
        if v == SRC:
            cv.text((cx(v), cy - 42), '起点 s', 18, T['green'], anchor='mb', bold=True)
        if v == DST:
            cv.text((cx(v), cy - 42), '终点 d', 18, T['pink'], anchor='mb', bold=True)
        if dis:
            for lv in range(K + 1):
                val = dis[v][lv]
                cv.text((cx(v), cy + 52 + lv * 30), f'L{lv}: ' + ('·' if val is None else str(val)), 22,
                        T['green'] if val is not None else T['dim'], anchor='mt', mono=True, bold=val is not None)


def _tbl_color(S, i, j, v):
    if S.get('_line', 0) in (16, 17) and i == S.get('now') and j == S.get('level'):
        return 'yellow'
    return None


def _cap_pop(S, B, r):
    return (f'弹出堆顶 `[{S.nowd}, {S.now}, {S.level}]`：当前==代价最小==的状态 = 到「节点 {S.now}、已跳 {S.level} 次」花 `{S.nowd}`')


def _cap_if(S, B, r):
    if S.dis[S.now][S.level] is None:
        return f'`dis[{S.now}][{S.level}]` 还没定下来 → 第一次弹出它，代价 `{S.nowd}` 就是==最短==，可以确定'
    return f'`dis[{S.now}][{S.level}] = {S.dis[S.now][S.level]}` 早已确定 → 堆里的旧记录，直接丢弃'


def _cap_hop(S, B, r):
    return (f'邻居 `{S.nxt}`：还有名额（`level < k`）且那层没定 → ==免费跳==这条边 → 第 `{S.level + 1}` 层，代价不变 `{S.nowd}`，入堆 `[{S.nowd}, {S.nxt}, {S.level + 1}]`')


def _cap_pay(S, B, r):
    w = S.g[S.now][S.nxt]
    return (f'邻居 `{S.nxt}`：==付费走==，权 `{w}`，代价 `{S.nowd} + {w} = {S.nowd + w}`，留在第 `{S.level}` 层，入堆 `[{S.nowd + w}, {S.nxt}, {S.level}]`')


CONFIG = dict(
    num=2714, title='找到最短路径的K次跨越', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='分层图 Dijkstra',
    tags=['灵神题单·图论算法'],
    code='''
class Solution(object):
    def shortestPathWithHops(self, n, edges, s, d, k):

        g = {}
        for x, y, w in edges:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = w            

        dis = [[None] * (k + 1) for _ in range(n)]
        heap = [[0, s, 0]]
        while heap:
            nowd, now, level = heapq.heappop(heap)
            if dis[now][level] is None:
                dis[now][level] = nowd
                if now in g:
                    for nxt in g[now]:
                        if level < k and dis[nxt][level + 1] is None:
                            heapq.heappush(heap, [nowd, nxt, level + 1])
                        
                        if dis[nxt][level] is None:
                            heapq.heappush(heap, [nowd + g[now][nxt], nxt, level])

        return min(dis[d])
''',
    call=f'Solution().shortestPathWithHops({N}, {EDGES}, {SRC}, {DST}, {K})',
    expect=6,
    skip=['g = {}', 'for x, y, w in edges', 'if x not in g', 'g[x] = {}', 'if y not in g', 'g[y] = {}', 'g[x][y] = g[y][x]',
          'if now in g', 'for nxt in g[now]', 'while heap', 'if level < k and', 'if dis[nxt][level] is None'],
    max_steps=75,
    views=[
        dict(type='custom', draw=_draw, h=240),
        dict(type='table', var='dis', label='dis[节点][层]（行 = 节点，列 = 已跳过几条边；· = 还没定）', h=270, cell=56,
             rows=lambda S: list(range(N)), cols=lambda S: [f'L{i}' for i in range(K + 1)], color=_tbl_color),
        dict(type='heap', var='heap', label='heap：[代价, 节点, 层]', h=110, fmt=lambda x: f'{x[0]}|{x[1]}|{x[2]}'),
    ],
    watch=[('nowd', 'nowd', 'yellow'), ('now', 'now', 'cyan'), ('level', 'level', 'orange'), ('nxt', 'nxt', 'blue')],
    captions={
        'dis = [[None]': '`dis[i][j]`：从第 0 层的 `s` 出发，走到第 `j` 层节点 `i` 的最短路；`j` = 已经跳过的边数',
        'heap = [[0, s, 0]]': '小根堆放 `[代价, 节点, 层]`；起点在第 0 层，代价 0',
        'heappop': _cap_pop,
        'if dis[now][level] is None': _cap_if,
        'dis[now][level] = nowd': '定下 `dis[{now}][{level}]` = =={nowd}==',
        'heappush(heap, [nowd, nxt': _cap_hop,
        'heappush(heap, [nowd + g': _cap_pay,
        'return min(dis': '终点 `d = {d}` 各层里取最小：`dis[{d}]` = `{dis[d]}` → =={ret}==（跳的边数不一定要用满）',
    },
    cards=dict(
        one_liner='把图复制成 k+1 层：付费走留在本层，免费跳到下一层',
        complexity='时间 `O(k·E·log(k·E))`，空间 `O(n·k + E)`',
        problem=['无向带权图，`n` 个节点；可以把最多 `k` 条边的权变成 `0`',
                 '求从 `s` 到 `d` 的最短路长度',
                 '本视频：`n=4`，`s=1`，`d=3`，`k=1` → `6`'],
        quote='经典的分层图最短路问题。……对于图中的某条边(x, y, v)，既可以花费v的代价，从当前层的x出发走到当前层的y，也可以不花费任何代价，从当前层的x出发走到下一层的y。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dis[i][j]`：走到第 `j` 层的节点 `i` 的最短路，`j` 就是已经「跳」过的边数',
              '一条边两种走法：付费走（同层，加权）或免费跳（下一层，代价不变）',
              '不用真的建 `k` 层图：遍历原图的边，按两种情况分别入堆',
              '最后 `min(dis[d])`：终点在任意一层的最小值',
              '视频里折叠了入堆前的判断，只展示真正入堆的那几步'],
        summary=['时间 `O(k·E·log(k·E))`，空间 `O(n·k + E)`',
                 '堆里的元素是 `[代价, 节点, 层]`，弹出时才确定最短（旧记录直接丢弃）',
                 '免费跳要判 `level < k`，否则数组越界',
                 '最终答案是 `min(dis[d])`，不是只看第 `k` 层',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
