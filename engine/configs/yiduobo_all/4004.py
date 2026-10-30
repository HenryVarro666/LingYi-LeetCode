def _bcolor(S, i, v):
    if v > 0:
        return 'green'
    if v < 0:
        return 'pink'
    return None


def _txt(S):
    if 'res' not in S:
        return '绿 = 有余额可以送出，粉 = 欠款要接收；每次移动 1 单位，沿环走一步费用 1'
    L = S.get('_line', 0)
    if 'flow' in S and L >= 84:
        return f"本轮沿最短路推 `flow = {S['flow']}` 单位，每单位费用 `dis[t] = {S['dis'][S['t']]}` → `res = {S['res']}`"
    return f"累计移动次数 `res = {S['res']}`；每轮 SPFA 找 s→t 最便宜的路"


CONFIG = dict(
    num=4004, title='使循环数组余额非负的最少移动次数II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='最小费用流（环上相邻连边 + SPFA）',
    tags=['图论算法'],
    code='''
class Solution(object):
    def minMoves(self, balance):
        
        if sum(balance) < 0:
            return -1
        
        if min(balance) >= 0:
            return 0
        
        n = len(balance)
        s = n
        t = s + 1
        pre = []
        last = [None] * (n + 2)
        edges = []

        def add_edge(x, y, c, cost, pre, last, edges):
            m = len(edges)
            edges.append([y, c, cost])
            pre.append(last[x])
            last[x] = m

            m += 1
            edges.append([x, 0, -cost])
            pre.append(last[y])
            last[y] = m

        tot = 0
        for index, v in enumerate(balance):
            if v > 0:
                add_edge(s, index, v, 0, pre, last, edges)
            elif v < 0:
                add_edge(index, t, -v, 0, pre, last, edges)
                tot -= v

        for index in range(n):
            left = index - 1
            if left < 0:
                left += n
            add_edge(index, left, tot, 1, pre, last, edges)

            right = index + 1
            if right == n:
                right = 0
            add_edge(index, right, tot, 1, pre, last, edges)

        res = 0
        while True:
            dis = [None] * (t + 1)
            edge_idx = [None] * (t + 1)
            used = [False] * (n + 2)
            used[s] = True            
            q = [s]
            head, tail = 0, 1
            dis[s] = 0
            while head < tail:
                now = q[head]
                head += 1
                used[now] = False
                
                index = last[now]
                while index is not None:
                    nxt, c, cost = edges[index]
                    if c > 0 and (dis[nxt] is None or dis[nxt] > dis[now] + cost):
                        dis[nxt] = dis[now] + cost
                        edge_idx[nxt] = index
                        if not used[nxt]:
                            q.append(nxt)
                            tail += 1
                            used[nxt] = True
                    
                    index = pre[index]

            if dis[t] is None:
                return res

            now = t
            flow = tot
            while now != s:
                index = edge_idx[now]
                flow = min(flow, edges[index][1])
                now = edges[index ^ 1][0]

            res += flow * dis[t]
            now = t
            while now != s:
                index = edge_idx[now]
                edges[index][1] -= flow
                edges[index ^ 1][1] += flow
                now = edges[index ^ 1][0]
''',
    call='Solution().minMoves([2, -1, 0, -1, 1])',
    expect=2,
    skip=['pre = []', 'last = [None]', 'edges = []', 'def add_edge', 'm = len(edges)', 'edges.append', 'pre.append',
          'last[x] = m', 'last[y] = m', 'm += 1', 'tot = 0', 'for index, v in enumerate', 'left = index - 1',
          'if left < 0', 'left += n', 'right = index + 1', 'if right == n', 'right = 0', 'for index in range(n)',
          'used = [False]', 'q = [s]', 'dis[s] = 0', 'edge_idx = [None]', 'if v > 0', 'elif v < 0', 'index = last[now]',
          'while index is not None', 'nxt, c, cost = edges[index]', 'index = pre[index]', 'head += 1', 'used[now] = False',
          'while head < tail', 'q.append(nxt)', 'used[nxt] = True', 'tail += 1', 'if not used[nxt]',
          'edge_idx[nxt] = index', 'now = t', 'flow = tot', 'index = edge_idx[now]', 'edges[index][1] -= flow',
          'edges[index ^ 1][1] += flow', 'now = edges[index ^ 1][0]', 'now = q[head]', 'while now != s',
          'flow = min(flow', 'if c > 0 and (dis[nxt]', 'add_edge(index, left, tot, 1', 'while True', 'dis = [None] * (t + 1)'],
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='balance', label='balance（环形数组；绿 = 能送出，粉 = 需要接收）', h=210, cell=90,
             color=lambda S, i, v: 'blue' if i == S.get('now') else _bcolor(S, i, v)),
        dict(type='array', var=lambda S: S['dis'][:len(S['balance'])] if 'dis' in S else None,
             label='dis：s 到各下标的最短费用（None = 暂时到不了）', h=210, cell=90, color=lambda S, i, v: 'blue' if i == S.get('now') else None),
        dict(type='array', var=lambda S: [x for x in S['q'][S['head']:]] if 'q' in S and 'head' in S else None,
             label='SPFA 队列（还没处理的点）', h=190, cell=80),
    ],
    watch=['tot', ('res', 'res', 'green'), 'flow', 'now'],
    captions={
        'if sum(balance) < 0': '总和 `{sum(balance)}` ≥ 0：所有余额加起来够补，有解',
        'if min(balance) >= 0': '有人为负（`min = {min(balance)}`），需要真正去转移',
        'n = len(balance)': '`n = {n}`，源点 `s = {s}`、汇点 `t = {t}` 各占一个编号',
        'add_edge(s, index, v, 0': '余额为正：源 → 该点，容量 `{v}`，费用 0',
        'add_edge(index, t, -v, 0': '余额为负：该点 → 汇，容量 `{-v}`，费用 0',
        'tot -= v': '`tot` 累计总欠款 = `{tot}`',
        'add_edge(index, left, tot, 1': '环上相邻连边：`{index} → {left}`，容量放大成 `tot`（可能当中转），费用 1',
        'add_edge(index, right, tot, 1': '下标 `{index}` 与左右邻居 `{left}`、`{right}` 双向连边：容量 `tot`（可当中转），费用 1',
        'while True': '每轮用 SPFA 找一条 s→t 的最便宜路',
        'dis = [None] * (t + 1)': '重置最短费用数组',
        'if c > 0 and (dis[nxt]': lambda S, B, r: (f'边 `{S.now}→{S.nxt}` 容量 {S.c}，费用 {S.cost}：`{S.dis[S.now]}+{S.cost}` 比当前更小 → ==松弛=='
                                                     if S.c > 0 and (S.dis[S.nxt] is None or S.dis[S.nxt] > S.dis[S.now] + S.cost)
                                                     else f'边 `{S.now}→{S.nxt}` 容量 {S.c}：不能更优或没容量，跳过'),
        'dis[nxt] = dis[now] + cost': '边 `{now}→{nxt}` 容量 {c}、费用 {cost}：更便宜 → ==松弛== `dis[{nxt}] = {dis[nxt]}`，入队等待继续扩展',
        'if dis[t] is None': lambda S, B, r: ('t 不可达 → 没有增广路了，结束' if S.dis[S.t] is None
                                               else f'找到最短路，到汇点费用 `dis[t] = {S.dis[S.t]}`'),
        'return res': '没有更多增广路，最少移动次数 `{ret}`',
        'res += flow * dis[t]': '这条路推 `{flow}` 单位，每单位费用 `{dis[t]}` → `res = {res}`',
    },
    cards=dict(
        one_liner='欠款人当汇、有钱人当源，沿环上相邻边跑最小费用流',
        complexity='时间 `O(n · SPFA)`，空间 `O(n)`',
        problem=['环形数组 `balance`，一次移动可把 1 单位余额给左/右邻居',
                 '要让所有人余额都非负，求最少移动次数；做不到返回 `-1`',
                 '本视频：`[2,-1,0,-1,1]` → `2`'],
        quote='不直接在正负余额之间连边，而是在下标相邻之间的节点连边，此时边的容量需要为总容量，理由是此时的节点可能作为其他节点的中转，因此边的容量需要放大最大，而费用则为1，因为是相邻移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['正余额 → 源，负余额 → 汇，转移总量恰好等于总欠款',
              '正负点两两连边是 `O(n^2)` 条会超时；改成只在环上相邻点连边（费用 1）',
              '相邻边容量设成 `tot`：中间的点可以当中转站；每轮 SPFA 增广'],
        summary=['先判断：总和为负返回 `-1`；全部非负返回 `0`',
                 '边数从 `O(n^2)` 降到 `O(n)`，用前向星存图（正反边成对存）',
                 '相邻点之间有正反重边，所以不能用邻接矩阵',
                 '原文作者也提到：按数据范围网络流可能被构造数据卡掉',
                 '原文为 Python 2 风格，代码未改，可直接在 Python 3 运行'],
    ),
)
