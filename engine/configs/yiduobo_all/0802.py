GRAPH = [[1], [0], [3], [], [2]]


def _orig(S):
    g = S.get('graph')
    if g is None:
        return ''
    return '原图（有向边 x → y）：' + '　'.join(f'`{x}`→{v}' for x, v in enumerate(g))


CONFIG = dict(
    num=802, title='找到最终的安全状态', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='反向建图 · 拓扑排序',
    tags=['灵神题单·图论算法'],
    code='''
class Solution(object):
    def eventualSafeNodes(self, graph):

        n = len(graph)
        oud = [0] * n
        g = {}
        for x, next_list in enumerate(graph):
            for y in next_list:
                if y not in g:
                    g[y] = set()
                g[y].add(x)
                oud[x] += 1
        
        q = []
        for x in range(n):
            if oud[x] == 0:
                q.append(x)
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for prev in g.get(now, set()):
                oud[prev] -= 1
                if oud[prev] == 0:
                    q.append(prev)
                    r += 1
        
        res = []
        for x in range(n):
            if oud[x] == 0:
                res.append(x)
    
        return res
''',
    call=f'Solution().eventualSafeNodes({GRAPH!r})',
    expect=[2, 3, 4],
    views=[
        dict(type='text', fn=_orig, h=70, size=26),
        dict(type='map', var='g', label='g（反向边：y → 指向 y 的点集合）', fmt=lambda k, v: f'{k}: {sorted(v)}', h=150, font=26),
        dict(type='array', var='oud', label='oud（出度，0 = 安全）', h=170, pointers={'now': 'blue', 'x': 'yellow'},
             color=lambda S, i, v: 'green' if v == 0 else None),
        dict(type='array', var='q', label='q（队列，l 之前已处理）', h=170, pointers={'l': 'pink', 'r': 'orange'}),
    ],
    watch=[('now', 'now', 'blue'), ('prev', 'prev', 'pink'), ('l', 'l', 'pink'), ('r', 'r', 'orange'), ('res', 'res', 'green')],
    skip=['oud = [0]', 'g = {}', 'res = []', 'q = []', 'n = len', 'for y in next_list', 'if y not in g', 'g[y] = set()', 'for x, next_list', 'for x in range(n)', 'l = 0', 'r = len(q)'],
    captions={
        'for x, next_list': lambda S, B, ret: (f'点 `{S.x}` 的出边：`{S.next_list}`' if 'x' not in B or S.x != B.x else '反向图、出度都建好了'),
        'for y in next_list': lambda S, B, ret: f'边 `{S.x} → {S.y}`',
        'if y not in g': lambda S, B, ret: (f'`g` 里还没有 `{S.y}` → 先建空集合' if S.y not in S.g else f'`g[{S.y}]` 已有'),
        'g[y] = set()': '新建 `g[{y}]`',
        'g[y].add(x)': '边反向：`{y} ← {x}`，记入 `g[{y}] = {g[y]}`',
        'oud[x] += 1': '`{x}` 多一条出边 → `oud[{x}] = {oud[x]}`',
        'for x in range(n)': lambda S, B, ret: (f'检查点 `{S.x}` 出度是不是 0' if 'q' in S and S.x != B.get('x') else f'检查点 `{S.x}`'),
        'if oud[x] == 0': lambda S, B, ret: (
            (f'`oud[{S.x}] = 0`：没有出边，肯定安全 → ==拓扑起点==' if S.oud[S.x] == 0 else f'`oud[{S.x}] = {S.oud[S.x]}`：还有出边，不一定安全')
            if S._line < 30 else
            (f'`oud[{S.x}] = 0`：被拓扑排序扫到的安全点 → 收进答案' if S.oud[S.x] == 0 else f'`oud[{S.x}] = {S.oud[S.x]}`：在环上或通向环，不安全')),
        'q.append(x)': '`{x}` 入队：`q = {q}`',
        'l = 0': '`l` 指向队头',
        'r = len(q)': '`r = {r}`：队尾（不含）',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：队里还有没处理的安全点' if S.l < S.r else f'`l = {S.l} = r`：队空，扩展结束'),
        'now = q[l]': '取队头 `{now}`：它是安全点，看谁指向它',
        'l += 1': '`l` → {l}',
        'for prev in g.get': lambda S, B, ret: (f'`{S.now}` 没有前驱（没有点指向它），不用扩展' if not S.g.get(S.now)
                                                else f'`{S.now}` 的前驱都处理完了' if B._line in (26, 28)
                                                else f'`{S.prev}` 有边指向 `{S.now}`'),
        'oud[prev] -= 1': '`{prev}` 指向的安全点又多一个 → `oud[{prev}] = {oud[prev]}`',
        'if oud[prev] == 0': lambda S, B, ret: (f'`oud[{S.prev}] = 0`：它所有出边的终点都安全 → ==它也安全==' if S.oud[S.prev] == 0
                                                 else f'`oud[{S.prev}] = {S.oud[S.prev]}`：还有出边没确认安全，先等着'),
        'q.append(prev)': '`{prev}` 入队：`q = {q}`',
        'r += 1': '`r` → {r}',
        'for x in range(n):\n': '',
        'res.append(x)': '`{x}` 的 `oud` 为 0 → 加入答案 `{res}`',
        'return res': '按下标顺序返回安全点 `{res}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='反向建边做拓扑排序：出度归零的点就是安全点',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['有向图，从某点出发无论怎么走最终都到终点（出度 0）才叫==安全点==',
                 '要返回所有安全点，升序',
                 '本视频：`graph = [[1],[0],[3],[],[2]]` → `[2,3,4]`（0 和 1 成环）'],
        quote='若该节点的出度为0，或者以该节点为起点的所有边对应的终点要么出度为0，要么也满足这个性质，那么这个节点就不是环上的。',
        quote_src='—— yiduobo 题解原文',
        idea=['安全点 = 出度为 0，或所有后继都安全',
              '把边全部反向：出度变入度，正好是标准拓扑排序',
              '`oud` 减到 0 的点入队；最后 `oud == 0` 的就是答案'],
        summary=['时间 `O(n + m)`；`g` 存反向边，`oud` 存原图出度',
                 '队列用数组 `q` + 指针 `l / r` 实现，不用 deque',
                 '环上的点出度永远减不到 0，所以不会入队',
                 '最后按下标 `0..n-1` 收集，答案自然有序',
                 '原文代码在 Python 3 下无需改动'],
    ),
)
