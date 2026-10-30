CONFIG = dict(
    num=2093, title='前往目的城市的最小费用', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='分层图 Dijkstra',
    tags=[],
    code='''
class Solution(object):
    def minimumCost(self, n, highways, discounts):

        g = {index : {} for index in range(n)}
        for x, y, t in highways:
            g[x][y] = t
            g[y][x] = t

        dis = [[-1] * (discounts + 1) for _ in range(n)]

        heap = [[0, 0, 0]]
        while heap:
            d, now, level = heapq.heappop(heap)
            if dis[now][level] == -1:
                dis[now][level] = d
                if now == n - 1:
                    return d

                for next in g[now]:
                    if dis[next][level] == -1:
                        heapq.heappush(heap, [d + g[now][next], next, level])
                    if level < discounts and dis[next][level + 1] == -1:
                        heapq.heappush(heap, [d + g[now][next] // 2, next, level + 1])

        return -1
''',
    call='Solution().minimumCost(5, [[0,1,4],[2,1,3],[1,4,11],[3,2,3],[3,4,2]], 1)',
    expect=9,
    views=[
        dict(type='text', fn=lambda S: (f"弹出 `({S['d']}, 城市{S['now']}, 第{S['level']}层)`：到城市 {S['now']} 已用 {S['level']} 次折扣，费用 =={S['d']}==" if 'level' in S else '')),
        dict(type='table', var='dis', label='dis[城市][用了几次折扣]（-1 = 还没定下来，绿 = 已定）', h=300, cell=90,
             rows=lambda S: [f'城市{i}' for i in range(len(S['dis']))],
             cols=lambda S: [f'折扣{j}' for j in range(len(S['dis'][0]))],
             cursors=[('now', 'level', 'yellow', '')],
             color=lambda S, i, j, v: 'green' if v != -1 else None),
        dict(type='heap', var='heap', label='堆：费用/城市/折扣数', h=240,
             fmt=lambda x: f'{x[0]}/c{x[1]}/L{x[2]}'),
    ],
    skip=['g[y][x] = t', 'heapq.heappush'],
    max_steps=60,
    watch=[('d', 'd', 'blue'), ('now', 'now', 'yellow'), ('level', 'level', 'pink'), 'discounts'],
    captions={
        'g = {index': '邻接表：`g[x]` 是 {{邻居: 过路费}} 的字典',
        'g[x][y] = t': '无向边：`g[{x}][{y}] = g[{y}][{x}] = {t}`',
        'dis = [[-1]': '`dis[i][level]`：到城市 i、==恰好用了 level 次折扣==的最小费用。多了一维，就是分层图',
        'heap = [[0, 0, 0]]': '起点：城市 0，费用 0，用了 0 次折扣',
        'while heap': '堆里还有候选状态 → 取费用最小的出来',
        'heapq.heappop': '弹出费用最小的状态：城市 `{now}`，第 `{level}` 层，费用 `{d}`',
        'if dis[now][level] == -1': lambda S, B, r: (f'`dis[{S.now}][{S.level}]` 还是 -1 → 这是该状态第一次弹出，费用 {S.d} 就是最小的' if S.dis[S.now][S.level] == -1
                                                    else f'`dis[{S.now}][{S.level}]` 已有值 → 旧状态，跳过'),
        'dis[now][level] = d': '定下来：`dis[{now}][{level}] = {d}`（Dijkstra：第一次出堆即最优）',
        'if now == n - 1': lambda S, B, r: (f'到达终点城市 {S.now}，最小费用 =={S.d}==' if S.now == S.n - 1 else f'城市 {S.now} 不是终点 {S.n - 1}，继续扩展'),
        'for next in g[now]': '枚举城市 `{now}` 的邻居 `{next}`，两种走法：原价 / 打折',
        'if dis[next][level] == -1': '原价走到 `{next}`（仍在第 `{level}` 层）：该状态未定 → 费用 `{d} + {g[now][next]}` 入堆',
        'level < discounts': lambda S, B, r: (f'还剩折扣（已用 {S.level} / {S.discounts}），且下一层 `dis[{S.next}][{S.level + 1}]` 未定 → 打折走到下一层，费用 `{S.d} + {S.g[S.now][S.next]}//2` 入堆'
                                              if S.level < S.discounts and S.dis[S.next][S.level + 1] == -1 else
                                              '折扣用完或下一层已定 → 不能打折'),
        'return -1': '堆空了仍没到终点 → 不可达，返回 -1',
    },
    cards=dict(
        one_liner='把「用了几次折扣」放进状态：一维变二维的 Dijkstra',
        complexity='时间 `O(m·k·log(m·k))`，空间 `O(n·k)`（k = discounts）',
        problem=['无向图，边权是过路费；至多可以对 `discounts` 条边打五折（过路费取一半）',
                 '求从城市 0 到城市 n−1 的最小总费用，到不了返回 `-1`',
                 '示例：`n=5`，`discounts=1` → `9`'],
        quote='将折扣使用的次数加入到最短路的状态表示中，也就是将dis[i]表示到达城市i的最小费用，升级成dis[i][level]表示到达城市i，使用了level次折扣的最小费用。',
        quote_src='—— yiduobo 题解原文',
        idea=['每条边视作两条：原价边留在同层，折扣边通向下一层',
              '图上多了 `discounts+1` 层，不用真的建图，状态里带上 `level` 即可',
              '之后就是普通 Dijkstra：首次出堆的状态费用最小，遇到终点直接返回'],
        summary=['时间 `O(m·k·log(m·k))`，空间 `O(n·k)`',
                 '易错：折扣边要判断 `level < discounts`，且去往的是 `level + 1` 层',
                 '终点在任何一层首次出堆就能返回，不必取各层最小值（堆保证最小优先）',
                 '原文为 Python 2 写法，折扣费用 `/ 2` 已改为整数除法 `// 2`',
                 '同类：灵神题单「分层图最短路」，状态多一维就套 Dijkstra'],
    ),
)
