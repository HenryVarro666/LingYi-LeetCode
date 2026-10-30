CONFIG = dict(
    num=815, title='公交路线', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='以公交线路为边的 BFS', tags=['灵神题单', '广度优先搜索', '难度分 1964'],
    code='''
class Solution:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:
        # 记录经过车站 x 的公交车编号
        stop_to_buses = defaultdict(list)
        for i, route in enumerate(routes):
            for x in route:
                stop_to_buses[x].append(i)

        # 小优化：如果没有公交车经过起点或终点，直接返回
        if source not in stop_to_buses or target not in stop_to_buses:
            # 注意原地 TP 的情况
            return -1 if source != target else 0

        # BFS
        dis = {source: 0}
        q = deque([source])
        while q:
            x = q.popleft()  # 当前在车站 x
            dis_x = dis[x]
            for i in stop_to_buses[x]:  # 遍历所有经过车站 x 的公交车 i
                if routes[i]:
                    for y in routes[i]:  # 遍历公交车 i 的路线
                        if y not in dis:  # 没有访问过车站 y
                            dis[y] = dis_x + 1  # 从 x 站上车然后在 y 站下车
                            q.append(y)
                    routes[i] = None  # 标记 routes[i] 遍历过

        return dis.get(target, -1)
''',
    call='Solution().numBusesToDestination([[1,2,7],[3,6,7]], 1, 6)',
    expect=2,
    views=[
        dict(type='map', var=lambda S: dict(S['stop_to_buses']) if 'stop_to_buses' in S else None, label='stop_to_buses：车站 → 经过它的公交车', fmt=lambda k, v: f'站{k}: 车{v}', font=24, h=130),
        dict(type='map', var=lambda S: {i: r for i, r in enumerate(S['routes'])} if 'routes' in S else None, label='routes（None = 这条线路已遍历）', fmt=lambda k, v: f'车{k}: ' + ('已遍历' if v is None else str(v)), font=24, h=110),
        dict(type='map', var=lambda S: S['dis'] if 'dis' in S else None, label='dis：到各车站最少乘几辆车', fmt=lambda k, v: f'站{k}: {v}', font=26, h=110),
        dict(type='queue', var=lambda S: S['q'] if 'q' in S and 'dis' in S else None, label='队列 q（车站）', h=110),
    ],
    watch=['x', 'dis_x', 'i', 'y', ('target', 'target', 'green')],
    captions={
        'if source not in': '`stop_to_buses` 建好了：起点 {source}、终点 {target} 都有车经过，否则直接返回 -1（或原地 0）',
        'dis = {source: 0}': '起点还没上车，已乘 0 辆；==车站是节点，乘一辆车就是一条“边”，BFS 层数 = 乘车数==',
        'x = q.popleft()': '站在车站 `{x}`，已乘 `{dis[x]}` 辆车',
        'if routes[i]': lambda S, B, ret: (f"车 {S['i']} 的线路还没遍历，上车" if S['routes'][S['i']] else f"车 {S['i']} 的线路已经遍历过（None），它能到的站早都入队了，跳过"),
        'if y not in dis': lambda S, B, ret: (f"车站 {S['y']} 还没到过，可以入队" if S['y'] not in S['dis'] else f"车站 {S['y']} 已在 dis 里（更早到过），==不重复入队=="),
        'dis[y] = dis_x + 1': '在 {x} 站上车、{y} 站下车：多乘一辆，`dis[{y}] = {dis_x} + 1 = {dis[y]}`',
        'routes[i] = None': '车 {i} 的整条线路都走完了：置为 None，==每条线路只遍历一次==，不会再重复扫',
        'return dis.get': '`dis.get({target}, -1)` = =={ret}==：到终点最少乘 {ret} 辆车',
    },
    skip=['stop_to_buses = defaultdict', 'for i, route in enumerate', 'for x in route', 'stop_to_buses[x].append', 'dis_x = dis[x]'],
    max_steps=80,
    cards=dict(
        one_liner='车站当节点，乘一辆车 = 一层：BFS 的层数就是乘车数',
        complexity='时间 `O(S)`，空间 `O(S)`（S 为所有线路长度之和）',
        problem=['`routes[i]` 是第 `i` 辆公交的循环路线，从 `source` 出发到 `target`',
                 '只能乘公交车，求==最少乘坐的公交车数量==，到不了返回 `-1`',
                 '示例：`[[1,2,7],[3,6,7]]`，1 → 6 → `2`（先 1→7，再换乘去 6）'],
        quote='在 BFS 中，如何保证每辆公交车的路线只遍历一次？更简单的办法是，当公交车路线 routes[i] 遍历结束后，把 routes[i] 置为空。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用哈希表 `stop_to_buses` 记下每个车站有哪些车经过',
              '从起点开始 BFS：在车站 x 上车，这辆车路线上所有没到过的站，距离都是 `dis[x] + 1`',
              '用 `dis` 判断车站是否入队过，用 `routes[i] = None` 保证每条线路只扫一遍'],
        summary=['时间 `O(S)`：每条线路至多遍历一次，每个车站至多入队一次',
                 '==起点等于终点时答案是 0==，所以要先处理“原地 TP”',
                 '没有车经过起点或终点，直接返回 -1（或 0）',
                 '思考题：记录乘车序列，需要在 `dis` 之外再存前驱线路'],
    ),
)
