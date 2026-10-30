CONFIG = dict(
    num=815, title='公交路线', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='按轮次 BFS，用集合管理未用线路/未到车站', tags=['灵神题单', '广度优先搜索', '难度分 1964'],
    code='''
class Solution:
    def numBusesToDestination(self, routes, S, T):

        if S == T:
            return 0

        n = len(routes)
        unuse_route_set = set(range(n))
        unreach_set = set()
        route_dict = {}
        for index, route in enumerate(routes):
            for num in route:
                unreach_set.add(num)
                if num not in route_dict:
                    route_dict[num] = set()
                route_dict[num].add(index)
        
        unreach_set.add(T)
        unreach_set.remove(S)
        q = [S]
        l = 0
        r = 1
        res = 0
        while l < r:
            res += 1
            for index in range(l, r):
                now = q[index]
                if now not in route_dict:
                    continue
                for route in route_dict[now]:
                    if route not in unuse_route_set:
                        continue
                    unuse_route_set.remove(route)
                    for num in routes[route]:
                        if num == T:
                            return res
                        if num in unreach_set:
                            unreach_set.remove(num)
                            q.append(num)
            l, r = r, len(q)
        
        return -1
''',
    call='Solution().numBusesToDestination([[1,2,7],[3,6,7],[4,5,9]], 1, 6)',
    expect=2,
    views=[
        dict(type='map', var=lambda S: {k: sorted(v) for k, v in S['route_dict'].items()} if 'route_dict' in S else None, label='route_dict：车站 → 可乘的线路', fmt=lambda k, v: f'站{k}: 线{v}', font=20, h=120),
        dict(type='set', var=lambda S: S['unuse_route_set'] if 'unuse_route_set' in S else None, label='unuse_route_set：还没乘过的线路', fmt=lambda x: f'线{x}', h=90),
        dict(type='set', var=lambda S: S['unreach_set'] if 'unreach_set' in S else None, label='unreach_set：还没入队的车站', fmt=lambda x: str(x), h=90),
        dict(type='array', var=lambda S: S['q'] if 'l' in S and 'q' in S else None, label='BFS 队列 q（车站）', window=('l', 'r - 1'), h=140),
    ],
    watch=[('轮次 res', 'res', 'green'), 'now', 'route', 'num', 'l', 'r'],
    captions={
        'unreach_set.add(T)': '终点 T={T} 也放进 unreach_set：保证它被当成“还没到”的站',
        'unreach_set.remove(S)': '起点 {S} 已经在队里，从 unreach_set 里去掉',
        'q = [S]': '起点入队：第 0 轮只有车站 `{S}`',
        'res += 1': '新一轮：从队里这批车站出发，再多乘一辆车 → `res = {res}`',
        'now = q[index]': '取出车站 `{now}`，看哪些线路经过它',
        'if now not in route_dict': lambda S, B, ret: (f"车站 {S['now']} 没有线路经过，跳过" if S['now'] not in S['route_dict'] else f"车站 {S['now']} 有线路 {sorted(S['route_dict'][S['now']])}"),
        'if route not in unuse_route_set': lambda S, B, ret: (f"线 {S['route']} 还没乘过，可以上车" if S['route'] in S['unuse_route_set'] else f"线 {S['route']} 已经乘过，==它上面的车站早都入队了==，跳过"),
        'unuse_route_set.remove': '乘上线 {route}，从未用集合里删掉：==每条线路只乘一次==',
        'if num == T': lambda S, B, ret: (f"到站 {S['num']} 就是终点！这轮 res = =={S['res']}== 辆车，直接返回" if S['num'] == S['T'] else f"站 {S['num']} 不是终点 {S['T']}"),
        'if num in unreach_set': lambda S, B, ret: (f"站 {S['num']} 还没入队，是新到的车站" if S['num'] in S['unreach_set'] else f"站 {S['num']} 以前到过，不重复入队"),
        'q.append(num)': '车站 {num} 入队，下一轮从这里换乘',
        'l, r = r, len(q)': '这一轮结束：下一轮处理 `q[{l}:{r}]` 新入队的车站',
        'return -1': 'BFS 走完仍没碰到终点，到不了：返回 -1',
    },
    skip=['n = len(routes)', 'unuse_route_set = set(range', 'unreach_set = set()', 'route_dict = {}', 'for index, route in enumerate', 12, 'unreach_set.add(num)', 'if num not in route_dict', 'route_dict[num] = set()', 'route_dict[num].add', 'l = 0', 'r = 1', 'res = 0', 'continue'],
    max_steps=80,
    cards=dict(
        one_liner='每一轮 BFS 多乘一辆车：线路和车站都只用一次',
        complexity='时间 `O(S)`，空间 `O(S)`（S 为线路长度之和）',
        problem=['`routes[i]` 是第 `i` 辆公交的循环路线，从 `S` 出发去 `T`',
                 '只能乘公交，求最少乘坐的公交车数量，到不了返回 `-1`',
                 '示例：`[[1,2,7],[3,6,7],[4,5,9]]`，1 → 6 → `2`'],
        quote='题目要求最少的换乘次数，那么很自然想到了bfs。对于当前处理的节点now，我们遍历还没有使用过的公交路线，对于这些公交路线上的所有车站，若该车站还没有加入到bfs队列中，则将其加入到队列中。',
        quote_src='—— yiduobo 题解',
        idea=['`route_dict` 记录每个车站能乘哪些线路',
              '`unuse_route_set` / `unreach_set` 记录没用过的线路和没入队的车站',
              '每轮 `res += 1`；扫线路时发现终点，当轮 `res` 就是答案'],
        summary=['时间 `O(S)`：每条线路只乘一次，每个车站只入队一次',
                 '==先判 `S == T` 返回 0==，否则起点会被误当成要到达的站',
                 '终点 `T` 要提前放进 `unreach_set`，否则无线路经过的情况不好处理',
                 '原文为 Python 2 写法，本题无需改动，可直接在 Python 3 运行'],
    ),
)
