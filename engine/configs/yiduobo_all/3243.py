def _edges(S):
    g = S.get('g')
    if g is None or 'x' not in S:
        return ''
    return f"新增道路 `{S['x']} → {S['y']}`；当前出边：" + '，'.join(f'`{i}→{v}`' for i, vs in enumerate(g) for v in vs if v != i + 1)


CONFIG = dict(
    num=3243, title='新增道路查询后的最短距离 I', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='每次加边后暴力 BFS',
    tags=['灵神题单·图论算法', '灵神题单·动态规划', '难度分 1568'],
    code='''
class Solution(object):
    def shortestDistanceAfterQueries(self, n, queries):

        g = [[] for _ in range(n)]
        for index in range(n - 1):
            g[index].append(index + 1)
        
        res = []
        for x, y in queries:
            g[x].append(y)
            q = [0]
            dis = [None] * n
            dis[0] = 0
            head, tail = 0, 1
            while head < tail:
                for now in q[head : tail]:
                    for nxt in g[now]:
                        if dis[nxt] is None:
                            dis[nxt] = dis[now] + 1
                            q.append(nxt)
                
                head, tail = tail, len(q)
            
            res.append(dis[n - 1])
        
        return res
''',
    call='Solution().shortestDistanceAfterQueries(5, [[1,3],[0,4]])',
    expect=[3, 1],
    views=[
        dict(type='text', fn=_edges, size=26, h=70),
        dict(type='array', var='dis', label='dis[i]：0 到 i 的最少步数（None=还没到过，蓝=当前点）', cell=100, h=230,
             pointers={'now': 'blue'},
             color=lambda S, i, v: 'green' if v is not None else None),
        dict(type='array', var='q', label='q（BFS 队列，head~tail 是这一轮要处理的点）', cell=80, h=170,
             pointers={'head': 'blue', 'tail': 'pink'}),
        dict(type='array', var='res', label='res（每次加边后的答案）', cell=100, h=170, color=lambda S, i, v: 'green'),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'now', 'nxt', ('head', 'head', 'blue'), ('tail', 'tail', 'pink')],
    max_steps=130,
    skip=['dis[0] = 0', 'head, tail = 0, 1', 'for index in range', 'g[index].append'],
    captions={
        'g = [[]': '`g[i]` 存 `i` 能直接走到的点（邻接表），再补上原始道路 `i → i+1`',
        'res = []': '`res` 存每次加边后的答案',
        'for x, y in queries': lambda S, B, ret: (f'新增一条道路 `{S.x} → {S.y}`，之后重新跑一遍 BFS' if (B.get('x'), B.get('y')) != (S.x, S.y) or 'res' not in B or len(S.res) == len(B.res) and not S.res else '所有查询都处理完了'),
        'g[x].append(y)': '把新边加进图：`g[{x}] = {g[x]}`',
        'q = [0]': '每次都从 0 号城市重新出发：队列 `[0]`，`dis[0] = 0`，`q[head:tail]` 是同一步数的一轮点',
        'dis = [None]': '`dis` 全部清空，表示谁都还没走到过',
        'dis[0] = 0': '起点 0 到自己是 0 步',
        'head, tail = 0, 1': '`q[head:tail]` 是当前这一轮（同一步数）的点',
        'for now in q[head': '这一轮的点：`{q[head:tail]}`，逐个处理',
        'for nxt in g[now]': '看点 `{now}` 的所有出边：`{g[now]}`',
        'while head < tail': lambda S, B, ret: ('这一轮还有点要处理' if S.head < S.tail else '队列走完，BFS 结束'),
        'if dis[nxt] is None': lambda S, B, ret: (f'`{S.nxt}` 没到过 → ==第一次到达就是最短==' if S.dis[S.nxt] is None
                                                  else f'`{S.nxt}` 已经到过（`dis = {S.dis[S.nxt]}`）→ 不用再走'),
        'dis[nxt] = dis[now] + 1': '`dis[{nxt}] = dis[{now}] + 1` = =={dis[nxt]}==',
        'q.append(nxt)': '`{nxt}` 入队：`q = {q}`',
        'head, tail = tail, len(q)': '这一轮结束，下一轮从 `{head}` 到 `{tail}`（步数加一）',
        'res.append(dis[n - 1])': '本次加边后 0 到 `{n-1}` 的最短路是 `{dis[n-1]}`',
        'return res': '全部查询完成：`{res}`',
    },
    cards=dict(
        one_liner='数据小，每加一条边就重新 BFS 一遍',
        complexity='时间 `O(q(n+q))`，空间 `O(n+q)`',
        problem=['`n` 个城市，`i → i+1` 有单向路；每次查询新增一条单向路 `u → v`',
                 '每次加边后求 `0 → n-1` 的最短路长度',
                 '示例：`n=5, [[2,4],[0,2],[0,4]]` → `[3,2,1]`',
                 '本视频：`n=5, [[1,3],[0,4]]` → `[3,1]`'],
        quote='题目中n和queries的规模都很小，因此可以直接暴力计算。……新增一条u[i]到v[i]的边，然后从0号节点开始做bfs，记录到达n - 1所需的轮次。',
        quote_src='—— yiduobo 题解原文',
        idea=['先建图：只有 `i → i+1` 的边', '每个查询：加边 → 从 0 开始 BFS，`dis` 记录步数',
              '边没有权重，BFS 第一次到达 `n-1` 的步数就是最短路'],
        summary=['时间 `O(q(n+q))`，空间 `O(n+q)`',
                 '易错：每次查询都要重新建 `dis` 和队列，不能沿用上一次的',
                 '`q[head:tail]` 一轮一轮扩展，所以 `dis[now] + 1` 就是步数',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神方法二用 DP 只更新受影响的点；这里是最直接的暴力'],
    ),
)
