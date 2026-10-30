GRAPH = [[4, 3, 1], [3, 2, 4], [3], [4], []]
POS = {0: (0.04, 0.5), 1: (0.34, 0.08), 2: (0.70, 0.08), 3: (0.52, 0.92), 4: (0.96, 0.5)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = GRAPH
    n = len(g)
    ind = S.get('ind')
    q = S.get('q') or []
    W, H, R = (x1 - x0) * 0.62, (y1 - y0) - 95, 28

    def P(u):
        fx, fy = POS[u]
        return x0 + 50 + fx * W, y0 + 35 + fy * H

    now, nxt = S.get('now'), S['_inner'].get('next')
    for u, vs in enumerate(g):
        for v in vs:
            (ax, ay), (bx, by) = P(u), P(v)
            dx, dy = bx - ax, by - ay
            L = max(1.0, (dx * dx + dy * dy) ** 0.5)
            ux, uy = dx / L, dy / L
            hot = (u, v) == (now, nxt)
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 4), by - uy * (R + 4)),
                     T['yellow'] if hot else T['muted'], 5 if hot else 3, 14)
    for u in range(n):
        X, Y = P(u)
        inq = u in q
        fill = T['green'] if inq else T['panel2']
        on = u == now
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill,
                     outline=T['yellow'] if on else T['border'], width=5 if on else 2)
        cv.text((X, Y), u, 28, T['bg'] if inq else T['text'], anchor='mm', bold=True)
        if isinstance(ind, list):
            if POS[u][1] > 0.8:
                cv.text((X, Y + R + 4), f'入度 {ind[u]}', 18, T['orange'], anchor='mt', bold=True)
            else:
                cv.text((X, Y - R - 4), f'入度 {ind[u]}', 18, T['orange'], anchor='mb', bold=True)
    lx = x0 + 50 + W + 70
    cv.d.ellipse((lx, y0 + 40, lx + 26, y0 + 66), fill=T['green'], outline=T['border'])
    cv.text((lx + 38, y0 + 53), '已进入拓扑序 q', 20, T['muted'], anchor='lm')
    cv.text((lx, y0 + 90), '黄圈 = 当前处理的 now', 19, T['dim'])
    cv.text((lx, y0 + 120), '黄边 = now → next', 19, T['dim'])


_LP = lambda S: None if 'f' in S else S.get('l')


def _f(S):
    f = S.get('f')
    if not isinstance(f, list):
        return None
    return {k: v for k, v in enumerate(f)}


def _ffmt(k, v):
    if not v:
        return f'f[{k}] = []'
    return f'f[{k}] = ' + ' | '.join('→'.join(map(str, p)) for p in v)


def _dp_for(S, B, ret):
    if 'f' in B and B.get('now') == S.q[S.index] and B.index == S.index:
        return '反向 DP 结束'
    return f'按拓扑序==从右往左==：`q[{S.index}] = {S.q[S.index]}`，计算 `f[{S.q[S.index]}]`'


def _ext(S, B, ret):
    now, nxt = S.now, S.next
    add = [[now] + p for p in S.f[nxt]]
    s = '、'.join('→'.join(map(str, p)) for p in add)
    return f'`f[{nxt}]` 里每条路径前面接上 {now}：`f[{now}]` 加入 {s}'


CONFIG = dict(
    num=797, title='所有可能的路径', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='拓扑排序 + 反向 DP',
    tags=['labuladong', '灵神题单·图论算法'],
    code='''
class Solution(object):
    def allPathsSourceTarget(self, graph):

        n = len(graph)
        ind = [0] * n
        g = {}
        for index, next_list in enumerate(graph):
            g[index] = set()
            for next in next_list:
                ind[next] += 1
                g[index].add(next)

        if ind[n - 1] == 0:
            return []

        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)

        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1
                    if next == n - 1:
                        break
            if ind[n - 1] == 0:
                break

        if ind[n - 1] != 0:
            return []

        f = [[] for _ in range(n)]
        f[n - 1].append([n - 1])
        for index in range(len(q) - 2, -1, -1):
            now = q[index]
            for next in g[now]:
                if ind[next] == 0:
                    f[now].extend([[now] + path for path in f[next]])

        return f[0]
''',
    call=f'Solution().allPathsSourceTarget({GRAPH})',
    expect=[[0, 1, 2, 3, 4], [0, 1, 3, 4], [0, 1, 4], [0, 3, 4], [0, 4]],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='q', label='q（拓扑序；暗 = 已处理）', cell=70, h=130, pointers={_LP: 'blue'}, pointer_labels={_LP: 'l'},
             dim=lambda S, i, v: 'f' not in S and i < S.get('l', 0)),
        dict(type='map', var=_f, label='f[x]：从 x 到 n−1 的所有路径', fmt=_ffmt, h=230, font=22),
    ],
    watch=[('now', 'now', 'yellow'), ('next', lambda S: S['_inner'].get('next')), 'l', 'r'],
    skip=['n = len(graph)', 'g = {}', 'g[index] = set()', 'g[index].add(next)', 'for next in next_list',
          'q = []', 'l = 0', 'r = len(q)', 'r += 1', 'if next == n - 1', 'if ind[n - 1] != 0',
          13, 'f = [[] for', 10, 17, 19, 23, 25, 26, 27, 29, 42],
    captions={
        'ind = [0] * n': '先做拓扑排序：统计每个点的==入度==',
        'for index, next_list in enumerate(graph)': lambda S, B, r: (f'点 {S.index} 的出边 → `{S.next_list}`，这些终点入度各 +1'
                                                                    if 'index' not in B or B.index != S.index else f'入度统计完毕：`ind = {S.ind}`'),
        14: '终点 n−1 有入边，可能有路径',
        18: lambda S, B, r: (f'`ind[{S.index}] = 0`：入度为 0，==入队==' if S.ind[S.index] == 0
                             else f'`ind[{S.index}] = {S.ind[S.index]}`，暂不入队'),
        24: '取出 `now = {now}`：它的每条出边终点入度 −1',
        28: lambda S, B, r: (f'边 `{S.now} → {S.next}`：`ind[{S.next}]` 减到 0 → {S.next} ==入队=='
                             if S.ind[S.next] == 0
                             else f'边 `{S.now} → {S.next}`：`ind[{S.next}]` 减到 {S.ind[S.next]}，还有别的前驱没处理'),
        31: '终点 {next} 已入队 → 跳出',
        33: lambda S, B, r: ('终点 n−1 入度减到 0、已经入队' if S.ind[S.n - 1] == 0 else f'终点入度还是 {S.ind[S.n - 1]}，继续 bfs'),
        34: '==拓扑排序可以提前终止==：没入队的点不会在 0 到 n−1 的路径上',
        'f[n - 1].append([n - 1])': '`f[x]` = 从 x 到 n−1 的所有路径。边界：`f[{n-1}] = [[{n-1}]]`',
        41: _dp_for,
        43: lambda S, B, r: (f'边 `{S.now} → {S.next}`' if not S.f[S.now] or B.get('next') != S.get('next')
                             else f'`f[{S.now}]` 算好了'),
        44: lambda S, B, r: (f'`ind[{S.next}] == 0`：{S.next} 在拓扑序里，`f[{S.next}]` 已算好 → 可以转移' if S.ind[S.next] == 0
                             else f'{S.next} 不在拓扑序里，跳过'),
        'f[now].extend': _ext,
        'return f[0]': '`f[0]` 就是答案：共 =={len(ret)}== 条路径',
    },
    max_steps=70,
    cards=dict(
        one_liner='f[x] = 从 x 到 n−1 的所有路径；按拓扑序反着做 DP',
        complexity='时间 `O(2^n · n)`，空间 `O(2^n · n)`',
        problem=['有向无环图 `graph`，`graph[i]` 是从 i 出发能到的点',
                 '找出所有从 `0` 到 `n − 1` 的路径（顺序不限）',
                 '示例：`[[4,3,1],[3,2,4],[3],[4],[]]` → 5 条路径'],
        quote='令f[x]表示节点x到n - 1的所有路径，那么我们就是要求f[0]。……由于给出的图是有向无环图，那么可以==先执行一次拓扑排序==，确定各个顶点的序，然后==根据这个序反向来做动态规划==。',
        quote_src='—— yiduobo 题解原文',
        idea=['n 很小，直接 dfs 也行；作者选了 DP：`f[now]` 由每个后继 `f[next]` 前面接上 now 得到',
              '拓扑排序保证算 `f[now]` 时，后继的 `f[next]` 都已算好',
              '终点入队后拓扑排序就能==提前终止=='],
        summary=['路径数最多 `2^(n-2)` 条，每条长 `O(n)`，复杂度由输出规模决定',
                 '转移：`f[now].extend([[now] + path for path in f[next]])`',
                 '只转移 `ind[next] == 0` 的后继：没进入拓扑序的点到不了终点',
                 '易错：DP 要按拓扑序==从后往前==，否则 `f[next]` 还没算出来',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
