def _names(S):
    m, ma = S['m'], S['ma']
    return [f'行{i}' for i in range(m)] + ['S'] + [f'值{j}' for j in range(1, ma + 1)] + ['T']


def _nm(S, x):
    m, ma = S['m'], S['ma']
    return f'行{x}' if x < m else 'S' if x == m else 'T' if x == m + ma + 1 else f'值{x - m}'


def _path(S):
    if 'prev' not in S or S['dis'][S['t']] is None:
        return set()
    p, now, out = S['prev'], S['t'], set()
    while now is not None and now != S['s']:
        out.add((p[now], now))
        now = p[now]
    return out


def _cc(S, r, c, v):
    if 'dis' not in S or 'prev' not in S:
        return 'green' if v > 0 and False else None
    if S['t'] in S.get('used', ()) and (r, c) in _path(S):
        return 'yellow'
    if v > 0:
        return 'blue' if r == S.get('now') else None
    return None


def _txt(S):
    if 'dis' not in S:
        return '把「每行选一个、每个数值只用一次」建成流网络：流量 = 选了几个数，费用 = ma − 数值'
    return f"黄 = 刚找到的增广路；累计得分 `res = {S.get('res', 0)}`"


CONFIG = dict(
    num=3276, title='选择矩阵中单元格的最大得分', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='最小费用最大流（SPFA 式找增广路）',
    tags=['网络流', '其他状压 DP', '难度分 2403'],
    code='''
class Solution(object):
    def maxScore(self, grid):

        m = len(grid)
        n = len(grid[0])

        ma = 0
        for i in range(m):
            for j in range(n):
                ma = max(ma, grid[i][j])
        
        s = m
        t = m + ma + 1

        c = [[0] * (t + 1) for _ in range(t + 1)]
        cost = [[0] * (t + 1) for _ in range(t + 1)]
        
        for i in range(m):
            c[s][i] = 1
        
        for j in range(m + 1, m + ma + 1):
            c[j][t] = 1
        
        for i in range(m):
            for j in range(n):
                c[i][m + grid[i][j]] = 1
                cost[i][m + grid[i][j]] = ma - grid[i][j]
                cost[m + grid[i][j]][i] = grid[i][j] - ma

        res = 0
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                nxt = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + cost[now][index]):
                        dis[index] = dis[now] + cost[now][index]
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

            res += ma - dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]
''',
    call='Solution().maxScore([[1,2,3],[4,3,2],[1,1,1]])',
    expect=8,
    views=[
        dict(type='table', var='c', label='容量矩阵 c[u][v]（1 = 还有容量；蓝 = 当前结点的出边）', h=400, cell=44,
             rows=_names, cols=_names, color=_cc),
        dict(type='array', var='dis', label='dis（到各点的最短费用，None = 还没到过）', h=130, cell=56),
        dict(type='text', fn=_txt, size=24, h=60),
    ],
    watch=[('now', 'now', 'blue'), ('nxt', 'nxt', 'pink'), ('res', 'res', 'green'), ('ma', 'ma', 'yellow')],
    skip=['for i in range(m)', 'for j in range(n)', 'for j in range(m + 1', 'for index in range', 'c[s][i] = 1',
          'c[j][t] = 1', 'cost[i][m', 'cost[m + grid', 'ma = max', 'min_dis = None', 'nxt = None', 'if c[now][index]',
          'dis[index] = dis[now]', 'prev[index] = now', 'if index in used', 'used.remove', 'if index not in used',
          'nxt = index', 'min_dis = dis[index]', 'n = len', 'while True', 'prev = [None]', 'used = set', 'dis[s] = 0',
          'now = s', 'while t not in used', 'cost = [[0]', 'now = nxt', 'now = t', 'while now != s', 'now = prev[now]',
          'c[now][prev[now]] += 1', 'if min_dis is None', 'prev = [None]', 'used = set'],
    captions={
        'm = len(grid)': '行数 `m = {m}`：每一行是一个点',
        'ma = 0': '`ma`：矩阵里的最大值，用来把「最大化得分」改成「最小化费用」',
        's = m': '源点 `s = {s}`（编号紧跟在各行之后）',
        't = m + ma + 1': '汇点 `t = {t}`；编号 `m+1 .. m+ma` 是==数值 1..ma 各一个点==',
        'c = [[0]': '`c[u][v]` 是容量矩阵（共 `{t+1}` 个点）。建边：源点→每行、每行→它含有的数值、数值→汇点，容量都是 1',
        'c[i][m + grid[i][j]] = 1': '第 `{i}` 行含有数值 `{grid[i][j]}` → 连边 行{i} → 值{grid[i][j]}，费用 `ma − {grid[i][j]}` = {ma - grid[i][j]}',
        'res = 0': '图建好：源点→行（每行至多选一个）、行→数值（费用 `ma − 数值`）、数值→汇点（每个数值只能选一次）',
        'dis = [None]': '新一轮：重新初始化 `dis` 找下一条增广路（从源点 `S` 出发）',
        'min_dis is None': lambda S, B, r: ('找不到新的点可扩展 → 没有增广路了，返回 `res`' if S.min_dis is None else '还有可扩展的点，继续找最短路'),
        'used.add(nxt)': lambda S, B, r: f'未定的点里 `dis` 最小的是 `{_nm(S, S.nxt)}`（`dis = {S.dis[S.nxt]}`）→ ==定下它的最短距离==，下一步从它扩展',
        'res += ma - dis[t]': '找到一条 S→T 的最短费用路：`dis[t] = {dis[t]}`，选到的数值 = `ma − 费用` = {ma - dis[t]} → `res = {res}`',
        'c[prev[now]][now] -= 1': lambda S, B, r: f'沿 `prev` 从汇点往回走：边 `{_nm(S, S.prev[S.now])} → {_nm(S, S.now)}` 容量 −1，反向边容量 +1（留后路，可反悔）',
        'return res': '再也找不到增广路 → 最大流已满，最大得分 `res` = =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='把每行、每个数值都建成点，用费用流选出尽量多、尽量大的数',
        complexity='时间约 `O(m · V²)`（每次 `V²` 找路，至多 `m` 次），空间 `O(V²)`，`V = m + max + 2`',
        problem=['矩阵 `grid`，选一个或多个格子：==每行至多一个，选中的值互不相同==',
                 '得分是所选值之和，求最大得分',
                 '示例：`[[1,2,3],[4,3,2],[1,1,1]]` → `8`'],
        quote='应该选择尽量多的单元格，即可以使用最大流相关的算法来解决这个问题。……有了这个前提，就可以使用费用流来求解了。',
        quote_src='—— yiduobo 题解原文',
        idea=['行点各有一条容量 1 的入边，数值点各有一条容量 1 的出边 → ==一行一个、一个值一次==',
              '边费用 `ma − 数值`：费用越小，选的数越大；最小费用 = 得分最大',
              '答案 = 流量 × `ma` − 最小费用；每次增广等价于多选一个数'],
        result='3 次增广，最大得分 8',
        summary=['原文已是 Python 3 可运行写法；为避开内置函数，仅把变量 `next` 改名 `nxt`',
                 '「尽量多选」成立：数都是正数，能多选一个就不亏',
                 '每次找最短路后，沿 `prev` 回溯更新容量，并加反向边（可反悔）',
                 '本视频用 `[[1,2,3],[4,3,2],[1,1,1]]`，共 3 次增广',
                 '灵神是状压记忆化 `O(mn·2^m)`；这里是多项式的网络流做法'],
    ),
)
