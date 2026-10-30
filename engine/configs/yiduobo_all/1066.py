W = [[0, 0], [2, 1]]
BK = [[1, 2], [3, 3]]
NAMES = ['s', 'w0', 'w1', 'b0', 'b1', 't']


def _ccolor(S, i, j, v):
    if v > 0:
        if i == S.get('now') and 'res' in S:
            return 'yellow'
        return 'blue'
    return None


def _txt(S):
    L = S.get('_line', 0)
    if 'res' not in S:
        return '节点：`s`=0，工人 `w0..`，自行车 `b..`，汇点 `t`；边权 = 曼哈顿距离'
    if 'dis' in S and S['dis'][-1] is not None and L >= 38:
        path = []
        now = len(S['dis']) - 1
        pv = S['prev']
        while now is not None and pv[now] is not None:
            path.append(NAMES[now])
            now = pv[now]
        path.append('s')
        return '最短增广路：`' + ' ← '.join(path) + f"`，本轮费用 `{S['dis'][-1]}`，累计 `res = {S['res']}`"
    return f"已累计费用 `res = {S['res']}`；每一轮找一条 s→t 的最便宜增广路"


CONFIG = dict(
    num=1066, title='校园自行车分配II', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='最小费用最大流',
    tags=['图论算法', '动态规划'],
    code='''
class Solution(object):
    def assignBikes(self, workers, bikes):

        n = len(workers)
        m = len(bikes)

        s = 0
        t = m + n + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        cost = [[0] * (t + 1) for _ in range(t + 1)]

        for i in range(1, n + 1):
            c[s][i] = 1
        for i in range(n + 1, m + n + 1):
            c[i][t] = 1
        
        for i in range(n):
            for j in range(m):
                v = abs(workers[i][0] - bikes[j][0]) + abs(workers[i][1] - bikes[j][1])
                c[i + 1][j + n + 1] = 1
                cost[i + 1][j + n + 1] = v
                cost[j + n + 1][i + 1] = -v
        
        res = 0
        for _ in range(n):
            heap = [[0, s, None]]
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            while heap:
                d, now, last = heapq.heappop(heap)
                if dis[now] is None:
                    dis[now] = d
                    prev[now] = last
                    for next in range(t + 1):
                        if c[now][next] > 0:
                            heapq.heappush(heap, [d + cost[now][next], next, now])
                
            res += dis[t]
            now = t
            while now != s:
                last = prev[now]
                c[last][now] -= 1
                c[now][last] += 1
                now = last
        
        return res
''',
    call=f'Solution().assignBikes({W}, {BK})',
    expect=6,
    skip=['n = len', 'm = len', 's = 0', 'c = [[0]', 'cost = [[0]', 'for i in range', 'for j in range', 'v = abs',
          'c[i + 1][j + n + 1] = 1', 'cost[i + 1]', 'cost[j + n + 1]', 'c[s][i] = 1', 'c[i][t] = 1',
          'for next in range', 'if c[now][next] > 0', 'prev[now] = last', 'while now != s', 'heapq.heappush', 'prev = [None]', 'c[last][now] -= 1', 'while heap', 'now = t', 'last = prev[now]', 'now = last'],
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='table', var='c', label='c：剩余容量（蓝 = 还能走；黄 = 正在扩展的出发点）', h=330, cell=60,
             rows=NAMES, cols=NAMES, color=_ccolor),
        dict(type='table', var='cost', label='cost：边费用（反向边为负）', h=330, cell=60, rows=NAMES, cols=NAMES),
        dict(type='array', var='dis', label='dis：s 到各点的最短费用', h=170, cell=80,
             pointers={'now': 'blue'}),
    ],
    watch=['now', 'd', 'last', ('res', 'res', 'green')],
    captions={
        't = m + n + 1': '`t = {t}`',
        'res = 0': '`res` 累计费用，共跑 `n = {n}` 轮：每轮给一个工人配一辆车',
        'for _ in range': '找一条 s→t 的最便宜增广路（共 `n` 轮，每轮多配一对）',
        'heap = [[0, s, None]]': '堆里存 `[距离, 节点, 来自哪个节点]`，从源点 `s` 出发',
        'dis = [None]': '`dis` 记录最短费用；`prev` 记录路径上的前驱',
        'heapq.heappop': lambda S, B, r: f'弹出堆里距离最小的：`{NAMES[S.now]}`，距离 `d = {S.d}`',
        'if dis[now] is None': lambda S, B, r: (f'`{NAMES[S.now]}` 第一次弹出 → ==距离定为 {S.d}==' if S.dis[S.now] is None
                                                  else f'`{NAMES[S.now]}` 已经有距离，跳过这条旧记录'),
        'dis[now] = d': lambda S, B, r: f'`dis[{S.now}] = {S.d}`，前驱 `prev` 记为 {NAMES[S.last] if S.last is not None else "无"}；再把容量 > 0 的出边按 `d + 费用` 压入堆',
        'res += dis[t]': '这条增广路总费用 `dis[t] = {dis[t]}` → `res = {res}`',
        'c[now][last] += 1': lambda S, B, r: f'沿路径回溯：`{NAMES[S.last]}→{NAMES[S.now]}` 容量 −1，反向边 +1（后面的轮次可以==反悔==）',
        'return res': '最小费用最大流的费用 `{res}` 就是最小总距离',
    },
    cards=dict(
        one_liner='工人到自行车建二分图，跑一趟最小费用最大流',
        complexity='时间 `O(n · V²)` 量级，空间 `O(V²)`（V = n + m + 2）',
        problem=['平面上有 `n` 个工人和 `m` 辆自行车（`n ≤ m`）',
                 '每人分配一辆不同的车，距离用==曼哈顿距离==',
                 '求所有人距离之和的最小值',
                 '本视频：工人 `[[0,0],[2,1]]`，自行车 `[[1,2],[3,3]]` → `6`'],
        quote='从题目的数据规模来看应该是想要用状态压缩动态规划来实现，不过在这里使用km算法或网络流是更好的选择。我在这里使用的是费用流。',
        quote_src='—— yiduobo 题解原文',
        idea=['源点 → 每个工人（容量 1，费用 0）；每辆车 → 汇点（容量 1，费用 0）',
              '工人 → 自行车：容量 1，费用 = 曼哈顿距离，并配一条费用取负的反向边',
              '每轮找一条最便宜的 s→t 路径推 1 单位流，共 `n` 轮，费用累加即答案'],
        summary=['时间约 `O(n · V²)`，空间 `O(V²)`（用邻接矩阵存图）',
                 '反向边容量为 0、费用为负：它让后续增广路能撤销之前的分配',
                 '原文用堆做最短路；有负权反向边时需要小心，作者的写法在题目规模下可通过',
                 '原文为 Python 2 风格，代码未改，可直接在 Python 3 运行'],
    ),
)
