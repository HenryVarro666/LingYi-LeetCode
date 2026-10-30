def _nm(S, x):
    m, n = S['m'], S['n']
    if x < m:
        return f'左{x}'
    if x < m + n:
        return f'右{x - m}'
    return {m + n: 'S', m + n + 1: 'T', m + n + 2: 'SS', m + n + 3: 'TT'}[x]


def _names(S):
    return [_nm(S, x) for x in range(S['m'] + S['n'] + 4)]


def _chain(S):
    p, now, out = S['prev'], S['super_t'], []
    while now is not None:
        out.append(now)
        now = p[now]
    return out[::-1]


def _path(S):
    if 'prev' not in S or S['dis'][S['super_t']] is None:
        return set()
    p, now, out = S['prev'], S['super_t'], set()
    while now is not None and now != S['super_s']:
        out.add((p[now], now))
        now = p[now]
    return out


def _cc(S, r, c, v):
    if 'dis' not in S:
        return None
    if S['super_t'] in S.get('used', ()) and (r, c) in _path(S):
        return 'yellow'
    if v > 0 and r == S.get('now') and S.get('_line') in (51, 52, 53):
        return 'blue'
    return None


def _txt(S):
    if 'dis' not in S:
        return '每个点至少连一条边 = 流量有下限 → 加 SS/TT 把它变成普通费用流；左右之间的边：容量 1，费用 `cost[i][j]`'
    return f"黄 = 刚找到的增广路（SS → TT）；累计费用 `res = {S.get('res', 0)}`"


CONFIG = dict(
    num=1595, title='连通两组点的最小成本', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='有流量下限的最小费用流（网络流）',
    tags=['网络流', '其他状压 DP', '难度分 2538'],
    code='''
class Solution(object):
    def connectTwoGroups(self, cost):

        m = len(cost)
        n = len(cost[0])
        s = m + n
        t = s + 1
        super_s = t + 1
        super_t = super_s + 1

        c = [[0] * (super_t + 1) for _ in range(super_t + 1)]
        v = [[0] * (super_t + 1) for _ in range(super_t + 1)]

        for i in range(m):
            c[s][i] = n - 1
            c[super_s][i] = 1
        
        for j in range(m, m + n):
            c[j][t] = m - 1
            c[j][super_t] = 1

        c[t][super_s] = n
        c[s][super_t] = m - n
        c[super_t][s] = n
        c[t][s] = m * n - n
        c[s][t] = n

        for i in range(m):
            for j in range(n):
                c[i][j + m] = 1
                v[i][j + m] = cost[i][j]
                v[j + m][i] = -cost[i][j]
        
        res = 0
        while True:
            dis = [None] * (super_t + 1)
            prev = [None] * (super_t + 1)
            used = set([super_s])
            dis[super_s] = 0
            now = super_s
            while super_t not in used:
                min_dis = None
                nxt = None
                for index in range(super_t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + v[now][index]):
                        dis[index] = dis[now] + v[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        nxt = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res
                
                used.add(nxt)
                now = nxt

            res += dis[super_t]
            now = super_t
            while now != super_s:
                c[now][prev[now]] += 1
                c[prev[now]][now] -= 1
                now = prev[now]
''',
    call='Solution().connectTwoGroups([[1,3,5],[4,1,1],[1,5,3]])',
    expect=4,
    views=[
        dict(type='table', var='c', label='容量矩阵 c[u][v]（黄 = 本轮增广路；蓝 = 当前结点的出边）', h=430, cell=40,
             rows=_names, cols=_names, color=_cc),
        dict(type='array', var='dis', label='dis（None = 还没到过）', h=120, cell=48),
        dict(type='text', fn=_txt, size=22, h=60),
    ],
    watch=[('now', 'now', 'blue'), ('nxt', 'nxt', 'pink'), ('res', 'res', 'green')],
    skip=['for i in range(m)', 'for j in range(n)', 'for j in range(m, m + n)', 'for index in range', 'c[s][i] = n - 1',
          'c[super_s][i] = 1', 'c[j][t] = m - 1', 'c[j][super_t] = 1', 'v[i][j + m]', 'v[j + m][i]', 'while True',
          'min_dis = None', 'nxt = None', 'if c[now][index]', 'dis[index] = dis[now]', 'prev[index] = now',
          'if index in used', 'used.remove', 'if index not in used', 'nxt = index', 'min_dis = dis[index]', 'n = len',
          'now = super_s', 'while super_t not in used', 'v = [[0]', 'now = nxt', 'while now != s', 'c[prev[now]][now] -= 1', 'c[i][j + m] = 1',
          'now = prev[now]', 'c[now][prev[now]] += 1', 'if min_dis is None', 'prev = [None]', 'used = set',
          'dis[super_s] = 0', 'c[t][s]', 'c[s][t]', 'c[super_t][s]', 'c[s][super_t]', 'super_t = super_s',
          'super_s = t', 't = s', 's = m'],
    captions={
        'm = len(cost)': '`m` = 第一组点数（左），`n` = 第二组点数（右）；题目保证 `m >= n`',
        'c = [[0]': '建图：点 `0..m-1` 是左组，`m..m+n-1` 是右组，另有源点 `S`、汇点 `T` 和一对超级源汇 `SS`、`TT`，共 `{len(c)}` 个点',
        'c[t][super_s] = n': '给「每点至少 1 次」的流量下限做变形：把下限 1 分流给 `SS`/`TT`，再补几条平衡边（`T→SS`、`S→TT`、`TT→S`、`T→S`、`S→T`）',
        'res = 0': '左右两组之间每对点连一条边：容量 1（可用可不用），费用 `cost[i][j]`；图建好，求 `SS → TT` 的最小费用最大流，累计费用就是答案',
        'dis = [None]': '新一轮：从 `SS` 出发，用最短路找一条费用最小的增广路',
        'min_dis is None': lambda S, B, r: ('没有新的点可扩展 → 再也找不到增广路，返回 `res`' if S.min_dis is None else '还有可扩展的点'),
        'used.add(nxt)': lambda S, B, r: f'未定的点里 `dis` 最小的是 `{_nm(S, S.nxt)}`（`dis = {S.dis[S.nxt]}`）→ ==定下它的最短距离==，下一步从它扩展',
        'res += dis[super_t]': '`SS → TT` 的最短费用 `dis[TT] = {dis[super_t]}`，这一路流量 1 → `res = {res}`',
        'now = super_t': lambda S, B, r: '沿 `prev` 从 `TT` 倒着走回 `SS`：' + ' → '.join(_nm(S, x) for x in _chain(S)) + '，路径上每条边容量 −1、反向边 +1（可反悔）',
        'return res': '没有增广路了 → 最小费用 `res` = =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='「每个点至少连一次」就是流量有下限，改图后跑最小费用流',
        complexity='多项式：每轮找路 `O(V²)`，增广轮数不超过 `O(m+n)`，空间 `O(V²)`，`V = m + n + 4`',
        problem=['两组点，`cost[i][j]` 是点 `i` 和点 `j` 的连接成本，保证 ==左组点数 ≥ 右组==',
                 '两组的每个点都至少连一条边，求最小总成本',
                 '示例：`[[1,3,5],[4,1,1],[1,5,3]]` → `4`'],
        quote='按题目的规模来看，可能是想要给出一种状态压缩动态规划的解法，不过还存在效率高得多的做法，也就是网络流。',
        quote_src='—— yiduobo 题解原文',
        idea=['左点的流量范围 `[1, n]`，右点 `[1, m]`；左右之间的边容量 1、费用 `cost`',
              '源汇相连的边费用 0，流量下限用超级源汇 `SS/TT` 变形掉',
              '变形后是普通最小费用最大流：每轮找最短路增广，累加费用'],
        result='3 轮增广，最小成本 4',
        summary=['原文已是 Python 3 可运行写法；仅把变量 `next` 改名 `nxt`',
                 '最短路里可能出现负费用（反向边），所以用「可撤销已定点」的 SPFA 式写法',
                 '灵神用状压 DP `O(nm·2^m)`；这里是网络流，规模大时更快',
                 '易错：流量下限变形时的几条平衡边，容量写错整个图就错了',
                 '本视频用 3×3 示例，共 3 轮增广'],
    ),
)
