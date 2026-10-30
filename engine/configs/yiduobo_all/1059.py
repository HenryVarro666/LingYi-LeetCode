CONFIG = dict(
    num=1059, title='从始点到终点的所有路径', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Tarjan 判环 + DFS',
    code='''
class Solution(object):
    def leadsToDestination(self, n, edges, source, destination):

        g = {}
        for x, y in edges:
            if x == destination:
                return False

            if x not in g:
                g[x] = set()
            if y not in g[x]:
                g[x].add(y)

        dfn = [None] * n
        low = [None] * n
        stack = []
        in_stack = set()
        global flag, vis_des, cnt
        flag = True
        vis_des = False
        cnt = 0

        def dfs(now):
            global flag, vis_des, cnt
            dfn[now] = low[now] = cnt
            cnt += 1
            stack.append(now)
            in_stack.add(now)

            if now not in g:
                if now == destination:
                    vis_des = True
                else:
                    flag = False
                    return
            else:
                for next in g.get(now, set()):
                    if now == next:
                        flag = False
                        return
                    if dfn[next] is None:
                        dfs(next)
                        if not flag:
                            return
                        low[now] = min(low[now], low[next])
                    elif next in in_stack:
                        low[now] = min(low[now], low[next])
            
            if dfn[now] == low[now]:
                if stack[-1] != now:
                    flag = False
                    return
                
                stack.pop()
                in_stack.remove(now)

        dfs(source)
        return flag and vis_des
''',
    call='Solution().leadsToDestination(3, [[0,1],[0,2],[1,2]], 0, 2)',
    expect=True,
    views=[
        dict(type='map', var='g', fmt=lambda k, v: f'→ {sorted(v)}', label='g：点 → 出边终点', h=180),
        dict(type='array', var='dfn', label='dfn（访问时间）', h=130),
        dict(type='array', var='low', label='low（能回溯到的最早时间）', h=130),
        dict(type='stack', var='stack', fmt=lambda x: str(x), h=150),
        dict(type='calls', h=200),
    ],
    watch=['now', 'in_stack'],
    max_steps=110,
    captions={
        'if x == destination': lambda S, B, r: f'边 `{S.x}→{S.y}`：起点是 destination？' + ('是 → 终点还有出边，直接 `False`' if S.x == S.destination else '否，继续'),
        'dfn[now] = low[now] = cnt': '第一次到达 `{now}`：`dfn = low = {dfn[now]}`（访问时间）',
        'stack.append': '`{now}` 入栈，表示正在这条路径上',
        'if now not in g': lambda S, B, r: (f'`{S.now}` 没有出边：' + ('正好是 destination → 记下 `vis_des = True`' if S.now == S.destination else '却不是 destination → 路径卡死，`flag = False`')) if S.now not in S.g else f'`{S.now}` 还有出边，继续往下走',
        'if now == next': '沿出边 `{now}` → `{next}`：是自环吗？`{now} == {next}` → 否',
        'if not flag': '子调用返回后检查：若里面已把 `flag` 置为 False（有环或死路），就一路 return 上去',
        'if dfn[next] is None': lambda S, B, r: (f'`{S.next}` 还没访问过 → 递归进入' if S['dfn'][S.next] is None else f'`{S.next}` 已访问过，看它是否还在栈里'),
        'low[now] = min(low[now], low[next])': '回溯更新：`low[{now}] = {low[now]}`',
        'if dfn[now] == low[now]': lambda S, B, r: f'`dfn[{S.now}] = {S.dfn[S.now]}`，`low[{S.now}] = {S.low[S.now]}`：' + ('相等 → 它是一个强连通分量的根' if S.dfn[S.now] == S.low[S.now] else '不等 → 还连着更早的点'),
        'if stack[-1] != now': lambda S, B, r: ('栈顶是 `{0}` 自己 → 这个强连通分量只有它一个点，没有环'.format(S.now) if S.stack[-1] == S.now else f'栈顶是 `{S.stack[-1]}` 而不是 `{S.now}` → 分量里不止一个点，==有环==，`flag = False`'),
        'stack.pop()': '出栈：`{now}` 处理完毕',
        'return flag and vis_des': '`flag`（无环、无死路）与 `vis_des`（到过终点）都为真 → =={ret}==',
    },
    cards=dict(
        one_liner='从起点跑一遍 Tarjan：有环、死路、没到终点都不行',
        complexity='时间 `O(n + e)`，空间 `O(n + e)`',
        problem=['有向图，给定 `source` 和 `destination`',
                 '判断从 `source` 出发的==所有==路径是否都在 `destination` 结束',
                 '示例：`n=3, edges=[[0,1],[0,2],[1,2]], 0 → 2` → `true`'],
        quote='从source出发的路径中存在环，包括自环。这里需要特别注意的是，不是从source出发的路径中存在环并不会影响最终结果，这也就意味着不能直接从source开始进行拓扑排序来判环，而是需要从source开始执行tarjan算法',
        quote_src='—— yiduobo 题解原文',
        idea=['先排除：destination 有出边 → 它不可能是路径终点',
              '三种失败：从起点可达的环（含自环）、在非终点处卡死、路径没经过终点',
              '用 Tarjan 的 `dfn/low`：`dfn == low` 但栈顶不是自己，说明强连通分量不止一点，有环'],
        summary=['时间 `O(n + e)`，空间 `O(n + e)`',
                 '易错点：只检查从 `source` 可达的部分，其他位置的环不影响答案',
                 '`dfs` 里要用 `global` 修改 `flag / vis_des / cnt`',
                 '原文没有 Python 2 专属语法，代码照搬，仅加了示例输入'],
    ),
)
