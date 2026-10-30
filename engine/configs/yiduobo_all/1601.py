_NAMES = ['0', '1', '2', 's', 't']


def _c(S, i, j, v):
    now, pv = S['_inner'].get('now'), S['_inner'].get('prev')
    if S.get('_line', 0) >= 46 and isinstance(pv, list):  # 回溯增广路径阶段
        if i == pv[j] and v > 0 and S['_inner'].get('now') is not None and j == S['_inner']['now']:
            return 'yellow'
    if i == now and v > 0 and S.get('_line', 0) < 46:
        return 'blue'
    return None


CONFIG = dict(
    num=1601, title='最多可达成的换楼请求数目', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='最小费用最大流（费用 0/1）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def maximumRequests(self, n, requests):

        s = n
        t = s + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        v = [[0] * (t + 1) for _ in range(t + 1)]

        ind = [0] * n
        oud = [0] * n
        for x, y in requests:
            c[x][y] += 1
            v[x][y] = 1
            ind[y] += 1
            oud[x] += 1

        for index in range(n):
            if ind[index] > oud[index]:
                c[index][t] = ind[index] - oud[index]
            else:
                c[s][index] = oud[index] - ind[index]

        res = len(requests)
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                next = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + v[now][index]):
                        dis[index] = dis[now] + v[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        next = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res

                used.add(next)
                now = next

            now = t
            f = None
            while now != s:
                if f is None or f > c[prev[now]][now]:
                    f = c[prev[now]][now]
                now = prev[now]

            res -= dis[t] * f
            now = t
            while now != s:
                c[now][prev[now]] += f
                c[prev[now]][now] -= f
                now = prev[now]
''',
    call='Solution().maximumRequests(3, [[0, 1], [1, 0], [0, 2]])',
    expect=2,
    views=[
        dict(type='table', var='c', label='c[x][y]：残量网络容量（行 = 起点，列 = 终点；s = 源，t = 汇）', h=290, cell=84,
             rows=_NAMES, cols=_NAMES, color=lambda S, i, j, v: 'blue' if i == S['_inner'].get('now') and v > 0 else None),
        dict(type='array', var='dis', label='dis[点]：从 s 到该点已用的最小费用（空 = 还没到）', cell=70, h=130),
        dict(type='array', var='prev', label='prev[点]：最短路上的前驱', cell=70, h=130),
        dict(type='text', h=50, fn=lambda S: f"当前可保留的请求数 `res` = =={S['_inner'].get('res', S.get('res'))}==" if 'res' in S else ''),
    ],
    watch=[('now', 'now', 'blue'), ('f', 'f', 'yellow'), ('res', 'res', 'green')],
    skip=['s = n', 't = s + 1', 'c = [[0]', 'v = [[0]', 'ind = [0]', 'oud = [0]', 'for x, y in requests', 'for index in range(n)', 'for index in range(t + 1)',
          'min_dis = None', 'next = None', 'if index in used', 'used.remove', 'prev = [None]', 'used = set', 'v[x][y] = 1', 'ind[y] += 1', 'oud[x] += 1',
          'dis[index] = dis[now]', 'if c[now][index] > 0', 'if index not in used', 'prev[index] = now', 'next = index', 'min_dis = dis[index]', 'now = prev[now]', 'f = None', 'now = t', 'now = s', 'while now != s', 'if f is None'],
    max_steps=110,
    captions={
        'c[x][y] += 1': '请求 `{x} → {y}`：边容量 +1（同样的请求出现几次就是几）',
        'if ind[index] > oud[index]': '楼 `{index}`：进 `{ind[index]}`，出 `{oud[index]}` → {"进多于出，向汇 t 连边" if ind[index] > oud[index] else "出不少于进，从源 s 连边"}',
        'c[index][t] =': '进来的人多 `{ind[index] - oud[index]}` → 连 `{index} → t`，容量 = =={c[index][t]}==',
        'c[s][index] =': '出去的人不少于进来 → 连 `s → {index}`，容量 = =={c[s][index]}==（可能是 0）',
        'res = len(requests)': '先假设请求全部能满足 `res = {res}`；之后每“牺牲”一个请求，`res` 减 1',
        'dis[s] = 0': '每轮找一条 s→t 的最小费用增广路：`dis[s] = 0`，从 `s` 出发',
        'while t not in used': lambda S, B, ret: (f"`t` 还没确定最短费用 → 从 `{S['now']}` 出发，沿容量 > 0 的边更新 `dis` 和 `prev`" if 't' in S and S['t'] not in S['used']
                                                  else '`t` 已确定最短费用 → 找到增广路，退出'),
        'if min_dis is None': lambda S, B, ret: ('扩展完 `{}` 的出边，没有任何未确定的点可达 → 再也找不到增广路'.format(S['now']) if S['min_dis'] is None
                                                 else f"扩展完 `{S['now']}` 的出边：未确定的点里 `dis` 最小的是 `{S['next']}`（`dis` = {S['min_dis']}）"),
        'return res': '没有增广路 → 最终保留的请求数 =={ret}==',
        'used.add(next)': '确定 `{next}` 的最短费用 `dis[{next}] = {dis[next]}`，下一轮从它扩展',
        'now = next': '移动到 `{now}`，继续扩展，直到 `t` 被确定',
        'f = c[prev[now]][now]': '沿着 `prev` 从 t 往回走，取路上容量最小值作为流量 `f` = =={f}==',
        'res -= dis[t] * f': '这条路总费用 `dis[t] = {dis[t]}`，流量 `f = {f}` → 牺牲 `{dis[t] * f}` 个请求：`res` = =={res}==',
        'c[now][prev[now]] += f': '沿路修改残量：反向边容量 +{f}',
        'c[prev[now]][now] -= f': '正向边容量 −{f}：`c[{prev[now]}][{now}]` = =={c[prev[now]][now]}==',
    },
    cards=dict(
        one_liner='不平衡的人流用最小费用最大流抹平，费用 = 被牺牲的请求',
        complexity='时间 `O(流量 · V^2)`，空间 `O(V^2)`',
        problem=['`n` 栋楼，`requests[i] = [from, to]` 表示有人要从 from 搬到 to',
                 '同意一批请求后，每栋楼进出的人数必须相等；求最多能同意几个请求',
                 '本视频：`n=3`，请求 `[[0,1],[1,0],[0,2]]` → 2'],
        quote='对于每个节点，统计其入度和出度。若入度大于出度，那么从该节点到汇点连一条容量为入度减去出度的边；反过来，若出度大于入度，则从源点到该节点连一条容量为出度减取入度的边。',
        quote_src='—— yiduobo 题解',
        idea=['请求是有向边：容量 = 出现次数，费用 = 1（牺牲它）',
              '不平衡的楼接到源 s 或汇 t，用最大流把不平衡抹平，流过的请求就是被删掉的',
              '要删得最少 → 最小费用最大流；费用只有 0/1，每轮用类 Dijkstra 找最短增广路'],
        result='最小费用 1，保留 3 − 1 = 2 个请求',
        summary=['时间约 `O(流量 · V^2)`，空间 `O(V^2)`，邻接矩阵实现',
                 '`res = 请求总数 − 最小费用`：费用 1 对应牺牲 1 个请求',
                 '每轮增广量不一定是 1，要取路径上容量的最小值',
                 '残量网络：正向边减 `f`，反向边加 `f`',
                 '题面为 LeetCode 1601（库中没有题面，按 yiduobo 文章与题意整理）'],
    ),
)
